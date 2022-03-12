"""


Gpencil Operators
*****************

:func:`active_frame_delete`

:func:`active_frames_delete_all`

:func:`annotate`

:func:`annotation_active_frame_delete`

:func:`annotation_add`

:func:`bake_grease_pencil_animation`

:func:`bake_mesh_animation`

:func:`blank_frame_add`

:func:`brush_reset`

:func:`brush_reset_all`

:func:`convert`

:func:`convert_old_files`

:func:`copy`

:func:`data_unlink`

:func:`delete`

:func:`dissolve`

:func:`draw`

:func:`duplicate`

:func:`duplicate_move`

:func:`editmode_toggle`

:func:`extract_palette_vertex`

:func:`extrude`

:func:`extrude_move`

:func:`fill`

:func:`frame_clean_duplicate`

:func:`frame_clean_fill`

:func:`frame_clean_loose`

:func:`frame_duplicate`

:func:`generate_weights`

:func:`guide_rotate`

:func:`hide`

:func:`image_to_grease_pencil`

:func:`interpolate`

:func:`interpolate_reverse`

:func:`interpolate_sequence`

:func:`layer_active`

:func:`layer_add`

:func:`layer_annotation_add`

:func:`layer_annotation_move`

:func:`layer_annotation_remove`

:func:`layer_change`

:func:`layer_duplicate`

:func:`layer_duplicate_object`

:func:`layer_isolate`

:func:`layer_mask_add`

:func:`layer_mask_move`

:func:`layer_mask_remove`

:func:`layer_merge`

:func:`layer_move`

:func:`layer_remove`

:func:`lock_all`

:func:`lock_layer`

:func:`material_hide`

:func:`material_isolate`

:func:`material_lock_all`

:func:`material_lock_unused`

:func:`material_reveal`

:func:`material_select`

:func:`material_set`

:func:`material_to_vertex_color`

:func:`material_unlock_all`

:func:`materials_copy_to_object`

:func:`move_to_layer`

:func:`paintmode_toggle`

:func:`paste`

:func:`primitive_box`

:func:`primitive_circle`

:func:`primitive_curve`

:func:`primitive_line`

:func:`primitive_polyline`

:func:`recalc_geometry`

:func:`reproject`

:func:`reset_transform_fill`

:func:`reveal`

:func:`sculpt_paint`

:func:`sculptmode_toggle`

:func:`segment_add`

:func:`segment_move`

:func:`segment_remove`

:func:`select`

:func:`select_all`

:func:`select_alternate`

:func:`select_box`

:func:`select_circle`

:func:`select_first`

:func:`select_grouped`

:func:`select_lasso`

:func:`select_last`

:func:`select_less`

:func:`select_linked`

:func:`select_more`

:func:`select_random`

:func:`select_vertex_color`

:func:`selection_opacity_toggle`

:func:`selectmode_toggle`

:func:`set_active_material`

:func:`snap_cursor_to_selected`

:func:`snap_to_cursor`

:func:`snap_to_grid`

:func:`stroke_apply_thickness`

:func:`stroke_arrange`

:func:`stroke_caps_set`

:func:`stroke_change_color`

:func:`stroke_cutter`

:func:`stroke_cyclical_set`

:func:`stroke_editcurve_set_handle_type`

:func:`stroke_enter_editcurve_mode`

:func:`stroke_flip`

:func:`stroke_join`

:func:`stroke_merge`

:func:`stroke_merge_by_distance`

:func:`stroke_merge_material`

:func:`stroke_normalize`

:func:`stroke_reset_vertex_color`

:func:`stroke_sample`

:func:`stroke_separate`

:func:`stroke_simplify`

:func:`stroke_simplify_fixed`

:func:`stroke_smooth`

:func:`stroke_split`

:func:`stroke_subdivide`

:func:`stroke_trim`

:func:`tint_flip`

:func:`trace_image`

:func:`transform_fill`

:func:`unlock_all`

:func:`vertex_color_brightness_contrast`

:func:`vertex_color_hsv`

:func:`vertex_color_invert`

:func:`vertex_color_levels`

:func:`vertex_color_set`

:func:`vertex_group_assign`

:func:`vertex_group_deselect`

:func:`vertex_group_invert`

:func:`vertex_group_normalize`

:func:`vertex_group_normalize_all`

:func:`vertex_group_remove_from`

:func:`vertex_group_select`

:func:`vertex_group_smooth`

:func:`vertex_paint`

:func:`vertexmode_toggle`

:func:`weight_paint`

:func:`weightmode_toggle`

"""

