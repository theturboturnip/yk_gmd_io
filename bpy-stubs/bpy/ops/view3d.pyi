"""


View3D Operators
****************

:func:`background_image_add`

:func:`background_image_remove`

:func:`bone_select_menu`

:func:`camera_to_view`

:func:`camera_to_view_selected`

:func:`clear_render_border`

:func:`clip_border`

:func:`copybuffer`

:func:`cursor3d`

:func:`dolly`

:func:`drop_world`

:func:`edit_mesh_extrude_individual_move`

:func:`edit_mesh_extrude_manifold_normal`

:func:`edit_mesh_extrude_move_normal`

:func:`edit_mesh_extrude_move_shrink_fatten`

:func:`fly`

:func:`interactive_add`

:func:`localview`

:func:`localview_remove_from`

:func:`move`

:func:`navigate`

:func:`ndof_all`

:func:`ndof_orbit`

:func:`ndof_orbit_zoom`

:func:`ndof_pan`

:func:`object_as_camera`

:func:`object_mode_pie_or_toggle`

:func:`pastebuffer`

:func:`render_border`

:func:`rotate`

:func:`ruler_add`

:func:`ruler_remove`

:func:`select`

:func:`select_box`

:func:`select_circle`

:func:`select_lasso`

:func:`select_menu`

:func:`smoothview`

:func:`snap_cursor_to_active`

:func:`snap_cursor_to_center`

:func:`snap_cursor_to_grid`

:func:`snap_cursor_to_selected`

:func:`snap_selected_to_active`

:func:`snap_selected_to_cursor`

:func:`snap_selected_to_grid`

:func:`toggle_matcap_flip`

:func:`toggle_shading`

:func:`toggle_xray`

:func:`transform_gizmo_set`

:func:`view_all`

:func:`view_axis`

:func:`view_camera`

:func:`view_center_camera`

:func:`view_center_cursor`

:func:`view_center_lock`

:func:`view_center_pick`

:func:`view_lock_clear`

:func:`view_lock_to_active`

:func:`view_orbit`

:func:`view_pan`

:func:`view_persportho`

:func:`view_roll`

:func:`view_selected`

:func:`walk`

:func:`zoom`

:func:`zoom_border`

:func:`zoom_camera_1_to_1`

"""

import typing

