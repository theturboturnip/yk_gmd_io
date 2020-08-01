import array
import time
from dataclasses import dataclass
from typing import List, Dict, Tuple, Iterable, TypeVar, Callable, Union, overload, Optional, Set

from mathutils import Matrix

from yk_gmd_blender.structurelib.base import FixedSizeArrayUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint16
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDMaterial, GMDAttributeSet, GMDUnk12, GMDUnk14
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene, depth_first_iterate
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBufferLayout, GMDShader, GMDVertexBuffer, VecStorage
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_object import GMDSkinnedObject, GMDUnskinnedObject
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
    # packed_mesh_matrixlist: bytes
    # packed_mesh_matrixlist_index: Dict[Tuple, int]
    pass


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
    # return mapping of string -> index in list
    pool = [ChecksumStrStruct.make_from_str(s) for s in strs]
    pool.sort(key=lambda css: css.checksum)
    return pool, build_index_mapping(pool, key=lambda css: css.text)


def pack_mesh_matrix_strings(mesh_matrixlist: List[Tuple[int, ...]], pack_as_16bit: bool) -> Tuple[bytes, Dict[Tuple, int]]:
    matrixlist_bytearray = bytearray()
    matrixlist_index = {}
    for matrixlist in mesh_matrixlist:
        matrixlist_index[matrixlist] = len(matrixlist_bytearray)

        if pack_as_16bit:
            matrixlist_bytearray += bytes([len(matrixlist)])
            FixedSizeArrayUnpacker(c_uint16, len(matrixlist)).pack(big_endian=True, value=matrixlist,
                                                                         append_to=matrixlist_bytearray)
        else:
            matrixlist_bytearray += bytes([len(matrixlist)] + list(matrixlist))

    return bytes(matrixlist_bytearray), matrixlist_index

def generate_vertex_layout_packing_flags(layout: GMDVertexBufferLayout) -> int:
    return layout.packing_flags
    # vertex_packing_flags = 0
    #
    # def pack_vector_type(vec_storage: Optional[VecStorage]) -> int:
    #
    #
    # # pos_count = extract_bits(0, 3)
    # # pos_precision = extract_bits(3, 1)
    # # if pos_precision == 1:
    # #     pos_storage = VecStorage.Vec3Half if pos_count == 3 else VecStorage.Vec4Half
    # # else:
    # #     pos_storage = VecStorage.Vec3Full if pos_count == 3 else VecStorage.Vec4Full
    # if layout.pos_storage in [VecStorage.Vec3Full, VecStorage.Vec3Half]:
    #     vertex_packing_flags |= 3
    # else:
    #     vertex_packing_flags |= 4
    # if layout.pos_storage in [VecStorage.Vec3Half, VecStorage.Vec4Half]:
    #     vertex_packing_flags |= (1 << 3)



