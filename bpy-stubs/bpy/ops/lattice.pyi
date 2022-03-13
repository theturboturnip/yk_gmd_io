"""


Lattice Operators
*****************

:func:`flip`

:func:`make_regular`

:func:`select_all`

:func:`select_less`

:func:`select_mirror`

:func:`select_more`

:func:`select_random`

:func:`select_ungrouped`

"""

import typing

def flip(axis: str = 'U') -> None:

  """

  Mirror all control points without inverting the lattice deform

  """

  ...

def make_regular() -> None:

  """

  Set UVW control points a uniform distance apart

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Change selection of all UVW control points

  """

  ...

def select_less() -> None:

  """

  Deselect vertices at the boundary of each selection region

  """

  ...

def select_mirror(axis: typing.Set[str] = {'X'}, extend: bool = False) -> None:

  """

  Select mirrored lattice points

  """

  ...

def select_more() -> None:

  """

  Select vertex directly linked to already selected ones

  """

  ...

def select_random(ratio: float = 0.5, seed: int = 0, action: str = 'SELECT') -> None:

  """

  Randomly select UVW control points

  """

  ...

def select_ungrouped(extend: bool = False) -> None:

  """

  Select vertices without a group

  """

  ...
