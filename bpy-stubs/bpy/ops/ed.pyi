"""


Ed Operators
************

:func:`flush_edits`

:func:`lib_id_fake_user_toggle`

:func:`lib_id_generate_preview`

:func:`lib_id_load_custom_preview`

:func:`lib_id_unlink`

:func:`redo`

:func:`undo`

:func:`undo_history`

:func:`undo_push`

:func:`undo_redo`

"""

import typing

def flush_edits() -> None:

  """

  Flush edit data from active editing modes

  """

  ...

def lib_id_fake_user_toggle() -> None:

  """

  Save this data-block even if it has no users

  """

  ...

def lib_id_generate_preview() -> None:

  """

  Create an automatic preview for the selected data-block

  """

  ...

def lib_id_load_custom_preview(filepath: str = '', hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = True, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Choose an image to help identify the data-block visually

  """

  ...

def lib_id_unlink() -> None:

  """

  Remove a usage of a data-block, clearing the assignment

  """

  ...

def redo() -> None:

  """

  Redo previous action

  """

  ...

def undo() -> None:

  """

  Undo previous action

  """

  ...

def undo_history(item: int = 0) -> None:

  """

  Redo specific action in history

  """

  ...

def undo_push(message: str = 'Add an undo step *argsfunction may be moved*args') -> None:

  """

  Add an undo state (internal use only)

  """

  ...

def undo_redo() -> None:

  """

  Undo and redo previous action

  """

  ...
