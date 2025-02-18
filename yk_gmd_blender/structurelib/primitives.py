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

from .base import BoundedPrimitiveUnpacker, BasePrimitive

c_uint8 = BoundedPrimitiveUnpacker(struct_fmt="B", python_type=int, range=(0, 255))
c_uint16 = BoundedPrimitiveUnpacker(struct_fmt="H", python_type=int, range=(0, 65_535))
c_uint32 = BoundedPrimitiveUnpacker(struct_fmt="I", python_type=int, range=(0, 4_294_967_295))
c_uint64 = BoundedPrimitiveUnpacker(struct_fmt="Q", python_type=int, range=(0, 18_446_744_073_709_551_615))

c_int8 = BoundedPrimitiveUnpacker(struct_fmt="b", python_type=int, range=(-128, 127))
c_int16 = BoundedPrimitiveUnpacker(struct_fmt="h", python_type=int, range=(-32_768, 32_767))
c_int32 = BoundedPrimitiveUnpacker(struct_fmt="i", python_type=int, range=(-2_147_483_648, 2_147_483_647))
c_int64 = BoundedPrimitiveUnpacker(struct_fmt="q", python_type=int,
                                   range=(-9_223_372_036_854_775_808, 9_223_372_036_854_775_807))

c_float16 = BasePrimitive(struct_fmt="e", python_type=float)
c_float32 = BasePrimitive(struct_fmt="f", python_type=float)


class U8ConverterPrimitive(BoundedPrimitiveUnpacker[float]):
    to_range: Tuple[float, float]

    def __init__(self, to_range: Tuple[float, float]):
        super().__init__(python_type=float, struct_fmt=c_uint8.struct_fmt, range=to_range)
        self.start = to_range[0]
        self.width = to_range[1] - to_range[0]

    def unpack(self, big_endian: bool, data: Union[bytes, bytearray], offset: int) -> Tuple[float, int]:
        value, offset = c_uint8.unpack(big_endian, data, offset)

        float_0_1 = value / 255.0
        target_range_float = (float_0_1 * self.width) + self.start

        return target_range_float, offset

    def pack(self, big_endian: bool, value: float, append_to: bytearray):
        self.validate_value(value)

        independent_float = (value - self.start) / self.width
        float_0_255 = independent_float * 255
        c_uint8.pack(big_endian, int(round(float_0_255)), append_to)

    def sizeof(self):
        return c_uint8.sizeof()


c_unorm8 = U8ConverterPrimitive(to_range=(0, 1))
c_u8_Minus1_1 = U8ConverterPrimitive(to_range=(-1.0, 1.0))
