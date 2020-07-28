from dataclasses import dataclass
from typing import List, Dict, Tuple, Iterable, TypeVar, Callable

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDMaterial
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_node import GMDObject, GMDNode
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBufferLayout
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStrStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeStruct, NodeStackOp


@dataclass(frozen=True)
class RearrangedData:
    nodes_arr: List[Tuple[GMDNode, NodeStackOp]]
    object_id_to_node_index: Dict[int, int]
    objects: List[GMDObject]

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

        # if node is instance of GMDObject
            # object_id_node_index_mapping[id(node)] = node
    # make sure to maintain original object order for scene
        # involves making sure the DFA happens with children in order []

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