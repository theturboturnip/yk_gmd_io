from typing import Union, List, Dict, cast, Tuple, Set

import bmesh
from mathutils import Matrix, Vector
from yk_gmd_blender.blender.common import AttribSetLayerNames, AttribSetLayers_bmesh
from yk_gmd_blender.blender.importer.mesh.vertex_fusion import vertex_fusion, make_bone_indices_consistent
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDSkinnedVertexBuffer, GMDVertexBuffer
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter


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
    vertices: Union[List[GMDVertexBuffer], List[GMDSkinnedVertexBuffer]]
    if is_skinned:
        if not all(isinstance(x, GMDSkinnedMesh) for x in gmd_meshes):
            error.fatal("Called gmd_meshes_to_bmesh with a mix of skinned and unskinned meshes")

        gmd_meshes = cast(List[GMDSkinnedMesh], gmd_meshes)
        # Rewrite vertices data to use consistent bone indices throughout
        relevant_bones, vertices = make_bone_indices_consistent(gmd_meshes)
    else:
        if any(isinstance(x, GMDSkinnedMesh) for x in gmd_meshes):
            error.fatal("Called gmd_meshes_to_bmesh with a mix of skinned and unskinned meshes")

        gmd_meshes = cast(List[GMDMesh], gmd_meshes)
        relevant_bones = None
        vertices = [
            m.vertices_data
            for m in gmd_meshes
        ]

    # Create the mesh and deform layer (if necessary)
    bm = bmesh.new()
    deform = bm.verts.layers.deform.new("Vertex Weights") if is_skinned else None
    if deform and (relevant_bones is None):
        error.fatal(f"Mismatch between deform/is_skinned, and the existence of relevant_bones")

    # Add a single vertex's (position, bone weights) to the BMesh
    def add_vertex_to_bmesh(buf, i: int):
        vert = bm.verts.new(gmd_to_blender_world @ Vector(buf.pos[i][:3]))
        if buf.normal is not None:
            # apply the matrix to normal.xyz.resized(4) to set the w component to 0 - normals cannot be translated!
            # Just using .xyz would make blender apply a translation
            vert.normal = (gmd_to_blender_world @ (Vector(buf.normal[i][:3]).resized(4))).xyz
        if is_skinned:
            for bone, weight in zip(buf.bone_data[i], buf.weight_data[i]):
                if weight > 0:
                    if bone >= len(relevant_bones):
                        error.debug("BONES", f"bone out of bounds - "
                                             f"bone {bone} in {[b.name for b in relevant_bones]}")
                        error.debug("BONES", f"submesh len = {len(buf)}")
                    vertex_group_index = vertex_group_indices[relevant_bones[bone].name]
                    vert[deform][vertex_group_index] = weight

    # Optionally apply vertex fusion (merging "adjacent" vertices while keeping per-loop data)
    # before adding all vertices in order
    if fuse_vertices:
        _, mesh_vtx_idx_to_bmesh_idx, is_fused = vertex_fusion([m.triangle_indices for m in gmd_meshes], vertices)
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
        i_vert = 0
        for i_buf, buf in enumerate(vertices):
            for i in range(len(buf)):
                add_vertex_to_bmesh(buf, i)
                mesh_vtx_idx_to_bmesh_idx[i_buf][i] = i_vert
                i_vert += 1

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
                    loop[layers.col0_layer] = color

            if layers.col1_layer:
                assert gmd_mesh.vertices_data.col1 is not None
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    color = gmd_mesh.vertices_data.col1[v_i]
                    loop[layers.col1_layer] = color

            if layers.weight_data_layer:
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    weight = gmd_mesh.vertices_data.weight_data[v_i]
                    loop[layers.weight_data_layer] = weight

            if layers.bone_data_layer:
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    # Divide by 255 to scale to 0..1
                    bones = gmd_mesh.vertices_data.bone_data[v_i] / 255
                    loop[layers.bone_data_layer] = bones

            if layers.normal_w_layer:
                assert gmd_mesh.vertices_data.normal is not None
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    normal_w = gmd_mesh.vertices_data.normal[v_i][3]
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
                    tangent_w = gmd_mesh.vertices_data.tangent[v_i][3]
                    # Convert from [-1, 1] to [0, 1]
                    # Not sure why, presumably numbers <0 aren't valid in a color? unsure tho
                    loop[layers.tangent_w_layer] = ((tangent_w + 1) / 2, 0, 0, 0)

            for uv_i, (uv_componentcount, uv_layer) in enumerate(layers.uv_layers):
                if uv_componentcount == 2:
                    for (v_i, loop) in zip(tri_idxs, face.loops):
                        original_uv = gmd_mesh.vertices_data.uvs[uv_i][v_i]
                        loop[uv_layer].uv = (original_uv[0], 1.0 - original_uv[1])
                else:
                    for (v_i, loop) in zip(tri_idxs, face.loops):
                        original_uv = gmd_mesh.vertices_data.uvs[uv_i][v_i]
                        loop[uv_layer] = Vector(original_uv).resized(4)
                        if any(x < 0 or x > 1 for x in original_uv):
                            error.recoverable(f"Data in UV{uv_i} is outside the range of values Blender can store. "
                                              f"Expected values between 0 and 1, got {original_uv}")
    return bm
