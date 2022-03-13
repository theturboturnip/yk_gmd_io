# Note - checked=False disables bitchecks but the time taken is the same, dw about it
import abc
import array
import time
from enum import Enum
from typing import List, Tuple, cast, Union, TypeVar, Generic

from mathutils import Matrix

from yk_gmd_blender.structurelib.base import FixedSizeArrayUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint16, c_uint8
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet, GMDUnk14, GMDUnk12, GMDMaterial
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDShader, GMDVertexBufferLayout, GMDVertexBuffer_Generic
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_object import GMDUnskinnedObject, GMDSkinnedObject
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter
from yk_gmd_blender.yk_gmd.v2.structure.common.attribute import AttributeStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStrStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.file import FileData_Common
from yk_gmd_blender.yk_gmd.v2.structure.common.material_base import MaterialBaseStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import IndicesStruct, MeshStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType, NodeStruct, NodeStackOp
from yk_gmd_blender.yk_gmd.v2.structure.common.unks import Unk14Struct, Unk12Struct
from yk_gmd_blender.yk_gmd.v2.structure.common.vertex_buffer_layout import VertexBufferLayoutStruct
from yk_gmd_blender.yk_gmd.v2.structure.version import VersionProperties


class ParentStack:
    def __init__(self):
        self.stack = []

    def handle_node(self, stack_op: NodeStackOp, to_push: GMDNode):
        if stack_op in [NodeStackOp.PopPush, NodeStackOp.Pop]:
            self.stack.pop()
        if stack_op in [NodeStackOp.PopPush, NodeStackOp.Push]:
            self.stack.append(to_push)

    def __bool__(self):
        return bool(self.stack)

    def peek(self) -> GMDNode:
        return self.stack[-1]


TFileData = TypeVar('TFileData', bound=FileData_Common)


class FileImportMode(Enum):
    SKINNED = 0
    UNSKINNED = 1


class VertexImportMode(Enum):
    IMPORT_VERTICES = 0
    # In this mode, vertex buffers will not be unpacked.
    # This is helpful in situations where the data is unnecessary,
    # such as imports for the sake of exporting-over
    NO_VERTICES = 1


