"""


Curve Operators
***************

:func:`cyclic_toggle`

:func:`de_select_first`

:func:`de_select_last`

:func:`decimate`

:func:`delete`

:func:`dissolve_verts`

:func:`draw`

:func:`duplicate`

:func:`duplicate_move`

:func:`extrude`

:func:`extrude_move`

:func:`handle_type_set`

:func:`hide`

:func:`make_segment`

:func:`match_texture_space`

:func:`normals_make_consistent`

:func:`primitive_bezier_circle_add`

:func:`primitive_bezier_curve_add`

:func:`primitive_nurbs_circle_add`

:func:`primitive_nurbs_curve_add`

:func:`primitive_nurbs_path_add`

:func:`radius_set`

:func:`reveal`

:func:`select_all`

:func:`select_less`

:func:`select_linked`

:func:`select_linked_pick`

:func:`select_more`

:func:`select_next`

:func:`select_nth`

:func:`select_previous`

:func:`select_random`

:func:`select_row`

:func:`select_similar`

:func:`separate`

:func:`shade_flat`

:func:`shade_smooth`

:func:`shortest_path_pick`

:func:`smooth`

:func:`smooth_radius`

:func:`smooth_tilt`

:func:`smooth_weight`

:func:`spin`

:func:`spline_type_set`

:func:`spline_weight_set`

:func:`split`

:func:`subdivide`

:func:`switch_direction`

:func:`tilt_clear`

:func:`vertex_add`

"""

import typing

def cyclic_toggle(direction: str = 'CYCLIC_U') -> None:

  """

  Make active spline closed/opened loop

  """

  ...

def de_select_first() -> None:

  """

  (De)select first of visible part of each NURBS

  """

  ...

def de_select_last() -> None:

  """

  (De)select last of visible part of each NURBS

  """

  ...

def decimate(ratio: float = 1.0) -> None:

  """

  Simplify selected curves

  """

  ...

def delete(type: str = 'VERT') -> None:

  """

  Delete selected control points or segments

  """

  ...

def dissolve_verts() -> None:

  """

  Delete selected control points, correcting surrounding handles

  """

  ...

def draw(error_threshold: float = 0.0, fit_method: str = 'REFIT', corner_angle: float = 1.22173, use_cyclic: bool = True, stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, wait_for_input: bool = True) -> None:

  """

  Draw a freehand spline

  """

  ...

def duplicate() -> None:

  """

  Duplicate selected control points

  """

  ...

def duplicate_move(CURVE_OT_duplicate: CURVE_OT_duplicate = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Duplicate curve and move

  """

  ...

def extrude(mode: str = 'TRANSLATION') -> None:

  """

  Extrude selected control point(s)

  """

  ...

def extrude_move(CURVE_OT_extrude: CURVE_OT_extrude = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Extrude curve and move result

  """

  ...

def handle_type_set(type: str = 'AUTOMATIC') -> None:

  """

  Set type of handles for selected control points

  """

  ...

def hide(unselected: bool = False) -> None:

  """

  Hide (un)selected control points

  """

  ...

def make_segment() -> None:

  """

  Join two curves by their selected ends

  """

  ...

def match_texture_space() -> None:

  """

  Match texture space to object's bounding box

  """

  ...

def normals_make_consistent(calc_length: bool = False) -> None:

  """

  Recalculate the direction of selected handles

  """

  ...

def primitive_bezier_circle_add(radius: float = 1.0, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a Bezier Circle

  """

  ...

def primitive_bezier_curve_add(radius: float = 1.0, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a Bezier Curve

  """

  ...

def primitive_nurbs_circle_add(radius: float = 1.0, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a Nurbs Circle

  """

  ...

def primitive_nurbs_curve_add(radius: float = 1.0, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a Nurbs Curve

  """

  ...

def primitive_nurbs_path_add(radius: float = 1.0, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a Path

  """

  ...

def radius_set(radius: float = 1.0) -> None:

  """

  Set per-point radius which is used for bevel tapering

  """

  ...

def reveal(select: bool = True) -> None:

  """

  Reveal hidden control points

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  (De)select all control points

  """

  ...

def select_less() -> None:

  """

  Deselect control points at the boundary of each selection region

  """

  ...

def select_linked() -> None:

  """

  Select all control points linked to the current selection

  """

  ...

def select_linked_pick(deselect: bool = False) -> None:

  """

  Select all control points linked to already selected ones

  """

  ...

def select_more() -> None:

  """

  Select control points at the boundary of each selection region

  """

  ...

def select_next() -> None:

  """

  Select control points following already selected ones along the curves

  """

  ...

def select_nth(skip: int = 1, nth: int = 1, offset: int = 0) -> None:

  """

  Deselect every Nth point starting from the active one

  """

  ...

def select_previous() -> None:

  """

  Select control points preceding already selected ones along the curves

  """

  ...

def select_random(ratio: float = 0.5, seed: int = 0, action: str = 'SELECT') -> None:

  """

  Randomly select some control points

  """

  ...

def select_row() -> None:

  """

  Select a row of control points including active one

  """

  ...

def select_similar(type: str = 'WEIGHT', compare: str = 'EQUAL', threshold: float = 0.1) -> None:

  """

  Select similar curve points by property type

  """

  ...

def separate() -> None:

  """

  Separate selected points from connected unselected points into a new object

  """

  ...

def shade_flat() -> None:

  """

  Set shading to flat

  """

  ...

def shade_smooth() -> None:

  """

  Set shading to smooth

  """

  ...

def shortest_path_pick() -> None:

  """

  Select shortest path between two selections

  """

  ...

def smooth() -> None:

  """

  Flatten angles of selected points

  """

  ...

def smooth_radius() -> None:

  """

  Interpolate radii of selected points

  """

  ...

def smooth_tilt() -> None:

  """

  Interpolate tilt of selected points

  """

  ...

def smooth_weight() -> None:

  """

  Interpolate weight of selected points

  """

  ...

def spin(center: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), axis: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Extrude selected boundary row around pivot point and current view axis

  """

  ...

def spline_type_set(type: str = 'POLY', use_handles: bool = False) -> None:

  """

  Set type of active spline

  """

  ...

def spline_weight_set(weight: float = 1.0) -> None:

  """

  Set softbody goal weight for selected points

  """

  ...

def split() -> None:

  """

  Split off selected points from connected unselected points

  """

  ...

def subdivide(number_cuts: int = 1) -> None:

  """

  Subdivide selected segments

  """

  ...

def switch_direction() -> None:

  """

  Switch direction of selected splines

  """

  ...

def tilt_clear() -> None:

  """

  Clear the tilt of selected control points

  """

  ...

def vertex_add(location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Add a new control point (linked to only selected end-curve one, if any)

  """

  ...
