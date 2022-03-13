"""


Image Buffer Types (imbuf.types)
********************************

This module provides access to image buffer types.

:class:`ImBuf`

"""

import typing

class ImBuf:

  def copy(self) -> ImBuf:

    ...

  def crop(self, min: typing.Tuple[int, int], max: typing.Tuple[int, int]) -> None:

    """

    Crop the image.

    """

    ...

  def free(self) -> None:

    """

    Clear image data immediately (causing an error on re-use).

    """

    ...

  def resize(self, size: typing.Tuple[int, int], method: str = 'FAST') -> None:

    """

    Resize the image.

    """

    ...

  channels: int = ...

  """

  Number of bit-planes.

  """

  filepath: str = ...

  """

  filepath associated with this image.

  """

  planes: int = ...

  """

  Number of bits associated with this image.

  """

  ppm: typing.Tuple[float, float] = ...

  """

  pixels per meter.

  """

  size: typing.Tuple[int, int] = ...

  """

  size of the image in pixels.

  """