# Note - checked=False disables bitchecks but the time taken is the same, dw about it
def build_vertex_buffer_layout_from_flags(vertex_packing_flags: int, checked: bool = True) -> GMDVertexBufferLayout:
    #item_packing_flags = vertex_packing_flags & 0xFFFF_FFFF
    #uv_list_flags = vertex_packing_flags >> 32

    # This derived from the 010 template

    if checked:
        touched_packing_bits = set()

        def touch_bits(bit_indices: Iterable[int]):
            touched_bits = set(bit_indices)
            if touched_bits.intersection(touched_packing_bits):
                raise Exception(f"Retouching bits {touched_bits.intersection(touched_packing_bits)}")
            touched_packing_bits.update(touched_bits)
    else:
        def touch_bits(bit_indices: Iterable[int]):
            pass

    def extract_bits(start, length):
        touch_bits(range(start, start+length))

        # Extract bits by shifting down to start and generating a mask of `length` 1's in binary
        return (vertex_packing_flags >> start) & int('1'*length, 2)

    def extract_bitmask(bitmask):
        touch_bits([i for i in range(32) if ((bitmask >> i) & 1)])

        return vertex_packing_flags & bitmask

    def extract_vector_type(en: bool, start: int, expected_full_precision: VecStorage) -> Optional[VecStorage]:
        bits = extract_bits(start, 2)
        if en:
            if bits == 0:
                return expected_full_precision
            elif bits == 1:
                return VecStorage.Vec4Half
            else:
                return VecStorage.Vec4Fixed
        else:
            return None

    # pos can be (3 or 4) * (half or full) floats
    pos_count = extract_bits(0, 3)
    pos_precision = extract_bits(3, 1)
    if pos_precision == 1:
        pos_storage = VecStorage.Vec3Half if pos_count == 3 else VecStorage.Vec4Half
    else:
        pos_storage = VecStorage.Vec3Full if pos_count == 3 else VecStorage.Vec4Full

    weight_en = extract_bitmask(0x70)
    weights_storage = extract_vector_type(weight_en, 7, expected_full_precision=VecStorage.Vec4Full)

    bones_en = extract_bitmask(0x200)
    bones_storage = VecStorage.Vec4Fixed if bones_en else None

    normal_en = extract_bitmask(0x400)
    normal_storage = extract_vector_type(normal_en, 11, expected_full_precision=VecStorage.Vec3Full)

    tangent_en = extract_bitmask(0x2000)
    tangent_storage = extract_vector_type(tangent_en, 14, expected_full_precision=VecStorage.Vec3Full)

    unk_en = extract_bitmask(0x0001_0000)
    unk_storage = extract_vector_type(unk_en, 17, expected_full_precision=VecStorage.Vec3Full)

    # TODO: Are we sure these bits aren't used for something?
    touch_bits((19, 20))

    # col0 is diffuse and opacity for GMD versions up to 0x03000B
    col0_en = extract_bitmask(0x0020_0000)
    col0_storage = extract_vector_type(col0_en, 22, expected_full_precision=VecStorage.Vec4Full)

    # col1 is specular for GMD versions up to 0x03000B
    col1_en = extract_bitmask(0x0100_0000)
    col1_storage = extract_vector_type(col1_en, 25, expected_full_precision=VecStorage.Vec4Full)

    # Extract the uv_enable and uv_count bits, to fill out the first 32 bits of the flags
    uv_en = extract_bits(27, 1)
    uv_count = extract_bits(28, 4)
    uv_storages = []
    if uv_count:
        if uv_en:
            # Iterate over all uv bits, checking for active UV slots
            for i in range(8):
                uv_slot_bits = extract_bits(32 + (i * 4), 4)
                if uv_slot_bits == 0xF:
                    continue

                format_bits = (uv_slot_bits >> 2) & 0b11
                if format_bits in [2, 3]:
                    # This should be formatted as a [-1, 1] range thing
                    # This is currently set in gmd_shader.py, although really it should be set in here
                    # TODO: shift make_vector_unpacker logic out of abstract/gmd_shader and into here
                    uv_storages.append(VecStorage.Vec4Fixed)
                else:
                    bit_count_idx = uv_slot_bits & 0b11
                    bit_count = (2, 3, 4, 1)[bit_count_idx]

                    if bit_count == 1:
                        raise Exception(f"UV with 1 element encountered - unsure how to proceed")
                    elif bit_count == 2:
                        uv_storages.append(VecStorage.Vec2Half if format_bits else VecStorage.Vec2Full)
                    elif bit_count == 3:
                        uv_storages.append(VecStorage.Vec3Half if format_bits else VecStorage.Vec3Full)
                    elif bit_count == 4:
                        uv_storages.append(VecStorage.Vec4Half if format_bits else VecStorage.Vec4Full)

                if len(uv_storages) == uv_count:
                    # Touch the rest of the bits
                    touch_bits(range(32 + ((i+1)*4), 64))
                    break

            if len(uv_storages) != uv_count:
                raise Exception(f"Layout Flags {vertex_packing_flags:016x} claimed to have {uv_count} UVs but specified {len(uv_storages)}")
        else:
            # Touch all of the uv bits, without doing anything with them
            touch_bits(range(32, 64))
            # TODO: Raise here? This is an unknown item
            uv_storages = [VecStorage.Vec2Full] * uv_count
        pass

    #print(uv_storages)

    if checked:
        expected_touched_bits = {x for x in range(64)}
        if touched_packing_bits != expected_touched_bits:
            raise Exception(f"Incomplete vertex format parse - bits {expected_touched_bits.difference(touched_packing_bits)} were not touched")

    print(f"packing-flags: {vertex_packing_flags:x}")

    return GMDVertexBufferLayout.make_vertex_buffer_layout(
        pos_storage=pos_storage,
        weights_storage=weights_storage,
        bones_storage=bones_storage,
        normal_storage=normal_storage,
        tangent_storage=tangent_storage,
        unk_storage=unk_storage,
        col0_storage=col0_storage,
        col1_storage=col1_storage,
        uv_storages=uv_storages,

        packing_flags=vertex_packing_flags,
    )

