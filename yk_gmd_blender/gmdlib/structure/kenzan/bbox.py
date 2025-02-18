from dataclasses import dataclass

from mathutils import Vector
from ...abstract.nodes.gmd_object import GMDBoundingBox
from ..common.vector import Vec3Unpacker, Vec4Unpacker
from ....structurelib.base import StructureUnpacker
from ....structurelib.primitives import c_float32


@dataclass
class BoundsDataStruct_Kenzan:
    # The center of the sphere and the Axis Aligned Bounding Box
    center: Vector
    sphere_radius: float
    aabb_extents: Vector

    unknown: Vector  # Could be an (xyz, radius) for a slightly larger bounding sphere?

    padding: float = 0.0

    def abstractify(self) -> GMDBoundingBox:
        return GMDBoundingBox(
            center=self.center,
            sphere_radius=self.sphere_radius,
            aabb_extents=self.aabb_extents
        )


BoundsDataStruct_Kenzan_Unpack = StructureUnpacker(
    BoundsDataStruct_Kenzan,
    fields=[
        ("center", Vec3Unpacker),
        ("sphere_radius", c_float32),

        ("unknown", Vec4Unpacker),

        ("aabb_extents", Vec3Unpacker),
        ("padding", c_float32),
    ]
)
