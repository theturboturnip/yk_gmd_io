"""


Freestyle Functions (freestyle.functions)
*****************************************

This module contains functions operating on vertices (0D elements) and
polylines (1D elements).  The module is also intended to be a
collection of examples for function definition in Python.

User-defined functions inherit one of the following base classes,
depending on the object type (0D or 1D) to operate on and the return
value type:

* :class:`freestyle.types.UnaryFunction0DDouble`

* :class:`freestyle.types.UnaryFunction0DEdgeNature`

* :class:`freestyle.types.UnaryFunction0DFloat`

* :class:`freestyle.types.UnaryFunction0DId`

* :class:`freestyle.types.UnaryFunction0DMaterial`

* :class:`freestyle.types.UnaryFunction0DUnsigned`

* :class:`freestyle.types.UnaryFunction0DVec2f`

* :class:`freestyle.types.UnaryFunction0DVec3f`

* :class:`freestyle.types.UnaryFunction0DVectorViewShape`

* :class:`freestyle.types.UnaryFunction0DViewShape`

* :class:`freestyle.types.UnaryFunction1DDouble`

* :class:`freestyle.types.UnaryFunction1DEdgeNature`

* :class:`freestyle.types.UnaryFunction1DFloat`

* :class:`freestyle.types.UnaryFunction1DUnsigned`

* :class:`freestyle.types.UnaryFunction1DVec2f`

* :class:`freestyle.types.UnaryFunction1DVec3f`

* :class:`freestyle.types.UnaryFunction1DVectorViewShape`

* :class:`freestyle.types.UnaryFunction1DVoid`

:class:`ChainingTimeStampF1D`

:class:`Curvature2DAngleF0D`

:class:`Curvature2DAngleF1D`

:class:`CurveMaterialF0D`

:class:`CurveNatureF0D`

:class:`CurveNatureF1D`

:class:`DensityF0D`

:class:`DensityF1D`

:class:`GetCompleteViewMapDensityF1D`

:class:`GetCurvilinearAbscissaF0D`

:class:`GetDirectionalViewMapDensityF1D`

:class:`GetOccludeeF0D`

:class:`GetOccludeeF1D`

:class:`GetOccludersF0D`

:class:`GetOccludersF1D`

:class:`GetParameterF0D`

:class:`GetProjectedXF0D`

:class:`GetProjectedXF1D`

:class:`GetProjectedYF0D`

:class:`GetProjectedYF1D`

:class:`GetProjectedZF0D`

:class:`GetProjectedZF1D`

:class:`GetShapeF0D`

:class:`GetShapeF1D`

:class:`GetSteerableViewMapDensityF1D`

:class:`GetViewMapGradientNormF0D`

:class:`GetViewMapGradientNormF1D`

:class:`GetXF0D`

:class:`GetXF1D`

:class:`GetYF0D`

:class:`GetYF1D`

:class:`GetZF0D`

:class:`GetZF1D`

:class:`IncrementChainingTimeStampF1D`

:class:`LocalAverageDepthF0D`

:class:`LocalAverageDepthF1D`

:class:`MaterialF0D`

:class:`Normal2DF0D`

:class:`Normal2DF1D`

:class:`Orientation2DF1D`

:class:`Orientation3DF1D`

:class:`QuantitativeInvisibilityF0D`

:class:`QuantitativeInvisibilityF1D`

:class:`ReadCompleteViewMapPixelF0D`

:class:`ReadMapPixelF0D`

:class:`ReadSteerableViewMapPixelF0D`

:class:`ShapeIdF0D`

:class:`TimeStampF1D`

:class:`VertexOrientation2DF0D`

:class:`VertexOrientation3DF0D`

:class:`ZDiscontinuityF0D`

:class:`ZDiscontinuityF1D`

:class:`pyCurvilinearLengthF0D`

:class:`pyDensityAnisotropyF0D`

:class:`pyDensityAnisotropyF1D`

:class:`pyGetInverseProjectedZF1D`

:class:`pyGetSquareInverseProjectedZF1D`

:class:`pyInverseCurvature2DAngleF0D`

:class:`pyViewMapGradientNormF0D`

:class:`pyViewMapGradientNormF1D`

:class:`pyViewMapGradientVectorF0D`

"""

