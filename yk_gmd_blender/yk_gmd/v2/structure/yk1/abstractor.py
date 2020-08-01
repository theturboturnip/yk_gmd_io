import time
from collections import Iterator
from typing import List, Iterable, Tuple, Dict

from mathutils import Quaternion

from yk_gmd_blender.structurelib.primitives import c_uint16
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDUnk12
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene, HierarchyData
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_object import GMDUnskinnedObject
from yk_gmd_blender.yk_gmd.v2.structure.common.abstractor import build_vertex_buffers_from_structs, \
    build_shaders_from_structs, build_materials_from_structs, build_index_mapping, \
    build_meshes_from_structs, build_object_nodes, build_skeleton_bones_from_structs, arrange_data_for_export, \
    RearrangedData, pack_mesh_matrix_strings
from yk_gmd_blender.yk_gmd.v2.structure.common.attribute import AttributeStruct, TextureIndexStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStrStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import IndicesStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeStruct, NodeType
from yk_gmd_blender.yk_gmd.v2.structure.common.unks import Unk12Struct, Unk14Struct
from yk_gmd_blender.yk_gmd.v2.structure.version import VersionProperties
from yk_gmd_blender.yk_gmd.v2.structure.yk1.bbox import BoundsDataStruct_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.file import FileData_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.mesh import MeshStruct_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.object import ObjectStruct_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.vertex_buffer_layout import VertexBufferLayoutStruct_YK1


def bounds_of(mesh) -> BoundsDataStruct_YK1:
    pass

def combine_bounds(bounds: Iterable[BoundsDataStruct_YK1]) -> BoundsDataStruct_YK1:
    pass


