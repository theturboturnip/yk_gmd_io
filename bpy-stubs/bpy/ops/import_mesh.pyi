"""


Import Mesh Operators
*********************

:func:`ply`

:func:`stl`

"""

import typing

def ply(filepath: str = '', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, hide_props_region: bool = True, directory: str = '', filter_glob: str = '*args.ply') -> None:

  """

  Load a PLY geometry file

  """

  ...

def stl(filepath: str = '', filter_glob: str = '*args.stl', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, directory: str = '', global_scale: float = 1.0, use_scene_unit: bool = False, use_facet_normal: bool = False, axis_forward: str = 'Y', axis_up: str = 'Z') -> None:

  """

  Load STL triangle mesh data

  """

  ...
