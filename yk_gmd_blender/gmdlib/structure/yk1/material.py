from dataclasses import dataclass
from typing import List

from ....structurelib.base import StructureUnpacker, FixedSizeArrayUnpacker
from ....structurelib.primitives import *
from ..common.material_base import MaterialBaseStruct


@dataclass(frozen=False)
class MaterialStruct_YK1(MaterialBaseStruct):
    diffuse: List[int]
    opacity: int
    specular: List[int]
    power: float

    unk1: List[int]
    unk2: List[int]

    padding: int = 0


# These are best guesses, we don't have a textdump of this like we do for Kenzan
MaterialStruct_YK1_Unpack = StructureUnpacker(
    MaterialStruct_YK1,
    fields=[
        ("power", c_float16),
        ("unk1", FixedSizeArrayUnpacker(c_uint8, 2)),

        ("specular", FixedSizeArrayUnpacker(c_uint8, 3)),
        ("padding", c_uint8),

        ("diffuse", FixedSizeArrayUnpacker(c_uint8, 3)),
        ("opacity", c_uint8),

        ("unk2", FixedSizeArrayUnpacker(c_uint8, 4))
    ]
)
