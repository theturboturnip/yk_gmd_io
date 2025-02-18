import functools
import re
from dataclasses import dataclass
from typing import TypeVar, Tuple, List, Dict, Iterable, Callable, Set, Union

from mathutils import Matrix
from ....structurelib.base import FixedSizeArrayUnpacker
from ....structurelib.primitives import c_uint16
from ...abstract.gmd_attributes import GMDMaterial, GMDAttributeSet
from ...abstract.gmd_mesh import GMDSkinnedMesh, GMDMesh
from ...abstract.gmd_scene import depth_first_iterate, GMDScene
from ...abstract.gmd_shader import GMDVertexBufferLayout
from ...abstract.nodes.gmd_bone import GMDBone
from ...abstract.nodes.gmd_node import GMDNode
from ...abstract.nodes.gmd_object import GMDSkinnedObject, GMDUnskinnedObject
from ...errors.error_reporter import ErrorReporter
from ...structure.common.checksum_str import ChecksumStrStruct
from ...structure.common.node import NodeStackOp


@dataclass(frozen=True)
class RearrangedData:
    ordered_nodes: List[Tuple[GMDNode, NodeStackOp]]
    ordered_matrices: List[Matrix]
    ordered_objects: List[Union[GMDSkinnedObject, GMDUnskinnedObject]]

    root_node_indices: List[int]
    node_id_to_node_index: Dict[int, int]
    node_id_to_object_index: Dict[int, int]
    object_id_to_matrix_index: Dict[int, int]

    texture_names: List[ChecksumStrStruct]
    texture_names_index: Dict[str, int]
    shader_names: List[ChecksumStrStruct]
    shader_names_index: Dict[str, int]
    node_names: List[ChecksumStrStruct]
    node_names_index: Dict[str, int]

    # Tuple of (layout, layout_vertex_packing_flags, meshes)
    vertex_layout_groups: List[Tuple[GMDVertexBufferLayout, int, List[GMDMesh]]]

    ordered_meshes: List[GMDMesh]
    mesh_id_to_index: Dict[int, int]
    mesh_id_to_matrixlist: Dict[int, Tuple]
    mesh_id_to_object_index: Dict[int, int]

    ordered_attribute_sets: List[GMDAttributeSet]
    attribute_set_id_to_index: Dict[int, int]
    # List of [start, end_exclusive) ranges
    attribute_set_id_to_mesh_index_range: Dict[int, Tuple[int, int]]

    ordered_materials: List[GMDMaterial]
    material_id_to_index: Dict[int, int]

    # This is only for skinned meshes
    mesh_matrixlist: List[Tuple]
    # build with build_index_mapping(pool, key=tuple)
    mesh_matrixlist_index: Dict[Tuple, int]


T = TypeVar('T')
TKey = TypeVar('TKey')


def build_index_mapping(pool: List[T], key: Callable[[T], TKey] = lambda x: x) -> Dict[TKey, int]:
    return {
        key(x): i
        for i, x in enumerate(pool)
    }


def build_pools(strs: Iterable[str]) -> Tuple[List[ChecksumStrStruct], Dict[str, int]]:
    # Given a set of strings, build the list of checksumstrs
    # don't sort the list by checksum - RGG *may* do this, but it's unlikely to affect anything
    # return mapping of string -> index in list
    pool = [ChecksumStrStruct.make_from_str(s) for s in strs]
    return pool, build_index_mapping(pool, key=lambda css: css.text)


def pack_mesh_matrix_strings(mesh_matrixlist: List[Tuple[int, ...]],
                             pack_as_16bit: bool, big_endian: bool) -> Tuple[bytes, Dict[Tuple, int]]:
    matrixlist_bytearray = bytearray()
    matrixlist_index = {}
    for matrixlist in mesh_matrixlist:
        matrixlist_index[matrixlist] = len(matrixlist_bytearray)

        if pack_as_16bit:
            c_uint16.pack(big_endian, value=len(matrixlist), append_to=matrixlist_bytearray)
            FixedSizeArrayUnpacker(c_uint16, len(matrixlist)).pack(big_endian=big_endian, value=matrixlist,
                                                                   append_to=matrixlist_bytearray)
            if not matrixlist:
                # Add a padding byte in case?
                c_uint16.pack(big_endian, value=0, append_to=matrixlist_bytearray)
        else:
            matrixlist_bytearray += bytes([len(matrixlist)] + list(matrixlist))

    return bytes(matrixlist_bytearray), matrixlist_index


