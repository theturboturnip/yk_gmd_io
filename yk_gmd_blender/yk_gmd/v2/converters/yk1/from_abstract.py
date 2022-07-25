from typing import Iterable

from mathutils import Quaternion, Vector

from yk_gmd_blender.structurelib.base import PackingValidationError
from yk_gmd_blender.structurelib.primitives import c_uint16
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDUnk12
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_object import GMDUnskinnedObject
from yk_gmd_blender.yk_gmd.v2.converters.common.from_abstract import RearrangedData, arrange_data_for_export, \
    pack_mesh_matrix_strings
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter
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


def bounds_from_minmax(min_pos: Vector, max_pos: Vector) -> BoundsDataStruct_YK1:
    box_rotation = Quaternion()
    box_rotation.identity()

    center = (min_pos + max_pos) / 2
    box_extents = (max_pos - center)
    sphere_radius = (box_extents).length

    return BoundsDataStruct_YK1(
        center=center,
        sphere_radius=sphere_radius,
        box_extents=box_extents,
        box_rotation=box_rotation
    )


def bounds_of(mesh) -> BoundsDataStruct_YK1:
    # min_pos = Vector(mesh.vertices_data.pos[0])
    # max_pos = Vector(mesh.vertices_data.pos[0])
    #
    # for pos in mesh.vertices_data.pos:
    #     min_pos.x = min(pos.x, min_pos.x)
    #     min_pos.y = min(pos.y, min_pos.y)
    #     min_pos.z = min(pos.z, min_pos.z)
    #
    #     max_pos.x = max(pos.x, max_pos.x)
    #     max_pos.y = max(pos.y, max_pos.y)
    #     max_pos.z = max(pos.z, max_pos.z)

    min_pos = Vector((-1000, -1000, -1000))
    max_pos = Vector((+1000, +1000, +1000))

    return bounds_from_minmax(min_pos, max_pos)


def combine_bounds(bounds: Iterable[BoundsDataStruct_YK1]) -> BoundsDataStruct_YK1:
    # min_pos = None
    # max_pos = None
    min_pos = Vector((-1000, -1000, -1000))
    max_pos = Vector((+1000, +1000, +1000))

    for bound in bounds:
        min_for_bound = bound.center - bound.box_extents
        max_for_bound = bound.center - bound.box_extents

        if min_pos is None:
            min_pos = min_for_bound
            max_pos = max_for_bound
        else:
            min_pos.x = min(min_for_bound.x, min_pos.x)
            min_pos.y = min(min_for_bound.y, min_pos.y)
            min_pos.z = min(min_for_bound.z, min_pos.z)

            max_pos.x = max(max_for_bound.x, max_pos.x)
            max_pos.y = max(max_for_bound.y, max_pos.y)
            max_pos.z = max(max_for_bound.z, max_pos.z)

    # TODO - This is for the sake of hierarchy objects which have no meshes themselves, but presumably have children with meshes.
    # Will these BBOXes need to be calculated with those other ones in mind?
    # Will these BBOXes need to be calculated with object position in mind?
    # if min_pos is None:
    #     min_pos = Vector((0, 0, 0, 0))
    #     max_pos = Vector((0, 0, 0, 0))

    return bounds_from_minmax(min_pos, max_pos)


def vec3_to_vec4(vec: Vector, w: float = 0.0):
    return Vector((vec.x, vec.y, vec.z, w))

