import array
from dataclasses import dataclass
from typing import List, Optional, Generator, Tuple, Iterable

import numpy as np

from .gmd_attributes import GMDAttributeSet
from .gmd_shader import GMDVertexBuffer, GMDSkinnedVertexBuffer
from .nodes.gmd_bone import GMDBone


def iterate_three(x: array.ArrayType) -> Generator[Tuple[int, int, int], None, None]:
    assert len(x) % 3 == 0
    i = iter(x)
    while True:
        try:
            a = next(i)
            b = next(i)
            c = next(i)
        except StopIteration:
            return
        yield a, b, c


class GMDMeshIndices:
    triangle_list: array.ArrayType
    triangle_strips_noreset: array.ArrayType
    triangle_strips_reset: array.ArrayType

    @classmethod
    def from_triangles(cls, triangles: Iterable[Tuple[int, int, int]]) -> 'GMDMeshIndices':
        triangle_indices = array.array("H")
        triangle_strip_noreset = array.array("H")
        triangle_strip_reset = array.array("H")

        for t0, t1, t2 in triangles:
            triangle_indices.append(t0)
            triangle_indices.append(t1)
            triangle_indices.append(t2)

            # If we can continue the strip, do so
            if not triangle_strip_noreset:
                # Starting the strip
                triangle_strip_noreset.append(t0)
                triangle_strip_noreset.append(t1)
                triangle_strip_noreset.append(t2)
            elif (triangle_strip_noreset[-2] == t0 and
                  triangle_strip_noreset[-1] == t1):
                # Continue the strip
                triangle_strip_noreset.append(t2)
            else:
                # End previous strip, start new strip
                # Two extra verts to create a degenerate triangle, signalling the end of the strip
                triangle_strip_noreset.append(triangle_strip_noreset[-1])
                triangle_strip_noreset.append(t0)
                # Add the triangle as normal
                triangle_strip_noreset.append(t0)
                triangle_strip_noreset.append(t1)
                triangle_strip_noreset.append(t2)

            # If we can continue the strip, do so
            if not triangle_strip_reset:
                # Starting the strip
                triangle_strip_reset.append(t0)
                triangle_strip_reset.append(t1)
                triangle_strip_reset.append(t2)
            elif (triangle_strip_reset[-2] == t0 and
                  triangle_strip_reset[-1] == t1):
                # Continue the strip
                triangle_strip_reset.append(t2)
            else:
                # End previous strip, start new strip
                # Reset index signalling the end of the strip
                triangle_strip_reset.append(0xFFFF)
                # Add the triangle as normal
                triangle_strip_reset.append(t0)
                triangle_strip_reset.append(t1)
                triangle_strip_reset.append(t2)

        return GMDMeshIndices(
            triangle_indices,
            triangle_strip_noreset,
            triangle_strip_reset
        )

    @classmethod
    def from_all_indices(cls, triangle_indices: array.ArrayType,
                         triangle_strip_noreset: Optional[array.ArrayType],
                         triangle_strip_reset: Optional[array.ArrayType]):
        if triangle_strip_noreset is None or triangle_strip_reset is None:
            return GMDMeshIndices.from_triangles(iterate_three(triangle_indices))
        return GMDMeshIndices(
            triangle_indices,
            triangle_strip_noreset,
            triangle_strip_reset
        )

    def __init__(self,
                 triangle_indices: array.ArrayType,
                 triangle_strip_noreset: array.ArrayType,
                 triangle_strip_reset: array.ArrayType
                 ):
        self.triangle_list = triangle_indices
        self.triangle_strips_noreset = triangle_strip_noreset
        self.triangle_strips_reset = triangle_strip_reset


@dataclass(repr=False, eq=False)
class GMDMesh:
    empty: bool

    vertices_data: GMDVertexBuffer

    triangles: GMDMeshIndices

    attribute_set: GMDAttributeSet

    def __post_init__(self):
        if not self.empty and len(self.vertices_data) < 3:
            raise TypeError(f"GMDMesh {self} has <3 vertices, at least 3 are required for a visible mesh")


@dataclass(repr=False, eq=False)
class GMDSkinnedMesh(GMDMesh):
    vertices_data: GMDSkinnedVertexBuffer
    relevant_bones: List[GMDBone]

    def __post_init__(self):
        super().__post_init__()
        referenced_bone_indices = set(np.unique(
            np.where(self.vertices_data.weight_data > 0, self.vertices_data.bone_data, -1)).flatten())
        referenced_bone_indices.discard(-1)
        if not self.empty and (not referenced_bone_indices or not self.relevant_bones):
            raise TypeError(
                f"Mesh is skinned but references no bones. "
                f"referenced_indices: {referenced_bone_indices}, relevant_bones: {self.relevant_bones}")
        if referenced_bone_indices and max(referenced_bone_indices) >= len(self.relevant_bones):
            raise Exception(
                f"Mesh uses {len(self.relevant_bones)} bones "
                f"but references {referenced_bone_indices} in {len(self.vertices_data)} verts")
