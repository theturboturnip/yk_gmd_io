"""


Particle Operators
******************

:func:`brush_edit`

:func:`connect_hair`

:func:`copy_particle_systems`

:func:`delete`

:func:`disconnect_hair`

:func:`duplicate_particle_system`

:func:`dupliob_copy`

:func:`dupliob_move_down`

:func:`dupliob_move_up`

:func:`dupliob_refresh`

:func:`dupliob_remove`

:func:`edited_clear`

:func:`hair_dynamics_preset_add`

:func:`hide`

:func:`mirror`

:func:`new`

:func:`new_target`

:func:`particle_edit_toggle`

:func:`rekey`

:func:`remove_doubles`

:func:`reveal`

:func:`select_all`

:func:`select_less`

:func:`select_linked`

:func:`select_linked_pick`

:func:`select_more`

:func:`select_random`

:func:`select_roots`

:func:`select_tips`

:func:`shape_cut`

:func:`subdivide`

:func:`target_move_down`

:func:`target_move_up`

:func:`target_remove`

:func:`unify_length`

:func:`weight_set`

"""

import typing

def brush_edit(stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None) -> None:

  """

  Apply a stroke of brush to the particles

  """

  ...

def connect_hair(all: bool = False) -> None:

  """

  Connect hair to the emitter mesh

  """

  ...

def copy_particle_systems(space: str = 'OBJECT', remove_target_particles: bool = True, use_active: bool = False) -> None:

  """

  Copy particle systems from the active object to selected objects

  """

  ...

def delete(type: str = 'PARTICLE') -> None:

  """

  Delete selected particles or keys

  """

  ...

def disconnect_hair(all: bool = False) -> None:

  """

  Disconnect hair from the emitter mesh

  """

  ...

def duplicate_particle_system(use_duplicate_settings: bool = False) -> None:

  """

  Duplicate particle system within the active object

  """

  ...

def dupliob_copy() -> None:

  """

  Duplicate the current instance object

  """

  ...

def dupliob_move_down() -> None:

  """

  Move instance object down in the list

  """

  ...

def dupliob_move_up() -> None:

  """

  Move instance object up in the list

  """

  ...

def dupliob_refresh() -> None:

  """

  Refresh list of instance objects and their weights

  """

  ...

def dupliob_remove() -> None:

  """

  Remove the selected instance object

  """

  ...

def edited_clear() -> None:

  """

  Undo all edition performed on the particle system

  """

  ...

def hair_dynamics_preset_add(name: str = '', remove_name: bool = False, remove_active: bool = False) -> None:

  """

  Add or remove a Hair Dynamics Preset

  """

  ...

def hide(unselected: bool = False) -> None:

  """

  Hide selected particles

  """

  ...

def mirror() -> None:

  """

  Duplicate and mirror the selected particles along the local X axis

  """

  ...

def new() -> None:

  """

  Add new particle settings

  """

  ...

def new_target() -> None:

  """

  Add a new particle target

  """

  ...

def particle_edit_toggle() -> None:

  """

  Toggle particle edit mode

  """

  ...

def rekey(keys_number: int = 2) -> None:

  """

  Change the number of keys of selected particles (root and tip keys included)

  """

  ...

def remove_doubles(threshold: float = 0.0002) -> None:

  """

  Remove selected particles close enough of others

  """

  ...

def reveal(select: bool = True) -> None:

  """

  Show hidden particles

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  (De)select all particles' keys

  """

  ...

def select_less() -> None:

  """

  Deselect boundary selected keys of each particle

  """

  ...

def select_linked() -> None:

  """

  Select all keys linked to already selected ones

  """

  ...

def select_linked_pick(deselect: bool = False, location: typing.Tuple[int, int] = (0, 0)) -> None:

  """

  Select nearest particle from mouse pointer

  """

  ...

def select_more() -> None:

  """

  Select keys linked to boundary selected keys of each particle

  """

  ...

def select_random(ratio: float = 0.5, seed: int = 0, action: str = 'SELECT', type: str = 'HAIR') -> None:

  """

  Select a randomly distributed set of hair or points

  """

  ...

def select_roots(action: str = 'SELECT') -> None:

  """

  Select roots of all visible particles

  """

  ...

def select_tips(action: str = 'SELECT') -> None:

  """

  Select tips of all visible particles

  """

  ...

def shape_cut() -> None:

  """

  Cut hair to conform to the set shape object

  """

  ...

def subdivide() -> None:

  """

  Subdivide selected particles segments (adds keys)

  """

  ...

def target_move_down() -> None:

  """

  Move particle target down in the list

  """

  ...

def target_move_up() -> None:

  """

  Move particle target up in the list

  """

  ...

def target_remove() -> None:

  """

  Remove the selected particle target

  """

  ...

def unify_length() -> None:

  """

  Make selected hair the same length

  """

  ...

def weight_set(factor: float = 1.0) -> None:

  """

  Set the weight of selected keys

  """

  ...
