"""


Collection Operators
********************

:func:`create`

:func:`objects_add_active`

:func:`objects_remove`

:func:`objects_remove_active`

:func:`objects_remove_all`

"""

import typing

def create(name: str = 'Collection') -> None:

  """

  Create an object collection from selected objects

  """

  ...

def objects_add_active(collection: str = '') -> None:

  """

  Add the object to an object collection that contains the active object

  """

  ...

def objects_remove(collection: str = '') -> None:

  """

  Remove selected objects from a collection

  """

  ...

def objects_remove_active(collection: str = '') -> None:

  """

  Remove the object from an object collection that contains the active object

  """

  ...

def objects_remove_all() -> None:

  """

  Remove selected objects from all collections

  """

  ...
