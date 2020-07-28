from yk_gmd_blender.yk_gmd.legacy.abstract.scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.structure.common.legacy_abstractor import extract_legacy_node_heirarchy, \
    extract_legacy_vertex_buffers, extract_legacy_materials, extract_legacy_submeshes
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.file import FileData_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.version import FileProperties

__all__ = [
    "convert_Kenzan_to_legacy_abstraction",
]


# NOTE - object indices are important!!! they must be maintained
def convert_Kenzan_to_legacy_abstraction(data: FileData_Kenzan, version_props: FileProperties) -> GMDScene:
    vertices_big_endian = data.vertices_are_big_endian()

    # get bones
    node_index_map = extract_legacy_node_heirarchy(data.node_arr, data.node_name_arr, data.matrix_arr)
    node_name_map = {b.name: b for b in node_index_map.values()}
    node_roots = [b for b in node_index_map.values() if not b.parent]

    # get vertex buffers
    vertex_buffers, abstract_vb_layout_to_struct = extract_legacy_vertex_buffers(data.vertex_buffer_arr, data.vertex_data, vertices_big_endian)
    # get materials
    materials = extract_legacy_materials(data.attribute_arr, data.shader_arr, data.texture_arr, data.mesh_arr, vertex_buffers)
    # get submeshes/parts
    print(f"kenzan file {version_props.version_str} rel_idx={version_props.relative_indices_used}, vtx_off={version_props.vertex_offset_used}")
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