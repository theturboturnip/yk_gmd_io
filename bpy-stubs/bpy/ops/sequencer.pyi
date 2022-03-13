"""


Sequencer Operators
*******************

:func:`change_effect_input`

:func:`change_effect_type`

:func:`change_path`

:func:`copy`

:func:`crossfade_sounds`

:func:`cursor_set`

:func:`deinterlace_selected_movies`

:func:`delete`

:func:`duplicate`

:func:`duplicate_move`

:func:`effect_strip_add`

:func:`enable_proxies`

:func:`export_subtitles`

:func:`fades_add`

:func:`fades_clear`

:func:`gap_insert`

:func:`gap_remove`

:func:`image_strip_add`

:func:`images_separate`

:func:`lock`

:func:`mask_strip_add`

:func:`meta_make`

:func:`meta_separate`

:func:`meta_toggle`

:func:`movie_strip_add`

:func:`movieclip_strip_add`

:func:`mute`

:func:`offset_clear`

:func:`paste`

:func:`reassign_inputs`

:func:`rebuild_proxy`

:func:`refresh_all`

:func:`reload`

:func:`rendersize`

:func:`sample`

:func:`scene_strip_add`

:func:`select`

:func:`select_all`

:func:`select_box`

:func:`select_grouped`

:func:`select_handles`

:func:`select_less`

:func:`select_linked`

:func:`select_linked_pick`

:func:`select_more`

:func:`select_side`

:func:`select_side_of_frame`

:func:`set_range_to_strips`

:func:`slip`

:func:`snap`

:func:`sound_strip_add`

:func:`split`

:func:`split_multicam`

:func:`strip_color_tag_set`

:func:`strip_jump`

:func:`strip_modifier_add`

:func:`strip_modifier_copy`

:func:`strip_modifier_move`

:func:`strip_modifier_remove`

:func:`strip_transform_clear`

:func:`strip_transform_fit`

:func:`swap`

:func:`swap_data`

:func:`swap_inputs`

:func:`unlock`

:func:`unmute`

:func:`view_all`

:func:`view_all_preview`

:func:`view_frame`

:func:`view_ghost_border`

:func:`view_selected`

:func:`view_zoom_ratio`

"""

import typing

def change_effect_input(swap: str = 'A_B') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def change_effect_type(type: str = 'CROSS') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def change_path(filepath: str = '', directory: str = '', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, display_type: str = 'DEFAULT', sort_method: str = '', use_placeholders: bool = False) -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def copy() -> None:

  """

  Copy selected strips to clipboard

  """

  ...

def crossfade_sounds() -> None:

  """

  Do cross-fading volume animation of two selected sound strips

  """

  ...

def cursor_set(location: typing.Tuple[float, float] = (0.0, 0.0)) -> None:

  """

  Set 2D cursor location

  """

  ...

def deinterlace_selected_movies() -> None:

  """

  Deinterlace all selected movie sources

  """

  ...

def delete() -> None:

  """

  Erase selected strips from the sequencer

  """

  ...

def duplicate() -> None:

  """

  Duplicate the selected strips

  """

  ...

def duplicate_move(SEQUENCER_OT_duplicate: SEQUENCER_OT_duplicate = None, TRANSFORM_OT_seq_slide: TRANSFORM_OT_seq_slide = None) -> None:

  """

  Duplicate selected strips and move them

  """

  ...

