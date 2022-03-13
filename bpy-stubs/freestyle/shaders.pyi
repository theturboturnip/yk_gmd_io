"""


Freestyle Shaders (freestyle.shaders)
*************************************

This module contains stroke shaders used for creation of stylized
strokes.  It is also intended to be a collection of examples for
shader definition in Python.

User-defined stroke shaders inherit the
:class:`freestyle.types.StrokeShader` class.

:class:`BackboneStretcherShader`

:class:`BezierCurveShader`

:class:`BlenderTextureShader`

:class:`CalligraphicShader`

:class:`ColorNoiseShader`

:class:`ConstantColorShader`

:class:`ConstantThicknessShader`

:class:`ConstrainedIncreasingThicknessShader`

:class:`GuidingLinesShader`

:class:`IncreasingColorShader`

:class:`IncreasingThicknessShader`

:class:`PolygonalizationShader`

:class:`RoundCapShader`

:class:`SamplingShader`

:class:`SmoothingShader`

:class:`SpatialNoiseShader`

:class:`SquareCapShader`

:class:`StrokeTextureStepShader`

:class:`ThicknessNoiseShader`

:class:`TipRemoverShader`

:class:`py2DCurvatureColorShader`

:class:`pyBackboneStretcherNoCuspShader`

:class:`pyBackboneStretcherShader`

:class:`pyBluePrintCirclesShader`

:class:`pyBluePrintDirectedSquaresShader`

:class:`pyBluePrintEllipsesShader`

:class:`pyBluePrintSquaresShader`

:class:`pyConstantColorShader`

:class:`pyConstantThicknessShader`

:class:`pyConstrainedIncreasingThicknessShader`

:class:`pyDecreasingThicknessShader`

:class:`pyDepthDiscontinuityThicknessShader`

:class:`pyDiffusion2Shader`

:class:`pyFXSVaryingThicknessWithDensityShader`

:class:`pyGuidingLineShader`

:class:`pyHLRShader`

:class:`pyImportance2DThicknessShader`

:class:`pyImportance3DThicknessShader`

:class:`pyIncreasingColorShader`

:class:`pyIncreasingThicknessShader`

:class:`pyInterpolateColorShader`

:class:`pyLengthDependingBackboneStretcherShader`

:class:`pyMaterialColorShader`

:class:`pyModulateAlphaShader`

:class:`pyNonLinearVaryingThicknessShader`

:class:`pyPerlinNoise1DShader`

:class:`pyPerlinNoise2DShader`

:class:`pyRandomColorShader`

:class:`pySLERPThicknessShader`

:class:`pySamplingShader`

:class:`pySinusDisplacementShader`

:class:`pyTVertexRemoverShader`

:class:`pyTVertexThickenerShader`

:class:`pyTimeColorShader`

:class:`pyTipRemoverShader`

:class:`pyZDependingThicknessShader`

"""

import typing

import mathutils

import freestyle

class BackboneStretcherShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`BackboneStretcherShader`

  [Geometry shader]

  """

  def __init__(self, amount: float = 2.0) -> None:

    """

    Builds a BackboneStretcherShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Stretches the stroke at its two extremities and following the
respective directions: v(1)v(0) and v(n-1)v(n).

    """

    ...

class BezierCurveShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`BezierCurveShader`

  [Geometry shader]

  """

  def __init__(self, error: float = 4.0) -> None:

    """

    Builds a BezierCurveShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Transforms the stroke backbone geometry so that it corresponds to a
Bezier Curve approximation of the original backbone geometry.

    """

    ...

class BlenderTextureShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`BlenderTextureShader`

  [Texture shader]

  """

  def __init__(self, texture: typing.Union[bpy.types.LineStyleTextureSlot]) -> None:

    """

    Builds a BlenderTextureShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Assigns a blender texture slot to the stroke  shading in order to
simulate marks.

    """

    ...

class CalligraphicShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`CalligraphicShader`

  [Thickness Shader]

  """

  def __init__(self, thickness_min: float, thickness_max: float, orientation: mathutils.Vector, clamp: bool) -> None:

    """

    Builds a CalligraphicShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Assigns thicknesses to the stroke vertices so that the stroke looks
like made with a calligraphic tool, i.e. the stroke will be the
thickest in a main direction, and the thinnest in the direction
perpendicular to this one, and an interpolation in between.

    """

    ...

class ColorNoiseShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`ColorNoiseShader`

  [Color shader]

  """

  def __init__(self, amplitude: float, period: float) -> None:

    """

    Builds a ColorNoiseShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Shader to add noise to the stroke colors.

    """

    ...

class ConstantColorShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`ConstantColorShader`

  [Color shader]

  """

  def __init__(self, red: float, green: float, blue: float, alpha: float = 1.0) -> None:

    """

    Builds a ConstantColorShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Assigns a constant color to every vertex of the Stroke.

    """

    ...

class ConstantThicknessShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`ConstantThicknessShader`

  [Thickness shader]

  """

  def __init__(self, thickness: float) -> None:

    """

    Builds a ConstantThicknessShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Assigns an absolute constant thickness to every vertex of the Stroke.

    """

    ...

class ConstrainedIncreasingThicknessShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`ConstrainedIncreasingThicknessShader`

  [Thickness shader]

  """

  def __init__(self, thickness_min: float, thickness_max: float, ratio: float) -> None:

    """

    Builds a ConstrainedIncreasingThicknessShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Same as the :class:`IncreasingThicknessShader`, but here we allow
the user to control the thickness/length ratio so that we don't get
fat short lines.

    """

    ...

class GuidingLinesShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`GuidingLinesShader`

  [Geometry shader]

  """

  def __init__(self, offset: float) -> None:

    """

    Builds a GuidingLinesShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Shader to modify the Stroke geometry so that it corresponds to its
main direction line.  This shader must be used together with the
splitting operator using the curvature criterion. Indeed, the
precision of the approximation will depend on the size of the
stroke's pieces.  The bigger the pieces are, the rougher the
approximation is.

    """

    ...

class IncreasingColorShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`IncreasingColorShader`

  [Color shader]

  """

  def __init__(self, red_min: float, green_min: float, blue_min: float, alpha_min: float, red_max: float, green_max: float, blue_max: float, alpha_max: float) -> None:

    """

    Builds an IncreasingColorShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Assigns a varying color to the stroke.  The user specifies two
colors A and B.  The stroke color will change linearly from A to B
between the first and the last vertex.

    """

    ...

class IncreasingThicknessShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`IncreasingThicknessShader`

  [Thickness shader]

  """

  def __init__(self, thickness_A: float, thickness_B: float) -> None:

    """

    Builds an IncreasingThicknessShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Assigns thicknesses values such as the thickness increases from a
thickness value A to a thickness value B between the first vertex
to the midpoint vertex and then decreases from B to a A between
this midpoint vertex and the last vertex.  The thickness is
linearly interpolated from A to B.

    """

    ...

class PolygonalizationShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`PolygonalizationShader`

  [Geometry shader]

  """

  def __init__(self, error: float) -> None:

    """

    Builds a PolygonalizationShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Modifies the Stroke geometry so that it looks more "polygonal".
The basic idea is to start from the minimal stroke approximation
consisting in a line joining the first vertex to the last one and
to subdivide using the original stroke vertices until a certain
error is reached.

    """

    ...

class RoundCapShader:

  def round_cap_thickness(self, x: typing.Any) -> None:

    ...

  def shade(self, stroke: typing.Any) -> None:

    ...

class SamplingShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`SamplingShader`

  [Geometry shader]

  """

  def __init__(self, sampling: float) -> None:

    """

    Builds a SamplingShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Resamples the stroke.

    """

    ...

class SmoothingShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`SmoothingShader`

  [Geometry shader]

  """

  def __init__(self, num_iterations: int = 100, factor_point: float = 0.1, factor_curvature: float = 0.0, factor_curvature_difference: float = 0.2, aniso_point: float = 0.0, aniso_normal: float = 0.0, aniso_curvature: float = 0.0, carricature_factor: float = 1.0) -> None:

    """

    Builds a SmoothingShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Smooths the stroke by moving the vertices to make the stroke
smoother.  Uses curvature flow to converge towards a curve of
constant curvature.  The diffusion method we use is anisotropic to
prevent the diffusion across corners.

    """

    ...

class SpatialNoiseShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`SpatialNoiseShader`

  [Geometry shader]

  """

  def __init__(self, amount: float, scale: float, num_octaves: int, smooth: bool, pure_random: bool) -> None:

    """

    Builds a SpatialNoiseShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Spatial Noise stroke shader.  Moves the vertices to make the stroke
more noisy.

    """

    ...

class SquareCapShader:

  def shade(self, stroke: typing.Any) -> None:

    ...

class StrokeTextureStepShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`StrokeTextureStepShader`

  [Texture shader]

  """

  def __init__(self, step: float) -> None:

    """

    Builds a StrokeTextureStepShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Assigns a spacing factor to the texture coordinates of the Stroke.

    """

    ...

class ThicknessNoiseShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`ThicknessNoiseShader`

  [Thickness shader]

  """

  def __init__(self, amplitude: float, period: float) -> None:

    """

    Builds a ThicknessNoiseShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Adds some noise to the stroke thickness.

    """

    ...

class TipRemoverShader:

  """

  Class hierarchy: :class:`freestyle.types.StrokeShader` > :class:`TipRemoverShader`

  [Geometry shader]

  """

  def __init__(self, tip_length: float) -> None:

    """

    Builds a TipRemoverShader object.

    """

    ...

  def shade(self, stroke: freestyle.types.Stroke) -> None:

    """

    Removes the stroke's extremities.

    """

    ...

class py2DCurvatureColorShader:

  """

  Assigns a color (grayscale) to the stroke based on the curvature.
A higher curvature will yield a brighter color.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyBackboneStretcherNoCuspShader:

  """

  Stretches the stroke's backbone, excluding cusp vertices (end junctions).

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyBackboneStretcherShader:

  """

  Stretches the stroke's backbone by a given length (in pixels).

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyBluePrintCirclesShader:

  """

  Draws the silhouette of the object as a circle.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyBluePrintDirectedSquaresShader:

  """

  Replaces the stroke with a directed square.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyBluePrintEllipsesShader:

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyBluePrintSquaresShader:

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyConstantColorShader:

  """

  Assigns a constant color to the stroke.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyConstantThicknessShader:

  """

  Assigns a constant thickness along the stroke.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyConstrainedIncreasingThicknessShader:

  """

  Increasingly thickens the stroke, constrained by a ratio of the
stroke's length.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyDecreasingThicknessShader:

  """

  Inverse of pyIncreasingThicknessShader, decreasingly thickens the stroke.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyDepthDiscontinuityThicknessShader:

  """

  Assigns a thickness to the stroke based on the stroke's distance
to the camera (Z-value).

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyDiffusion2Shader:

  """

  Iteratively adds an offset to the position of each stroke vertex
in the direction perpendicular to the stroke direction at the
point. The offset is scaled by the 2D curvature (i.e. how quickly
the stroke curve is) at the point.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyFXSVaryingThicknessWithDensityShader:

  """

  Assigns thickness to a stroke based on the density of the diffuse map.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyGuidingLineShader:

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyHLRShader:

  """

  Controls visibility based upon the quantitative invisibility (QI)
based on hidden line removal (HLR).

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyImportance2DThicknessShader:

  """

  Assigns thickness based on distance to a given point in 2D space.
the thickness is inverted, so the vertices closest to the
specified point have the lowest thickness.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyImportance3DThicknessShader:

  """

  Assigns thickness based on distance to a given point in 3D space.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyIncreasingColorShader:

  """

  Fades from one color to another along the stroke.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyIncreasingThicknessShader:

  """

  Increasingly thickens the stroke.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyInterpolateColorShader:

  """

  Fades from one color to another and back.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyLengthDependingBackboneStretcherShader:

  """

  Stretches the stroke's backbone proportional to the stroke's length
NOTE: you'll probably want an l somewhere between (0.5 - 0). A value that
is too high may yield unexpected results.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyMaterialColorShader:

  """

  Assigns the color of the underlying material to the stroke.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyModulateAlphaShader:

  """

  Limits the stroke's alpha between a min and max value.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyNonLinearVaryingThicknessShader:

  """

  Assigns thickness to a stroke based on an exponential function.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyPerlinNoise1DShader:

  """

  Displaces the stroke using the curvilinear abscissa.  This means
that lines with the same length and sampling interval will be
identically distorded.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyPerlinNoise2DShader:

  """

  Displaces the stroke using the strokes coordinates.  This means
that in a scene no strokes will be distorded identically.

  More information on the noise shaders can be found at:
freestyleintegration.wordpress.com/2011/09/25/development-updates-on-september-25/

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyRandomColorShader:

  """

  Assigns a color to the stroke based on given seed.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pySLERPThicknessShader:

  """

  Assigns thickness to a stroke based on spherical linear interpolation.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pySamplingShader:

  """

  Resamples the stroke, which gives the stroke the amount of
vertices specified.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pySinusDisplacementShader:

  """

  Displaces the stroke in the shape of a sine wave.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyTVertexRemoverShader:

  """

  Removes t-vertices from the stroke.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyTVertexThickenerShader:

  """

  Thickens TVertices (visual intersections between two edges).

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyTimeColorShader:

  """

  Assigns a grayscale value that increases for every vertex.
The brightness will increase along the stroke.

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyTipRemoverShader:

  """

  Removes the tips of the stroke.

  Undocumented

  """

  def shade(self, stroke: typing.Any) -> None:

    ...

class pyZDependingThicknessShader:

  """

  Assigns thickness based on an object's local Z depth (point
closest to camera is 1, point furthest from camera is zero).

  """

  def shade(self, stroke: typing.Any) -> None:

    ...
