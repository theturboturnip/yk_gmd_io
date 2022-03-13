"""


Clip Operators
**************

:func:`add_marker`

:func:`add_marker_at_click`

:func:`add_marker_move`

:func:`add_marker_slide`

:func:`apply_solution_scale`

:func:`average_tracks`

:func:`bundles_to_mesh`

:func:`camera_preset_add`

:func:`change_frame`

:func:`clean_tracks`

:func:`clear_solution`

:func:`clear_track_path`

:func:`constraint_to_fcurve`

:func:`copy_tracks`

:func:`create_plane_track`

:func:`cursor_set`

:func:`delete_marker`

:func:`delete_proxy`

:func:`delete_track`

:func:`detect_features`

:func:`disable_markers`

:func:`dopesheet_select_channel`

:func:`dopesheet_view_all`

:func:`filter_tracks`

:func:`frame_jump`

:func:`graph_center_current_frame`

:func:`graph_delete_curve`

:func:`graph_delete_knot`

:func:`graph_disable_markers`

:func:`graph_select`

:func:`graph_select_all_markers`

:func:`graph_select_box`

:func:`graph_view_all`

:func:`hide_tracks`

:func:`hide_tracks_clear`

:func:`join_tracks`

:func:`keyframe_delete`

:func:`keyframe_insert`

:func:`lock_selection_toggle`

:func:`lock_tracks`

:func:`mode_set`

:func:`open`

:func:`paste_tracks`

:func:`prefetch`

:func:`rebuild_proxy`

:func:`refine_markers`

:func:`reload`

:func:`select`

:func:`select_all`

:func:`select_box`

:func:`select_circle`

:func:`select_grouped`

:func:`select_lasso`

:func:`set_active_clip`

:func:`set_axis`

:func:`set_center_principal`

:func:`set_origin`

:func:`set_plane`

:func:`set_scale`

:func:`set_scene_frames`

:func:`set_solution_scale`

:func:`set_solver_keyframe`

:func:`set_viewport_background`

:func:`setup_tracking_scene`

:func:`slide_marker`

:func:`slide_plane_marker`

:func:`solve_camera`

:func:`stabilize_2d_add`

:func:`stabilize_2d_remove`

:func:`stabilize_2d_rotation_add`

:func:`stabilize_2d_rotation_remove`

:func:`stabilize_2d_rotation_select`

:func:`stabilize_2d_select`

:func:`track_color_preset_add`

:func:`track_copy_color`

:func:`track_markers`

:func:`track_settings_as_default`

:func:`track_settings_to_track`

:func:`track_to_empty`

:func:`tracking_object_new`

:func:`tracking_object_remove`

:func:`tracking_settings_preset_add`

:func:`view_all`

:func:`view_center_cursor`

:func:`view_ndof`

:func:`view_pan`

:func:`view_selected`

:func:`view_zoom`

:func:`view_zoom_in`

:func:`view_zoom_out`

:func:`view_zoom_ratio`

"""

import typing

def add_marker(location: typing.Tuple[float, float] = (0.0, 0.0)) -> None:

  """

  Place new marker at specified location

  """

  ...

def add_marker_at_click() -> None:

  """

  Place new marker at the desired (clicked) position

  """

  ...

