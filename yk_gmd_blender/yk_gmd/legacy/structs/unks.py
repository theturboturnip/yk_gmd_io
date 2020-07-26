from ctypes import *
from ._base.base_structure import BaseBigEndianStructure


# This is likely some set of material properties.
class Unk12(BaseBigEndianStructure):
    _fields_ = [
        #("data_hidden", c_uint8 * 128)
        ("data_hidden", c_float * 32)
    ]

    @property
    def data(self):
        return self.data_hidden[:]


class Unk14(BaseBigEndianStructure):
    _fields_ = [
        ("data_hidden", c_uint32 * 32)
    ]

    @property
    def data(self):
        return self.data_hidden[:]


class Unk5(BaseBigEndianStructure):
    _fields_ = [
        ("a", c_uint8),
        ("b", c_uint8),
        ("c", c_uint8), # Usually 0x3C or 0x40. .f changes when == 0x40
        ("zero1", c_uint8),

        ("color_maybe", c_uint32), # Seen to be 0x80_80_80_00, 0x33_33_33_00 0xBF_BF_BF_00 etc.
        # bottom byte always 0

        ("all_ones", c_uint32), # always 0xFFFFFFFF

        ("e", c_uint16), # always 0x80000
        ("f", c_uint16), # 0x005C if c == 0x3C, or 0x0006 if c == 0x40
    ]


class Unk13(BaseBigEndianStructure):
    _fields_ = [
        ("data", c_uint16)
    ]