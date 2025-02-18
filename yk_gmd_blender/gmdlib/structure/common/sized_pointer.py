from dataclasses import dataclass

from ....structurelib.base import StructureUnpacker
from ....structurelib.primitives import c_uint32


@dataclass
class SizedPointerStruct:
    ptr: int
    size: int

    def extract_bytes(self, data: bytes):
        return data[self.ptr:self.ptr + self.size]

    def __repr__(self):
        return f"{self.__class__.__name__}(ptr=0x{self.ptr:x}, size={self.size})"


SizedPointerStruct_Unpack = StructureUnpacker(
    SizedPointerStruct,
    fields=[
        ("ptr", c_uint32),
        ("size", c_uint32),
    ]
)
