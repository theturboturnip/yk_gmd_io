"""


Geometry Utilities (mathutils.geometry)
***************************************

The Blender geometry module

:func:`area_tri`

:func:`barycentric_transform`

:func:`box_fit_2d`

:func:`box_pack_2d`

:func:`closest_point_on_tri`

:func:`convex_hull_2d`

:func:`delaunay_2d_cdt`

:func:`distance_point_to_plane`

:func:`interpolate_bezier`

:func:`intersect_line_line`

:func:`intersect_line_line_2d`

:func:`intersect_line_plane`

:func:`intersect_line_sphere`

:func:`intersect_line_sphere_2d`

:func:`intersect_plane_plane`

:func:`intersect_point_line`

:func:`intersect_point_quad_2d`

:func:`intersect_point_tri`

:func:`intersect_point_tri_2d`

:func:`intersect_ray_tri`

:func:`intersect_sphere_sphere_2d`

:func:`intersect_tri_tri_2d`

:func:`normal`

:func:`points_in_planes`

:func:`tessellate_polygon`

:func:`volume_tetrahedron`

"""

import typing

import mathutils

def area_tri(v1: mathutils.Vector, v2: mathutils.Vector, v3: mathutils.Vector) -> float:

  """

  Returns the area size of the 2D or 3D triangle defined.

  """

  ...

def barycentric_transform(point: mathutils.Vector, tri_a1: mathutils.Vector, tri_a2: mathutils.Vector, tri_a3: mathutils.Vector, tri_b1: mathutils.Vector, tri_b2: mathutils.Vector, tri_b3: mathutils.Vector) -> typing.Any:

  """

  Return a transformed point, the transformation is defined by 2 triangles.

  """

  ...

def box_fit_2d(points: typing.List[typing.Any]) -> float:

  """

  Returns an angle that best fits the points to an axis aligned rectangle

  """

  ...

def box_pack_2d(boxes: typing.List[typing.Any]) -> typing.Tuple[typing.Any, ...]:

  """

  Returns a tuple with the width and height of the packed bounding box.

  """

  ...

def closest_point_on_tri(pt: mathutils.Vector, tri_p1: mathutils.Vector, tri_p2: mathutils.Vector, tri_p3: mathutils.Vector) -> mathutils.Vector:

  """

  Takes 4 vectors: one is the point and the next 3 define the triangle.

  """

  ...

def convex_hull_2d(points: typing.List[typing.Any]) -> typing.List[int]:

  """

  Returns a list of indices into the list given

  """

  ...

def delaunay_2d_cdt(vert_coords: typing.Any, edges: typing.Any, faces: typing.Any, output_type: typing.Any, epsilon: typing.Any, need_ids: typing.Any = True) -> None:

  """

  Computes the Constrained Delaunay Triangulation of a set of vertices,
with edges and faces that must appear in the triangulation.
Some triangles may be eaten away, or combined with other triangles,
according to output type.
The returned verts may be in a different order from input verts, may be moved
slightly, and may be merged with other nearby verts.
The three returned orig lists give, for each of verts, edges, and faces, the list of
input element indices corresponding to the positionally same output element.
For edges, the orig indices start with the input edges and then continue
with the edges implied by each of the faces (n of them for an n-gon).
If the need_ids argument is supplied, and False, then the code skips the preparation
of the orig arrays, which may save some time.
:arg vert_coords: Vertex coordinates (2d)
:type vert_coords: list of :class:`mathutils.Vector`
:arg edges: Edges, as pairs of indices in *vert_coords*
:type edges: list of (int, int)
:arg faces: Faces, each sublist is a face, as indices in *vert_coords* (CCW oriented)
:type faces: list of list of int
:arg output_type: What output looks like. 0 => triangles with convex hull. 1 => triangles inside constraints. 2 => the input constraints, intersected. 3 => like 2 but detect holes and omit them from output. 4 => like 2 but with extra edges to make valid BMesh faces. 5 => like 4 but detect holes and omit them from output.
:type output_type: intn   :arg epsilon: For nearness tests; should not be zero
:type epsilon: float
:arg need_ids: are the orig output arrays needed?
:type need_args: bool
:return: Output tuple, (vert_coords, edges, faces, orig_verts, orig_edges, orig_faces)
:rtype: (list of *mathutils.Vector*, list of (int, int), list of list of int, list of list of int, list of list of int, list of list of int)

  """

  ...

def distance_point_to_plane(pt: mathutils.Vector, plane_co: mathutils.Vector, plane_no: mathutils.Vector) -> float:

  """

  Returns the signed distance between a point and a plane    (negative when below the normal).

  """

  ...

def interpolate_bezier(knot1: mathutils.Vector, handle1: mathutils.Vector, handle2: mathutils.Vector, knot2: mathutils.Vector, resolution: int) -> typing.List[mathutils.Vector]:

  """

  Interpolate a bezier spline segment.

  """

  ...

def intersect_line_line(v1: mathutils.Vector, v2: mathutils.Vector, v3: mathutils.Vector, v4: mathutils.Vector) -> typing.Tuple[mathutils.Vector, ...]:

  """

  Returns a tuple with the points on each line respectively closest to the other.

  """

  ...

