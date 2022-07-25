from dataclasses import dataclass
from typing import Union, List, Dict, cast, Tuple, Set

import bmesh
from mathutils import Matrix

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import BoneWeight, ==, GMDVertexBuffer_Skinned
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter
from yk_gmd_blender.blender.common import AttribSetLayerNames, AttribSetLayers_bmesh


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

    # Fix up bone mappings if the meshes are skinned
    remapped_vertices = [m.vertices_data for m in gmd_meshes]
    if is_skinned:
        if not all(isinstance(x, GMDSkinnedMesh) for x in gmd_meshes):
            error.fatal("Called gmd_meshes_to_bmesh with a mix of skinned and unskinned meshes")

        gmd_meshes = cast(List[GMDSkinnedMesh], gmd_meshes)

        # Skinned meshes are more complicated because vertices reference bones using a *per-mesh* index into that "relevant_bones" list
        # These indices have to be merged into a single relevant bones list,
        # for each GMD mesh, because each mesh will usually have a different "relevant_bones" list
        relevant_bones = gmd_meshes[0].relevant_bones[:]
        # merged_vertex_buffer = gmd_meshes[0].vertices_data[:]
        for i_mesh in range(1, len(gmd_meshes)):
            gmd_mesh = gmd_meshes[i_mesh]

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

            # Turn the remapped_vertices into a copy instead of a reference
            remapped_vertices[i_mesh] = remapped_vertices[i_mesh][:]
            verts_to_remap = cast(GMDVertexBuffer_Skinned, remapped_vertices[i_mesh])
            # Remap the bones in the vertices
            for i_vtx in range(len(verts_to_remap)):
                old_weights = verts_to_remap.bone_weights[i_vtx]
                verts_to_remap.bone_weights[i_vtx] = (
                    remap_weight(old_weights[0]),
                    remap_weight(old_weights[1]),
                    remap_weight(old_weights[2]),
                    remap_weight(old_weights[3]),
                )
    else:
        if any(isinstance(x, GMDSkinnedMesh) for x in gmd_meshes):
            error.fatal("Called gmd_meshes_to_bmesh with a mix of skinned and unskinned meshes")

        relevant_bones = None

    # Maps an index (x, y) for remapped_vertices[x][y] to a vertex index in the actual BMesh
    mesh_vtx_idx_to_bmesh_idx: Dict[Tuple[int, int], int] = {}
    bm = bmesh.new()
    deform = bm.verts.layers.deform.new("Vertex Weights") if is_skinned else None
    if deform and (relevant_bones is None):
        error.fatal(f"Mismatch between deform/is_skinned, and the existence of relevant_bones")

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
                        error.debug("BONES",
                            f"bone out of bounds - bone {bone_weight.bone} in {[b.name for b in relevant_bones]}")
                        error.debug("BONES", f"submesh len = {len(buf)}")
                    vertex_group_index = vertex_group_indices[relevant_bones[bone_weight.bone].name]
                    vert[deform][vertex_group_index] = bone_weight.weight

    # Put the raw vertices - i.e. positions - into the BMesh
    if fuse_vertices:
        # Find unique (position, normal, boneweight) pairs, assign to BMesh vertex indices
        vert_indices: Dict[Tuple[Vector, Vector, BoneWeight]] = {}
        for i_buf, buf in enumerate(remapped_vertices):
            for i in range(len(buf)):
                vert_info = (
                    buf.pos[i].xyz.copy().freeze(),
                    buf.normal[i].xyz.copy().freeze() if buf.normal else None,
                    buf.bone_weights[i] if is_skinned else None
                )
                if vert_info in vert_indices:
                    # TODO check if merging this set of verts will create a degenerate triangle somehow?
                    mesh_vtx_idx_to_bmesh_idx[(i_buf, i)] = vert_indices[vert_info]
                else:
                    next_idx = len(bm.verts)
                    vert_indices[vert_info] = next_idx
                    mesh_vtx_idx_to_bmesh_idx[(i_buf, i)] = next_idx
                    add_vertex_to_bmesh(buf, i)
    else:
        # Assign each vertex in each mesh to the bmesh
        for i_buf, buf in enumerate(remapped_vertices):
            for i in range(len(buf)):
                add_vertex_to_bmesh(buf, i)
                mesh_vtx_idx_to_bmesh_idx[(i_buf, i)] = len(bm.verts)

    bm.verts.ensure_lookup_table()
    bm.verts.index_update()

    # The GMD meshes may have different vertex layouts -> may need to send vertex data to different layers
    # => for each unique vertex layout in our meshes, find the layers they need and create/reuse them
    unique_vertex_layouts = set([buf.layout for buf in remapped_vertices])
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
        attr_idx = attr_set_material_idx_mapping[id(gmd_mesh.attribute_set)]

        # For face in mesh
        for ti in range(0, len(gmd_mesh.triangle_indices), 3):
            tri_idxs = gmd_mesh.triangle_indices[ti:ti + 3]
            if 0xFFFF in tri_idxs:
                error.recoverable(f"Found an 0xFFFF index inside a triangle_indices list! That shouldn't happen.")
                continue

            remapped_tri_idxs = tuple(mesh_vtx_idx_to_bmesh_idx[(m_i, v_i)] for v_i in tri_idxs)
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
                    loop[layers.tangent_layer] = ((tangent[0] + 1) / 2, (tangent[1] + 1) / 2, (tangent[2] + 1) / 2, (tangent[3  ] + 1) / 2)

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
