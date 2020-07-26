__all__ = [
    "c_uint8",
    "c_uint16",
    "c_uint32",

    "c_int8",
    "c_int16",
    "c_int32",

    "c_float16",
    "c_float32",

    "c_unorm8"
]

from typing import *

from yk_gmd_blender.structurelib.base import BoundedPrimitiveUnpacker, BasePrimitive

# TODO: Rename these primitives to not match ctypes

c_uint8 = BoundedPrimitiveUnpacker(struct_fmt="B", python_type=int, range=(0, 255))
c_uint16 = BoundedPrimitiveUnpacker(struct_fmt="H", python_type=int, range=(0, 65_535))
c_uint32 = BoundedPrimitiveUnpacker(struct_fmt="I", python_type=int, range=(0, 4_294_967_295))
c_uint64 = BoundedPrimitiveUnpacker(struct_fmt="Q", python_type=int, range=(0, 18_446_744_073_709_551_615))

c_int8 = BoundedPrimitiveUnpacker(struct_fmt="b", python_type=int, range=(-128, 127))
c_int16 = BoundedPrimitiveUnpacker(struct_fmt="h", python_type=int, range=(-32_768, 32_767))
c_int32 = BoundedPrimitiveUnpacker(struct_fmt="i", python_type=int, range=(-2_147_483_648, 2_147_483_647))
c_int64 = BoundedPrimitiveUnpacker(struct_fmt="q", python_type=int, range=(-9_223_372_036_854_775_808, 9_223_372_036_854_775_807))

c_float16 = BasePrimitive(struct_fmt="e", python_type=float)
c_float32 = BasePrimitive(struct_fmt="f", python_type=float)


class UnormPrimitive(BoundedPrimitiveUnpacker[float]):
    base_unpack: BasePrimitive
    divisor: float

    def __init__(self, base_unpack: BasePrimitive, divisor: float):
        super().__init__(python_type=float, struct_fmt=base_unpack.struct_fmt, range=(0,1))
        self.base_unpack = base_unpack
        self.divisor = divisor

    def unpack(self, big_endian: bool, data: Union[bytes, bytearray], offset:int) -> Tuple[float, int]:
        byteval, offset = self.base_unpack.unpack(big_endian, data, offset)
        return (byteval/self.divisor), offset

    def pack(self, big_endian: bool, value: float, append_to: bytearray):
        self.base_unpack.pack(big_endian, self.base_unpack.python_type(value * self.divisor), append_to)

    def sizeof(self):
        return self.base_unpack.sizeof()

c_unorm8 = UnormPrimitive(base_unpack=c_uint8, divisor=255.0)