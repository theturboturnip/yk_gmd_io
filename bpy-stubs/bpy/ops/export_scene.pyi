"""


Export Scene Operators
**********************

:func:`fbx`

:func:`gltf`

:func:`obj`

:func:`x3d`

"""

import typing

def fbx(filepath: str = '', check_existing: bool = True, filter_glob: str = '*args.fbx', use_selection: bool = False, use_active_collection: bool = False, global_scale: float = 1.0, apply_unit_scale: bool = True, apply_scale_options: str = 'FBX_SCALE_NONE', use_space_transform: bool = True, bake_space_transform: bool = False, object_types: typing.Set[str] = {'ARMATURE', 'CAMERA', 'EMPTY', 'LIGHT', 'MESH', 'OTHER'}, use_mesh_modifiers: bool = True, use_mesh_modifiers_render: bool = True, mesh_smooth_type: str = 'OFF', use_subsurf: bool = False, use_mesh_edges: bool = False, use_tspace: bool = False, use_custom_props: bool = False, add_leaf_bones: bool = True, primary_bone_axis: str = 'Y', secondary_bone_axis: str = 'X', use_armature_deform_only: bool = False, armature_nodetype: str = 'NULL', bake_anim: bool = True, bake_anim_use_all_bones: bool = True, bake_anim_use_nla_strips: bool = True, bake_anim_use_all_actions: bool = True, bake_anim_force_startend_keying: bool = True, bake_anim_step: float = 1.0, bake_anim_simplify_factor: float = 1.0, path_mode: str = 'AUTO', embed_textures: bool = False, batch_mode: str = 'OFF', use_batch_own_dir: bool = True, use_metadata: bool = True, axis_forward: str = '-Z', axis_up: str = 'Y') -> None:

  """

  Write a FBX file

  """

  ...

def gltf(filepath: str = '', check_existing: bool = True, export_format: str = 'GLB', ui_tab: str = 'GENERAL', export_copyright: str = '', export_image_format: str = 'AUTO', export_texture_dir: str = '', export_keep_originals: bool = False, export_texcoords: bool = True, export_normals: bool = True, export_draco_mesh_compression_enable: bool = False, export_draco_mesh_compression_level: int = 6, export_draco_position_quantization: int = 14, export_draco_normal_quantization: int = 10, export_draco_texcoord_quantization: int = 12, export_draco_color_quantization: int = 10, export_draco_generic_quantization: int = 12, export_tangents: bool = False, export_materials: str = 'EXPORT', export_colors: bool = True, use_mesh_edges: bool = False, use_mesh_vertices: bool = False, export_cameras: bool = False, export_selected: bool = False, use_selection: bool = False, use_visible: bool = False, use_renderable: bool = False, use_active_collection: bool = False, export_extras: bool = False, export_yup: bool = True, export_apply: bool = False, export_animations: bool = True, export_frame_range: bool = True, export_frame_step: int = 1, export_force_sampling: bool = True, export_nla_strips: bool = True, export_def_bones: bool = False, export_current_frame: bool = False, export_skins: bool = True, export_all_influences: bool = False, export_morph: bool = True, export_morph_normal: bool = True, export_morph_tangent: bool = False, export_lights: bool = False, export_displacement: bool = False, will_save_settings: bool = False, filter_glob: str = '*args.glb;*args.gltf') -> None:

  """

  Export scene as glTF 2.0 file

  """

  ...

def obj(filepath: str = '', check_existing: bool = True, filter_glob: str = '*args.obj;*args.mtl', use_selection: bool = False, use_animation: bool = False, use_mesh_modifiers: bool = True, use_edges: bool = True, use_smooth_groups: bool = False, use_smooth_groups_bitflags: bool = False, use_normals: bool = True, use_uvs: bool = True, use_materials: bool = True, use_triangles: bool = False, use_nurbs: bool = False, use_vertex_groups: bool = False, use_blen_objects: bool = True, group_by_object: bool = False, group_by_material: bool = False, keep_vertex_order: bool = False, global_scale: float = 1.0, path_mode: str = 'AUTO', axis_forward: str = '-Z', axis_up: str = 'Y') -> None:

  """

  Save a Wavefront OBJ File

  """

  ...

def x3d(filepath: str = '', check_existing: bool = True, filter_glob: str = '*args.x3d', use_selection: bool = False, use_mesh_modifiers: bool = True, use_triangulate: bool = False, use_normals: bool = False, use_compress: bool = False, use_hierarchy: bool = True, name_decorations: bool = True, use_h3d: bool = False, global_scale: float = 1.0, path_mode: str = 'AUTO', axis_forward: str = 'Z', axis_up: str = 'Y') -> None:

  """

  Export selection to Extensible 3D file (.x3d)

  """

  ...
