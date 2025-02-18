from dataclasses import dataclass

from ....structurelib.base import StructureUnpacker
from ....structurelib.primitives import c_uint32
from ..common.mesh import MeshStruct, IndicesStruct_Unpack


@dataclass(frozen=True)
class MeshStruct_Kenzan(MeshStruct):
    pass


MeshStruct_Kenzan_Unpack = StructureUnpacker(
    MeshStruct_Kenzan,
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

        ("min_index", c_uint32),

        ("vertex_offset_from_index", c_uint32)
    ]
)
