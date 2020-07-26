from dataclasses import dataclass

from yk_gmd_blender.structurelib.base import StructureUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint32
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.bbox import BoundsData_Kenzan, BoundsData_Kenzan_Unpack


@dataclass
class Object_Kenzan:
    index: int
    node_index_1: int
    node_index_2: int
    drawlist_rel_ptr: int

    bbox: BoundsData_Kenzan


Object_Kenzan_Unpack = StructureUnpacker(
    Object_Kenzan,
    fields=[
        ("index", c_uint32),
        ("node_index_1", c_uint32),
        ("node_index_2", c_uint32),
        ("drawlist_rel_ptr", c_uint32),

        ("bbox", BoundsData_Kenzan_Unpack)
    ]
)