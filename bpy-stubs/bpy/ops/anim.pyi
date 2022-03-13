"""


Anim Operators
**************

:func:`change_frame`

:func:`channel_select_keys`

:func:`channels_clean_empty`

:func:`channels_click`

:func:`channels_collapse`

:func:`channels_delete`

:func:`channels_editable_toggle`

:func:`channels_expand`

:func:`channels_fcurves_enable`

:func:`channels_group`

:func:`channels_move`

:func:`channels_rename`

:func:`channels_select_all`

:func:`channels_select_box`

:func:`channels_select_filter`

:func:`channels_setting_disable`

:func:`channels_setting_enable`

:func:`channels_setting_toggle`

:func:`channels_ungroup`

:func:`clear_useless_actions`

:func:`copy_driver_button`

:func:`driver_button_add`

:func:`driver_button_edit`

:func:`driver_button_remove`

:func:`end_frame_set`

:func:`keyframe_clear_button`

:func:`keyframe_clear_v3d`

:func:`keyframe_delete`

:func:`keyframe_delete_button`

:func:`keyframe_delete_by_name`

:func:`keyframe_delete_v3d`

:func:`keyframe_insert`

:func:`keyframe_insert_button`

:func:`keyframe_insert_by_name`

:func:`keyframe_insert_menu`

:func:`keying_set_active_set`

:func:`keying_set_add`

:func:`keying_set_export`

:func:`keying_set_path_add`

:func:`keying_set_path_remove`

:func:`keying_set_remove`

:func:`keyingset_button_add`

:func:`keyingset_button_remove`

:func:`paste_driver_button`

:func:`previewrange_clear`

:func:`previewrange_set`

:func:`start_frame_set`

:func:`update_animated_transform_constraints`

"""

import typing

def change_frame(frame: float = 0.0, snap: bool = False) -> None:

  """

  Interactively change the current frame number

  """

  ...

def channel_select_keys(extend: bool = False) -> None:

  """

  Select all keyframes of channel under mouse

  """

  ...

def channels_clean_empty() -> None:

  """

  Delete all empty animation data containers from visible data-blocks

  """

  ...

def channels_click(extend: bool = False, children_only: bool = False) -> None:

  """

  Handle mouse clicks over animation channels

  """

  ...

def channels_collapse(all: bool = True) -> None:

  """

  Collapse (close) all selected expandable animation channels

  """

  ...

def channels_delete() -> None:

  """

  Delete all selected animation channels

  """

  ...

def channels_editable_toggle(mode: str = 'TOGGLE', type: str = 'PROTECT') -> None:

  """

  Toggle editability of selected channels

  """

  ...

def channels_expand(all: bool = True) -> None:

  """

  Expand (open) all selected expandable animation channels

  """

  ...

def channels_fcurves_enable() -> None:

  """

  Clears 'disabled' tag from all F-Curves to get broken F-Curves working again

  """

  ...

def channels_group(name: str = 'New Group') -> None:

  """

  Add selected F-Curves to a new group

  """

  ...

def channels_move(direction: str = 'DOWN') -> None:

  """

  Rearrange selected animation channels

  """

  ...

def channels_rename() -> None:

  """

  Rename animation channel under mouse

  """

  ...

def channels_select_all(action: str = 'TOGGLE') -> None:

  """

  Toggle selection of all animation channels

  """

  ...

def channels_select_box(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, deselect: bool = False, extend: bool = True) -> None:

  """

  Select all animation channels within the specified region

  """

  ...

def channels_select_filter() -> None:

  """

  Start entering text which filters the set of channels shown to only include those with matching names

  """

  ...

def channels_setting_disable(mode: str = 'DISABLE', type: str = 'PROTECT') -> None:

  """

  Disable specified setting on all selected animation channels

  """

  ...

def channels_setting_enable(mode: str = 'ENABLE', type: str = 'PROTECT') -> None:

  """

  Enable specified setting on all selected animation channels

  """

  ...

