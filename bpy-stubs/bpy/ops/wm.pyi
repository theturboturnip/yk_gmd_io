"""


Wm Operators
************

:func:`alembic_export`

:func:`alembic_import`

:func:`append`

:func:`batch_rename`

:func:`blend_strings_utf8_validate`

:func:`call_menu`

:func:`call_menu_pie`

:func:`call_panel`

:func:`collada_export`

:func:`collada_import`

:func:`context_collection_boolean_set`

:func:`context_cycle_array`

:func:`context_cycle_enum`

:func:`context_cycle_int`

:func:`context_menu_enum`

:func:`context_modal_mouse`

:func:`context_pie_enum`

:func:`context_scale_float`

:func:`context_scale_int`

:func:`context_set_boolean`

:func:`context_set_enum`

:func:`context_set_float`

:func:`context_set_id`

:func:`context_set_int`

:func:`context_set_string`

:func:`context_set_value`

:func:`context_toggle`

:func:`context_toggle_enum`

:func:`debug_menu`

:func:`doc_view`

:func:`doc_view_manual`

:func:`doc_view_manual_ui_context`

:func:`drop_blend_file`

:func:`gpencil_export_pdf`

:func:`gpencil_export_svg`

:func:`gpencil_import_svg`

:func:`interface_theme_preset_add`

:func:`keyconfig_preset_add`

:func:`lib_reload`

:func:`lib_relocate`

:func:`link`

:func:`memory_statistics`

:func:`open_mainfile`

:func:`operator_cheat_sheet`

:func:`operator_defaults`

:func:`operator_pie_enum`

:func:`operator_preset_add`

:func:`owner_disable`

:func:`owner_enable`

:func:`path_open`

:func:`previews_batch_clear`

:func:`previews_batch_generate`

:func:`previews_clear`

:func:`previews_ensure`

:func:`properties_add`

:func:`properties_context_change`

:func:`properties_edit`

:func:`properties_edit_value`

:func:`properties_remove`

:func:`quit_blender`

:func:`radial_control`

:func:`read_factory_settings`

:func:`read_factory_userpref`

:func:`read_history`

:func:`read_homefile`

:func:`read_userpref`

:func:`recover_auto_save`

:func:`recover_last_session`

:func:`redraw_timer`

:func:`revert_mainfile`

:func:`save_as_mainfile`

:func:`save_homefile`

:func:`save_mainfile`

:func:`save_userpref`

:func:`search_menu`

:func:`search_operator`

:func:`set_stereo_3d`

:func:`splash`

:func:`splash_about`

:func:`sysinfo`

:func:`tool_set_by_id`

:func:`tool_set_by_index`

:func:`toolbar`

:func:`toolbar_fallback_pie`

:func:`toolbar_prompt`

:func:`url_open`

:func:`url_open_preset`

:func:`usd_export`

:func:`usd_import`

:func:`window_close`

:func:`window_fullscreen_toggle`

:func:`window_new`

:func:`window_new_main`

:func:`xr_navigation_fly`

:func:`xr_navigation_grab`

:func:`xr_navigation_reset`

:func:`xr_navigation_teleport`

:func:`xr_session_toggle`

"""

import typing

def alembic_export(filepath: str = '', check_existing: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = True, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, display_type: str = 'DEFAULT', sort_method: str = '', start: int = -2147483648, end: int = -2147483648, xsamples: int = 1, gsamples: int = 1, sh_open: float = 0.0, sh_close: float = 1.0, selected: bool = False, visible_objects_only: bool = False, flatten: bool = False, uvs: bool = True, packuv: bool = True, normals: bool = True, vcolors: bool = False, orcos: bool = True, face_sets: bool = False, subdiv_schema: bool = False, apply_subdiv: bool = False, curves_as_mesh: bool = False, use_instancing: bool = True, global_scale: float = 1.0, triangulate: bool = False, quad_method: str = 'SHORTEST_DIAGONAL', ngon_method: str = 'BEAUTY', export_hair: bool = True, export_particles: bool = True, export_custom_properties: bool = True, as_background_job: bool = False, evaluation_mode: str = 'RENDER', init_scene_frame_range: bool = False) -> None:

  """

  Export current scene in an Alembic archive

  """

  ...

