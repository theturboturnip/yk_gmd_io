from dataclasses import dataclass

from yk_gmd_blender.structurelib.base import StructureUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint32, c_uint64
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import MeshStruct, IndicesStruct_Unpack


@dataclass(frozen=True)
class MeshStruct_YK1(MeshStruct):
    pass


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

        ("flags", c_uint32),

        ("vertex_offset", c_uint32)
    ],
)