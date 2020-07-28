from dataclasses import dataclass
from enum import IntEnum
from typing import Dict

from .vertices import GMDVertexBufferLayout


class GMDMaterialTextureIndex(IntEnum):
    Diffuse = 0
    UNK_Reflection = 1
    Multi = 2
    UNK_Empty = 3
    UNK_RS = 4
    Normal = 5
    UNK_RT = 6
    UNK_RD = 7


@dataclass(repr=False, frozen=True)
class GMDMaterial:
    id: int
    shader_name: str
    texture_names: Dict[GMDMaterialTextureIndex, str]
    vertex_buffer_layout: GMDVertexBufferLayout

