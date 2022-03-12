"""


Image Buffer (imbuf)
********************

This module provides access to Blender's image manipulation API.

:func:`load`

:func:`new`

:func:`write`

"""

from . import types

import typing

def load(filepath: str) -> ImBuf:

  """

  Load an image from a file.

  """

  ...

def new(size: typing.Tuple[int, int]) -> ImBuf:

  """

  Load a new image.

  """

  ...

def write(image: ImBuf, filepath: str = image.filepath) -> None:

  """

  Write an image.

  """

  ...
