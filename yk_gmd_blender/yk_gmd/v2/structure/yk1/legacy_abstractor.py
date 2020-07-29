import collections
from collections import deque
from dataclasses import dataclass
from typing import List, Dict, Tuple, Deque

from mathutils import Vector, Quaternion

from yk_gmd_blender.structurelib.base import FixedSizeArrayUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint16
from yk_gmd_blender.yk_gmd.v2.structure.common.legacy_abstractor import extract_legacy_node_heirarchy, \
    extract_legacy_vertex_buffers, extract_legacy_materials, extract_legacy_submeshes
from yk_gmd_blender.yk_gmd.v2.structure.common.attribute import AttributeStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStrStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.file import FileData_Common
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import MeshStruct, IndicesStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeStackOp, NodeStruct, NodeType
from yk_gmd_blender.yk_gmd.v2.structure.version import FileProperties
from yk_gmd_blender.yk_gmd.v2.structure.yk1.file import FileData_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.mesh import MeshStruct_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.object import ObjectStruct_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.vertex_buffer_layout import VertexBufferLayoutStruct_YK1
from yk_gmd_blender.yk_gmd.legacy.abstract.bone import GMDBone
from yk_gmd_blender.yk_gmd.legacy.abstract.material import GMDMaterial, GMDMaterialTextureIndex
from yk_gmd_blender.yk_gmd.legacy.abstract.scene import GMDScene
from yk_gmd_blender.yk_gmd.legacy.abstract.submesh import GMDSubmesh
from yk_gmd_blender.yk_gmd.legacy.abstract.vector import Vec3, Quat, Vec4
from yk_gmd_blender.yk_gmd.legacy.abstract.vertices import GMDVertexBuffer, GMDVertexBufferLayout, GMDVertex, BoneWeight

__all__ = [
    "convert_YK1_to_legacy_abstraction",
    "package_legacy_abstraction_to_YK1",
]


# NOTE - object indices are important!!! they must be maintained
def convert_YK1_to_legacy_abstraction(data: FileData_YK1, version_props: FileProperties) -> GMDScene:
    # get bones
    node_index_map = extract_legacy_node_heirarchy(data.node_arr, data.node_name_arr, data.matrix_arr)
    node_name_map = {b.name: b for b in node_index_map.values()}
    node_roots = [b for b in node_index_map.values() if not b.parent]

    # get vertex buffers
    vertices_big_endian = data.vertices_are_big_endian()
    vertex_buffers, abstract_vb_layout_to_struct = extract_legacy_vertex_buffers(data.vertex_buffer_arr, data.vertex_data, vertices_big_endian)
    # get materials
    materials = extract_legacy_materials(data.attribute_arr, data.shader_arr, data.texture_arr, data.mesh_arr, vertex_buffers)
    # get submeshes/parts
    #submeshes = extract_legacy_submeshes(data.mesh_arr, data.mesh_matrix_bytestrings, data.index_data, materials, vertex_buffers,
    #                                     relative_indices_used=version_props.relative_indices_used,
    #                                     vertex_offset_used=version_props.vertex_offset_used)
    bytestrings_16bit = bool(data.flags[5] & 0x8000_0000)
    submeshes = extract_legacy_submeshes(data.file_is_big_endian(),
                                         data.mesh_arr, data.mesh_matrix_bytestrings, data.index_data, materials,
                                         vertex_buffers,
                                         relative_indices_used=version_props.relative_indices_used,
                                         vertex_offset_used=version_props.vertex_offset_used,
                                         bytestrings_are_16bit=bytestrings_16bit)

    return GMDScene(
        name=data.name.text,

        bone_roots=node_roots,
        bone_index_map=node_index_map,
        bone_name_map=node_name_map,

        vertex_buffers=vertex_buffers,
        submeshes=submeshes,
        materials=materials,
        abstract_vb_layout_to_struct=abstract_vb_layout_to_struct,
    )


