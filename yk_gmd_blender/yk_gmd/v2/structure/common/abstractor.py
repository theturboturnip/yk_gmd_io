import array
from dataclasses import dataclass
from typing import List, Dict, Tuple, Iterable, TypeVar, Callable, Union, overload

from mathutils import Matrix

from yk_gmd_blender.structurelib.base import FixedSizeArrayUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint16
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDMaterial, GMDAttributeSet, GMDUnk12, GMDUnk14
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_node import GMDSkinnedObject, GMDNode, GMDUnskinnedObject, GMDBone
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBufferLayout, GMDShader, GMDVertexBuffer
from yk_gmd_blender.yk_gmd.v2.structure.common.attribute import AttributeStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStrStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.material_base import MaterialBaseStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import MeshStruct, IndicesStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeStruct, NodeStackOp, NodeType
from yk_gmd_blender.yk_gmd.v2.structure.common.unks import Unk12Struct, Unk14Struct
from yk_gmd_blender.yk_gmd.v2.structure.common.vertex_buffer_layout import VertexBufferLayoutStruct
from yk_gmd_blender.yk_gmd.v2.structure.version import GMDVersion, VersionProperties


@dataclass(frozen=True)
class RearrangedData:
    nodes_arr: List[Tuple[GMDNode, NodeStackOp]]
    object_id_to_node_index: Dict[int, int]
    skinned_objects: List[GMDSkinnedObject]
    unskinned_objects: List[GMDUnskinnedObject]
    ordered_matrices: List[Matrix]
    object_id_to_matrix_index: Dict[int, int]
    root_node_indices: List[int]

    texture_names: List[ChecksumStrStruct]
    texture_names_index: Dict[str, int]
    shader_names: List[ChecksumStrStruct]
    shader_names_index: Dict[str, int]
    node_names: List[ChecksumStrStruct]
    node_names_index: Dict[str, int]

    ordered_meshes: List[Tuple[GMDVertexBufferLayout, List[GMDMesh]]]
    mesh_id_to_index: Dict[int, int]

    ordered_materials: List[GMDMaterial]
    material_id_to_index: Dict[int, int]

    # This is only for skinned meshes
    mesh_matrix_index_strings: List[List[int]]
    # build with build_index_mapping(pool, key=tuple)
    mesh_matrix_index_strings_index: Dict[Tuple, int]


T = TypeVar('T')
TKey = TypeVar('TKey')


def build_index_mapping(pool: List[T], key: Callable[[T], TKey] = lambda x: x) -> Dict[TKey, int]:
    return {
        key(x):i
        for i, x in enumerate(pool)
    }


def build_pools(strs: Iterable[str]) -> Tuple[List[ChecksumStrStruct], Dict[str, int]]:
    # Given a set of strings, build the list of checksumstrs
    # sort the list by checksum (?) - I think RGG do this
    # return mapping of string -> index in list (generator)
    pool = [ChecksumStrStruct.make_from_str(s) for s in strs]
    pool.sort(key=lambda css: css.checksum)
    return pool, build_index_mapping(pool, key=lambda css: css.text)


def arrange_data_for_export(scene: GMDScene) -> RearrangedData:
    # Order the nodes
    # Depth-first indexing
    # Track touched nodes in set T(n)
    # for i in order:
        # stackop = none
        # if has parent and all other children of your parent have been touched - stackop += pop
        # if not leaf: stackop += push

        # emit (node, stackop)

        # if node is instance of GMDObject (skinned or unskinned)
            # object_id_node_index_mapping[id(node)] = node index

        # if node is bone or unskinned
            # emit matrix
            # object_id_to_matrix_index[id(node)] = index

        # if node has no parent
            # add index to roots
    # make sure to maintain original object order for scene
        # involves making sure the DFA happens with objects in order
    # Note - flags
        # many bones flag is important, but so are the others - look into which ones are supposed to be there
        # is relative-indexing set in a flag?

    # build texture, shader, node name pools

    # ordering meshes:
    # build list of vertex buffers to use
    # sort by descending flags int value (?)
    # for buffer_layout in buffers:
        # meshes_for_buffer = [m for m in meshes if m.material.shader.vertex_buffer_layout == buffer_layout]
        # sort meshes by id(material) - just to group the common materials together
        # emit buffer_layout, meshes_for_buffer

    # ordered_materials = []
    # for _,ms in buffer_meshes_pairs:
        # for m in ms
            # if m.material != ordered_materials[-1]
                # ordered_materials.append(m.material)
    # make index mapping for ordered_materials

    # now all arrangements should be made - next is to port into the respective file formats
    # this is for tomorrow tho

    pass