def arrange_data_for_export(scene: GMDScene) -> RearrangedData:
    # Note - flags
        # many bones flag is important, but so are the others - look into which ones are supposed to be there
        # is relative-indexing set in a flag?

    # ordered_nodes = []
    # node_id_to_node_index = {}
    # ordered_matrices = []
    # node_id_to_matrix_index = {}
    # root_node_indices = []
    #
    # skinned_objects = list(scene.skinned_objects.depth_first_iterate())
    # unskinned_objects = list(scene.unskinned_objects.depth_first_iterate())

    ordered_nodes = []
    ordered_matrices = []
    ordered_objects = []

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
    root_gmd_nodes = []
    if scene.bones:
        root_gmd_nodes += scene.bones.roots
    if scene.skinned_objects:
        root_gmd_nodes += scene.skinned_objects.roots
    if scene.unskinned_objects:
        root_gmd_nodes += scene.unskinned_objects.roots
    for i, gmd_node in enumerate(depth_first_iterate(root_gmd_nodes)):
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

        # emit (node, stackop)
        ordered_nodes.append((gmd_node, stack_op))
        node_id_to_node_index[id(gmd_node)] = i

        # if node is instance of GMDObject (skinned or unskinned) add to ordered_objects
        if isinstance(gmd_node, (GMDSkinnedObject, GMDUnskinnedObject)):
            node_id_to_object_index[id(gmd_node)] = len(ordered_objects)
            ordered_objects.append(gmd_node)

        # if node is bone or unskinned, emit a matrix
        if isinstance(gmd_node, (GMDBone, GMDUnskinnedObject)):
            node_id_to_matrix_index[id(gmd_node)] = len(ordered_matrices)
            ordered_matrices.append(gmd_node.matrix)

        # if node has no parent, add index to roots
        if not gmd_node.parent:
            root_node_indices.append(i)

        # Add name to node names
        node_names.add(gmd_node.name)

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
        if mesh.attribute_set.texture_unk1:
            texture_names.add(mesh.attribute_set.texture_unk1)
        if mesh.attribute_set.texture_rs:
            texture_names.add(mesh.attribute_set.texture_rs)
        if mesh.attribute_set.texture_normal:
            texture_names.add(mesh.attribute_set.texture_normal)
        if mesh.attribute_set.texture_rt:
            texture_names.add(mesh.attribute_set.texture_rt)
        if mesh.attribute_set.texture_rd:
            texture_names.add(mesh.attribute_set.texture_rd)

    # build texture, shader, node name pools
    texture_names, texture_names_index = build_pools(texture_names)
    shader_names, shader_names_index = build_pools(shader_names)
    node_names, node_names_index = build_pools(node_names)

    # ordering meshes:
    # build list of vertex buffer layouts to use
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
        meshes_for_buffer.sort(key=lambda m: id(m.attribute_set))
        # emit buffer_layout, meshes_for_buffer
        vertex_layout_groups.append((layout, flag, meshes_for_buffer))

    ordered_meshes = sum([ms for _, _, ms in vertex_layout_groups], [])
    mesh_id_to_index = build_index_mapping(ordered_meshes, key=id)

    mesh_id_to_object_index = {}
    # These are only for skinned meshes
    mesh_id_to_matrixlist = {}
    mesh_matrixlist_set = set()
    for object_idx, object in enumerate(ordered_objects):
        for mesh in object.mesh_list:
            if id(mesh) in mesh_id_to_object_index:
                raise Exception(f"Mesh is mapped to two objects {object.name} and {ordered_objects[mesh_id_to_object_index[id(mesh)]].name}")
            mesh_id_to_object_index[id(mesh)] = object_idx

            if isinstance(object, GMDSkinnedObject):
                if not isinstance(mesh, GMDSkinnedMesh):
                    raise Exception(f"SkinnedObject {object.name} has unskinned mesh")
                matrixlist = tuple([node_id_to_matrix_index[id(bone)] for bone in mesh.relevant_bones])
                mesh_id_to_matrixlist[id(mesh)] = matrixlist
                mesh_matrixlist_set.add(matrixlist)

    mesh_matrixlist = list(mesh_matrixlist_set)
    mesh_matrixlist_index = build_index_mapping(mesh_matrixlist)
    # mesh_id_to_matrix_string_index = {
    #     mesh_id:mesh_matrixlist.index(matrixlist)
    #     for mesh_id, matrixlist in mesh_id_to_matrixlist.items()
    # }

    if set(mesh_id_to_index.keys()) != set(mesh_id_to_object_index.keys()):
        raise Exception("Somehow the mapping of mesh -> mesh index maps different meshes than the mesh -> object index")

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
    attribute_set_id_to_mesh_index_range[id(ordered_attribute_sets[-1])] = (attr_index_start, len(ordered_meshes))

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

    # TODO: Build drawlists?

    # Build matrixlists
    # mesh_matrix_index_list_set = set()
    # mesh_id_to_matrixlist: Dict[int, List[int]] = {}
    # for mesh in ordered_meshes:
    #     if not isinstance(mesh, GMDSkinnedMesh):
    #         continue
    #
    #     matrix_list = [node_id_to_node_index[id(bone)] for bone in mesh.relevant_bones]
    #     mesh_matrix_index_list_set.add(tuple(matrix_list))
    #     mesh_id_to_matrixlist[id(mesh)] = matrix_list
    # mesh_matrixlist = [list(s) for s in mesh_matrix_index_list_set]
    # mesh_matrixlist_index = build_index_mapping(mesh_matrixlist, key=tuple)

    # now all arrangements should be made - next is to port into the respective file formats
    # this is for tomorrow tho

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