import typing

import mathutils

import freestyle

class ChainingTimeStampF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DVoid` > :class:`ChainingTimeStampF1D`

  """

  def __init__(self) -> None:

    """

    Builds a ChainingTimeStampF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> None:

    """

    Sets the chaining time stamp of the Interface1D.

    """

    ...

class Curvature2DAngleF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DDouble` > :class:`Curvature2DAngleF0D`

  """

  def __init__(self) -> None:

    """

    Builds a Curvature2DAngleF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns a real value giving the 2D curvature (as an angle) of the 1D
element to which the :class:`freestyle.types.Interface0D` pointed by
the Interface0DIterator belongs.  The 2D curvature is evaluated at the
Interface0D.

    """

    ...

class Curvature2DAngleF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`Curvature2DAngleF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds a Curvature2DAngleF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the 2D curvature as an angle for an Interface1D.

    """

    ...

class CurveMaterialF0D:

  """

  A replacement of the built-in MaterialF0D for stroke creation.
MaterialF0D does not work with Curves and Strokes.  Line color
priority is used to pick one of the two materials at material
boundaries.

  Notes: expects instances of CurvePoint to be iterated over
    can return None if no fedge can be found

  """

  ...

class CurveNatureF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DEdgeNature` > :class:`CurveNatureF0D`

  """

  def __init__(self) -> None:

    """

    Builds a CurveNatureF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> freestyle.types.Nature:

    """

    Returns the :class:`freestyle.types.Nature` of the 1D element the
Interface0D pointed by the Interface0DIterator belongs to.

    """

    ...

class CurveNatureF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DEdgeNature` > :class:`CurveNatureF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds a CurveNatureF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> freestyle.types.Nature:

    """

    Returns the nature of the Interface1D (silhouette, ridge, crease, and
so on).  Except if the Interface1D is a
:class:`freestyle.types.ViewEdge`, this result might be ambiguous.
Indeed, the Interface1D might result from the gathering of several 1D
elements, each one being of a different nature.  An integration
method, such as the MEAN, might give, in this case, irrelevant
results.

    """

    ...

class DensityF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DDouble` > :class:`DensityF0D`

  """

  def __init__(self, sigma: float = 2.0) -> None:

    """

    Builds a DensityF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns the density of the (result) image evaluated at the
:class:`freestyle.types.Interface0D` pointed by the
Interface0DIterator. This density is evaluated using a pixels square
window around the evaluation point and integrating these values using
a gaussian.

    """

    ...

class DensityF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`DensityF1D`

  """

  def __init__(self, sigma: float = 2.0, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN, sampling: float = 2.0) -> None:

    """

    Builds a DensityF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the density evaluated for an Interface1D. The density is
evaluated for a set of points along the Interface1D (using the
:class:`freestyle.functions.DensityF0D` functor) with a user-defined
sampling and then integrated into a single value using a user-defined
integration method.

    """

    ...

class GetCompleteViewMapDensityF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`GetCompleteViewMapDensityF1D`

  """

  def __init__(self, level: int, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN, sampling: float = 2.0) -> None:

    """

    Builds a GetCompleteViewMapDensityF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the density evaluated for an Interface1D in the complete
viewmap image.  The density is evaluated for a set of points along the
Interface1D (using the
:class:`freestyle.functions.ReadCompleteViewMapPixelF0D` functor) and
then integrated into a single value using a user-defined integration
method.

    """

    ...

class GetCurvilinearAbscissaF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DFloat` > :class:`GetCurvilinearAbscissaF0D`

  """

  def __init__(self) -> None:

    """

    Builds a GetCurvilinearAbscissaF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns the curvilinear abscissa of the
:class:`freestyle.types.Interface0D` pointed by the
Interface0DIterator in the context of its 1D element.

    """

    ...

