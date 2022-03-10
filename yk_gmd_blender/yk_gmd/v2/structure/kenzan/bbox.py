from dataclasses import dataclass

from mathutils import Vector

from yk_gmd_blender.structurelib.base import StructureUnpacker
from yk_gmd_blender.structurelib.primitives import c_float32
from yk_gmd_blender.yk_gmd.v2.structure.common.vector import Vec3Unpacker


@dataclass
class BoundsDataStruct_Kenzan:
    sphere_pos: Vector
    sphere_radius: float

    aabox_bottomleft: Vector
    aabox_topright: Vector

    padding: float = 0.0
    padding2: float = 0.0


BoundsDataStruct_Kenzan_Unpack = StructureUnpacker(
    BoundsDataStruct_Kenzan,
    fields=[
        ("sphere_pos", Vec3Unpacker),
        ("sphere_radius", c_float32),
        ("padding", c_float32),

        ("aabox_bottomleft", Vec3Unpacker),
        ("aabox_topright", Vec3Unpacker),
        ("padding2", c_float32),
    ]
)