import typing

def active_frame_delete() -> None:

  """

  Delete the active frame for the active Grease Pencil Layer

  """

  ...

def active_frames_delete_all() -> None:

  """

  Delete the active frame(s) of all editable Grease Pencil layers

  """

  ...

def annotate(mode: str = 'DRAW', arrowstyle_start: str = 'NONE', arrowstyle_end: str = 'NONE', use_stabilizer: bool = False, stabilizer_factor: float = 0.75, stabilizer_radius: int = 35, stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, wait_for_input: bool = True) -> None:

  """

  Make annotations on the active data

  """

  ...

def annotation_active_frame_delete() -> None:

  """

  Delete the active frame for the active Annotation Layer

  """

  ...

def annotation_add() -> None:

  """

  Add new Annotation data-block

  """

  ...

def bake_grease_pencil_animation(frame_start: int = 1, frame_end: int = 250, step: int = 1, only_selected: bool = False, frame_target: int = 1, project_type: str = 'KEEP') -> None:

  """

  Bake grease pencil object transform to grease pencil keyframes

  """

  ...

def bake_mesh_animation(target: str = 'NEW', frame_start: int = 1, frame_end: int = 250, step: int = 1, thickness: int = 1, angle: float = 1.22173, offset: float = 0.001, seams: bool = False, faces: bool = True, only_selected: bool = False, frame_target: int = 1, project_type: str = 'VIEW') -> None:

  """

  Bake mesh animation to grease pencil strokes

  """

  ...

def blank_frame_add(all_layers: bool = False) -> None:

  """

  Insert a blank frame on the current frame (all subsequently existing frames, if any, are shifted right by one frame)

  """

  ...

def brush_reset() -> None:

  """

  Reset brush to default parameters

  """

  ...

def brush_reset_all() -> None:

  """

  Delete all mode brushes and recreate a default set

  """

  ...

def convert(type: str = 'PATH', bevel_depth: float = 0.0, bevel_resolution: int = 0, use_normalize_weights: bool = True, radius_multiplier: float = 1.0, use_link_strokes: bool = False, timing_mode: str = 'FULL', frame_range: int = 100, start_frame: int = 1, use_realtime: bool = False, end_frame: int = 250, gap_duration: float = 0.0, gap_randomness: float = 0.0, seed: int = 0, use_timing_data: bool = False) -> None:

  """

  Convert the active Grease Pencil layer to a new Curve Object

  """

  ...

def convert_old_files(annotation: bool = False) -> None:

  """

  Convert 2.7x grease pencil files to 2.80

  """

  ...

def copy() -> None:

  """

  Copy selected Grease Pencil points and strokes

  """

  ...

def data_unlink() -> None:

  """

  Unlink active Annotation data-block

  """

  ...

def delete(type: str = 'POINTS') -> None:

  """

  Delete selected Grease Pencil strokes, vertices, or frames

  """

  ...

def dissolve(type: str = 'POINTS') -> None:

  """

  Delete selected points without splitting strokes

  """

  ...

def draw(mode: str = 'DRAW', stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, wait_for_input: bool = True, disable_straight: bool = False, disable_fill: bool = False, disable_stabilizer: bool = False, guide_last_angle: float = 0.0) -> None:

  """

  Draw a new stroke in the active Grease Pencil object

  """

  ...

def duplicate() -> None:

  """

  Duplicate the selected Grease Pencil strokes

  """

  ...

