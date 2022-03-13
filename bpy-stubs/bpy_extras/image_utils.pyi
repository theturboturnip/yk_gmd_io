"""


bpy_extras submodule (bpy_extras.image_utils)
*********************************************

:func:`load_image`

"""

import typing

import bpy

def load_image(imagepath: typing.Any, dirname: str = '', place_holder: bool = False, recursive: bool = False, ncase_cmp: bool = True, convert_callback: typing.Callable = None, verbose: typing.Any = False, relpath: typing.Any = None, check_existing: bool = False, force_reload: bool = False) -> bpy.types.Image:

  """

  Return an image from the file path with options to search multiple paths
and return a placeholder if its not found.

  """

  ...
