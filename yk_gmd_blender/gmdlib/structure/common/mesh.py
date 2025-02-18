from dataclasses import dataclass
from typing import List

from ....structurelib.base import StructureUnpacker
from ....structurelib.primitives import c_uint32


@dataclass(frozen=True)
class IndicesStruct:
    index_offset: int
    index_count: int

    def extract_range(self, data: List[int]) -> List[int]:
        return data[self.index_offset:self.index_offset + self.index_count]


IndicesStruct_Unpack = StructureUnpacker(
    IndicesStruct,
    fields=[
        ("index_count", c_uint32),
        ("index_offset", c_uint32),
    ]
)


@dataclass(frozen=True)
class MeshStruct:
    # Index of the Mesh structure in the array
    index: int
    # Mapped attribute set index
    attribute_index: int
    # Vertex buffer index
    vertex_buffer_index: int
    # Associated object index
    object_index: int
    # object's associated node index
    node_index: int

    # Minimum value of the associated indices in the index buffer
    min_index: int
    # Number of vertices referenced
    vertex_count: int
    # Index offset - if the index buffer references vertex X, we should remap it to reference vertex X + offset_from_index.
    # Used to allow 16bit index buffers to reference all vertices in a vertex buffer with >65535 vertices
    vertex_offset_from_index: int

    # Each vertex in the mesh can be linked to up to 4 matrices.
    # These matrices are linked to bones in the skeleton, and as the bones move the matrices are updated, which updates the vertices
    matrixlist_offset: int
    matrixlist_length: int

    triangle_list_indices: IndicesStruct
    noreset_strip_indices: IndicesStruct
    reset_strip_indices: IndicesStruct
