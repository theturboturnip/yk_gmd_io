"""


Asset Operators
***************

:func:`assign_action`

:func:`bundle_install`

:func:`catalog_delete`

:func:`catalog_new`

:func:`catalog_redo`

:func:`catalog_undo`

:func:`catalog_undo_push`

:func:`catalogs_save`

:func:`clear`

:func:`library_refresh`

:func:`mark`

:func:`open_containing_blend_file`

:func:`tag_add`

:func:`tag_remove`

"""

import typing

def assign_action() -> None:

  """

  Set this pose Action as active Action on the active Object

  """

  ...

def bundle_install(asset_library_ref: str = '', filepath: str = '', hide_props_region: bool = True, check_existing: bool = True, filter_blender: bool = True, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Copy the current .blend file into an Asset Library. Only works on standalone .blend files (i.e. when no other files are referenced)

  """

  ...

def catalog_delete(catalog_id: str = '') -> None:

  """

  Remove an asset catalog from the asset library (contained assets will not be affected and show up as unassigned)

  """

  ...

def catalog_new(parent_path: str = '') -> None:

  """

  Create a new catalog to put assets in

  """

  ...

def catalog_redo() -> None:

  """

  Redo the last undone edit to the asset catalogs

  """

  ...

def catalog_undo() -> None:

  """

  Undo the last edit to the asset catalogs

  """

  ...

def catalog_undo_push() -> None:

  """

  Store the current state of the asset catalogs in the undo buffer

  """

  ...

def catalogs_save() -> None:

  """

  Make any edits to any catalogs permanent by writing the current set up to the asset library

  """

  ...

def clear(set_fake_user: bool = False) -> None:

  """

  Delete all asset metadata and turn the selected asset data-blocks back into normal data-blocks

  """

  ...

def library_refresh() -> None:

  """

  Reread assets and asset catalogs from the asset library on disk

  """

  ...

def mark() -> None:

  """

  Enable easier reuse of selected data-blocks through the Asset Browser, with the help of customizable metadata (like previews, descriptions and tags)

  """

  ...

def open_containing_blend_file() -> None:

  """

  Open the blend file that contains the active asset

  """

  ...

def tag_add() -> None:

  """

  Add a new keyword tag to the active asset

  """

  ...

def tag_remove() -> None:

  """

  Remove an existing keyword tag from the active asset

  """

  ...
