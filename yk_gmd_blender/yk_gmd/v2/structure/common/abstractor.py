import collections
from typing import *

from mathutils import Matrix

from yk_gmd_blender.structurelib.base import FixedSizeArrayUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint16
from yk_gmd_blender.yk_gmd.legacy.abstract.bone import GMDBone
from yk_gmd_blender.yk_gmd.legacy.abstract.material import GMDMaterial, GMDMaterialTextureIndex
from yk_gmd_blender.yk_gmd.legacy.abstract.submesh import GMDSubmesh
from yk_gmd_blender.yk_gmd.legacy.abstract.vector import Vec3, Quat
from yk_gmd_blender.yk_gmd.legacy.abstract.vertices import GMDVertexBuffer, GMDVertexBufferLayout

from yk_gmd_blender.yk_gmd.v2.structure.common.attributestruct import AttributeStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStrStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import MeshStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType, NodeStackOp, NodeStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.vertex_buffer_layout import VertexBufferLayoutStruct


def extract_legacy_materials(attribute_arr: List[AttributeStruct], shader_arr: List[ChecksumStrStruct], texture_arr: List[ChecksumStrStruct], mesh_arr: List[MeshStruct], abstract_vertex_buffers: List[GMDVertexBuffer]) -> List[GMDMaterial]:
    materials = []
    shader_vb_layouts = {}

    for attr in attribute_arr:
        shader_name = shader_arr[attr.shader_index].text
        textures = {
            GMDMaterialTextureIndex.Diffuse: texture_arr[attr.texture_diffuse.tex_index].text,
            GMDMaterialTextureIndex.Normal: texture_arr[attr.texture_normal.tex_index].text
        }
        # To find the vertex buffer layout, check to see which submeshes use the material and then see what layout is used.
        # Assumed that each shader requires a specific layout.
        if shader_name not in shader_vb_layouts:
            for mesh in mesh_arr:
                if mesh.attribute_index == attr.index:
                    shader_vb_layouts[shader_name] = abstract_vertex_buffers[mesh.vertex_buffer_index].layout
        vertex_buffer_layout = shader_vb_layouts.get(shader_name, None)

        materials.append(GMDMaterial(
            id=attr.index,
            shader_name=shader_name,
            texture_names=textures,
            vertex_buffer_layout=vertex_buffer_layout
        ))

    return materials

