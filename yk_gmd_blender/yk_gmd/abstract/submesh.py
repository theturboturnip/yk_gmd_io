from dataclasses import dataclass
from typing import List

from .material import GMDMaterial
from .vertices import GMDVertex


@dataclass(frozen=True)
class GMDPart:
    name: str
    submeshes: List['GMDSubmesh']


@dataclass(frozen=True,repr=False)
class GMDSubmesh:
    #parent_part: GMDPart

    material: GMDMaterial # The vertex buffer layout is derived from which material is used.

    relevant_bones: List[int] # This can be at most 32 elements long

    vertices: List[GMDVertex]

    triangle_indices: List[int]
    triangle_strip_noreset_indices: List[int]
    triangle_strip_reset_indices: List[int]

    # TODO: columns 12 and 13 in the struct aren't present
