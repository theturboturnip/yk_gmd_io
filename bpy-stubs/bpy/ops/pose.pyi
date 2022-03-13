"""


Pose Operators
**************

:func:`armature_apply`

:func:`autoside_names`

:func:`blend_to_neighbor`

:func:`bone_layers`

:func:`breakdown`

:func:`constraint_add`

:func:`constraint_add_with_targets`

:func:`constraints_clear`

:func:`constraints_copy`

:func:`copy`

:func:`flip_names`

:func:`group_add`

:func:`group_assign`

:func:`group_deselect`

:func:`group_move`

:func:`group_remove`

:func:`group_select`

:func:`group_sort`

:func:`group_unassign`

:func:`hide`

:func:`ik_add`

:func:`ik_clear`

:func:`loc_clear`

:func:`paste`

:func:`paths_calculate`

:func:`paths_clear`

:func:`paths_range_update`

:func:`paths_update`

:func:`propagate`

:func:`push`

:func:`push_rest`

:func:`quaternions_flip`

:func:`relax`

:func:`relax_rest`

:func:`reveal`

:func:`rot_clear`

:func:`rotation_mode_set`

:func:`scale_clear`

:func:`select_all`

:func:`select_constraint_target`

:func:`select_grouped`

:func:`select_hierarchy`

:func:`select_linked`

:func:`select_linked_pick`

:func:`select_mirror`

:func:`select_parent`

:func:`transforms_clear`

:func:`user_transforms_clear`

:func:`visual_transform_apply`

"""

import typing

def armature_apply(selected: bool = False) -> None:

  """

  Apply the current pose as the new rest pose

  """

  ...

def autoside_names(axis: str = 'XAXIS') -> None:

  """

  Automatically renames the selected bones according to which side of the target axis they fall on

  """

  ...

def blend_to_neighbor(factor: float = 0.5, prev_frame: int = 0, next_frame: int = 0, channels: str = 'ALL', axis_lock: str = 'FREE') -> None:

  """

  Blend from current position to previous or next keyframe

  """

  ...

def bone_layers(layers: typing.Tuple[bool, ...] = (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)) -> None:

  """

  Change the layers that the selected bones belong to

  """

  ...

def breakdown(factor: float = 0.5, prev_frame: int = 0, next_frame: int = 0, channels: str = 'ALL', axis_lock: str = 'FREE') -> None:

  """

  Create a suitable breakdown pose on the current frame

  """

  ...

def constraint_add(type: str = '') -> None:

  """

  Add a constraint to the active bone

  """

  ...

def constraint_add_with_targets(type: str = '') -> None:

  """

  Add a constraint to the active bone, with target (where applicable) set to the selected Objects/Bones

  """

  ...

def constraints_clear() -> None:

  """

  Clear all the constraints for the selected bones

  """

  ...

def constraints_copy() -> None:

  """

  Copy constraints to other selected bones

  """

  ...

def copy() -> None:

  """

  Copies the current pose of the selected bones to copy/paste buffer

  """

  ...

def flip_names(do_strip_numbers: bool = False) -> None:

  """

  Flips (and corrects) the axis suffixes of the names of selected bones

  """

  ...

def group_add() -> None:

  """

  Add a new bone group

  """

  ...

def group_assign(type: int = 0) -> None:

  """

  Add selected bones to the chosen bone group

  """

  ...

def group_deselect() -> None:

  """

  Deselect bones of active Bone Group

  """

  ...

def group_move(direction: str = 'UP') -> None:

  """

  Change position of active Bone Group in list of Bone Groups

  """

  ...

def group_remove() -> None:

  """

  Remove the active bone group

  """

  ...

def group_select() -> None:

  """

  Select bones in active Bone Group

  """

  ...

def group_sort() -> None:

  """

  Sort Bone Groups by their names in ascending order

  """

  ...

def group_unassign() -> None:

  """

  Remove selected bones from all bone groups

  """

  ...

def hide(unselected: bool = False) -> None:

  """

  Tag selected bones to not be visible in Pose Mode

  """

  ...

