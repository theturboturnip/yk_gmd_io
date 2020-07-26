import collections
from collections import deque
from typing import List, Dict, Tuple, Deque

from mathutils import Vector, Quaternion

from yk_gmd_blender.structurelib.primitives import c_uint16
from yk_gmd_blender.yk_gmd.v2.structure.common.attribute import Attribute
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStr
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import Mesh, Indices_YK1
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeStackOp, Node, NodeType
from yk_gmd_blender.yk_gmd.v2.structure.yk1.file import FileData_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.object import Object_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.vertex_buffer_layout import VertexBufferLayout_YK1
from yk_gmd_blender.yk_gmd.abstract.bone import GMDBone
from yk_gmd_blender.yk_gmd.abstract.material import GMDMaterial, GMDMaterialTextureIndex
from yk_gmd_blender.yk_gmd.abstract.scene import GMDScene
from yk_gmd_blender.yk_gmd.abstract.submesh import GMDSubmesh
from yk_gmd_blender.yk_gmd.abstract.vector import Vec3, Quat, Vec4
from yk_gmd_blender.yk_gmd.abstract.vertices import GMDVertexBuffer, GMDVertexBufferLayout, GMDVertex, BoneWeight

__all__ = [
    "convert_YK1_to_legacy_abstraction",
    "package_legacy_abstraction_to_YK1",
]


def _extract_legacy_materials(data: FileData_YK1, abstract_vertex_buffers: List[GMDVertexBuffer]) -> List[GMDMaterial]:
    materials = []
    shader_vb_layouts = {}

    for attr in data.attribute_arr:
        shader_name = data.shader_arr[attr.shader_index].text
        textures = {
            GMDMaterialTextureIndex.Diffuse: data.texture_arr[attr.texture_diffuse.tex_index].text,
            GMDMaterialTextureIndex.Normal: data.texture_arr[attr.texture_normal.tex_index].text
        }
        # To find the vertex buffer layout, check to see which submeshes use the material and then see what layout is used.
        # Assumed that each shader requires a specific layout.
        if shader_name not in shader_vb_layouts:
            for mesh in data.mesh_arr:
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


def _extract_legacy_vertex_buffers(data: FileData_YK1, vertex_big_endian: bool) -> Tuple[
    List[GMDVertexBuffer], Dict[GMDVertexBufferLayout, VertexBufferLayout_YK1]]:
    vertex_buffers = []
    vertex_buffer_layouts = {}
    vertex_bytes = data.vertex_data
    for layout in data.vertex_buffer_arr:
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


def _extract_legacy_node_heirarchy(data: FileData_YK1) -> Dict[int, GMDBone]:
    parent_stack: Deque[int] = deque()
    bone_index_to_object = {}

    for node_struct in data.node_arr:
        # "Skin" types are objects, and the legacy exporter shouldn't care about objects
        if node_struct.node_type == NodeType.Skin or node_struct.object_index != -1:
            continue

        name = data.node_name_arr[node_struct.name_index].text
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

        if 0 <= node_struct.matrix_index < len(data.matrix_arr):
            bone.set_matrix(data.matrix_arr[node_struct.matrix_index])

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
        for bone_info in data.node_arr:
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


def _extract_legacy_submeshes(data: FileData_YK1, materials: List[GMDMaterial],
                              vertex_buffers: List[GMDVertexBuffer]) -> List[GMDSubmesh]:
    submeshes = []

    for mesh_struct in data.mesh_arr:
        material = materials[mesh_struct.attribute_index]
        relevant_bone_bytestr = data.mesh_matrix_bytestrings[
                                mesh_struct.matrixlist_offset:mesh_struct.matrixlist_offset + mesh_struct.matrixlist_length + 1]
        relevant_bones = [
            int(x) for x in relevant_bone_bytestr[1:]  # First byte is length, remove it
        ]
        if len(relevant_bones) != mesh_struct.matrixlist_length:
            raise Exception(f"Length of relevant bones bytestring didn't match expected")
        vtx_buffer = vertex_buffers[mesh_struct.vertex_buffer_index]
        start = mesh_struct.vertex_offset
        cnt = mesh_struct.vertex_count
        vertices = vtx_buffer.vertices[start:start + cnt]

        # This used to reverse endians, but that isn't necessary anymore
        parse_index = lambda x: 0xFFFF if x == 0xFFFF else (x - start)

        # print(submesh_struct.indices_triangle.extract_range(self.structs.index_data))
        triangle_list_indices = [parse_index(x) for x in
                                 mesh_struct.triangle_list_indices.extract_range(data.index_data)]
        noreset_strip_indices = [parse_index(x) for x in
                                 mesh_struct.noreset_strip_indices.extract_range(data.index_data)]
        reset_strip_indices = [parse_index(x) for x in
                               mesh_struct.reset_strip_indices.extract_range(data.index_data)]

        # parent_part = part_index_to_gmdpart[submesh_struct.part_number]

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


