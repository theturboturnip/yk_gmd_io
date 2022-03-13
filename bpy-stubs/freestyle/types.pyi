"""


Freestyle Types (freestyle.types)
*********************************

This module contains core classes of the Freestyle Python API,
including data types of view map components (0D and 1D elements), base
classes for user-defined line stylization rules (predicates,
functions, chaining iterators, and stroke shaders), and operators.

Class hierarchy:

* :class:`BBox`

* :class:`BinaryPredicate0D`

* :class:`BinaryPredicate1D`

* :class:`Id`

* :class:`Interface0D`

  * :class:`CurvePoint`

    * :class:`StrokeVertex`

  * :class:`SVertex`

  * :class:`ViewVertex`

    * :class:`NonTVertex`

    * :class:`TVertex`

* :class:`Interface1D`

  * :class:`Curve`

    * :class:`Chain`

  * :class:`FEdge`

    * :class:`FEdgeSharp`

    * :class:`FEdgeSmooth`

  * :class:`Stroke`

  * :class:`ViewEdge`

* :class:`Iterator`

  * :class:`AdjacencyIterator`

  * :class:`CurvePointIterator`

  * :class:`Interface0DIterator`

  * :class:`SVertexIterator`

  * :class:`StrokeVertexIterator`

  * :class:`ViewEdgeIterator`

    * :class:`ChainingIterator`

  * :class:`orientedViewEdgeIterator`

* :class:`Material`

* :class:`Noise`

* :class:`Operators`

* :class:`SShape`

* :class:`StrokeAttribute`

* :class:`StrokeShader`

* :class:`UnaryFunction0D`

  * :class:`UnaryFunction0DDouble`

  * :class:`UnaryFunction0DEdgeNature`

  * :class:`UnaryFunction0DFloat`

  * :class:`UnaryFunction0DId`

  * :class:`UnaryFunction0DMaterial`

  * :class:`UnaryFunction0DUnsigned`

  * :class:`UnaryFunction0DVec2f`

  * :class:`UnaryFunction0DVec3f`

  * :class:`UnaryFunction0DVectorViewShape`

  * :class:`UnaryFunction0DViewShape`

* :class:`UnaryFunction1D`

  * :class:`UnaryFunction1DDouble`

  * :class:`UnaryFunction1DEdgeNature`

  * :class:`UnaryFunction1DFloat`

  * :class:`UnaryFunction1DUnsigned`

  * :class:`UnaryFunction1DVec2f`

  * :class:`UnaryFunction1DVec3f`

  * :class:`UnaryFunction1DVectorViewShape`

  * :class:`UnaryFunction1DVoid`

* :class:`UnaryPredicate0D`

* :class:`UnaryPredicate1D`

* :class:`ViewMap`

* :class:`ViewShape`

* :class:`IntegrationType`

* :class:`MediumType`

* :class:`Nature`

:class:`AdjacencyIterator`

:class:`BBox`

:class:`BinaryPredicate0D`

:class:`BinaryPredicate1D`

:class:`Chain`

:class:`ChainingIterator`

:class:`Curve`

:class:`CurvePoint`

:class:`CurvePointIterator`

:class:`FEdge`

:class:`FEdgeSharp`

:class:`FEdgeSmooth`

:class:`Id`

:class:`IntegrationType`

:class:`Interface0D`

:class:`Interface0DIterator`

:class:`Interface1D`

:class:`Iterator`

:class:`Material`

:class:`MediumType`

:class:`Nature`

:class:`Noise`

:class:`NonTVertex`

:class:`Operators`

:class:`SShape`

:class:`SVertex`

:class:`SVertexIterator`

:class:`Stroke`

:class:`StrokeAttribute`

:class:`StrokeShader`

:class:`StrokeVertex`

:class:`StrokeVertexIterator`

:class:`TVertex`

:class:`UnaryFunction0D`

:class:`UnaryFunction0DDouble`

:class:`UnaryFunction0DEdgeNature`

:class:`UnaryFunction0DFloat`

:class:`UnaryFunction0DId`

:class:`UnaryFunction0DMaterial`

:class:`UnaryFunction0DUnsigned`

:class:`UnaryFunction0DVec2f`

:class:`UnaryFunction0DVec3f`

:class:`UnaryFunction0DVectorViewShape`

:class:`UnaryFunction0DViewShape`

:class:`UnaryFunction1D`

:class:`UnaryFunction1DDouble`

:class:`UnaryFunction1DEdgeNature`

:class:`UnaryFunction1DFloat`

:class:`UnaryFunction1DUnsigned`

:class:`UnaryFunction1DVec2f`

:class:`UnaryFunction1DVec3f`

:class:`UnaryFunction1DVectorViewShape`

:class:`UnaryFunction1DVoid`

:class:`UnaryPredicate0D`

:class:`UnaryPredicate1D`

:class:`ViewEdge`

:class:`ViewEdgeIterator`

:class:`ViewMap`

:class:`ViewShape`

:class:`ViewVertex`

:class:`orientedViewEdgeIterator`

"""

import typing

import mathutils

class AdjacencyIterator:

  """

  Class hierarchy: :class:`Iterator` > :class:`AdjacencyIterator`

  Class for representing adjacency iterators used in the chaining
process.  An AdjacencyIterator is created in the increment() and
decrement() methods of a :class:`ChainingIterator` and passed to the
traverse() method of the ChainingIterator.

  """

  def __init__(self) -> None:

    """

    Builds an :class:`AdjacencyIterator` using the default constructor,
copy constructor or the overloaded constructor.

    """

    ...

  def __init__(self, brother: AdjacencyIterator) -> None:

    """

    Builds an :class:`AdjacencyIterator` using the default constructor,
copy constructor or the overloaded constructor.

    """

    ...

  def __init__(self, vertex: ViewVertex, restrict_to_selection: bool = True, restrict_to_unvisited: bool = True) -> None:

    """

    Builds an :class:`AdjacencyIterator` using the default constructor,
copy constructor or the overloaded constructor.

    """

    ...

  is_incoming: bool = ...

  """

  True if the current ViewEdge is coming towards the iteration vertex, and
False otherwise.

  """

  object: ViewEdge = ...

  """

  The ViewEdge object currently pointed to by this iterator.

  """

class BBox:

  """

  Class for representing a bounding box.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

class BinaryPredicate0D:

  """

  Base class for binary predicates working on :class:`Interface0D`
objects.  A BinaryPredicate0D is typically an ordering relation
between two Interface0D objects.  The predicate evaluates a relation
between the two Interface0D instances and returns a boolean value (true
or false).  It is used by invoking the __call__() method.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

  def __call__(self, inter1: Interface0D, inter2: Interface0D) -> bool:

    """

    Must be overload by inherited classes.  It evaluates a relation
between two Interface0D objects.

    """

    ...

  name: str = ...

  """

  The name of the binary 0D predicate.

  """

class BinaryPredicate1D:

  """

  Base class for binary predicates working on :class:`Interface1D`
objects.  A BinaryPredicate1D is typically an ordering relation
between two Interface1D objects.  The predicate evaluates a relation
between the two Interface1D instances and returns a boolean value (true
or false).  It is used by invoking the __call__() method.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

  def __call__(self, inter1: Interface1D, inter2: Interface1D) -> bool:

    """

    Must be overload by inherited classes. It evaluates a relation
between two Interface1D objects.

    """

    ...

  name: str = ...

  """

  The name of the binary 1D predicate.

  """

class Chain:

  """

  Class hierarchy: :class:`Interface1D` > :class:`Curve` > :class:`Chain`

  Class to represent a 1D elements issued from the chaining process.  A
Chain is the last step before the :class:`Stroke` and is used in the
Splitting and Creation processes.

  """

  def __init__(self) -> None:

    """

    Builds a :class:`Chain` using the default constructor,
copy constructor or from an :class:`Id`.

    """

    ...

  def __init__(self, brother: Chain) -> None:

    """

    Builds a :class:`Chain` using the default constructor,
copy constructor or from an :class:`Id`.

    """

    ...

  def __init__(self, id: Id) -> None:

    """

    Builds a :class:`Chain` using the default constructor,
copy constructor or from an :class:`Id`.

    """

    ...

  def push_viewedge_back(self, viewedge: ViewEdge, orientation: bool) -> None:

    """

    Adds a ViewEdge at the end of the Chain.

    """

    ...

  def push_viewedge_front(self, viewedge: ViewEdge, orientation: bool) -> None:

    """

    Adds a ViewEdge at the beginning of the Chain.

    """

    ...

class ChainingIterator:

  """

  Class hierarchy: :class:`Iterator` > :class:`ViewEdgeIterator` > :class:`ChainingIterator`

  Base class for chaining iterators.  This class is designed to be
