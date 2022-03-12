"""


Poselib Operators
*****************

:func:`action_sanitize`

:func:`apply_pose`

:func:`apply_pose_asset`

:func:`apply_pose_asset_for_keymap`

:func:`blend_pose_asset`

:func:`blend_pose_asset_for_keymap`

:func:`browse_interactive`

:func:`convert_old_poselib`

:func:`copy_as_asset`

:func:`create_pose_asset`

:func:`new`

:func:`paste_asset`

:func:`pose_add`

:func:`pose_asset_select_bones`

:func:`pose_move`

:func:`pose_remove`

:func:`pose_rename`

:func:`restore_previous_action`

:func:`unlink`

"""

import typing

def action_sanitize() -> None:

  """

  Make action suitable for use as a Pose Library

  """

  ...

def apply_pose(pose_index: int = -1) -> None:

  """

  Apply specified Pose Library pose to the rig

  """

  ...

def apply_pose_asset(blend_factor: float = 1.0, flipped: bool = False) -> None:

  """

  Apply the given Pose Action to the rig

  """

  ...

def apply_pose_asset_for_keymap() -> None:

  """

  Apply the given Pose Action to the rig

  """

  ...

def blend_pose_asset(blend_factor: float = 0.0, flipped: bool = False, release_confirm: bool = False) -> None:

  """

  Blend the given Pose Action to the rig

  """

  ...

def blend_pose_asset_for_keymap() -> None:

  """

  Blend the given Pose Action to the rig

  """

  ...

def browse_interactive(pose_index: int = -1) -> None:

  """

  Interactively browse poses in 3D-View

  """

  ...

def convert_old_poselib() -> None:

  """

  Create a pose asset for each pose marker in the current action

  """

  ...

def copy_as_asset() -> None:

  """

  Create a new pose asset on the clipboard, to be pasted into an Asset Browser

  """

  ...

def create_pose_asset(pose_name: str = '', activate_new_action: bool = True) -> None:

  """

  Create a new Action that contains the pose of the selected bones, and mark it as Asset. The asset will be stored in the current blend file

  """

  ...

def new() -> None:

  """

  Add New Pose Library to active Object

  """

  ...

def paste_asset() -> None:

  """

  Paste the Asset that was previously copied using Copy As Asset

  """

  ...

def pose_add(frame: int = 1, name: str = 'Pose') -> None:

  """

  Add the current Pose to the active Pose Library

  """

  ...

def pose_asset_select_bones(select: bool = True, flipped: bool = False) -> None:

  """

  Select those bones that are used in this pose

  """

  ...

def pose_move(pose: str = '', direction: str = 'UP') -> None:

  """

  Move the pose up or down in the active Pose Library

  """

  ...

def pose_remove(pose: str = '') -> None:

  """

  Remove nth pose from the active Pose Library

  """

  ...

def pose_rename(name: str = 'RenamedPose', pose: str = '') -> None:

  """

  Rename specified pose from the active Pose Library

  """

  ...

def restore_previous_action() -> None:

  """

  Switch back to the previous Action, after creating a pose asset

  """

  ...

def unlink() -> None:

  """

  Remove Pose Library from active Object

  """

  ...