def pack_abstract_contents_YK1(version_properties: VersionProperties, file_big_endian: bool, vertices_big_endian: bool, scene: GMDScene) -> FileData_YK1:
    rearranged_data: RearrangedData = arrange_data_for_export(scene)

    packed_mesh_matrix_strings, packed_mesh_matrix_strings_index = pack_mesh_matrix_strings(rearranged_data.mesh_matrixlist_index)

    # Set >255 bones flag
    int16_bone_indices = len([x for x in rearranged_data.ordered_nodes if isinstance(x, GMDBone)])

    node_arr = []
    for i, (gmd_node, stack_op) in enumerate(rearranged_data.ordered_nodes):
        parent_of = -1 if not gmd_node.children else rearranged_data.node_id_to_node_index[id(gmd_node.children[0])]
        sibling_of = -1
        if gmd_node.parent:
            this_node_child_index = gmd_node.parent.children.index(gmd_node)
            if this_node_child_index != len(gmd_node.parent.children) - 1:
                sibling_of = rearranged_data.node_id_to_node_index[id(gmd_node.parent.children[this_node_child_index+1])]

        if gmd_node.node_type == NodeType.MatrixTransform:
            object_index = -1
        else:
            object_index = rearranged_data.node_id_to_object_index[id(gmd_node)]

        if isinstance(gmd_node, (GMDBone, GMDUnskinnedObject)):
            matrix_index = rearranged_data.object_id_to_matrix_index[id(gmd_node)]
        else:
            matrix_index = -1

        if isinstance(gmd_node, GMDBone):
            bone_pos = gmd_node.bone_pos
            bone_axis = gmd_node.bone_axis
        else:
            bone_pos = gmd_node.pos
            bone_pos.w = 1
            bone_axis = Quaternion((0,0,0,0))
            pass

        node_arr.append(NodeStruct(
            index=i,
            parent_of=parent_of,
            sibling_of=sibling_of,
            object_index=object_index,
            matrix_index=matrix_index,
            stack_op=stack_op,
            name_index=rearranged_data.node_names_index[gmd_node.name],
            node_type=gmd_node.node_type,

            pos=gmd_node.pos,
            rot=gmd_node.rot,
            scale=gmd_node.scale,

            bone_pos=bone_pos,
            bone_axis=bone_axis,
            # TODO: GMD Node Flags
            flags=[0,0,0,0],
        ))

    vertex_buffer_arr = []
    vertex_data_bytearray = bytearray()
    index_buffer = List[int]
    mesh_arr = []
    for buffer_idx, (gmd_buffer_layout, packing_flags, meshes_for_buffer) in enumerate(rearranged_data.vertex_layout_groups):
        buffer_vertex_count=sum(m.vertices_data.vertex_count() for m in meshes_for_buffer)

        vertex_buffer_arr.append(VertexBufferLayoutStruct_YK1(
            index=buffer_idx,

            vertex_count=buffer_vertex_count,

            vertex_packing_flags=packing_flags,
            bytes_per_vertex=gmd_buffer_layout.bytes_per_vertex(),

            vertex_data_offset=len(vertex_data_bytearray),
            vertex_data_length=buffer_vertex_count * gmd_buffer_layout.bytes_per_vertex(),
        ))

        vertex_buffer_length = 0

        for gmd_mesh in meshes_for_buffer:
            object_index = rearranged_data.mesh_id_to_object_index[id(gmd_mesh)]
            node = rearranged_data.ordered_objects[object_index]
            node_index = rearranged_data.node_id_to_node_index[id(node)]

            vertex_offset = vertex_buffer_length
            vertex_count = len(gmd_mesh.vertices_data)
            gmd_mesh.vertices_data.layout.pack_into(vertices_big_endian, gmd_mesh.vertices_data, vertex_data_bytearray)
            vertex_buffer_length += vertex_count

            if isinstance(gmd_mesh, GMDSkinnedMesh):
                matrix_list = rearranged_data.mesh_id_to_matrixlist[id(gmd_mesh)]
            else:
                matrix_list = []

            if version_properties.relative_indices_used:
                pack_index = lambda x: x
            else:
                pack_index = lambda x: 0xFFFF if x == 0xFFFF else (x + vertex_offset)

            # Set up the pointer for the next set of indices
            triangle_indices = IndicesStruct(
                index_offset=len(index_buffer),
                index_count=len(gmd_mesh.triangle_indices)
            )
            # then add them to the data
            index_buffer += [pack_index(x) for x in gmd_mesh.triangle_indices]

            # Set up the pointer for the next set of indices
            triangle_strip_noreset_indices = IndicesStruct(
                index_offset=len(index_buffer),
                index_count=len(gmd_mesh.triangle_strip_noreset_indices)
            )
            # then add them to the data
            index_buffer += [pack_index(x) for x in gmd_mesh.triangle_strip_noreset_indices]

            # Set up the pointer for the next set of indices
            triangle_strip_reset_indices = IndicesStruct(
                index_offset=len(index_buffer),
                index_count=len(gmd_mesh.triangle_strip_reset_indices)
            )
            # then add them to the data
            index_buffer += [pack_index(x) for x in gmd_mesh.triangle_strip_reset_indices]

            mesh_arr.append(MeshStruct_YK1(
                index=len(mesh_arr),
                attribute_index=rearranged_data.attribute_set_id_to_index[id(gmd_mesh.attribute_set)],
                vertex_buffer_index=buffer_idx,
                object_index=object_index,
                node_index=node_index,

                matrixlist_offset=packed_mesh_matrix_strings_index[tuple(matrix_list)] if matrix_list else 0,
                matrixlist_length=len(matrix_list),

                vertex_offset=vertex_offset,
                vertex_count=vertex_count,

                triangle_list_indices=triangle_indices,
                noreset_strip_indices=triangle_strip_noreset_indices,
                reset_strip_indices=triangle_strip_reset_indices,
            ))

        pass

    obj_arr = []
    # This isn't going to have duplicates -> don't bother with the packing
    drawlist_bytearray = bytearray()
    for i, obj in enumerate(rearranged_data.ordered_objects):

        mesh_bounds = combine_bounds([bounds_of(gmd_mesh) for gmd_mesh in obj.mesh_list])
        node_index = rearranged_data.node_id_to_node_index[id(obj)]

        drawlist_rel_ptr = len(drawlist_bytearray)
        c_uint16.pack(file_big_endian, len(obj.mesh_list), drawlist_bytearray)
        c_uint16.pack(file_big_endian, 0, drawlist_bytearray)
        for i, mesh in enumerate(obj.mesh_list):
            c_uint16.pack(file_big_endian, rearranged_data.attribute_set_id_to_index[id(mesh.attribute_set)], drawlist_bytearray)
            c_uint16.pack(file_big_endian, rearranged_data.mesh_id_to_index[id(mesh)], drawlist_bytearray)

        obj_arr.append(ObjectStruct_YK1(
            index=i,
            node_index_1=node_index,
            node_index_2=node_index, # TODO: This could be a matrix index - I'm pretty sure those are interchangeable
            drawlist_rel_ptr=drawlist_rel_ptr,

            bbox=mesh_bounds,
        ))
    overall_bounds = combine_bounds(obj.bbox for obj in obj_arr)

    material_arr = []
    for gmd_material in rearranged_data.ordered_materials:
        material_arr.append(gmd_material.port_to_version(version_properties.major_version))
    unk12_arr = []
    unk14_arr = []
    attribute_arr = []
    make_texture_index = lambda s: TextureIndexStruct(rearranged_data.texture_names_index[s] if s else -1)
    for i, gmd_attribute_set in enumerate(rearranged_data.ordered_attribute_sets):
        unk12_arr.append(Unk12Struct(
            data=gmd_attribute_set.unk12.port_to_version(version_properties.major_version)
                    if gmd_attribute_set.unk12 else GMDUnk12.get_default()
        ))
        unk14_arr.append(Unk14Struct(
            data=gmd_attribute_set.unk14.port_to_version(version_properties.major_version)
            if gmd_attribute_set.unk14 else GMDUnk12.get_default()
        ))

        mesh_range = rearranged_data.attribute_set_id_to_mesh_index_range[id(gmd_attribute_set)]
        attribute_arr.append(AttributeStruct(
            index=i,
            material_index=rearranged_data.material_id_to_index[id(gmd_attribute_set.material)],
            shader_index=rearranged_data.shader_names_index[gmd_attribute_set.shader.name],

            # Which meshes use this material - offsets in the Mesh_YK1 array
            mesh_indices_start=mesh_range[0],
            mesh_indices_count=mesh_range[1] - mesh_range[0],

            texture_init_count=8, # TODO: Set this properly?
            flags=gmd_attribute_set.attr_flags,
            extra_properties=gmd_attribute_set.attr_extra_properties,

            texture_diffuse=make_texture_index(gmd_attribute_set.texture_diffuse),
            texture_refl=make_texture_index(gmd_attribute_set.texture_refl),
            texture_multi=make_texture_index(gmd_attribute_set.texture_multi),
            texture_unk1=make_texture_index(gmd_attribute_set.texture_unk1),
            texture_ts=make_texture_index(gmd_attribute_set.texture_rs), # TODO: ugh, name mismatch
            texture_normal=make_texture_index(gmd_attribute_set.texture_normal),
            texture_rt=make_texture_index(gmd_attribute_set.texture_rt),
            texture_rd=make_texture_index(gmd_attribute_set.texture_rd),
        ))

    file_endian_check = 1 if file_big_endian else 0
    vertex_endian_check = 1 if vertices_big_endian else 0

    flags = [0, 0, 0, 0, 0, 0]
    if int16_bone_indices:
        flags[5] |= 0x8000_0000
    else:
        flags[5] &= ~0x8000_0000
    # TODO: This is in all(?) Yakuza Kiwami 1 files
    # It could be worth passing on the flags from original files if we're still exporting "over" them
    flags[5] |= 0x20

    return FileData_YK1(
        magic="GSGM",
        file_endian_check=file_endian_check,
        vertex_endian_check=vertex_endian_check,
        version_combined=version_properties.combined_version(),

        name=ChecksumStrStruct.make_from_str(scene.name),

        overall_bounds=overall_bounds,

        node_arr=node_arr,
        obj_arr=obj_arr,
        mesh_arr=mesh_arr,
        attribute_arr=attribute_arr,
        material_arr=material_arr,
        matrix_arr=rearranged_data.ordered_matrices,
        vertex_buffer_arr=vertex_buffer_arr,
        vertex_data=bytes(vertex_data_bytearray),
        texture_arr=rearranged_data.texture_names,
        shader_arr=rearranged_data.shader_names,
        node_name_arr=rearranged_data.node_names,
        index_data=index_buffer,
        meshset_data=bytes(drawlist_bytearray),
        mesh_matrix_bytestrings=packed_mesh_matrix_strings,

        unk12=unk12_arr,
        unk13=rearranged_data.root_node_indices,
        unk14=unk14_arr,
        flags=flags,
    )


