from dataclasses import dataclass

from mathutils import Vector
from ..common.vector import Vec3Unpacker
from ...abstract.nodes.gmd_object import GMDBoundingBox
from ....structurelib.base import StructureUnpacker
from ....structurelib.primitives import c_float32


@dataclass
class TopLevelBoundsDataStruct_Y3:
    """
    This class represents a bounding sphere and axis-aligned bounding box.
    Both the sphere and box are centered on the same point.
    The sphere defines a radius, and the box defines extents (equiv. to size/2)
    """

    center: Vector
    sphere_radius: float
    aabb_extents: Vector

    padding: float = 0.0

    @property
    def center_distance_from_origin(self):
        return self.center.length

    def abstractify(self) -> GMDBoundingBox:
        return GMDBoundingBox(
            center=self.center,
            sphere_radius=self.sphere_radius,
            aabb_extents=self.aabb_extents
        )


TopLevelBoundsData_Y3_Unpack = StructureUnpacker(
    TopLevelBoundsDataStruct_Y3,
    fields=[
        ("center", Vec3Unpacker),
        ("sphere_radius", c_float32),

        ("center", Vec3Unpacker),
        ("sphere_radius", c_float32),

        ("aabb_extents", Vec3Unpacker),
        ("padding", c_float32),
    ]
)


@dataclass
class ObjectBoundsDataStruct_Y3:
    """
    This class represents a bounding sphere and axis-aligned bounding box.
    Both the sphere and box are centered on the same point.
    The sphere defines a radius, and the box defines extents (equiv. to size/2).
    It includes a center_distance_from_origin field, the purpose of which is currently unknown.
    """

    center: Vector
    center_distance_from_origin: float
    sphere_radius: float
    aabb_extents: Vector

    padding: float = 0.0

    def abstractify(self) -> GMDBoundingBox:
        return GMDBoundingBox(
            center=self.center,
            sphere_radius=self.sphere_radius,
            aabb_extents=self.aabb_extents
        )


ObjectBoundsData_Y3_Unpack = StructureUnpacker(
    ObjectBoundsDataStruct_Y3,
    fields=[
        ("aabb_extents", Vec3Unpacker),
        ("center_distance_from_origin", c_float32),

        ("center", Vec3Unpacker),
        ("sphere_radius", c_float32),

        ("aabb_extents", Vec3Unpacker),
        ("padding", c_float32),
    ]
)