def channels_setting_toggle(mode: str = 'TOGGLE', type: str = 'PROTECT') -> None:

  """

  Toggle specified setting on all selected animation channels

  """

  ...

def channels_ungroup() -> None:

  """

  Remove selected F-Curves from their current groups

  """

  ...

def clear_useless_actions(only_unused: bool = True) -> None:

  """

  Mark actions with no F-Curves for deletion after save and reload of file preserving "action libraries"

  """

  ...

def copy_driver_button() -> None:

  """

  Copy the driver for the highlighted button

  """

  ...

def driver_button_add() -> None:

  """

  Add driver for the property under the cursor

  """

  ...

def driver_button_edit() -> None:

  """

  Edit the drivers for the property connected represented by the highlighted button

  """

  ...

def driver_button_remove(all: bool = True) -> None:

  """

  Remove the driver(s) for the property(s) connected represented by the highlighted button

  """

  ...

def end_frame_set() -> None:

  """

  Set the current frame as the preview or scene end frame

  """

  ...

def keyframe_clear_button(all: bool = True) -> None:

  """

  Clear all keyframes on the currently active property

  """

  ...

def keyframe_clear_v3d() -> None:

  """

  Remove all keyframe animation for selected objects

  """

  ...

def keyframe_delete(type: str = 'DEFAULT') -> None:

  """

  Delete keyframes on the current frame for all properties in the specified Keying Set

  """

  ...

def keyframe_delete_button(all: bool = True) -> None:

  """

  Delete current keyframe of current UI-active property

  """

  ...

def keyframe_delete_by_name(type: str = 'Type') -> None:

  """

  Alternate access to 'Delete Keyframe' for keymaps to use

  """

  ...

def keyframe_delete_v3d() -> None:

  """

  Remove keyframes on current frame for selected objects and bones

  """

  ...

def keyframe_insert(type: str = 'DEFAULT') -> None:

  """

  Insert keyframes on the current frame for all properties in the specified Keying Set

  """

  ...

def keyframe_insert_button(all: bool = True) -> None:

  """

  Insert a keyframe for current UI-active property

  """

  ...

def keyframe_insert_by_name(type: str = 'Type') -> None:

  """

  Alternate access to 'Insert Keyframe' for keymaps to use

  """

  ...

def keyframe_insert_menu(type: str = 'DEFAULT', always_prompt: bool = False) -> None:

  """

  Insert Keyframes for specified Keying Set, with menu of available Keying Sets if undefined

  """

  ...

def keying_set_active_set(type: str = 'DEFAULT') -> None:

  """

  Select a new keying set as the active one

  """

  ...

def keying_set_add() -> None:

  """

  Add a new (empty) Keying Set to the active Scene

  """

  ...

def keying_set_export(filepath: str = '', filter_folder: bool = True, filter_text: bool = True, filter_python: bool = True) -> None:

  """

  Export Keying Set to a python script

  """

  ...

def keying_set_path_add() -> None:

  """

  Add empty path to active Keying Set

  """

  ...

def keying_set_path_remove() -> None:

  """

  Remove active Path from active Keying Set

  """

  ...

def keying_set_remove() -> None:

  """

  Remove the active Keying Set

  """

  ...

def keyingset_button_add(all: bool = True) -> None:

  """

  Add current UI-active property to current keying set

  """

  ...

def keyingset_button_remove() -> None:

  """

  Remove current UI-active property from current keying set

  """

  ...

def paste_driver_button() -> None:

  """

  Paste the driver in the copy/paste buffer for the highlighted button

  """

  ...

def previewrange_clear() -> None:

  """

  Clear preview range

  """

  ...

def previewrange_set(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True) -> None:

  """

  Interactively define frame range used for playback

  """

  ...

def start_frame_set() -> None:

  """

  Set the current frame as the preview or scene start frame

  """

  ...

def update_animated_transform_constraints(use_convert_to_radians: bool = True) -> None:

  """

  Update f-curves/drivers affecting Transform constraints (use it with files from 2.70 and earlier)

  """

  ...
