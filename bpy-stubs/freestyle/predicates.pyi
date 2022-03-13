"""


Freestyle Predicates (freestyle.predicates)
*******************************************

This module contains predicates operating on vertices (0D elements)
and polylines (1D elements).  It is also intended to be a collection
of examples for predicate definition in Python.

User-defined predicates inherit one of the following base classes,
depending on the object type (0D or 1D) to operate on and the arity
(unary or binary):

* :class:`freestyle.types.BinaryPredicate0D`

* :class:`freestyle.types.BinaryPredicate1D`

* :class:`freestyle.types.UnaryPredicate0D`

* :class:`freestyle.types.UnaryPredicate1D`

:class:`AndBP1D`

:class:`AndUP1D`

:class:`ContourUP1D`

:class:`DensityLowerThanUP1D`

:class:`EqualToChainingTimeStampUP1D`

:class:`EqualToTimeStampUP1D`

:class:`ExternalContourUP1D`

:class:`FalseBP1D`

:class:`FalseUP0D`

:class:`FalseUP1D`

:class:`Length2DBP1D`

:class:`MaterialBP1D`

:class:`NotBP1D`

:class:`NotUP1D`

:class:`ObjectNamesUP1D`

:class:`OrBP1D`

:class:`OrUP1D`

:class:`QuantitativeInvisibilityRangeUP1D`

:class:`QuantitativeInvisibilityUP1D`

:class:`SameShapeIdBP1D`

:class:`ShapeUP1D`

:class:`TrueBP1D`

:class:`TrueUP0D`

:class:`TrueUP1D`

:class:`ViewMapGradientNormBP1D`

:class:`WithinImageBoundaryUP1D`

:class:`pyBackTVertexUP0D`

:class:`pyClosedCurveUP1D`

:class:`pyDensityFunctorUP1D`

:class:`pyDensityUP1D`

:class:`pyDensityVariableSigmaUP1D`

:class:`pyHighDensityAnisotropyUP1D`

:class:`pyHighDirectionalViewMapDensityUP1D`

:class:`pyHighSteerableViewMapDensityUP1D`

:class:`pyHighViewMapDensityUP1D`

:class:`pyHighViewMapGradientNormUP1D`

:class:`pyHigherCurvature2DAngleUP0D`

:class:`pyHigherLengthUP1D`

:class:`pyHigherNumberOfTurnsUP1D`

:class:`pyIsInOccludersListUP1D`

:class:`pyIsOccludedByIdListUP1D`

:class:`pyIsOccludedByItselfUP1D`

:class:`pyIsOccludedByUP1D`

:class:`pyLengthBP1D`

:class:`pyLowDirectionalViewMapDensityUP1D`

:class:`pyLowSteerableViewMapDensityUP1D`

:class:`pyNFirstUP1D`

:class:`pyNatureBP1D`

:class:`pyNatureUP1D`

:class:`pyParameterUP0D`

:class:`pyParameterUP0DGoodOne`

:class:`pyProjectedXBP1D`

:class:`pyProjectedYBP1D`

:class:`pyShapeIdListUP1D`

:class:`pyShapeIdUP1D`

:class:`pyShuffleBP1D`

:class:`pySilhouetteFirstBP1D`

:class:`pyUEqualsUP0D`

:class:`pyVertexNatureUP0D`

:class:`pyViewMapGradientNormBP1D`

:class:`pyZBP1D`

:class:`pyZDiscontinuityBP1D`

:class:`pyZSmallerUP1D`

"""

import typing

import freestyle

class AndBP1D:

  ...

class AndUP1D:

  ...

