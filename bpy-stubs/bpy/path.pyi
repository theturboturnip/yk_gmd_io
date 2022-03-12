"""


Path Utilities (bpy.path)
*************************

This module has a similar scope to os.path, containing utility
functions for dealing with paths in Blender.

:func:`abspath`

:func:`basename`

:func:`clean_name`

:func:`display_name`

:func:`display_name_to_filepath`

:func:`display_name_from_filepath`

:func:`ensure_ext`

:func:`is_subdir`

:func:`module_names`

:func:`native_pathsep`

:func:`reduce_dirs`

:func:`relpath`

:func:`resolve_ncase`

"""

import typing

import bpy

def abspath(path: typing.Any, *args, start: str = None, library: bpy.types.Library = None) -> str:

  """

  Returns the absolute path relative to the current blend file
using the "//" prefix.

  """

  ...

def basename(path: typing.Any) -> None:

  """

  Equivalent to ``os.path.basename``, but skips a "//" prefix.

  Use for Windows compatibility.
:return: The base name of the given path.
:rtype: string

  """

  ...

def clean_name(name: typing.Any, *args, replace: typing.Any = '_') -> None:

  """

  Returns a name with characters replaced that
may cause problems under various circumstances,
such as writing to a file.
All characters besides A-Z/a-z, 0-9 are replaced with "_"
or the *replace* argument if defined.
:arg name: The path name.
:type name: string or bytes
:arg replace: The replacement for non-valid characters.
:type replace: string
:return: The cleaned name.
:rtype: string

  """

  ...

def display_name(name: str, *args, has_ext: bool = True, title_case: bool = True) -> str:

  """

  Creates a display string from name to be used menus and the user interface.
Intended for use with filenames and module names.

  """

  ...

def display_name_to_filepath(name: typing.Any) -> None:

  """

  Performs the reverse of display_name using literal versions of characters
which aren't supported in a filepath.
:arg name: The display name to convert.
:type name: string
:return: The file path.
:rtype: string

  """

  ...

def display_name_from_filepath(name: typing.Any) -> None:

  """

  Returns the path stripped of directory and extension,
ensured to be utf8 compatible.
:arg name: The file path to convert.
:type name: string
:return: The display name.
:rtype: string

  """

  ...

def ensure_ext(filepath: str, ext: str, *args, case_sensitive: bool = False) -> str:

  """

  Return the path with the extension added if it is not already set.

  """

  ...

def is_subdir(path: str, directory: typing.Any) -> bool:

  """

  Returns true if *path* in a subdirectory of *directory*.
Both paths must be absolute.

  """

  ...

def module_names(path: str, *args, recursive: bool = False) -> typing.List[str]:

  """

  Return a list of modules which can be imported from *path*.

  """

  ...

def native_pathsep(path: typing.Any) -> None:

  """

  Replace the path separator with the systems native ``os.sep``.
:arg path: The path to replace.
:type path: string
:return: The path with system native separators.
:rtype: string

  """

  ...

def reduce_dirs(dirs: typing.Sequence[str]) -> typing.List[str]:

  """

  Given a sequence of directories, remove duplicates and
any directories nested in one of the other paths.
(Useful for recursive path searching).

  """

  ...

def relpath(path: str, *args, start: str = None) -> str:

  """

  Returns the path relative to the current blend file using the "//" prefix.

  """

  ...

def resolve_ncase(path: typing.Any) -> None:

  """

  Resolve a case insensitive path on a case sensitive system,
returning a string with the path if found else return the original path.
:arg path: The path name to resolve.
:type path: string
:return: The resolved path.
:rtype: string

  """

  ...
