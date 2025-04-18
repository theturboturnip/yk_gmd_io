from dataclasses import dataclass

from .bbox import ObjectBoundsDataStruct_Y3, ObjectBoundsData_Y3_Unpack
from ....structurelib.base import StructureUnpacker
from ....structurelib.primitives import c_uint32


@dataclass
class ObjectStruct_Y3:
    index: int
    node_index_1: int
    node_index_2: int
    # TODO: whyyyy is this a rel_ptr? What is it rel_ to?
    drawlist_rel_ptr: int

    bbox: ObjectBoundsDataStruct_Y3


ObjectStruct_Y3_Unpack = StructureUnpacker(
    ObjectStruct_Y3,
    fields=[
        ("index", c_uint32),
        ("node_index_1", c_uint32),
        ("node_index_2", c_uint32),
        ("drawlist_rel_ptr", c_uint32),

        ("bbox", ObjectBoundsData_Y3_Unpack),
    ]
)