# NOTE - object indices are important!!! they must be maintained
def convert_YK1_to_legacy_abstraction(data: FileData_YK1) -> GMDScene:
    # get bones
    node_index_map = _extract_legacy_node_heirarchy(data)
    node_name_map = {b.name: b for b in node_index_map.values()}
    node_roots = [b for b in node_index_map.values() if not b.parent]

    # get vertex buffers
    vertices_big_endian = (data.vertex_endian_check - 1 <= 2) or (data.vertex_endian_check == 6)
    vertex_buffers, abstract_vb_layout_to_struct = _extract_legacy_vertex_buffers(data, vertices_big_endian)
    # get materials
    materials = _extract_legacy_materials(data, vertex_buffers)
    # get submeshes/parts
    submeshes = _extract_legacy_submeshes(data, materials, vertex_buffers)

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


def package_legacy_abstraction_to_YK1(big_endian: bool, initial_data: FileData_YK1, scene: GMDScene) -> FileData_YK1:
    # Check vertex endianness
    # TODO: Add function to FileData to do this logic
    vertices_big_endian = (initial_data.vertex_endian_check - 1 <= 2) or (initial_data.vertex_endian_check == 6)

    # Generate string pool
    texture_names = initial_data.texture_arr[:]
    shader_names = initial_data.shader_arr[:]
    node_names = initial_data.node_name_arr[:]

    # Generate nodes and global object
    nodes = [n for n in initial_data.node_arr if n.object_index == -1]
    # Check that the indices are in a [0...n] range
    if [n.index for n in nodes] != [x for x in range(len(nodes))]:
        raise Exception("stripping non-bone nodes from initial data led to index discrepancy")
    global_object_node = Node(
        index=len(nodes),
        parent_of=-1,
        sibling_of=-1,
        object_index=0,
        matrix_index=len(nodes),  # TODO: Does changing this do anything?
        stack_op=NodeStackOp.PopPush,
        name_index=len(node_names),
        node_type=NodeType.Skin,

        pos=Vector((0, 0, 0, 0)),
        rot=Quaternion(),
        scale=Vector((1, 1, 1, 0)),

        bone_pos=Vector((0, 0, 0, 1)),
        bone_axis=Quaternion(),
        padding=Vector((0, 0, 0, 0))
    )
    node_names.append(ChecksumStr.make_from_str("[l0]global_object"))
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
    global_object = Object_YK1(
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

    vertex_buffer_layout_structs: List[VertexBufferLayout_YK1] = []
    overall_vertex_buffer_data = bytearray()
    overall_index_buffer_data: List[int] = []
    submesh_structs: List[Mesh] = []
    submesh_bonelists = bytearray()

    for abstract_layout, vb_submeshes in vb_layout_submeshes:
        # Create a copy of the correct layout structure, in case we've reordered it or something
        original = scene.abstract_vb_layout_to_struct[abstract_layout]
        layout_index = len(vertex_buffer_layout_structs)
        layout_vertex_count = sum(len(s.vertices) for s in vb_submeshes)
        layout_vertex_data_offset = len(overall_vertex_buffer_data)
        layout_vertex_data_length = layout_vertex_count * original.bytes_per_vertex

        layout_struct = VertexBufferLayout_YK1(
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
            pack_index = lambda x: 0xFFFF if x == 0xFFFF else (x + vertex_offset)

            # Set up the pointer for the next set of indices
            triangle_indices = Indices_YK1(
                index_offset=len(overall_index_buffer_data),
                index_count=len(s.triangle_indices)
            )
            # then add them to the data
            overall_index_buffer_data += [pack_index(x) for x in s.triangle_indices]

            # Set up the pointer for the next set of indices
            triangle_strip_noreset_indices = Indices_YK1(
                index_offset=len(overall_index_buffer_data),
                index_count=len(s.triangle_strip_noreset_indices)
            )
            # then add them to the data
            overall_index_buffer_data += [pack_index(x) for x in s.triangle_strip_noreset_indices]

            # Set up the pointer for the next set of indices
            triangle_strip_reset_indices = Indices_YK1(
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
            submesh_bonelists += bytes([len(s.relevant_bones)] + s.relevant_bones)

            submesh_structs.append(Mesh(
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
        new_attribute_packs.append(Attribute(
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
        version=initial_data.version,
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
        finish=initial_data.finish,
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
