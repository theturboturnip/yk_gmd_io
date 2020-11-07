from typing import Union, List, Dict, cast, Tuple, Set

from mathutils import Vector, Matrix

import bmesh

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import BoneWeight, BoneWeight4, VecStorage
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter


def gmd_meshes_to_bmesh(gmd_meshes: Union[List[GMDMesh], List[GMDSkinnedMesh]], vertex_group_indices: Dict[str, int], attr_idx: int, gmd_to_blender_world: Matrix, fuse_vertices: bool, error: ErrorReporter):
    if len(gmd_meshes) == 0:
        error.fatal("Called make_merged_gmd_mesh with 0 meshes!")

    is_skinned = isinstance(gmd_meshes[0], GMDSkinnedMesh)
    print(f"make_merged_gmd_mesh called with {gmd_meshes} skinned={is_skinned} fusing={fuse_vertices}")

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
            # Just using .xyz would make blender apply a translation (TODO - check this?)
            vert.normal = (gmd_to_blender_world @ (merged_vertex_buffer.normal[i].xyz.resized(4))).xyz
        if deform:
            for bone_weight in merged_vertex_buffer.bone_weights[i]:
                if bone_weight.weight > 0:
                    if bone_weight.bone >= len(relevant_bones):
                        print(
                            f"bone out of bounds - bone {bone_weight.bone} in {[b.name for b in relevant_bones]}")
                        print(f"mesh len = {len(merged_vertex_buffer)}")
                    vertex_group_index = vertex_group_indices[relevant_bones[bone_weight.bone].name]
                    vert[deform][vertex_group_index] = bone_weight.weight

    # Set up the indexing table inside the bmesh so lookups work
    if fuse_vertices:
        # Find unique (position, normal, boneweight) pairs, assign to BMesh vertex indices
        vert_indices = {}
        for i in range(len(merged_vertex_buffer)):
            vert_info = (merged_vertex_buffer.pos[i].xyz.copy().freeze(), merged_vertex_buffer.normal[i].xyz.copy().freeze(), merged_vertex_buffer.bone_weights[i] if is_skinned else None)
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
        print(f"Generating layer for UV {i} with storage {merged_vertex_buffer.layout.uv_storages[i]}, componentcount = {VecStorage.component_count(merged_vertex_buffer.layout.uv_storages[i])}")
        if i == primary_uv_i:
            print(f"Making layer as UV layer")
            uv_layers.append(bm.loops.layers.uv.new(f"UV_Primary"))
        elif VecStorage.component_count(merged_vertex_buffer.layout.uv_storages[i]) == 2:
            print(f"Making layer as UV layer")
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

