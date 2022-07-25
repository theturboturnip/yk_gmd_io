from typing import Union, List, Dict, cast, Tuple, Set

import bmesh
from mathutils import Matrix

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import BoneWeight, VecStorage
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter


def gmd_meshes_to_bmesh(
        gmd_meshes: Union[List[GMDMesh], List[GMDSkinnedMesh]],
        vertex_group_indices: Dict[str, int],
        attr_idx: int, gmd_to_blender_world: Matrix,
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
    if is_skinned:
        if not all(isinstance(x, GMDSkinnedMesh) for x in gmd_meshes):
            error.fatal("Called gmd_meshes_to_bmesh with a mix of skinned and unskinned meshes")

        gmd_meshes = cast(List[GMDSkinnedMesh], gmd_meshes)

        # Skinned meshes are more complicated because vertices reference bones using a *per-mesh* index into that "relevant_bones" list
        # These indices have to be changed for the merged mesh, because each mesh will usually have a different "relevant_bones" list
        relevant_bones = gmd_meshes[0].relevant_bones[:]
        merged_vertex_buffer = gmd_meshes[0].vertices_data[:]
        for gmd_mesh in gmd_meshes[1:]:
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

            index_start_to_adjust_bones = len(merged_vertex_buffer)
            merged_vertex_buffer += gmd_mesh.vertices_data
            for i in range(index_start_to_adjust_bones, len(merged_vertex_buffer)):
                old_weights = merged_vertex_buffer.bone_weights[i]
                merged_vertex_buffer.bone_weights[i] = (
                    remap_weight(old_weights[0]),
                    remap_weight(old_weights[1]),
                    remap_weight(old_weights[2]),
                    remap_weight(old_weights[3]),
                )
    else:
        if any(isinstance(x, GMDSkinnedMesh) for x in gmd_meshes):
            error.fatal("Called gmd_meshes_to_bmesh with a mix of skinned and unskinned meshes")

        merged_vertex_buffer = gmd_meshes[0].vertices_data[:]
        for gmd_mesh in gmd_meshes[1:]:
            merged_vertex_buffer += gmd_mesh.vertices_data
        relevant_bones = None

    merged_idx_to_bmesh_idx: Dict[int, int] = {}
    mesh_vtx_idx_to_bmesh_idx: Dict[Tuple[int, int], int] = {}
    bm = bmesh.new()
    deform = bm.verts.layers.deform.new("Vertex Weights") if is_skinned else None
    if deform and (relevant_bones is None):
        error.fatal(f"Mismatch between deform/is_skinned, and the existence of relevant_bones")

    def add_vertex_to_bmesh(i: int):
        vert = bm.verts.new(gmd_to_blender_world @ merged_vertex_buffer.pos[i].xyz)
        if merged_vertex_buffer.normal:
            # apply the matrix to normal.xyz.resized(4) to set the w component to 0 - normals cannot be translated!
            # Just using .xyz would make blender apply a translation
            vert.normal = (gmd_to_blender_world @ (merged_vertex_buffer.normal[i].xyz.resized(4))).xyz
        if deform:
            for bone_weight in merged_vertex_buffer.bone_weights[i]:
                if bone_weight.weight > 0:
                    if bone_weight.bone >= len(relevant_bones):
                        error.debug("BONES",
                            f"bone out of bounds - bone {bone_weight.bone} in {[b.name for b in relevant_bones]}")
                        error.debug("BONES", f"mesh len = {len(merged_vertex_buffer)}")
                    vertex_group_index = vertex_group_indices[relevant_bones[bone_weight.bone].name]
                    vert[deform][vertex_group_index] = bone_weight.weight

    # Set up the indexing table inside the bmesh so lookups work
    if fuse_vertices:
        # Find unique (position, normal, boneweight) pairs, assign to BMesh vertex indices
        vert_indices = {}
        for i in range(len(merged_vertex_buffer)):
            vert_info = (
                merged_vertex_buffer.pos[i].xyz.copy().freeze(),
                merged_vertex_buffer.normal[i].xyz.copy().freeze() if merged_vertex_buffer.normal else None,
                merged_vertex_buffer.bone_weights[i] if is_skinned else None
            )
            if vert_info in vert_indices:
                merged_idx_to_bmesh_idx[i] = vert_indices[vert_info]
            else:
                next_idx = len(bm.verts)
                vert_indices[vert_info] = next_idx
                merged_idx_to_bmesh_idx[i] = next_idx
                add_vertex_to_bmesh(i)
    else:
        # Assign each vertex in each mesh to the bmesh
        for i in range(len(merged_vertex_buffer)):
            merged_idx_to_bmesh_idx[i] = i
            add_vertex_to_bmesh(i)

    merged_idx = 0
    for (m_i, gmd_mesh) in enumerate(gmd_meshes):
        for v_i in range(len(gmd_mesh.vertices_data)):
            mesh_vtx_idx_to_bmesh_idx[(m_i, v_i)] = merged_idx_to_bmesh_idx[merged_idx]
            merged_idx += 1

    bm.verts.ensure_lookup_table()
    bm.verts.index_update()

    # For Col0, Col1, TangentW, UVs
    #   Create layer
    # Color0
    col0_layer = None
    if merged_vertex_buffer.col0:
        col0_layer = bm.loops.layers.color.new("Color0")

    # Color1
    col1_layer = None
    if merged_vertex_buffer.col1:
        col1_layer = bm.loops.layers.color.new("Color1")

    # Weight Data
    weight_data_layer = None
    if merged_vertex_buffer.weight_data and not is_skinned:
        error.debug("MESH", f"Generating layer for Weight Data with storage {merged_vertex_buffer.layout.weights_storage}, componentcount = {VecStorage.component_count(merged_vertex_buffer.layout.weights_storage)}")
        weight_data_layer = bm.loops.layers.color.new("Weight_Data")

    # Bone Data
    bone_data_layer = None
    if merged_vertex_buffer.bone_data and not is_skinned:
        error.debug("MESH", f"Generating layer for Bone Data with storage {merged_vertex_buffer.layout.bones_storage}, componentcount = {VecStorage.component_count(merged_vertex_buffer.layout.bones_storage)}")
        bone_data_layer = bm.loops.layers.color.new("Bone_Data")

    # Normal W data
    tangent_w_layer = None
    if merged_vertex_buffer.layout.tangent_storage in [VecStorage.Vec4Half, VecStorage.Vec4Fixed, VecStorage.Vec4Full]:
        tangent_w_layer = bm.loops.layers.color.new("TangentW")

    # UVs
    # Yakuza has 3D/4D UV coordinates. Blender doesn't support this in the UV channel.
    # The solution is to have a deterministic "primary UV" designation that can only be 2D
    # This is the only UV loaded into the actual UV layer, the rest are all loaded into the vertex colors with special names.
    primary_uv_i = merged_vertex_buffer.layout.get_primary_uv_index()
    uv_layers = []
    for i, uv in enumerate(merged_vertex_buffer.uvs):
        error.debug("MESH", f"Generating layer for UV {i} with storage {merged_vertex_buffer.layout.uv_storages[i]}, componentcount = {VecStorage.component_count(merged_vertex_buffer.layout.uv_storages[i])}")
        if i == primary_uv_i:
            error.debug("MESH", f"Making layer as UV layer")
            uv_layers.append(bm.loops.layers.uv.new(f"UV_Primary"))
        elif VecStorage.component_count(merged_vertex_buffer.layout.uv_storages[i]) == 2:
            error.debug("MESH", f"Making layer as UV layer")
            uv_layers.append(bm.loops.layers.uv.new(f"UV{i}"))
        else:
            uv_layers.append(bm.loops.layers.color.new(f"UV{i}"))

    # For mesh in meshes
    triangles: Set[Tuple[int, int, int]] = set()

    def add_face_to_bmesh(face_idx: Tuple[int, int, int]):
        try:
            # This can throw ValueError if the triangle is "degenerate" - i.e. has two vertices that are the same
            # [1, 2, 3] is fine
            # [1, 2, 2] is degenerate
            # This should never be called with degenerate triangles, but if there is one we skip it and recover.
            face = bm.faces.new((bm.verts[face_idx[0]], bm.verts[face_idx[1]], bm.verts[face_idx[2]]))
        except ValueError as e:
            error.recoverable(
                f"Adding face {face_idx} resulted in ValueError - This should have been a valid triangle. Vert count: {len(bm.verts)}.\n{e}")
        else:
            face.smooth = True
            face.material_index = attr_idx
            triangles.add(tuple(sorted(face_idx)))
            return face

    for m_i, gmd_mesh in enumerate(gmd_meshes):
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
            face = add_face_to_bmesh(remapped_tri_idxs)
            if not face:
                # Creating the face failed for some reason
                continue
            # Apply Col0, Col1, TangentW, UV for each loop
            if col0_layer:
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    color = gmd_mesh.vertices_data.col0[v_i]
                    loop[col0_layer] = (color.x, color.y, color.z, color.w)

            if col1_layer:
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    color = gmd_mesh.vertices_data.col1[v_i]
                    loop[col1_layer] = (color.x, color.y, color.z, color.w)

            if weight_data_layer:
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    weight = gmd_mesh.vertices_data.weight_data[v_i]
                    loop[weight_data_layer] = (weight.x, weight.y, weight.z, weight.w)

            if bone_data_layer:
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    # Divide by 255 to scale to 0..1
                    bones = gmd_mesh.vertices_data.bone_data[v_i] / 255
                    loop[bone_data_layer] = (bones.x, bones.y, bones.z, bones.w)

            if tangent_w_layer:
                for (v_i, loop) in zip(tri_idxs, face.loops):
                    tangent_w = gmd_mesh.vertices_data.tangent[v_i].w
                    # Convert from [-1, 1] to [0, 1]
                    # Not sure why, presumably numbers <0 aren't valid in a color? unsure tho
                    loop[tangent_w_layer] = ((tangent_w + 1) / 2, 0, 0, 0)

            for uv_i, uv_layer in enumerate(uv_layers):
                if VecStorage.component_count(merged_vertex_buffer.layout.uv_storages[uv_i]) == 2:
                    for (v_i, loop) in zip(tri_idxs, face.loops):
                        original_uv = gmd_mesh.vertices_data.uvs[uv_i][v_i]
                        loop[uv_layer].uv = (original_uv.x, 1.0 - original_uv.y)
                else:
                    for (v_i, loop) in zip(tri_idxs, face.loops):
                        original_uv = gmd_mesh.vertices_data.uvs[uv_i][v_i]
                        loop[uv_layer] = original_uv.resized(4)
                        if any(x < 0 or x > 1 for x in original_uv):
                            error.recoverable(f"Data in UV{uv_i} is outside the range of values Blender can store. Expected values between 0 and 1, got {original_uv}")
    return bm
