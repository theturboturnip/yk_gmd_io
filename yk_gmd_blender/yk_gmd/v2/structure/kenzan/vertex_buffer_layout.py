from dataclasses import dataclass

from yk_gmd_blender.structurelib.base import StructureUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint32, c_uint64
from yk_gmd_blender.yk_gmd.v2.structure.common.vertex_buffer_layout import VertexBufferLayout


@dataclass(frozen=True)
class VertexBufferLayout_Kenzan(VertexBufferLayout):
    padding: int = 0


VertexBufferLayout_Kenzan_Unpack = StructureUnpacker(
    VertexBufferLayout_Kenzan,
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