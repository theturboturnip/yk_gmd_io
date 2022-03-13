"""


Marker Operators
****************

:func:`add`

:func:`camera_bind`

:func:`delete`

:func:`duplicate`

:func:`make_links_scene`

:func:`move`

:func:`rename`

:func:`select`

:func:`select_all`

:func:`select_box`

"""

import typing

def add() -> None:

  """

  Add a new time marker

  """

  ...

def camera_bind() -> None:

  """

  Bind the selected camera to a marker on the current frame

  """

  ...

def delete() -> None:

  """

  Delete selected time marker(s)

  """

  ...

def duplicate(frames: int = 0) -> None:

  """

  Duplicate selected time marker(s)

  """

  ...

def make_links_scene(scene: str = '') -> None:

  """

  Copy selected markers to another scene

  """

  ...

def move(frames: int = 0, tweak: bool = False) -> None:

  """

  Move selected time marker(s)

  """

  ...

def rename(name: str = 'RenamedMarker') -> None:

  """

  Rename first selected time marker

  """

  ...

def select(wait_to_deselect_others: bool = False, mouse_x: int = 0, mouse_y: int = 0, extend: bool = False, camera: bool = False) -> None:

  """

  Select time marker(s)

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Change selection of all time markers

  """

  ...

def select_box(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, mode: str = 'SET', tweak: bool = False) -> None:

  """

  Select all time markers using box selection

  """

  ...