class GetDirectionalViewMapDensityF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`GetDirectionalViewMapDensityF1D`

  """

  def __init__(self, orientation: int, level: int, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN, sampling: float = 2.0) -> None:

    """

    Builds a GetDirectionalViewMapDensityF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the density evaluated for an Interface1D in of the steerable
viewmaps image.  The direction telling which Directional map to choose
is explicitly specified by the user.  The density is evaluated for a
set of points along the Interface1D (using the
:class:`freestyle.functions.ReadSteerableViewMapPixelF0D` functor) and
then integrated into a single value using a user-defined integration
method.

    """

    ...

class GetOccludeeF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DViewShape` > :class:`GetOccludeeF0D`

  """

  def __init__(self) -> None:

    """

    Builds a GetOccludeeF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> freestyle.types.ViewShape:

    """

    Returns the :class:`freestyle.types.ViewShape` that the Interface0D
pointed by the Interface0DIterator occludes.

    """

    ...

class GetOccludeeF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DVectorViewShape` > :class:`GetOccludeeF1D`

  """

  def __init__(self) -> None:

    """

    Builds a GetOccludeeF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> typing.List[freestyle.types.ViewShape]:

    """

    Returns a list of occluded shapes covered by this Interface1D.

    """

    ...

class GetOccludersF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DVectorViewShape` > :class:`GetOccludersF0D`

  """

  def __init__(self) -> None:

    """

    Builds a GetOccludersF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> typing.List[freestyle.types.ViewShape]:

    """

    Returns a list of :class:`freestyle.types.ViewShape` objects occluding the
:class:`freestyle.types.Interface0D` pointed by the Interface0DIterator.

    """

    ...

class GetOccludersF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DVectorViewShape` > :class:`GetOccludersF1D`

  """

  def __init__(self) -> None:

    """

    Builds a GetOccludersF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> typing.List[freestyle.types.ViewShape]:

    """

    Returns a list of occluding shapes that cover this Interface1D.

    """

    ...

class GetParameterF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DFloat` > :class:`GetParameterF0D`

  """

  def __init__(self) -> None:

    """

    Builds a GetParameterF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns the parameter of the :class:`freestyle.types.Interface0D`
pointed by the Interface0DIterator in the context of its 1D element.

    """

    ...

class GetProjectedXF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DDouble` > :class:`GetProjectedXF0D`

  """

  def __init__(self) -> None:

    """

    Builds a GetProjectedXF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns the X 3D projected coordinate of the :class:`freestyle.types.Interface0D`
pointed by the Interface0DIterator.

    """

    ...

class GetProjectedXF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`GetProjectedXF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds a GetProjectedXF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the projected X 3D coordinate of an Interface1D.

    """

    ...

class GetProjectedYF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DDouble` > :class:`GetProjectedYF0D`

  """

  def __init__(self) -> None:

    """

    Builds a GetProjectedYF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns the Y 3D projected coordinate of the :class:`freestyle.types.Interface0D`
pointed by the Interface0DIterator.

    """

    ...

class GetProjectedYF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`GetProjectedYF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds a GetProjectedYF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the projected Y 3D coordinate of an Interface1D.

    """

    ...

class GetProjectedZF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DDouble` > :class:`GetProjectedZF0D`

  """

  def __init__(self) -> None:

    """

    Builds a GetProjectedZF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns the Z 3D projected coordinate of the :class:`freestyle.types.Interface0D`
pointed by the Interface0DIterator.

    """

    ...

class GetProjectedZF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`GetProjectedZF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds a GetProjectedZF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the projected Z 3D coordinate of an Interface1D.

    """

    ...

