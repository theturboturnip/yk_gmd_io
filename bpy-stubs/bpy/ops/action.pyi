"""


Action Operators
****************

:func:`clean`

:func:`clickselect`

:func:`copy`

:func:`delete`

:func:`duplicate`

:func:`duplicate_move`

:func:`easing_type`

:func:`extrapolation_type`

:func:`frame_jump`

:func:`handle_type`

:func:`interpolation_type`

:func:`keyframe_insert`

:func:`keyframe_type`

:func:`layer_next`

:func:`layer_prev`

:func:`markers_make_local`

:func:`mirror`

:func:`new`

:func:`paste`

:func:`previewrange_set`

:func:`push_down`

:func:`sample`

:func:`select_all`

:func:`select_box`

:func:`select_circle`

:func:`select_column`

:func:`select_lasso`

:func:`select_leftright`

:func:`select_less`

:func:`select_linked`

:func:`select_more`

:func:`snap`

:func:`stash`

:func:`stash_and_create`

:func:`unlink`

:func:`view_all`

:func:`view_frame`

:func:`view_selected`

"""

import typing

def clean(threshold: float = 0.001, channels: bool = False) -> None:

  """

  Simplify F-Curves by removing closely spaced keyframes

  """

  ...

def clickselect(wait_to_deselect_others: bool = False, mouse_x: int = 0, mouse_y: int = 0, extend: bool = False, deselect_all: bool = False, column: bool = False, channel: bool = False) -> None:

  """

  Select keyframes by clicking on them

  """

  ...

def copy() -> None:

  """

  Copy selected keyframes to the copy/paste buffer

  """

  ...

def delete(confirm: bool = True) -> None:

  """

  Remove all selected keyframes

  """

  ...

def duplicate() -> None:

  """

  Make a copy of all selected keyframes

  """

  ...

def duplicate_move(ACTION_OT_duplicate: ACTION_OT_duplicate = None, TRANSFORM_OT_transform: TRANSFORM_OT_transform = None) -> None:

  """

  Make a copy of all selected keyframes and move them

  """

  ...

def easing_type(type: str = 'AUTO') -> None:

  """

  Set easing type for the F-Curve segments starting from the selected keyframes

  """

  ...

def extrapolation_type(type: str = 'CONSTANT') -> None:

  """

  Set extrapolation mode for selected F-Curves

  """

  ...

def frame_jump() -> None:

  """

  Set the current frame to the average frame value of selected keyframes

  """

  ...

def handle_type(type: str = 'FREE') -> None:

  """

  Set type of handle for selected keyframes

  """

  ...

def interpolation_type(type: str = 'CONSTANT') -> None:

  """

  Set interpolation mode for the F-Curve segments starting from the selected keyframes

  """

  ...

def keyframe_insert(type: str = 'ALL') -> None:

  """

  Insert keyframes for the specified channels

  """

  ...

def keyframe_type(type: str = 'KEYFRAME') -> None:

  """

  Set type of keyframe for the selected keyframes

  """

  ...

def layer_next() -> None:

  """

  Switch to editing action in animation layer above the current action in the NLA Stack

  """

  ...

def layer_prev() -> None:

  """

  Switch to editing action in animation layer below the current action in the NLA Stack

  """

  ...

def markers_make_local() -> None:

  """

  Move selected scene markers to the active Action as local 'pose' markers

  """

  ...

def mirror(type: str = 'CFRA') -> None:

  """

  Flip selected keyframes over the selected mirror line

  """

  ...

def new() -> None:

  """

  Create new action

  """

  ...

def paste(offset: str = 'START', merge: str = 'MIX', flipped: bool = False) -> None:

  """

  Paste keyframes from copy/paste buffer for the selected channels, starting on the current frame

  """

  ...

def previewrange_set() -> None:

  """

  Set Preview Range based on extents of selected Keyframes

  """

  ...

def push_down() -> None:

  """

  Push action down on to the NLA stack as a new strip

  """

  ...

def sample() -> None:

  """

  Add keyframes on every frame between the selected keyframes

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Toggle selection of all keyframes

  """

  ...

def select_box(axis_range: bool = False, xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, mode: str = 'SET', tweak: bool = False) -> None:

  """

  Select all keyframes within the specified region

  """

  ...

def select_circle(x: int = 0, y: int = 0, radius: int = 25, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Select keyframe points using circle selection

  """

  ...

def select_column(mode: str = 'KEYS') -> None:

  """

  Select all keyframes on the specified frame(s)

  """

  ...

def select_lasso(path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None, mode: str = 'SET') -> None:

  """

  Select keyframe points using lasso selection

  """

  ...

def select_leftright(mode: str = 'CHECK', extend: bool = False) -> None:

  """

  Select keyframes to the left or the right of the current frame

  """

  ...

def select_less() -> None:

  """

  Deselect keyframes on ends of selection islands

  """

  ...

def select_linked() -> None:

  """

  Select keyframes occurring in the same F-Curves as selected ones

  """

  ...

def select_more() -> None:

  """

  Select keyframes beside already selected ones

  """

  ...

def snap(type: str = 'CFRA') -> None:

  """

  Snap selected keyframes to the times specified

  """

  ...

def stash(create_new: bool = True) -> None:

  """

  Store this action in the NLA stack as a non-contributing strip for later use

  """

  ...

def stash_and_create() -> None:

  """

  Store this action in the NLA stack as a non-contributing strip for later use, and create a new action

  """

  ...

def unlink(force_delete: bool = False) -> None:

  """

  Unlink this action from the active action slot (and/or exit Tweak Mode)

  """

  ...

def view_all() -> None:

  """

  Reset viewable area to show full keyframe range

  """

  ...

def view_frame() -> None:

  """

  Move the view to the current frame

  """

  ...

def view_selected() -> None:

  """

  Reset viewable area to show selected keyframes range

  """

  ...