def build_vertex_buffers_from_structs(version_properties: VersionProperties,

                                      vertex_layout_arr: List[VertexBufferLayoutStruct], vertex_bytes: bytes,
                                      vertices_big_endian: bool,

                                      profile:bool = False) \
        -> List[GMDVertexBuffer]:

    abstract_vertex_buffers = []
    vertex_bytes_offset = 0
    for layout_struct in vertex_layout_arr:
        layout_build_start = time.time()
        abstract_layout = build_vertex_buffer_layout_from_flags(layout_struct.vertex_packing_flags)
        if abstract_layout.bytes_per_vertex() != layout_struct.bytes_per_vertex:
            raise Exception(f"Abstract Layout BPV {abstract_layout.bytes_per_vertex()} didn't match expected {layout_struct.bytes_per_vertex}\n"
                            f"Packing Flags {layout_struct.vertex_packing_flags:08x} created layout {abstract_layout}")

        unpack_start = time.time()

        abstract_vertex_buffer, vertex_bytes_offset = \
            abstract_layout.unpack_from(vertices_big_endian, layout_struct.vertex_count,
                                        vertex_bytes, vertex_bytes_offset)

        unpack_finish = time.time()

        unpack_delta = unpack_finish - unpack_start
        if profile:
            # Note - importing st_dead_sera takes ~3seconds total - this doesn't seem like a perf regression from the original tho
            # This profiling is here incase we want to optimize vertex unpacking
            print(f"Time to build layout: {unpack_start - layout_build_start}")
            print(f"Time to unpack {layout_struct.vertex_count} verts: {unpack_delta} ({unpack_delta/layout_struct.vertex_count * 1000:2f}ms/vert)")

        abstract_vertex_buffers.append(abstract_vertex_buffer)

    return abstract_vertex_buffers

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

            attr_flags=attribute_struct.flags,
            attr_extra_properties=attribute_struct.extra_properties,
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
        -> List[Union[GMDSkinnedMesh, GMDMesh]]:
    file_uses_relative_indices = version_properties.relative_indices_used
    file_uses_vertex_offset = version_properties.mesh_vertex_offset_used
    # TODO: Check if uses_relative_indices and not(uses_vertex_offset), that should error

    def read_bytestring(start_byte: int, length: int):
        if not mesh_matrix_bytestrings:
            return []

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
        index_offset = 0 if file_uses_relative_indices else mesh_struct.vertex_offset
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
        triangle_indices, min_index, max_index = process_indices(mesh_struct, mesh_struct.triangle_list_indices)
        triangle_strip_noreset_indices, min_index, max_index = process_indices(mesh_struct, mesh_struct.noreset_strip_indices, min_index, max_index)
        triangle_strip_reset_indices, min_index, max_index = process_indices(mesh_struct, mesh_struct.reset_strip_indices, min_index, max_index)

        if file_uses_vertex_offset and (not file_uses_relative_indices) and mesh_struct.vertex_offset != min_index:
            raise Exception(f"Mesh uses a minimum absolute index of {min_index}, but file specifies a vertex offset of {mesh_struct.vertex_offset}")

        vertex_start = mesh_struct.vertex_offset if file_uses_relative_indices else min_index
        vertex_end = vertex_start + mesh_struct.vertex_count

        if (not file_uses_relative_indices) and vertex_end < max_index:
            raise Exception(f"Mesh vertex_count is {mesh_struct.vertex_count} but indices show a range of length {max_index-min_index} is used.")

        relevant_bone_indices = read_bytestring(mesh_struct.matrixlist_offset, mesh_struct.matrixlist_length)
        if relevant_bone_indices:
            meshes.append(GMDSkinnedMesh(
                relevant_bones=[abstract_bones_ordered[bone_idx] for bone_idx in relevant_bone_indices],

                vertices_data=abstract_vertex_buffers[mesh_struct.vertex_buffer_index][vertex_start:vertex_end+1],

                triangle_indices=triangle_indices,
                triangle_strip_noreset_indices=triangle_strip_noreset_indices,
                triangle_strip_reset_indices=triangle_strip_reset_indices,

                attribute_set=abstract_attributes[mesh_struct.attribute_index]
            ))
        else:
            meshes.append(GMDMesh(
                vertices_data=abstract_vertex_buffers[mesh_struct.vertex_buffer_index][vertex_start:vertex_end + 1],

                triangle_indices=triangle_indices,
                triangle_strip_noreset_indices=triangle_strip_noreset_indices,
                triangle_strip_reset_indices=triangle_strip_reset_indices,

                attribute_set=abstract_attributes[mesh_struct.attribute_index]
            ))

    return meshes