def generate_vertex_layout_packing_flags(layout: GMDVertexBufferLayout) -> int:
    return layout.packing_flags


def arrange_data_for_export(scene: GMDScene, error: ErrorReporter) -> RearrangedData:
    # Note - flags
    # many bones flag is important, but so are the others - look into which ones are supposed to be there
    # is relative-indexing set in a flag?

    ordered_nodes = []
    ordered_matrices = []
    ordered_skinned_objects = []
    ordered_unskinned_objects = []

    root_node_indices = []
    node_id_to_node_index = {}
    node_id_to_object_index = {}
    node_id_to_matrix_index = {}

    texture_names = set()
    shader_names = set()
    node_names = set()

    # Order the nodes
    # Depth-first indexing
    # Track touched nodes in set T(n)?
    root_gmd_nodes = scene.overall_hierarchy.roots
    for i, (_, gmd_node) in enumerate(depth_first_iterate(root_gmd_nodes)):
        # stackop = none
        # if has parent and all other children of your parent have been touched - stackop += pop
        # the depth_first_iterate iterates through children in order
        #   -> if we are the last child, all others must have been touched
        want_pop = bool(gmd_node.parent) and gmd_node.parent.children[-1] is gmd_node
        # if not leaf: stackop += push
        want_push = bool(gmd_node.children)

        stack_op = NodeStackOp.NoOp
        if want_pop:
            stack_op = NodeStackOp.Pop
            if want_push:
                stack_op = NodeStackOp.PopPush
        elif want_push:
            stack_op = NodeStackOp.Push

        if len(gmd_node.name.encode("shift-jis")) > 30:
            error.fatal(f"Node {gmd_node.name} has a name that's longer than 30 bytes long. Please shorten it!")

        # emit (node, stackop)
        ordered_nodes.append((gmd_node, stack_op))
        node_id_to_node_index[id(gmd_node)] = i

        # if node is instance of GMDObject (skinned or unskinned) add to ordered_objects
        if isinstance(gmd_node, GMDSkinnedObject):
            ordered_skinned_objects.append(gmd_node)

        if isinstance(gmd_node, GMDUnskinnedObject):
            ordered_unskinned_objects.append(gmd_node)

        if isinstance(gmd_node, GMDSkinnedObject) and not gmd_node.mesh_list:
            error.fatal(f"Skinned Object {gmd_node.name} has no meshes, cannot export")

        if isinstance(gmd_node, GMDUnskinnedObject) and not gmd_node.children and not gmd_node.mesh_list:
            error.info(f"Unskinned object {gmd_node.name} has no meshes and no children.")

        # if node is bone or unskinned, emit a matrix
        if isinstance(gmd_node, (GMDBone, GMDUnskinnedObject)):
            node_id_to_matrix_index[id(gmd_node)] = len(ordered_matrices)
            ordered_matrices.append(gmd_node.matrix)
        # else:
        #     # also emit an identity matrix for skinned meshes just in case - it can't hurt
        #     node_id_to_matrix_index[id(gmd_node)] = len(ordered_matrices)
        #     ordered_matrices.append(Matrix.Identity(4))

        # if node has no parent, add index to roots
        if not gmd_node.parent:
            root_node_indices.append(i)

        # Add name to node names
        node_names.add(gmd_node.name)

    # Put unskinned objects before skinned ones
    # Skinned objects don't have matrices, so don't put them before things that do,
    # because it's a sequential id and it could go wrong.
    ordered_objects = ordered_unskinned_objects + ordered_skinned_objects
    node_id_to_object_index = build_index_mapping(ordered_objects, key=id)

    # make sure to maintain original object order for scene
    # involves making sure the DFA happens with objects in order

    # collect meshes
    meshes: List[GMDMesh] = [
        mesh
        for obj in ordered_objects
        for mesh in obj.mesh_list
    ]

    for mesh in meshes:
        shader_names.add(mesh.attribute_set.shader.name)

        if mesh.attribute_set.texture_diffuse:
            texture_names.add(mesh.attribute_set.texture_diffuse)
        if mesh.attribute_set.texture_refl:
            texture_names.add(mesh.attribute_set.texture_refl)
        if mesh.attribute_set.texture_multi:
            texture_names.add(mesh.attribute_set.texture_multi)
        if mesh.attribute_set.texture_rm:
            texture_names.add(mesh.attribute_set.texture_rm)
        if mesh.attribute_set.texture_rs:
            texture_names.add(mesh.attribute_set.texture_rs)
        if mesh.attribute_set.texture_normal:
            texture_names.add(mesh.attribute_set.texture_normal)
        if mesh.attribute_set.texture_rt:
            texture_names.add(mesh.attribute_set.texture_rt)
        if mesh.attribute_set.texture_rd:
            texture_names.add(mesh.attribute_set.texture_rd)

    # build texture, node name pools
    texture_names, texture_names_index = build_pools(texture_names)
    node_names, node_names_index = build_pools(node_names)

    # Order attributesets first.
    #  then, order meshes based only on attributesets.
    #  then, order vertexlayouts independently.

    # ordering meshes:
    # build list of vertex buffer layouts to use
    # TODO - sorting order is required for Dragon Engine, but not other engines?
    # TODO - with this setup K2 kiryu has unused shader names?
    # YK2 kiryu sort order is by prefix (sd_o*, sd_d*, sd_c*, sd_b*) and then some unknown ordering within those groups.
    # This will achieve the requested ordering for prefixes, but not for other things.
    # However, we only care about ordering transparent shaders together at the end.
    def compare_attr_sets(a1: GMDAttributeSet, a2: GMDAttributeSet):
        a1_prefix = re.match(r'^[a-z]+_[a-z]', a1.shader.name).group(0)
        a2_prefix = re.match(r'^[a-z]+_[a-z]', a2.shader.name).group(0)

        if a1_prefix < a2_prefix:
            # sort by inverted prefix first
            return 1
        elif a1_prefix > a2_prefix:
            # sort by inverted prefix first
            return -1
        else:
            # just sort by name???
            if a1.shader.name > a2.shader.name:
                return 1
            elif a1.shader.name < a2.shader.name:
                return -1
            else:
                return 0

    # Order the attribute sets, and get a nice order for shaders too
    expected_attribute_set_order = sorted({id(m.attribute_set): m.attribute_set for m in meshes}.values(),
                                          key=functools.cmp_to_key(compare_attr_sets))
    shader_names = [a.shader.name for a in expected_attribute_set_order]
    # remove dupes
    shader_names = list(dict.fromkeys(shader_names))
    shader_names, shader_names_index = build_pools(shader_names)

    known_vertex_layouts_set: Set[GMDVertexBufferLayout] = {
        mesh.vertices_data.layout
        for mesh in meshes
    }
    # sort by descending flags int value (?)
    known_vertex_layouts_and_flags = [(l, generate_vertex_layout_packing_flags(l)) for l in known_vertex_layouts_set]
    known_vertex_layouts_and_flags.sort(key=lambda l_with_flags: l_with_flags[1], reverse=True)
    vertex_layout_groups = []
    for layout, flag in known_vertex_layouts_and_flags:
        meshes_for_buffer = [m for m in meshes if m.attribute_set.shader.vertex_buffer_layout == layout]
        # sort meshes by id(material) - just to group the common materials together
        meshes_for_buffer.sort(key=lambda m: expected_attribute_set_order.index(m.attribute_set))
        # emit buffer_layout, meshes_for_buffer
        vertex_layout_groups.append((layout, flag, meshes_for_buffer))

    # ordered_meshes = sum([ms for _, _, ms in vertex_layout_groups], [])
    ordered_meshes = meshes[:]
    ordered_meshes.sort(key=lambda m: expected_attribute_set_order.index(m.attribute_set))
    mesh_id_to_index = build_index_mapping(ordered_meshes, key=id)

    mesh_id_to_object_index = {}
    # These are only for skinned meshes
    mesh_id_to_matrixlist = {}
    mesh_matrixlist_set = set()
    for object_idx, object in enumerate(ordered_objects):
        for mesh in object.mesh_list:
            if id(mesh) in mesh_id_to_object_index:
                error.fatal(
                    f"Mesh is mapped to two objects {object.name} and {ordered_objects[mesh_id_to_object_index[id(mesh)]].name}")
            mesh_id_to_object_index[id(mesh)] = object_idx

            if isinstance(object, GMDSkinnedObject):
                if not isinstance(mesh, GMDSkinnedMesh):
                    error.fatal(f"SkinnedObject {object.name} has unskinned mesh")
                matrixlist = tuple([node_id_to_matrix_index[id(bone)] for bone in mesh.relevant_bones])
                mesh_id_to_matrixlist[id(mesh)] = matrixlist
                mesh_matrixlist_set.add(matrixlist)

    mesh_matrixlist = list(mesh_matrixlist_set)
    mesh_matrixlist_index = build_index_mapping(mesh_matrixlist)

    if set(mesh_id_to_index.keys()) != set(mesh_id_to_object_index.keys()):
        error.fatal("Somehow the mapping of mesh -> mesh index maps different meshes than the mesh -> object index")

    # Order the attribute sets
    attribute_set_id_to_mesh_index_range = {}
    ordered_attribute_sets = []
    attr_index_start = -1
    for i, m in enumerate(ordered_meshes):
        if not ordered_attribute_sets:
            ordered_attribute_sets.append(m.attribute_set)
            attr_index_start = i
        elif m.attribute_set != ordered_attribute_sets[-1]:
            curr_attribute_set = ordered_attribute_sets[-1]
            attr_index_end = i
            attribute_set_id_to_mesh_index_range[id(curr_attribute_set)] = (attr_index_start, attr_index_end)
            attr_index_start = i
            ordered_attribute_sets.append(m.attribute_set)
    if ordered_attribute_sets:
        attribute_set_id_to_mesh_index_range[id(ordered_attribute_sets[-1])] = (attr_index_start, len(ordered_meshes))
    if ordered_attribute_sets != expected_attribute_set_order:
        error.recoverable(f"Export Error - Attribute Sets were reordered from the intended order!")

    # make index mapping for ordered_materials
    attribute_set_id_to_index = build_index_mapping(ordered_attribute_sets, key=id)

    # Order the materials
    material_ids = set()
    ordered_materials = []
    for attribute_set in ordered_attribute_sets:
        if id(attribute_set.material) not in material_ids:
            ordered_materials.append(attribute_set.material)
            material_ids.add(id(attribute_set.material))
    material_id_to_index = build_index_mapping(ordered_materials, key=id)

    return RearrangedData(
        ordered_nodes=ordered_nodes,
        ordered_matrices=ordered_matrices,
        ordered_objects=ordered_objects,

        root_node_indices=root_node_indices,
        node_id_to_node_index=node_id_to_node_index,
        node_id_to_object_index=node_id_to_object_index,
        object_id_to_matrix_index=node_id_to_matrix_index,

        texture_names=texture_names,
        texture_names_index=texture_names_index,
        shader_names=shader_names,
        shader_names_index=shader_names_index,
        node_names=node_names,
        node_names_index=node_names_index,

        # Tuple of (layout, layout_vertex_packing_flags, meshes)
        vertex_layout_groups=vertex_layout_groups,

        ordered_meshes=ordered_meshes,
        mesh_id_to_index=mesh_id_to_index,
        mesh_id_to_object_index=mesh_id_to_object_index,
        # These are only for skinned meshes
        mesh_id_to_matrixlist=mesh_id_to_matrixlist,
        mesh_matrixlist=mesh_matrixlist,
        mesh_matrixlist_index=mesh_matrixlist_index,

        ordered_attribute_sets=ordered_attribute_sets,
        attribute_set_id_to_index=attribute_set_id_to_index,
        # List of [start, end_exclusive) ranges
        attribute_set_id_to_mesh_index_range=attribute_set_id_to_mesh_index_range,

        ordered_materials=ordered_materials,
        material_id_to_index=material_id_to_index,

    )
