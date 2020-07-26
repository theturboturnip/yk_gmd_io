from dataclasses import dataclass

from mathutils import Vector, Quaternion
from yk_gmd_blender.structurelib.base import StructureUnpacker
from yk_gmd_blender.structurelib.primitives import c_float32
from yk_gmd_blender.yk_gmd.v2.structure.common.vector import Vec3Unpacker, QuatUnpacker


@dataclass
class BoundsData_YK1:
    """
    This class represents a bounding sphere and bounding box.
    Both the sphere and box are centered on the same point.
    The sphere defines a radius, and the box defines extents (equiv. to size/2) along with a rotation
    """

    center: Vector

    sphere_radius: float

    box_extents: Vector
    box_rotation: Quaternion

    padding: float



BoundsData_YK1_Unpack = StructureUnpacker(
    BoundsData_YK1,
    fields=[
        ("center", Vec3Unpacker),
        ("sphere_radius", c_float32),

        ("box_extents", Vec3Unpacker),
        ("padding", c_float32),
        ("box_rotation", QuatUnpacker),
    ]
)