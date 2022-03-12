"""


View2D Operators
****************

:func:`edge_pan`

:func:`ndof`

:func:`pan`

:func:`reset`

:func:`scroll_down`

:func:`scroll_left`

:func:`scroll_right`

:func:`scroll_up`

:func:`scroller_activate`

:func:`smoothview`

:func:`zoom`

:func:`zoom_border`

:func:`zoom_in`

:func:`zoom_out`

"""

import typing

def edge_pan(inside_padding: float = 1.0, outside_padding: float = 0.0, speed_ramp: float = 1.0, max_speed: float = 500.0, delay: float = 1.0, zoom_influence: float = 0.0) -> None:

  """

  Pan the view when the mouse is held at an edge

  """

  ...

def ndof() -> None:

  """

  Use a 3D mouse device to pan/zoom the view

  """

  ...

def pan(deltax: int = 0, deltay: int = 0) -> None:

  """

  Pan the view

  """

  ...

def reset() -> None:

  """

  Reset the view

  """

  ...

def scroll_down(deltax: int = 0, deltay: int = 0, page: bool = False) -> None:

  """

  Scroll the view down

  """

  ...

def scroll_left(deltax: int = 0, deltay: int = 0) -> None:

  """

  Scroll the view left

  """

  ...

def scroll_right(deltax: int = 0, deltay: int = 0) -> None:

  """

  Scroll the view right

  """

  ...

def scroll_up(deltax: int = 0, deltay: int = 0, page: bool = False) -> None:

  """

  Scroll the view up

  """

  ...

def scroller_activate() -> None:

  """

  Scroll view by mouse click and drag

  """

  ...

def smoothview(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True) -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def zoom(deltax: float = 0.0, deltay: float = 0.0, use_cursor_init: bool = True) -> None:

  """

  Zoom in/out the view

  """

  ...

def zoom_border(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, zoom_out: bool = False) -> None:

  """

  Zoom in the view to the nearest item contained in the border

  """

  ...

def zoom_in(zoomfacx: float = 0.0, zoomfacy: float = 0.0) -> None:

  """

  Zoom in the view

  """

  ...

def zoom_out(zoomfacx: float = 0.0, zoomfacy: float = 0.0) -> None:

  """

  Zoom out the view

  """

  ...
