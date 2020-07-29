from dataclasses import dataclass
from typing import List, Dict, Tuple, Iterable, TypeVar, Callable, Union, overload

from mathutils import Matrix

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDMaterial, GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_node import GMDSkinnedObject, GMDNode, GMDUnskinnedObject, GMDBone
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBufferLayout, GMDShader, GMDVertexBuffer
from yk_gmd_blender.yk_gmd.v2.structure.common.attribute import AttributeStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStrStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.material_base import MaterialBaseStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import MeshStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeStruct, NodeStackOp
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
    pass

def build_materials_from_structs(version_properties: VersionProperties,

                                 abstract_shaders: List[GMDShader],

                                 attribute_arr: List[AttributeStruct], material_arr: List[MaterialBaseStruct],
                                 unk12_arr: List[Unk12Struct], unk14_arr: List[Unk14Struct],
                                 texture_name_arr: List[ChecksumStrStruct]) \
        -> List[GMDAttributeSet]:
    pass

def build_skeleton_bones_from_structs(version_properties: VersionProperties,

                                      node_arr: List[NodeStruct],
                                      node_name_arr: List[ChecksumStrStruct], matrix_arr: List[Matrix]) \
        -> Tuple[List[GMDBone], List[NodeStruct]]:
    pass

def build_meshes_from_structs(version_properties: VersionProperties,

                              abstract_attributes: List[GMDAttributeSet], abstract_vertex_buffers: List[GMDVertexBuffer],
                              abstract_bones_ordered: List[GMDBone],

                              mesh_arr: List[MeshStruct], index_buffer: List[int]) \
        -> List[GMDMesh]:
    pass

def build_object_nodes(version_properties: VersionProperties,

                       abstract_meshes: List[GMDMesh],

                       remaining_node_arr: List[NodeStruct], matrix_arr: List[Matrix],
                       mesh_bytestrings: bytes) \
        -> Tuple[List[GMDSkinnedObject], List[GMDUnskinnedObject]]:
    pass


# TODO: Think about how to do this
def validate_scene(scene: GMDScene):
    pass