"""


Sound Operators
***************

:func:`bake_animation`

:func:`mixdown`

:func:`open`

:func:`open_mono`

:func:`pack`

:func:`unpack`

:func:`update_animation_flags`

"""

import typing

def bake_animation() -> None:

  """

  Update the audio animation cache

  """

  ...

def mixdown(filepath: str = '', check_existing: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = True, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, display_type: str = 'DEFAULT', sort_method: str = '', accuracy: int = 1024, container: str = 'FLAC', codec: str = 'FLAC', format: str = 'S16', bitrate: int = 192, split_channels: bool = False) -> None:

  """

  Mix the scene's audio to a sound file

  """

  ...

def open(filepath: str = '', hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = True, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = True, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '', cache: bool = False, mono: bool = False) -> None:

  """

  Load a sound file

  """

  ...

def open_mono(filepath: str = '', hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = True, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = True, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '', cache: bool = False, mono: bool = True) -> None:

  """

  Load a sound file as mono

  """

  ...

def pack() -> None:

  """

  Pack the sound into the current blend file

  """

  ...

def unpack(method: str = 'USE_LOCAL', id: str = '') -> None:

  """

  Unpack the sound to the samples filename

  """

  ...

def update_animation_flags() -> None:

  """

  Update animation flags

  """

  ...
