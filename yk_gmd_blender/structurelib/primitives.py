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


class RangeConverterPrimitive(BoundedPrimitiveUnpacker[float]):
    base_unpack: BasePrimitive
    from_range: Tuple[float, float]
    to_range: Tuple[float, float]

    def __init__(self, base_unpack: BasePrimitive, from_range: Tuple[float, float], to_range: Tuple[float, float]):
        super().__init__(python_type=float, struct_fmt=base_unpack.struct_fmt, range=to_range)
        self.base_unpack = base_unpack

        self.from_range = from_range
        self.to_range = to_range

    def unpack(self, big_endian: bool, data: Union[bytes, bytearray], offset:int) -> Tuple[float, int]:
        value, offset = self.base_unpack.unpack(big_endian, data, offset)

        independent_float = (value - self.from_range[0]) / (self.from_range[1] - self.from_range[0])
        target_range_float = (independent_float * (self.to_range[1] - self.to_range[0])) + self.to_range[0]

        return target_range_float, offset

    def pack(self, big_endian: bool, value: float, append_to: bytearray):
        self.validate_value(value)

        independent_float = (value - self.to_range[0])/(self.to_range[1] - self.to_range[0])
        target_range_float = (independent_float * (self.from_range[1] - self.from_range[0])) + self.from_range[0]
        self.base_unpack.pack(big_endian, self.base_unpack.python_type(target_range_float), append_to)

    def sizeof(self):
        return self.base_unpack.sizeof()

c_unorm8 = RangeConverterPrimitive(base_unpack=c_uint8, from_range=(0,255), to_range=(0,1))