# def make_merged_gmd_mesh(self, gmd_meshes: List[TMesh], remove_dupes: bool = True) -> TMesh:
#     """
#     Given multiple GMD Meshes that use the same material, merge them into a single GMDMesh that uses a single vertex buffer and index set.
#     :param gmd_meshes: A list of at least one mesh, that are all of the same type, and use the same attribute set.
#     :return: A merged GMD Mesh. Only has triangle indices, not strips.
#     """
#     if len(gmd_meshes) == 0:
#         self.error.fatal("Called make_merged_gmd_mesh with 0 meshes!")
#
#     print(f"make_merged_gmd_mesh called with {gmd_meshes} fusing={remove_dupes}")
#
#     # if len(gmd_meshes) == 1:
#     #    return gmd_meshes[0]
#
#     # All of the meshes should have the same attribute set
#     if not all(gmd_mesh.attribute_set is gmd_meshes[0].attribute_set for gmd_mesh in gmd_meshes[1:]):
#         self.error.fatal("Trying to merge GMDMeshes that do not share an attribute set!")
#
#     # Assume that all meshes in the list have the same type
#     # -> if one is skinned, all of them are
#     making_skinned_mesh = isinstance(gmd_meshes[0], GMDSkinnedMesh)
#     if making_skinned_mesh:
#         # Skinned meshes are more complicated because vertices reference bones using a *per-mesh* index into that "relevant_bones" list
#         # These indices have to be changed for the merged mesh, because each mesh will usually have a different "relevant_bones" list
#         gmd_meshes = cast(List[GMDSkinnedMesh], gmd_meshes)
#
#         relevant_bones = gmd_meshes[0].relevant_bones[:]
#         merged_vertex_buffer = gmd_meshes[0].vertices_data[:]
#         for gmd_mesh in gmd_meshes[1:]:
#             bone_index_mapping = {}
#             for i, bone in enumerate(gmd_mesh.relevant_bones):
#                 if bone not in relevant_bones:
#                     relevant_bones.append(bone)
#                 bone_index_mapping[i] = relevant_bones.index(bone)
#
#             def remap_weight(bone_weight: BoneWeight):
#                 # If the weight is 0 the bone is unused, so map it to a consistent 0.
#                 if bone_weight.weight == 0:
#                     return BoneWeight(0, weight=0.0)
#                 else:
#                     return BoneWeight(bone_index_mapping[bone_weight.bone], bone_weight.weight)
#
#             index_start_to_adjust_bones = len(merged_vertex_buffer)
#             merged_vertex_buffer += gmd_mesh.vertices_data
#             for i in range(index_start_to_adjust_bones, len(merged_vertex_buffer)):
#                 old_weights = merged_vertex_buffer.bone_weights[i]
#                 merged_vertex_buffer.bone_weights[i] = (
#                     remap_weight(old_weights[0]),
#                     remap_weight(old_weights[1]),
#                     remap_weight(old_weights[2]),
#                     remap_weight(old_weights[3]),
#                 )
#     else:
#         merged_vertex_buffer = gmd_meshes[0].vertices_data[:]
#         for gmd_mesh in gmd_meshes[1:]:
#             merged_vertex_buffer += gmd_mesh.vertices_data
#
#     # Mapping of vertex index pre-merge -> merged vertex index
#     # i.e. if the merger decides vertex 5 and vertex 7 are merged, mapping[5] = 5 and mapping[7] = 5
#     merged_indices_map = {}
#     dupes_of_map = collections.defaultdict(list)
#     unused_indices = set()
#     if remove_dupes:
#         # Build a 3D tree of positions, so we can efficiently find the closest vertices
#         from mathutils import kdtree
#
#         size = len(merged_vertex_buffer)
#         kd = kdtree.KDTree(size)
#         for i, pos in enumerate(merged_vertex_buffer.pos):
#             kd.insert(pos.xyz, i)
#         kd.balance()
#
#         # Build the initial state for the merged index map, just x:x for all indices
#         merged_indices_map = {
#             i: i
#             for i in range(len(merged_vertex_buffer))
#         }
#
#         equality_check_distance = 0.000001
#         for i, pos in enumerate(merged_vertex_buffer.pos):
#             # If this index has been merged, don't re-merge it
#             if i in unused_indices:
#                 continue
#
#             for (co, index, dist) in kd.find_range(pos.xyz, equality_check_distance):
#                 # Ignore this index and any indices which have already been merged elsewhere
#                 if index == i:
#                     continue
#                 if index in unused_indices:
#                     continue
#
#                 # If the new vertex is *exactly* equal (except maybe for the tangent)...
#                 if dist == 0 and merged_vertex_buffer.verts_equalish(i, index):
#                     # then set its map entry to refer to i
#                     unused_indices.add(index)
#                     merged_indices_map[index] = i
#                     dupes_of_map[i].append(index)
#
#     # Build a separate index map for each mesh, of (mesh-local index) -> (overall merged index)
#     index_maps = []
#     overall_i = 0
#     for gmd_mesh in gmd_meshes:
#         index_map = {}
#         if merged_indices_map:
#             for i in range(len(gmd_mesh.vertices_data)):
#                 index_map[i] = merged_indices_map[overall_i]
#                 overall_i += 1
#         else:
#             for i in range(len(gmd_mesh.vertices_data)):
#                 index_map[i] = overall_i
#                 overall_i += 1
#
#         index_maps.append(index_map)
#
#     # Apply the index mappings to the actual index buffers, and merge them.
#     # We could also do this for the triangle strip indices, but it's unnecessary.
#     # TODO - This can create degenerate faces if a triangle of equal vertices exists in multiple meshes
#     # i.e. if Mesh 1 has triangle (0,1,2) and Mesh 2 has triangle (60,61,62) and 0/60, 1/61, 2/62 are merged then both triangles are (0,1,2) and invalid
#     triangle_indices = array.array('i')
#     for gmd_mesh, index_map in zip(gmd_meshes, index_maps):
#         for index in gmd_mesh.triangle_indices:
#             triangle_indices.append(index_map[index])
#
#     if making_skinned_mesh:
#         return GMDSkinnedMesh(
#             attribute_set=gmd_meshes[0].attribute_set,
#
#             vertices_data=merged_vertex_buffer,
#             triangle_indices=triangle_indices,
#             triangle_strip_noreset_indices=array.array('i'),
#             triangle_strip_reset_indices=array.array('i'),
#
#             relevant_bones=relevant_bones
#         )
#     else:
#         return GMDMesh(
#             attribute_set=gmd_meshes[0].attribute_set,
#
#             vertices_data=merged_vertex_buffer,
#             triangle_indices=triangle_indices,
#             triangle_strip_noreset_indices=array.array('i'),
#             triangle_strip_reset_indices=array.array('i'),
#         )
#
#
# def gmd_to_bmesh(gmd_mesh: Union[GMDMesh, GMDSkinnedMesh], vertex_group_indices: Dict[str, int],
#                  material_index: int, custom_normals: List[Vector]) -> bmesh.types.BMesh:
#     """
#     Given a GMDMesh/GMDSkinnedMesh, convert it to a BMesh.
#     :param gmd_mesh: The mesh to convert.
#     :param vertex_group_indices: A mapping of bone name -> vertex group index.
#     :param material_index: The material index this mesh uses.
#     :return: A BMesh representing this GMDMesh, with bone weights included if the gmd_mesh is an instance of GMDSkinnedMesh.
#     """
#     apply_bone_weights = isinstance(gmd_mesh, GMDSkinnedMesh)
#
#     bm = bmesh.new()
#
#     # Create initial vertices (position, normal, bone weights if present)
#     if apply_bone_weights:
#         deform = bm.verts.layers.deform.new("Vertex Weights")
#
#     custom_normals_with_unused = []
#
#     vtx_buffer = gmd_mesh.vertices_data
#     for i in range(len(vtx_buffer)):
#         vert = bm.verts.new(self.gmd_to_blender_world @ vtx_buffer.pos[i].xyz)
#         if vtx_buffer.normal:
#             # apply the matrix to normal.xyz.resized(4) to set the w component to 0 - normals cannot be translated!
#             # Just using .xyz would make blender apply a translation (TODO - check this?)
#             normal = (self.gmd_to_blender_world @ (vtx_buffer.normal[i].xyz.resized(4))).xyz
#             custom_normals_with_unused.append(normal)
#             vert.normal = normal
#         # Tangents cannot be applied
#         if apply_bone_weights and vtx_buffer.bone_weights:
#             for bone_weight in vtx_buffer.bone_weights[i]:
#                 if bone_weight.weight > 0:
#                     if bone_weight.bone >= len(gmd_mesh.relevant_bones):
#                         print(
#                             f"bone out of bounds - bone {bone_weight.bone} in {[b.name for b in gmd_mesh.relevant_bones]}")
#                         print(f"mesh len = {len(vtx_buffer)}")
#                     vertex_group_index = vertex_group_indices[gmd_mesh.relevant_bones[bone_weight.bone].name]
#                     vert[deform][vertex_group_index] = bone_weight.weight
#     # Set up the indexing table inside the bmesh so lookups work
#     bm.verts.ensure_lookup_table()
#     bm.verts.index_update()
#
#     # Connect triangles
#     def add_face_to_bmesh(face: Tuple[int, int, int]):
#         try:
#             # This can throw ValueError if the triangle is "degenerate" - i.e. has two vertices that are the same
#             # [1, 2, 3] is fine
#             # [1, 2, 2] is degenerate
#             # This should never be called with degenerate triangles, but if there is one we skip it and recover.
#             face = bm.faces.new((bm.verts[face[0]], bm.verts[face[1]], bm.verts[face[2]]))
#         except ValueError as e:
#             self.error.recoverable(
#                 f"Adding face {face} resulted in ValueError - This should have been a valid triangle. Vert count: {len(bm.verts)}.\n{e}")
#         else:
#             face.smooth = True
#             face.material_index = material_index
#
#     # For each triangle, add it to the bmesh
#     for i in range(0, len(gmd_mesh.triangle_indices), 3):
#         tri_idxs = gmd_mesh.triangle_indices[i:i + 3]
#         if len(set(tri_idxs)) != 3:
#             continue
#         if 0xFFFF in tri_idxs:
#             self.error.recoverable(f"Found an 0xFFFF index inside a triangle_indices list! That shouldn't happen.")
#             continue
#         add_face_to_bmesh(tri_idxs)
#
#     # Color0
#     if vtx_buffer.col0:
#         col0_layer = bm.loops.layers.color.new("Color0")
#         for face in bm.faces:
#             for loop in face.loops:
#                 color = vtx_buffer.col0[loop.vert.index]
#                 loop[col0_layer] = (color.x, color.y, color.z, color.w)
#
#     # Color1
#     if vtx_buffer.col1:
#         col1_layer = bm.loops.layers.color.new("Color1")
#         for face in bm.faces:
#             for loop in face.loops:
#                 color = vtx_buffer.col1[loop.vert.index]
#                 loop[col1_layer] = (color.x, color.y, color.z, color.w)
#
#     # Tangent Data
#     if vtx_buffer.tangent:
#         tangent_layer = bm.loops.layers.color.new("TangentStorage")
#         for face in bm.faces:
#             for loop in face.loops:
#                 color = vtx_buffer.tangent[loop.vert.index]
#                 loop[tangent_layer] = (color.x, color.y, color.z, color.w)
#
#     # Normal W data
#     if vtx_buffer.layout.normal_storage in [VecStorage.Vec4Half, VecStorage.Vec4Fixed, VecStorage.Vec4Full]:
#         normal_w_layer = bm.loops.layers.color.new("NormalW")
#         for face in bm.faces:
#             for loop in face.loops:
#                 # normals are stored [-1, 1] so convert to [0, 1] range
#                 loop[normal_w_layer] = ((vtx_buffer.normal[vert.index].w + 1) / 2, 0, 0, 0)
#
#     # UVs
#     # Yakuza has 3D/4D UV coordinates. Blender doesn't support this in the UV channel.
#     # The solution is to have a deterministic "primary UV" designation that can only be 2D
#     # This is the only UV loaded into the actual UV layer, the rest are all loaded into the vertex colors with special names.
#     primary_uv_i = gmd_mesh.vertices_data.layout.get_primary_uv_index()
#     for i, uv in enumerate(vtx_buffer.uvs):
#         if i == primary_uv_i:
#             uv_layer = bm.loops.layers.uv.new(f"UV_Primary")
#             for face in bm.faces:
#                 for loop in face.loops:
#                     original_uv = uv[loop.vert.index]
#                     loop[uv_layer].uv = (original_uv.x, 1.0 - original_uv.y)
#         else:
#             uv_layer = bm.loops.layers.color.new(f"UV{i}")
#             for face in bm.faces:
#                 for loop in face.loops:
#                     original_uv = uv[loop.vert.index]
#                     loop[uv_layer] = original_uv.resized(4)
#
#     # Removed unused verts
#     # Typically the mesh passed into this function comes from make_merged_gmd_mesh, which "fuses" vertices by changing the index buffer
#     # However, the unused verts themselves are still in the buffer, and should be removed.
#     # THIS MUST ONLY HAPPEN AFTER ALL OTHER LOADING - otherwise different data channels will be messed up
#     # Remove indices in reverse order, so we can remove them from custom_normals_with_unused
#     unused_verts = sorted([v for v in bm.verts if not v.link_faces], key=lambda v: v.index, reverse=True)
#     # equiv of bmesh.ops.delete(bm, geom=verts, context='VERTS')
#     # unused_indices = [v.index for v in unused_verts]
#     for v in unused_verts:
#         # Deleting from the middle of a list sucks and is slow, but idk how to do it better
#         del custom_normals_with_unused[v.index]
#         bm.verts.remove(v)
#     bm.verts.ensure_lookup_table()
#     bm.verts.index_update()
#
#     custom_normals.extend(custom_normals_with_unused)
#
#     return bm


