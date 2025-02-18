from dataclasses import dataclass
from typing import Generic, TypeVar, List

from ....structurelib.base import BaseUnpacker, FixedSizeArrayUnpacker, StructureUnpacker
from .sized_pointer import SizedPointerStruct, SizedPointerStruct_Unpack

T = TypeVar('T')


@dataclass
class ArrayPointerStruct(Generic[T]):
    sized_ptr: SizedPointerStruct

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


ArrayPointerStruct_Unpack = StructureUnpacker(
    ArrayPointerStruct,
    fields=[
        ("sized_ptr", SizedPointerStruct_Unpack)
    ]
)
