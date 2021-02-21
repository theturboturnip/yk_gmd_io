from dataclasses import dataclass


@dataclass(frozen=True)
class VertexBufferLayoutStruct:
    index: int

    vertex_count: int

    vertex_packing_flags: int
    bytes_per_vertex: int

    vertex_data_offset: int
    vertex_data_length: int