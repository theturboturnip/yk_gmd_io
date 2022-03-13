"""


Sculpt Operators
****************

:func:`brush_stroke`

:func:`cloth_filter`

:func:`color_filter`

:func:`detail_flood_fill`

:func:`dirty_mask`

:func:`dynamic_topology_toggle`

:func:`dyntopo_detail_size_edit`

:func:`expand`

:func:`face_set_box_gesture`

:func:`face_set_change_visibility`

:func:`face_set_edit`

:func:`face_set_lasso_gesture`

:func:`face_sets_create`

:func:`face_sets_init`

:func:`face_sets_randomize_colors`

:func:`loop_to_vertex_colors`

:func:`mask_by_color`

:func:`mask_expand`

:func:`mask_filter`

:func:`mask_init`

:func:`mesh_filter`

:func:`optimize`

:func:`project_line_gesture`

:func:`sample_color`

:func:`sample_detail_size`

:func:`sculptmode_toggle`

:func:`set_detail_size`

:func:`set_persistent_base`

:func:`set_pivot_position`

:func:`symmetrize`

:func:`trim_box_gesture`

:func:`trim_lasso_gesture`

:func:`uv_sculpt_stroke`

:func:`vertex_to_loop_colors`

"""

import typing

def brush_stroke(stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, mode: str = 'NORMAL', ignore_background_click: bool = False) -> None:

  """

  Sculpt a stroke into the geometry

  """

  ...

def cloth_filter(type: str = 'GRAVITY', strength: float = 1.0, force_axis: typing.Set[str] = {'X', 'Y', 'Z'}, orientation: str = 'LOCAL', cloth_mass: float = 1.0, cloth_damping: float = 0.0, use_face_sets: bool = False, use_collisions: bool = False) -> None:

  """

  Applies a cloth simulation deformation to the entire mesh

  """

  ...

