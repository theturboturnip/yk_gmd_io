"""


Export Mesh Operators
*********************

:func:`ply`

:func:`stl`

"""

import typing

def ply(filepath: str = '', check_existing: bool = True, filter_glob: str = '*args.ply', use_ascii: bool = False, use_selection: bool = False, use_mesh_modifiers: bool = True, use_normals: bool = True, use_uv_coords: bool = True, use_colors: bool = True, global_scale: float = 1.0, axis_forward: str = 'Y', axis_up: str = 'Z') -> None:

  """

  Export as a Stanford PLY with normals, vertex colors and texture coordinates

  """

  ...

def stl(filepath: str = '', check_existing: bool = True, filter_glob: str = '*args.stl', use_selection: bool = False, global_scale: float = 1.0, use_scene_unit: bool = False, ascii: bool = False, use_mesh_modifiers: bool = True, batch_mode: str = 'OFF', axis_forward: str = 'Y', axis_up: str = 'Z') -> None:

  """

  Save STL triangle mesh data

  """

  ...
