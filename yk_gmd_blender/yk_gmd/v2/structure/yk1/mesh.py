from dataclasses import dataclass

from yk_gmd_blender.structurelib.base import StructureUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint32, c_uint64, c_int32
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import MeshStruct, IndicesStruct_Unpack


@dataclass(frozen=True)
class MeshStruct_YK1(MeshStruct):
    # padding: int = 0

    def check_padding(self):
        if self.padding_maybe:
            print(f"Unexpected nonzero mesh padding {self.padding_maybe}")


MeshStruct_YK1_Unpack = StructureUnpacker(
    MeshStruct_YK1,
    fields=[
        ("index", c_uint32),
        ("attribute_index", c_uint32),
        ("vertex_buffer_index", c_uint32),
        ("vertex_count", c_uint32),

        ("triangle_list_indices", IndicesStruct_Unpack),
        ("noreset_strip_indices", IndicesStruct_Unpack),
        ("reset_strip_indices", IndicesStruct_Unpack),

        ("matrixlist_length", c_uint32),
        ("matrixlist_offset", c_uint32),

        ("node_index", c_uint32),
        ("object_index", c_uint32),

        ("padding_maybe", c_int32), # Always 0

        ("vertex_offset", c_uint32)
    ],
    load_validate=lambda m: m.check_padding()
)

#     ushort m_index; (index)
#     ushort m_attribute_index; (attribute_index)
#     ushort m_vb_index; (vertex_buffer_index)
#     ushort m_vertex_num; (vertex_count)

# (presumably derived from IndicesStruct)
#     uint m_index_offset;
#     uint m_index_num:24;
#     uint m_primitive_type:8;

#     struct t_relative_ptr<pxd::cgs_mesh_matrix_tbl,1> mp_matrix_tbl; (matrixlist_length/offset)


#     ushort m_node_index; (node_index)
#     ushort m_object_index; (object_index)

#     struct t_relative_long_ptr<pxd::cgs_mesh,0> mp_mesh; (padding???)

#     uint m_vertex_offset; (vertex_offset)