def background_image_add(name: str = 'Image', filepath: str = '', hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = True, filter_movie: bool = True, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Add a new background image

  """

  ...

def background_image_remove(index: int = 0) -> None:

  """

  Remove a background image from the 3D view

  """

  ...

def bone_select_menu(name: str = '', extend: bool = False, deselect: bool = False, toggle: bool = False) -> None:

  """

  Menu bone selection

  """

  ...

def camera_to_view() -> None:

  """

  Set camera view to active view

  """

  ...

def camera_to_view_selected() -> None:

  """

  Move the camera so selected objects are framed

  """

  ...

def clear_render_border() -> None:

  """

  Clear the boundaries of the border render and disable border render

  """

  ...

def clip_border(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True) -> None:

  """

  Set the view clipping region

  """

  ...

def copybuffer() -> None:

  """

  Selected objects are copied to the clipboard

  """

  ...

def cursor3d(use_depth: bool = True, orientation: str = 'VIEW') -> None:

  """

  Set the location of the 3D cursor

  """

  ...

def dolly(mx: int = 0, my: int = 0, delta: int = 0, use_cursor_init: bool = True) -> None:

  """

  Dolly in/out in the view

  """

  ...

def drop_world(name: str = 'World') -> None:

  """

  Drop a world into the scene

  """

  ...

def edit_mesh_extrude_individual_move() -> None:

  """

  Extrude each individual face separately along local normals

  """

  ...

def edit_mesh_extrude_manifold_normal() -> None:

  """

  Extrude manifold region along normals

  """

  ...

def edit_mesh_extrude_move_normal(dissolve_and_intersect: bool = False) -> None:

  """

  Extrude region together along the average normal

  """

  ...

def edit_mesh_extrude_move_shrink_fatten() -> None:

  """

  Extrude region together along local normals

  """

  ...

def fly() -> None:

  """

  Interactively fly around the scene

  """

  ...

def interactive_add(primitive_type: str = 'CUBE', plane_axis: str = 'Z', plane_axis_auto: bool = False, plane_depth: str = 'SURFACE', plane_orientation: str = 'SURFACE', snap_target: str = 'GEOMETRY', plane_origin_base: str = 'EDGE', plane_origin_depth: str = 'EDGE', plane_aspect_base: str = 'FREE', plane_aspect_depth: str = 'FREE', wait_for_input: bool = True) -> None:

  """

  Interactively add an object

  """

  ...

def localview(frame_selected: bool = True) -> None:

  """

  Toggle display of selected object(s) separately and centered in view

  """

  ...

def localview_remove_from() -> None:

  """

  Move selected objects out of local view

  """

  ...

def move(use_cursor_init: bool = True) -> None:

  """

  Move the view

  """

  ...

def navigate() -> None:

  """

  Interactively navigate around the scene (uses the mode (walk/fly) preference)

  """

  ...

def ndof_all() -> None:

  """

  Pan and rotate the view with the 3D mouse

  """

  ...

def ndof_orbit() -> None:

  """

  Orbit the view using the 3D mouse

  """

  ...

def ndof_orbit_zoom() -> None:

  """

  Orbit and zoom the view using the 3D mouse

  """

  ...

def ndof_pan() -> None:

  """

  Pan the view with the 3D mouse

  """

  ...

def object_as_camera() -> None:

  """

  Set the active object as the active camera for this view or scene

  """

  ...

def object_mode_pie_or_toggle() -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def pastebuffer(autoselect: bool = True, active_collection: bool = True) -> None:

  """

  Objects from the clipboard are pasted

  """

  ...

def render_border(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True) -> None:

  """

  Set the boundaries of the border render and enable border render

  """

  ...

def rotate(use_cursor_init: bool = True) -> None:

  """

  Rotate the view

  """

  ...

def ruler_add() -> None:

  """

  Add ruler

  """

  ...

def ruler_remove() -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def select(extend: bool = False, deselect: bool = False, toggle: bool = False, deselect_all: bool = False, center: bool = False, enumerate: bool = False, object: bool = False, location: typing.Tuple[int, int] = (0, 0)) -> None:

  """

  Select and activate item(s)

  """

  ...

def select_box(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Select items using box selection

  """

  ...

def select_circle(x: int = 0, y: int = 0, radius: int = 25, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Select items using circle selection

  """

  ...

def select_lasso(path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None, mode: str = 'SET') -> None:

  """

  Select items using lasso selection

  """

  ...

def select_menu(name: str = '', extend: bool = False, deselect: bool = False, toggle: bool = False) -> None:

  """

  Menu object selection

  """

  ...

def smoothview() -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def snap_cursor_to_active() -> None:

  """

  Snap 3D cursor to the active item

  """

  ...

def snap_cursor_to_center() -> None:

  """

  Snap 3D cursor to the world origin

  """

  ...

def snap_cursor_to_grid() -> None:

  """

  Snap 3D cursor to the nearest grid division

  """

  ...

def snap_cursor_to_selected() -> None:

  """

  Snap 3D cursor to the middle of the selected item(s)

  """

  ...

def snap_selected_to_active() -> None:

  """

  Snap selected item(s) to the active item

  """

  ...

def snap_selected_to_cursor(use_offset: bool = True) -> None:

  """

  Snap selected item(s) to the 3D cursor

  """

  ...

def snap_selected_to_grid() -> None:

  """

  Snap selected item(s) to their nearest grid division

  """

  ...

def toggle_matcap_flip() -> None:

  """

  Flip MatCap

  """

  ...

def toggle_shading(type: str = 'WIREFRAME') -> None:

  """

  Toggle shading type in 3D viewport

  """

  ...

def toggle_xray() -> None:

  """

  Transparent scene display. Allow selecting through items

  """

  ...

def transform_gizmo_set(extend: bool = False, type: typing.Set[str] = {}) -> None:

  """

  Set the current transform gizmo

  """

  ...

def view_all(use_all_regions: bool = False, center: bool = False) -> None:

  """

  View all objects in scene

  """

  ...

def view_axis(type: str = 'LEFT', align_active: bool = False, relative: bool = False) -> None:

  """

  Use a preset viewpoint

  """

  ...

def view_camera() -> None:

  """

  Toggle the camera view

  """

  ...

def view_center_camera() -> None:

  """

  Center the camera view, resizing the view to fit its bounds

  """

  ...

def view_center_cursor() -> None:

  """

  Center the view so that the cursor is in the middle of the view

  """

  ...

def view_center_lock() -> None:

  """

  Center the view lock offset

  """

  ...

def view_center_pick() -> None:

  """

  Center the view to the Z-depth position under the mouse cursor

  """

  ...

def view_lock_clear() -> None:

  """

  Clear all view locking

  """

  ...

def view_lock_to_active() -> None:

  """

  Lock the view to the active object/bone

  """

  ...

def view_orbit(angle: float = 0.0, type: str = 'ORBITLEFT') -> None:

  """

  Orbit the view

  """

  ...

def view_pan(type: str = 'PANLEFT') -> None:

  """

  Pan the view in a given direction

  """

  ...

def view_persportho() -> None:

  """

  Switch the current view from perspective/orthographic projection

  """

  ...

def view_roll(angle: float = 0.0, type: str = 'ANGLE') -> None:

  """

  Roll the view

  """

  ...

def view_selected(use_all_regions: bool = False) -> None:

  """

  Move the view to the selection center

  """

  ...

def walk() -> None:

  """

  Interactively walk around the scene

  """

  ...

def zoom(mx: int = 0, my: int = 0, delta: int = 0, use_cursor_init: bool = True) -> None:

  """

  Zoom in/out in the view

  """

  ...

def zoom_border(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, zoom_out: bool = False) -> None:

  """

  Zoom in the view to the nearest object contained in the border

  """

  ...

def zoom_camera_1_to_1() -> None:

  """

  Match the camera to 1:1 to the render output

  """

  ...