def duplicate_move(GPENCIL_OT_duplicate: GPENCIL_OT_duplicate = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Make copies of the selected Grease Pencil strokes and move them

  """

  ...

def editmode_toggle(back: bool = False) -> None:

  """

  Enter/Exit edit mode for Grease Pencil strokes

  """

  ...

def extract_palette_vertex(selected: bool = False, threshold: int = 1) -> None:

  """

  Extract all colors used in Grease Pencil Vertex and create a Palette

  """

  ...

def extrude() -> None:

  """

  Extrude the selected Grease Pencil points

  """

  ...

def extrude_move(GPENCIL_OT_extrude: GPENCIL_OT_extrude = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Extrude selected points and move them

  """

  ...

def fill(on_back: bool = False) -> None:

  """

  Fill with color the shape formed by strokes

  """

  ...

def frame_clean_duplicate(type: str = 'ALL') -> None:

  """

  Remove any duplicated frame

  """

  ...

def frame_clean_fill(mode: str = 'ACTIVE') -> None:

  """

  Remove 'no fill' boundary strokes

  """

  ...

def frame_clean_loose(limit: int = 1) -> None:

  """

  Remove loose points

  """

  ...

def frame_duplicate(mode: str = 'ACTIVE') -> None:

  """

  Make a copy of the active Grease Pencil Frame

  """

  ...

def generate_weights(mode: str = 'NAME', armature: str = 'DEFAULT', ratio: float = 0.1, decay: float = 0.8) -> None:

  """

  Generate automatic weights for armatures (requires armature modifier)

  """

  ...

def guide_rotate(increment: bool = True, angle: float = 0.0) -> None:

  """

  Rotate guide angle

  """

  ...

def hide(unselected: bool = False) -> None:

  """

  Hide selected/unselected Grease Pencil layers

  """

  ...

def image_to_grease_pencil(size: float = 0.005, mask: bool = False) -> None:

  """

  Generate a Grease Pencil Object using Image as source

  """

  ...

def interpolate(shift: float = 0.0, layers: str = 'ACTIVE', interpolate_selected_only: bool = False, flip: str = 'AUTO', smooth_steps: int = 1, smooth_factor: float = 0.0, release_confirm: bool = False) -> None:

  """

  Interpolate grease pencil strokes between frames

  """

  ...

def interpolate_reverse() -> None:

  """

  Remove breakdown frames generated by interpolating between two Grease Pencil frames

  """

  ...

def interpolate_sequence(step: int = 1, layers: str = 'ACTIVE', interpolate_selected_only: bool = False, flip: str = 'AUTO', smooth_steps: int = 1, smooth_factor: float = 0.0, type: str = 'LINEAR', easing: str = 'AUTO', back: float = 1.702, amplitude: float = 0.15, period: float = 0.15) -> None:

  """

  Generate 'in-betweens' to smoothly interpolate between Grease Pencil frames

  """

  ...

def layer_active(layer: int = 0) -> None:

  """

  Active Grease Pencil layer

  """

  ...

def layer_add() -> None:

  """

  Add new layer or note for the active data-block

  """

  ...

def layer_annotation_add() -> None:

  """

  Add new Annotation layer or note for the active data-block

  """

  ...

def layer_annotation_move(type: str = 'UP') -> None:

  """

  Move the active Annotation layer up/down in the list

  """

  ...

def layer_annotation_remove() -> None:

  """

  Remove active Annotation layer

  """

  ...

def layer_change(layer: str = 'DEFAULT') -> None:

  """

  Change active Grease Pencil layer

  """

  ...

def layer_duplicate(mode: str = 'ALL') -> None:

  """

  Make a copy of the active Grease Pencil layer

  """

  ...

def layer_duplicate_object(mode: str = 'ALL', only_active: bool = True) -> None:

  """

  Make a copy of the active Grease Pencil layer to selected object

  """

  ...

def layer_isolate(affect_visibility: bool = False) -> None:

  """

  Toggle whether the active layer is the only one that can be edited and/or visible

  """

  ...

def layer_mask_add(name: str = '') -> None:

  """

  Add new layer as masking

  """

  ...

def layer_mask_move(type: str = 'UP') -> None:

  """

  Move the active Grease Pencil mask layer up/down in the list

  """

  ...

def layer_mask_remove() -> None:

  """

  Remove Layer Mask

  """

  ...

def layer_merge() -> None:

  """

  Merge the current layer with the layer below

  """

  ...

def layer_move(type: str = 'UP') -> None:

  """

  Move the active Grease Pencil layer up/down in the list

  """

  ...

def layer_remove() -> None:

  """

  Remove active Grease Pencil layer

  """

  ...

def lock_all() -> None:

  """

  Lock all Grease Pencil layers to prevent them from being accidentally modified

  """

  ...

def lock_layer() -> None:

  """

  Lock and hide any color not used in any layer

  """

  ...

def material_hide(unselected: bool = False) -> None:

  """

  Hide selected/unselected Grease Pencil materials

  """

  ...

def material_isolate(affect_visibility: bool = False) -> None:

  """

  Toggle whether the active material is the only one that is editable and/or visible

  """

  ...

def material_lock_all() -> None:

  """

  Lock all Grease Pencil materials to prevent them from being accidentally modified

  """

  ...

def material_lock_unused() -> None:

  """

  Lock any material not used in any selected stroke

  """

  ...

def material_reveal() -> None:

  """

  Unhide all hidden Grease Pencil materials

  """

  ...

def material_select(deselect: bool = False) -> None:

  """

  Select/Deselect all Grease Pencil strokes using current material

  """

  ...

def material_set(slot: str = 'DEFAULT') -> None:

  """

  Set active material

  """

  ...

def material_to_vertex_color(remove: bool = True, palette: bool = True, selected: bool = False, threshold: int = 3) -> None:

  """

  Replace materials in strokes with Vertex Color

  """

  ...

def material_unlock_all() -> None:

  """

  Unlock all Grease Pencil materials so that they can be edited

  """

  ...

def materials_copy_to_object(only_active: bool = True) -> None:

  """

  Append Materials of the active Grease Pencil to other object

  """

  ...

def move_to_layer(layer: int = 0) -> None:

  """

  Move selected strokes to another layer

  """

  ...

def paintmode_toggle(back: bool = False) -> None:

  """

  Enter/Exit paint mode for Grease Pencil strokes

  """

  ...

def paste(type: str = 'ACTIVE', paste_back: bool = False) -> None:

  """

  Paste previously copied strokes to active layer or to original layer

  """

  ...

def primitive_box(subdivision: int = 3, edges: int = 2, type: str = 'BOX', wait_for_input: bool = True) -> None:

  """

  Create predefined grease pencil stroke box shapes

  """

  ...

def primitive_circle(subdivision: int = 94, edges: int = 2, type: str = 'CIRCLE', wait_for_input: bool = True) -> None:

  """

  Create predefined grease pencil stroke circle shapes

  """

  ...

def primitive_curve(subdivision: int = 62, edges: int = 2, type: str = 'CURVE', wait_for_input: bool = True) -> None:

  """

  Create predefined grease pencil stroke curve shapes

  """

  ...

def primitive_line(subdivision: int = 6, edges: int = 2, type: str = 'LINE', wait_for_input: bool = True) -> None:

  """

  Create predefined grease pencil stroke lines

  """

  ...

def primitive_polyline(subdivision: int = 6, edges: int = 2, type: str = 'POLYLINE', wait_for_input: bool = True) -> None:

  """

  Create predefined grease pencil stroke polylines

  """

  ...

def recalc_geometry() -> None:

  """

  Update all internal geometry data

  """

  ...

def reproject(type: str = 'VIEW', keep_original: bool = False) -> None:

  """

  Reproject the selected strokes from the current viewpoint as if they had been newly drawn (e.g. to fix problems from accidental 3D cursor movement or accidental viewport changes, or for matching deforming geometry)

  """

  ...

def reset_transform_fill(mode: str = 'ALL') -> None:

  """

  Reset any UV transformation and back to default values

  """

  ...

def reveal(select: bool = True) -> None:

  """

  Show all Grease Pencil layers

  """

  ...

def sculpt_paint(stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, wait_for_input: bool = True) -> None:

  """

  Apply tweaks to strokes by painting over the strokes

  """

  ...

def sculptmode_toggle(back: bool = False) -> None:

  """

  Enter/Exit sculpt mode for Grease Pencil strokes

  """

  ...

def segment_add(modifier: str = '') -> None:

  """

  Add a segment to the dash modifier

  """

  ...

def segment_move(modifier: str = '', type: str = 'UP') -> None:

  """

  Move the active dash segment up or down

  """

  ...

def segment_remove(modifier: str = '', index: int = 0) -> None:

  """

  Remove the active segment from the dash modifier

  """

  ...

def select(extend: bool = False, deselect: bool = False, toggle: bool = False, deselect_all: bool = False, entire_strokes: bool = False, location: typing.Tuple[int, int] = (0, 0), use_shift_extend: bool = False) -> None:

  """

  Select Grease Pencil strokes and/or stroke points

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Change selection of all Grease Pencil strokes currently visible

  """

  ...

def select_alternate(unselect_ends: bool = False) -> None:

  """

  Select alternative points in same strokes as already selected points

  """

  ...

def select_box(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Select Grease Pencil strokes within a rectangular region

  """

  ...

def select_circle(x: int = 0, y: int = 0, radius: int = 25, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Select Grease Pencil strokes using brush selection

  """

  ...

def select_first(only_selected_strokes: bool = False, extend: bool = False) -> None:

  """

  Select first point in Grease Pencil strokes

  """

  ...

def select_grouped(type: str = 'LAYER') -> None:

  """

  Select all strokes with similar characteristics

  """

  ...

def select_lasso(mode: str = 'SET', path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None) -> None:

  """

  Select Grease Pencil strokes using lasso selection

  """

  ...

def select_last(only_selected_strokes: bool = False, extend: bool = False) -> None:

  """

  Select last point in Grease Pencil strokes

  """

  ...

def select_less() -> None:

  """

  Shrink sets of selected Grease Pencil points

  """

  ...

def select_linked() -> None:

  """

  Select all points in same strokes as already selected points

  """

  ...

def select_more() -> None:

  """

  Grow sets of selected Grease Pencil points

  """

  ...

def select_random(ratio: float = 0.5, seed: int = 0, action: str = 'SELECT', unselect_ends: bool = False) -> None:

  """

  Select random points for non selected strokes

  """

  ...

def select_vertex_color(threshold: int = 0) -> None:

  """

  Select all points with similar vertex color of current selected

  """

  ...

def selection_opacity_toggle() -> None:

  """

  Hide/Unhide selected points for Grease Pencil strokes setting alpha factor

  """

  ...

def selectmode_toggle(mode: int = 0) -> None:

  """

  Set selection mode for Grease Pencil strokes

  """

  ...

def set_active_material() -> None:

  """

  Set the selected stroke material as the active material

  """

  ...

def snap_cursor_to_selected() -> None:

  """

  Snap cursor to center of selected points

  """

  ...

def snap_to_cursor(use_offset: bool = True) -> None:

  """

  Snap selected points/strokes to the cursor

  """

  ...

def snap_to_grid() -> None:

  """

  Snap selected points to the nearest grid points

  """

  ...

def stroke_apply_thickness() -> None:

  """

  Apply the thickness change of the layer to its strokes

  """

  ...

def stroke_arrange(direction: str = 'UP') -> None:

  """

  Arrange selected strokes up/down in the display order of the active layer

  """

  ...

def stroke_caps_set(type: str = 'TOGGLE') -> None:

  """

  Change stroke caps mode (rounded or flat)

  """

  ...

def stroke_change_color(material: str = '') -> None:

  """

  Move selected strokes to active material

  """

  ...

def stroke_cutter(path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None, flat_caps: bool = False) -> None:

  """

  Select section and cut

  """

  ...

def stroke_cyclical_set(type: str = 'TOGGLE', geometry: bool = False) -> None:

  """

  Close or open the selected stroke adding an edge from last to first point

  """

  ...

def stroke_editcurve_set_handle_type(type: str = 'AUTOMATIC') -> None:

  """

  Set the type of a edit curve handle

  """

  ...

def stroke_enter_editcurve_mode(error_threshold: float = 0.1) -> None:

  """

  Called to transform a stroke into a curve

  """

  ...

def stroke_flip() -> None:

  """

  Change direction of the points of the selected strokes

  """

  ...

def stroke_join(type: str = 'JOIN', leave_gaps: bool = False) -> None:

  """

  Join selected strokes (optionally as new stroke)

  """

  ...

def stroke_merge(mode: str = 'STROKE', back: bool = False, additive: bool = False, cyclic: bool = False, clear_point: bool = False, clear_stroke: bool = False) -> None:

  """

  Create a new stroke with the selected stroke points

  """

  ...

def stroke_merge_by_distance(threshold: float = 0.001, use_unselected: bool = False) -> None:

  """

  Merge points by distance

  """

  ...

def stroke_merge_material(hue_threshold: float = 0.001, sat_threshold: float = 0.001, val_threshold: float = 0.001) -> None:

  """

  Replace materials in strokes merging similar

  """

  ...

def stroke_normalize(mode: str = 'THICKNESS', factor: float = 1.0, value: int = 10) -> None:

  """

  Normalize stroke attributes

  """

  ...

def stroke_reset_vertex_color(mode: str = 'BOTH') -> None:

  """

  Reset vertex color for all or selected strokes

  """

  ...

def stroke_sample(length: float = 0.1) -> None:

  """

  Sample stroke points to predefined segment length

  """

  ...

def stroke_separate(mode: str = 'POINT') -> None:

  """

  Separate the selected strokes or layer in a new grease pencil object

  """

  ...

def stroke_simplify(factor: float = 0.0) -> None:

  """

  Simplify selected stroked reducing number of points

  """

  ...

def stroke_simplify_fixed(step: int = 1) -> None:

  """

  Simplify selected stroked reducing number of points using fixed algorithm

  """

  ...

def stroke_smooth(repeat: int = 1, factor: float = 0.5, only_selected: bool = True, smooth_position: bool = True, smooth_thickness: bool = True, smooth_strength: bool = False, smooth_uv: bool = False) -> None:

  """

  Smooth selected strokes

  """

  ...

def stroke_split() -> None:

  """

  Split selected points as new stroke on same frame

  """

  ...

def stroke_subdivide(number_cuts: int = 1, factor: float = 0.0, repeat: int = 1, only_selected: bool = True, smooth_position: bool = True, smooth_thickness: bool = True, smooth_strength: bool = False, smooth_uv: bool = False) -> None:

  """

  Subdivide between continuous selected points of the stroke adding a point half way between them

  """

  ...

def stroke_trim() -> None:

  """

  Trim selected stroke to first loop or intersection

  """

  ...

def tint_flip() -> None:

  """

  Switch tint colors

  """

  ...

def trace_image(target: str = 'NEW', thickness: int = 10, resolution: int = 5, scale: float = 1.0, sample: float = 0.0, threshold: float = 0.5, turnpolicy: str = 'MINORITY', mode: str = 'SINGLE', use_current_frame: bool = True) -> None:

  """

  Extract Grease Pencil strokes from image

  """

  ...

def transform_fill(mode: str = 'ROTATE', location: typing.Tuple[float, float] = (0.0, 0.0), rotation: float = 0.0, scale: float = 0.0, release_confirm: bool = False) -> None:

  """

  Transform grease pencil stroke fill

  """

  ...

def unlock_all() -> None:

  """

  Unlock all Grease Pencil layers so that they can be edited

  """

  ...

def vertex_color_brightness_contrast(mode: str = 'BOTH', brightness: float = 0.0, contrast: float = 0.0) -> None:

  """

  Adjust vertex color brightness/contrast

  """

  ...

def vertex_color_hsv(mode: str = 'BOTH', h: float = 0.5, s: float = 1.0, v: float = 1.0) -> None:

  """

  Adjust vertex color HSV values

  """

  ...

def vertex_color_invert(mode: str = 'BOTH') -> None:

  """

  Invert RGB values

  """

  ...

def vertex_color_levels(mode: str = 'BOTH', offset: float = 0.0, gain: float = 1.0) -> None:

  """

  Adjust levels of vertex colors

  """

  ...

def vertex_color_set(mode: str = 'BOTH', factor: float = 1.0) -> None:

  """

  Set active color to all selected vertex

  """

  ...

def vertex_group_assign() -> None:

  """

  Assign the selected vertices to the active vertex group

  """

  ...

def vertex_group_deselect() -> None:

  """

  Deselect all selected vertices assigned to the active vertex group

  """

  ...

def vertex_group_invert() -> None:

  """

  Invert weights to the active vertex group

  """

  ...

def vertex_group_normalize() -> None:

  """

  Normalize weights to the active vertex group

  """

  ...

def vertex_group_normalize_all(lock_active: bool = True) -> None:

  """

  Normalize all weights of all vertex groups, so that for each vertex, the sum of all weights is 1.0

  """

  ...

def vertex_group_remove_from() -> None:

  """

  Remove the selected vertices from active or all vertex group(s)

  """

  ...

def vertex_group_select() -> None:

  """

  Select all the vertices assigned to the active vertex group

  """

  ...

def vertex_group_smooth(factor: float = 0.5, repeat: int = 1) -> None:

  """

  Smooth weights to the active vertex group

  """

  ...

def vertex_paint(stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, wait_for_input: bool = True) -> None:

  """

  Paint stroke points with a color

  """

  ...

def vertexmode_toggle(back: bool = False) -> None:

  """

  Enter/Exit vertex paint mode for Grease Pencil strokes

  """

  ...

def weight_paint(stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, wait_for_input: bool = True) -> None:

  """

  Paint stroke points with a color

  """

  ...

def weightmode_toggle(back: bool = False) -> None:

  """

  Enter/Exit weight paint mode for Grease Pencil strokes

  """

  ...