def build_vertex_buffers_from_structs(version_properties: VersionProperties,

                                      vertex_layout_arr: List[VertexBufferLayoutStruct], vertex_bytes: bytes) \
        -> List[GMDVertexBuffer]:
    pass


def build_shaders_from_structs(version_properties: VersionProperties,

                               abstract_vertex_buffers: List[GMDVertexBuffer],

                               mesh_arr: List[MeshStruct], attribute_arr: List[AttributeStruct],
                               shader_name_arr: List[ChecksumStrStruct]) \
        -> List[GMDShader]:
    shader_vertex_layout_map = {}
    shaders_map = {}
    for mesh_struct in mesh_arr:
        shader_name = shader_name_arr[attribute_arr[mesh_struct.attribute_index].shader_index].text
        vertex_layout = abstract_vertex_buffers[mesh_struct.vertex_buffer_index].layout

        if shader_name not in shader_vertex_layout_map:
            shader_vertex_layout_map[shader_name] = vertex_layout
            shaders_map[shader_name] = GMDShader(
                name=shader_name,
                vertex_buffer_layout=vertex_layout
            )
        elif shader_vertex_layout_map[shader_name] != vertex_layout:
            raise Exception(f"Shader {shader_name} was found to be mapped to two different vertex layouts")

    # Return shaders in the same order as the shader_name_arr
    return [shaders_map[name.text] for name in shader_name_arr]


def build_materials_from_structs(version_properties: VersionProperties,

                                 abstract_shaders: List[GMDShader],

                                 attribute_arr: List[AttributeStruct], material_arr: List[MaterialBaseStruct],
                                 unk12_arr: List[Unk12Struct], unk14_arr: List[Unk14Struct],
                                 texture_name_arr: List[ChecksumStrStruct]) \
        -> List[GMDAttributeSet]:

    attributes = []
    parse_texture_index = lambda idx: None if idx.tex_index == -1 else texture_name_arr[idx.tex_index].text

    gmd_materials = [
        GMDMaterial(origin_version=version_properties.major_version, origin_data=mat)
        for mat in material_arr
    ]
    if unk12_arr:
        gmd_unk12s = [
            GMDUnk12(origin_version=version_properties.major_version, float_data=unk12.data)
            for unk12 in unk12_arr
        ]
    if unk14_arr:
        gmd_unk14s = [
            GMDUnk14(origin_version=version_properties.major_version, int_data=unk14.data)
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
        ))

    return attributes

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


def build_skeleton_bones_from_structs(version_properties: VersionProperties,

                                      node_arr: List[NodeStruct],
                                      node_name_arr: List[ChecksumStrStruct], matrix_arr: List[Matrix]) \
        -> Tuple[List[GMDBone], List[NodeStruct]]:

    bones = []
    parent_stack = ParentStack()
    bone_idx = 0
    for bone_idx, node_struct in enumerate(node_arr):
        name = node_name_arr[node_struct.name_index].text

        if node_struct.node_type != NodeType.MatrixTransform:
            if not bones:
                # Assume the file has no skeleton nodes
                break
            elif parent_stack:
                # Hit a new node inside of the hierarchy => type mismatch
                raise Exception(f"Node {name} of type {node_struct.node_type} found inside heirarchy of Bone")
            else:
                # Hit a new node type when at the root => assume everything is fine
                break

        # This is guaranteed to be a bone node
        bone = GMDBone(
            name=name,
            node_type=node_struct.node_type,

            pos=node_struct.pos,
            rot=node_struct.rot,
            scale=node_struct.scale,

            bone_pos=node_struct.bone_pos,
            bone_axis=node_struct.bone_axis,
            matrix=matrix_arr[node_struct.matrix_index],

            parent=parent_stack.peek() if parent_stack else None
        )

        bones.append(bone)

        # Apply the stack operation to the parent_stack
        parent_stack.handle_node(node_struct.stack_op, bone)

    return bones, node_arr[bone_idx:]