overloaded in order to describe chaining rules.  It makes the
description of chaining rules easier.  The two main methods that need
to overloaded are traverse() and init().  traverse() tells which
:class:`ViewEdge` to follow, among the adjacent ones.  If you specify
restriction rules (such as "Chain only ViewEdges of the selection"),
they will be included in the adjacency iterator (i.e, the adjacent
iterator will only stop on "valid" edges).

  """

  def __init__(self, restrict_to_selection: bool = True, restrict_to_unvisited: bool = True, begin: ViewEdge = None, orientation: bool = True) -> None:

    """

    Builds a Chaining Iterator from the first ViewEdge used for
iteration and its orientation or by using the copy constructor.

    """

    ...

  def __init__(self, brother: typing.Any) -> None:

    """

    Builds a Chaining Iterator from the first ViewEdge used for
iteration and its orientation or by using the copy constructor.

    """

    ...

  def init(self) -> None:

    """

    Initializes the iterator context.  This method is called each
time a new chain is started.  It can be used to reset some
history information that you might want to keep.

    """

    ...

  def traverse(self, it: AdjacencyIterator) -> ViewEdge:

    """

    This method iterates over the potential next ViewEdges and returns
the one that will be followed next.  Returns the next ViewEdge to
follow or None when the end of the chain is reached.

    """

    ...

  is_incrementing: bool = ...

  """

  True if the current iteration is an incrementation.

  """

  next_vertex: ViewVertex = ...

  """

  The ViewVertex that is the next crossing.

  """

  object: ViewEdge = ...

  """

  The ViewEdge object currently pointed by this iterator.

  """

class Curve:

  """

  Class hierarchy: :class:`Interface1D` > :class:`Curve`

  Base class for curves made of CurvePoints.  :class:`SVertex` is the
type of the initial curve vertices.  A :class:`Chain` is a
specialization of a Curve.

  """

  def __init__(self) -> None:

    """

    Builds a :class:`FrsCurve` using a default constructor,
copy constructor or from an :class:`Id`.

    """

    ...

  def __init__(self, brother: Curve) -> None:

    """

    Builds a :class:`FrsCurve` using a default constructor,
copy constructor or from an :class:`Id`.

    """

    ...

  def __init__(self, id: Id) -> None:

    """

    Builds a :class:`FrsCurve` using a default constructor,
copy constructor or from an :class:`Id`.

    """

    ...

  def push_vertex_back(self, vertex: typing.Union[SVertex, CurvePoint]) -> None:

    """

    Adds a single vertex at the end of the Curve.

    """

    ...

  def push_vertex_front(self, vertex: typing.Union[SVertex, CurvePoint]) -> None:

    """

    Adds a single vertex at the front of the Curve.

    """

    ...

  is_empty: bool = ...

  """

  True if the Curve doesn't have any Vertex yet.

  """

  segments_size: int = ...

  """

  The number of segments in the polyline constituting the Curve.

  """

class CurvePoint:

  """

  Class hierarchy: :class:`Interface0D` > :class:`CurvePoint`

  Class to represent a point of a curve.  A CurvePoint can be any point
