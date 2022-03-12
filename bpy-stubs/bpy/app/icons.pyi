"""


Application Icons (bpy.app.icons)
*********************************

:func:`new_triangles`

:func:`new_triangles_from_file`

:func:`release`

"""

import typing

def new_triangles(range: typing.Tuple[typing.Any, ...], coords: typing.Any, colors: typing.Any) -> int:

  """

  Create a new icon from triangle geometry.

  """

  ...

def new_triangles_from_file(filename: str) -> int:

  """

  Create a new icon from triangle geometry.

  """

  ...

def release(icon_id: typing.Any) -> None:

  """

  Release the icon.

  """

  ...
