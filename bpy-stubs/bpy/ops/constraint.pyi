"""


Constraint Operators
********************

:func:`add_target`

:func:`apply`

:func:`childof_clear_inverse`

:func:`childof_set_inverse`

:func:`copy`

:func:`copy_to_selected`

:func:`delete`

:func:`disable_keep_transform`

:func:`followpath_path_animate`

:func:`limitdistance_reset`

:func:`move_down`

:func:`move_to_index`

:func:`move_up`

:func:`normalize_target_weights`

:func:`objectsolver_clear_inverse`

:func:`objectsolver_set_inverse`

:func:`remove_target`

:func:`stretchto_reset`

"""

import typing

def add_target() -> None:

  """

  Add a target to the constraint

  """

  ...

def apply(constraint: str = '', owner: str = 'OBJECT', report: bool = False) -> None:

  """

  Apply constraint and remove from the stack

  """

  ...

def childof_clear_inverse(constraint: str = '', owner: str = 'OBJECT') -> None:

  """

  Clear inverse correction for Child Of constraint

  """

  ...

def childof_set_inverse(constraint: str = '', owner: str = 'OBJECT') -> None:

  """

  Set inverse correction for Child Of constraint

  """

  ...

def copy(constraint: str = '', owner: str = 'OBJECT', report: bool = False) -> None:

  """

  Duplicate constraint at the same position in the stack

  """

  ...

def copy_to_selected(constraint: str = '', owner: str = 'OBJECT') -> None:

  """

  Copy constraint to other selected objects/bones

  """

  ...

def delete(constraint: str = '', owner: str = 'OBJECT', report: bool = False) -> None:

  """

  Remove constraint from constraint stack

  """

  ...

def disable_keep_transform() -> None:

  """

  Set the influence of this constraint to zero while trying to maintain the object's transformation. Other active constraints can still influence the final transformation

  """

  ...

def followpath_path_animate(constraint: str = '', owner: str = 'OBJECT', frame_start: int = 1, length: int = 100) -> None:

  """

  Add default animation for path used by constraint if it isn't animated already

  """

  ...

def limitdistance_reset(constraint: str = '', owner: str = 'OBJECT') -> None:

  """

  Reset limiting distance for Limit Distance Constraint

  """

  ...

def move_down(constraint: str = '', owner: str = 'OBJECT') -> None:

  """

  Move constraint down in constraint stack

  """

  ...

def move_to_index(constraint: str = '', owner: str = 'OBJECT', index: int = 0) -> None:

  """

  Change the constraint's position in the list so it evaluates after the set number of others

  """

  ...

def move_up(constraint: str = '', owner: str = 'OBJECT') -> None:

  """

  Move constraint up in constraint stack

  """

  ...

def normalize_target_weights() -> None:

  """

  Normalize weights of all target bones

  """

  ...

def objectsolver_clear_inverse(constraint: str = '', owner: str = 'OBJECT') -> None:

  """

  Clear inverse correction for Object Solver constraint

  """

  ...

def objectsolver_set_inverse(constraint: str = '', owner: str = 'OBJECT') -> None:

  """

  Set inverse correction for Object Solver constraint

  """

  ...

def remove_target(index: int = 0) -> None:

  """

  Remove the target from the constraint

  """

  ...

def stretchto_reset(constraint: str = '', owner: str = 'OBJECT') -> None:

  """

  Reset original length of bone for Stretch To Constraint

  """

  ...
