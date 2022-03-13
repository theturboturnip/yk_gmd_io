"""


Utilities (bpy.utils)
*********************

This module contains utility functions specific to blender but
not associated with blenders internal data.

:func:`blend_paths`

:func:`escape_identifier`

:func:`unescape_identifier`

:func:`register_class`

:func:`resource_path`

:func:`unregister_class`

:func:`keyconfig_init`

:func:`keyconfig_set`

:func:`load_scripts`

:func:`modules_from_path`

:func:`preset_find`

:func:`preset_paths`

:func:`refresh_script_paths`

:func:`app_template_paths`

:func:`register_manual_map`

:func:`unregister_manual_map`

:func:`register_classes_factory`

:func:`register_submodule_factory`

:func:`register_tool`

:func:`make_rna_paths`

:func:`manual_map`

:func:`script_path_user`

:func:`script_path_pref`

:func:`script_paths`

:func:`smpte_from_frame`

:func:`smpte_from_seconds`

:func:`unregister_tool`

:func:`user_resource`

:func:`execfile`

"""

from . import units

from . import previews

import typing

def blend_paths(absolute: bool = False, packed: bool = False, local: bool = False) -> typing.List[str]:

  """

  Returns a list of paths to external files referenced by the loaded .blend file.

  """

  ...

def escape_identifier(string: str) -> str:

  """

  Simple string escaping function used for animation paths.

  """

  ...

def unescape_identifier(string: str) -> str:

  """

  Simple string un-escape function used for animation paths.
This performs the reverse of *escape_identifier*.

  """

  ...

def register_class(cls: typing.Type) -> None:

  """

  Register a subclass of a Blender type class.

  Note: If the class has a *register* class method it will be called
before registration.

  """

  ...

def resource_path(type: str, major: int = bpy.app.version[0], minor: str = bpy.app.version[1]) -> str:

  """

  Return the base path for storing system files.

  """

  ...

def unregister_class(cls: typing.Any) -> None:

  """

  Unload the Python class from blender.

  If the class has an *unregister* class method it will be called
before unregistering.

  """

  ...

def keyconfig_init() -> None:

  ...

def keyconfig_set(filepath: typing.Any, *args, report: typing.Any = None) -> None:

  ...

def load_scripts(*args, reload_scripts: bool = False, refresh_scripts: bool = False) -> None:

  """

  Load scripts and run each modules register function.

  """

  ...

def modules_from_path(path: str, loaded_modules: typing.Set[typing.Any]) -> typing.List[typing.Any]:

  """

  Load all modules in a path and return them as a list.

  """

  ...

def preset_find(name: typing.Any, preset_path: typing.Any, *args, display_name: typing.Any = False, ext: typing.Any = '.py') -> None:

  ...

def preset_paths(subdir: str) -> typing.List[typing.Any]:

  """

  Returns a list of paths for a specific preset.

  """

  ...

def refresh_script_paths() -> None:

  """

  Run this after creating new script paths to update sys.path

  """

  ...

def app_template_paths(*args, path: str = None) -> typing.Any:

  """

  Returns valid application template paths.

  """

  ...

def register_manual_map(manual_hook: typing.Any) -> None:

  ...

def unregister_manual_map(manual_hook: typing.Any) -> None:

  ...

def register_classes_factory(classes: typing.Any) -> None:

  """

  Utility function to create register and unregister functions
which simply registers and unregisters a sequence of classes.

  """

  ...

def register_submodule_factory(module_name: str, submodule_names: typing.List[str]) -> typing.Tuple[typing.Any, ...]:

  """

  Utility function to create register and unregister functions
which simply load submodules,
calling their register & unregister functions.

  Note: Modules are registered in the order given,
unregistered in reverse order.

  """

  ...

def register_tool(tool_cls: typing.Any, *args, after: typing.Any = None, separator: bool = False, group: bool = False) -> None:

  """

  Register a tool in the toolbar.

  """

  ...

def make_rna_paths(struct_name: str, prop_name: str, enum_name: str) -> typing.Tuple[str, ...]:

  """

  Create RNA "paths" from given names.

  """

  ...

def manual_map() -> None:

  ...

def script_path_user() -> None:

  """

  returns the env var and falls back to home dir or None

  """

  ...

def script_path_pref() -> None:

  """

  returns the user preference or None

  """

  ...

def script_paths(*args, subdir: str = None, user_pref: bool = True, check_all: bool = False, use_user: typing.Any = True) -> typing.List[typing.Any]:

  """

  Returns a list of valid script paths.

  """

  ...

def smpte_from_frame(frame: typing.Union[int, float], *args, fps: typing.Any = None, fps_base: typing.Any = None) -> str:

  """

  Returns an SMPTE formatted string from the *frame*:
``HH:MM:SS:FF``.

  If *fps* and *fps_base* are not given the current scene is used.

  """

  ...

def smpte_from_seconds(time: int, *args, fps: typing.Any = None, fps_base: typing.Any = None) -> str:

  """

  Returns an SMPTE formatted string from the *time*:
``HH:MM:SS:FF``.

  If *fps* and *fps_base* are not given the current scene is used.

  """

  ...

def unregister_tool(tool_cls: typing.Any) -> None:

  ...

def user_resource(resource_type: typing.Any, *args, path: str = '', create: bool = False) -> str:

  """

  Return a user resource path (normally from the users home directory).

  """

  ...

def execfile(filepath: str, *args, mod: typing.Any = None) -> typing.Any:

  """

  Execute a file path as a Python script.

  """

  ...