class GetShapeF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DViewShape` > :class:`GetShapeF0D`

  """

  def __init__(self) -> None:

    """

    Builds a GetShapeF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> freestyle.types.ViewShape:

    """

    Returns the :class:`freestyle.types.ViewShape` containing the
Interface0D pointed by the Interface0DIterator.

    """

    ...

class GetShapeF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DVectorViewShape` > :class:`GetShapeF1D`

  """

  def __init__(self) -> None:

    """

    Builds a GetShapeF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> typing.List[freestyle.types.ViewShape]:

    """

    Returns a list of shapes covered by this Interface1D.

    """

    ...

class GetSteerableViewMapDensityF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`GetSteerableViewMapDensityF1D`

  """

  def __init__(self, level: int, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN, sampling: float = 2.0) -> None:

    """

    Builds a GetSteerableViewMapDensityF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the density of the ViewMap for a given Interface1D.  The
density of each :class:`freestyle.types.FEdge` is evaluated in the
proper steerable :class:`freestyle.types.ViewMap` depending on its
orientation.

    """

    ...

class GetViewMapGradientNormF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DFloat` > :class:`GetViewMapGradientNormF0D`

  """

  def __init__(self, level: int) -> None:

    """

    Builds a GetViewMapGradientNormF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns the norm of the gradient of the global viewmap density
image.

    """

    ...

class GetViewMapGradientNormF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`GetViewMapGradientNormF1D`

  """

  def __init__(self, level: int, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN, sampling: float = 2.0) -> None:

    """

    Builds a GetViewMapGradientNormF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the density of the ViewMap for a given Interface1D.  The
density of each :class:`freestyle.types.FEdge` is evaluated in the
proper steerable :class:`freestyle.types.ViewMap` depending on its
orientation.

    """

    ...

class GetXF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DDouble` > :class:`GetXF0D`

  """

  def __init__(self) -> None:

    """

    Builds a GetXF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns the X 3D coordinate of the :class:`freestyle.types.Interface0D` pointed by
the Interface0DIterator.

    """

    ...

class GetXF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`GetXF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds a GetXF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the X 3D coordinate of an Interface1D.

    """

    ...

class GetYF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DDouble` > :class:`GetYF0D`

  """

  def __init__(self) -> None:

    """

    Builds a GetYF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns the Y 3D coordinate of the :class:`freestyle.types.Interface0D` pointed by
the Interface0DIterator.

    """

    ...

class GetYF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`GetYF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds a GetYF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the Y 3D coordinate of an Interface1D.

    """

    ...

class GetZF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DDouble` > :class:`GetZF0D`

  """

  def __init__(self) -> None:

    """

    Builds a GetZF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns the Z 3D coordinate of the :class:`freestyle.types.Interface0D` pointed by
the Interface0DIterator.

    """

    ...

class GetZF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`GetZF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds a GetZF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the Z 3D coordinate of an Interface1D.

    """

    ...

class IncrementChainingTimeStampF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DVoid` > :class:`IncrementChainingTimeStampF1D`

  """

  def __init__(self) -> None:

    """

    Builds an IncrementChainingTimeStampF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> None:

    """

    Increments the chaining time stamp of the Interface1D.

    """

    ...

class LocalAverageDepthF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DDouble` > :class:`LocalAverageDepthF0D`

  """

  def __init__(self, mask_size: float = 5.0) -> None:

    """

    Builds a LocalAverageDepthF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns the average depth around the
:class:`freestyle.types.Interface0D` pointed by the
Interface0DIterator.  The result is obtained by querying the depth
buffer on a window around that point.

    """

    ...

class LocalAverageDepthF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`LocalAverageDepthF1D`

  """

  def __init__(self, sigma: float, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds a LocalAverageDepthF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns the average depth evaluated for an Interface1D.  The average
depth is evaluated for a set of points along the Interface1D (using
the :class:`freestyle.functions.LocalAverageDepthF0D` functor) with a
user-defined sampling and then integrated into a single value using a
user-defined integration method.

    """

    ...

