"""


Palette Operators
*****************

:func:`color_add`

:func:`color_delete`

:func:`color_move`

:func:`extract_from_image`

:func:`join`

:func:`new`

:func:`sort`

"""

import typing

def color_add() -> None:

  """

  Add new color to active palette

  """

  ...

def color_delete() -> None:

  """

  Remove active color from palette

  """

  ...

def color_move(type: str = 'UP') -> None:

  """

  Move the active Color up/down in the list

  """

  ...

def extract_from_image(threshold: int = 1) -> None:

  """

  Extract all colors used in Image and create a Palette

  """

  ...

def join(palette: str = '') -> None:

  """

  Join Palette Swatches

  """

  ...

def new() -> None:

  """

  Add new palette

  """

  ...

def sort(type: str = 'HSV') -> None:

  """

  Sort Palette Colors

  """

  ...
