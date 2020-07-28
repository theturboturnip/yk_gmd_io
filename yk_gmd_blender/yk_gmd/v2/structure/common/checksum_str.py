from dataclasses import dataclass

from yk_gmd_blender.structurelib.base import StructureUnpacker, FixedSizeASCIIUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint16


@dataclass(frozen=True)
class ChecksumStrStruct:
    checksum: int
    text: str

    @staticmethod
    def make_from_str(text: str):
        return ChecksumStrStruct(sum(text.encode("ascii")), text)


ChecksumStrStruct_Unpack = StructureUnpacker(
    ChecksumStrStruct,
    fields=[
        ("checksum", c_uint16),
        ("text", FixedSizeASCIIUnpacker(30))
    ]
)