def alembic_import(filepath: str = '', filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = True, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, relative_path: bool = True, display_type: str = 'DEFAULT', sort_method: str = '', scale: float = 1.0, set_frame_range: bool = True, validate_meshes: bool = False, always_add_cache_reader: bool = False, is_sequence: bool = False, as_background_job: bool = False) -> None:

  """

  Load an Alembic archive

  """

  ...

def append(filepath: str = '', directory: str = '', filename: str = '', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, filter_blender: bool = True, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = True, filemode: int = 1, display_type: str = 'DEFAULT', sort_method: str = '', link: bool = False, do_reuse_local_id: bool = False, autoselect: bool = True, active_collection: bool = True, instance_collections: bool = False, instance_object_data: bool = True, set_fake: bool = False, use_recursive: bool = True) -> None:

  """

  Append from a Library .blend file

  """

  ...

def batch_rename(data_type: str = 'OBJECT', data_source: str = 'SELECT', actions: typing.Union[typing.Sequence[BatchRenameAction], typing.Mapping[str, BatchRenameAction], bpy.types.bpy_prop_collection] = None) -> None:

  """

  Rename multiple items at once

  """

  ...

def blend_strings_utf8_validate() -> None:

  """

  Check and fix all strings in current .blend file to be valid UTF-8 Unicode (needed for some old, 2.4x area files)

  """

  ...

def call_menu(name: str = '') -> None:

  """

  Open a predefined menu

  """

  ...

def call_menu_pie(name: str = '') -> None:

  """

  Open a predefined pie menu

  """

  ...

def call_panel(name: str = '', keep_open: bool = True) -> None:

  """

  Open a predefined panel

  """

  ...

def collada_export(filepath: str = '', check_existing: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = True, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, display_type: str = 'DEFAULT', sort_method: str = '', prop_bc_export_ui_section: str = 'main', apply_modifiers: bool = False, export_mesh_type: int = 0, export_mesh_type_selection: str = 'view', export_global_forward_selection: str = 'Y', export_global_up_selection: str = 'Z', apply_global_orientation: bool = False, selected: bool = False, include_children: bool = False, include_armatures: bool = False, include_shapekeys: bool = False, deform_bones_only: bool = False, include_animations: bool = True, include_all_actions: bool = True, export_animation_type_selection: str = 'sample', sampling_rate: int = 1, keep_smooth_curves: bool = False, keep_keyframes: bool = False, keep_flat_curves: bool = False, active_uv_only: bool = False, use_texture_copies: bool = True, triangulate: bool = True, use_object_instantiation: bool = True, use_blender_profile: bool = True, sort_by_name: bool = False, export_object_transformation_type: int = 0, export_object_transformation_type_selection: str = 'matrix', export_animation_transformation_type: int = 0, export_animation_transformation_type_selection: str = 'matrix', open_sim: bool = False, limit_precision: bool = False, keep_bind_info: bool = False) -> None:

  """

  Save a Collada file

  """

  ...

def collada_import(filepath: str = '', filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = True, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, display_type: str = 'DEFAULT', sort_method: str = '', import_units: bool = False, fix_orientation: bool = False, find_chains: bool = False, auto_connect: bool = False, min_chain_length: int = 0, keep_bind_info: bool = False) -> None:

  """

  Load a Collada file

  """

  ...

def context_collection_boolean_set(data_path_iter: str = '', data_path_item: str = '', type: str = 'TOGGLE') -> None:

  """

  Set boolean values for a collection of items

  """

  ...

def context_cycle_array(data_path: str = '', reverse: bool = False) -> None:

  """

  Set a context array value (useful for cycling the active mesh edit mode)

  """

  ...

def context_cycle_enum(data_path: str = '', reverse: bool = False, wrap: bool = False) -> None:

  """

  Toggle a context value

  """

  ...