class ContourUP1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryPredicate1D` > :class:`ContourUP1D`

  """

  def __call__(self, inter: freestyle.types.Interface1D) -> bool:

    """

    Returns true if the Interface1D is a contour.  An Interface1D is a
contour if it is bordered by a different shape on each of its sides.

    """

    ...

class DensityLowerThanUP1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryPredicate1D` > :class:`DensityLowerThanUP1D`

  """

  def __init__(self, threshold: float, sigma: float = 2.0) -> None:

    """

    Builds a DensityLowerThanUP1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> bool:

    """

    Returns true if the density evaluated for the Interface1D is less
than a user-defined density value.

    """

    ...

class EqualToChainingTimeStampUP1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryPredicate1D` > :class:`freestyle.types.EqualToChainingTimeStampUP1D`

  """

  def __init__(self, ts: int) -> None:

    """

    Builds a EqualToChainingTimeStampUP1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> bool:

    """

    Returns true if the Interface1D's time stamp is equal to a certain
user-defined value.

    """

    ...

class EqualToTimeStampUP1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryPredicate1D` > :class:`EqualToTimeStampUP1D`

  """

  def __init__(self, ts: int) -> None:

    """

    Builds a EqualToTimeStampUP1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> bool:

    """

    Returns true if the Interface1D's time stamp is equal to a certain
user-defined value.

    """

    ...

class ExternalContourUP1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryPredicate1D` > :class:`ExternalContourUP1D`

  """

  def __call__(self, inter: freestyle.types.Interface1D) -> bool:

    """

    Returns true if the Interface1D is an external contour.  An
Interface1D is an external contour if it is bordered by no shape on
one of its sides.

    """

    ...

class FalseBP1D:

  """

  Class hierarchy: :class:`freestyle.types.BinaryPredicate1D` > :class:`FalseBP1D`

  """

  def __call__(self, inter1: freestyle.types.Interface1D, inter2: freestyle.types.Interface1D) -> bool:

    """

    Always returns false.

    """

    ...

class FalseUP0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryPredicate0D` > :class:`FalseUP0D`

  """

  def __call__(self, it: freestyle.types.Interface0DIterator) -> bool:

    """

    Always returns false.

    """

    ...

class FalseUP1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryPredicate1D` > :class:`FalseUP1D`

  """

  def __call__(self, inter: freestyle.types.Interface1D) -> bool:

    """

    Always returns false.

    """

    ...

class Length2DBP1D:

  """

  Class hierarchy: :class:`freestyle.types.BinaryPredicate1D` > :class:`Length2DBP1D`

  """

  def __call__(self, inter1: freestyle.types.Interface1D, inter2: freestyle.types.Interface1D) -> bool:

    """

    Returns true if the 2D length of inter1 is less than the 2D length
of inter2.

    """

    ...

class MaterialBP1D:

  """

  Checks whether the two supplied ViewEdges have the same material.

  """

  ...

class NotBP1D:

  ...

class NotUP1D:

  ...

class ObjectNamesUP1D:

  ...

class OrBP1D:

  ...

class OrUP1D:

  ...

class QuantitativeInvisibilityRangeUP1D:

  ...

class QuantitativeInvisibilityUP1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryPredicate1D` > :class:`QuantitativeInvisibilityUP1D`

  """

  def __init__(self, qi: int = 0) -> None:

    """

    Builds a QuantitativeInvisibilityUP1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> bool:

    """

    Returns true if the Quantitative Invisibility evaluated at an
Interface1D, using the
:class:`freestyle.functions.QuantitativeInvisibilityF1D` functor,
equals a certain user-defined value.

    """

    ...

class SameShapeIdBP1D:

  """

  Class hierarchy: :class:`freestyle.types.BinaryPredicate1D` > :class:`SameShapeIdBP1D`

  """

  def __call__(self, inter1: freestyle.types.Interface1D, inter2: freestyle.types.Interface1D) -> bool:

    """

    Returns true if inter1 and inter2 belong to the same shape.

    """

    ...

class ShapeUP1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryPredicate1D` > :class:`ShapeUP1D`

  """

  def __init__(self, first: int, second: int = 0) -> None:

    """

    Builds a ShapeUP1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> bool:

    """

    Returns true if the shape to which the Interface1D belongs to has the
same :class:`freestyle.types.Id` as the one specified by the user.

    """

    ...

