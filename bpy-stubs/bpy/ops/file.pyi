"""


File Operators
**************

:func:`autopack_toggle`

:func:`bookmark_add`

:func:`bookmark_cleanup`

:func:`bookmark_delete`

:func:`bookmark_move`

:func:`cancel`

:func:`delete`

:func:`directory_new`

:func:`execute`

:func:`filenum`

:func:`filepath_drop`

:func:`find_missing_files`

:func:`hidedot`

:func:`highlight`

:func:`make_paths_absolute`

:func:`make_paths_relative`

:func:`mouse_execute`

:func:`next`

:func:`pack_all`

:func:`pack_libraries`

:func:`parent`

:func:`previous`

:func:`refresh`

:func:`rename`

:func:`report_missing_files`

:func:`reset_recent`

:func:`select`

:func:`select_all`

:func:`select_bookmark`

:func:`select_box`

:func:`select_walk`

:func:`smoothscroll`

:func:`sort_column_ui_context`

:func:`start_filter`

:func:`unpack_all`

:func:`unpack_item`

:func:`unpack_libraries`

:func:`view_selected`

"""

import typing

def autopack_toggle() -> None:

  """

  Automatically pack all external files into the .blend file

  """

  ...

def bookmark_add() -> None:

  """

  Add a bookmark for the selected/active directory

  """

  ...

def bookmark_cleanup() -> None:

  """

  Delete all invalid bookmarks

  """

  ...

def bookmark_delete(index: int = -1) -> None:

  """

  Delete selected bookmark

  """

  ...

def bookmark_move(direction: str = 'TOP') -> None:

  """

  Move the active bookmark up/down in the list

  """

  ...

def cancel() -> None:

  """

  Cancel loading of selected file

  """

  ...

def delete() -> None:

  """

  Move selected files to the trash or recycle bin

  """

  ...

def directory_new(directory: str = '', open: bool = False, confirm: bool = True) -> None:

  """

  Create a new directory

  """

  ...

def execute() -> None:

  """

  Execute selected file

  """

  ...

def filenum(increment: int = 1) -> None:

  """

  Increment number in filename

  """

  ...

def filepath_drop(filepath: str = 'Path') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def find_missing_files(find_all: bool = False, directory: str = '', hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = False, filter_blenlib: bool = False, filemode: int = 9, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Try to find missing external files

  """

  ...

def hidedot() -> None:

  """

  Toggle hide hidden dot files

  """

  ...

def highlight() -> None:

  """

  Highlight selected file(s)

  """

  ...

def make_paths_absolute() -> None:

  """

  Make all paths to external files absolute

  """

  ...

def make_paths_relative() -> None:

  """

  Make all paths to external files relative to current .blend

  """

  ...

def mouse_execute() -> None:

  """

  Perform the current execute action for the file under the cursor (e.g. open the file)

  """

  ...

def next() -> None:

  """

  Move to next folder

  """

  ...

def pack_all() -> None:

  """

  Pack all used external files into this .blend

  """

  ...

def pack_libraries() -> None:

  """

  Store all data-blocks linked from other .blend files in the current .blend file. Library references are preserved so the linked data-blocks can be unpacked again

  """

  ...

def parent() -> None:

  """

  Move to parent directory

  """

  ...

def previous() -> None:

  """

  Move to previous folder

  """

  ...

def refresh() -> None:

  """

  Refresh the file list

  """

  ...

def rename() -> None:

  """

  Rename file or file directory

  """

  ...

def report_missing_files() -> None:

  """

  Report all missing external files

  """

  ...

def reset_recent() -> None:

  """

  Reset recent files

  """

  ...

def select(wait_to_deselect_others: bool = False, mouse_x: int = 0, mouse_y: int = 0, extend: bool = False, fill: bool = False, open: bool = True, deselect_all: bool = False, only_activate_if_selected: bool = False, pass_through: bool = False) -> None:

  """

  Handle mouse clicks to select and activate items

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Select or deselect all files

  """

  ...

def select_bookmark(dir: str = '') -> None:

  """

  Select a bookmarked directory

  """

  ...

def select_box(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Activate/select the file(s) contained in the border

  """

  ...

def select_walk(direction: str = 'UP', extend: bool = False, fill: bool = False) -> None:

  """

  Select/Deselect files by walking through them

  """

  ...

def smoothscroll() -> None:

  """

  Smooth scroll to make editable file visible

  """

  ...

def sort_column_ui_context() -> None:

  """

  Change sorting to use column under cursor

  """

  ...

def start_filter() -> None:

  """

  Start entering filter text

  """

  ...

def unpack_all(method: str = 'USE_LOCAL') -> None:

  """

  Unpack all files packed into this .blend to external ones

  """

  ...

def unpack_item(method: str = 'USE_LOCAL', id_name: str = '', id_type: int = 19785) -> None:

  """

  Unpack this file to an external file

  """

  ...

def unpack_libraries() -> None:

  """

  Restore all packed linked data-blocks to their original locations

  """

  ...

def view_selected() -> None:

  """

  Scroll the selected files into view

  """

  ...
