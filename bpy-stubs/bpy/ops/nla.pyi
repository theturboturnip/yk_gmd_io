"""


Nla Operators
*************

:func:`action_pushdown`

:func:`action_sync_length`

:func:`action_unlink`

:func:`actionclip_add`

:func:`apply_scale`

:func:`bake`

:func:`channels_click`

:func:`clear_scale`

:func:`click_select`

:func:`delete`

:func:`duplicate`

:func:`fmodifier_add`

:func:`fmodifier_copy`

:func:`fmodifier_paste`

:func:`make_single_user`

:func:`meta_add`

:func:`meta_remove`

:func:`move_down`

:func:`move_up`

:func:`mute_toggle`

:func:`previewrange_set`

:func:`select_all`

:func:`select_box`

:func:`select_leftright`

:func:`selected_objects_add`

:func:`snap`

:func:`soundclip_add`

:func:`split`

:func:`swap`

:func:`tracks_add`

:func:`tracks_delete`

:func:`transition_add`

:func:`tweakmode_enter`

:func:`tweakmode_exit`

:func:`view_all`

:func:`view_frame`

:func:`view_selected`

"""

import typing

def action_pushdown(channel_index: int = -1) -> None:

  """

  Push action down onto the top of the NLA stack as a new strip

  """

  ...

def action_sync_length(active: bool = True) -> None:

  """

  Synchronize the length of the referenced Action with the length used in the strip

  """

  ...

def action_unlink(force_delete: bool = False) -> None:

  """

  Unlink this action from the active action slot (and/or exit Tweak Mode)

  """

  ...

def actionclip_add(action: str = '') -> None:

  """

  Add an Action-Clip strip (i.e. an NLA Strip referencing an Action) to the active track

  """

  ...

def apply_scale() -> None:

  """

  Apply scaling of selected strips to their referenced Actions

  """

  ...

def bake(frame_start: int = 1, frame_end: int = 250, step: int = 1, only_selected: bool = True, visual_keying: bool = False, clear_constraints: bool = False, clear_parents: bool = False, use_current_action: bool = False, clean_curves: bool = False, bake_types: typing.Set[str] = {'POSE'}) -> None:

  """

  Bake all selected objects location/scale/rotation animation to an action

  """

  ...

def channels_click(extend: bool = False) -> None:

  """

  Handle clicks to select NLA channels

  """

  ...

def clear_scale() -> None:

  """

  Reset scaling of selected strips

  """

  ...

def click_select(wait_to_deselect_others: bool = False, mouse_x: int = 0, mouse_y: int = 0, extend: bool = False, deselect_all: bool = False) -> None:

  """

  Handle clicks to select NLA Strips

  """

  ...

def delete() -> None:

  """

  Delete selected strips

  """

  ...

def duplicate(linked: bool = False, mode: str = 'TRANSLATION') -> None:

  """

  Duplicate selected NLA-Strips, adding the new strips in new tracks above the originals

  """

  ...

def fmodifier_add(type: str = 'NULL', only_active: bool = True) -> None:

  """

  Add F-Modifier to the active/selected NLA-Strips

  """

  ...

def fmodifier_copy() -> None:

  """

  Copy the F-Modifier(s) of the active NLA-Strip

  """

  ...

def fmodifier_paste(only_active: bool = True, replace: bool = False) -> None:

  """

  Add copied F-Modifiers to the selected NLA-Strips

  """

  ...

def make_single_user() -> None:

  """

  Ensure that each action is only used once in the set of strips selected

  """

  ...

def meta_add() -> None:

  """

  Add new meta-strips incorporating the selected strips

  """

  ...

def meta_remove() -> None:

  """

  Separate out the strips held by the selected meta-strips

  """

  ...

def move_down() -> None:

  """

  Move selected strips down a track if there's room

  """

  ...

def move_up() -> None:

  """

  Move selected strips up a track if there's room

  """

  ...

def mute_toggle() -> None:

  """

  Mute or un-mute selected strips

  """

  ...

def previewrange_set() -> None:

  """

  Set Preview Range based on extends of selected strips

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Select or deselect all NLA-Strips

  """

  ...

def select_box(axis_range: bool = False, tweak: bool = False, xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Use box selection to grab NLA-Strips

  """

  ...

def select_leftright(mode: str = 'CHECK', extend: bool = False) -> None:

  """

  Select strips to the left or the right of the current frame

  """

  ...

def selected_objects_add() -> None:

  """

  Make selected objects appear in NLA Editor by adding Animation Data

  """

  ...

def snap(type: str = 'CFRA') -> None:

  """

  Move start of strips to specified time

  """

  ...

def soundclip_add() -> None:

  """

  Add a strip for controlling when speaker plays its sound clip

  """

  ...

def split() -> None:

  """

  Split selected strips at their midpoints

  """

  ...

def swap() -> None:

  """

  Swap order of selected strips within tracks

  """

  ...

def tracks_add(above_selected: bool = False) -> None:

  """

  Add NLA-Tracks above/after the selected tracks

  """

  ...

def tracks_delete() -> None:

  """

  Delete selected NLA-Tracks and the strips they contain

  """

  ...

def transition_add() -> None:

  """

  Add a transition strip between two adjacent selected strips

  """

  ...

def tweakmode_enter(isolate_action: bool = False) -> None:

  """

  Enter tweaking mode for the action referenced by the active strip to edit its keyframes

  """

  ...

def tweakmode_exit(isolate_action: bool = False) -> None:

  """

  Exit tweaking mode for the action referenced by the active strip

  """

  ...

def view_all() -> None:

  """

  Reset viewable area to show full strips range

  """

  ...

def view_frame() -> None:

  """

  Move the view to the current frame

  """

  ...

def view_selected() -> None:

  """

  Reset viewable area to show selected strips range

  """

  ...