def pack_abstract_contents_YK1(version_properties: VersionProperties, file_big_endian: bool, vertices_big_endian: bool,
                               scene: GMDScene, error: ErrorReporter, base_flags=(0, 0, 0, 0, 0, 0)) -> FileData_YK1:
    rearranged_data: RearrangedData = arrange_data_for_export(scene, error)

    # Set >255 bones flag
    bones_count = len([x for x, stackop in rearranged_data.ordered_nodes if isinstance(x, GMDBone)])
    int16_bone_indices = bones_count > 255

    if int16_bone_indices:
        error.recoverable(f"This file has >255 bones. Pre-dragon engine titles have not been tested with this value.\n"
                          f"To keep going uncheck \"Strict Export\" in the Export window.")

    packed_mesh_matrixlists, packed_mesh_matrix_strings_index = pack_mesh_matrix_strings(
        rearranged_data.mesh_matrixlist, int16_bone_indices, big_endian=file_big_endian)

    node_arr = []
    for i, (gmd_node, stack_op) in enumerate(rearranged_data.ordered_nodes):
        parent_of = -1 if not gmd_node.children else rearranged_data.node_id_to_node_index[id(gmd_node.children[0])]
        sibling_of = -1
        if gmd_node.parent:
            this_node_child_index = gmd_node.parent.children.index(gmd_node)
            if this_node_child_index != len(gmd_node.parent.children) - 1:
                sibling_of = rearranged_data.node_id_to_node_index[
                    id(gmd_node.parent.children[this_node_child_index + 1])]

        if gmd_node.node_type == NodeType.MatrixTransform:
            object_index = -1
        else:
            object_index = rearranged_data.node_id_to_object_index[id(gmd_node)]

        if isinstance(gmd_node, (GMDBone, GMDUnskinnedObject)):
            matrix_index = rearranged_data.object_id_to_matrix_index[id(gmd_node)]
        else:
            matrix_index = -1

        world_pos = gmd_node.world_pos
        anim_axis = gmd_node.anim_axis
        flags = gmd_node.flags

        node_arr.append(NodeStruct(
            index=i,
            parent_of=parent_of,
            sibling_of=sibling_of,
            object_index=object_index,
            matrix_index=matrix_index,
            stack_op=stack_op,
            name_index=rearranged_data.node_names_index[gmd_node.name],
            node_type=gmd_node.node_type,

            pos=vec3_to_vec4(gmd_node.pos),
            rot=gmd_node.rot,
            scale=vec3_to_vec4(gmd_node.scale),

            world_pos=vec3_to_vec4(world_pos, 1),
            anim_axis=anim_axis,
            flags=flags,
        ))

    vertex_buffer_arr = []
    vertex_data_bytearray = bytearray()
    index_buffer = []
    # Dict of GMDMesh id -> (buffer_id, vertex_offset_from_index, min_index, vertex_count)
    mesh_buffer_stats = {}
    for buffer_idx, (gmd_buffer_layout, packing_flags, meshes_for_buffer) in enumerate(rearranged_data.vertex_layout_groups):
        buffer_vertex_count = sum(m.vertices_data.vertex_count() for m in meshes_for_buffer)

        vertex_buffer_arr.append(VertexBufferLayoutStruct_YK1(
            index=buffer_idx,

            vertex_count=buffer_vertex_count,

            vertex_packing_flags=packing_flags,
            bytes_per_vertex=gmd_buffer_layout.bytes_per_vertex(),

            vertex_data_offset=len(vertex_data_bytearray),
            vertex_data_length=buffer_vertex_count * gmd_buffer_layout.bytes_per_vertex(),
        ))

        # vertex_offset = (vertex_offset_from_index: u32, min_index: u16)
        vertex_offset_from_index = 0
        min_index = 0

        for gmd_mesh in meshes_for_buffer:
            object_index = rearranged_data.mesh_id_to_object_index[id(gmd_mesh)]
            node = rearranged_data.ordered_objects[object_index]

            vertex_count = len(gmd_mesh.vertices_data)
            # We need to store from (min_index, min_index + vertex_count) in a u16
            # If min_index + vertex_count > 65535, we can't store it in a u16
            # (we ensure min_index always fits in u16)
            # => add the current base_index to the vertex_offset_from_index, set new base_index to 0
            # We *could* probably just set min_index = 0 each time, but that's not how RGG does it
            if min_index + vertex_count > 65535:
                vertex_offset_from_index += min_index
                min_index = 0

            if vertex_count > 65535:
                error.fatal(f"Encountered a mesh with more than 65k vertices, needs to be split before it arrives")
            elif vertex_offset_from_index > 4294967295:
                error.fatal(f"Encountered a vertex_offset_from_index greater than 32bit, needs")

            try:
                gmd_mesh.vertices_data.layout.pack_into(vertices_big_endian, gmd_mesh.vertices_data, vertex_data_bytearray)
            except PackingValidationError as e:
                error.fatal(f"Error while packing a mesh for {node.name}: {e}")

            error.debug("MESH_EXPORT", f"(buffer_idx: {buffer_idx}, vertex_offset_from_index: {vertex_offset_from_index}, min_index: {min_index}, vertex_count: {vertex_count})")
            mesh_buffer_stats[id(gmd_mesh)] = (buffer_idx, vertex_offset_from_index, min_index, vertex_count)

            min_index += vertex_count

        pass

    mesh_arr = []
    for gmd_mesh in rearranged_data.ordered_meshes:
        object_index = rearranged_data.mesh_id_to_object_index[id(gmd_mesh)]
        node = rearranged_data.ordered_objects[object_index]
        node_index = rearranged_data.node_id_to_node_index[id(node)]
        (buffer_idx, vertex_offset_from_index, min_index, vertex_count) = mesh_buffer_stats[id(gmd_mesh)]

        if isinstance(gmd_mesh, GMDSkinnedMesh):
            matrix_list = rearranged_data.mesh_id_to_matrixlist[id(gmd_mesh)]
        else:
            matrix_list = []

        if version_properties.relative_indices_used:
            pack_index = lambda x: x
        else:
            pack_index = lambda x: 0xFFFF if x == 0xFFFF else (x + min_index)

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

            min_index=min_index,
            vertex_count=vertex_count,
            vertex_offset_from_index=vertex_offset_from_index,

            triangle_list_indices=triangle_indices,
            noreset_strip_indices=triangle_strip_noreset_indices,
            reset_strip_indices=triangle_strip_reset_indices,
        ))

    obj_arr = []
    # This isn't going to have duplicates -> don't bother with the packing
    drawlist_bytearray = bytearray()
    touched_meshes = set()
    for i, obj in enumerate(rearranged_data.ordered_objects):

        mesh_bounds = combine_bounds([bounds_of(gmd_mesh) for gmd_mesh in obj.mesh_list])
        node_index = rearranged_data.node_id_to_node_index[id(obj)]

        drawlist_rel_ptr = len(drawlist_bytearray)
        c_uint16.pack(file_big_endian, len(obj.mesh_list), drawlist_bytearray)
        c_uint16.pack(file_big_endian, 0, drawlist_bytearray)
        # TODO - is order important here?
        for mesh in obj.mesh_list:
            c_uint16.pack(file_big_endian, rearranged_data.attribute_set_id_to_index[id(mesh.attribute_set)],
                          drawlist_bytearray)
            c_uint16.pack(file_big_endian, rearranged_data.mesh_id_to_index[id(mesh)], drawlist_bytearray)
            touched_meshes.add(id(mesh))

        obj_arr.append(ObjectStruct_YK1(
            index=i,
            node_index_1=node_index,
            node_index_2=node_index,  # TODO: This could be a matrix index - I'm pretty sure those are interchangeable
            drawlist_rel_ptr=drawlist_rel_ptr,

            bbox=mesh_bounds,
        ))
    if len(touched_meshes) != len(mesh_arr):
        error.fatal(f"Didn't export drawlists for all meshes")
    overall_bounds = combine_bounds(obj.bbox for obj in obj_arr)

    material_arr = []
    for gmd_material in rearranged_data.ordered_materials:
        material_arr.append(gmd_material.port_to_version(version_properties.major_version).origin_data)
    unk12_arr = []
    unk14_arr = []
    attribute_arr = []
    make_texture_index = lambda s: TextureIndexStruct(rearranged_data.texture_names_index[s] if s else -1)
    for i, gmd_attribute_set in enumerate(rearranged_data.ordered_attribute_sets):
        unk12_arr.append(Unk12Struct(
            data=gmd_attribute_set.unk12.float_data#.port_to_version(version_properties.major_version).float_data
            if gmd_attribute_set.unk12 else GMDUnk12.get_default()
        ))
        unk14_arr.append(Unk14Struct(
            data=gmd_attribute_set.unk14.int_data#port_to_version(version_properties.major_version).int_data
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

            texture_init_count=8,  # TODO: Set this properly?
            flags=gmd_attribute_set.attr_flags,
            extra_properties=gmd_attribute_set.attr_extra_properties,

            texture_diffuse=make_texture_index(gmd_attribute_set.texture_diffuse),
            texture_refl=make_texture_index(gmd_attribute_set.texture_refl),
            texture_multi=make_texture_index(gmd_attribute_set.texture_multi),
            texture_unk1=make_texture_index(gmd_attribute_set.texture_unk1),
            texture_ts=make_texture_index(gmd_attribute_set.texture_rs),  # TODO: ugh, name mismatch
            texture_normal=make_texture_index(gmd_attribute_set.texture_normal),
            texture_rt=make_texture_index(gmd_attribute_set.texture_rt),
            texture_rd=make_texture_index(gmd_attribute_set.texture_rd),
        ))

    file_endian_check = 1 if file_big_endian else 0
    vertex_endian_check = 1 if vertices_big_endian else 0

    flags = list(base_flags)
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
        object_drawlist_bytes=bytes(drawlist_bytearray),
        mesh_matrixlist_bytes=packed_mesh_matrixlists,

        unk12=unk12_arr,
        unk13=rearranged_data.root_node_indices,
        unk14=unk14_arr,
        flags=flags,
    )

