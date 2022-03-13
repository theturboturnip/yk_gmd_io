"""


GPU State Utilities (gpu.state)
*******************************

This module provides access to the gpu state.

:func:`framebuffer_active_get`

:func:`blend_get`

:func:`blend_set`

:func:`clip_distances_set`

:func:`color_mask_set`

:func:`depth_mask_set_get`

:func:`depth_mask_set`

:func:`blend_depth_test_get`

:func:`depth_test_set`

:func:`face_culling_set`

:func:`front_facing_set`

:func:`line_width_get`

:func:`line_width_set`

:func:`point_size_set`

:func:`use_program_point_size`

:func:`viewport_get`

:func:`viewport_set`

"""

import typing

def framebuffer_active_get(enable: typing.Any) -> None:

  """

  Return the active framefuffer in context.

  """

  ...

def blend_get() -> None:

  """

  Current blending equation.

  """

  ...

def blend_set(mode: str) -> None:

  """

  Defines the fixed pipeline blending equation.

  """

  ...

def clip_distances_set(distances_enabled: int) -> None:

  """

  Sets the number of *gl_ClipDistance* planes used for clip geometry.

  """

  ...

def color_mask_set(r: typing.Any, g: typing.Any, b: typing.Any, a: typing.Any) -> None:

  """

  Enable or disable writing of frame buffer color components.

  """

  ...

def depth_mask_set_get() -> None:

  """

  Writing status in the depth component.

  """

  ...

def depth_mask_set(value: typing.Any) -> None:

  """

  Write to depth component.

  """

  ...

def blend_depth_test_get() -> None:

  """

  Current depth_test equation.

  """

  ...

def depth_test_set(mode: str) -> None:

  """

  Defines the depth_test equation.

  """

  ...

def face_culling_set(culling: typing.Any) -> None:

  """

  Specify whether none, front-facing or back-facing facets can be culled.

  """

  ...

def front_facing_set(invert: typing.Any) -> None:

  """

  Specifies the orientation of front-facing polygons.

  """

  ...

def line_width_get() -> None:

  """

  Current width of rasterized lines.

  """

  ...

def line_width_set(width: typing.Any) -> None:

  """

  Specify the width of rasterized lines.

  """

  ...

def point_size_set(size: typing.Any) -> None:

  """

  Specify the diameter of rasterized points.

  """

  ...

def use_program_point_size(enable: bool) -> None:

  """

  If enabled, the derived point size is taken from the (potentially clipped) shader builtin gl_PointSize.

  """

  ...

def viewport_get() -> None:

  """

  Viewport of the active framebuffer.

  """

  ...

def viewport_set(x: typing.Any, y: typing.Any, xsize: typing.Any, ysize: typing.Any) -> None:

  """

  Specifies the viewport of the active framebuffer.
Note: The viewport state is not saved upon framebuffer rebind.

  """

  ...
