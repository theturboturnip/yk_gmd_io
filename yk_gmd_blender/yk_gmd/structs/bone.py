from ctypes import *
from ._base.base_structure import BaseBigEndianStructure


class BoneStruct(BaseBigEndianStructure):
    _fields_ = [
        ("ints_internal", c_int32 * 8),
        #("id", c_uint32),
        #("unk1", c_int32),
        #("unk2", c_int32),
        #("part_id_maybe", c_int32),
        #("name_string_maybe", c_uint32),
        #("unk3", c_uint32),
        #("unk4", c_uint32),
        #("unk5", c_uint32),

        ("pos", c_float * 4),
        ("rot", c_float * 4), # Seem to be vectors of 0,0,0,1 or very small floats for 0s, but also seens as 0, 0.25, 0.25, 1. When treated as a quaternion and converted to eulerangles, gets (0,0,0) or (0, 30, 30)
        # note - was treated as [x,y,z,w], not [w,x,y,z] for quaternion function in main.py
        ("scl", c_float * 4), # Always 1,1,1,0 - should be scaling

        ("world_pos", c_float * 4), # Usually close to p, most likely a position. although, unk1[3] == 1 in all cases despite p[3] == 0 in all
        # Equal to (-translation) column of associated matrix

        # unk2 can be 0,0,0,0 in many cases
        ("world_rot_maybe", c_float * 4), # X and Y components in [-1,1], Z in [-0.65,0.91] (so probably [-1,1]), W in [0, 0.45] Quaternion?

        ("unk3", c_float * 4), # Always 0,0,0,0
    ]

    @property
    def ints(self):
        return list(self.ints_internal)

    @property
    def id(self) -> int:
        return self.ints[0]

    @property
    def part_id(self) -> int:
        return self.ints[3]

    @property
    def parent_of(self) -> int:
        return self.ints[1]

    @property
    def sibling_of(self) -> int:
        return self.ints[2]

    @property
    def name_string(self) -> int:
        return self.ints[6]

    @property
    def matrix_id_maybe(self) -> int:
        return self.ints[4]