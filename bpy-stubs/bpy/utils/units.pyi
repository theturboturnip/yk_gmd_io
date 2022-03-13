"""


bpy.utils submodule (bpy.utils.units)
*************************************

This module contains some data/methods regarding units handling.

:data:`categories`

:data:`systems`

:func:`to_string`

:func:`to_value`

"""

import typing

categories: typing.Any = ...

"""

Constant value bpy.utils.units.categories(NONE='NONE', LENGTH='LENGTH', AREA='AREA', VOLUME='VOLUME', MASS='MASS', ROTATION='ROTATION', TIME='TIME', VELOCITY='VELOCITY', ACCELERATION='ACCELERATION', CAMERA='CAMERA', POWER='POWER')

"""

systems: typing.Any = ...

"""

Constant value bpy.utils.units.systems(NONE='NONE', METRIC='METRIC', IMPERIAL='IMPERIAL')

"""

def to_string(self, unit_system: str, unit_category: str, value: float, precision: int = 3, split_unit: bool = False, compatible_unit: bool = False) -> str:

  """

  Convert a given input float value into a string with units.

  """

  ...

def to_value(self, unit_system: str, unit_category: str, str_input: str, str_ref_unit: str = None) -> float:

  """

  Convert a given input string into a float value.

  """

  ...
