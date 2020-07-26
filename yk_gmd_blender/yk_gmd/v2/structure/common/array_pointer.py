from dataclasses import dataclass
from typing import Generic, TypeVar, List

from yk_gmd_blender.structurelib.base import BaseUnpacker, FixedSizeArrayUnpacker, StructureUnpacker
from yk_gmd_blender.yk_gmd.v2.structure.common.sized_pointer import SizedPointer, SizedPointerUnpack

T = TypeVar('T')

@dataclass
class ArrayPointer(Generic[T]):
    sized_ptr: SizedPointer

    def extract(self, unpack: BaseUnpacker[T], big_endian: bool, data: bytes) -> List[T]:
        return FixedSizeArrayUnpacker(unpack, self.sized_ptr.size).unpack(big_endian, data, self.sized_ptr.ptr)[0]

    @property
    def ptr(self):
        return self.sized_ptr.ptr
    @property
    def count(self):
        return self.sized_ptr.size

    def __repr__(self):
        return f"{self.__class__.__name__}(ptr=0x{self.ptr:x}, cnt={self.count})"

ArrayPointerUnpack = StructureUnpacker(
    ArrayPointer,
    fields=[
        ("sized_ptr", SizedPointerUnpack)
    ]
)