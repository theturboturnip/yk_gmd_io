"""


bpy_extras submodule (bpy_extras.mesh_utils)
********************************************

:func:`mesh_linked_uv_islands`

:func:`mesh_linked_triangles`

:func:`edge_face_count_dict`

:func:`edge_face_count`

:func:`edge_loops_from_edges`

:func:`ngon_tessellate`

:func:`triangle_random_points`

"""

import typing

import bpy

def mesh_linked_uv_islands(mesh: bpy.types.Mesh) -> typing.List[typing.Any]:

  """

  Splits the mesh into connected polygons, use this for separating cubes from
other mesh elements within 1 mesh datablock.

  """

  ...

def mesh_linked_triangles(mesh: bpy.types.Mesh) -> typing.List[typing.Any]:

  """

  Splits the mesh into connected triangles, use this for separating cubes from
other mesh elements within 1 mesh datablock.

  """

  ...

def edge_face_count_dict(mesh: typing.Any) -> typing.Dict[str, typing.Any]:

  ...

def edge_face_count(mesh: typing.Any) -> typing.List[typing.Any]:

  ...

def edge_loops_from_edges(mesh: typing.Any, edges: typing.Any = None) -> None:

  """

  Edge loops defined by edges

  Takes me.edges or a list of edges and returns the edge loops

  return a list of vertex indices.
[ [1, 6, 7, 2], ...]

  closed loops have matching start and end values.

  """

  ...

def ngon_tessellate(from_data: typing.Union[typing.List[typing.Any], bpy.types.Mesh], indices: typing.List[typing.Any], fix_loops: bool = True, debug_print: typing.Any = True) -> None:

  """

  Takes a polyline of indices (ngon) and returns a list of face
index lists. Designed to be used for importers that need indices for an
ngon to create from existing verts.

  """

  ...

def triangle_random_points(num_points: typing.Any, loop_triangles: bpy.types.MeshLoopTriangle) -> typing.List[typing.Any]:

  """

  Generates a list of random points over mesh loop triangles.

  """

  ...
