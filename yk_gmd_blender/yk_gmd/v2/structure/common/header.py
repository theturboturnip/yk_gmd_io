import abc
from dataclasses import dataclass
from typing import Tuple

from yk_gmd_blender.structurelib.base import *
from yk_gmd_blender.structurelib.primitives import *
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStr, ChecksumStr_Unpack


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

    version: int
    file_size: int

    name: ChecksumStr

    padding: int

GMDHeaderUnpack = StructureUnpacker(
    GMDHeader,
    fields=[
        ("magic", FixedSizeASCIIUnpacker(4)),
        ("vertex_endian_check", c_uint8),
        ("file_endian_check", c_uint8),
        ("padding", c_uint16),
        ("version", c_uint32),
        ("file_size", c_uint32),

        ("name", ChecksumStr_Unpack),
    ]
)