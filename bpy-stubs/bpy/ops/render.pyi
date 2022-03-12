"""


Render Operators
****************

:func:`cycles_integrator_preset_add`

:func:`cycles_sampling_preset_add`

:func:`cycles_viewport_sampling_preset_add`

:func:`opengl`

:func:`play_rendered_anim`

:func:`preset_add`

:func:`render`

:func:`shutter_curve_preset`

:func:`view_cancel`

:func:`view_show`

"""

import typing

def cycles_integrator_preset_add(name: str = '', remove_name: bool = False, remove_active: bool = False) -> None:

  """

  Add an Integrator Preset

  """

  ...

def cycles_sampling_preset_add(name: str = '', remove_name: bool = False, remove_active: bool = False) -> None:

  """

  Add a Sampling Preset

  """

  ...

def cycles_viewport_sampling_preset_add(name: str = '', remove_name: bool = False, remove_active: bool = False) -> None:

  """

  Add a Viewport Sampling Preset

  """

  ...

def opengl(animation: bool = False, render_keyed_only: bool = False, sequencer: bool = False, write_still: bool = False, view_context: bool = True) -> None:

  """

  Take a snapshot of the active viewport

  """

  ...

def play_rendered_anim() -> None:

  """

  Play back rendered frames/movies using an external player

  """

  ...

def preset_add(name: str = '', remove_name: bool = False, remove_active: bool = False) -> None:

  """

  Add or remove a Render Preset

  """

  ...

def render(animation: bool = False, write_still: bool = False, use_viewport: bool = False, layer: str = '', scene: str = '') -> None:

  """

  Render active scene

  """

  ...

def shutter_curve_preset(shape: str = 'SMOOTH') -> None:

  """

  Set shutter curve

  """

  ...

def view_cancel() -> None:

  """

  Cancel show render view

  """

  ...

def view_show() -> None:

  """

  Toggle show render view

  """

  ...