class MaterialF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DMaterial` > :class:`MaterialF0D`

  """

  def __init__(self) -> None:

    """

    Builds a MaterialF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> freestyle.types.Material:

    """

    Returns the material of the object evaluated at the
:class:`freestyle.types.Interface0D` pointed by the
Interface0DIterator.  This evaluation can be ambiguous (in the case of
a :class:`freestyle.types.TVertex` for example.  This functor tries to
remove this ambiguity using the context offered by the 1D element to
which the Interface0DIterator belongs to and by arbitrary choosing the
material of the face that lies on its left when following the 1D
element if there are two different materials on each side of the
point.  However, there still can be problematic cases, and the user
willing to deal with this cases in a specific way should implement its
own getMaterial functor.

    """

    ...

class Normal2DF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DVec2f` > :class:`Normal2DF0D`

  """

  def __init__(self) -> None:

    """

    Builds a Normal2DF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> mathutils.Vector:

    """

    Returns a two-dimensional vector giving the normalized 2D normal to
the 1D element to which the :class:`freestyle.types.Interface0D`
pointed by the Interface0DIterator belongs.  The normal is evaluated
at the pointed Interface0D.

    """

    ...

class Normal2DF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DVec2f` > :class:`Normal2DF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds a Normal2DF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> mathutils.Vector:

    """

    Returns the 2D normal for the Interface1D.

    """

    ...

class Orientation2DF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DVec2f` > :class:`Orientation2DF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds an Orientation2DF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> mathutils.Vector:

    """

    Returns the 2D orientation of the Interface1D.

    """

    ...

class Orientation3DF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DVec3f` > :class:`Orientation3DF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds an Orientation3DF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> mathutils.Vector:

    """

    Returns the 3D orientation of the Interface1D.

    """

    ...

class QuantitativeInvisibilityF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DUnsigned` > :class:`QuantitativeInvisibilityF0D`

  """

  def __init__(self) -> None:

    """

    Builds a QuantitativeInvisibilityF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> int:

    """

    Returns the quantitative invisibility of the
:class:`freestyle.types.Interface0D` pointed by the
Interface0DIterator.  This evaluation can be ambiguous (in the case of
a :class:`freestyle.types.TVertex` for example).  This functor tries
to remove this ambiguity using the context offered by the 1D element
to which the Interface0D belongs to.  However, there still can be
problematic cases, and the user willing to deal with this cases in a
specific way should implement its own getQIF0D functor.

    """

    ...

class QuantitativeInvisibilityF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DUnsigned` > :class:`QuantitativeInvisibilityF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds a QuantitativeInvisibilityF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> int:

    """

    Returns the Quantitative Invisibility of an Interface1D element. If
the Interface1D is a :class:`freestyle.types.ViewEdge`, then there is
no ambiguity concerning the result.  But, if the Interface1D results
of a chaining (chain, stroke), then it might be made of several 1D
elements of different Quantitative Invisibilities.

    """

    ...

class ReadCompleteViewMapPixelF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DFloat` > :class:`ReadCompleteViewMapPixelF0D`

  """

  def __init__(self, level: int) -> None:

    """

    Builds a ReadCompleteViewMapPixelF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Reads a pixel in one of the level of the complete viewmap.

    """

    ...

class ReadMapPixelF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DFloat` > :class:`ReadMapPixelF0D`

  """

  def __init__(self, map_name: str, level: int) -> None:

    """

    Builds a ReadMapPixelF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Reads a pixel in a map.

    """

    ...

