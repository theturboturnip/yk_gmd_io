"""


Armature Operators
******************

:func:`align`

:func:`armature_layers`

:func:`autoside_names`

:func:`bone_layers`

:func:`bone_primitive_add`

:func:`calculate_roll`

:func:`click_extrude`

:func:`delete`

:func:`dissolve`

:func:`duplicate`

:func:`duplicate_move`

:func:`extrude`

:func:`extrude_forked`

:func:`extrude_move`

:func:`fill`

:func:`flip_names`

:func:`hide`

:func:`layers_show_all`

:func:`parent_clear`

:func:`parent_set`

:func:`reveal`

:func:`roll_clear`

:func:`select_all`

:func:`select_hierarchy`

:func:`select_less`

:func:`select_linked`

:func:`select_linked_pick`

:func:`select_mirror`

:func:`select_more`

:func:`select_similar`

:func:`separate`

:func:`shortest_path_pick`

:func:`split`

:func:`subdivide`

:func:`switch_direction`

:func:`symmetrize`

"""

import typing

def align() -> None:

  """

  Align selected bones to the active bone (or to their parent)

  """

  ...

def armature_layers(layers: typing.Tuple[bool, ...] = (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)) -> None:

  """

  Change the visible armature layers

  """

  ...

def autoside_names(type: str = 'XAXIS') -> None:

  """

  Automatically renames the selected bones according to which side of the target axis they fall on

  """

  ...

def bone_layers(layers: typing.Tuple[bool, ...] = (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)) -> None:

  """

  Change the layers that the selected bones belong to

  """

  ...

def bone_primitive_add(name: str = 'Bone') -> None:

  """

  Add a new bone located at the 3D cursor

  """

  ...

def calculate_roll(type: str = 'POS_X', axis_flip: bool = False, axis_only: bool = False) -> None:

  """

  Automatically fix alignment of select bones' axes

  """

  ...

def click_extrude() -> None:

  """

  Create a new bone going from the last selected joint to the mouse position

  """

  ...

def delete() -> None:

  """

  Remove selected bones from the armature

  """

  ...

def dissolve() -> None:

  """

  Dissolve selected bones from the armature

  """

  ...

def duplicate(do_flip_names: bool = False) -> None:

  """

  Make copies of the selected bones within the same armature

  """

  ...

def duplicate_move(ARMATURE_OT_duplicate: ARMATURE_OT_duplicate = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Make copies of the selected bones within the same armature and move them

  """

  ...

def extrude(forked: bool = False) -> None:

  """

  Create new bones from the selected joints

  """

  ...

def extrude_forked(ARMATURE_OT_extrude: ARMATURE_OT_extrude = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Create new bones from the selected joints and move them

  """

  ...

def extrude_move(ARMATURE_OT_extrude: ARMATURE_OT_extrude = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Create new bones from the selected joints and move them

  """

  ...

def fill() -> None:

  """

  Add bone between selected joint(s) and/or 3D cursor

  """

  ...

def flip_names(do_strip_numbers: bool = False) -> None:

  """

  Flips (and corrects) the axis suffixes of the names of selected bones

  """

  ...

def hide(unselected: bool = False) -> None:

  """

  Tag selected bones to not be visible in Edit Mode

  """

  ...

def layers_show_all(all: bool = True) -> None:

  """

  Make all armature layers visible

  """

  ...

def parent_clear(type: str = 'CLEAR') -> None:

  """

  Remove the parent-child relationship between selected bones and their parents

  """

  ...

def parent_set(type: str = 'CONNECTED') -> None:

  """

  Set the active bone as the parent of the selected bones

  """

  ...

def reveal(select: bool = True) -> None:

  """

  Reveal all bones hidden in Edit Mode

  """

  ...

def roll_clear(roll: float = 0.0) -> None:

  """

  Clear roll for selected bones

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Toggle selection status of all bones

  """

  ...

def select_hierarchy(direction: str = 'PARENT', extend: bool = False) -> None:

  """

  Select immediate parent/children of selected bones

  """

  ...

def select_less() -> None:

  """

  Deselect those bones at the boundary of each selection region

  """

  ...

def select_linked(all_forks: bool = False) -> None:

  """

  Select all bones linked by parent/child connections to the current selection

  """

  ...

def select_linked_pick(deselect: bool = False, all_forks: bool = False) -> None:

  """

  (De)select bones linked by parent/child connections under the mouse cursor

  """

  ...

def select_mirror(only_active: bool = False, extend: bool = False) -> None:

  """

  Mirror the bone selection

  """

  ...

def select_more() -> None:

  """

  Select those bones connected to the initial selection

  """

  ...

def select_similar(type: str = 'LENGTH', threshold: float = 0.1) -> None:

  """

  Select similar bones by property types

  """

  ...

def separate() -> None:

  """

  Isolate selected bones into a separate armature

  """

  ...

def shortest_path_pick() -> None:

  """

  Select shortest path between two bones

  """

  ...

def split() -> None:

  """

  Split off selected bones from connected unselected bones

  """

  ...

def subdivide(number_cuts: int = 1) -> None:

  """

  Break selected bones into chains of smaller bones

  """

  ...

def switch_direction() -> None:

  """

  Change the direction that a chain of bones points in (head and tail swap)

  """

  ...

def symmetrize(direction: str = 'NEGATIVE_X') -> None:

  """

  Enforce symmetry, make copies of the selection or use existing

  """

  ...
