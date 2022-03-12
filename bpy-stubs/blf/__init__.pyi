"""


Font Drawing (blf)
******************

This module provides access to Blender's text drawing functions.


Hello World Text Example
========================

Example of using the blf module. For this module to work we
need to use the OpenGL wrapper :class:`~bgl` as well.

.. code::

  # import stand alone modules
  import blf
  import bpy

  font_info = {
      "font_id": 0,
      "handler": None,
  }


  def init():
      \"\"\"init function - runs once\"\"\"
      import os
      # Create a new font object, use external ttf file.
      font_path = bpy.path.abspath('//Zeyada.ttf')
      # Store the font indice - to use later.
      if os.path.exists(font_path):
          font_info["font_id"] = blf.load(font_path)
      else:
          # Default font.
          font_info["font_id"] = 0

      # set the font drawing routine to run every frame
      font_info["handler"] = bpy.types.SpaceView3D.draw_handler_add(
          draw_callback_px, (None, None), 'WINDOW', 'POST_PIXEL')


  def draw_callback_px(self, context):
      \"\"\"Draw on the viewports\"\"\"
      # BLF drawing routine
      font_id = font_info["font_id"]
      blf.position(font_id, 2, 80, 0)
      blf.size(font_id, 50, 72)
      blf.draw(font_id, "Hello World")


  if __name__ == '__main__':
      init()

:func:`aspect`

:func:`clipping`

:func:`color`

:func:`dimensions`

:func:`disable`

:func:`draw`

:func:`enable`

:func:`load`

:func:`position`

:func:`rotation`

:func:`shadow`

:func:`shadow_offset`

:func:`size`

:func:`unload`

:func:`word_wrap`

:data:`CLIPPING`

:data:`MONOCHROME`

:data:`ROTATION`

:data:`SHADOW`

:data:`WORD_WRAP`

"""

import typing

def aspect(fontid: int, aspect: float) -> None:

  """

  Set the aspect for drawing text.

  """

  ...

def clipping(fontid: int, xmin: float, ymin: float, xmax: float, ymax: float) -> None:

  """

  Set the clipping, enable/disable using CLIPPING.

  """

  ...

def color(fontid: int, r: float, g: float, b: float, a: float) -> None:

  """

  Set the color for drawing text.

  """

  ...

def dimensions(fontid: int, text: str) -> typing.Tuple[typing.Any, ...]:

  """

  Return the width and height of the text.

  """

  ...

def disable(fontid: int, option: int) -> None:

  """

  Disable option.

  """

  ...

def draw(fontid: int, text: str) -> None:

  """

  Draw text in the current context.

  """

  ...

def enable(fontid: int, option: int) -> None:

  """

  Enable option.

  """

  ...

def load(filename: str) -> int:

  """

  Load a new font.

  """

  ...

def position(fontid: int, x: float, y: float, z: float) -> None:

  """

  Set the position for drawing text.

  """

  ...

def rotation(fontid: int, angle: float) -> None:

  """

  Set the text rotation angle, enable/disable using ROTATION.

  """

  ...

def shadow(fontid: int, level: int, r: float, g: float, b: float, a: float) -> None:

  """

  Shadow options, enable/disable using SHADOW .

  """

  ...

def shadow_offset(fontid: int, x: float, y: float) -> None:

  """

  Set the offset for shadow text.

  """

  ...

def size(fontid: int, size: int, dpi: int) -> None:

  """

  Set the size and dpi for drawing text.

  """

  ...

def unload(filename: str) -> None:

  """

  Unload an existing font.

  """

  ...

def word_wrap(fontid: int, wrap_width: int) -> None:

  """

  Set the wrap width, enable/disable using WORD_WRAP.

  """

  ...

CLIPPING: typing.Any = ...

"""

Constant value 2

"""

MONOCHROME: typing.Any = ...

"""

Constant value 128

"""

ROTATION: typing.Any = ...

"""

Constant value 1

"""

SHADOW: typing.Any = ...

"""

Constant value 4

"""

WORD_WRAP: typing.Any = ...

"""

Constant value 64

"""
