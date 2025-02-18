from dataclasses import dataclass
from typing import Tuple

from ....structurelib.base import *
from ....structurelib.primitives import *
from .checksum_str import ChecksumStrStruct, ChecksumStrStruct_Unpack
from ..endianness import check_are_vertices_big_endian, check_is_file_big_endian
from ..version import get_combined_version_properties, VersionProperties


def extract_base_header(data: bytes) -> Tuple['GMDHeaderStruct', bool]:
    big_endian = True
    base_header, _ = GMDHeaderStruct_Unpack.unpack(big_endian, data=data, offset=0)
    if base_header.file_endian_check == 0:
        big_endian = False
    elif base_header.file_endian_check == 1:
        big_endian = True
    else:
        raise Exception(f"Unknown base_header file endian check {base_header.file_endian_check}")

    base_header, _ = GMDHeaderStruct_Unpack.unpack(big_endian, data=data, offset=0)

    return base_header, big_endian


@dataclass(frozen=True)
class GMDHeaderStruct:
    magic: str
    vertex_endian_check: int
    file_endian_check: int

    version_combined: int
    file_size: int

    name: ChecksumStrStruct

    padding: int

    def file_is_big_endian(self):
        return check_is_file_big_endian(self.file_endian_check)

    def vertices_are_big_endian(self):
        return check_are_vertices_big_endian(self.vertex_endian_check)

    @property
    def version_major(self) -> int:
        return (self.version_combined >> 16) & 0xFFFF

    @property
    def version_minor(self) -> int:
        return (self.version_combined >> 0) & 0xFFFF

    def get_version_properties(self) -> VersionProperties:
        return get_combined_version_properties(self.version_combined)

    def version_str(self) -> str:
        return f"{self.version_major}.{self.version_minor}"


GMDHeaderStruct_Unpack = StructureUnpacker(
    GMDHeaderStruct,
    fields=[
        ("magic", FixedSizeASCIIUnpacker(4)),
        ("vertex_endian_check", c_uint8),
        ("file_endian_check", c_uint8),
        ("padding", c_uint16),
        ("version_combined", c_uint32),
        ("file_size", c_uint32),

        ("name", ChecksumStrStruct_Unpack),
    ]
)
