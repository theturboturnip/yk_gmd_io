"""


Screen Operators
****************

:func:`actionzone`

:func:`animation_cancel`

:func:`animation_play`

:func:`animation_step`

:func:`area_close`

:func:`area_dupli`

:func:`area_join`

:func:`area_move`

:func:`area_options`

:func:`area_split`

:func:`area_swap`

:func:`back_to_previous`

:func:`delete`

:func:`drivers_editor_show`

:func:`frame_jump`

:func:`frame_offset`

:func:`header_toggle_menus`

:func:`info_log_show`

:func:`keyframe_jump`

:func:`marker_jump`

:func:`new`

:func:`redo_last`

:func:`region_blend`

:func:`region_context_menu`

:func:`region_flip`

:func:`region_quadview`

:func:`region_scale`

:func:`region_toggle`

:func:`repeat_history`

:func:`repeat_last`

:func:`screen_full_area`

:func:`screen_set`

:func:`screenshot`

:func:`screenshot_area`

:func:`space_context_cycle`

:func:`space_type_set_or_cycle`

:func:`spacedata_cleanup`

:func:`userpref_show`

:func:`workspace_cycle`

"""

import typing

def actionzone(modifier: int = 0) -> None:

  """

  Handle area action zones for mouse actions/gestures

  """

  ...

def animation_cancel(restore_frame: bool = True) -> None:

  """

  Cancel animation, returning to the original frame

  """

  ...

def animation_play(reverse: bool = False, sync: bool = False) -> None:

  """

  Play animation

  """

  ...

def animation_step() -> None:

  """

  Step through animation by position

  """

  ...

def area_close() -> None:

  """

  Close selected area

  """

  ...

def area_dupli() -> None:

  """

  Duplicate selected area into new window

  """

  ...

def area_join(cursor: typing.Tuple[int, int] = (0, 0)) -> None:

  """

  Join selected areas into new window

  """

  ...

def area_move(x: int = 0, y: int = 0, delta: int = 0) -> None:

  """

  Move selected area edges

  """

  ...

def area_options() -> None:

  """

  Operations for splitting and merging

  """

  ...

def area_split(direction: str = 'HORIZONTAL', factor: float = 0.5, cursor: typing.Tuple[int, int] = (0, 0)) -> None:

  """

  Split selected area into new windows

  """

  ...

def area_swap(cursor: typing.Tuple[int, int] = (0, 0)) -> None:

  """

  Swap selected areas screen positions

  """

  ...

def back_to_previous() -> None:

  """

  Revert back to the original screen layout, before fullscreen area overlay

  """

  ...

def delete() -> None:

  """

  Delete active screen

  """

  ...

def drivers_editor_show() -> None:

  """

  Show drivers editor in a separate window

  """

  ...

def frame_jump(end: bool = False) -> None:

  """

  Jump to first/last frame in frame range

  """

  ...

def frame_offset(delta: int = 0) -> None:

  """

  Move current frame forward/backward by a given number

  """

  ...

def header_toggle_menus() -> None:

  """

  Expand or collapse the header pulldown menus

  """

  ...

def info_log_show() -> None:

  """

  Show info log in a separate window

  """

  ...

def keyframe_jump(next: bool = True) -> None:

  """

  Jump to previous/next keyframe

  """

  ...

def marker_jump(next: bool = True) -> None:

  """

  Jump to previous/next marker

  """

  ...

def new() -> None:

  """

  Add a new screen

  """

  ...

def redo_last() -> None:

  """

  Display parameters for last action performed

  """

  ...

def region_blend() -> None:

  """

  Blend in and out overlapping region

  """

  ...

def region_context_menu() -> None:

  """

  Display region context menu

  """

  ...

def region_flip() -> None:

  """

  Toggle the region's alignment (left/right or top/bottom)

  """

  ...

def region_quadview() -> None:

  """

  Split selected area into camera, front, right, and top views

  """

  ...

def region_scale() -> None:

  """

  Scale selected area

  """

  ...

def region_toggle(region_type: str = 'WINDOW') -> None:

  """

  Hide or unhide the region

  """

  ...

def repeat_history(index: int = 0) -> None:

  """

  Display menu for previous actions performed

  """

  ...

def repeat_last() -> None:

  """

  Repeat last action

  """

  ...

def screen_full_area(use_hide_panels: bool = False) -> None:

  """

  Toggle display selected area as fullscreen/maximized

  """

  ...

def screen_set(delta: int = 1) -> None:

  """

  Cycle through available screens

  """

  ...

def screenshot(filepath: str = '', hide_props_region: bool = True, check_existing: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = True, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Capture a picture of the whole Blender window

  """

  ...

def screenshot_area(filepath: str = '', hide_props_region: bool = True, check_existing: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = True, filter_movie: bool = False, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Capture a picture of an editor

  """

  ...

def space_context_cycle(direction: str = 'NEXT') -> None:

  """

  Cycle through the editor context by activating the next/previous one

  """

  ...

def space_type_set_or_cycle(space_type: str = 'EMPTY') -> None:

  """

  Set the space type or cycle subtype

  """

  ...

def spacedata_cleanup() -> None:

  """

  Remove unused settings for invisible editors

  """

  ...

def userpref_show(section: str = 'INTERFACE') -> None:

  """

  Edit user preferences and system settings

  """

  ...

def workspace_cycle(direction: str = 'NEXT') -> None:

  """

  Cycle through workspaces

  """

  ...
