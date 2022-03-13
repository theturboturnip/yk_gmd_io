"""


BMesh Geometry Utilities (bmesh.geometry)
*****************************************

This module provides access to bmesh geometry evaluation functions.

:func:`intersect_face_point`

"""

import typing

import bmesh

def intersect_face_point(self, face: bmesh.types.BMFace, point: float) -> bool:

  """

  Tests if the projection of a point is inside a face (using the face's normal).

  """

  ...
