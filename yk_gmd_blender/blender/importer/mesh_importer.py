from typing import Union, List, Dict, cast, Tuple, Set

import bmesh
from mathutils import Matrix, Vector
from yk_gmd_blender.blender.common import AttribSetLayerNames, AttribSetLayers_bmesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import BoneWeight, GMDVertexBuffer_Skinned, GMDVertexBuffer_Generic
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter


def make_bone_indices_consistent(
        gmd_meshes: List[GMDSkinnedMesh],
        vertices: List[GMDVertexBuffer_Skinned]
) -> List[GMDBone]:
    """
    Mutate a list of vertex buffers, so that all of the bone indices are consistent
    i.e. vertices in different buffers use the same indices to refer to the same bones.
    Mutates the list of vertex buffers, but makes copies of the buffers themselves before changing them.
    Returns the overall list of bones.

    :param gmd_meshes:
    :param vertices:
    :return:
    """

    # Fix up bone mappings if the meshes are skinned

    # Build a list of references bones
    # All vertex buffers will have their data remapped to indexes into this list.
    # Start from the first mesh's bone list, then grow from there
    relevant_bones = gmd_meshes[0].relevant_bones[:]
    # The first mesh doesn't need remapping, because we start from its bone list, but subsequent ones do
    for i_mesh in range(1, len(gmd_meshes)):
        gmd_mesh = gmd_meshes[i_mesh]

        # Mapping of gmd_meshes[i] bone indices to relevant_bones indices
        bone_index_mapping = {}
        for i, bone in enumerate(gmd_mesh.relevant_bones):
            if bone not in relevant_bones:
                relevant_bones.append(bone)
            bone_index_mapping[i] = relevant_bones.index(bone)

        def remap_weight(bone_weight: BoneWeight):
            # If the weight is 0 the bone is unused, so map it to a consistent 0.
            if bone_weight.weight == 0:
                return BoneWeight(0, weight=0.0)
            else:
                return BoneWeight(bone_index_mapping[bone_weight.bone], bone_weight.weight)

        # Turn the vertices into a copy instead of a reference
        vertices[i_mesh] = vertices[i_mesh][:]
        verts_to_remap = vertices[i_mesh]
        # Remap the bones in the vertices
        for i_vtx in range(len(verts_to_remap)):
            old_weights = verts_to_remap.bone_weights[i_vtx]
            verts_to_remap.bone_weights[i_vtx] = (
                remap_weight(old_weights[0]),
                remap_weight(old_weights[1]),
                remap_weight(old_weights[2]),
                remap_weight(old_weights[3]),
            )

    # Done, return the full list of relevant bones.
    return relevant_bones


def vertex_fusion(vertices: List[GMDVertexBuffer_Generic]) -> Tuple[List[List[int]], List[List[bool]]]:
    """
    Applies "vertex fusion" to a set of vertex buffers, returning a list of which vertices were "fused"
    and a mapping of (i_buf, i_vertex_in_buf) to fused index.

    Fuses "adjacent" vertices, where adjacent vertices have the same
    - position
    - normal
    - bone mapping
    - weight mapping

    :param vertices:
    :return:
    """

    vert_indices: Dict[Tuple[Vector, Vector, Vector, Vector], int] = {}
    # fused_idx_to_buf_idx[i] contains (i_buf, i_vertex_in_buf) indices that are all fused into vertex [i]
    # each element of this list defines an adjacency relation - all vertices in fused_idx_to_buf_idx[i] are "adjacent"
    fused_idx_to_buf_idx: List[List[Tuple[int, int]]] = []
    # buf_idx_to_fused_idx[i_buf][i_vertex_in_buf] contains the fused index
    buf_idx_to_fused_idx: List[List[int]] = [
        [-1] * len(buf)
        for buf in vertices
    ]
    # is_fused[i_buf][i_vertex_in_buf] = was that vertex fused, or did it create a new one.
    is_fused: List[List[bool]] = [
        [False] * len(buf)
        for buf in vertices
    ]

    for i_buf, buf in enumerate(vertices):
        for i in range(len(buf)):
            vert_info = (
                buf.pos[i].xyz.copy().freeze(),
                buf.normal[i].xyz.copy().freeze() if buf.normal else None,
                buf.bone_data[i].copy().freeze() if buf.bone_data else None,
                buf.weight_data[i].copy().freeze() if buf.weight_data else None,
            )
            if vert_info in vert_indices:
                # Fuse this into a previous vertex
                fusion_idx = vert_indices[vert_info]
                fused_idx_to_buf_idx[fusion_idx].append((i_buf, i))
                buf_idx_to_fused_idx[i_buf][i] = fusion_idx
                is_fused[i_buf][i] = True
            else:
                fusion_idx = len(fused_idx_to_buf_idx)
                vert_indices[vert_info] = fusion_idx
                fused_idx_to_buf_idx.append([(i_buf, i)])
                buf_idx_to_fused_idx[i_buf][i] = fusion_idx
                is_fused[i_buf][i] = False

    return buf_idx_to_fused_idx, is_fused


