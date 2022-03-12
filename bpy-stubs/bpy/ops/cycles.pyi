"""


Cycles Operators
****************

:func:`denoise_animation`

:func:`merge_images`

:func:`use_shading_nodes`

"""

import typing

def denoise_animation(input_filepath: str = '', output_filepath: str = '') -> None:

  """

  Denoise rendered animation sequence using current scene and view layer settings. Requires denoising data passes and output to OpenEXR multilayer files

  """

  ...

def merge_images(input_filepath1: str = '', input_filepath2: str = '', output_filepath: str = '') -> None:

  """

  Combine OpenEXR multilayer images rendered with different sample ranges into one image with reduced noise

  """

  ...

def use_shading_nodes() -> None:

  """

  Enable nodes on a material, world or light

  """

  ...
