"""


Additional Math Functions (bl_math)
***********************************

Miscellaneous math utilities module

:func:`clamp`

:func:`lerp`

:func:`smoothstep`

"""

import typing

def clamp(value: float, min: float = 0, max: float = 1) -> float:

  """

  Clamps the float value between minimum and maximum. To avoid
confusion, any call must use either one or all three arguments.

  """

  ...

def lerp(from_value: float, to_value: float, factor: float) -> float:

  """

  Linearly interpolate between two float values based on factor.

  """

  ...

def smoothstep(from_value: float, to_value: float, value: typing.Any) -> float:

  """

  Performs smooth interpolation between 0 and 1 as value changes between from and to values.
Outside the range the function returns the same value as the nearest edge.

  """

  ...