of a 1D curve (it doesn't have to be a vertex of the curve).  Any
:class:`Interface1D` is built upon ViewEdges, themselves built upon
FEdges.  Therefore, a curve is basically a polyline made of a list of
:class:`SVertex` objects.  Thus, a CurvePoint is built by linearly
interpolating two :class:`SVertex` instances.  CurvePoint can be used
as virtual points while querying 0D information along a curve at a
given resolution.

  """

  def __init__(self) -> None:

    """

    Builds a CurvePoint using the default constructor, copy constructor,
or one of the overloaded constructors. The over loaded constructors
can either take two :class:`SVertex` or two :class:`CurvePoint`
objects and an interpolation parameter

    """

    ...

  def __init__(self, brother: CurvePoint) -> None:

    """

    Builds a CurvePoint using the default constructor, copy constructor,
or one of the overloaded constructors. The over loaded constructors
can either take two :class:`SVertex` or two :class:`CurvePoint`
objects and an interpolation parameter

    """

    ...

  def __init__(self, first_vertex: SVertex, second_vertex: SVertex, t2d: float) -> None:

    """

    Builds a CurvePoint using the default constructor, copy constructor,
or one of the overloaded constructors. The over loaded constructors
can either take two :class:`SVertex` or two :class:`CurvePoint`
objects and an interpolation parameter

    """

    ...

  def __init__(self, first_point: CurvePoint, second_point: CurvePoint, t2d: float) -> None:

    """

    Builds a CurvePoint using the default constructor, copy constructor,
or one of the overloaded constructors. The over loaded constructors
can either take two :class:`SVertex` or two :class:`CurvePoint`
objects and an interpolation parameter

    """

    ...

  fedge: FEdge = ...

  """

  Gets the FEdge for the two SVertices that given CurvePoints consists out of.
A shortcut for CurvePoint.first_svertex.get_fedge(CurvePoint.second_svertex).

  """

  first_svertex: SVertex = ...

  """

  The first SVertex upon which the CurvePoint is built.

  """

  second_svertex: SVertex = ...

  """

  The second SVertex upon which the CurvePoint is built.

  """

  t2d: float = ...

  """

  The 2D interpolation parameter.

  """

class CurvePointIterator:

  """

  Class hierarchy: :class:`Iterator` > :class:`CurvePointIterator`

  Class representing an iterator on a curve.  Allows an iterating
outside initial vertices.  A CurvePoint is instantiated and returned
through the .object attribute.

  """

  def __init__(self) -> None:

    """

    Builds a CurvePointIterator object using either the default constructor,
copy constructor, or the overloaded constructor.

    """

    ...

  def __init__(self, brother: CurvePointIterator) -> None:

    """

    Builds a CurvePointIterator object using either the default constructor,
copy constructor, or the overloaded constructor.

    """

    ...

  def __init__(self, step: float = 0.0) -> None:

    """

    Builds a CurvePointIterator object using either the default constructor,
copy constructor, or the overloaded constructor.

    """

    ...

  object: CurvePoint = ...

  """

  The CurvePoint object currently pointed by this iterator.

  """

  t: float = ...

  """

  The curvilinear abscissa of the current point.

  """

  u: float = ...

  """

  The point parameter at the current point in the stroke (0 <= u <= 1).

  """

class FEdge:

  """

  Class hierarchy: :class:`Interface1D` > :class:`FEdge`

  Base Class for feature edges.  This FEdge can represent a silhouette,
a crease, a ridge/valley, a border or a suggestive contour.  For
silhouettes, the FEdge is oriented so that the visible face lies on
the left of the edge.  For borders, the FEdge is oriented so that the
face lies on the left of the edge.  An FEdge can represent an initial
edge of the mesh or runs across a face of the initial mesh depending
on the smoothness or sharpness of the mesh.  This class is specialized
into a smooth and a sharp version since their properties slightly vary
from one to the other.

  """

  def FEdge(self) -> None:

    """

    Builds an :class:`FEdge` using the default constructor,
copy constructor, or between two :class:`SVertex` objects.

    """

    ...

  def FEdge(self, brother: FEdge) -> None:

    """

    Builds an :class:`FEdge` using the default constructor,
copy constructor, or between two :class:`SVertex` objects.

    """

    ...

  first_svertex: SVertex = ...

  """

  The first SVertex constituting this FEdge.

  """

  id: Id = ...

  """

  The Id of this FEdge.

  """

  is_smooth: bool = ...

  """

  True if this FEdge is a smooth FEdge.

  """

  nature: Nature = ...

  """

  The nature of this FEdge.

  """

  next_fedge: FEdge = ...

  """

  The FEdge following this one in the ViewEdge.  The value is None if
this FEdge is the last of the ViewEdge.

  """

  previous_fedge: FEdge = ...

  """

  The FEdge preceding this one in the ViewEdge.  The value is None if
this FEdge is the first one of the ViewEdge.

  """

  second_svertex: SVertex = ...

  """

  The second SVertex constituting this FEdge.

  """

  viewedge: ViewEdge = ...

  """

  The ViewEdge to which this FEdge belongs to.

  """

class FEdgeSharp:

  """

  Class hierarchy: :class:`Interface1D` > :class:`FEdge` > :class:`FEdgeSharp`

  Class defining a sharp FEdge.  A Sharp FEdge corresponds to an initial
edge of the input mesh.  It can be a silhouette, a crease or a border.
If it is a crease edge, then it is bordered by two faces of the mesh.
Face a lies on its right whereas Face b lies on its left.  If it is a
border edge, then it doesn't have any face on its right, and thus Face
a is None.

  """

  def __init__(self) -> None:

    """

    Builds an :class:`FEdgeSharp` using the default constructor,
copy constructor, or between two :class:`SVertex` objects.

    """

    ...

  def __init__(self, brother: FEdgeSharp) -> None:

    """

    Builds an :class:`FEdgeSharp` using the default constructor,
copy constructor, or between two :class:`SVertex` objects.

    """

    ...

  def __init__(self, first_vertex: SVertex, second_vertex: SVertex) -> None:

    """

    Builds an :class:`FEdgeSharp` using the default constructor,
copy constructor, or between two :class:`SVertex` objects.

    """

    ...

  face_mark_left: bool = ...

  """

  The face mark of the face lying on the left of the FEdge.

  """

  face_mark_right: bool = ...

  """

  The face mark of the face lying on the right of the FEdge.  If this FEdge
is a border, it has no face on the right and thus this property is set to
false.

  """

  material_index_left: int = ...

  """

  The index of the material of the face lying on the left of the FEdge.

  """

  material_index_right: int = ...

  """

  The index of the material of the face lying on the right of the FEdge.
If this FEdge is a border, it has no Face on its right and therefore
no material.

  """

  material_left: Material = ...

  """

  The material of the face lying on the left of the FEdge.

  """

  material_right: Material = ...

  """

  The material of the face lying on the right of the FEdge.  If this FEdge
is a border, it has no Face on its right and therefore no material.

  """

  normal_left: mathutils.Vector = ...

  """

  The normal to the face lying on the left of the FEdge.

  """

  normal_right: mathutils.Vector = ...

  """

  The normal to the face lying on the right of the FEdge.  If this FEdge
is a border, it has no Face on its right and therefore no normal.

  """

class FEdgeSmooth:

  """

  Class hierarchy: :class:`Interface1D` > :class:`FEdge` > :class:`FEdgeSmooth`

  Class defining a smooth edge.  This kind of edge typically runs across
a face of the input mesh.  It can be a silhouette, a ridge or valley,
a suggestive contour.

  """

  def __init__(self) -> None:

    """

    Builds an :class:`FEdgeSmooth` using the default constructor,
copy constructor, or between two :class:`SVertex`.

    """

    ...

  def __init__(self, brother: FEdgeSmooth) -> None:

    """

    Builds an :class:`FEdgeSmooth` using the default constructor,
copy constructor, or between two :class:`SVertex`.

    """

    ...

  def __init__(self, first_vertex: SVertex, second_vertex: SVertex) -> None:

    """

    Builds an :class:`FEdgeSmooth` using the default constructor,
copy constructor, or between two :class:`SVertex`.

    """

    ...

  face_mark: bool = ...

  """

  The face mark of the face that this FEdge is running across.

  """

  material: Material = ...

  """

  The material of the face that this FEdge is running across.

  """

  material_index: int = ...

  """

  The index of the material of the face that this FEdge is running across.

  """

  normal: mathutils.Vector = ...

  """

  The normal of the face that this FEdge is running across.

  """

class Id:

  """

  Class for representing an object Id.

  """

  def __init__(self, brother: Id) -> None:

    """

    Build the Id from two numbers or another :class:`Id` using the copy constructor.

    """

    ...

  def __init__(self, first: int = 0, second: int = 0) -> None:

    """

    Build the Id from two numbers or another :class:`Id` using the copy constructor.

    """

    ...

  first: int = ...

  """

  The first number constituting the Id.

  """

  second: int = ...

  """

  The second number constituting the Id.

  """

class IntegrationType:

  """

  Class hierarchy: int > :class:`IntegrationType`

  Different integration methods that can be invoked to integrate into a
single value the set of values obtained from each 0D element of an 1D
element:

  * IntegrationType.MEAN: The value computed for the 1D element is the
mean of the values obtained for the 0D elements.

  * IntegrationType.MIN: The value computed for the 1D element is the
minimum of the values obtained for the 0D elements.

  * IntegrationType.MAX: The value computed for the 1D element is the
maximum of the values obtained for the 0D elements.

  * IntegrationType.FIRST: The value computed for the 1D element is the
first of the values obtained for the 0D elements.

  * IntegrationType.LAST: The value computed for the 1D element is the
last of the values obtained for the 0D elements.

  """

  ...

class Interface0D:

  """

  Base class for any 0D element.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

  def get_fedge(self, inter: Interface0D) -> FEdge:

    """

    Returns the FEdge that lies between this 0D element and the 0D
element given as the argument.

    """

    ...

  id: Id = ...

  """

  The Id of this 0D element.

  """

  name: str = ...

  """

  The string of the name of this 0D element.

  """

  nature: Nature = ...

  """

  The nature of this 0D element.

  """

  point_2d: mathutils.Vector = ...

  """

  The 2D point of this 0D element.

  """

  point_3d: mathutils.Vector = ...

  """

  The 3D point of this 0D element.

  """

  projected_x: float = ...

  """

  The X coordinate of the projected 3D point of this 0D element.

  """

  projected_y: float = ...

  """

  The Y coordinate of the projected 3D point of this 0D element.

  """

  projected_z: float = ...

  """

  The Z coordinate of the projected 3D point of this 0D element.

  """

class Interface0DIterator:

  """

  Class hierarchy: :class:`Iterator` > :class:`Interface0DIterator`

  Class defining an iterator over Interface0D elements.  An instance of
this iterator is always obtained from a 1D element.

  """

  def __init__(self, brother: Interface0DIterator) -> None:

    """

    Construct a nested Interface0DIterator using either the copy constructor
or the constructor that takes an he argument of a Function0D.

    """

    ...

  def __init__(self, it: typing.Any) -> None:

    """

    Construct a nested Interface0DIterator using either the copy constructor
or the constructor that takes an he argument of a Function0D.

    """

    ...

  at_last: bool = ...

  """

  True if the iterator points to the last valid element.
For its counterpart (pointing to the first valid element), use it.is_begin.

  """

  object: Interface0D = ...

  """

  The 0D object currently pointed to by this iterator.  Note that the object
may be an instance of an Interface0D subclass. For example if the iterator
has been created from the *vertices_begin()* method of the :class:`Stroke`
class, the .object property refers to a :class:`StrokeVertex` object.

  """

  t: float = ...

  """

  The curvilinear abscissa of the current point.

  """

  u: float = ...

  """

  The point parameter at the current point in the 1D element (0 <= u <= 1).

  """

class Interface1D:

  """

  Base class for any 1D element.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

  def points_begin(self, t: float = 0.0) -> Interface0DIterator:

    """

    Returns an iterator over the Interface1D points, pointing to the
first point. The difference with vertices_begin() is that here we can
iterate over points of the 1D element at a any given sampling.
Indeed, for each iteration, a virtual point is created.

    """

    ...

  def points_end(self, t: float = 0.0) -> Interface0DIterator:

    """

    Returns an iterator over the Interface1D points, pointing after the
last point. The difference with vertices_end() is that here we can
iterate over points of the 1D element at a given sampling.  Indeed,
for each iteration, a virtual point is created.

    """

    ...

  def vertices_begin(self) -> Interface0DIterator:

    """

    Returns an iterator over the Interface1D vertices, pointing to the
first vertex.

    """

    ...

  def vertices_end(self) -> Interface0DIterator:

    """

    Returns an iterator over the Interface1D vertices, pointing after
the last vertex.

    """

    ...

  id: Id = ...

  """

  The Id of this Interface1D.

  """

  length_2d: float = ...

  """

  The 2D length of this Interface1D.

  """

  name: str = ...

  """

  The string of the name of the 1D element.

  """

  nature: Nature = ...

  """

  The nature of this Interface1D.

  """

  time_stamp: int = ...

  """

  The time stamp of the 1D element, mainly used for selection.

  """

class Iterator:

  """

  Base class to define iterators.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

  def decrement(self) -> None:

    """

    Makes the iterator point the previous element.

    """

    ...

  def increment(self) -> None:

    """

    Makes the iterator point the next element.

    """

    ...

  is_begin: bool = ...

  """

  True if the iterator points to the first element.

  """

  is_end: bool = ...

  """

  True if the iterator points to the last element.

  """

  name: str = ...

  """

  The string of the name of this iterator.

  """

class Material:

  """

  Class defining a material.

  """

  def __init__(self) -> None:

    """

    Creates a :class:`FrsMaterial` using either default constructor,
copy constructor, or an overloaded constructor

    """

    ...

  def __init__(self, brother: Material) -> None:

    """

    Creates a :class:`FrsMaterial` using either default constructor,
copy constructor, or an overloaded constructor

    """

    ...

  def __init__(self, line: mathutils.Vector, diffuse: mathutils.Vector, ambient: mathutils.Vector, specular: mathutils.Vector, emission: mathutils.Vector, shininess: float, priority: int) -> None:

    """

    Creates a :class:`FrsMaterial` using either default constructor,
copy constructor, or an overloaded constructor

    """

    ...

  ambient: mathutils.Color = ...

  """

  RGBA components of the ambient color of the material.

  """

  diffuse: mathutils.Vector = ...

  """

  RGBA components of the diffuse color of the material.

  """

  emission: mathutils.Color = ...

  """

  RGBA components of the emissive color of the material.

  """

  line: mathutils.Vector = ...

  """

  RGBA components of the line color of the material.

  """

  priority: int = ...

  """

  Line color priority of the material.

  """

  shininess: float = ...

  """

  Shininess coefficient of the material.

  """

  specular: mathutils.Vector = ...

  """

  RGBA components of the specular color of the material.

  """

class MediumType:

  """

  Class hierarchy: int > :class:`MediumType`

  The different blending modes available to similate the interaction
media-medium:

  * Stroke.DRY_MEDIUM: To simulate a dry medium such as Pencil or Charcoal.

  * Stroke.HUMID_MEDIUM: To simulate ink painting (color subtraction blending).

  * Stroke.OPAQUE_MEDIUM: To simulate an opaque medium (oil, spray...).

  """

  ...

class Nature:

  """

  Class hierarchy: int > :class:`Nature`

  Different possible natures of 0D and 1D elements of the ViewMap.

  Vertex natures:

  * Nature.POINT: True for any 0D element.

  * Nature.S_VERTEX: True for SVertex.

  * Nature.VIEW_VERTEX: True for ViewVertex.

  * Nature.NON_T_VERTEX: True for NonTVertex.

  * Nature.T_VERTEX: True for TVertex.

  * Nature.CUSP: True for CUSP.

  Edge natures:

  * Nature.NO_FEATURE: True for non feature edges (always false for 1D
elements of the ViewMap).

  * Nature.SILHOUETTE: True for silhouettes.

  * Nature.BORDER: True for borders.

  * Nature.CREASE: True for creases.

  * Nature.RIDGE: True for ridges.

  * Nature.VALLEY: True for valleys.

  * Nature.SUGGESTIVE_CONTOUR: True for suggestive contours.

  * Nature.MATERIAL_BOUNDARY: True for edges at material boundaries.

  * Nature.EDGE_MARK: True for edges having user-defined edge marks.

  """

  ...

class Noise:

  """

  Class to provide Perlin noise functionalities.

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  def __init__(self, seed: int = -1) -> None:

    """

    Builds a Noise object.  Seed is an optional argument.  The seed value is used
as a seed for random number generation if it is equal to or greater than zero;
otherwise, time is used as a seed.

    """

    ...

  def smoothNoise1(self, v: float) -> float:

    """

    Returns a smooth noise value for a 1D element.

    """

    ...

  def smoothNoise2(self, v: mathutils.Vector) -> float:

    """

    Returns a smooth noise value for a 2D element.

    """

    ...

  def smoothNoise3(self, v: mathutils.Vector) -> float:

    """

    Returns a smooth noise value for a 3D element.

    """

    ...

  def turbulence1(self, v: float, freq: float, amp: float, oct: int = 4) -> float:

    """

    Returns a noise value for a 1D element.

    """

    ...

  def turbulence2(self, v: mathutils.Vector, freq: float, amp: float, oct: int = 4) -> float:

    """

    Returns a noise value for a 2D element.

    """

    ...

  def turbulence3(self, v: mathutils.Vector, freq: float, amp: float, oct: int = 4) -> float:

    """

    Returns a noise value for a 3D element.

    """

    ...

class NonTVertex:

  """

  Class hierarchy: :class:`Interface0D` > :class:`ViewVertex` > :class:`NonTVertex`

  View vertex for corners, cusps, etc. associated to a single SVertex.
Can be associated to 2 or more view edges.

  """

  def __init__(self) -> None:

    """

    Builds a :class:`NonTVertex` using the default constructor or a :class:`SVertex`.

    """

    ...

  def __init__(self, svertex: SVertex) -> None:

    """

    Builds a :class:`NonTVertex` using the default constructor or a :class:`SVertex`.

    """

    ...

  svertex: SVertex = ...

  """

  The SVertex on top of which this NonTVertex is built.

  """

class Operators:

  """

  Class defining the operators used in a style module.  There are five
types of operators: Selection, chaining, splitting, sorting and
creation.  All these operators are user controlled through functors,
predicates and shaders that are taken as arguments.

  """

  @staticmethod

  def bidirectional_chain(it: ChainingIterator, pred: UnaryPredicate1D) -> None:

    """

    Builds a set of chains from the current set of ViewEdges.  Each
ViewEdge of the current list potentially starts a new chain.  The
chaining operator then iterates over the ViewEdges of the ViewMap
using the user specified iterator.  This operator iterates both using
the increment and decrement operators and is therefore bidirectional.
This operator works with a ChainingIterator which contains the
chaining rules.  It is this last one which can be told to chain only
edges that belong to the selection or not to process twice a ViewEdge
during the chaining.  Each time a ViewEdge is added to a chain, its
chaining time stamp is incremented.  This allows you to keep track of
the number of chains to which a ViewEdge belongs to.

    """

    ...

  @staticmethod

  def bidirectional_chain(it: ChainingIterator) -> None:

    """

    Builds a set of chains from the current set of ViewEdges.  Each
ViewEdge of the current list potentially starts a new chain.  The
chaining operator then iterates over the ViewEdges of the ViewMap
using the user specified iterator.  This operator iterates both using
the increment and decrement operators and is therefore bidirectional.
This operator works with a ChainingIterator which contains the
chaining rules.  It is this last one which can be told to chain only
edges that belong to the selection or not to process twice a ViewEdge
during the chaining.  Each time a ViewEdge is added to a chain, its
chaining time stamp is incremented.  This allows you to keep track of
the number of chains to which a ViewEdge belongs to.

    """

    ...

  @staticmethod

  def chain(it: ViewEdgeIterator, pred: UnaryPredicate1D, modifier: UnaryFunction1DVoid) -> None:

    """

    Builds a set of chains from the current set of ViewEdges.  Each
ViewEdge of the current list starts a new chain.  The chaining
operator then iterates over the ViewEdges of the ViewMap using the
user specified iterator.  This operator only iterates using the
increment operator and is therefore unidirectional.

    """

    ...

  @staticmethod

  def chain(it: ViewEdgeIterator, pred: UnaryPredicate1D) -> None:

    """

    Builds a set of chains from the current set of ViewEdges.  Each
ViewEdge of the current list starts a new chain.  The chaining
operator then iterates over the ViewEdges of the ViewMap using the
user specified iterator.  This operator only iterates using the
increment operator and is therefore unidirectional.

    """

    ...

  @staticmethod

  def create(pred: UnaryPredicate1D, shaders: typing.List[StrokeShader]) -> None:

    """

    Creates and shades the strokes from the current set of chains.  A
predicate can be specified to make a selection pass on the chains.

    """

    ...

  @staticmethod

  def get_chain_from_index(i: int) -> Chain:

    """

    Returns the Chain at the index in the current set of Chains.

    """

    ...

  @staticmethod

  def get_chains_size() -> int:

    """

    Returns the number of Chains.

    """

    ...

  @staticmethod

  def get_stroke_from_index(i: int) -> Stroke:

    """

    Returns the Stroke at the index in the current set of Strokes.

    """

    ...

  @staticmethod

  def get_strokes_size() -> int:

    """

    Returns the number of Strokes.

    """

    ...

  @staticmethod

  def get_view_edges_size() -> int:

    """

    Returns the number of ViewEdges.

    """

    ...

  @staticmethod

  def get_viewedge_from_index(i: int) -> ViewEdge:

    """

    Returns the ViewEdge at the index in the current set of ViewEdges.

    """

    ...

  @staticmethod

  def recursive_split(func: UnaryFunction0DDouble, pred_1d: UnaryPredicate1D, sampling: float = 0.0) -> None:

    """

    Splits the current set of chains in a recursive way.  We process the
points of each chain (with a specified sampling) to find the point
minimizing a specified function. The chain is split in two at this
point and the two new chains are processed in the same way. The
recursivity level is controlled through a predicate 1D that expresses
a stopping condition on the chain that is about to be processed.

    The user can also specify a 0D predicate to make a first selection on the points
that can potentially be split. A point that doesn't verify the 0D
predicate won't be candidate in realizing the min.

    """

    ...

  @staticmethod

  def recursive_split(func: UnaryFunction0DDouble, pred_0d: UnaryPredicate0D, pred_1d: UnaryPredicate1D, sampling: float = 0.0) -> None:

    """

    Splits the current set of chains in a recursive way.  We process the
points of each chain (with a specified sampling) to find the point
minimizing a specified function. The chain is split in two at this
point and the two new chains are processed in the same way. The
recursivity level is controlled through a predicate 1D that expresses
a stopping condition on the chain that is about to be processed.

    The user can also specify a 0D predicate to make a first selection on the points
that can potentially be split. A point that doesn't verify the 0D
predicate won't be candidate in realizing the min.

    """

    ...

  @staticmethod

  def reset(delete_strokes: bool = True) -> None:

    """

    Resets the line stylization process to the initial state.  The results of
stroke creation are accumulated if **delete_strokes** is set to False.

    """

    ...

  @staticmethod

  def select(pred: UnaryPredicate1D) -> None:

    """

    Selects the ViewEdges of the ViewMap verifying a specified
condition.

    """

    ...

  @staticmethod

  def sequential_split(starting_pred: UnaryPredicate0D, stopping_pred: UnaryPredicate0D, sampling: float = 0.0) -> None:

    """

    Splits each chain of the current set of chains in a sequential way.
The points of each chain are processed (with a specified sampling)
sequentially. The first point of the initial chain is the
first point of one of the resulting chains. The splitting ends when
no more chain can start.

    Tip: By specifying a starting and stopping predicate allows
the chains to overlap rather than chains partitioning.

    """

    ...

  @staticmethod

  def sequential_split(pred: UnaryPredicate0D, sampling: float = 0.0) -> None:

    """

    Splits each chain of the current set of chains in a sequential way.
The points of each chain are processed (with a specified sampling)
sequentially. The first point of the initial chain is the
first point of one of the resulting chains. The splitting ends when
no more chain can start.

    Tip: By specifying a starting and stopping predicate allows
the chains to overlap rather than chains partitioning.

    """

    ...

  @staticmethod

  def sort(pred: BinaryPredicate1D) -> None:

    """

    Sorts the current set of chains (or viewedges) according to the
comparison predicate given as argument.

    """

    ...

class SShape:

  """

  Class to define a feature shape.  It is the gathering of feature
elements from an identified input shape.

  """

  def __init__(self) -> None:

    """

    Creates a :class:`SShape` class using either a default constructor or copy constructor.

    """

    ...

  def __init__(self, brother: SShape) -> None:

    """

    Creates a :class:`SShape` class using either a default constructor or copy constructor.

    """

    ...

  def add_edge(self, edge: FEdge) -> None:

    """

    Adds an FEdge to the list of FEdges.

    """

    ...

  def add_vertex(self, vertex: SVertex) -> None:

    """

    Adds an SVertex to the list of SVertex of this Shape.  The SShape
attribute of the SVertex is also set to this SShape.

    """

    ...

  def compute_bbox(self) -> None:

    """

    Compute the bbox of the SShape.

    """

    ...

  bbox: BBox = ...

  """

  The bounding box of the SShape.

  """

  edges: typing.List[typing.Any] = ...

  """

  The list of edges constituting this SShape.

  """

  id: Id = ...

  """

  The Id of this SShape.

  """

  name: str = ...

  """

  The name of the SShape.

  """

  vertices: typing.List[typing.Any] = ...

  """

  The list of vertices constituting this SShape.

  """

class SVertex:

  """

  Class hierarchy: :class:`Interface0D` > :class:`SVertex`

  Class to define a vertex of the embedding.

  """

  def __init__(self) -> None:

    """

    Builds a :class:`SVertex` using the default constructor,
copy constructor or the overloaded constructor which builds   a :class:`SVertex` from 3D coordinates and an Id.

    """

    ...

  def __init__(self, brother: SVertex) -> None:

    """

    Builds a :class:`SVertex` using the default constructor,
copy constructor or the overloaded constructor which builds   a :class:`SVertex` from 3D coordinates and an Id.

    """

    ...

  def __init__(self, point_3d: mathutils.Vector, id: Id) -> None:

    """

    Builds a :class:`SVertex` using the default constructor,
copy constructor or the overloaded constructor which builds   a :class:`SVertex` from 3D coordinates and an Id.

    """

    ...

  def add_fedge(self, fedge: FEdge) -> None:

    """

    Add an FEdge to the list of edges emanating from this SVertex.

    """

    ...

  def add_normal(self, normal: mathutils.Vector) -> None:

    """

    Adds a normal to the SVertex's set of normals.  If the same normal
is already in the set, nothing changes.

    """

    ...

  curvatures: typing.Tuple[typing.Any, ...] = ...

  """

  Curvature information expressed in the form of a seven-element tuple
(K1, e1, K2, e2, Kr, er, dKr), where K1 and K2 are scalar values
representing the first (maximum) and second (minimum) principal
curvatures at this SVertex, respectively; e1 and e2 are
three-dimensional vectors representing the first and second principal
directions, i.e. the directions of the normal plane where the
curvature takes its maximum and minimum values, respectively; and Kr,
er and dKr are the radial curvature, radial direction, and the
derivative of the radial curvature at this SVertex, respectively.

  """

  id: Id = ...

  """

  The Id of this SVertex.

  """

  normals: typing.List[mathutils.Vector] = ...

  """

  The normals for this Vertex as a list.  In a sharp surface, an SVertex
has exactly one normal.  In a smooth surface, an SVertex can have any
number of normals.

  """

  normals_size: int = ...

  """

  The number of different normals for this SVertex.

  """

  point_2d: mathutils.Vector = ...

  """

  The projected 3D coordinates of the SVertex.

  """

  point_3d: mathutils.Vector = ...

  """

  The 3D coordinates of the SVertex.

  """

  viewvertex: ViewVertex = ...

  """

  If this SVertex is also a ViewVertex, this property refers to the
ViewVertex, and None otherwise.

  """

class SVertexIterator:

  """

  Class hierarchy: :class:`Iterator` > :class:`SVertexIterator`

  Class representing an iterator over :class:`SVertex` of a
:class:`ViewEdge`.  An instance of an SVertexIterator can be obtained
from a ViewEdge by calling verticesBegin() or verticesEnd().

  """

  def __init__(self) -> None:

    ...

  def __init__(self, brother: SVertexIterator) -> None:

    ...

  def __init__(self, vertex: SVertex, begin: SVertex, previous_edge: FEdge, next_edge: FEdge, t: float) -> None:

    ...

  object: SVertex = ...

  """

  The SVertex object currently pointed by this iterator.

  """

  t: float = ...

  """

  The curvilinear abscissa of the current point.

  """

  u: float = ...

  """

  The point parameter at the current point in the 1D element (0 <= u <= 1).

  """

class Stroke:

  """

  Class hierarchy: :class:`Interface1D` > :class:`Stroke`

  Class to define a stroke.  A stroke is made of a set of 2D vertices
(:class:`StrokeVertex`), regularly spaced out.  This set of vertices
defines the stroke's backbone geometry.  Each of these stroke vertices
defines the stroke's shape and appearance at this vertex position.

  """

  def Stroke(self) -> None:

    """

    Creates a :class:`Stroke` using the default constructor or copy constructor

    """

    ...

  def Stroke(self, brother: typing.Any) -> None:

    """

    Creates a :class:`Stroke` using the default constructor or copy constructor

    """

    ...

  def compute_sampling(self, n: int) -> float:

    """

    Compute the sampling needed to get N vertices.  If the
specified number of vertices is less than the actual number of
vertices, the actual sampling value is returned. (To remove Vertices,
use the RemoveVertex() method of this class.)

    """

    ...

  def insert_vertex(self, vertex: StrokeVertex, next: StrokeVertexIterator) -> None:

    """

    Inserts the StrokeVertex given as argument into the Stroke before the
point specified by next.  The length and curvilinear abscissa are
updated consequently.

    """

    ...

  def remove_all_vertices(self) -> None:

    """

    Removes all vertices from the Stroke.

    """

    ...

  def remove_vertex(self, vertex: StrokeVertex) -> None:

    """

    Removes the StrokeVertex given as argument from the Stroke. The length
and curvilinear abscissa are updated consequently.

    """

    ...

  def resample(self, n: int) -> None:

    """

    Resamples the stroke so using one of two methods with the goal
of creating a stroke with fewer points and the same shape.

    """

    ...

  def resample(self, sampling: float) -> None:

    """

    Resamples the stroke so using one of two methods with the goal
of creating a stroke with fewer points and the same shape.

    """

    ...

  def stroke_vertices_begin(self, t: float = 0.0) -> StrokeVertexIterator:

    """

    Returns a StrokeVertexIterator pointing on the first StrokeVertex of
the Stroke. One can specify a sampling value to re-sample the Stroke
on the fly if needed.

    """

    ...

  def stroke_vertices_end(self) -> StrokeVertexIterator:

    """

    Returns a StrokeVertexIterator pointing after the last StrokeVertex
of the Stroke.

    """

    ...

  def stroke_vertices_size(self) -> int:

    """

    Returns the number of StrokeVertex constituting the Stroke.

    """

    ...

  def update_length(self) -> None:

    """

    Updates the 2D length of the Stroke.

    """

    ...

  id: Id = ...

  """

  The Id of this Stroke.

  """

  length_2d: float = ...

  """

  The 2D length of the Stroke.

  """

  medium_type: MediumType = ...

  """

  The MediumType used for this Stroke.

  """

  texture_id: int = ...

  """

  The ID of the texture used to simulate th marks system for this Stroke.

  """

  tips: bool = ...

  """

  True if this Stroke uses a texture with tips, and false otherwise.

  """

class StrokeAttribute:

  """

  Class to define a set of attributes associated with a :class:`StrokeVertex`.
The attribute set stores the color, alpha and thickness values for a Stroke
Vertex.

  """

  def __init__(self) -> None:

    """

    Creates a :class:`StrokeAttribute` object using either a default constructor,
copy constructor, overloaded constructor, or and interpolation constructor
to interpolate between two :class:`StrokeAttribute` objects.

    """

    ...

  def __init__(self, brother: StrokeAttribute) -> None:

    """

    Creates a :class:`StrokeAttribute` object using either a default constructor,
copy constructor, overloaded constructor, or and interpolation constructor
to interpolate between two :class:`StrokeAttribute` objects.

    """

    ...

  def __init__(self, red: float, green: float, blue: float, alpha: float, thickness_right: float, thickness_left: float) -> None:

    """

    Creates a :class:`StrokeAttribute` object using either a default constructor,
copy constructor, overloaded constructor, or and interpolation constructor
to interpolate between two :class:`StrokeAttribute` objects.

    """

    ...

  def __init__(self, attribute1: StrokeAttribute, attribute2: StrokeAttribute, t: float) -> None:

    """

    Creates a :class:`StrokeAttribute` object using either a default constructor,
copy constructor, overloaded constructor, or and interpolation constructor
to interpolate between two :class:`StrokeAttribute` objects.

    """

    ...

  def get_attribute_real(self, name: str) -> float:

    """

    Returns an attribute of float type.

    """

    ...

  def get_attribute_vec2(self, name: str) -> mathutils.Vector:

    """

    Returns an attribute of two-dimensional vector type.

    """

    ...

  def get_attribute_vec3(self, name: str) -> mathutils.Vector:

    """

    Returns an attribute of three-dimensional vector type.

    """

    ...

  def has_attribute_real(self, name: str) -> bool:

    """

    Checks whether the attribute name of float type is available.

    """

    ...

  def has_attribute_vec2(self, name: str) -> bool:

    """

    Checks whether the attribute name of two-dimensional vector type
is available.

    """

    ...

  def has_attribute_vec3(self, name: str) -> bool:

    """

    Checks whether the attribute name of three-dimensional vector
type is available.

    """

    ...

  def set_attribute_real(self, name: str, value: float) -> None:

    """

    Adds a user-defined attribute of float type.  If there is no
attribute of the given name, it is added.  Otherwise, the new value
replaces the old one.

    """

    ...

  def set_attribute_vec2(self, name: str, value: mathutils.Vector) -> None:

    """

    Adds a user-defined attribute of two-dimensional vector type.  If
there is no attribute of the given name, it is added.  Otherwise,
the new value replaces the old one.

    """

    ...

  def set_attribute_vec3(self, name: str, value: mathutils.Vector) -> None:

    """

    Adds a user-defined attribute of three-dimensional vector type.
If there is no attribute of the given name, it is added.
Otherwise, the new value replaces the old one.

    """

    ...

  alpha: float = ...

  """

  Alpha component of the stroke color.

  """

  color: mathutils.Color = ...

  """

  RGB components of the stroke color.

  """

  thickness: mathutils.Vector = ...

  """

  Right and left components of the stroke thickness.
The right (left) component is the thickness on the right (left) of the vertex
when following the stroke.

  """

  visible: bool = ...

  """

  The visibility flag.  True if the StrokeVertex is visible.

  """

class StrokeShader:

  """

  Base class for stroke shaders.  Any stroke shader must inherit from
this class and overload the shade() method.  A StrokeShader is
designed to modify stroke attributes such as thickness, color,
geometry, texture, blending mode, and so on.  The basic way for this
operation is to iterate over the stroke vertices of the :class:`Stroke`
and to modify the :class:`StrokeAttribute` of each vertex.  Here is a
code example of such an iteration:

  ::

    it = ioStroke.strokeVerticesBegin()
    while not it.is_end:
        att = it.object.attribute
        ## perform here any attribute modification
        it.increment()

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

  def shade(self, stroke: Stroke) -> None:

    """

    The shading method.  Must be overloaded by inherited classes.

    """

    ...

  name: str = ...

  """

  The name of the stroke shader.

  """

class StrokeVertex:

  """

  Class hierarchy: :class:`Interface0D` > :class:`CurvePoint` > :class:`StrokeVertex`

  Class to define a stroke vertex.

  """

  def __init__(self) -> None:

    """

    Builds a :class:`StrokeVertex` using the default constructor,
copy constructor, from 2 :class:`StrokeVertex` and an interpolation parameter,
from a CurvePoint, from a SVertex, or a :class:`SVertex`   and a :class:`StrokeAttribute` object.

    """

    ...

  def __init__(self, brother: StrokeVertex) -> None:

    """

    Builds a :class:`StrokeVertex` using the default constructor,
copy constructor, from 2 :class:`StrokeVertex` and an interpolation parameter,
from a CurvePoint, from a SVertex, or a :class:`SVertex`   and a :class:`StrokeAttribute` object.

    """

    ...

  def __init__(self, first_vertex: StrokeVertex, second_vertex: StrokeVertex, t3d: float) -> None:

    """

    Builds a :class:`StrokeVertex` using the default constructor,
copy constructor, from 2 :class:`StrokeVertex` and an interpolation parameter,
from a CurvePoint, from a SVertex, or a :class:`SVertex`   and a :class:`StrokeAttribute` object.

    """

    ...

  def __init__(self, point: CurvePoint) -> None:

    """

    Builds a :class:`StrokeVertex` using the default constructor,
copy constructor, from 2 :class:`StrokeVertex` and an interpolation parameter,
from a CurvePoint, from a SVertex, or a :class:`SVertex`   and a :class:`StrokeAttribute` object.

    """

    ...

  def __init__(self, svertex: SVertex) -> None:

    """

    Builds a :class:`StrokeVertex` using the default constructor,
copy constructor, from 2 :class:`StrokeVertex` and an interpolation parameter,
from a CurvePoint, from a SVertex, or a :class:`SVertex`   and a :class:`StrokeAttribute` object.

    """

    ...

  def __init__(self, svertex: SVertex, attribute: StrokeAttribute) -> None:

    """

    Builds a :class:`StrokeVertex` using the default constructor,
copy constructor, from 2 :class:`StrokeVertex` and an interpolation parameter,
from a CurvePoint, from a SVertex, or a :class:`SVertex`   and a :class:`StrokeAttribute` object.

    """

    ...

  attribute: StrokeAttribute = ...

  """

  StrokeAttribute for this StrokeVertex.

  """

  curvilinear_abscissa: float = ...

  """

  Curvilinear abscissa of this StrokeVertex in the Stroke.

  """

  point: mathutils.Vector = ...

  """

  2D point coordinates.

  """

  stroke_length: float = ...

  """

  Stroke length (it is only a value retained by the StrokeVertex,
and it won't change the real stroke length).

  """

  u: float = ...

  """

  Curvilinear abscissa of this StrokeVertex in the Stroke.

  """

class StrokeVertexIterator:

  """

  Class hierarchy: :class:`Iterator` > :class:`StrokeVertexIterator`

  Class defining an iterator designed to iterate over the
:class:`StrokeVertex` of a :class:`Stroke`.  An instance of a
StrokeVertexIterator can be obtained from a Stroke by calling
iter(), stroke_vertices_begin() or stroke_vertices_begin().  It is iterating
over the same vertices as an :class:`Interface0DIterator`.  The difference
resides in the object access: an Interface0DIterator only allows
access to an Interface0D while one might need to access the
specialized StrokeVertex type.  In this case, one should use a
StrokeVertexIterator.  To call functions of the UnaryFuntion0D type,
a StrokeVertexIterator can be converted to an Interface0DIterator by
by calling Interface0DIterator(it).

  """

  def __init__(self) -> None:

    """

    Creates a :class:`StrokeVertexIterator` using either the
default constructor or the copy constructor.

    """

    ...

  def __init__(self, brother: StrokeVertexIterator) -> None:

    """

    Creates a :class:`StrokeVertexIterator` using either the
default constructor or the copy constructor.

    """

    ...

  def decremented(self) -> StrokeVertexIterator:

    """

    Returns a copy of a decremented StrokeVertexIterator.

    """

    ...

  def incremented(self) -> StrokeVertexIterator:

    """

    Returns a copy of an incremented StrokeVertexIterator.

    """

    ...

  def reversed(self) -> StrokeVertexIterator:

    """

    Returns a StrokeVertexIterator that traverses stroke vertices in the
reversed order.

    """

    ...

  at_last: bool = ...

  """

  True if the iterator points to the last valid element.
For its counterpart (pointing to the first valid element), use it.is_begin.

  """

  object: StrokeVertex = ...

  """

  The StrokeVertex object currently pointed to by this iterator.

  """

  t: float = ...

  """

  The curvilinear abscissa of the current point.

  """

  u: float = ...

  """

  The point parameter at the current point in the stroke (0 <= u <= 1).

  """

class TVertex:

  """

  Class hierarchy: :class:`Interface0D` > :class:`ViewVertex` > :class:`TVertex`

  Class to define a T vertex, i.e. an intersection between two edges.
It points towards two SVertex and four ViewEdges.  Among the
ViewEdges, two are front and the other two are back.  Basically a
front edge hides part of a back edge.  So, among the back edges, one
is of invisibility N and the other of invisibility N+1.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

  def get_mate(self, viewedge: ViewEdge) -> ViewEdge:

    """

    Returns the mate edge of the ViewEdge given as argument.  If the
ViewEdge is frontEdgeA, frontEdgeB is returned.  If the ViewEdge is
frontEdgeB, frontEdgeA is returned.  Same for back edges.

    """

    ...

  def get_svertex(self, fedge: FEdge) -> SVertex:

    """

    Returns the SVertex (among the 2) belonging to the given FEdge.

    """

    ...

  back_svertex: SVertex = ...

  """

  The SVertex that is further away from the viewpoint.

  """

  front_svertex: SVertex = ...

  """

  The SVertex that is closer to the viewpoint.

  """

  id: Id = ...

  """

  The Id of this TVertex.

  """

class UnaryFunction0D:

  """

  Base class for Unary Functions (functors) working on
:class:`Interface0DIterator`.  A unary function will be used by
invoking __call__() on an Interface0DIterator.  In Python, several
different subclasses of UnaryFunction0D are used depending on the
types of functors' return values.  For example, you would inherit from
a :class:`UnaryFunction0DDouble` if you wish to define a function that
returns a double value.  Available UnaryFunction0D subclasses are:

  * :class:`UnaryFunction0DDouble`

  * :class:`UnaryFunction0DEdgeNature`

  * :class:`UnaryFunction0DFloat`

  * :class:`UnaryFunction0DId`

  * :class:`UnaryFunction0DMaterial`

  * :class:`UnaryFunction0DUnsigned`

  * :class:`UnaryFunction0DVec2f`

  * :class:`UnaryFunction0DVec3f`

  * :class:`UnaryFunction0DVectorViewShape`

  * :class:`UnaryFunction0DViewShape`

  """

  name: str = ...

  """

  The name of the unary 0D function.

  """

class UnaryFunction0DDouble:

  """

  Class hierarchy: :class:`UnaryFunction0D` > :class:`UnaryFunction0DDouble`

  Base class for unary functions (functors) that work on
:class:`Interface0DIterator` and return a float value.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

class UnaryFunction0DEdgeNature:

  """

  Class hierarchy: :class:`UnaryFunction0D` > :class:`UnaryFunction0DEdgeNature`

  Base class for unary functions (functors) that work on
:class:`Interface0DIterator` and return a :class:`Nature` object.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

class UnaryFunction0DFloat:

  """

  Class hierarchy: :class:`UnaryFunction0D` > :class:`UnaryFunction0DFloat`

  Base class for unary functions (functors) that work on
:class:`Interface0DIterator` and return a float value.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

class UnaryFunction0DId:

  """

  Class hierarchy: :class:`UnaryFunction0D` > :class:`UnaryFunction0DId`

  Base class for unary functions (functors) that work on
:class:`Interface0DIterator` and return an :class:`Id` object.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

class UnaryFunction0DMaterial:

  """

  Class hierarchy: :class:`UnaryFunction0D` > :class:`UnaryFunction0DMaterial`

  Base class for unary functions (functors) that work on
:class:`Interface0DIterator` and return a :class:`Material` object.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

class UnaryFunction0DUnsigned:

  """

  Class hierarchy: :class:`UnaryFunction0D` > :class:`UnaryFunction0DUnsigned`

  Base class for unary functions (functors) that work on
:class:`Interface0DIterator` and return an int value.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

class UnaryFunction0DVec2f:

  """

  Class hierarchy: :class:`UnaryFunction0D` > :class:`UnaryFunction0DVec2f`

  Base class for unary functions (functors) that work on
:class:`Interface0DIterator` and return a 2D vector.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

class UnaryFunction0DVec3f:

  """

  Class hierarchy: :class:`UnaryFunction0D` > :class:`UnaryFunction0DVec3f`

  Base class for unary functions (functors) that work on
:class:`Interface0DIterator` and return a 3D vector.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

class UnaryFunction0DVectorViewShape:

  """

  Class hierarchy: :class:`UnaryFunction0D` > :class:`UnaryFunction0DVectorViewShape`

  Base class for unary functions (functors) that work on
:class:`Interface0DIterator` and return a list of :class:`ViewShape`
objects.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

class UnaryFunction0DViewShape:

  """

  Class hierarchy: :class:`UnaryFunction0D` > :class:`UnaryFunction0DViewShape`

  Base class for unary functions (functors) that work on
:class:`Interface0DIterator` and return a :class:`ViewShape` object.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

class UnaryFunction1D:

  """

  Base class for Unary Functions (functors) working on
:class:`Interface1D`.  A unary function will be used by invoking
__call__() on an Interface1D.  In Python, several different subclasses
of UnaryFunction1D are used depending on the types of functors' return
values.  For example, you would inherit from a
:class:`UnaryFunction1DDouble` if you wish to define a function that
returns a double value.  Available UnaryFunction1D subclasses are:

  * :class:`UnaryFunction1DDouble`

  * :class:`UnaryFunction1DEdgeNature`

  * :class:`UnaryFunction1DFloat`

  * :class:`UnaryFunction1DUnsigned`

  * :class:`UnaryFunction1DVec2f`

  * :class:`UnaryFunction1DVec3f`

  * :class:`UnaryFunction1DVectorViewShape`

  * :class:`UnaryFunction1DVoid`

  """

  name: str = ...

  """

  The name of the unary 1D function.

  """

class UnaryFunction1DDouble:

  """

  Class hierarchy: :class:`UnaryFunction1D` > :class:`UnaryFunction1DDouble`

  Base class for unary functions (functors) that work on
:class:`Interface1D` and return a float value.

  """

  def __init__(self) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  def __init__(self, integration_type: IntegrationType) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  integration_type: IntegrationType = ...

  """

  The integration method.

  """

class UnaryFunction1DEdgeNature:

  """

  Class hierarchy: :class:`UnaryFunction1D` > :class:`UnaryFunction1DEdgeNature`

  Base class for unary functions (functors) that work on
:class:`Interface1D` and return a :class:`Nature` object.

  """

  def __init__(self) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  def __init__(self, integration_type: IntegrationType) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  integration_type: IntegrationType = ...

  """

  The integration method.

  """

class UnaryFunction1DFloat:

  """

  Class hierarchy: :class:`UnaryFunction1D` > :class:`UnaryFunction1DFloat`

  Base class for unary functions (functors) that work on
:class:`Interface1D` and return a float value.

  """

  def __init__(self) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  def __init__(self, integration_type: IntegrationType) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  integration_type: IntegrationType = ...

  """

  The integration method.

  """

class UnaryFunction1DUnsigned:

  """

  Class hierarchy: :class:`UnaryFunction1D` > :class:`UnaryFunction1DUnsigned`

  Base class for unary functions (functors) that work on
:class:`Interface1D` and return an int value.

  """

  def __init__(self) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  def __init__(self, integration_type: IntegrationType) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  integration_type: IntegrationType = ...

  """

  The integration method.

  """

class UnaryFunction1DVec2f:

  """

  Class hierarchy: :class:`UnaryFunction1D` > :class:`UnaryFunction1DVec2f`

  Base class for unary functions (functors) that work on
:class:`Interface1D` and return a 2D vector.

  """

  def __init__(self) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  def __init__(self, integration_type: IntegrationType) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  integration_type: IntegrationType = ...

  """

  The integration method.

  """

class UnaryFunction1DVec3f:

  """

  Class hierarchy: :class:`UnaryFunction1D` > :class:`UnaryFunction1DVec3f`

  Base class for unary functions (functors) that work on
:class:`Interface1D` and return a 3D vector.

  """

  def __init__(self) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  def __init__(self, integration_type: IntegrationType) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  integration_type: IntegrationType = ...

  """

  The integration method.

  """

class UnaryFunction1DVectorViewShape:

  """

  Class hierarchy: :class:`UnaryFunction1D` > :class:`UnaryFunction1DVectorViewShape`

  Base class for unary functions (functors) that work on
:class:`Interface1D` and return a list of :class:`ViewShape`
objects.

  """

  def __init__(self) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  def __init__(self, integration_type: IntegrationType) -> None:

    """

    Builds a unary 1D function using the default constructor
or the integration method given as an argument.

    """

    ...

  integration_type: IntegrationType = ...

  """

  The integration method.

  """

class UnaryFunction1DVoid:

  """

  Class hierarchy: :class:`UnaryFunction1D` > :class:`UnaryFunction1DVoid`

  Base class for unary functions (functors) working on
:class:`Interface1D`.

  """

  def __init__(self) -> None:

    """

    Builds a unary 1D function using either a default constructor
or the integration method given as an argument.

    """

    ...

  def __init__(self, integration_type: IntegrationType) -> None:

    """

    Builds a unary 1D function using either a default constructor
or the integration method given as an argument.

    """

    ...

  integration_type: IntegrationType = ...

  """

  The integration method.

  """

class UnaryPredicate0D:

  """

  Base class for unary predicates that work on
:class:`Interface0DIterator`.  A UnaryPredicate0D is a functor that
evaluates a condition on an Interface0DIterator and returns true or
false depending on whether this condition is satisfied or not.  The
UnaryPredicate0D is used by invoking its __call__() method.  Any
inherited class must overload the __call__() method.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

  def __call__(self, it: Interface0DIterator) -> bool:

    """

    Must be overload by inherited classes.

    """

    ...

  name: str = ...

  """

  The name of the unary 0D predicate.

  """

class UnaryPredicate1D:

  """

  Base class for unary predicates that work on :class:`Interface1D`.  A
UnaryPredicate1D is a functor that evaluates a condition on a
Interface1D and returns true or false depending on whether this
condition is satisfied or not.  The UnaryPredicate1D is used by
invoking its __call__() method.  Any inherited class must overload the
__call__() method.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

  def __call__(self, inter: Interface1D) -> bool:

    """

    Must be overload by inherited classes.

    """

    ...

  name: str = ...

  """

  The name of the unary 1D predicate.

  """

class ViewEdge:

  """

  Class hierarchy: :class:`Interface1D` > :class:`ViewEdge`

  Class defining a ViewEdge.  A ViewEdge in an edge of the image graph.
it connects two :class:`ViewVertex` objects.  It is made by connecting
a set of FEdges.

  """

  def __init__(self) -> None:

    """

    Builds a :class:`ViewEdge` using the default constructor or the copy constructor.

    """

    ...

  def __init__(self, brother: ViewEdge) -> None:

    """

    Builds a :class:`ViewEdge` using the default constructor or the copy constructor.

    """

    ...

  def update_fedges(self) -> None:

    """

    Sets Viewedge to this for all embedded fedges.

    """

    ...

  chaining_time_stamp: int = ...

  """

  The time stamp of this ViewEdge.

  """

  first_fedge: FEdge = ...

  """

  The first FEdge that constitutes this ViewEdge.

  """

  first_viewvertex: ViewVertex = ...

  """

  The first ViewVertex.

  """

  id: Id = ...

  """

  The Id of this ViewEdge.

  """

  is_closed: bool = ...

  """

  True if this ViewEdge forms a closed loop.

  """

  last_fedge: FEdge = ...

  """

  The last FEdge that constitutes this ViewEdge.

  """

  last_viewvertex: ViewVertex = ...

  """

  The second ViewVertex.

  """

  nature: Nature = ...

  """

  The nature of this ViewEdge.

  """

  occludee: ViewShape = ...

  """

  The shape that is occluded by the ViewShape to which this ViewEdge
belongs to.  If no object is occluded, this property is set to None.

  """

  qi: int = ...

  """

  The quantitative invisibility.

  """

  viewshape: ViewShape = ...

  """

  The ViewShape to which this ViewEdge belongs to.

  """

class ViewEdgeIterator:

  """

  Class hierarchy: :class:`Iterator` > :class:`ViewEdgeIterator`

  Base class for iterators over ViewEdges of the :class:`ViewMap` Graph.
Basically the increment() operator of this class should be able to
take the decision of "where" (on which ViewEdge) to go when pointing
on a given ViewEdge.

  """

  def __init__(self, begin: ViewEdge = None, orientation: bool = True) -> None:

    """

    Builds a ViewEdgeIterator from a starting ViewEdge and its
orientation or the copy constructor.

    """

    ...

  def __init__(self, brother: ViewEdgeIterator) -> None:

    """

    Builds a ViewEdgeIterator from a starting ViewEdge and its
orientation or the copy constructor.

    """

    ...

  def change_orientation(self) -> None:

    """

    Changes the current orientation.

    """

    ...

  begin: ViewEdge = ...

  """

  The first ViewEdge used for the iteration.

  """

  current_edge: ViewEdge = ...

  """

  The ViewEdge object currently pointed by this iterator.

  """

  object: ViewEdge = ...

  """

  The ViewEdge object currently pointed by this iterator.

  """

  orientation: bool = ...

  """

  The orientation of the pointed ViewEdge in the iteration.
If true, the iterator looks for the next ViewEdge among those ViewEdges
that surround the ending ViewVertex of the "begin" ViewEdge.  If false,
the iterator searches over the ViewEdges surrounding the ending ViewVertex
of the "begin" ViewEdge.

  """

class ViewMap:

  """

  Class defining the ViewMap.

  """

  def __init__(self) -> None:

    """

    Default constructor.

    """

    ...

  def get_closest_fedge(self, x: float, y: float) -> FEdge:

    """

    Gets the FEdge nearest to the 2D point specified as arguments.

    """

    ...

  def get_closest_viewedge(self, x: float, y: float) -> ViewEdge:

    """

    Gets the ViewEdge nearest to the 2D point specified as arguments.

    """

    ...

  scene_bbox: BBox = ...

  """

  The 3D bounding box of the scene.

  """

class ViewShape:

  """

  Class gathering the elements of the ViewMap (i.e., :class:`ViewVertex`
and :class:`ViewEdge`) that are issued from the same input shape.

  """

  def __init__(self) -> None:

    """

    Builds a :class:`ViewShape` using the default constructor,
copy constructor, or from a :class:`SShape`.

    """

    ...

  def __init__(self, brother: ViewShape) -> None:

    """

    Builds a :class:`ViewShape` using the default constructor,
copy constructor, or from a :class:`SShape`.

    """

    ...

  def __init__(self, sshape: SShape) -> None:

    """

    Builds a :class:`ViewShape` using the default constructor,
copy constructor, or from a :class:`SShape`.

    """

    ...

  def add_edge(self, edge: ViewEdge) -> None:

    """

    Adds a ViewEdge to the list of ViewEdge objects.

    """

    ...

  def add_vertex(self, vertex: ViewVertex) -> None:

    """

    Adds a ViewVertex to the list of the ViewVertex objects.

    """

    ...

  edges: typing.List[typing.Any] = ...

  """

  The list of ViewEdge objects contained in this ViewShape.

  """

  id: Id = ...

  """

  The Id of this ViewShape.

  """

  library_path: str = ...

  """

  The library path of the ViewShape.

  """

  name: str = ...

  """

  The name of the ViewShape.

  """

  sshape: SShape = ...

  """

  The SShape on top of which this ViewShape is built.

  """

  vertices: typing.List[typing.Any] = ...

  """

  The list of ViewVertex objects contained in this ViewShape.

  """

class ViewVertex:

  """

  Class hierarchy: :class:`Interface0D` > :class:`ViewVertex`

  Class to define a view vertex.  A view vertex is a feature vertex
corresponding to a point of the image graph, where the characteristics
of an edge (e.g., nature and visibility) might change.  A
:class:`ViewVertex` can be of two kinds: A :class:`TVertex` when it
corresponds to the intersection between two ViewEdges or a
:class:`NonTVertex` when it corresponds to a vertex of the initial
input mesh (it is the case for vertices such as corners for example).
Thus, this class can be specialized into two classes, the
:class:`TVertex` class and the :class:`NonTVertex` class.

  """

  def edges_begin(self) -> orientedViewEdgeIterator:

    """

    Returns an iterator over the ViewEdges that goes to or comes from
this ViewVertex pointing to the first ViewEdge of the list. The
orientedViewEdgeIterator allows to iterate in CCW order over these
ViewEdges and to get the orientation for each ViewEdge
(incoming/outgoing).

    """

    ...

  def edges_end(self) -> orientedViewEdgeIterator:

    """

    Returns an orientedViewEdgeIterator over the ViewEdges around this
ViewVertex, pointing after the last ViewEdge.

    """

    ...

  def edges_iterator(self, edge: ViewEdge) -> orientedViewEdgeIterator:

    """

    Returns an orientedViewEdgeIterator pointing to the ViewEdge given
as argument.

    """

    ...

  nature: Nature = ...

  """

  The nature of this ViewVertex.

  """

class orientedViewEdgeIterator:

  """

  Class hierarchy: :class:`Iterator` > :class:`orientedViewEdgeIterator`

  Class representing an iterator over oriented ViewEdges around a
:class:`ViewVertex`.  This iterator allows a CCW iteration (in the image
plane).  An instance of an orientedViewEdgeIterator can only be
obtained from a ViewVertex by calling edges_begin() or edges_end().

  """

  def __init__(self) -> None:

    """

    Creates an :class:`orientedViewEdgeIterator` using either the
default constructor or the copy constructor.

    """

    ...

  def __init__(self, iBrother: orientedViewEdgeIterator) -> None:

    """

    Creates an :class:`orientedViewEdgeIterator` using either the
default constructor or the copy constructor.

    """

    ...

  object: typing.Any = ...

  """

  The oriented ViewEdge (i.e., a tuple of the pointed ViewEdge and a boolean
value) currently pointed to by this iterator. If the boolean value is true,
the ViewEdge is incoming.

  """