def context_cycle_int(data_path: str = '', reverse: bool = False, wrap: bool = False) -> None:

  """

  Set a context value (useful for cycling active material, vertex keys, groups, etc.)

  """

  ...

def context_menu_enum(data_path: str = '') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def context_modal_mouse(data_path_iter: str = '', data_path_item: str = '', header_text: str = '', input_scale: float = 0.01, invert: bool = False, initial_x: int = 0) -> None:

  """

  Adjust arbitrary values with mouse input

  """

  ...

def context_pie_enum(data_path: str = '') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def context_scale_float(data_path: str = '', value: float = 1.0) -> None:

  """

  Scale a float context value

  """

  ...

def context_scale_int(data_path: str = '', value: float = 1.0, always_step: bool = True) -> None:

  """

  Scale an int context value

  """

  ...

def context_set_boolean(data_path: str = '', value: bool = True) -> None:

  """

  Set a context value

  """

  ...

def context_set_enum(data_path: str = '', value: str = '') -> None:

  """

  Set a context value

  """

  ...

def context_set_float(data_path: str = '', value: float = 0.0, relative: bool = False) -> None:

  """

  Set a context value

  """

  ...

def context_set_id(data_path: str = '', value: str = '') -> None:

  """

  Set a context value to an ID data-block

  """

  ...

def context_set_int(data_path: str = '', value: int = 0, relative: bool = False) -> None:

  """

  Set a context value

  """

  ...

def context_set_string(data_path: str = '', value: str = '') -> None:

  """

  Set a context value

  """

  ...

def context_set_value(data_path: str = '', value: str = '') -> None:

  """

  Set a context value

  """

  ...

def context_toggle(data_path: str = '', module: str = '') -> None:

  """

  Toggle a context value

  """

  ...

def context_toggle_enum(data_path: str = '', value_1: str = '', value_2: str = '') -> None:

  """

  Toggle a context value

  """

  ...

def debug_menu(debug_value: int = 0) -> None:

  """

  Open a popup to set the debug level

  """

  ...

def doc_view(doc_id: str = '') -> None:

  """

  Open online reference docs in a web browser

  """

  ...

def doc_view_manual(doc_id: str = '') -> None:

  """

  Load online manual

  """

  ...

def doc_view_manual_ui_context() -> None:

  """

  View a context based online manual in a web browser

  """

  ...

def drop_blend_file(filepath: str = '') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def gpencil_export_pdf(filepath: str = '', check_existing: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = False, filter_blenlib: bool = False, filemode: int = 8, display_type: str = 'DEFAULT', sort_method: str = '', use_fill: bool = True, selected_object_type: str = 'SELECTED', stroke_sample: float = 0.0, use_normalized_thickness: bool = False, frame_mode: str = 'ACTIVE') -> None:

  """

  Export grease pencil to PDF

  """

  ...

def gpencil_export_svg(filepath: str = '', check_existing: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = False, filter_blenlib: bool = False, filemode: int = 8, display_type: str = 'DEFAULT', sort_method: str = '', use_fill: bool = True, selected_object_type: str = 'SELECTED', stroke_sample: float = 0.0, use_normalized_thickness: bool = False, use_clip_camera: bool = False) -> None:

  """

  Export grease pencil to SVG

  """

  ...

def gpencil_import_svg(filepath: str = '', filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = False, filter_blenlib: bool = False, filemode: int = 8, relative_path: bool = True, display_type: str = 'DEFAULT', sort_method: str = '', resolution: int = 10, scale: float = 10.0) -> None:

  """

  Import SVG into grease pencil

  """

  ...

def interface_theme_preset_add(name: str = '', remove_name: bool = False, remove_active: bool = False) -> None:

  """

  Add or remove a theme preset

  """

  ...

def keyconfig_preset_add(name: str = '', remove_name: bool = False, remove_active: bool = False) -> None:

  """

  Add or remove a Key-config Preset

  """

  ...