def add_marker_move(CLIP_OT_add_marker: CLIP_OT_add_marker = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Add new marker and move it on movie

  """

  ...

def add_marker_slide(CLIP_OT_add_marker: CLIP_OT_add_marker = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Add new marker and slide it with mouse until mouse button release

  """

  ...

def apply_solution_scale(distance: float = 0.0) -> None:

  """

  Apply scale on solution itself to make distance between selected tracks equals to desired

  """

  ...

def average_tracks(keep_original: bool = True) -> None:

  """

  Average selected tracks into active

  """

  ...

def bundles_to_mesh() -> None:

  """

  Create vertex cloud using coordinates of reconstructed tracks

  """

  ...

def camera_preset_add(name: str = '', remove_name: bool = False, remove_active: bool = False, use_focal_length: bool = True) -> None:

  """

  Add or remove a Tracking Camera Intrinsics Preset

  """

  ...

def change_frame(frame: int = 0) -> None:

  """

  Interactively change the current frame number

  """

  ...

def clean_tracks(frames: int = 0, error: float = 0.0, action: str = 'SELECT') -> None:

  """

  Clean tracks with high error values or few frames

  """

  ...

def clear_solution() -> None:

  """

  Clear all calculated data

  """

  ...

def clear_track_path(action: str = 'REMAINED', clear_active: bool = False) -> None:

  """

  Clear tracks after/before current position or clear the whole track

  """

  ...

def constraint_to_fcurve() -> None:

  """

  Create F-Curves for object which will copy object's movement caused by this constraint

  """

  ...

def copy_tracks() -> None:

  """

  Copy selected tracks to clipboard

  """

  ...

def create_plane_track() -> None:

  """

  Create new plane track out of selected point tracks

  """

  ...

def cursor_set(location: typing.Tuple[float, float] = (0.0, 0.0)) -> None:

  """

  Set 2D cursor location

  """

  ...

def delete_marker() -> None:

  """

  Delete marker for current frame from selected tracks

  """

  ...

def delete_proxy() -> None:

  """

  Delete movie clip proxy files from the hard drive

  """

  ...

def delete_track() -> None:

  """

  Delete selected tracks

  """

  ...

def detect_features(placement: str = 'FRAME', margin: int = 16, threshold: float = 0.5, min_distance: int = 120) -> None:

  """

  Automatically detect features and place markers to track

  """

  ...

def disable_markers(action: str = 'DISABLE') -> None:

  """

  Disable/enable selected markers

  """

  ...

def dopesheet_select_channel(location: typing.Tuple[float, float] = (0.0, 0.0), extend: bool = False) -> None:

  """

  Select movie tracking channel

  """

  ...

def dopesheet_view_all() -> None:

  """

  Reset viewable area to show full keyframe range

  """

  ...

def filter_tracks(track_threshold: float = 5.0) -> None:

  """

  Filter tracks which has weirdly looking spikes in motion curves

  """

  ...

def frame_jump(position: str = 'PATHSTART') -> None:

  """

  Jump to special frame

  """

  ...

def graph_center_current_frame() -> None:

  """

  Scroll view so current frame would be centered

  """

  ...

def graph_delete_curve() -> None:

  """

  Delete track corresponding to the selected curve

  """

  ...

def graph_delete_knot() -> None:

  """

  Delete curve knots

  """

  ...

def graph_disable_markers(action: str = 'DISABLE') -> None:

  """

  Disable/enable selected markers

  """

  ...

def graph_select(location: typing.Tuple[float, float] = (0.0, 0.0), extend: bool = False) -> None:

  """

  Select graph curves

  """

  ...

def graph_select_all_markers(action: str = 'TOGGLE') -> None:

  """

  Change selection of all markers of active track

  """

  ...

def graph_select_box(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, deselect: bool = False, extend: bool = True) -> None:

  """

  Select curve points using box selection

  """

  ...

def graph_view_all() -> None:

  """

  View all curves in editor

  """

  ...

def hide_tracks(unselected: bool = False) -> None:

  """

  Hide selected tracks

  """

  ...

def hide_tracks_clear() -> None:

  """

  Clear hide selected tracks

  """

  ...

def join_tracks() -> None:

  """

  Join selected tracks

  """

  ...

def keyframe_delete() -> None:

  """

  Delete a keyframe from selected tracks at current frame

  """

  ...

def keyframe_insert() -> None:

  """

  Insert a keyframe to selected tracks at current frame

  """

  ...

def lock_selection_toggle() -> None:

  """

  Toggle Lock Selection option of the current clip editor

  """

  ...

def lock_tracks(action: str = 'LOCK') -> None:

  """

  Lock/unlock selected tracks

  """

  ...

def mode_set(mode: str = 'TRACKING') -> None:

  """

  Set the clip interaction mode

  """

  ...

def open(directory: str = '', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = True, filter_movie: bool = True, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Load a sequence of frames or a movie file

  """

  ...

def paste_tracks() -> None:

  """

  Paste tracks from clipboard

  """

  ...

def prefetch() -> None:

  """

  Prefetch frames from disk for faster playback/tracking

  """

  ...

def rebuild_proxy() -> None:

  """

  Rebuild all selected proxies and timecode indices in the background

  """

  ...

def refine_markers(backwards: bool = False) -> None:

  """

  Refine selected markers positions by running the tracker from track's reference to current frame

  """

  ...

def reload() -> None:

  """

  Reload clip

  """

  ...

def select(extend: bool = False, deselect_all: bool = False, location: typing.Tuple[float, float] = (0.0, 0.0)) -> None:

  """

  Select tracking markers

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Change selection of all tracking markers

  """

  ...

def select_box(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Select markers using box selection

  """

  ...

def select_circle(x: int = 0, y: int = 0, radius: int = 25, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Select markers using circle selection

  """

  ...

def select_grouped(group: str = 'ESTIMATED') -> None:

  """

  Select all tracks from specified group

  """

  ...

def select_lasso(path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None, mode: str = 'SET') -> None:

  """

  Select markers using lasso selection

  """

  ...

def set_active_clip() -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def set_axis(axis: str = 'X') -> None:

  """

  Set direction of scene axis rotating camera (or its parent if present) and assume selected track lies on real axis, joining it with the origin

  """

  ...

def set_center_principal() -> None:

  """

  Set optical center to center of footage

  """

  ...

def set_origin(use_median: bool = False) -> None:

  """

  Set active marker as origin by moving camera (or its parent if present) in 3D space

  """

  ...

def set_plane(plane: str = 'FLOOR') -> None:

  """

  Set plane based on 3 selected bundles by moving camera (or its parent if present) in 3D space

  """

  ...

def set_scale(distance: float = 0.0) -> None:

  """

  Set scale of scene by scaling camera (or its parent if present)

  """

  ...

def set_scene_frames() -> None:

  """

  Set scene's start and end frame to match clip's start frame and length

  """

  ...

def set_solution_scale(distance: float = 0.0) -> None:

  """

  Set object solution scale using distance between two selected tracks

  """

  ...

def set_solver_keyframe(keyframe: str = 'KEYFRAME_A') -> None:

  """

  Set keyframe used by solver

  """

  ...

def set_viewport_background() -> None:

  """

  Set current movie clip as a camera background in 3D Viewport (works only when a 3D Viewport is visible)

  """

  ...

def setup_tracking_scene() -> None:

  """

  Prepare scene for compositing 3D objects into this footage

  """

  ...

def slide_marker(offset: typing.Tuple[float, float] = (0.0, 0.0)) -> None:

  """

  Slide marker areas

  """

  ...

def slide_plane_marker() -> None:

  """

  Slide plane marker areas

  """

  ...

def solve_camera() -> None:

  """

  Solve camera motion from tracks

  """

  ...

def stabilize_2d_add() -> None:

  """

  Add selected tracks to 2D translation stabilization

  """

  ...

def stabilize_2d_remove() -> None:

  """

  Remove selected track from translation stabilization

  """

  ...

def stabilize_2d_rotation_add() -> None:

  """

  Add selected tracks to 2D rotation stabilization

  """

  ...

def stabilize_2d_rotation_remove() -> None:

  """

  Remove selected track from rotation stabilization

  """

  ...

def stabilize_2d_rotation_select() -> None:

  """

  Select tracks which are used for rotation stabilization

  """

  ...

def stabilize_2d_select() -> None:

  """

  Select tracks which are used for translation stabilization

  """

  ...

def track_color_preset_add(name: str = '', remove_name: bool = False, remove_active: bool = False) -> None:

  """

  Add or remove a Clip Track Color Preset

  """

  ...

def track_copy_color() -> None:

  """

  Copy color to all selected tracks

  """

  ...

def track_markers(backwards: bool = False, sequence: bool = False) -> None:

  """

  Track selected markers

  """

  ...

def track_settings_as_default() -> None:

  """

  Copy tracking settings from active track to default settings

  """

  ...

def track_settings_to_track() -> None:

  """

  Copy tracking settings from active track to selected tracks

  """

  ...

def track_to_empty() -> None:

  """

  Create an Empty object which will be copying movement of active track

  """

  ...

def tracking_object_new() -> None:

  """

  Add new object for tracking

  """

  ...

def tracking_object_remove() -> None:

  """

  Remove object for tracking

  """

  ...

def tracking_settings_preset_add(name: str = '', remove_name: bool = False, remove_active: bool = False) -> None:

  """

  Add or remove a motion tracking settings preset

  """

  ...

def view_all(fit_view: bool = False) -> None:

  """

  View whole image with markers

  """

  ...

def view_center_cursor() -> None:

  """

  Center the view so that the cursor is in the middle of the view

  """

  ...

def view_ndof() -> None:

  """

  Use a 3D mouse device to pan/zoom the view

  """

  ...

def view_pan(offset: typing.Tuple[float, float] = (0.0, 0.0)) -> None:

  """

  Pan the view

  """

  ...

def view_selected() -> None:

  """

  View all selected elements

  """

  ...

def view_zoom(factor: float = 0.0, use_cursor_init: bool = True) -> None:

  """

  Zoom in/out the view

  """

  ...

def view_zoom_in(location: typing.Tuple[float, float] = (0.0, 0.0)) -> None:

  """

  Zoom in the view

  """

  ...

def view_zoom_out(location: typing.Tuple[float, float] = (0.0, 0.0)) -> None:

  """

  Zoom out the view

  """

  ...

def view_zoom_ratio(ratio: float = 0.0) -> None:

  """

  Set the zoom ratio (based on clip size)

  """

  ...
