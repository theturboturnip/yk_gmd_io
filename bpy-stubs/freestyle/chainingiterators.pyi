"""


Freestyle Chaining Iterators (freestyle.chainingiterators)
**********************************************************

This module contains chaining iterators used for the chaining
operation to construct long strokes by concatenating feature edges
according to selected chaining rules.  The module is also intended to
be a collection of examples for defining chaining iterators in Python.

:class:`ChainPredicateIterator`

:class:`ChainSilhouetteIterator`

:class:`pyChainSilhouetteIterator`

:class:`pyChainSilhouetteGenericIterator`

:class:`pyExternalContourChainingIterator`

:class:`pySketchyChainSilhouetteIterator`

:class:`pySketchyChainingIterator`

:class:`pyFillOcclusionsRelativeChainingIterator`

:class:`pyFillOcclusionsAbsoluteChainingIterator`

:class:`pyFillOcclusionsAbsoluteAndRelativeChainingIterator`

:class:`pyFillQi0AbsoluteAndRelativeChainingIterator`

:class:`pyNoIdChainSilhouetteIterator`

"""

import typing

import freestyle

class ChainPredicateIterator:

  """

  Class hierarchy: :class:`freestyle.types.Iterator` >
:class:`freestyle.types.ViewEdgeIterator` >
:class:`freestyle.types.ChainingIterator` >
:class:`ChainPredicateIterator`

  A "generic" user-controlled ViewEdge iterator.  This iterator is in
particular built from a unary predicate and a binary predicate.
First, the unary predicate is evaluated for all potential next
ViewEdges in order to only keep the ones respecting a certain
constraint.  Then, the binary predicate is evaluated on the current
ViewEdge together with each ViewEdge of the previous selection.  The
first ViewEdge respecting both the unary predicate and the binary
predicate is kept as the next one.  If none of the potential next
ViewEdge respects these two predicates, None is returned.

  """

  def __init__(self, upred: freestyle.types.UnaryPredicate1D, bpred: freestyle.types.BinaryPredicate1D, restrict_to_selection: bool = True, restrict_to_unvisited: bool = True, begin: freestyle.types.ViewEdge = None, orientation: bool = True) -> None:

    """

    Builds a ChainPredicateIterator from a unary predicate, a binary
predicate, a starting ViewEdge and its orientation or using the copy constructor.

    """

    ...

  def __init__(self, brother: ChainPredicateIterator) -> None:

    """

    Builds a ChainPredicateIterator from a unary predicate, a binary
predicate, a starting ViewEdge and its orientation or using the copy constructor.

    """

    ...

class ChainSilhouetteIterator:

  """

  Class hierarchy: :class:`freestyle.types.Iterator` >
:class:`freestyle.types.ViewEdgeIterator` >
:class:`freestyle.types.ChainingIterator` >
:class:`ChainSilhouetteIterator`

  A ViewEdge Iterator used to follow ViewEdges the most naturally.  For
example, it will follow visible ViewEdges of same nature.  As soon, as
the nature or the visibility changes, the iteration stops (by setting
the pointed ViewEdge to 0).  In the case of an iteration over a set of
ViewEdge that are both Silhouette and Crease, there will be a
precedence of the silhouette over the crease criterion.

  """

  def __init__(self, restrict_to_selection: bool = True, begin: freestyle.types.ViewEdge = None, orientation: bool = True) -> None:

    """

    Builds a ChainSilhouetteIterator from the first ViewEdge used for
iteration and its orientation or the copy constructor.

    """

    ...

  def __init__(self, brother: ChainSilhouetteIterator) -> None:

    """

    Builds a ChainSilhouetteIterator from the first ViewEdge used for
iteration and its orientation or the copy constructor.

    """

    ...

class pyChainSilhouetteIterator:

  """

  Natural chaining iterator that follows the edges of the same nature
following the topology of objects, with decreasing priority for
silhouettes, then borders, then suggestive contours, then all other edge
types.  A ViewEdge is only chained once.

  """

  def init(self) -> None:

    ...

  def traverse(self, iter: typing.Any) -> None:

    ...

