"""


Paintcurve Operators
********************

:func:`add_point`

:func:`add_point_slide`

:func:`cursor`

:func:`delete_point`

:func:`draw`

:func:`new`

:func:`select`

:func:`slide`

"""

import typing

def add_point(location: typing.Tuple[int, int] = (0, 0)) -> None:

  """

  Add New Paint Curve Point

  """

  ...

def add_point_slide(PAINTCURVE_OT_add_point: PAINTCURVE_OT_add_point = None, PAINTCURVE_OT_slide: PAINTCURVE_OT_slide = None) -> None:

  """

  Add new curve point and slide it

  """

  ...

def cursor() -> None:

  """

  Place cursor

  """

  ...

def delete_point() -> None:

  """

  Remove Paint Curve Point

  """

  ...

def draw() -> None:

  """

  Draw curve

  """

  ...

def new() -> None:

  """

  Add new paint curve

  """

  ...

def select(location: typing.Tuple[int, int] = (0, 0), toggle: bool = False, extend: bool = False) -> None:

  """

  Select a paint curve point

  """

  ...

def slide(align: bool = False, select: bool = True) -> None:

  """

  Select and slide paint curve point

  """

  ...