def lib_reload(library: str = '', filepath: str = '', directory: str = '', filename: str = '', hide_props_region: bool = True, filter_blender: bool = True, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, relative_path: bool = True, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Reload the given library

  """

  ...

def lib_relocate(library: str = '', filepath: str = '', directory: str = '', filename: str = '', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, hide_props_region: bool = True, filter_blender: bool = True, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, relative_path: bool = True, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Relocate the given library to one or several others

  """

  ...

def link(filepath: str = '', directory: str = '', filename: str = '', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, filter_blender: bool = True, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = True, filemode: int = 1, relative_path: bool = True, display_type: str = 'DEFAULT', sort_method: str = '', link: bool = True, do_reuse_local_id: bool = False, autoselect: bool = True, active_collection: bool = True, instance_collections: bool = True, instance_object_data: bool = True) -> None:

  """

  Link from a Library .blend file

  """

  ...

def memory_statistics() -> None:

  """

  Print memory statistics to the console

  """

  ...

def open_mainfile(filepath: str = '', hide_props_region: bool = True, filter_blender: bool = True, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, display_type: str = 'DEFAULT', sort_method: str = '', load_ui: bool = True, use_scripts: bool = True, display_file_selector: bool = True, state: int = 0) -> None:

  """

  Open a Blender file

  """

  ...

def operator_cheat_sheet() -> None:

  """

  List all the operators in a text-block, useful for scripting

  """

  ...

def operator_defaults() -> None:

  """

  Set the active operator to its default values

  """

  ...

def operator_pie_enum(data_path: str = '', prop_string: str = '') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def operator_preset_add(name: str = '', remove_name: bool = False, remove_active: bool = False, operator: str = '') -> None:

  """

  Add or remove an Operator Preset

  """

  ...

def owner_disable(owner_id: str = '') -> None:

  """

  Enable workspace owner ID

  """

  ...

def owner_enable(owner_id: str = '') -> None:

  """

  Enable workspace owner ID

  """

  ...

def path_open(filepath: str = '') -> None:

  """

  Open a path in a file browser

  """

  ...

def previews_batch_clear(files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, directory: str = '', filter_blender: bool = True, filter_folder: bool = True, use_scenes: bool = True, use_collections: bool = True, use_objects: bool = True, use_intern_data: bool = True, use_trusted: bool = False, use_backups: bool = True) -> None:

  """

  Clear selected .blend file's previews

  """

  ...

def previews_batch_generate(files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, directory: str = '', filter_blender: bool = True, filter_folder: bool = True, use_scenes: bool = True, use_collections: bool = True, use_objects: bool = True, use_intern_data: bool = True, use_trusted: bool = False, use_backups: bool = True) -> None:

  """

  Generate selected .blend file's previews

  """

  ...

def previews_clear(id_type: typing.Set[str] = {}) -> None:

  """

  Clear data-block previews (only for some types like objects, materials, textures, etc.)

  """

  ...

def previews_ensure() -> None:

  """

  Ensure data-block previews are available and up-to-date (to be saved in .blend file, only for some types like materials, textures, etc.)

  """

  ...

def properties_add(data_path: str = '') -> None:

  """

  Add your own property to the data-block

  """

  ...

def properties_context_change(context: str = '') -> None:

  """

  Jump to a different tab inside the properties editor

  """

  ...

def properties_edit(data_path: str = '', property_name: str = '', property_type: str = 'FLOAT', is_overridable_library: bool = False, description: str = '', use_soft_limits: bool = False, array_length: int = 3, default_int: typing.Tuple[int, ...] = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), min_int: int = -10000, max_int: int = 10000, soft_min_int: int = -10000, soft_max_int: int = 10000, step_int: int = 1, default_float: typing.Tuple[float, ...] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), min_float: float = -10000, max_float: float = -10000, soft_min_float: float = -10000, soft_max_float: float = -10000, precision: int = 3, step_float: float = 0.1, subtype: str = '', default_string: str = '', eval_string: str = '') -> None:

  """

  Change a custom property's type, or adjust how it is displayed in the interface

  """

  ...