def gmd_meshes_to_bmesh(
        gmd_meshes: Union[List[GMDMesh], List[GMDSkinnedMesh]],
        vertex_group_indices: Dict[str, int],
        attr_set_material_idx_mapping: Dict[int, int],
        gmd_to_blender_world: Matrix,
        fuse_vertices: bool,
        error: ErrorReporter):
    if len(gmd_meshes) == 0:
        error.fatal("Called gmd_meshes_to_bmesh with 0 meshes!")
    if len([m for m in gmd_meshes if m.empty]) > 0:
        error.fatal("Called gmd_meshes_to_bmesh with meshes marked as empty! This can only happen if using "
                    "VertexImportMode.NO_VERTICES, which shouldn't be the case here.")

    is_skinned = isinstance(gmd_meshes[0], GMDSkinnedMesh) and gmd_meshes[0].vertices_data.layout.assume_skinned
    error.debug("MESH", f"make_merged_gmd_mesh called with {gmd_meshes} skinned={is_skinned} fusing={fuse_vertices}")
    error.debug("MESH", f"vertex layout: {str(gmd_meshes[0].vertices_data.layout)}")

    # If necessary, rewrite bone indices to be consistent
    vertices: Union[List[GMDVertexBuffer_Generic], List[GMDVertexBuffer_Skinned]] = [
        m.vertices_data
        for m in gmd_meshes
    ]
    if is_skinned:
        if not all(isinstance(x, GMDSkinnedMesh) for x in gmd_meshes):
            error.fatal("Called gmd_meshes_to_bmesh with a mix of skinned and unskinned meshes")

        gmd_meshes = cast(List[GMDSkinnedMesh], gmd_meshes)
        vertices = cast(List[GMDVertexBuffer_Skinned], vertices)
        # Rewrite vertices data to use consistent bone indices throughout
        relevant_bones = make_bone_indices_consistent(gmd_meshes, vertices)
    else:
        if any(isinstance(x, GMDSkinnedMesh) for x in gmd_meshes):
            error.fatal("Called gmd_meshes_to_bmesh with a mix of skinned and unskinned meshes")

        gmd_meshes = cast(List[GMDMesh], gmd_meshes)
        relevant_bones = None

    # Create the mesh and deform layer (if necessary)
    bm = bmesh.new()
    deform = bm.verts.layers.deform.new("Vertex Weights") if is_skinned else None
    if deform and (relevant_bones is None):
        error.fatal(f"Mismatch between deform/is_skinned, and the existence of relevant_bones")

    # Add a single vertex's (position, bone weights) to the BMesh
    def add_vertex_to_bmesh(buf, i: int):
        vert = bm.verts.new(gmd_to_blender_world @ buf.pos[i].xyz)
        if buf.normal:
            # apply the matrix to normal.xyz.resized(4) to set the w component to 0 - normals cannot be translated!
            # Just using .xyz would make blender apply a translation
            vert.normal = (gmd_to_blender_world @ (buf.normal[i].xyz.resized(4))).xyz
        if deform:
            for bone_weight in buf.bone_weights[i]:
                if bone_weight.weight > 0:
                    if bone_weight.bone >= len(relevant_bones):
                        error.debug("BONES", f"bone out of bounds - "
                                             f"bone {bone_weight.bone} in {[b.name for b in relevant_bones]}")
                        error.debug("BONES", f"submesh len = {len(buf)}")
                    vertex_group_index = vertex_group_indices[relevant_bones[bone_weight.bone].name]
                    vert[deform][vertex_group_index] = bone_weight.weight

    # Optionally apply vertex fusion (merging "adjacent" vertices while keeping per-loop data)
    # before adding all vertices in order
    if fuse_vertices:
        mesh_vtx_idx_to_bmesh_idx, is_fused = vertex_fusion(vertices)
        for i_buf, buf in enumerate(vertices):
            for i in range(len(buf)):
                if not is_fused[i_buf][i]:
                    assert len(bm.verts) == mesh_vtx_idx_to_bmesh_idx[i_buf][i]
                    add_vertex_to_bmesh(buf, i)
    else:
        mesh_vtx_idx_to_bmesh_idx = [
            [-1] * len(buf)
            for buf in vertices
        ]
        # Assign each vertex in each mesh to the bmesh
        for i_buf, buf in enumerate(vertices):
            for i in range(len(buf)):
                add_vertex_to_bmesh(buf, i)
                mesh_vtx_idx_to_bmesh_idx[i_buf][i] = len(bm.verts)

    # Now we've added the vertices, update bmesh internal structures
    bm.verts.ensure_lookup_table()
    bm.verts.index_update()

    # The GMD meshes may have different vertex layouts -> may need to send vertex data to different layers
    # => for each unique vertex layout in our meshes, find the layers they need and create/reuse them
    unique_vertex_layouts = set([buf.layout for buf in vertices])
    # Map the "packing flags" to the set of layers to use (packing flags are essentially the hash of the attribute set)
    attr_set_layers: Dict[int, AttribSetLayers_bmesh] = {
        layout.packing_flags: AttribSetLayerNames.build_from(layout, is_skinned).create_on(bm, error)
        for layout in unique_vertex_layouts
    }

    # Put the faces and extra data in the BMesh
    triangles: Set[Tuple[int, int, int]] = set()

    # Helper function for adding a face to the BMesh
    def add_face_to_bmesh(face_idx: Tuple[int, int, int], attr_idx: int):
        try:
            # This can throw ValueError if the triangle is "degenerate" - i.e. has two vertices that are the same
            # [1, 2, 3] is fine
            # [1, 2, 2] is degenerate
            # This should never be called with degenerate triangles, but if there is one we skip it and recover.
            face = bm.faces.new((bm.verts[face_idx[0]], bm.verts[face_idx[1]], bm.verts[face_idx[2]]))
        except ValueError as e:
            error.recoverable(
                f"Adding face {face_idx} resulted in ValueError - This should have been a valid triangle. "
                f"Vert count: {len(bm.verts)}.\n{e}")
        else:
            face.smooth = True
            face.material_index = attr_idx
            triangles.add(tuple(sorted(face_idx)))
            return face

    for m_i, gmd_mesh in enumerate(gmd_meshes):
        layers = attr_set_layers[gmd_mesh.vertices_data.layout.packing_flags]
        # Check the layers
        if not layers.tangent_layer and gmd_mesh.vertices_data.layout.tangent_storage and layers.primary_uv_i is None:
            error.recoverable(f"Material/shader {gmd_mesh.attribute_set.shader} requires tangents to be calculated, "
                              f"but doesn't have a primary UV map."
                              f"This will fail if you try to export it, because Blender calculates tangents from UV maps."
                              f"If you're OK with this, disable Strict Import and try again")

        attr_idx = attr_set_material_idx_mapping[id(gmd_mesh.attribute_set)]

        # For face in mesh
        for ti in range(0, len(gmd_mesh.triangle_indices), 3):
            tri_idxs = gmd_mesh.triangle_indices[ti:ti + 3]
            if 0xFFFF in tri_idxs:
                error.recoverable(f"Found an 0xFFFF index inside a triangle_indices list! That shouldn't happen.")
                continue

            remapped_tri_idxs = tuple(mesh_vtx_idx_to_bmesh_idx[m_i][v_i] for v_i in tri_idxs)
            # If face doesn't already exist, and is valid
            if len(set(remapped_tri_idxs)) != 3:
                continue
            if tuple(sorted(remapped_tri_idxs)) in triangles:
                continue
            # Create face
            face = add_face_to_bmesh(remapped_tri_idxs, attr_idx)
            if not face:
                # Creating the face failed for some reason
                continue

            # Apply Col0, Col1, TangentW, UV for each loop
            if layers.col0_layer:
                assert gmd_mesh.vertices_data.col0 is not None
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    color = gmd_mesh.vertices_data.col0[v_i]
                    loop[layers.col0_layer] = (color.x, color.y, color.z, color.w)

            if layers.col1_layer:
                assert gmd_mesh.vertices_data.col1 is not None
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    color = gmd_mesh.vertices_data.col1[v_i]
                    loop[layers.col1_layer] = (color.x, color.y, color.z, color.w)

            if layers.weight_data_layer:
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    weight = gmd_mesh.vertices_data.weight_data[v_i]
                    loop[layers.weight_data_layer] = (weight.x, weight.y, weight.z, weight.w)

            if layers.bone_data_layer:
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    # Divide by 255 to scale to 0..1
                    bones = gmd_mesh.vertices_data.bone_data[v_i] / 255
                    loop[layers.bone_data_layer] = (bones.x, bones.y, bones.z, bones.w)

            if layers.normal_w_layer:
                assert gmd_mesh.vertices_data.normal is not None
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    normal_w = gmd_mesh.vertices_data.normal[v_i].w
                    # Convert from [-1, 1] to [0, 1]
                    # Not sure why, presumably numbers <0 aren't valid in a color? unsure tho
                    loop[layers.normal_w_layer] = ((normal_w + 1) / 2, 0, 0, 0)

            if layers.tangent_layer:
                assert gmd_mesh.vertices_data.tangent is not None
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    tangent = gmd_mesh.vertices_data.tangent[v_i]
                    # Convert from [-1, 1] to [0, 1]
                    # Not sure why, presumably numbers <0 aren't valid in a color? unsure tho
                    loop[layers.tangent_layer] = (
                        (tangent[0] + 1) / 2, (tangent[1] + 1) / 2, (tangent[2] + 1) / 2, (tangent[3] + 1) / 2)

            if layers.tangent_w_layer:
                assert gmd_mesh.vertices_data.tangent is not None
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    tangent_w = gmd_mesh.vertices_data.tangent[v_i].w
                    # Convert from [-1, 1] to [0, 1]
                    # Not sure why, presumably numbers <0 aren't valid in a color? unsure tho
                    loop[layers.tangent_w_layer] = ((tangent_w + 1) / 2, 0, 0, 0)

            for uv_i, (uv_componentcount, uv_layer) in enumerate(layers.uv_layers):
                if uv_componentcount == 2:
                    for (v_i, loop) in zip(tri_idxs, face.loops):
                        original_uv = gmd_mesh.vertices_data.uvs[uv_i][v_i]
                        loop[uv_layer].uv = (original_uv.x, 1.0 - original_uv.y)
                else:
                    for (v_i, loop) in zip(tri_idxs, face.loops):
                        original_uv = gmd_mesh.vertices_data.uvs[uv_i][v_i]
                        loop[uv_layer] = original_uv.resized(4)
                        if any(x < 0 or x > 1 for x in original_uv):
                            error.recoverable(f"Data in UV{uv_i} is outside the range of values Blender can store. "
                                              f"Expected values between 0 and 1, got {original_uv}")
    return bm