def extract_legacy_submeshes(big_endian: bool,
                             mesh_arr: List[MeshStruct], mesh_matrix_bytestrings: bytes, index_data: List[int], materials: List[GMDMaterial],
                             vertex_buffers: List[GMDVertexBuffer], relative_indices_used: bool, vertex_offset_used: bool, bytestrings_are_16bit: bool) -> List[GMDSubmesh]:
    submeshes = []

    if relative_indices_used and not vertex_offset_used:
        raise Exception("extract_legacy_submeshes told that indices are relative, but vertex offset is unused. Indices are relative to what?")

    #print(f"extracting submeshes - relidx {relative_indices_used} vtx off {vertex_offset_used}")

    for mesh_struct in mesh_arr:
        material = materials[mesh_struct.attribute_index]
        if bytestrings_are_16bit:
            # First byte is length in shorts
            bytestr_len = int(mesh_matrix_bytestrings[mesh_struct.matrixlist_offset])
            # TODO: Is extracting this length of data necessary? Could just read with the FixedSizeArrayUnpacker
            start = mesh_struct.matrixlist_offset + 1
            end = start + 2*mesh_struct.matrixlist_length
            bytestr_data = mesh_matrix_bytestrings[start:end]
            relevant_bones, _ = FixedSizeArrayUnpacker(c_uint16, mesh_struct.matrixlist_length).unpack(True, bytestr_data, 0)
        else:
            relevant_bone_bytestr = mesh_matrix_bytestrings[
                                    mesh_struct.matrixlist_offset:mesh_struct.matrixlist_offset + mesh_struct.matrixlist_length + 1]
            relevant_bones = [
                int(x) for x in relevant_bone_bytestr[1:]  # First byte is length, remove it
            ]
        if len(relevant_bones) != mesh_struct.matrixlist_length:
            raise Exception(f"Length of relevant bones bytestring didn't match expected: expected {mesh_struct.matrixlist_length} got {len(relevant_bones)}")
        vtx_buffer = vertex_buffers[mesh_struct.vertex_buffer_index]

        if vertex_offset_used:
            start = mesh_struct.vertex_offset
            cnt = mesh_struct.vertex_count
            vertices = vtx_buffer.vertices[start:start + cnt]

        # This used to reverse endians, but that isn't necessary anymore
        if (not relative_indices_used) and vertex_offset_used:
            #print(f"Making indices relative to {start}")
            parse_index = lambda x: 0xFFFF if x == 0xFFFF else (x - start)
        else:
            parse_index = lambda x: x

        # print(submesh_struct.indices_triangle.extract_range(self.structs.index_data))
        triangle_list_indices = [parse_index(x) for x in
                                 mesh_struct.triangle_list_indices.extract_range(index_data)]
        noreset_strip_indices = [parse_index(x) for x in
                                 mesh_struct.noreset_strip_indices.extract_range(index_data)]
        reset_strip_indices = [parse_index(x) for x in
                               mesh_struct.reset_strip_indices.extract_range(index_data)]

        if not vertex_offset_used:
            # Assume the range of vertices used by this mesh is contiguous and doesn't overlap any other mesh.
            start = min(noreset_strip_indices)
            end = max(noreset_strip_indices)
            # The end of list ranges in Python are exclusive, so add 1 to make sure index=end is included
            vertices = vtx_buffer.vertices[start:end+1]
            # Remap all indices to be relative to this range

            remap_index = lambda x: 0xFFFF if x == 0xFFFF else (x - start)
            triangle_list_indices = [remap_index(x) for x in triangle_list_indices]
            noreset_strip_indices = [remap_index(x) for x in noreset_strip_indices]
            reset_strip_indices = [remap_index(x) for x in reset_strip_indices]

        # TODO: Validations? i.e. check len(vertices) == vertex_count

        submesh = GMDSubmesh(
            material=material,
            relevant_bones=relevant_bones,
            vertices=vertices,
            triangle_indices=triangle_list_indices,
            triangle_strip_noreset_indices=noreset_strip_indices,
            triangle_strip_reset_indices=reset_strip_indices,
            # parent_part=parent_part
        )
        submeshes.append(submesh)

        # parent_part.submeshes.append(submesh)
    return submeshes

def extract_legacy_vertex_buffers(vertex_buffer_arr: List[VertexBufferLayoutStruct], vertex_data: bytes, vertex_big_endian: bool) -> Tuple[List[GMDVertexBuffer], Dict[GMDVertexBufferLayout, VertexBufferLayoutStruct]]:
    vertex_buffers = []
    vertex_buffer_layouts = {}
    vertex_bytes = vertex_data
    for layout in vertex_buffer_arr:
        abstract_layout: GMDVertexBufferLayout = layout.get_vertex_layout()

        if abstract_layout.calc_bytes_per_vertex() != layout.bytes_per_vertex:
            print(f"BPV mismatch: {abstract_layout.calc_bytes_per_vertex()} != layout BPV {layout.bytes_per_vertex}")

        #print(abstract_layout)
        if layout.vertex_count > 2 ** 20:
            print(f"Not going to try and allocate {layout.vertex_count} verts, too big")
        else:
            abstract_buffer = GMDVertexBuffer(
                layout.index,
                layout=abstract_layout,
                vertices=abstract_layout.unpack_vertices(vertex_big_endian, layout.vertex_count, vertex_bytes, layout.vertex_data_offset),
            )
            vertex_buffers.append(abstract_buffer)

        if abstract_layout in vertex_buffer_layouts:
            raise ValueError("Found multiple layout structs that map to the same vertex layout")
        vertex_buffer_layouts[abstract_layout] = layout

    return vertex_buffers, vertex_buffer_layouts

