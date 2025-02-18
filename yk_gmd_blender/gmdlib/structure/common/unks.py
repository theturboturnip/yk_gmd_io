from dataclasses import dataclass
from typing import List

from ....structurelib.base import StructureUnpacker, FixedSizeArrayUnpacker
from ....structurelib.primitives import c_float32, c_uint32


@dataclass(frozen=True)
class Unk12Struct:
    data: List[float]


Unk12Struct_Unpack = StructureUnpacker(
    Unk12Struct,
    fields=[
        ("data", FixedSizeArrayUnpacker(c_float32, 32))
    ]
)


@dataclass(frozen=True)
class Unk14Struct:
    data: List[int]


Unk14Struct_Unpack = StructureUnpacker(
    Unk14Struct,
    fields=[
        ("data", FixedSizeArrayUnpacker(c_uint32, 32))
    ]
)
