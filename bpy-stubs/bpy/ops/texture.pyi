"""


Texture Operators
*****************

:func:`new`

:func:`slot_copy`

:func:`slot_move`

:func:`slot_paste`

"""

import typing

def new() -> None:

  """

  Add a new texture

  """

  ...

def slot_copy() -> None:

  """

  Copy the material texture settings and nodes

  """

  ...

def slot_move(type: str = 'UP') -> None:

  """

  Move texture slots up and down

  """

  ...

def slot_paste() -> None:

  """

  Copy the texture settings and nodes

  """

  ...
