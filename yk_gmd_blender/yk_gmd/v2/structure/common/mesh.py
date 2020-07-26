from dataclasses import dataclass
from typing import List

from yk_gmd_blender.structurelib.base import StructureUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint32


@dataclass(frozen=True)
class Indices_YK1:
    index_offset: int
    index_count: int

    def extract_range(self, data: List[int]) -> List[int]:
        return data[self.index_offset:self.index_offset+self.index_count]

Indices_YK1_Unpack = StructureUnpacker(
    Indices_YK1,
    fields=[
        ("index_count", c_uint32),
        ("index_offset", c_uint32),
    ]
)


@dataclass(frozen=True)
class Mesh:
    index: int
    attribute_index: int
    vertex_buffer_index: int
    object_index: int
    node_index: int

    vertex_offset: int
    vertex_count: int

    # Each vertex in the mesh can be linked to up to 4 matrices.
    # These matrices are linked to bones in the skeleton, and as the bones move the matrices are updated, which updates the vertices
    matrixlist_offset: int
    matrixlist_length: int

    triangle_list_indices: Indices_YK1
    noreset_strip_indices: Indices_YK1
    reset_strip_indices: Indices_YK1

    padding: int = 0


Mesh_Unpack = StructureUnpacker(
    Mesh,
    fields=[
        ("index", c_uint32),
        ("attribute_index", c_uint32),
        ("vertex_buffer_index", c_uint32),
        ("vertex_count", c_uint32),

        ("triangle_list_indices", Indices_YK1_Unpack),
        ("noreset_strip_indices", Indices_YK1_Unpack),
        ("reset_strip_indices", Indices_YK1_Unpack),

        ("matrixlist_length", c_uint32),
        ("matrixlist_offset", c_uint32),

        ("node_index", c_uint32),
        ("object_index", c_uint32),

        ("padding", c_uint32), # Always 0

        ("vertex_offset", c_uint32)
    ]
)