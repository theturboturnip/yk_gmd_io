from dataclasses import dataclass

from ....structurelib.base import StructureUnpacker
from ....structurelib.primitives import c_uint32, c_uint64
from ..common.vertex_buffer_layout import VertexBufferLayoutStruct


@dataclass(frozen=True)
class VertexBufferLayoutStruct_Kenzan(VertexBufferLayoutStruct):
    padding: int = 0


VertexBufferLayoutStruct_Kenzan_Unpack = StructureUnpacker(
    VertexBufferLayoutStruct_Kenzan,
    fields=[
        ("index", c_uint32),
        ("vertex_count", c_uint32),

        ("vertex_packing_flags", c_uint64),

        ("vertex_data_offset", c_uint32),
        ("vertex_data_length", c_uint32),
        ("bytes_per_vertex", c_uint32),

        ("padding", c_uint32),
    ]
)