def _generate_legacy_submesh_list(scene: GMDScene) -> List[GMDSubmesh]:
    total_submeshes = scene.submeshes[:]

    # Add a null submesh for each unused material so each material is used
    v = GMDVertex()
    v.pos = Vec3(0, 0, 0)
    v.normal = v.tangent = Vec4(0, 0, 0, 1)
    v.uv0 = (0, 0)
    v.uv1 = (0, 0)
    v.col0 = Vec4(0, 0, 0, 0)
    v.col1 = Vec4(0, 0, 0, 0)
    v.weights = (
        BoneWeight(bone=0, weight=1.0),
        BoneWeight(bone=0, weight=0.0),
        BoneWeight(bone=0, weight=0.0),
        BoneWeight(bone=0, weight=0.0),
    )

    for material in scene.materials:
        if len([s for s in total_submeshes if s.material.id == material.id]) > 0:
            # A submesh already exists for this, so don't make a new one
            continue
            # pass
        sm = GMDSubmesh(
            material=material,
            relevant_bones=[0],
            vertices=[v, v, v],
            triangle_indices=[0, 1, 2],
            triangle_strip_noreset_indices=[0, 1, 2],
            triangle_strip_reset_indices=[0, 1, 2],
            # parent_part=null_part
        )
        total_submeshes.append(sm)

    # TODO: Check sort order for when multiple layouts are present - vertex buffers should be arranged according to material layout.
    #print([len(s.vertices) for s in total_submeshes])
    total_submeshes.sort(key=lambda s: s.material.id)
    #print([len(s.vertices) for s in total_submeshes])
    return total_submeshes

#
# @dataclass
# class IndependentBuiltScene:
#     texture_names: List[ChecksumStr]
#     shader_names: List[ChecksumStr]
#     node_names: List[ChecksumStr]
#
#     nodes: List[Node]
#     global_object_node: Node
#
# def make_common_built_scene(global_object_name: str) -> IndependentBuiltScene:
#

