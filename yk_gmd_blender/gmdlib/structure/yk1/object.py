from dataclasses import dataclass

from ....structurelib.base import StructureUnpacker
from ....structurelib.primitives import c_uint32
from .bbox import BoundsDataStruct_YK1, BoundsData_YK1_Unpack


@dataclass
class ObjectStruct_YK1:
    index: int
    node_index_1: int
    node_index_2: int
    # TODO: whyyyy is this a rel_ptr? What is it rel_ to?
    drawlist_rel_ptr: int

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