class GMDAbstractor_Common(abc.ABC, Generic[TFileData]):
    version_props: VersionProperties
    file_is_big_endian: bool
    vertices_are_big_endian: bool
    file_import_mode: FileImportMode
    vertex_import_mode: VertexImportMode

    error: ErrorReporter

    file_data: TFileData

    def __init__(self, version_props: VersionProperties, file_import_mode: FileImportMode, vertex_import_mode: VertexImportMode, file_data: TFileData, error_reporter: ErrorReporter):
        self.version_props = version_props
        self.file_is_big_endian = file_data.file_is_big_endian()
        self.vertices_are_big_endian = file_data.vertices_are_big_endian()
        self.file_import_mode = file_import_mode
        self.vertex_import_mode = vertex_import_mode
        self.error = error_reporter

        self.file_data = file_data

    def make_abstract_scene(self) -> GMDScene:
        raise NotImplementedError()

    def build_vertex_buffers_from_structs(self,

                                          vertex_layout_arr: List[VertexBufferLayoutStruct], vertex_bytes: bytes,

                                          profile: bool = False) \
            -> List[GMDVertexBuffer_Generic]:
        assume_skinned_vertex_buffers = (self.file_import_mode == FileImportMode.SKINNED)

        abstract_vertex_buffers = []
        vertex_bytes_offset = 0
        for layout_struct in vertex_layout_arr:
            layout_build_start = time.time()
            abstract_layout = GMDVertexBufferLayout.build_vertex_buffer_layout_from_flags(layout_struct.vertex_packing_flags, assume_skinned_vertex_buffers, self.error)
            if abstract_layout.bytes_per_vertex() != layout_struct.bytes_per_vertex:
                self.error.fatal(
                    f"Abstract Layout BPV {abstract_layout.bytes_per_vertex()} didn't match expected {layout_struct.bytes_per_vertex}\n"
                    f"Packing Flags {layout_struct.vertex_packing_flags:08x} created layout {abstract_layout}")

            if self.vertex_import_mode == VertexImportMode.NO_VERTICES:
                # Create an empty vertex buffer
                abstract_vertex_buffer = GMDVertexBuffer_Generic.build_empty(abstract_layout, 0)
            else:
                # Actually unpack vertices
                unpack_start = time.time()

                abstract_vertex_buffer, vertex_bytes_offset = \
                    abstract_layout.unpack_from(self.vertices_are_big_endian, layout_struct.vertex_count,
                                                vertex_bytes, vertex_bytes_offset)

                unpack_finish = time.time()

                unpack_delta = unpack_finish - unpack_start
                if profile:
                    # Note - importing st_dead_sera takes ~3seconds total - this doesn't seem like a perf regression from the original tho
                    # This profiling is here incase we want to optimize vertex unpacking
                    print(f"Time to build layout: {unpack_start - layout_build_start}")
                    print(
                        f"Time to unpack {layout_struct.vertex_count} verts: {unpack_delta} ({unpack_delta / layout_struct.vertex_count * 1000:2f}ms/vert)")

            abstract_vertex_buffers.append(abstract_vertex_buffer)

        return abstract_vertex_buffers


    def build_shaders_from_structs(self,

                                   abstract_vertex_buffers: List[GMDVertexBuffer_Generic],

                                   mesh_arr: List[MeshStruct], attribute_arr: List[AttributeStruct],
                                   shader_name_arr: List[ChecksumStrStruct]) \
            -> List[GMDShader]:
        shader_vertex_layout_map = {}
        shaders_map = {}
        for mesh_struct in mesh_arr:
            shader_name = shader_name_arr[attribute_arr[mesh_struct.attribute_index].shader_index].text
            vertex_layout = abstract_vertex_buffers[mesh_struct.vertex_buffer_index].layout
            # If we're importing in a skinned context AND the vertex layout has both bones and weight,
            # we assume the shader is skinned.
            assume_skinned_from_mesh = vertex_layout.assume_skinned and \
                                       bool(vertex_layout.bones_storage) and \
                                       bool(vertex_layout.weights_storage)

            if shader_name not in shader_vertex_layout_map:
                shader_vertex_layout_map[shader_name] = vertex_layout
                shaders_map[shader_name] = GMDShader(
                    name=shader_name,
                    vertex_buffer_layout=vertex_layout,
                    assume_skinned=assume_skinned_from_mesh
                )
            elif shader_vertex_layout_map[shader_name] != vertex_layout:
                self.error.fatal(f"Shader {shader_name} was found to be mapped to two different vertex layouts")
                # assume_skinned_from_mesh = entirely vertex layout dependent, so it must be the same
                # if the vertex layout is the same

        # Return shaders in the same order as the shader_name_arr
        return [shaders_map[name.text] for name in shader_name_arr]


    def build_materials_from_structs(self,

                                     abstract_shaders: List[GMDShader],

                                     attribute_arr: List[AttributeStruct], material_arr: List[MaterialBaseStruct],
                                     unk12_arr: List[Unk12Struct], unk14_arr: List[Unk14Struct],
                                     texture_name_arr: List[ChecksumStrStruct]) \
            -> List[GMDAttributeSet]:
        attributes = []
        parse_texture_index = lambda idx: None if idx.tex_index == -1 else texture_name_arr[idx.tex_index].text

        gmd_materials = [
            GMDMaterial(origin_version=self.version_props.major_version, origin_data=mat)
            for mat in material_arr
        ]
        if unk12_arr:
            gmd_unk12s = [
                GMDUnk12(float_data=unk12.data)
                for unk12 in unk12_arr
            ]
        if unk14_arr:
            gmd_unk14s = [
                GMDUnk14(int_data=unk14.data)
                for unk14 in unk14_arr
            ]

        for i, attribute_struct in enumerate(attribute_arr):
            attributes.append(GMDAttributeSet(
                shader=abstract_shaders[attribute_struct.shader_index],

                texture_diffuse=parse_texture_index(attribute_struct.texture_diffuse),
                texture_refl=parse_texture_index(attribute_struct.texture_refl),
                texture_multi=parse_texture_index(attribute_struct.texture_multi),
                texture_unk1=parse_texture_index(attribute_struct.texture_unk1),
                texture_rs=parse_texture_index(attribute_struct.texture_ts),
                texture_normal=parse_texture_index(attribute_struct.texture_normal),
                texture_rt=parse_texture_index(attribute_struct.texture_rt),
                texture_rd=parse_texture_index(attribute_struct.texture_rd),

                material=gmd_materials[attribute_struct.material_index],
                unk12=gmd_unk12s[i] if unk12_arr else None,
                unk14=gmd_unk14s[i] if unk14_arr else None,

                attr_flags=attribute_struct.flags,
                attr_extra_properties=attribute_struct.extra_properties,
            ))

        return attributes

    def build_node_hierarchy_from_structs(self,

                                          node_arr: List[NodeStruct],
                                          node_name_arr: List[ChecksumStrStruct], matrix_arr: List[Matrix]) \
            -> List[GMDNode]:
        nodes = []
        parent_stack = ParentStack()
        for bone_idx, node_struct in enumerate(node_arr):
            name = node_name_arr[node_struct.name_index].text

            if node_struct.node_type == NodeType.SkinnedMesh and parent_stack:
                # As far as we know Skinned Objects having a "parent" in the hierarchy is meaningless
                self.error.fatal(f"Node {name} of type {node_struct.node_type} found inside hierarchy of Bone")

            # This is guaranteed to be a bone node
            if node_struct.node_type == NodeType.MatrixTransform:
                node = GMDBone(
                    name=name,
                    node_type=node_struct.node_type,

                    pos=node_struct.pos,
                    rot=node_struct.rot,
                    scale=node_struct.scale,

                    world_pos=node_struct.world_pos,
                    anim_axis=node_struct.anim_axis,
                    matrix=matrix_arr[node_struct.matrix_index],

                    parent=parent_stack.peek() if parent_stack else None,
                    flags=node_struct.flags
                )
            elif node_struct.node_type == NodeType.SkinnedMesh:
                if 0 <= node_struct.matrix_index < len(matrix_arr):
                    self.error.recoverable(f"Skinned object {name} references a valid matrix, even though skinned meshes aren't supposed to have them!")

                node = GMDSkinnedObject(
                    name=name,
                    node_type=node_struct.node_type,

                    pos=node_struct.pos,
                    rot=node_struct.rot,
                    scale=node_struct.scale,

                    world_pos=node_struct.world_pos,
                    anim_axis=node_struct.anim_axis,

                    parent=parent_stack.peek() if parent_stack else None,
                    flags=node_struct.flags
                )
            elif node_struct.node_type == NodeType.UnskinnedMesh:
                if not (0 <= node_struct.matrix_index < len(matrix_arr)):
                    self.error.fatal(f"Unskinned object {name} doesn't reference a valid matrix")

                matrix = matrix_arr[node_struct.matrix_index]

                node = GMDUnskinnedObject(
                    name=name,
                    node_type=node_struct.node_type,

                    pos=node_struct.pos,
                    rot=node_struct.rot,
                    scale=node_struct.scale,

                    world_pos=node_struct.world_pos,
                    anim_axis=node_struct.anim_axis,
                    matrix=matrix,

                    parent=parent_stack.peek() if parent_stack else None,
                    flags=node_struct.flags
                )
            else:
                self.error.fatal(f"Unknown node type enum value {node_struct.node_type} for {name}")

            nodes.append(node)
            # Apply the stack operation to the parent_stack
            parent_stack.handle_node(node_struct.stack_op, node)

        return nodes


    def build_meshes_from_structs(self,

                                  abstract_attributes: List[GMDAttributeSet],
                                  abstract_vertex_buffers: List[GMDVertexBuffer_Generic],
                                  abstract_nodes_ordered: List[GMDNode],

                                  mesh_arr: List[MeshStruct], index_buffer: List[int], mesh_matrix_bytestrings: bytes,
                                  bytestrings_are_16bit: bool,
                                  ) \
            -> List[Union[GMDSkinnedMesh, GMDMesh]]:
        file_uses_relative_indices = self.version_props.relative_indices_used
        file_uses_min_index = self.version_props.indices_offset_by_min_index

        # TODO: Check if uses_relative_indices and not(uses_min_index), that should error?

        def read_bytestring(start_byte: int, length: int):
            if (not mesh_matrix_bytestrings) or (length == 0):
                return []

            unpack_type = c_uint16 if bytestrings_are_16bit else c_uint8
            #len_bytes = length * unpack_type.sizeof()
            actual_len, offset = unpack_type.unpack(self.file_is_big_endian, mesh_matrix_bytestrings, offset=start_byte)
            if actual_len != length:
                actual_bytes = mesh_matrix_bytestrings[start_byte:start_byte+actual_len*unpack_type.sizeof()]
                actual_bytes = [f"{x:02x}" for x in actual_bytes]
                self.error.fatal(f"Bytestring length mismatch: expected {length}, got {actual_len}. bytes: {actual_bytes}")
            print(start_byte, actual_len, (start_byte + (actual_len + 1) * unpack_type.sizeof()))
            # data_start = start_byte + 1
            # data_end = data_start + len_bytes
            # data = mesh_matrix_bytestrings[data_start:data_end]
            # if bytestrings_are_16bit:
            #     # TODO: are 16bit strings always big-endian?
            #     data, _ = FixedSizeArrayUnpacker(c_uint16, length).unpack(True, data, 0)
            #     return data
            # else:
            #     return [int(bone_idx_byte) for bone_idx_byte in data]
            data, _ = FixedSizeArrayUnpacker(unpack_type, length).unpack(self.file_is_big_endian, mesh_matrix_bytestrings, offset=offset)
            return data

        # Take a range, look up that range in the index buffer, return normalized indices from 0 to vertex_count
        def process_indices(mesh_struct: MeshStruct, indices_range: IndicesStruct, min_index: int = 0xFFFF,
                            max_index: int = -1) -> Tuple[array.ArrayType, int, int]:
            index_ptr_min = indices_range.index_offset
            index_ptr_max = index_ptr_min + indices_range.index_count

            if file_uses_relative_indices:
                index_offset = 0
            else:
                if file_uses_min_index:
                    index_offset = mesh_struct.min_index
                else:
                    # Look through the range and find the smallest index, take everything relative to that.
                    index_offset = min(index_buffer[i] for i in range(index_ptr_min, index_ptr_max))
            indices = array.array("H")
            for i in range(index_ptr_min, index_ptr_max):
                index = index_buffer[i]
                if index != 0xFFFF:
                    # Update min/max absolute index values
                    min_index = min(min_index, index)
                    max_index = max(max_index, index)

                    index = index - index_offset

                indices.append(index)
            return indices, min_index, max_index

        meshes = []
        for mesh_struct in mesh_arr:
            if self.vertex_import_mode == VertexImportMode.NO_VERTICES:
                triangle_indices = array.array("H")
                triangle_strip_noreset_indices = array.array("H")
                triangle_strip_reset_indices = array.array("H")

                vertex_start = 0
                vertex_end = 0
                self.error.debug("MESH_PROPS", "index props: none, because importing with NO_VERTICES")
            else:
                # Actually import data
                triangle_indices, min_index, max_index = process_indices(mesh_struct, mesh_struct.triangle_list_indices)
                triangle_strip_noreset_indices, min_index, max_index = process_indices(mesh_struct,
                                                                                       mesh_struct.noreset_strip_indices,
                                                                                       min_index, max_index)
                triangle_strip_reset_indices, min_index, max_index = process_indices(mesh_struct,
                                                                                     mesh_struct.reset_strip_indices, min_index,
                                                                                     max_index)

                if file_uses_min_index and (not file_uses_relative_indices) and mesh_struct.min_index != min_index:
                    self.error.fatal(
                        f"Mesh uses a minimum absolute index of {min_index}, but file specifies a minimum index of {mesh_struct.min_index}")

                # Define the range of vertices that are referenced by the indices.
                # This is shifted up by the vertex_offset_from_index field.
                # This means if a single vertex buffer has >65535 elements, and a mesh wants to index into it with 16-bit unsigned,
                # it can shift its indices down by a set amount to prevent exceeding the limit.
                vertex_start = (mesh_struct.min_index if file_uses_min_index else min_index) + mesh_struct.vertex_offset_from_index
                vertex_end = vertex_start + mesh_struct.vertex_count

                if vertex_start < 0 or vertex_end < 0 or vertex_end <= vertex_start:
                    self.error.fatal(f"Invalid vertex_start {vertex_start} vertex_end {vertex_end} pair")

                # [min_index, max_index] is an *inclusive* range
                # [vertex_start, vertex_end) is *exclusive* at the end
                if (not file_uses_relative_indices) and (vertex_end - vertex_start) != (max_index - min_index + 1):
                    self.error.fatal(
                        f"Mesh vertex_count is {mesh_struct.vertex_count} and calculated range is {vertex_end - vertex_start} long but indices show a range of length {max_index - min_index + 1} is used.")

                self.error.debug("MESH_PROPS", f"index props: min_index {min_index}, max_index {max_index}, vertex_start {vertex_start}, vertex_end {vertex_end}")

            vertex_buffer = abstract_vertex_buffers[mesh_struct.vertex_buffer_index]
            vertex_slice = slice(vertex_start, vertex_end)

            relevant_bone_indices = read_bytestring(mesh_struct.matrixlist_offset, mesh_struct.matrixlist_length)
            if relevant_bone_indices:
                relevant_bones = [abstract_nodes_ordered[bone_idx] for bone_idx in relevant_bone_indices]
                if any(not isinstance(node, GMDBone) for node in relevant_bones):
                    self.error.fatal(
                        f"Skinned mesh references some non-bone nodes {[node.name for node in relevant_bones if not isinstance(node, GMDBone)]}")

                if self.file_import_mode == FileImportMode.UNSKINNED:
                    self.error.fatal("Found mesh with a matrixlist in an unskinned file - can't import this yet")

                meshes.append(GMDSkinnedMesh(
                    empty=(self.vertex_import_mode == VertexImportMode.NO_VERTICES),

                    relevant_bones=cast(List[GMDBone], relevant_bones),

                    vertices_data=vertex_buffer.extract_as_skinned(vertex_slice),

                    triangle_indices=triangle_indices,
                    triangle_strip_noreset_indices=triangle_strip_noreset_indices,
                    triangle_strip_reset_indices=triangle_strip_reset_indices,

                    attribute_set=abstract_attributes[mesh_struct.attribute_index]
                ))
            else:
                meshes.append(GMDMesh(
                    empty=(self.vertex_import_mode == VertexImportMode.NO_VERTICES),

                    vertices_data=vertex_buffer.extract_as_generic(vertex_slice),

                    triangle_indices=triangle_indices,
                    triangle_strip_noreset_indices=triangle_strip_noreset_indices,
                    triangle_strip_reset_indices=triangle_strip_reset_indices,

                    attribute_set=abstract_attributes[mesh_struct.attribute_index]
                ))

        return meshes


    def connect_object_meshes(self,

                              abstract_meshes: List[GMDMesh], abstract_attribute_sets: List[GMDAttributeSet],
                              abstract_nodes: List[GMDNode],

                              node_arr: List[NodeStruct],
                              object_drawlist_ptrs: List[int], mesh_drawlists: bytes):
        for i, node_struct in enumerate(node_arr):
            if node_struct.node_type in [NodeType.UnskinnedMesh, NodeType.SkinnedMesh]:
                abstract_node = abstract_nodes[i]

                if not isinstance(abstract_node, (GMDSkinnedObject, GMDUnskinnedObject)):
                    self.error.fatal(
                        f"Node type mismatch: node {i} is of type {node_struct.node_type} but the abstract version is a {type(abstract_node)}")

                # This is guaranteed to be some sort of object
                # Parse the drawlist

                drawlist_ptr = object_drawlist_ptrs[node_struct.object_index]
                offset = drawlist_ptr
                big_endian = self.file_is_big_endian
                drawlist_len, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
                zero, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
                for i in range(drawlist_len):
                    material_idx, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
                    mesh_idx, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)

                    abstract_attribute_set = abstract_attribute_sets[material_idx]
                    abstract_mesh = abstract_meshes[mesh_idx]
                    if abstract_attribute_set != abstract_mesh.attribute_set:
                        self.error.recoverable(
                            f"Object {abstract_node.name} specifies an unexpected material/mesh pair in it's drawlist, that doesn't match the mesh's requested material")

                    abstract_node.add_mesh(abstract_mesh)
                    pass


