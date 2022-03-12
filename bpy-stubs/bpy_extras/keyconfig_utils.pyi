"""


bpy_extras submodule (bpy_extras.keyconfig_utils)
*************************************************

:func:`addon_keymap_register`

:func:`addon_keymap_unregister`

:func:`keyconfig_test`

"""

import typing

def addon_keymap_register(keymap_data: typing.Any) -> None:

  """

  Register a set of keymaps for addons using a list of keymaps.

  See 'blender_defaults.py' for examples of the format this takes.

  """

  ...

def addon_keymap_unregister(keymap_data: typing.Any) -> None:

  """

  Unregister a set of keymaps for addons.

  """

  ...

def keyconfig_test(kc: typing.Any) -> None:

  ...