class pyChainSilhouetteGenericIterator:

  """

  Natural chaining iterator that follows the edges of the same nature
following the topology of objects, with decreasing priority for
silhouettes, then borders, then suggestive contours, then all other
edge types.

  """

  def __init__(self, stayInSelection: bool = True, stayInUnvisited: bool = True) -> None:

    """

    Builds a pyChainSilhouetteGenericIterator object.

    """

    ...

  def init(self) -> None:

    ...

  def traverse(self, iter: typing.Any) -> None:

    ...

class pyExternalContourChainingIterator:

  """

  Chains by external contour

  """

  def checkViewEdge(self, ve: typing.Any, orientation: typing.Any) -> None:

    ...

  def init(self) -> None:

    ...

  def traverse(self, iter: typing.Any) -> None:

    ...

class pySketchyChainSilhouetteIterator:

  """

  Natural chaining iterator with a sketchy multiple touch.  It chains the
same ViewEdge multiple times to achieve a sketchy effect.

  """

  def __init__(self, nRounds: int = 3, stayInSelection: bool = True) -> None:

    """

    Builds a pySketchyChainSilhouetteIterator object.

    """

    ...

  def init(self) -> None:

    ...

  def make_sketchy(self, ve: typing.Any) -> None:

    """

    Creates the skeychy effect by causing the chain to run from
the start again. (loop over itself again)

    """

    ...

  def traverse(self, iter: typing.Any) -> None:

    ...

class pySketchyChainingIterator:

  """

  Chaining iterator designed for sketchy style. It chains the same
ViewEdge several times in order to produce multiple strokes per
ViewEdge.

  """

  def init(self) -> None:

    ...

  def traverse(self, iter: typing.Any) -> None:

    ...

class pyFillOcclusionsRelativeChainingIterator:

  """

  Chaining iterator that fills small occlusions

  """

  def __init__(self, percent: float) -> None:

    """

    Builds a pyFillOcclusionsRelativeChainingIterator object.

    """

    ...

  def init(self) -> None:

    ...

  def traverse(self, iter: typing.Any) -> None:

    ...

class pyFillOcclusionsAbsoluteChainingIterator:

  """

  Chaining iterator that fills small occlusions

  """

  def __init__(self, length: int) -> None:

    """

    Builds a pyFillOcclusionsAbsoluteChainingIterator object.

    """

    ...

  def init(self) -> None:

    ...

  def traverse(self, iter: typing.Any) -> None:

    ...

class pyFillOcclusionsAbsoluteAndRelativeChainingIterator:

  """

  Chaining iterator that fills small occlusions regardless of the
selection.

  """

  def __init__(self, percent: float, l: float) -> None:

    """

    Builds a pyFillOcclusionsAbsoluteAndRelativeChainingIterator object.

    """

    ...

  def init(self) -> None:

    ...

  def traverse(self, iter: typing.Any) -> None:

    ...

class pyFillQi0AbsoluteAndRelativeChainingIterator:

  """

  Chaining iterator that fills small occlusions regardless of the
selection.

  """

  def __init__(self, percent: float, l: float) -> None:

    """

    Builds a pyFillQi0AbsoluteAndRelativeChainingIterator object.

    """

    ...

  def init(self) -> None:

    ...

  def traverse(self, iter: typing.Any) -> None:

    ...

class pyNoIdChainSilhouetteIterator:

  """

  Natural chaining iterator that follows the edges of the same nature
following the topology of objects, with decreasing priority for
silhouettes, then borders, then suggestive contours, then all other edge
types.  It won't chain the same ViewEdge twice.

  """

  def __init__(self, stayInSelection: bool = True) -> None:

    """

    Builds a pyNoIdChainSilhouetteIterator object.

    """

    ...

  def init(self) -> None:

    ...

  def traverse(self, iter: typing.Any) -> None:

    ...