def build_meshes_from_structs(version_properties: VersionProperties,

                              abstract_attributes: List[GMDAttributeSet], abstract_vertex_buffers: List[GMDVertexBuffer],
                              abstract_bones_ordered: List[GMDBone],

                              mesh_arr: List[MeshStruct], index_buffer: List[int], mesh_matrix_bytestrings: bytes,
                              bytestrings_are_16bit: bool,
                              ) \
        -> List[GMDMesh]:
    file_uses_relative_indices = version_properties.relative_indices_used
    file_uses_vertex_offset = version_properties.vertex_offset_used
    # TODO: Check if uses_relative_indices and not(uses_vertex_offset), that should error

    def read_bytestring(start_byte: int, length: int):
        len_bytes = length * (2 if bytestrings_are_16bit else 1)
        actual_len = mesh_matrix_bytestrings[start_byte]
        if actual_len != length:
            raise Exception(f"Bytestring length mismatch: expected {length}, got {actual_len}")

        data_start = start_byte + 1
        data_end = data_start + len_bytes
        data = mesh_matrix_bytestrings[data_start:data_end]
        if bytestrings_are_16bit:
            # TODO: are 16bit strings always big-endian?
            data, _ = FixedSizeArrayUnpacker(c_uint16, length).unpack(True, data, 0)
            return data
        else:
            return [int(bone_idx_byte) for bone_idx_byte in data]

    def process_indices(mesh_struct: MeshStruct, indices_range: IndicesStruct, min_index: int = 0xFFFF, max_index: int = -1) -> Tuple[array.ArrayType, int, int]:
        index_offset = mesh_struct.vertex_offset if file_uses_relative_indices else 0
        indices = array.array("H")
        for i in range(indices_range.index_offset, indices_range.index_offset + indices_range.index_count):
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
        relevant_bone_indices = read_bytestring(mesh_struct.matrixlist_offset, mesh_struct.matrixlist_length)

        triangle_indices, min_index, max_index = process_indices(mesh_struct, mesh_struct.triangle_list_indices)
        triangle_strip_noreset_indices, min_index, max_index = process_indices(mesh_struct, mesh_struct.noreset_strip_indices, min_index, max_index)
        triangle_strip_reset_indices, min_index, max_index = process_indices(mesh_struct, mesh_struct.reset_strip_indices, min_index, max_index)

        if file_uses_vertex_offset and (not file_uses_relative_indices) and mesh_struct.vertex_offset != min_index:
            raise Exception(f"Mesh uses a minimum absolute index of {min_index}, but file specifies a vertex offset of {mesh_struct.vertex_offset}")

        vertex_start = mesh_struct.vertex_offset if file_uses_relative_indices else min_index
        vertex_end = vertex_start + mesh_struct.vertex_count

        if (not file_uses_relative_indices) and vertex_end < max_index:
            raise Exception(f"Mesh vertex_count is {mesh_struct.vertex_count} but indices show a range of length {max_index-min_index} is used.")

        meshes.append(GMDMesh(
            relevant_bones=[abstract_bones_ordered[bone_idx] for bone_idx in relevant_bone_indices],

            vertices_data=abstract_vertex_buffers[mesh_struct.vertex_buffer_index][vertex_start:vertex_end+1],

            triangle_indices=triangle_indices,
            triangle_strip_noreset_indices=triangle_indices,
            triangle_strip_reset_indices=triangle_indices,

            attribute_set=abstract_attributes[mesh_struct.attribute_index]
        ))

    return meshes

def build_object_nodes(version_properties: VersionProperties,

                       abstract_meshes: List[GMDMesh],

                       remaining_node_arr: List[NodeStruct], matrix_arr: List[Matrix],
                       mesh_bytestrings: bytes) \
        -> Tuple[List[GMDSkinnedObject], List[GMDUnskinnedObject]]:
    pass


# TODO: Think about how to do this
def validate_scene(scene: GMDScene):
    pass