def package_legacy_abstraction_to_YK1(big_endian: bool, version_props: FileProperties, initial_data: FileData_YK1, scene: GMDScene) -> FileData_YK1:
    # Check vertex endianness
    # TODO: Add function to FileData to do this logic
    vertices_big_endian = initial_data.vertices_are_big_endian()
    bytestrings_16bit = bool(initial_data.flags[5] & 0x8000_0000)

    # Generate string pool
    texture_names = initial_data.texture_arr[:]
    shader_names = initial_data.shader_arr[:]
    node_names = initial_data.node_name_arr[:]

    # Generate nodes and global object
    nodes = [n for n in initial_data.node_arr if n.object_index == -1]
    # Check that the indices are in a [0...n] range
    if [n.index for n in nodes] != [x for x in range(len(nodes))]:
        raise Exception("stripping non-bone nodes from initial data led to index discrepancy")
    global_object_node = NodeStruct(
        index=len(nodes),
        parent_of=-1,
        sibling_of=-1,
        object_index=0,
        matrix_index=len(nodes),  # TODO: Does changing this do anything?
        stack_op=NodeStackOp.PopPush,
        name_index=len(node_names),
        node_type=NodeType.SkinnedMesh,

        pos=Vector((0, 0, 0, 0)),
        rot=Quaternion(),
        scale=Vector((1, 1, 1, 0)),

        bone_pos=Vector((0, 0, 0, 1)),
        bone_axis=Quaternion(),
        padding=Vector((0, 0, 0, 0))
    )
    node_names.append(ChecksumStrStruct.make_from_str("[l0]global_object"))
    nodes.append(global_object_node)

    total_submeshes = _generate_legacy_submesh_list(scene)
    vb_layouts = {v for v in scene.abstract_vb_layout_to_struct.keys()}
    # Sort vb_layouts so that the largest packing flag is first
    vb_layouts = sorted(vb_layouts, key=lambda v: scene.abstract_vb_layout_to_struct[v].vertex_packing_flags, reverse=True)
    vb_layout_submeshes: List[Tuple[GMDVertexBufferLayout, List[GMDSubmesh]]] = []
    for layout in vb_layouts:
        vb_submeshes = [s for s in total_submeshes if s.material.vertex_buffer_layout == layout]
        vb_layout_submeshes.append((layout, vb_submeshes))
        pass
    total_submeshes = sum((sms for vbl, sms in vb_layout_submeshes), [])

    # HACK - This puts all meshes under a single object
    global_object = ObjectStruct_YK1(
        index=0,
        node_index_1=global_object_node.index,
        node_index_2=global_object_node.index,
        drawlist_rel_ptr=0,
        bbox=initial_data.overall_bounds  # TODO: calculate bounds?
    )
    global_drawlist = bytearray()
    c_uint16.pack(big_endian, len(total_submeshes), global_drawlist)
    c_uint16.pack(big_endian, 0, global_drawlist)
    for i, submesh in enumerate(total_submeshes):
        c_uint16.pack(big_endian, submesh.material.id, global_drawlist)
        c_uint16.pack(big_endian, i, global_drawlist)
    drawlist_bytes = bytes(global_drawlist)
    object_arr = [global_object]

    vertex_buffer_layout_structs: List[VertexBufferLayoutStruct_YK1] = []
    overall_vertex_buffer_data = bytearray()
    overall_index_buffer_data: List[int] = []
    submesh_structs: List[MeshStruct] = []
    submesh_bonelists = bytearray()

    for abstract_layout, vb_submeshes in vb_layout_submeshes:
        # Create a copy of the correct layout structure, in case we've reordered it or something
        original = scene.abstract_vb_layout_to_struct[abstract_layout]
        layout_index = len(vertex_buffer_layout_structs)
        layout_vertex_count = sum(len(s.vertices) for s in vb_submeshes)
        layout_vertex_data_offset = len(overall_vertex_buffer_data)
        layout_vertex_data_length = layout_vertex_count * original.bytes_per_vertex

        layout_struct = VertexBufferLayoutStruct_YK1(
            index=layout_index,
            vertex_count=layout_vertex_count,
            vertex_packing_flags=original.vertex_packing_flags,
            bytes_per_vertex=original.bytes_per_vertex,
            vertex_data_offset=layout_vertex_data_offset,
            vertex_data_length=layout_vertex_data_length,
        )
        vertex_buffer_layout_structs.append(layout_struct)

        vertex_buffer_data = bytearray()
        current_vertex_count = 0

        for s in vb_submeshes:
            # submesh_struct.id = len(submesh_structs)
            # submesh_struct.material_id = s.material.id
            # submesh_struct.vertex_buffer_id = layout_struct.id
            # submesh_struct.vertex_count = len(s.vertices)

            # Set up the pointer for the next set of vertices
            vertex_offset = current_vertex_count
            # then add the data
            vertex_buffer_data += abstract_layout.pack_vertices(vertices_big_endian, s.vertices)
            current_vertex_count += len(s.vertices)

            #print(vertex_offset)
            # relative indices == true
            # TODO: Update this once Kenzan export is enabled
            if version_props.relative_indices_used:
                pack_index = lambda x: x
            else:
                pack_index = lambda x: 0xFFFF if x == 0xFFFF else (x + vertex_offset)

            # Set up the pointer for the next set of indices
            triangle_indices = IndicesStruct(
                index_offset=len(overall_index_buffer_data),
                index_count=len(s.triangle_indices)
            )
            # then add them to the data
            overall_index_buffer_data += [pack_index(x) for x in s.triangle_indices]

            # Set up the pointer for the next set of indices
            triangle_strip_noreset_indices = IndicesStruct(
                index_offset=len(overall_index_buffer_data),
                index_count=len(s.triangle_strip_noreset_indices)
            )
            # then add them to the data
            overall_index_buffer_data += [pack_index(x) for x in s.triangle_strip_noreset_indices]

            # Set up the pointer for the next set of indices
            triangle_strip_reset_indices = IndicesStruct(
                index_offset=len(overall_index_buffer_data),
                index_count=len(s.triangle_strip_reset_indices)
            )
            # then add them to the data
            overall_index_buffer_data += [pack_index(x) for x in s.triangle_strip_reset_indices]

            # Set up the pointer for the next list of bones
            bonelist_length = len(s.relevant_bones)
            bonelist_start = len(submesh_bonelists)
            # then add them to the data
            # TODO: Check that at least one bone is assigned?
            # TODO: The actual engine reuses strings, that might be cool here?
            if bytestrings_16bit:
                bonelist_arr = bytearray()
                bonelist_arr += bytes([len(s.relevant_bones)])
                FixedSizeArrayUnpacker(c_uint16, len(s.relevant_bones)).pack(big_endian=True, value=s.relevant_bones, append_to=bonelist_arr)
                submesh_bonelists += bytes(bonelist_arr)
            else:
                submesh_bonelists += bytes([len(s.relevant_bones)] + s.relevant_bones)

            submesh_structs.append(MeshStruct_YK1(
                index=len(submesh_structs),
                attribute_index=s.material.id,
                vertex_buffer_index=layout_struct.index,
                object_index=global_object.index,
                node_index=global_object_node.index,

                vertex_count=len(s.vertices),
                vertex_offset=vertex_offset,

                triangle_list_indices=triangle_indices,
                noreset_strip_indices=triangle_strip_noreset_indices,
                reset_strip_indices=triangle_strip_reset_indices,

                matrixlist_offset=bonelist_start,
                matrixlist_length=bonelist_length,
            ))

        overall_vertex_buffer_data += vertex_buffer_data

    # Update material structs
    new_attribute_packs = []
    for i, attribute in enumerate(initial_data.attribute_arr):
        # TODO: It seems that this doesn't matter
        indices_using_mat = [i for i, s in enumerate(total_submeshes) if s.material.id == attribute.index]
        new_attribute_packs.append(AttributeStruct(
            index=i,
            material_index=attribute.material_index,
            shader_index=attribute.shader_index,
            meshset_start=indices_using_mat[0],
            meshset_count=len(indices_using_mat),
            unk1=attribute.unk1,
            unk2=attribute.unk2,

            flags=attribute.flags,
            padding=attribute.padding,

            texture_diffuse=attribute.texture_diffuse,
            texture_refl_cubemap=attribute.texture_refl_cubemap,
            texture_multi=attribute.texture_multi,
            texture_unk1=attribute.texture_unk1,
            texture_unk2=attribute.texture_unk2,
            texture_normal=attribute.texture_normal,
            texture_rt=attribute.texture_rt,
            texture_rd=attribute.texture_rd,

            extra_properties=attribute.extra_properties
        ))
        pass

    new_filedata = FileData_YK1(
        magic=initial_data.magic,
        file_endian_check=initial_data.file_endian_check,
        vertex_endian_check=initial_data.vertex_endian_check,
        # padding=initial_data.padding,
        version_combined=initial_data.version_combined,
        # file_size=initial_data.file_size,
        name=initial_data.name,

        node_arr=nodes,
        obj_arr=object_arr,
        mesh_arr=submesh_structs,
        attribute_arr=new_attribute_packs,
        material_arr=initial_data.material_arr,
        matrix_arr=initial_data.matrix_arr,
        vertex_buffer_arr=vertex_buffer_layout_structs,
        vertex_data=bytes(overall_vertex_buffer_data),
        texture_arr=texture_names,
        shader_arr=shader_names,
        node_name_arr=node_names,
        index_data=overall_index_buffer_data,
        meshset_data=drawlist_bytes,
        mesh_matrix_bytestrings=bytes(submesh_bonelists),

        overall_bounds=initial_data.overall_bounds,  # TODO: Bounds calcs
        unk12=initial_data.unk12,
        unk13=initial_data.unk13,
        unk14=initial_data.unk14,
        flags=initial_data.flags,
    )

    # self.structs.vertex_buffer_layouts = GMDArray[VertexBufferLayoutStruct](vertex_buffer_layout_structs)
    # self.structs.vertex_data = GMDArray[ctypes.c_uint8]([ctypes.c_uint8(x) for x in overall_vertex_buffer_data])
    # # Find the index type because it could be big endian or little
    # index_type = self.structs.index_data.elem_type()
    # print(type(overall_index_buffer_data[0]))
    # correctly_typed_index_data = [index_type(x) for x in overall_index_buffer_data]
    # self.structs.index_data = GMDArray[ctypes.c_uint16](correctly_typed_index_data)
    # self.structs.submeshes = GMDArray[SubmeshStruct](submesh_structs)
    # print(sorted(self.structs.submesh_bone_lists.items))
    # print(sorted(submesh_bonelists))
    # self.structs.submesh_bone_lists = GMDVarLenArray(submesh_bonelists)
    #
    # # Delete all "parts" except for the first
    # self.structs.parts.items = self.structs.parts.items[:1]
    # # This first part will always use the first unk10 entry for draw lists, so we can replace the whole unk10 area
    # # Unk10 = set of big-endian uint16s
    # new_unk10 = [len(self.structs.submeshes), 0]
    # for submesh_struct in self.structs.submeshes:
    #     new_unk10.append(submesh_struct.material_id)
    #     new_unk10.append(submesh_struct.id)
    # new_unk10_bytes = bytearray()
    # for item in new_unk10:
    #     new_unk10_bytes += struct.pack(">H", item)
    # self.structs.unk10.items = [ctypes.c_uint8(x) for x in new_unk10_bytes]
    # print(self.structs.unk10.items)

    # Packing into a file should
    # - Update vertex buffers
    # - Update index buffers
    # - Update vertex buffer counts etc. without changing layout
    # - Update submeshes
    # - Update submesh bone lists
    # - CANNOT update texture names - IDs are important too, and we don't know how to change them
    # TODO - ask in the discord how texture modding is usually done
    # - Update bone transforms and matrices
    # everything else should remain intact
    return new_filedata
