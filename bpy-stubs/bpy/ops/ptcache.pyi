"""


Ptcache Operators
*****************

:func:`add`

:func:`bake`

:func:`bake_all`

:func:`bake_from_cache`

:func:`free_bake`

:func:`free_bake_all`

:func:`remove`

"""

import typing

def add() -> None:

  """

  Add new cache

  """

  ...

def bake(bake: bool = False) -> None:

  """

  Bake physics

  """

  ...

def bake_all(bake: bool = True) -> None:

  """

  Bake all physics

  """

  ...

def bake_from_cache() -> None:

  """

  Bake from cache

  """

  ...

def free_bake() -> None:

  """

  Delete physics bake

  """

  ...

def free_bake_all() -> None:

  """

  Delete all baked caches of all objects in the current scene

  """

  ...

def remove() -> None:

  """

  Delete current cache

  """

  ...
