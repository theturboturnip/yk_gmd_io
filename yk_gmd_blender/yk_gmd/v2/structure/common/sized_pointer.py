from dataclasses import dataclass

from yk_gmd_blender.structurelib.base import StructureUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint32


@dataclass
class SizedPointer:
    ptr: int
    size: int

    def extract_bytes(self, data: bytes):
        return data[self.ptr:self.ptr+self.size]

    def __repr__(self):
        return f"{self.__class__.__name__}(ptr=0x{self.ptr:x}, size={self.size})"

SizedPointerUnpack = StructureUnpacker(
    SizedPointer,
    fields=[
        ("ptr", c_uint32),
        ("size", c_uint32),
    ]
)