def properties_edit_value(data_path: str = '', property_name: str = '', eval_string: str = '') -> None:

  """

  Edit the value of a custom property

  """

  ...

def properties_remove(data_path: str = '', property_name: str = '') -> None:

  """

  Internal use (edit a property data_path)

  """

  ...

def quit_blender() -> None:

  """

  Quit Blender

  """

  ...

def radial_control(data_path_primary: str = '', data_path_secondary: str = '', use_secondary: str = '', rotation_path: str = '', color_path: str = '', fill_color_path: str = '', fill_color_override_path: str = '', fill_color_override_test_path: str = '', zoom_path: str = '', image_id: str = '', secondary_tex: bool = False, release_confirm: bool = False) -> None:

  """

  Set some size property (e.g. brush size) with mouse wheel

  """

  ...

def read_factory_settings(app_template: str = 'Template', use_empty: bool = False) -> None:

  """

  Load factory default startup file and preferences. To make changes permanent, use "Save Startup File" and "Save Preferences"

  """

  ...

def read_factory_userpref() -> None:

  """

  Load factory default preferences. To make changes to preferences permanent, use "Save Preferences"

  """

  ...

def read_history() -> None:

  """

  Reloads history and bookmarks

  """

  ...

def read_homefile(filepath: str = '', load_ui: bool = True, use_splash: bool = False, use_factory_startup: bool = False, app_template: str = 'Template', use_empty: bool = False) -> None:

  """

  Open the default file (doesn't save the current file)

  """

  ...

def read_userpref() -> None:

  """

  Load last saved preferences

  """

  ...

def recover_auto_save(filepath: str = '', hide_props_region: bool = True, filter_blender: bool = True, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = False, filter_blenlib: bool = False, filemode: int = 8, display_type: str = 'LIST_VERTICAL', sort_method: str = '', use_scripts: bool = True) -> None:

  """

  Open an automatically saved file to recover it

  """

  ...

def recover_last_session(use_scripts: bool = True) -> None:

  """

  Open the last closed file ("quit.blend")

  """

  ...

def redraw_timer(type: str = 'DRAW', iterations: int = 10, time_limit: float = 0.0) -> None:

  """

  Simple redraw timer to test the speed of updating the interface

  """

  ...

def revert_mainfile(use_scripts: bool = True) -> None:

  """

  Reload the saved file

  """

  ...

def save_as_mainfile(filepath: str = '', hide_props_region: bool = True, check_existing: bool = True, filter_blender: bool = True, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, display_type: str = 'DEFAULT', sort_method: str = '', compress: bool = False, relative_remap: bool = True, copy: bool = False) -> None:

  """

  Save the current file in the desired location

  """

  ...

def save_homefile() -> None:

  """

  Make the current file the default .blend file

  """

  ...

def save_mainfile(filepath: str = '', hide_props_region: bool = True, check_existing: bool = True, filter_blender: bool = True, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, display_type: str = 'DEFAULT', sort_method: str = '', compress: bool = False, relative_remap: bool = False, exit: bool = False) -> None:

  """

  Save the current Blender file

  """

  ...

def save_userpref() -> None:

  """

  Make the current preferences default

  """

  ...

def search_menu() -> None:

  """

  Pop-up a search over all menus in the current context

  """

  ...

def search_operator() -> None:

  """

  Pop-up a search over all available operators in current context

  """

  ...

def set_stereo_3d(display_mode: str = 'ANAGLYPH', anaglyph_type: str = 'RED_CYAN', interlace_type: str = 'ROW_INTERLEAVED', use_interlace_swap: bool = False, use_sidebyside_crosseyed: bool = False) -> None:

  """

  Toggle 3D stereo support for current window (or change the display mode)

  """

  ...

def splash() -> None:

  """

  Open the splash screen with release info

  """

  ...

def splash_about() -> None:

  """

  Open a window with information about Blender

  """

  ...

def sysinfo(filepath: str = '') -> None:

  """

  Generate system information, saved into a text file

  """

  ...

