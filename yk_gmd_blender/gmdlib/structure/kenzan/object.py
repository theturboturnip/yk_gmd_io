from dataclasses import dataclass

from ....structurelib.base import StructureUnpacker
from ....structurelib.primitives import c_uint32
from .bbox import BoundsDataStruct_Kenzan, BoundsDataStruct_Kenzan_Unpack


@dataclass
class ObjectStruct_Kenzan:
    index: int
    node_index_1: int
    node_index_2: int
    drawlist_rel_ptr: int

    bbox: BoundsDataStruct_Kenzan


ObjectStruct_Kenzan_Unpack = StructureUnpacker(
    ObjectStruct_Kenzan,
    fields=[
        ("index", c_uint32),
        ("node_index_1", c_uint32),
        ("node_index_2", c_uint32),
        ("drawlist_rel_ptr", c_uint32),

        ("bbox", BoundsDataStruct_Kenzan_Unpack)
    ]
)
