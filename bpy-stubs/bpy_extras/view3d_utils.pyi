"""


bpy_extras submodule (bpy_extras.view3d_utils)
**********************************************

:func:`region_2d_to_vector_3d`

:func:`region_2d_to_origin_3d`

:func:`region_2d_to_location_3d`

:func:`location_3d_to_region_2d`

"""

import typing

import mathutils

import bpy

def region_2d_to_vector_3d(region: bpy.types.Region, rv3d: bpy.types.RegionView3D, coord: mathutils.Vector) -> mathutils.Vector:

  """

  Return a direction vector from the viewport at the specific 2d region
coordinate.

  """

  ...

def region_2d_to_origin_3d(region: bpy.types.Region, rv3d: bpy.types.RegionView3D, coord: mathutils.Vector, *args, clamp: float = None) -> mathutils.Vector:

  """

  Return the 3d view origin from the region relative 2d coords.

  Note: Orthographic views have a less obvious origin,
the far clip is used to define the viewport near/far extents.
Since far clip can be a very large value,
the result may give with numeric precision issues.To avoid this problem, you can optionally clamp the far clip to a
smaller value based on the data you're operating on.

  """

  ...

def region_2d_to_location_3d(region: bpy.types.Region, rv3d: bpy.types.RegionView3D, coord: mathutils.Vector, depth_location: mathutils.Vector) -> mathutils.Vector:

  """

  Return a 3d location from the region relative 2d coords, aligned with
*depth_location*.

  """

  ...

def location_3d_to_region_2d(region: bpy.types.Region, rv3d: bpy.types.RegionView3D, coord: mathutils.Vector, *args, default: typing.Any = None) -> mathutils.Vector:

  """

  Return the *region* relative 2d location of a 3d position.

  """

  ...
