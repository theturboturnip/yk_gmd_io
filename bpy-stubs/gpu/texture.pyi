"""


GPU Texture Utilities (gpu.texture)
***********************************

This module provides utils for textures.

:func:`from_image`

"""

import typing

import gpu

import bpy

def from_image(image: bpy.types.Image) -> gpu.types.GPUTexture:

  """

  Get GPUTexture corresponding to an Image datablock. The GPUTexture memory is shared with Blender.
Note: Colors read from the texture will be in scene linear color space and have premultiplied or straight alpha matching the image alpha mode.

  """

  ...