def effect_strip_add(type: str = 'CROSS', frame_start: int = 0, frame_end: int = 0, channel: int = 1, replace_sel: bool = True, overlap: bool = False, color: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Add an effect to the sequencer, most are applied on top of existing strips

  """

  ...

def enable_proxies(proxy_25: bool = False, proxy_50: bool = False, proxy_75: bool = False, proxy_100: bool = False, overwrite: bool = False) -> None:

  """

  Enable selected proxies on all selected Movie and Image strips

  """

  ...

def export_subtitles(filepath: str = '', hide_props_region: bool = True, check_existing: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 8, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Export .srt file containing text strips

  """

  ...

def fades_add(duration_seconds: float = 1.0, type: str = 'IN_OUT') -> None:

  """

  Adds or updates a fade animation for either visual or audio strips

  """

  ...

def fades_clear() -> None:

  """

  Removes fade animation from selected sequences

  """

  ...

def gap_insert(frames: int = 10) -> None:

  """

  Insert gap at current frame to first strips at the right, independent of selection or locked state of strips

  """

  ...

def gap_remove(all: bool = False) -> None:

  """

  Remove gap at current frame to first strip at the right, independent of selection or locked state of strips

  """

  ...

def image_strip_add(directory: str = '', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = True, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '', frame_start: int = 0, frame_end: int = 0, channel: int = 1, replace_sel: bool = True, overlap: bool = False, fit_method: str = 'FIT', set_view_transform: bool = True, use_placeholders: bool = False) -> None:

  """

  Add an image or image sequence to the sequencer

  """

  ...

def images_separate(length: int = 1) -> None:

  """

  On image sequence strips, it returns a strip for each image

  """

  ...

def lock() -> None:

  """

  Lock strips so they can't be transformed

  """

  ...

def mask_strip_add(frame_start: int = 0, channel: int = 1, replace_sel: bool = True, overlap: bool = False, mask: str = '') -> None:

  """

  Add a mask strip to the sequencer

  """

  ...

def meta_make() -> None:

  """

  Group selected strips into a meta-strip

  """

  ...

def meta_separate() -> None:

  """

  Put the contents of a meta-strip back in the sequencer

  """

  ...

def meta_toggle() -> None:

  """

  Toggle a meta-strip (to edit enclosed strips)

  """

  ...

def movie_strip_add(filepath: str = '', directory: str = '', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = True, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '', frame_start: int = 0, channel: int = 1, replace_sel: bool = True, overlap: bool = False, fit_method: str = 'FIT', set_view_transform: bool = True, sound: bool = True, use_framerate: bool = True) -> None:

  """

  Add a movie strip to the sequencer

  """

  ...

def movieclip_strip_add(frame_start: int = 0, channel: int = 1, replace_sel: bool = True, overlap: bool = False, clip: str = '') -> None:

  """

  Add a movieclip strip to the sequencer

  """

  ...

def mute(unselected: bool = False) -> None:

  """

  Mute (un)selected strips

  """

  ...

def offset_clear() -> None:

  """

  Clear strip offsets from the start and end frames

  """

  ...

def paste(keep_offset: bool = False) -> None:

  """

  Paste strips from clipboard

  """

  ...

def reassign_inputs() -> None:

  """

  Reassign the inputs for the effect strip

  """

  ...

def rebuild_proxy() -> None:

  """

  Rebuild all selected proxies and timecode indices using the job system

  """

  ...

def refresh_all() -> None:

  """

  Refresh the sequencer editor

  """

  ...

def reload(adjust_length: bool = False) -> None:

  """

  Reload strips in the sequencer

  """

  ...

def rendersize() -> None:

  """

  Set render size and aspect from active sequence

  """

  ...

def sample(size: int = 1) -> None:

  """

  Use mouse to sample color in current frame

  """

  ...

def scene_strip_add(frame_start: int = 0, channel: int = 1, replace_sel: bool = True, overlap: bool = False, scene: str = '') -> None:

  """

  Add a strip to the sequencer using a blender scene as a source

  """

  ...

def select(wait_to_deselect_others: bool = False, mouse_x: int = 0, mouse_y: int = 0, extend: bool = False, deselect: bool = False, toggle: bool = False, deselect_all: bool = False, center: bool = False, linked_handle: bool = False, linked_time: bool = False, side_of_frame: bool = False) -> None:

  """

  Select a strip (last selected becomes the "active strip")

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Select or deselect all strips

  """

  ...

def select_box(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, mode: str = 'SET', tweak: bool = False, include_handles: bool = False) -> None:

  """

  Select strips using box selection

  """

  ...

def select_grouped(type: str = 'TYPE', extend: bool = False, use_active_channel: bool = False) -> None:

  """

  Select all strips grouped by various properties

  """

  ...

def select_handles(side: str = 'BOTH') -> None:

  """

  Select gizmo handles on the sides of the selected strip

  """

  ...

def select_less() -> None:

  """

  Shrink the current selection of adjacent selected strips

  """

  ...

def select_linked() -> None:

  """

  Select all strips adjacent to the current selection

  """

  ...

def select_linked_pick(extend: bool = False) -> None:

  """

  Select a chain of linked strips nearest to the mouse pointer

  """

  ...

def select_more() -> None:

  """

  Select more strips adjacent to the current selection

  """

  ...

def select_side(side: str = 'BOTH') -> None:

  """

  Select strips on the nominated side of the selected strips

  """

  ...

def select_side_of_frame(extend: bool = False, side: str = 'LEFT') -> None:

  """

  Select strips relative to the current frame

  """

  ...

def set_range_to_strips(preview: bool = False) -> None:

  """

  Set the frame range to the selected strips start and end

  """

  ...

def slip(offset: int = 0) -> None:

  """

  Slip the contents of selected strips

  """

  ...

def snap(frame: int = 0) -> None:

  """

  Frame where selected strips will be snapped

  """

  ...

def sound_strip_add(filepath: str = '', directory: str = '', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = True, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, display_type: str = 'DEFAULT', sort_method: str = '', frame_start: int = 0, channel: int = 1, replace_sel: bool = True, overlap: bool = False, cache: bool = False, mono: bool = False) -> None:

  """

  Add a sound strip to the sequencer

  """

  ...

def split(frame: int = 0, channel: int = 0, type: str = 'SOFT', use_cursor_position: bool = False, side: str = 'MOUSE', ignore_selection: bool = False) -> None:

  """

  Split the selected strips in two

  """

  ...

def split_multicam(camera: int = 1) -> None:

  """

  Split multicam strip and select camera

  """

  ...

def strip_color_tag_set(color: str = 'NONE') -> None:

  """

  Set a color tag for the selected strips

  """

  ...

def strip_jump(next: bool = True, center: bool = True) -> None:

  """

  Move frame to previous edit point

  """

  ...

def strip_modifier_add(type: str = 'COLOR_BALANCE') -> None:

  """

  Add a modifier to the strip

  """

  ...

def strip_modifier_copy(type: str = 'REPLACE') -> None:

  """

  Copy modifiers of the active strip to all selected strips

  """

  ...

def strip_modifier_move(name: str = 'Name', direction: str = 'UP') -> None:

  """

  Move modifier up and down in the stack

  """

  ...

def strip_modifier_remove(name: str = 'Name') -> None:

  """

  Remove a modifier from the strip

  """

  ...

def strip_transform_clear(property: str = 'ALL') -> None:

  """

  Reset image transformation to default value

  """

  ...

def strip_transform_fit(fit_method: str = 'FIT') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def swap(side: str = 'RIGHT') -> None:

  """

  Swap active strip with strip to the right or left

  """

  ...

def swap_data() -> None:

  """

  Swap 2 sequencer strips

  """

  ...

def swap_inputs() -> None:

  """

  Swap the first two inputs for the effect strip

  """

  ...

def unlock() -> None:

  """

  Unlock strips so they can be transformed

  """

  ...

def unmute(unselected: bool = False) -> None:

  """

  Unmute (un)selected strips

  """

  ...

def view_all() -> None:

  """

  View all the strips in the sequencer

  """

  ...

def view_all_preview() -> None:

  """

  Zoom preview to fit in the area

  """

  ...

def view_frame() -> None:

  """

  Move the view to the current frame

  """

  ...

def view_ghost_border(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True) -> None:

  """

  Set the boundaries of the border used for offset view

  """

  ...

def view_selected() -> None:

  """

  Zoom the sequencer on the selected strips

  """

  ...

def view_zoom_ratio(ratio: float = 1.0) -> None:

  """

  Change zoom ratio of sequencer preview

  """

  ...