# def build_object_nodes(self,
#
#                        abstract_meshes: List[GMDMesh], abstract_attribute_sets: List[GMDAttributeSet],
#
#                        remaining_node_arr: List[NodeStruct], node_name_arr: List[ChecksumStrStruct],
#                        object_drawlist_ptrs: List[int],
#                        matrix_arr: List[Matrix], mesh_drawlists: bytes,
#                        big_endian: bool) \
#         -> Tuple[List[GMDSkinnedObject], List[GMDUnskinnedObject]]:
#     skinned_objects = []
#     unskinned_objects = []
#
#     # TODO - the model sword has unskinned BEFORE matrix transform (despite none of those matrix transforms actually being used)
#     # TODO - the shotgun model has unskinned INSIDE A HIERARCHY
#         # Blender has a "Child Of" constraint for this
#
#     parent_stack = ParentStack()
#     for node_struct in remaining_node_arr:
#         name = node_name_arr[node_struct.name_index].text
#
#         if node_struct.node_type == NodeType.MatrixTransform:
#             # print(skinned_objects)
#             # print(unskinned_objects)
#             raise Exception(f"Node {name} of type {node_struct.node_type} found after bone heirarchy had finished")
#
#         # This is guaranteed to be some sort of object
#         # Parse the drawlist
#         object_abstract_meshes = []
#
#         drawlist_ptr = object_drawlist_ptrs[node_struct.object_index]
#         offset = drawlist_ptr
#         drawlist_len, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
#         zero, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
#         for i in range(drawlist_len):
#             material_idx, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
#             mesh_idx, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
#
#             abstract_attribute_set = abstract_attribute_sets[material_idx]
#             abstract_mesh = abstract_meshes[mesh_idx]
#             if abstract_attribute_set != abstract_mesh.attribute_set:
#                 raise Exception(f"Object {name} specifies an unexpected material/mesh pair in it's drawlist, that doesn't match the mesh's requested material")
#
#             object_abstract_meshes.append(abstract_mesh)
#             pass
#
#         if node_struct.node_type == NodeType.SkinnedMesh:
#             if 0 <= node_struct.matrix_index < len(matrix_arr):
#                 raise Exception(f"Skinned object {name} references a valid matrix, even though skinned meshes aren't supposed to have them!")
#
#             obj = GMDSkinnedObject(
#                 name=name,
#                 node_type=node_struct.node_type,
#
#                 pos=node_struct.pos,
#                 rot=node_struct.rot,
#                 scale=node_struct.scale,
#
#                 parent=parent_stack.peek() if parent_stack else None,
#
#                 mesh_list=object_abstract_meshes
#             )
#             skinned_objects.append(obj)
#         else:
#             if not(0 <= node_struct.matrix_index < len(matrix_arr)):
#                 raise Exception(f"Unskinned object {name} doesn't reference a valid matrix")
#
#             matrix = matrix_arr[node_struct.matrix_index]
#
#             obj = GMDUnskinnedObject(
#                 name=name,
#                 node_type=node_struct.node_type,
#
#                 pos=node_struct.pos,
#                 rot=node_struct.rot,
#                 scale=node_struct.scale,
#
#                 parent=parent_stack.peek() if parent_stack else None,
#
#                 matrix=matrix,
#
#                 mesh_list=object_abstract_meshes
#             )
#             unskinned_objects.append(obj)
#
#         # Apply the stack operation to the parent_stack
#         parent_stack.handle_node(node_struct.stack_op, obj)
#
#     return skinned_objects, unskinned_objects


# TODO: Think about how to do this
def validate_scene(scene: GMDScene):
    pass