def build_object_nodes(version_properties: VersionProperties,

                       abstract_meshes: List[GMDMesh], abstract_attribute_sets: List[GMDAttributeSet],

                       remaining_node_arr: List[NodeStruct], node_name_arr: List[ChecksumStrStruct],
                       object_drawlist_ptrs: List[int],
                       matrix_arr: List[Matrix], mesh_drawlists: bytes,
                       big_endian: bool) \
        -> Tuple[List[GMDSkinnedObject], List[GMDUnskinnedObject]]:
    skinned_objects = []
    unskinned_objects = []

    parent_stack = ParentStack()
    for node_struct in remaining_node_arr:
        name = node_name_arr[node_struct.name_index].text

        if node_struct.node_type == NodeType.MatrixTransform:
            raise Exception(f"Node {name} of type {node_struct.node_type} found after bone heirarchy had finished")

        # This is guaranteed to be some sort of object
        # Parse the drawlist
        object_abstract_meshes = []

        drawlist_ptr = object_drawlist_ptrs[node_struct.object_index]
        offset = drawlist_ptr
        drawlist_len, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
        zero, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
        for i in range(drawlist_len):
            material_idx, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
            mesh_idx, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)

            abstract_attribute_set = abstract_attribute_sets[material_idx]
            abstract_mesh = abstract_meshes[mesh_idx]
            if abstract_attribute_set != abstract_mesh.attribute_set:
                raise Exception(f"Object {name} specifies an unexpected material/mesh pair in it's drawlist, that doesn't match the mesh's requested material")

            object_abstract_meshes.append(abstract_mesh)
            pass

        if node_struct.node_type == NodeType.SkinnedMesh:
            if 0 <= node_struct.matrix_index < len(matrix_arr):
                raise Exception(f"Skinned object {name} references a valid matrix, even though skinned meshes aren't supposed to have them!")

            obj = GMDSkinnedObject(
                name=name,
                node_type=node_struct.node_type,

                pos=node_struct.pos,
                rot=node_struct.rot,
                scale=node_struct.scale,

                parent=parent_stack.peek() if parent_stack else None,

                mesh_list=object_abstract_meshes
            )
            skinned_objects.append(obj)
        else:
            if not(0 <= node_struct.matrix_index < len(matrix_arr)):
                raise Exception(f"Unskinned object {name} doesn't reference a valid matrix")

            matrix = matrix_arr[node_struct.matrix_index]

            obj = GMDUnskinnedObject(
                name=name,
                node_type=node_struct.node_type,

                pos=node_struct.pos,
                rot=node_struct.rot,
                scale=node_struct.scale,

                parent=parent_stack.peek() if parent_stack else None,

                matrix=matrix,

                mesh_list=object_abstract_meshes
            )
            unskinned_objects.append(obj)

        # Apply the stack operation to the parent_stack
        parent_stack.handle_node(node_struct.stack_op, obj)

    return skinned_objects, unskinned_objects


# TODO: Think about how to do this
def validate_scene(scene: GMDScene):
    pass