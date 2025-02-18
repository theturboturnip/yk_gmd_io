from dataclasses import dataclass
from typing import List, Optional

from .base import StructureUnpacker, FixedSizeArrayUnpacker
from .primitives import *

short_arr_6 = FixedSizeArrayUnpacker(c_uint16, 6)

bs = bytes([0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5])
print(short_arr_6.unpack(big_endian=True, data=bs, offset=0))
print(short_arr_6.unpack(big_endian=False, data=bs, offset=0))


@dataclass(frozen=True)
class TestStructure:
    top_int: int
    bottom_float: float
    array: List[int]


TestStructureUnpacker = StructureUnpacker(
    TestStructure,
    fields=[
        ("top_int", c_uint32),
        ("bottom_float", c_float32),
        ("array", short_arr_6)
    ]
)

structure_bytes = bytes([0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5])

struct, _ = TestStructureUnpacker.unpack(big_endian=True, data=structure_bytes, offset=0)
struct_little, _ = TestStructureUnpacker.unpack(big_endian=False, data=structure_bytes, offset=0)
print(struct)
print(struct_little)

repacked_be = bytearray()
TestStructureUnpacker.pack(big_endian=True, value=struct, append_to=repacked_be)
repacked_le = bytearray()
TestStructureUnpacker.pack(big_endian=False, value=struct_little, append_to=repacked_le)
print(structure_bytes)
print(bytes(repacked_be))
print(bytes(repacked_le))


@dataclass(frozen=True)
class TestNestedStructure:
    nested: TestStructure
    extra_bytes: List[int]
    unpacker: Optional[int]


TestNestedStructureUnpacker = StructureUnpacker(
    TestNestedStructure,
    fields=[
        ("nested", TestStructureUnpacker),
        ("extra_bytes", FixedSizeArrayUnpacker(c_uint8, 16)),
    ]
)

test_nested_data = structure_bytes + bytes(range(16))
struct, _ = TestNestedStructureUnpacker.unpack(big_endian=True, data=test_nested_data, offset=0)
struct_little, _ = TestNestedStructureUnpacker.unpack(big_endian=False, data=test_nested_data, offset=0)
print(struct)
print(struct_little)

repacked_be = bytearray()
TestNestedStructureUnpacker.pack(big_endian=True, value=struct, append_to=repacked_be)
repacked_le = bytearray()
TestNestedStructureUnpacker.pack(big_endian=False, value=struct_little, append_to=repacked_le)
print(test_nested_data)
print(bytes(repacked_be))
print(bytes(repacked_le))
