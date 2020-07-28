from dataclasses import dataclass

from yk_gmd_blender.structurelib.base import StructureUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint32
from yk_gmd_blender.yk_gmd.v2.structure.yk1.bbox import BoundsDataStruct_YK1, BoundsData_YK1_Unpack


@dataclass
class ObjectStruct_YK1:
    index: int
    node_index_1: int
    node_index_2: int
    drawlist_rel_ptr: int

    # TODO: 010 template says this is a matrix
    bbox: BoundsDataStruct_YK1


ObjectStruct_YK1_Unpack = StructureUnpacker(
    ObjectStruct_YK1,
    fields=[
        ("index", c_uint32),
        ("node_index_1", c_uint32),
        ("node_index_2", c_uint32),
        ("drawlist_rel_ptr", c_uint32),

        ("bbox", BoundsData_YK1_Unpack)
    ]
)