class TrueBP1D:

  """

  Class hierarchy: :class:`freestyle.types.BinaryPredicate1D` > :class:`TrueBP1D`

  """

  def __call__(self, inter1: freestyle.types.Interface1D, inter2: freestyle.types.Interface1D) -> bool:

    """

    Always returns true.

    """

    ...

class TrueUP0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryPredicate0D` > :class:`TrueUP0D`

  """

  def __call__(self, it: freestyle.types.Interface0DIterator) -> bool:

    """

    Always returns true.

    """

    ...

class TrueUP1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryPredicate1D` > :class:`TrueUP1D`

  """

  def __call__(self, inter: freestyle.types.Interface1D) -> bool:

    """

    Always returns true.

    """

    ...

class ViewMapGradientNormBP1D:

  """

  Class hierarchy: :class:`freestyle.types.BinaryPredicate1D` > :class:`ViewMapGradientNormBP1D`

  """

  def __init__(self, level: int, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN, sampling: float = 2.0) -> None:

    """

    Builds a ViewMapGradientNormBP1D object.

    """

    ...

  def __call__(self, inter1: freestyle.types.Interface1D, inter2: freestyle.types.Interface1D) -> bool:

    """

    Returns true if the evaluation of the Gradient norm Function is
higher for inter1 than for inter2.

    """

    ...

class WithinImageBoundaryUP1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryPredicate1D` > :class:`WithinImageBoundaryUP1D`

  """

  def __init__(self, xmin: float, ymin: float, xmax: float, ymax: float) -> None:

    """

    Builds an WithinImageBoundaryUP1D object.

    """

    ...

  def __call__(self, inter: typing.Any) -> None:

    """

    Returns true if the Interface1D intersects with image boundary.

    """

    ...

class pyBackTVertexUP0D:

  """

  Check whether an Interface0DIterator references a TVertex and is
the one that is hidden (inferred from the context).

  """

  ...

class pyClosedCurveUP1D:

  ...

class pyDensityFunctorUP1D:

  ...

class pyDensityUP1D:

  ...

class pyDensityVariableSigmaUP1D:

  ...

class pyHighDensityAnisotropyUP1D:

  ...

class pyHighDirectionalViewMapDensityUP1D:

  ...

class pyHighSteerableViewMapDensityUP1D:

  ...

class pyHighViewMapDensityUP1D:

  ...

class pyHighViewMapGradientNormUP1D:

  ...

class pyHigherCurvature2DAngleUP0D:

  ...

class pyHigherLengthUP1D:

  ...

class pyHigherNumberOfTurnsUP1D:

  ...

class pyIsInOccludersListUP1D:

  ...

class pyIsOccludedByIdListUP1D:

  ...

class pyIsOccludedByItselfUP1D:

  ...

class pyIsOccludedByUP1D:

  ...

class pyLengthBP1D:

  ...

class pyLowDirectionalViewMapDensityUP1D:

  ...

class pyLowSteerableViewMapDensityUP1D:

  ...

class pyNFirstUP1D:

  ...

class pyNatureBP1D:

  ...

class pyNatureUP1D:

  ...

class pyParameterUP0D:

  ...

class pyParameterUP0DGoodOne:

  ...

class pyProjectedXBP1D:

  ...

class pyProjectedYBP1D:

  ...

class pyShapeIdListUP1D:

  ...

class pyShapeIdUP1D:

  ...

class pyShuffleBP1D:

  ...

class pySilhouetteFirstBP1D:

  ...

class pyUEqualsUP0D:

  ...

class pyVertexNatureUP0D:

  ...

class pyViewMapGradientNormBP1D:

  ...

class pyZBP1D:

  ...

class pyZDiscontinuityBP1D:

  ...

class pyZSmallerUP1D:

  ...