class ReadSteerableViewMapPixelF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DFloat` > :class:`ReadSteerableViewMapPixelF0D`

  """

  def __init__(self, orientation: int, level: int) -> None:

    """

    Builds a ReadSteerableViewMapPixelF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Reads a pixel in one of the level of one of the steerable viewmaps.

    """

    ...

class ShapeIdF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DId` > :class:`ShapeIdF0D`

  """

  def __init__(self) -> None:

    """

    Builds a ShapeIdF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> freestyle.types.Id:

    """

    Returns the :class:`freestyle.types.Id` of the Shape the
:class:`freestyle.types.Interface0D` pointed by the
Interface0DIterator belongs to. This evaluation can be ambiguous (in
the case of a :class:`freestyle.types.TVertex` for example).  This
functor tries to remove this ambiguity using the context offered by
the 1D element to which the Interface0DIterator belongs to. However,
there still can be problematic cases, and the user willing to deal
with this cases in a specific way should implement its own
getShapeIdF0D functor.

    """

    ...

class TimeStampF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DVoid` > :class:`TimeStampF1D`

  """

  def __init__(self) -> None:

    """

    Builds a TimeStampF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> None:

    """

    Returns the time stamp of the Interface1D.

    """

    ...

class VertexOrientation2DF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DVec2f` > :class:`VertexOrientation2DF0D`

  """

  def __init__(self) -> None:

    """

    Builds a VertexOrientation2DF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> mathutils.Vector:

    """

    Returns a two-dimensional vector giving the 2D oriented tangent to the
1D element to which the :class:`freestyle.types.Interface0D` pointed
by the Interface0DIterator belongs.  The 2D oriented tangent is
evaluated at the pointed Interface0D.

    """

    ...

class VertexOrientation3DF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DVec3f` > :class:`VertexOrientation3DF0D`

  """

  def __init__(self) -> None:

    """

    Builds a VertexOrientation3DF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> mathutils.Vector:

    """

    Returns a three-dimensional vector giving the 3D oriented tangent to
the 1D element to which the :class:`freestyle.types.Interface0D`
pointed by the Interface0DIterator belongs.  The 3D oriented tangent
is evaluated at the pointed Interface0D.

    """

    ...

class ZDiscontinuityF0D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction0D` > :class:`freestyle.types.UnaryFunction0DDouble` > :class:`ZDiscontinuityF0D`

  """

  def __init__(self) -> None:

    """

    Builds a ZDiscontinuityF0D object.

    """

    ...

  def __call__(self, it: freestyle.types.Interface0DIterator) -> float:

    """

    Returns a real value giving the distance between the
:class:`freestyle.types.Interface0D` pointed by the
Interface0DIterator and the shape that lies behind (occludee).  This
distance is evaluated in the camera space and normalized between 0 and
1.  Therefore, if no object is occluded by the shape to which the
Interface0D belongs to, 1 is returned.

    """

    ...

class ZDiscontinuityF1D:

  """

  Class hierarchy: :class:`freestyle.types.UnaryFunction1D` > :class:`freestyle.types.UnaryFunction1DDouble` > :class:`ZDiscontinuityF1D`

  """

  def __init__(self, integration_type: freestyle.types.IntegrationType = IntegrationType.MEAN) -> None:

    """

    Builds a ZDiscontinuityF1D object.

    """

    ...

  def __call__(self, inter: freestyle.types.Interface1D) -> float:

    """

    Returns a real value giving the distance between an Interface1D
and the shape that lies behind (occludee).  This distance is
evaluated in the camera space and normalized between 0 and 1.
Therefore, if no object is occluded by the shape to which the
Interface1D belongs to, 1 is returned.

    """

    ...

class pyCurvilinearLengthF0D:

  ...

class pyDensityAnisotropyF0D:

  """

  Estimates the anisotropy of density.

  """

  ...

class pyDensityAnisotropyF1D:

  ...

class pyGetInverseProjectedZF1D:

  ...

class pyGetSquareInverseProjectedZF1D:

  ...

class pyInverseCurvature2DAngleF0D:

  ...

class pyViewMapGradientNormF0D:

  ...

class pyViewMapGradientNormF1D:

  ...

class pyViewMapGradientVectorF0D:

  """

  Returns the gradient vector for a pixel.

  """

  def __init__(self, level: int) -> None:

    """

    Builds a pyViewMapGradientVectorF0D object.

    """

    ...
