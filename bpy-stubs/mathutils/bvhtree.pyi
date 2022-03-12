"""


BVHTree Utilities (mathutils.bvhtree)
*************************************

BVH tree structures for proximity searches and ray casts on geometry.

:class:`BVHTree`

"""

import typing

class BVHTree:

  @classmethod

  def FromBMesh(cls, bmesh: BMesh, epsilon: float = 0.0) -> None:

    """

    BVH tree based on :class:`BMesh` data.

    """

    ...

  @classmethod

  def FromObject(cls, object: Object, depsgraph: Depsgraph, deform: bool = True, render: typing.Any = False, cage: bool = False, epsilon: float = 0.0) -> None:

    """

    BVH tree based on :class:`Object` data.

    """

    ...

  @classmethod

  def FromPolygons(cls, vertices: float, polygons: typing.Sequence[typing.Any], all_triangles: bool = False, epsilon: float = 0.0) -> None:

    """

    BVH tree constructed geometry passed in as arguments.

    """

    ...

  def find_nearest(self, origin: typing.Any, distance: float = 1.84467e+19) -> tuple:

    """

    Find the nearest element (typically face index) to a point.

    """

    ...

  def find_nearest_range(self, origin: typing.Any, distance: float = 1.84467e+19) -> list:

    """

    Find the nearest elements (typically face index) to a point in the distance range.

    """

    ...

  def overlap(self, other_tree: BVHTree) -> list:

    """

    Find overlapping indices between 2 trees.

    """

    ...

  def ray_cast(self, origin: Vector, direction: Vector, distance: float = sys.float_info.max) -> tuple:

    """

    Cast a ray onto the mesh.

    """

    ...
