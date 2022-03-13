"""


Import Scene Operators
**********************

:func:`fbx`

:func:`gltf`

:func:`obj`

:func:`x3d`

"""

import typing

def fbx(filepath: str = '', directory: str = '', filter_glob: str = '*args.fbx', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, ui_tab: str = 'MAIN', use_manual_orientation: bool = False, global_scale: float = 1.0, bake_space_transform: bool = False, use_custom_normals: bool = True, use_image_search: bool = True, use_alpha_decals: bool = False, decal_offset: float = 0.0, use_anim: bool = True, anim_offset: float = 1.0, use_subsurf: bool = False, use_custom_props: bool = True, use_custom_props_enum_as_string: bool = True, ignore_leaf_bones: bool = False, force_connect_children: bool = False, automatic_bone_orientation: bool = False, primary_bone_axis: str = 'Y', secondary_bone_axis: str = 'X', use_prepost_rot: bool = True, axis_forward: str = '-Z', axis_up: str = 'Y') -> None:

  """

  Load a FBX file

  """

  ...

def gltf(filepath: str = '', filter_glob: str = '*args.glb;*args.gltf', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, loglevel: int = 0, import_pack_images: bool = True, merge_vertices: bool = False, import_shading: str = 'NORMALS', bone_heuristic: str = 'TEMPERANCE', guess_original_bind_pose: bool = True) -> None:

  """

  Load a glTF 2.0 file

  """

  ...

def obj(filepath: str = '', filter_glob: str = '*args.obj;*args.mtl', use_edges: bool = True, use_smooth_groups: bool = True, use_split_objects: bool = True, use_split_groups: bool = False, use_groups_as_vgroups: bool = False, use_image_search: bool = True, split_mode: str = 'ON', global_clamp_size: float = 0.0, axis_forward: str = '-Z', axis_up: str = 'Y') -> None:

  """

  Load a Wavefront OBJ File

  """

  ...

def x3d(filepath: str = '', filter_glob: str = '*args.x3d;*args.wrl', axis_forward: str = 'Z', axis_up: str = 'Y') -> None:

  """

  Import an X3D or VRML2 file

  """

  ...