def read_abstract_contents_YK1(version_properties: VersionProperties, file_data: FileData_YK1) -> GMDScene:
    start_time = time.time()

    bytestrings_are_16bit = bool(file_data.flags[5] & 0x8000_0000)
    vertices_are_big_endian = file_data.vertices_are_big_endian()

    abstract_vertex_buffers = build_vertex_buffers_from_structs(version_properties,
                                                                file_data.vertex_buffer_arr, file_data.vertex_data,
                                                                vertices_are_big_endian)
    print(f"Time after build_vertex_buffers_from_structs: {time.time() - start_time}")

    abstract_shaders = build_shaders_from_structs(version_properties,

                                                  abstract_vertex_buffers,

                                                  file_data.mesh_arr, file_data.attribute_arr,
                                                  file_data.shader_arr)

    print(f"Time after build_shaders_from_structs: {time.time() - start_time}")

    abstract_attributes = build_materials_from_structs(version_properties,

                                                      abstract_shaders,

                                                      file_data.attribute_arr, file_data.material_arr,
                                                      file_data.unk12, file_data.unk14,
                                                      file_data.texture_arr)

    print(f"Time after build_materials_from_structs: {time.time() - start_time}")

    abstract_skeleton_bones, remaining_nodes = build_skeleton_bones_from_structs(version_properties,

                                                                                 file_data.node_arr,
                                                                                 file_data.node_name_arr,
                                                                                 file_data.matrix_arr)

    print(f"Time after build_skeleton_bones_from_structs: {time.time() - start_time}")

    abstract_meshes = build_meshes_from_structs(version_properties,

                                                abstract_attributes, abstract_vertex_buffers, abstract_skeleton_bones,

                                                file_data.mesh_arr, file_data.index_data, file_data.mesh_matrix_bytestrings,
                                                bytestrings_are_16bit)

    print(f"Time after build_meshes_from_structs: {time.time() - start_time}")

    object_drawlist_ptrs = [
        o.drawlist_rel_ptr
        for o in file_data.obj_arr
    ]
    skinned_abstract_objects, unskinned_abstract_objects = build_object_nodes(version_properties,

                                                                              abstract_meshes, abstract_attributes,

                                                                              remaining_nodes, file_data.node_name_arr,
                                                                              object_drawlist_ptrs,
                                                                              file_data.matrix_arr,
                                                                              file_data.meshset_data,
                                                                              big_endian=file_data.file_is_big_endian())

    abstract_bones_roots = [b for b in abstract_skeleton_bones if not b.parent]
    skinned_roots = [s for s in skinned_abstract_objects if not s.parent]
    unskinned_roots = [s for s in unskinned_abstract_objects if not s.parent]

    overall_roots = abstract_bones_roots + skinned_roots + unskinned_roots

    return GMDScene(
        name=file_data.name.text,

        overall_heirarchy=HierarchyData[GMDNode](overall_roots),

        bones=HierarchyData(abstract_bones_roots) if abstract_bones_roots else None,
        skinned_objects=HierarchyData(skinned_roots) if skinned_roots else None,
        unskinned_objects=HierarchyData(unskinned_roots) if unskinned_roots else None,
    )