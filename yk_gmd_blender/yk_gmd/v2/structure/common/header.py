import abc
from dataclasses import dataclass
from typing import Tuple

from yk_gmd_blender.structurelib.base import *
from yk_gmd_blender.structurelib.primitives import *
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStr, ChecksumStr_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.version import GMDVersion, get_version_properties, \
    get_combined_version_properties, FileProperties


def extract_base_header(data: bytes) -> Tuple['GMDHeader', bool]:
    big_endian = True
    base_header, _ = GMDHeaderUnpack.unpack(big_endian, data=data, offset=0)
    if base_header.file_endian_check == 0:
        big_endian = False
    elif base_header.file_endian_check == 1:
        big_endian = True
    else:
        raise Exception(f"Unknown base_header file endian check {base_header.file_endian_check}")

    base_header, _ = GMDHeaderUnpack.unpack(big_endian, data=data, offset=0)

    return base_header, big_endian

@dataclass(frozen=True)
class GMDHeader:
    magic: str
    vertex_endian_check: int
    file_endian_check: int

    version_combined: int
    file_size: int

    name: ChecksumStr

    padding: int

    @property
    def version_major(self) -> int:
        return (self.version_combined >> 16) & 0xFF_FF

    @property
    def version_minor(self) -> int:
        return (self.version_combined >> 0) & 0xFF_FF

    def get_version_properties(self) -> FileProperties:
        return get_combined_version_properties(self.version_combined)

    def version_str(self) -> str:
        return f"{self.version_major}.{self.version_minor}"

GMDHeaderUnpack = StructureUnpacker(
    GMDHeader,
    fields=[
        ("magic", FixedSizeASCIIUnpacker(4)),
        ("vertex_endian_check", c_uint8),
        ("file_endian_check", c_uint8),
        ("padding", c_uint16),
        ("version_combined", c_uint32),
        ("file_size", c_uint32),

        ("name", ChecksumStr_Unpack),
    ]
)