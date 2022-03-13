"""


bpy_extras submodule (bpy_extras.object_utils)
**********************************************

:func:`add_object_align_init`

:func:`object_data_add`

:func:`object_add_grid_scale`

:func:`object_add_grid_scale_apply_operator`

:func:`world_to_camera_view`

:class:`AddObjectHelper`

"""

import typing

import mathutils

import bpy

def add_object_align_init(context: bpy.types.Context, operator: bpy.types.Operator) -> mathutils.Matrix:

  """

  Return a matrix using the operator settings and view context.

  """

  ...

def object_data_add(context: bpy.types.Context, obdata: typing.Any, operator: bpy.types.Operator = None, name: str = None) -> bpy.types.Object:

  """

  Add an object using the view context and preference to initialize the
location, rotation and layer.

  """

  ...

def object_add_grid_scale(context: typing.Any) -> None:

  """

  Return scale which should be applied on object
data to align it to grid scale

  """

  ...

def object_add_grid_scale_apply_operator(operator: typing.Any, context: typing.Any) -> None:

  """

  Scale an operators distance values by the grid size.

  """

  ...

def world_to_camera_view(scene: bpy.types.Scene, obj: bpy.types.Object, coord: mathutils.Vector) -> mathutils.Vector:

  """

  Returns the camera space coords for a 3d point.
(also known as: normalized device coordinates - NDC).

  Where (0, 0) is the bottom left and (1, 1)
is the top right of the camera frame.
values outside 0-1 are also supported.
A negative 'z' value means the point is behind the camera.

  Takes shift-x/y, lens angle and sensor size into account
as well as perspective/ortho projections.

  """

  ...

class AddObjectHelper:

  def align_update_callback(self, _context: typing.Any) -> None:

    ...
