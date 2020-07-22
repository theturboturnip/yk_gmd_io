from ctypes import *

from yk_gmd_blender.yk_gmd.structs.transform_12float import Transform12Float
from ._base.base_structure import BaseBigEndianStructure


class PartStruct(BaseBigEndianStructure):
    _fields_ = [
        ("id", c_uint32),
        ("bone_id_1", c_uint32), # Same as bone ID for relevant part
        ("bone_id_2", c_uint32), # Same as bone_id_1
        ("unk3", c_uint32), # incremental in 8?

        ("bbox_maybe", Transform12Float),
    ]