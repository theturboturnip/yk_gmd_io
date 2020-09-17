from dataclasses import dataclass
from typing import List

from yk_gmd_blender.structurelib.base import StructureUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint32
from yk_gmd_blender.yk_gmd.legacy.abstract.material import GMDMaterial
from yk_gmd_blender.yk_gmd.legacy.abstract.submesh import GMDSubmesh
from yk_gmd_blender.yk_gmd.legacy.abstract.vertices import GMDVertexBuffer


@dataclass(frozen=True)
class IndicesStruct:
    index_offset: int
    index_count: int

    def extract_range(self, data: List[int]) -> List[int]:
        return data[self.index_offset:self.index_offset+self.index_count]

IndicesStruct_Unpack = StructureUnpacker(
    IndicesStruct,
    fields=[
        ("index_count", c_uint32),
        ("index_offset", c_uint32),
    ]
)


@dataclass(frozen=True)
class MeshStruct:
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

    triangle_list_indices: IndicesStruct
    noreset_strip_indices: IndicesStruct
    reset_strip_indices: IndicesStruct

    flags: int = 0