def ik_add(with_targets: bool = True) -> None:

  """

  Add IK Constraint to the active Bone

  """

  ...

def ik_clear() -> None:

  """

  Remove all IK Constraints from selected bones

  """

  ...

def loc_clear() -> None:

  """

  Reset locations of selected bones to their default values

  """

  ...

def paste(flipped: bool = False, selected_mask: bool = False) -> None:

  """

  Paste the stored pose on to the current pose

  """

  ...

def paths_calculate(start_frame: int = 1, end_frame: int = 250, bake_location: str = 'HEADS') -> None:

  """

  Calculate paths for the selected bones

  """

  ...

def paths_clear(only_selected: bool = False) -> None:

  """

  Clear path caches for all bones, hold Shift key for selected bones only

  """

  ...

def paths_range_update() -> None:

  """

  Update frame range for motion paths from the Scene's current frame range

  """

  ...

def paths_update() -> None:

  """

  Recalculate paths for bones that already have them

  """

  ...

def propagate(mode: str = 'WHILE_HELD', end_frame: float = 250.0) -> None:

  """

  Copy selected aspects of the current pose to subsequent poses already keyframed

  """

  ...

def push(factor: float = 0.5, prev_frame: int = 0, next_frame: int = 0, channels: str = 'ALL', axis_lock: str = 'FREE') -> None:

  """

  Exaggerate the current pose in regards to the breakdown pose

  """

  ...

def push_rest(factor: float = 0.5, prev_frame: int = 0, next_frame: int = 0, channels: str = 'ALL', axis_lock: str = 'FREE') -> None:

  """

  Push the current pose further away from the rest pose

  """

  ...

def quaternions_flip() -> None:

  """

  Flip quaternion values to achieve desired rotations, while maintaining the same orientations

  """

  ...

def relax(factor: float = 0.5, prev_frame: int = 0, next_frame: int = 0, channels: str = 'ALL', axis_lock: str = 'FREE') -> None:

  """

  Make the current pose more similar to its breakdown pose

  """

  ...

def relax_rest(factor: float = 0.5, prev_frame: int = 0, next_frame: int = 0, channels: str = 'ALL', axis_lock: str = 'FREE') -> None:

  """

  Make the current pose more similar to the rest pose

  """

  ...

def reveal(select: bool = True) -> None:

  """

  Reveal all bones hidden in Pose Mode

  """

  ...

def rot_clear() -> None:

  """

  Reset rotations of selected bones to their default values

  """

  ...

def rotation_mode_set(type: str = 'QUATERNION') -> None:

  """

  Set the rotation representation used by selected bones

  """

  ...

def scale_clear() -> None:

  """

  Reset scaling of selected bones to their default values

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Toggle selection status of all bones

  """

  ...

def select_constraint_target() -> None:

  """

  Select bones used as targets for the currently selected bones

  """

  ...

def select_grouped(extend: bool = False, type: str = 'LAYER') -> None:

  """

  Select all visible bones grouped by similar properties

  """

  ...

def select_hierarchy(direction: str = 'PARENT', extend: bool = False) -> None:

  """

  Select immediate parent/children of selected bones

  """

  ...

def select_linked() -> None:

  """

  Select all bones linked by parent/child connections to the current selection

  """

  ...

def select_linked_pick(extend: bool = False) -> None:

  """

  Select bones linked by parent/child connections under the mouse cursor

  """

  ...

def select_mirror(only_active: bool = False, extend: bool = False) -> None:

  """

  Mirror the bone selection

  """

  ...

def select_parent() -> None:

  """

  Select bones that are parents of the currently selected bones

  """

  ...

def transforms_clear() -> None:

  """

  Reset location, rotation, and scaling of selected bones to their default values

  """

  ...

def user_transforms_clear(only_selected: bool = True) -> None:

  """

  Reset pose bone transforms to keyframed state

  """

  ...

def visual_transform_apply() -> None:

  """

  Apply final constrained position of pose bones to their transform

  """

  ...
