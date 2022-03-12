"""


Brush Operators
***************

:func:`add`

:func:`add_gpencil`

:func:`curve_preset`

:func:`reset`

:func:`scale_size`

:func:`stencil_control`

:func:`stencil_fit_image_aspect`

:func:`stencil_reset_transform`

"""

import typing

def add() -> None:

  """

  Add brush by mode type

  """

  ...

def add_gpencil() -> None:

  """

  Add brush for Grease Pencil

  """

  ...

def curve_preset(shape: str = 'SMOOTH') -> None:

  """

  Set brush shape

  """

  ...

def reset() -> None:

  """

  Return brush to defaults based on current tool

  """

  ...

def scale_size(scalar: float = 1.0) -> None:

  """

  Change brush size by a scalar

  """

  ...

def stencil_control(mode: str = 'TRANSLATION', texmode: str = 'PRIMARY') -> None:

  """

  Control the stencil brush

  """

  ...

def stencil_fit_image_aspect(use_repeat: bool = True, use_scale: bool = True, mask: bool = False) -> None:

  """

  When using an image texture, adjust the stencil size to fit the image aspect ratio

  """

  ...

def stencil_reset_transform(mask: bool = False) -> None:

  """

  Reset the stencil transformation to the default

  """

  ...
