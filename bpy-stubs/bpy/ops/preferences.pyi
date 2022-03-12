"""


Preferences Operators
*********************

:func:`addon_disable`

:func:`addon_enable`

:func:`addon_expand`

:func:`addon_install`

:func:`addon_refresh`

:func:`addon_remove`

:func:`addon_show`

:func:`app_template_install`

:func:`asset_library_add`

:func:`asset_library_remove`

:func:`associate_blend`

:func:`autoexec_path_add`

:func:`autoexec_path_remove`

:func:`copy_prev`

:func:`keyconfig_activate`

:func:`keyconfig_export`

:func:`keyconfig_import`

:func:`keyconfig_remove`

:func:`keyconfig_test`

:func:`keyitem_add`

:func:`keyitem_remove`

:func:`keyitem_restore`

:func:`keymap_restore`

:func:`reset_default_theme`

:func:`studiolight_copy_settings`

:func:`studiolight_install`

:func:`studiolight_new`

:func:`studiolight_show`

:func:`studiolight_uninstall`

:func:`theme_install`

"""

import typing

def addon_disable(module: str = '') -> None:

  """

  Disable an add-on

  """

  ...

def addon_enable(module: str = '') -> None:

  """

  Enable an add-on

  """

  ...

def addon_expand(module: str = '') -> None:

  """

  Display information and preferences for this add-on

  """

  ...

def addon_install(overwrite: bool = True, target: str = 'DEFAULT', filepath: str = '', filter_folder: bool = True, filter_python: bool = True, filter_glob: str = '*args.py;*args.zip') -> None:

  """

  Install an add-on

  """

  ...

def addon_refresh() -> None:

  """

  Scan add-on directories for new modules

  """

  ...

def addon_remove(module: str = '') -> None:

  """

  Delete the add-on from the file system

  """

  ...

def addon_show(module: str = '') -> None:

  """

  Show add-on preferences

  """

  ...

def app_template_install(overwrite: bool = True, filepath: str = '', filter_folder: bool = True, filter_glob: str = '*args.zip') -> None:

  """

  Install an application template

  """

  ...

def asset_library_add(directory: str = '', hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Add a directory to be used by the Asset Browser as source of assets

  """

  ...

def asset_library_remove(index: int = 0) -> None:

  """

  Remove a path to a .blend file, so the Asset Browser will not attempt to show it anymore

  """

  ...

def associate_blend() -> None:

  """

  Use this installation for .blend files and to display thumbnails

  """

  ...

def autoexec_path_add() -> None:

  """

  Add path to exclude from auto-execution

  """

  ...

def autoexec_path_remove(index: int = 0) -> None:

  """

  Remove path to exclude from auto-execution

  """

  ...

def copy_prev() -> None:

  """

  Copy settings from previous version

  """

  ...

def keyconfig_activate(filepath: str = '') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def keyconfig_export(all: bool = False, filepath: str = '', filter_folder: bool = True, filter_text: bool = True, filter_python: bool = True) -> None:

  """

  Export key configuration to a python script

  """

  ...

def keyconfig_import(filepath: str = 'keymap.py', filter_folder: bool = True, filter_text: bool = True, filter_python: bool = True, keep_original: bool = True) -> None:

  """

  Import key configuration from a python script

  """

  ...

def keyconfig_remove() -> None:

  """

  Remove key config

  """

  ...

def keyconfig_test() -> None:

  """

  Test key configuration for conflicts

  """

  ...

def keyitem_add() -> None:

  """

  Add key map item

  """

  ...

def keyitem_remove(item_id: int = 0) -> None:

  """

  Remove key map item

  """

  ...

def keyitem_restore(item_id: int = 0) -> None:

  """

  Restore key map item

  """

  ...

def keymap_restore(all: bool = False) -> None:

  """

  Restore key map(s)

  """

  ...

def reset_default_theme() -> None:

  """

  Reset to the default theme colors

  """

  ...

def studiolight_copy_settings(index: int = 0) -> None:

  """

  Copy Studio Light settings to the Studio Light editor

  """

  ...

def studiolight_install(files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, directory: str = '', filter_folder: bool = True, filter_glob: str = '*args.png;*args.jpg;*args.hdr;*args.exr', type: str = 'MATCAP') -> None:

  """

  Install a user defined light

  """

  ...

def studiolight_new(filename: str = 'StudioLight') -> None:

  """

  Save custom studio light from the studio light editor settings

  """

  ...

def studiolight_show() -> None:

  """

  Show light preferences

  """

  ...

def studiolight_uninstall(index: int = 0) -> None:

  """

  Delete Studio Light

  """

  ...

def theme_install(overwrite: bool = True, filepath: str = '', filter_folder: bool = True, filter_glob: str = '*args.xml') -> None:

  """

  Load and apply a Blender XML theme file

  """

  ...
