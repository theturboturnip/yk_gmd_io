"""


ID Property Access (idprop.types)
*********************************

:class:`IDPropertyArray`

:class:`IDPropertyGroup`

:class:`IDPropertyGroupIterItems`

:class:`IDPropertyGroupIterKeys`

:class:`IDPropertyGroupIterValues`

:class:`IDPropertyGroupViewItems`

:class:`IDPropertyGroupViewKeys`

:class:`IDPropertyGroupViewValues`

"""

import typing

class IDPropertyArray:

  def to_list(self) -> None:

    """

    Return the array as a list.

    """

    ...

  typecode: typing.Any = ...

  """

  The type of the data in the array {'f': float, 'd': double, 'i': int}.

  """

class IDPropertyGroup:

  """"""

  def clear(self) -> None:

    """

    Clear all members from this group.

    """

    ...

  def get(self, key: typing.Any, default: typing.Any = None) -> None:

    """

    Return the value for key, if it exists, else default.

    """

    ...

  def items(self) -> None:

    """

    Iterate through the items in the dict; behaves like dictionary method items.

    """

    ...

  def keys(self) -> None:

    """

    Return the keys associated with this group as a list of strings.

    """

    ...

  def pop(self, key: str, default: typing.Any) -> None:

    """

    Remove an item from the group, returning a Python representation.

    """

    ...

  def to_dict(self) -> None:

    """

    Return a purely python version of the group.

    """

    ...

  def update(self, other: typing.Union[IDPropertyGroup, typing.Dict[str, typing.Any]]) -> None:

    """

    Update key, values.

    """

    ...

  def values(self) -> None:

    """

    Return the values associated with this group.

    """

    ...

  name: typing.Any = ...

  """

  The name of this Group.

  """

class IDPropertyGroupIterItems:

  ...

class IDPropertyGroupIterKeys:

  ...

class IDPropertyGroupIterValues:

  ...

class IDPropertyGroupViewItems:

  ...

class IDPropertyGroupViewKeys:

  ...

class IDPropertyGroupViewValues:

  ...
