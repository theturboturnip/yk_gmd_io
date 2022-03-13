"""


Workspace Operators
*******************

:func:`add`

:func:`append_activate`

:func:`delete`

:func:`duplicate`

:func:`reorder_to_back`

:func:`reorder_to_front`

"""

import typing

def add() -> None:

  """

  Add a new workspace by duplicating the current one or appending one from the user configuration

  """

  ...

def append_activate(idname: str = '', filepath: str = '') -> None:

  """

  Append a workspace and make it the active one in the current window

  """

  ...

def delete() -> None:

  """

  Delete the active workspace

  """

  ...

def duplicate() -> None:

  """

  Add a new workspace

  """

  ...

def reorder_to_back() -> None:

  """

  Reorder workspace to be first in the list

  """

  ...

def reorder_to_front() -> None:

  """

  Reorder workspace to be first in the list

  """

  ...
