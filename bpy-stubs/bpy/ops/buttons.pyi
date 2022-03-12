"""


Buttons Operators
*****************

:func:`clear_filter`

:func:`context_menu`

:func:`directory_browse`

:func:`file_browse`

:func:`start_filter`

:func:`toggle_pin`

"""

import typing

def clear_filter() -> None:

  """

  Clear the search filter

  """

  ...

def context_menu() -> None:

  """

  Display properties editor context_menu

  """

  ...

def directory_browse(directory: str = '', hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = False, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Open a directory browser, hold Shift to open the file, Alt to browse containing directory

  """

  ...

def file_browse(filepath: str = '', hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = False, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Open a file browser, hold Shift to open the file, Alt to browse containing directory

  """

  ...

def start_filter() -> None:

  """

  Start entering filter text

  """

  ...

def toggle_pin() -> None:

  """

  Keep the current data-block displayed

  """

  ...
