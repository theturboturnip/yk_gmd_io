"""


Dpaint Operators
****************

:func:`bake`

:func:`output_toggle`

:func:`surface_slot_add`

:func:`surface_slot_remove`

:func:`type_toggle`

"""

import typing

def bake() -> None:

  """

  Bake dynamic paint image sequence surface

  """

  ...

def output_toggle(output: str = 'A') -> None:

  """

  Add or remove Dynamic Paint output data layer

  """

  ...

def surface_slot_add() -> None:

  """

  Add a new Dynamic Paint surface slot

  """

  ...

def surface_slot_remove() -> None:

  """

  Remove the selected surface slot

  """

  ...

def type_toggle(type: str = 'CANVAS') -> None:

  """

  Toggle whether given type is active or not

  """

  ...