def color_filter(type: str = 'HUE', strength: float = 1.0, fill_color: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Applies a filter to modify the current sculpt vertex colors

  """

  ...

def detail_flood_fill() -> None:

  """

  Flood fill the mesh with the selected detail setting

  """

  ...

def dirty_mask(dirty_only: bool = False) -> None:

  """

  Generates a mask based on the geometry cavity and pointiness

  """

  ...

def dynamic_topology_toggle() -> None:

  """

  Dynamic topology alters the mesh topology while sculpting

  """

  ...

def dyntopo_detail_size_edit() -> None:

  """

  Modify the detail size of dyntopo interactively

  """

  ...

def expand(target: str = 'MASK', falloff_type: str = 'GEODESIC', invert: bool = False, use_mask_preserve: bool = False, use_falloff_gradient: bool = False, use_modify_active: bool = False, use_reposition_pivot: bool = True, max_geodesic_move_preview: int = 10000) -> None:

  """

  Generic sculpt expand operator

  """

  ...

def face_set_box_gesture(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, use_front_faces_only: bool = False, use_limit_to_segment: bool = False) -> None:

  """

  Add face set within the box as you move the brush

  """

  ...

def face_set_change_visibility(mode: str = 'TOGGLE') -> None:

  """

  Change the visibility of the Face Sets of the sculpt

  """

  ...

def face_set_edit(mode: str = 'GROW', modify_hidden: bool = True) -> None:

  """

  Edits the current active Face Set

  """

  ...

def face_set_lasso_gesture(path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None, use_front_faces_only: bool = False, use_limit_to_segment: bool = False) -> None:

  """

  Add face set within the lasso as you move the brush

  """

  ...

def face_sets_create(mode: str = 'MASKED') -> None:

  """

  Create a new Face Set

  """

  ...

def face_sets_init(mode: str = 'LOOSE_PARTS', threshold: float = 0.5) -> None:

  """

  Initializes all Face Sets in the mesh

  """

  ...

def face_sets_randomize_colors() -> None:

  """

  Generates a new set of random colors to render the Face Sets in the viewport

  """

  ...

def loop_to_vertex_colors() -> None:

  """

  Copy the active loop color layer to the vertex color

  """

  ...

def mask_by_color(contiguous: bool = False, invert: bool = False, preserve_previous_mask: bool = False, threshold: float = 0.35) -> None:

  """

  Creates a mask based on the sculpt vertex colors

  """

  ...

def mask_expand(invert: bool = True, use_cursor: bool = True, update_pivot: bool = True, smooth_iterations: int = 2, mask_speed: int = 5, use_normals: bool = True, keep_previous_mask: bool = False, edge_sensitivity: int = 300, create_face_set: bool = False) -> None:

  """

  Expands a mask from the initial active vertex under the cursor

  """

  ...

def mask_filter(filter_type: str = 'SMOOTH', iterations: int = 1, auto_iteration_count: bool = False) -> None:

  """

  Applies a filter to modify the current mask

  """

  ...

def mask_init(mode: str = 'RANDOM_PER_VERTEX') -> None:

  """

  Creates a new mask for the entire mesh

  """

  ...

def mesh_filter(type: str = 'INFLATE', strength: float = 1.0, deform_axis: typing.Set[str] = {'X', 'Y', 'Z'}, orientation: str = 'LOCAL', surface_smooth_shape_preservation: float = 0.5, surface_smooth_current_vertex: float = 0.5, sharpen_smooth_ratio: float = 0.35, sharpen_intensify_detail_strength: float = 0.0, sharpen_curvature_smooth_iterations: int = 0) -> None:

  """

  Applies a filter to modify the current mesh

  """

  ...

def optimize() -> None:

  """

  Recalculate the sculpt BVH to improve performance

  """

  ...

def project_line_gesture(xstart: int = 0, xend: int = 0, ystart: int = 0, yend: int = 0, flip: bool = False, cursor: int = 5, use_front_faces_only: bool = False, use_limit_to_segment: bool = False) -> None:

  """

  Project the geometry onto a plane defined by a line

  """

  ...

def sample_color() -> None:

  """

  Sample the vertex color of the active vertex

  """

  ...

def sample_detail_size(location: typing.Tuple[int, int] = (0, 0), mode: str = 'DYNTOPO') -> None:

  """

  Sample the mesh detail on clicked point

  """

  ...

def sculptmode_toggle() -> None:

  """

  Toggle sculpt mode in 3D view

  """

  ...

def set_detail_size() -> None:

  """

  Set the mesh detail (either relative or constant one, depending on current dyntopo mode)

  """

  ...

def set_persistent_base() -> None:

  """

  Reset the copy of the mesh that is being sculpted on

  """

  ...

def set_pivot_position(mode: str = 'UNMASKED', mouse_x: float = 0.0, mouse_y: float = 0.0) -> None:

  """

  Sets the sculpt transform pivot position

  """

  ...

def symmetrize(merge_tolerance: float = 0.001) -> None:

  """

  Symmetrize the topology modifications

  """

  ...

def trim_box_gesture(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, use_front_faces_only: bool = False, use_limit_to_segment: bool = False, trim_mode: str = 'DIFFERENCE', use_cursor_depth: bool = False, trim_orientation: str = 'VIEW') -> None:

  """

  Trims the mesh within the box as you move the brush

  """

  ...

def trim_lasso_gesture(path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None, use_front_faces_only: bool = False, use_limit_to_segment: bool = False, trim_mode: str = 'DIFFERENCE', use_cursor_depth: bool = False, trim_orientation: str = 'VIEW') -> None:

  """

  Trims the mesh within the lasso as you move the brush

  """

  ...

def uv_sculpt_stroke(mode: str = 'NORMAL') -> None:

  """

  Sculpt UVs using a brush

  """

  ...

def vertex_to_loop_colors() -> None:

  """

  Copy the Sculpt Vertex Color to a regular color layer

  """

  ...