def tool_set_by_id(name: str = '', cycle: bool = False, as_fallback: bool = False, space_type: str = 'EMPTY') -> None:

  """

  Set the tool by name (for keymaps)

  """

  ...

def tool_set_by_index(index: int = 0, cycle: bool = False, expand: bool = True, as_fallback: bool = False, space_type: str = 'EMPTY') -> None:

  """

  Set the tool by index (for keymaps)

  """

  ...

def toolbar() -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def toolbar_fallback_pie() -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def toolbar_prompt() -> None:

  """

  Leader key like functionality for accessing tools

  """

  ...

def url_open(url: str = '') -> None:

  """

  Open a website in the web browser

  """

  ...

def url_open_preset(type: str = '', id: str = '') -> None:

  """

  Open a preset website in the web browser

  """

  ...

def usd_export(filepath: str = '', check_existing: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = True, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, display_type: str = 'DEFAULT', sort_method: str = '', selected_objects_only: bool = False, visible_objects_only: bool = True, export_animation: bool = False, export_hair: bool = False, export_uvmaps: bool = True, export_normals: bool = True, export_materials: bool = True, use_instancing: bool = False, evaluation_mode: str = 'RENDER') -> None:

  """

  Export current scene in a USD archive

  """

  ...

def usd_import(filepath: str = '', filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = True, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, relative_path: bool = True, display_type: str = 'DEFAULT', sort_method: str = '', scale: float = 1.0, set_frame_range: bool = True, import_cameras: bool = True, import_curves: bool = True, import_lights: bool = True, import_materials: bool = True, import_meshes: bool = True, import_volumes: bool = True, import_subdiv: bool = False, import_instance_proxies: bool = True, import_visible_only: bool = True, create_collection: bool = False, read_mesh_uvs: bool = True, read_mesh_colors: bool = False, prim_path_mask: str = '', import_guide: bool = False, import_proxy: bool = True, import_render: bool = True, import_usd_preview: bool = False, set_material_blend: bool = True, light_intensity_scale: float = 1.0) -> None:

  """

  Import USD stage into current scene

  """

  ...

def window_close() -> None:

  """

  Close the current window

  """

  ...

def window_fullscreen_toggle() -> None:

  """

  Toggle the current window fullscreen

  """

  ...

def window_new() -> None:

  """

  Create a new window

  """

  ...

def window_new_main() -> None:

  """

  Create a new main window with its own workspace and scene selection

  """

  ...

def xr_navigation_fly(mode: str = 'VIEWER_FORWARD', lock_location_z: bool = False, lock_direction: bool = False, speed_frame_based: bool = True, speed_min: float = 0.018, speed_max: float = 0.054, speed_interpolation0: typing.Tuple[float, float] = (0.0, 0.0), speed_interpolation1: typing.Tuple[float, float] = (1.0, 1.0)) -> None:

  """

  Move/turn relative to the VR viewer or controller

  """

  ...

def xr_navigation_grab(lock_location: bool = False, lock_location_z: bool = False, lock_rotation: bool = False, lock_rotation_z: bool = False, lock_scale: bool = False) -> None:

  """

  Navigate the VR scene by grabbing with controllers

  """

  ...

def xr_navigation_reset(location: bool = True, rotation: bool = True, scale: bool = True) -> None:

  """

  Reset VR navigation deltas relative to session base pose

  """

  ...

def xr_navigation_teleport(teleport_axes: typing.Tuple[bool, bool, bool] = (True, True, True), interpolation: float = 1.0, offset: float = 0.0, selectable_only: bool = True, distance: float = 1.70141e+38, from_viewer: bool = False, axis: typing.Tuple[float, float, float] = (0.0, 0.0, -1), color: typing.Tuple[float, float, float, float] = (0.35, 0.35, 1.0, 1.0)) -> None:

  """

  Set VR viewer location to controller raycast hit location

  """

  ...

def xr_session_toggle() -> None:

  """

  Open a view for use with virtual reality headsets, or close it if already opened

  """

  ...
