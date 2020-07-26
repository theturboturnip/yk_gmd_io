from ctypes import *
from typing import Type, TypeVar, List, Dict

from ._base.base_structure import BaseBigEndianStructure


T = TypeVar('T')


# TODO: This should really be dependent on the endianness of the header
class ArrayPtrStruct(BaseBigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("ptr", c_uint32),
        ("cnt", c_uint32)
    ]
    elem_type = Type#[T]

    #def __init__(self, elem_type: Optional[Type] = None):
    #    super().__init__()
    #    if not elem_type:
    #        self.elem_type = c_uint8
    #    else:
    #        self.elem_type = elem_type

    #@staticmethod
    #def of(elem_type: Type) -> 'ArrayPtrStruct':
    #    return ArrayPtrStruct(elem_type)

    @classmethod
    def from_data(cls: Type['ArrayPtrStruct'], ptr: int, cnt: int) -> 'ArrayPtrStruct':
        array_ptr = cls()
        array_ptr.ptr = ptr
        array_ptr.cnt = cnt
        return array_ptr

    def extract(self, data: bytes) -> List:
        #if self.elem_type in [c_byte, c_uint8]:
        #    return extract_array_bytes(data, self)
        #else:
        #    return extract_array_of(data, self, self.elem_type)
        elements = []
        offset = self.ptr
        for i in range(self.cnt):
            elements.append(self.elem_type.from_buffer_copy(data, offset))
            offset += sizeof(self.elem_type)
        return elements

    def __str__(self):
        if self.elem_type:
            return f"<{self.elem_type.__name__}[{self.cnt}] @ 0x{self.ptr:x}>"
        return f"<???[{self.cnt}] @ 0x{self.ptr:x}>"

    #def __repr__(self):
        #return f"<ArrayPointer[{self.elem_type.__name__}]:0x{self.ptr:x} cnt:{self.cnt}>"


array_pointer_types: Dict[Type, Type[ArrayPtrStruct]] = {}
def array_pointer_of(elem_type: Type) -> Type[ArrayPtrStruct]:
#    return ArrayPtrStruct[T](elem_type)
    if elem_type not in array_pointer_types:
        array_type = type(
            f"ArrayPointer_{elem_type.__qualname__}",
            (ArrayPtrStruct,),
            {
                "elem_type": elem_type
            }
        )
        array_pointer_types[elem_type] = array_type
    return array_pointer_types[elem_type]

#def extract_array_of(data: bytes, array: ArrayPtrStruct, type: Type[Structure]):
#    elements = []
#    offset = array.ptr
#    for i in range(array.cnt):
#        elements.append(type.from_buffer_copy(data, offset))
#        offset += sizeof(type)
#    return elements


#def extract_array_bytes(data: bytes, array: ArrayPtrStruct):
#    return data[array.ptr:array.ptr + array.cnt]