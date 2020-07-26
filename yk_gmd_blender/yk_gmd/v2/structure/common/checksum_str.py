from dataclasses import dataclass

from yk_gmd_blender.structurelib.base import StructureUnpacker, FixedSizeASCIIUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint16


@dataclass(frozen=True)
class ChecksumStr:
    checksum: int
    text: str

    @staticmethod
    def make_from_str(text: str):
        return ChecksumStr(sum(text.encode("ascii")), text)


ChecksumStr_Unpack = StructureUnpacker(
    ChecksumStr,
    fields=[
        ("checksum", c_uint16),
        ("text", FixedSizeASCIIUnpacker(30))
    ]
)