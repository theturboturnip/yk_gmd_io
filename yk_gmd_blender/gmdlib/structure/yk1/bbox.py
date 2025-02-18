from dataclasses import dataclass

from mathutils import Vector, Quaternion
from ...abstract.nodes.gmd_object import GMDBoundingBox
from ..common.vector import Vec3Unpacker, QuatUnpacker
from ....structurelib.base import StructureUnpacker
from ....structurelib.primitives import c_float32


@dataclass
class BoundsDataStruct_YK1:
    """
    This class represents a bounding sphere and bounding box.
    Both the sphere and box are centered on the same point.
    The sphere defines a radius, and the box defines extents (equiv. to size/2) along with a rotation
    """

    center: Vector

    sphere_radius: float

    box_extents: Vector
    box_rotation: Quaternion

    padding: float = 0.0

    def abstractify(self) -> GMDBoundingBox:
        ex = self.box_extents.xyz
        corners = (
            (ex.x, ex.y, ex.z),
            (ex.x, ex.y, -ex.z),
            (ex.x, -ex.y, ex.z),
            (ex.x, -ex.y, -ex.z),

            (-ex.x, ex.y, ex.z),
            (-ex.x, ex.y, -ex.z),
            (-ex.x, -ex.y, ex.z),
            (-ex.x, -ex.y, -ex.z),
        )
        rotated_corners = tuple(
            self.box_rotation @ Vector(c)
            for c in corners
        )
        max_abs_x, max_abs_y, max_abs_z = -1, -1, -1
        for rc in rotated_corners:
            max_abs_x = max(max_abs_x, abs(rc.x))
            max_abs_y = max(max_abs_y, abs(rc.y))
            max_abs_z = max(max_abs_z, abs(rc.z))

        return GMDBoundingBox(
            center=self.center,
            sphere_radius=self.sphere_radius,
            aabb_extents=Vector((max_abs_x, max_abs_y, max_abs_z))
        )


BoundsData_YK1_Unpack = StructureUnpacker(
    BoundsDataStruct_YK1,
    fields=[
        ("center", Vec3Unpacker),
        ("sphere_radius", c_float32),

        ("box_extents", Vec3Unpacker),
        ("padding", c_float32),
        ("box_rotation", QuatUnpacker),
    ]
)
