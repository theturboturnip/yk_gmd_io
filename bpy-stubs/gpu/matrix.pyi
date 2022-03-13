"""


GPU Matrix Utilities (gpu.matrix)
*********************************

This module provides access to the matrix stack.

:func:`get_model_view_matrix`

:func:`get_normal_matrix`

:func:`get_projection_matrix`

:func:`load_identity`

:func:`load_matrix`

:func:`load_projection_matrix`

:func:`multiply_matrix`

:func:`pop`

:func:`pop_projection`

:func:`push`

:func:`push_pop`

:func:`push_pop_projection`

:func:`push_projection`

:func:`reset`

:func:`scale`

:func:`scale_uniform`

:func:`translate`

"""

import typing

import mathutils

def get_model_view_matrix() -> mathutils.Matrix:

  """

  Return a copy of the model-view matrix.

  """

  ...

def get_normal_matrix() -> mathutils.Matrix:

  """

  Return a copy of the normal matrix.

  """

  ...

def get_projection_matrix() -> mathutils.Matrix:

  """

  Return a copy of the projection matrix.

  """

  ...

def load_identity() -> None:

  """

  Empty stack and set to identity.

  """

  ...

def load_matrix(matrix: mathutils.Matrix) -> None:

  """

  Load a matrix into the stack.

  """

  ...

def load_projection_matrix(matrix: mathutils.Matrix) -> None:

  """

  Load a projection matrix into the stack.

  """

  ...

def multiply_matrix(matrix: mathutils.Matrix) -> None:

  """

  Multiply the current stack matrix.

  """

  ...

def pop() -> None:

  """

  Remove the last model-view matrix from the stack.

  """

  ...

def pop_projection() -> None:

  """

  Remove the last projection matrix from the stack.

  """

  ...

def push() -> None:

  """

  Add to the model-view matrix stack.

  """

  ...

def push_pop() -> None:

  """

  Context manager to ensure balanced push/pop calls, even in the case of an error.

  """

  ...

def push_pop_projection() -> None:

  """

  Context manager to ensure balanced push/pop calls, even in the case of an error.

  """

  ...

def push_projection() -> None:

  """

  Add to the projection matrix stack.

  """

  ...

def reset() -> None:

  """

  Empty stack and set to identity.

  """

  ...

def scale(scale: typing.Sequence[typing.Any]) -> None:

  """

  Scale the current stack matrix.

  """

  ...

def scale_uniform(scale: float) -> None:

  ...

def translate(offset: typing.Sequence[typing.Any]) -> None:

  """

  Scale the current stack matrix.

  """

  ...
