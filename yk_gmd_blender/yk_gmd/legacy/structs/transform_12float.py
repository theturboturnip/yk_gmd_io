from ctypes import c_float

from ._base.base_structure import BaseBigEndianStructure


class Transform12Float(BaseBigEndianStructure):
    _fields_ = [
        ("bbox_midpoint_maybe", c_float * 3),
        ("bbox_extents_maybe", c_float * 3),
        ("floats", c_float * 2),
        ("quaternion_maybe", c_float * 4),
    ]