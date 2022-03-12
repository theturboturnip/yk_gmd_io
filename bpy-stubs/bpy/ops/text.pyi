"""


Text Operators
**************

:func:`autocomplete`

:func:`comment_toggle`

:func:`convert_whitespace`

:func:`copy`

:func:`cursor_set`

:func:`cut`

:func:`delete`

:func:`duplicate_line`

:func:`find`

:func:`find_set_selected`

:func:`indent`

:func:`indent_or_autocomplete`

:func:`insert`

:func:`jump`

:func:`line_break`

:func:`line_number`

:func:`make_internal`

:func:`move`

:func:`move_lines`

:func:`move_select`

:func:`new`

:func:`open`

:func:`overwrite_toggle`

:func:`paste`

:func:`refresh_pyconstraints`

:func:`reload`

:func:`replace`

:func:`replace_set_selected`

:func:`resolve_conflict`

:func:`run_script`

:func:`save`

:func:`save_as`

:func:`scroll`

:func:`scroll_bar`

:func:`select_all`

:func:`select_line`

:func:`select_word`

:func:`selection_set`

:func:`start_find`

:func:`to_3d_object`

:func:`unindent`

:func:`unlink`

"""

import typing

def autocomplete() -> None:

  """

  Show a list of used text in the open document

  """

  ...

def comment_toggle(type: str = 'TOGGLE') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def convert_whitespace(type: str = 'SPACES') -> None:

  """

  Convert whitespaces by type

  """

  ...

def copy() -> None:

  """

  Copy selected text to clipboard

  """

  ...

def cursor_set(x: int = 0, y: int = 0) -> None:

  """

  Set cursor position

  """

  ...

def cut() -> None:

  """

  Cut selected text to clipboard

  """

  ...

def delete(type: str = 'NEXT_CHARACTER') -> None:

  """

  Delete text by cursor position

  """

  ...

def duplicate_line() -> None:

  """

  Duplicate the current line

  """

  ...

def find() -> None:

  """

  Find specified text

  """

  ...

def find_set_selected() -> None:

  """

  Find specified text and set as selected

  """

  ...

def indent() -> None:

  """

  Indent selected text

  """

  ...

def indent_or_autocomplete() -> None:

  """

  Indent selected text or autocomplete

  """

  ...

def insert(text: str = '') -> None:

  """

  Insert text at cursor position

  """

  ...

def jump(line: int = 1) -> None:

  """

  Jump cursor to line

  """

  ...

def line_break() -> None:

  """

  Insert line break at cursor position

  """

  ...

def line_number() -> None:

  """

  The current line number

  """

  ...

def make_internal() -> None:

  """

  Make active text file internal

  """

  ...

def move(type: str = 'LINE_BEGIN') -> None:

  """

  Move cursor to position type

  """

  ...

def move_lines(direction: str = 'DOWN') -> None:

  """

  Move the currently selected line(s) up/down

  """

  ...

def move_select(type: str = 'LINE_BEGIN') -> None:

  """

  Move the cursor while selecting

  """

  ...

def new() -> None:

  """

  Create a new text data-block

  """

  ...

def open(filepath: str = '', hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = True, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = True, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, display_type: str = 'DEFAULT', sort_method: str = '', internal: bool = False) -> None:

  """

  Open a new text data-block

  """

  ...

def overwrite_toggle() -> None:

  """

  Toggle overwrite while typing

  """

  ...

def paste(selection: bool = False) -> None:

  """

  Paste text from clipboard

  """

  ...

def refresh_pyconstraints() -> None:

  """

  Refresh all pyconstraints

  """

  ...

def reload() -> None:

  """

  Reload active text data-block from its file

  """

  ...

def replace(all: bool = False) -> None:

  """

  Replace text with the specified text

  """

  ...

def replace_set_selected() -> None:

  """

  Replace text with specified text and set as selected

  """

  ...

def resolve_conflict(resolution: str = 'IGNORE') -> None:

  """

  When external text is out of sync, resolve the conflict

  """

  ...

def run_script() -> None:

  """

  Run active script

  """

  ...

def save() -> None:

  """

  Save active text data-block

  """

  ...

def save_as(filepath: str = '', hide_props_region: bool = True, check_existing: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = True, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = True, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Save active text file with options

  """

  ...

def scroll(lines: int = 1) -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def scroll_bar(lines: int = 1) -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def select_all() -> None:

  """

  Select all text

  """

  ...

def select_line() -> None:

  """

  Select text by line

  """

  ...

def select_word() -> None:

  """

  Select word under cursor

  """

  ...

def selection_set() -> None:

  """

  Set cursor selection

  """

  ...

def start_find() -> None:

  """

  Start searching text

  """

  ...

def to_3d_object(split_lines: bool = False) -> None:

  """

  Create 3D text object from active text data-block

  """

  ...

def unindent() -> None:

  """

  Unindent selected text

  """

  ...

def unlink() -> None:

  """

  Unlink active text data-block

  """

  ...
