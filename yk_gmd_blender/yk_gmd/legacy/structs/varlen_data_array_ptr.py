from ctypes import c_uint32
from typing import List, Type

from ._base.base_structure import BaseBigEndianStructure


class VarLenDataArrayPtrStruct(BaseBigEndianStructure):
    _fields_ = [
        ("ptr", c_uint32),
        ("len", c_uint32),
    ]

    @classmethod
    def from_data(cls: Type['VarLenDataArrayPtrStruct'], ptr: int, len: int) -> 'VarLenDataArrayPtrStruct':
        array_ptr = cls()
        array_ptr.ptr = ptr
        array_ptr.len = len
        return array_ptr

    def extract_strings(self, data:bytes) -> List[bytes]:
        i = 0
        items = []
        while i < self.len:
            next_data_len = data[self.ptr+i]
            next_i = i+1+next_data_len
            items.append(bytes(data[self.ptr+i+1:self.ptr+next_i]))#[int(x) for x in ]
            i = next_i
        return items