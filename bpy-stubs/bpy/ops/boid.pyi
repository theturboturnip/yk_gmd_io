"""


Boid Operators
**************

:func:`rule_add`

:func:`rule_del`

:func:`rule_move_down`

:func:`rule_move_up`

:func:`state_add`

:func:`state_del`

:func:`state_move_down`

:func:`state_move_up`

"""

import typing

def rule_add(type: str = 'GOAL') -> None:

  """

  Add a boid rule to the current boid state

  """

  ...

def rule_del() -> None:

  """

  Delete current boid rule

  """

  ...

def rule_move_down() -> None:

  """

  Move boid rule down in the list

  """

  ...

def rule_move_up() -> None:

  """

  Move boid rule up in the list

  """

  ...

def state_add() -> None:

  """

  Add a boid state to the particle system

  """

  ...

def state_del() -> None:

  """

  Delete current boid state

  """

  ...

def state_move_down() -> None:

  """

  Move boid state down in the list

  """

  ...

def state_move_up() -> None:

  """

  Move boid state up in the list

  """

  ...
