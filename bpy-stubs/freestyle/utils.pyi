"""


Freestyle Utilities (freestyle.utils)
*************************************

This module contains helper functions used for Freestyle style module
writing.

:func:`getCurrentScene`

:func:`integrate`

:func:`angle_x_normal`

:func:`bound`

:func:`bounding_box`

:func:`curvature_from_stroke_vertex`

:func:`find_matching_vertex`

:func:`get_chain_length`

:func:`get_object_name`

:func:`get_strokes`

:func:`get_test_stroke`

:func:`is_poly_clockwise`

:func:`iter_distance_along_stroke`

:func:`iter_distance_from_camera`

:func:`iter_distance_from_object`

:func:`iter_material_value`

:func:`iter_t2d_along_stroke`

:func:`material_from_fedge`

:func:`normal_at_I0D`

:func:`rgb_to_bw`

:func:`simplify`

:func:`stroke_curvature`

:func:`stroke_normal`

:func:`tripplewise`

:class:`BoundingBox`

:class:`StrokeCollector`

"""

import typing

import bpy

def getCurrentScene() -> bpy.types.Scene:

  """

  Returns the current scene.

  """

  ...

def integrate(func: UnaryFunction0D, it: Interface0DIterator, it_end: Interface0DIterator, integration_type: IntegrationType) -> typing.Union[int, float]:

  """

  Returns a single value from a set of values evaluated at each 0D
element of this 1D element.

  """

  ...

def angle_x_normal(it: typing.Any) -> None:

  """

  unsigned angle between a Point's normal and the X axis, in radians

  """

  ...

def bound(lower: typing.Any, x: typing.Any, higher: typing.Any) -> None:

  """

  Returns x bounded by a maximum and minimum value. Equivalent to:
    return min(max(x, lower), higher)

  """

  ...

def bounding_box(stroke: typing.Any) -> None:

  """

  Returns the maximum and minimum coordinates (the bounding box) of the stroke's vertices

  """

  ...

def curvature_from_stroke_vertex(svert: typing.Any) -> None:

  """

  The 3D curvature of an stroke vertex' underlying geometry
    The result is None or in the range [-inf, inf]

  """

  ...

def find_matching_vertex(id: typing.Any, it: typing.Any) -> None:

  """

  Finds the matching vertex, or returns None.

  """

  ...

def get_chain_length(ve: typing.Any, orientation: typing.Any) -> None:

  """

  Returns the 2d length of a given ViewEdge.

  """

  ...

def get_object_name(stroke: typing.Any) -> None:

  """

  Returns the name of the object that this stroke is drawn on.

  """

  ...

def get_strokes() -> None:

  """

  Get all strokes that are currently available

  """

  ...

def get_test_stroke() -> None:

  """

  Returns a static stroke object for testing

  """

  ...

def is_poly_clockwise(stroke: typing.Any) -> None:

  """

  True if the stroke is orientated in a clockwise way, False otherwise

  """

  ...

def iter_distance_along_stroke(stroke: typing.Any) -> None:

  """

  Yields the absolute distance along the stroke up to the current vertex.

  """

  ...

def iter_distance_from_camera(stroke: typing.Any, range_min: typing.Any, range_max: typing.Any, normfac: typing.Any) -> None:

  """

  Yields the distance to the camera relative to the maximum
possible distance for every stroke vertex, constrained by
given minimum and maximum values.

  """

  ...

def iter_distance_from_object(stroke: typing.Any, location: typing.Any, range_min: typing.Any, range_max: typing.Any, normfac: typing.Any) -> None:

  """

  yields the distance to the given object relative to the maximum
possible distance for every stroke vertex, constrained by
given minimum and maximum values.

  """

  ...

def iter_material_value(stroke: typing.Any, func: typing.Any, attribute: typing.Any) -> None:

  """

  Yields a specific material attribute from the vertex' underlying material.

  """

  ...

def iter_t2d_along_stroke(stroke: typing.Any) -> None:

  """

  Yields the progress along the stroke.

  """

  ...

def material_from_fedge(fe: typing.Any) -> None:

  """

  get the diffuse rgba color from an FEdge

  """

  ...

def normal_at_I0D(it: typing.Any) -> None:

  """

  Normal at an Interface0D object. In contrast to Normal2DF0D this
    function uses the actual data instead of underlying Fedge objects.

  """

  ...

def rgb_to_bw(r: typing.Any, g: typing.Any, b: typing.Any) -> None:

  """

  Method to convert rgb to a bw intensity value.

  """

  ...

def simplify(points: typing.Any, tolerance: typing.Any) -> None:

  """

  Simplifies a set of points

  """

  ...

def stroke_curvature(it: typing.Any) -> None:

  """

  Compute the 2D curvature at the stroke vertex pointed by the iterator 'it'.
K = 1 / R
where R is the radius of the circle going through the current vertex and its neighbors

  """

  ...

def stroke_normal(stroke: typing.Any) -> None:

  """

  Compute the 2D normal at the stroke vertex pointed by the iterator
'it'.  It is noted that Normal2DF0D computes normals based on
underlying FEdges instead, which is inappropriate for strokes when
they have already been modified by stroke geometry modifiers.

  The returned normals are dynamic: they update when the
vertex position (and therefore the vertex normal) changes.
for use in geometry modifiers it is advised to
cast this generator function to a tuple or list

  """

  ...

def tripplewise(iterable: typing.Any) -> None:

  """

  Yields a tuple containing the current object and its immediate neighbors

  """

  ...

class BoundingBox:

  """

  Object representing a bounding box consisting out of 2 2D vectors

  """

  def inside(self, other: typing.Any) -> None:

    """

    True if self inside other, False otherwise

    """

    ...

class StrokeCollector:

  """

  Collects and Stores stroke objects

  """

  def shade(self, stroke: typing.Any) -> None:

    ...
