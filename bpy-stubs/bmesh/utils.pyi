"""


BMesh Utilities (bmesh.utils)
*****************************

This module provides access to blenders bmesh data structures.

:func:`edge_rotate`

:func:`edge_split`

:func:`face_flip`

:func:`face_join`

:func:`face_split`

:func:`face_split_edgenet`

:func:`face_vert_separate`

:func:`loop_separate`

:func:`vert_collapse_edge`

:func:`vert_collapse_faces`

:func:`vert_dissolve`

:func:`vert_separate`

:func:`vert_splice`

"""

import typing

import bmesh

def edge_rotate(self, edge: bmesh.types.BMEdge, ccw: bool = False) -> bmesh.types.BMEdge:

  """

  Rotate the edge and return the newly created edge.
If rotating the edge fails, None will be returned.

  """

  ...

def edge_split(self, edge: bmesh.types.BMEdge, vert: bmesh.types.BMVert, fac: float) -> typing.Tuple[typing.Any, ...]:

  """

  Split an edge, return the newly created data.

  """

  ...

def face_flip(self, faces: typing.Any) -> None:

  """

  Flip the faces direction.

  """

  ...

def face_join(self, faces: bmesh.types.BMFace, remove: bool = True) -> bmesh.types.BMFace:

  """

  Joins a sequence of faces.

  """

  ...

def face_split(self, face: bmesh.types.BMFace, vert_a: bmesh.types.BMVert, vert_b: bmesh.types.BMVert, coords: typing.Sequence[float] = (), use_exist: bool = True, example: bmesh.types.BMEdge = None) -> typing.Any:

  """

  Face split with optional intermediate points.

  """

  ...

def face_split_edgenet(self, face: bmesh.types.BMFace, edgenet: bmesh.types.BMEdge) -> typing.Tuple[typing.Any, ...]:

  """

  Splits a face into any number of regions defined by an edgenet.

  Note: Regions defined by edges need to connect to the face, otherwise they're ignored as loose edges.

  """

  ...

def face_vert_separate(self, face: bmesh.types.BMFace, vert: bmesh.types.BMVert) -> None:

  """

  Rip a vertex in a face away and add a new vertex.

  Note: This is the same as loop_separate, and has only been added for convenience.

  """

  ...

def loop_separate(self, loop: bmesh.types.BMLoop) -> None:

  """

  Rip a vertex in a face away and add a new vertex.

  """

  ...

def vert_collapse_edge(self, vert: bmesh.types.BMVert, edge: bmesh.types.BMEdge) -> bmesh.types.BMEdge:

  """

  Collapse a vertex into an edge.

  """

  ...

def vert_collapse_faces(self, vert: bmesh.types.BMVert, edge: bmesh.types.BMEdge, fac: float, join_faces: bool) -> bmesh.types.BMEdge:

  """

  Collapses a vertex that has only two manifold edges onto a vertex it shares an edge with.

  """

  ...

def vert_dissolve(self, vert: bmesh.types.BMVert) -> bool:

  """

  Dissolve this vertex (will be removed).

  """

  ...

def vert_separate(self, vert: bmesh.types.BMVert, edges: bmesh.types.BMEdge) -> typing.Tuple[bmesh.types.BMVert, ...]:

  """

  Separate this vertex at every edge.

  """

  ...

def vert_splice(self, vert: bmesh.types.BMVert, vert_target: bmesh.types.BMVert) -> None:

  """

  Splice vert into vert_target.

  Note: The verts mustn't share an edge or face.

  """

  ...
