"""


Graph Operators
***************

:func:`bake`

:func:`clean`

:func:`click_insert`

:func:`clickselect`

:func:`copy`

:func:`cursor_set`

:func:`decimate`

:func:`delete`

:func:`driver_delete_invalid`

:func:`driver_variables_copy`

:func:`driver_variables_paste`

:func:`duplicate`

:func:`duplicate_move`

:func:`easing_type`

:func:`euler_filter`

:func:`extrapolation_type`

:func:`fmodifier_add`

:func:`fmodifier_copy`

:func:`fmodifier_paste`

:func:`frame_jump`

:func:`ghost_curves_clear`

:func:`ghost_curves_create`

:func:`handle_type`

:func:`hide`

:func:`interpolation_type`

:func:`keyframe_insert`

:func:`mirror`

:func:`paste`

:func:`previewrange_set`

:func:`reveal`

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

:func:`smooth`

:func:`snap`

:func:`snap_cursor_value`

:func:`sound_bake`

:func:`unbake`

:func:`view_all`

:func:`view_frame`

:func:`view_selected`

"""

import typing

def bake() -> None:

  """

  Bake selected F-Curves to a set of sampled points defining a similar curve

  """

  ...

def clean(threshold: float = 0.001, channels: bool = False) -> None:

  """

  Simplify F-Curves by removing closely spaced keyframes

  """

  ...

def click_insert(frame: float = 1.0, value: float = 1.0, extend: bool = False) -> None:

  """

  Insert new keyframe at the cursor position for the active F-Curve

  """

  ...

def clickselect(wait_to_deselect_others: bool = False, mouse_x: int = 0, mouse_y: int = 0, extend: bool = False, deselect_all: bool = False, column: bool = False, curves: bool = False) -> None:

  """

  Select keyframes by clicking on them

  """

  ...

def copy() -> None:

  """

  Copy selected keyframes to the copy/paste buffer

  """

  ...

def cursor_set(frame: float = 0.0, value: float = 0.0) -> None:

  """

  Interactively set the current frame and value cursor

  """

  ...

def decimate(mode: str = 'RATIO', remove_ratio: float = 0.333333, remove_error_margin: float = 0.0) -> None:

  """

  Decimate F-Curves by removing keyframes that influence the curve shape the least

  """

  ...

def delete(confirm: bool = True) -> None:

  """

  Remove all selected keyframes

  """

  ...

def driver_delete_invalid() -> None:

  """

  Delete all visible drivers considered invalid

  """

  ...

def driver_variables_copy() -> None:

  """

  Copy the driver variables of the active driver

  """

  ...

def driver_variables_paste(replace: bool = False) -> None:

  """

  Add copied driver variables to the active driver

  """

  ...

def duplicate(mode: str = 'TRANSLATION') -> None:

  """

  Make a copy of all selected keyframes

  """

  ...

def duplicate_move(GRAPH_OT_duplicate: GRAPH_OT_duplicate = None, TRANSFORM_OT_transform: TRANSFORM_OT_transform = None) -> None:

  """

  Make a copy of all selected keyframes and move them

  """

  ...

def easing_type(type: str = 'AUTO') -> None:

  """

  Set easing type for the F-Curve segments starting from the selected keyframes

  """

  ...

def euler_filter() -> None:

  """

  Fix large jumps and flips in the selected Euler Rotation F-Curves arising from rotation values being clipped when baking physics

  """

  ...

def extrapolation_type(type: str = 'CONSTANT') -> None:

  """

  Set extrapolation mode for selected F-Curves

  """

  ...

def fmodifier_add(type: str = 'NULL', only_active: bool = True) -> None:

  """

  Add F-Modifier to the active/selected F-Curves

  """

  ...

def fmodifier_copy() -> None:

  """

  Copy the F-Modifier(s) of the active F-Curve

  """

  ...

def fmodifier_paste(only_active: bool = False, replace: bool = False) -> None:

  """

  Add copied F-Modifiers to the selected F-Curves

  """

  ...

def frame_jump() -> None:

  """

  Place the cursor on the midpoint of selected keyframes

  """

  ...

def ghost_curves_clear() -> None:

  """

  Clear F-Curve snapshots (Ghosts) for active Graph Editor

  """

  ...

def ghost_curves_create() -> None:

  """

  Create snapshot (Ghosts) of selected F-Curves as background aid for active Graph Editor

  """

  ...

def handle_type(type: str = 'FREE') -> None:

  """

  Set type of handle for selected keyframes

  """

  ...

def hide(unselected: bool = False) -> None:

  """

  Hide selected curves from Graph Editor view

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

def mirror(type: str = 'CFRA') -> None:

  """

  Flip selected keyframes over the selected mirror line

  """

  ...

def paste(offset: str = 'START', merge: str = 'MIX', flipped: bool = False) -> None:

  """

  Paste keyframes from copy/paste buffer for the selected channels, starting on the current frame

  """

  ...

def previewrange_set() -> None:

  """

  Set Preview Range based on range of selected keyframes

  """

  ...

def reveal(select: bool = True) -> None:

  """

  Make previously hidden curves visible again in Graph Editor view

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

def select_box(axis_range: bool = False, include_handles: bool = True, tweak: bool = False, use_curve_selection: bool = True, xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Select all keyframes within the specified region

  """

  ...

def select_circle(x: int = 0, y: int = 0, radius: int = 25, wait_for_input: bool = True, mode: str = 'SET', use_curve_selection: bool = True) -> None:

  """

  Select keyframe points using circle selection

  """

  ...

def select_column(mode: str = 'KEYS') -> None:

  """

  Select all keyframes on the specified frame(s)

  """

  ...

def select_lasso(path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None, mode: str = 'SET', use_curve_selection: bool = True) -> None:

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

def smooth() -> None:

  """

  Apply weighted moving means to make selected F-Curves less bumpy

  """

  ...

def snap(type: str = 'CFRA') -> None:

  """

  Snap selected keyframes to the chosen times/values

  """

  ...

def snap_cursor_value() -> None:

  """

  Place the cursor value on the average value of selected keyframes

  """

  ...

def sound_bake(filepath: str = '', filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = False, filter_movie: bool = True, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = True, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '', low: float = 0.0, high: float = 100000.0, attack: float = 0.005, release: float = 0.2, threshold: float = 0.0, use_accumulate: bool = False, use_additive: bool = False, use_square: bool = False, sthreshold: float = 0.1) -> None:

  """

  Bakes a sound wave to selected F-Curves

  """

  ...

def unbake() -> None:

  """

  Un-Bake selected F-Points to F-Curves

  """

  ...

def view_all(include_handles: bool = True) -> None:

  """

  Reset viewable area to show full keyframe range

  """

  ...

def view_frame() -> None:

  """

  Move the view to the current frame

  """

  ...

def view_selected(include_handles: bool = True) -> None:

  """

  Reset viewable area to show selected keyframe range

  """

  ...