def extract_legacy_node_heirarchy(node_arr: List[NodeStruct], node_name_arr: List[ChecksumStrStruct], matrix_arr: List[Matrix]) -> Dict[int, GMDBone]:
    parent_stack: Deque[int] = collections.deque()
    bone_index_to_object = {}

    for node_struct in node_arr:
        # "Skin" types are objects, and the legacy exporter shouldn't care about objects
        if node_struct.node_type == NodeType.Skin or node_struct.object_index != -1:
            continue

        name = node_name_arr[node_struct.name_index].text
        pos = Vec3(*node_struct.pos[:3])
        rot = Quat(node_struct.rot.x, node_struct.rot.y, node_struct.rot.z, node_struct.rot.w)
        scl = Vec3(*node_struct.scale[:3])
        bone = GMDBone(node_struct.index, name, pos, rot, scl)

        if parent_stack:
            #print(f"parent for {node_struct.index}: {parent_stack[-1]}")
            parent_bone_index = parent_stack[-1]
            parent_bone = bone_index_to_object[parent_bone_index]
            # sanity check
            # if data.node_arr[parent_bone_index].parent_of != node_struct.index
            #    and not any(child)
            bone.set_hierarchy_props(parent_bone, [])
            parent_bone.children.append(bone)
        else:
            bone.set_hierarchy_props(None, [])

        if 0 <= node_struct.matrix_index < len(matrix_arr):
            bone.set_matrix(matrix_arr[node_struct.matrix_index])

        if node_struct.stack_op in [NodeStackOp.Pop, NodeStackOp.PopPush]:
            # print("pop")
            if parent_stack:
                parent_stack.pop()
            else:
                print(f"Corrupted parent stack ops, popping from empty at index {node_struct.index}")
        if node_struct.stack_op in [NodeStackOp.Push, NodeStackOp.PopPush]:
            # print(f"push {node_struct.index}")
            parent_stack.append(node_struct.index)
        # print(f"{parent_stack}")

        bone_index_to_object[bone.id] = bone

    if True:
        # Find bone index infos the normal way to compare it
        root_ids = []
        child_list_dict = collections.defaultdict(lambda: [])
        child_to_parent = {}  # collections.defaultdict(lambda: None)
        for bone_info in node_arr:
            # if bone_info.part_id != -1:
            #    continue #
            # "Skin" types are objects, and the legacy exporter shouldn't care about objects
            if bone_info.node_type == NodeType.Skin or bone_info.object_index != -1:
                continue

            if bone_info.parent_of >= 0:
                child_list_dict[bone_info.index] = [bone_info.parent_of]
                child_to_parent[bone_info.parent_of] = bone_info.index

            if bone_info.sibling_of >= 0:
                # Look up our parent
                parent_id = child_to_parent[bone_info.index]
                # Add our sibling to the child_list_dict
                child_list_dict[parent_id].append(bone_info.sibling_of)
                # Add the mapping for our sibling to the child_to_parent mapping
                child_to_parent[bone_info.sibling_of] = parent_id

            if bone_info.index not in child_to_parent:
                root_ids.append(bone_info.index)

        if set(bone_index_to_object[x] for x in root_ids) != set(x for x in bone_index_to_object.values() if not x.parent):
            print("mismatched roots")
        for idx,bone in bone_index_to_object.items():
            if idx not in child_to_parent and bone.parent is None:
                continue
            expected_parent = bone_index_to_object[child_to_parent[idx]]
            if expected_parent is not bone.parent:
                print(f"Mismatched parents for {bone.name}: expected {expected_parent.name} got {bone.parent.name}")
    #for i,bone in bone_index_to_object.items():
    #    if bone.children:
    #        expected_parent_of_value = min(b.index for b in )

    # print(f"Parent stack after hitting bone_index_to_object")
    return bone_index_to_object