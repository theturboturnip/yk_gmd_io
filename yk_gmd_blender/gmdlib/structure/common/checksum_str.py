from dataclasses import dataclass

from ....structurelib.base import StructureUnpacker, FixedSizeASCIIUnpacker
from ....structurelib.primitives import c_uint16


@dataclass(frozen=True)
class ChecksumStrStruct:
    checksum: int
    text: str

    @staticmethod
    def make_from_str(text: str):
        return ChecksumStrStruct(sum(text.encode("shift_jis")), text)


ChecksumStrStruct_Unpack = StructureUnpacker(
    ChecksumStrStruct,
    fields=[
        ("checksum", c_uint16),
        ("text", FixedSizeASCIIUnpacker(30, encoding="shift_jis"))
    ]
)