def intersect_line_line_2d(lineA_p1: mathutils.Vector, lineA_p2: mathutils.Vector, lineB_p1: mathutils.Vector, lineB_p2: mathutils.Vector) -> mathutils.Vector:

  """

  Takes 2 segments (defined by 4 vectors) and returns a vector for their point of intersection or None.

  Warning: Despite its name, this function works on segments, and not on lines.

  """

  ...

def intersect_line_plane(line_a: mathutils.Vector, line_b: mathutils.Vector, plane_co: mathutils.Vector, plane_no: mathutils.Vector, no_flip: typing.Any = False) -> mathutils.Vector:

  """

  Calculate the intersection between a line (as 2 vectors) and a plane.
Returns a vector for the intersection or None.

  """

  ...

def intersect_line_sphere(line_a: mathutils.Vector, line_b: mathutils.Vector, sphere_co: mathutils.Vector, sphere_radius: typing.Any, clip: typing.Any = True) -> typing.Any:

  """

  Takes a line (as 2 points) and a sphere (as a point and a radius) and
returns the intersection

  """

  ...

def intersect_line_sphere_2d(line_a: mathutils.Vector, line_b: mathutils.Vector, sphere_co: mathutils.Vector, sphere_radius: typing.Any, clip: typing.Any = True) -> typing.Any:

  """

  Takes a line (as 2 points) and a sphere (as a point and a radius) and
returns the intersection

  """

  ...

def intersect_plane_plane(plane_a_co: mathutils.Vector, plane_a_no: mathutils.Vector, plane_b_co: mathutils.Vector, plane_b_no: mathutils.Vector) -> typing.Tuple[typing.Any, ...]:

  """

  Return the intersection between two planes

  """

  ...

def intersect_point_line(pt: mathutils.Vector, line_p1: mathutils.Vector, line_p2: typing.Any) -> typing.Any:

  """

  Takes a point and a line and returns a tuple with the closest point on the line and its distance from the first point of the line as a percentage of the length of the line.

  """

  ...

def intersect_point_quad_2d(pt: mathutils.Vector, quad_p1: mathutils.Vector, quad_p2: mathutils.Vector, quad_p3: mathutils.Vector, quad_p4: mathutils.Vector) -> int:

  """

  Takes 5 vectors (using only the x and y coordinates): one is the point and the next 4 define the quad,
only the x and y are used from the vectors. Returns 1 if the point is within the quad, otherwise 0.
Works only with convex quads without singular edges.

  """

  ...

def intersect_point_tri(pt: mathutils.Vector, tri_p1: mathutils.Vector, tri_p2: mathutils.Vector, tri_p3: mathutils.Vector) -> mathutils.Vector:

  """

  Takes 4 vectors: one is the point and the next 3 define the triangle. Projects the point onto the triangle plane and checks if it is within the triangle.

  """

  ...

def intersect_point_tri_2d(pt: mathutils.Vector, tri_p1: mathutils.Vector, tri_p2: mathutils.Vector, tri_p3: mathutils.Vector) -> int:

  """

  Takes 4 vectors (using only the x and y coordinates): one is the point and the next 3 define the triangle. Returns 1 if the point is within the triangle, otherwise 0.

  """

  ...

def intersect_ray_tri(v1: mathutils.Vector, v2: mathutils.Vector, v3: mathutils.Vector, ray: mathutils.Vector, orig: mathutils.Vector, clip: bool = True) -> mathutils.Vector:

  """

  Returns the intersection between a ray and a triangle, if possible, returns None otherwise.

  """

  ...

def intersect_sphere_sphere_2d(p_a: mathutils.Vector, radius_a: float, p_b: mathutils.Vector, radius_b: float) -> typing.Tuple[mathutils.Vector, ...]:

  """

  Returns 2 points on between intersecting circles.

  """

  ...

def intersect_tri_tri_2d(tri_a1: typing.Any, tri_a2: typing.Any, tri_a3: typing.Any, tri_b1: typing.Any, tri_b2: typing.Any, tri_b3: typing.Any) -> bool:

  """

  Check if two 2D triangles intersect.

  """

  ...

def normal(vectors: typing.Sequence[typing.Any]) -> mathutils.Vector:

  """

  Returns the normal of a 3D polygon.

  """

  ...

def points_in_planes(planes: typing.List[mathutils.Vector]) -> typing.Tuple[typing.List[typing.Any], typing.List[typing.Any]]:

  """

  Returns a list of points inside all planes given and a list of index values for the planes used.

  """

  ...

def tessellate_polygon(veclist_list: typing.Any) -> typing.List[typing.Any]:

  """

  Takes a list of polylines (each point a pair or triplet of numbers) and returns the point indices for a polyline filled with triangles. Does not handle degenerate geometry (such as zero-length lines due to consecutive identical points).

  """

  ...

def volume_tetrahedron(v1: mathutils.Vector, v2: mathutils.Vector, v3: mathutils.Vector, v4: mathutils.Vector) -> float:

  """

  Return the volume formed by a tetrahedron (points can be in any order).

  """

  ...
