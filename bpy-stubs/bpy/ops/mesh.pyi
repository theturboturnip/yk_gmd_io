"""


Mesh Operators
**************

:func:`average_normals`

:func:`beautify_fill`

:func:`bevel`

:func:`bisect`

:func:`blend_from_shape`

:func:`bridge_edge_loops`

:func:`colors_reverse`

:func:`colors_rotate`

:func:`convex_hull`

:func:`customdata_custom_splitnormals_add`

:func:`customdata_custom_splitnormals_clear`

:func:`customdata_mask_clear`

:func:`customdata_skin_add`

:func:`customdata_skin_clear`

:func:`decimate`

:func:`delete`

:func:`delete_edgeloop`

:func:`delete_loose`

:func:`dissolve_degenerate`

:func:`dissolve_edges`

:func:`dissolve_faces`

:func:`dissolve_limited`

:func:`dissolve_mode`

:func:`dissolve_verts`

:func:`dupli_extrude_cursor`

:func:`duplicate`

:func:`duplicate_move`

:func:`edge_collapse`

:func:`edge_face_add`

:func:`edge_rotate`

:func:`edge_split`

:func:`edgering_select`

:func:`edges_select_sharp`

:func:`extrude_context`

:func:`extrude_context_move`

:func:`extrude_edges_indiv`

:func:`extrude_edges_move`

:func:`extrude_faces_indiv`

:func:`extrude_faces_move`

:func:`extrude_manifold`

:func:`extrude_region`

:func:`extrude_region_move`

:func:`extrude_region_shrink_fatten`

:func:`extrude_repeat`

:func:`extrude_vertices_move`

:func:`extrude_verts_indiv`

:func:`face_make_planar`

:func:`face_set_extract`

:func:`face_split_by_edges`

:func:`faces_mirror_uv`

:func:`faces_select_linked_flat`

:func:`faces_shade_flat`

:func:`faces_shade_smooth`

:func:`fill`

:func:`fill_grid`

:func:`fill_holes`

:func:`flip_normals`

:func:`hide`

:func:`inset`

:func:`intersect`

:func:`intersect_boolean`

:func:`knife_project`

:func:`knife_tool`

:func:`loop_multi_select`

:func:`loop_select`

:func:`loop_to_region`

:func:`loopcut`

:func:`loopcut_slide`

:func:`mark_freestyle_edge`

:func:`mark_freestyle_face`

:func:`mark_seam`

:func:`mark_sharp`

:func:`merge`

:func:`merge_normals`

:func:`mod_weighted_strength`

:func:`normals_make_consistent`

:func:`normals_tools`

:func:`offset_edge_loops`

:func:`offset_edge_loops_slide`

:func:`paint_mask_extract`

:func:`paint_mask_slice`

:func:`point_normals`

:func:`poke`

:func:`polybuild_delete_at_cursor`

:func:`polybuild_dissolve_at_cursor`

:func:`polybuild_extrude_at_cursor_move`

:func:`polybuild_face_at_cursor`

:func:`polybuild_face_at_cursor_move`

:func:`polybuild_split_at_cursor`

:func:`polybuild_split_at_cursor_move`

:func:`polybuild_transform_at_cursor`

:func:`polybuild_transform_at_cursor_move`

:func:`primitive_circle_add`

:func:`primitive_cone_add`

:func:`primitive_cube_add`

:func:`primitive_cube_add_gizmo`

:func:`primitive_cylinder_add`

:func:`primitive_grid_add`

:func:`primitive_ico_sphere_add`

:func:`primitive_monkey_add`

:func:`primitive_plane_add`

:func:`primitive_torus_add`

:func:`primitive_uv_sphere_add`

:func:`quads_convert_to_tris`

:func:`region_to_loop`

:func:`remove_doubles`

:func:`reveal`

:func:`rip`

:func:`rip_edge`

:func:`rip_edge_move`

:func:`rip_move`

:func:`screw`

:func:`sculpt_vertex_color_add`

:func:`sculpt_vertex_color_remove`

:func:`select_all`

:func:`select_axis`

:func:`select_face_by_sides`

:func:`select_interior_faces`

:func:`select_less`

:func:`select_linked`

:func:`select_linked_pick`

:func:`select_loose`

:func:`select_mirror`

:func:`select_mode`

:func:`select_more`

:func:`select_next_item`

:func:`select_non_manifold`

:func:`select_nth`

:func:`select_prev_item`

:func:`select_random`

:func:`select_similar`

:func:`select_similar_region`

:func:`select_ungrouped`

:func:`separate`

:func:`set_normals_from_faces`

:func:`shape_propagate_to_all`

:func:`shortest_path_pick`

:func:`shortest_path_select`

:func:`smooth_normals`

:func:`solidify`

:func:`sort_elements`

:func:`spin`

:func:`split`

:func:`split_normals`

:func:`subdivide`

:func:`subdivide_edgering`

:func:`symmetrize`

:func:`symmetry_snap`

:func:`tris_convert_to_quads`

:func:`unsubdivide`

:func:`uv_texture_add`

:func:`uv_texture_remove`

:func:`uvs_reverse`

:func:`uvs_rotate`

:func:`vert_connect`

:func:`vert_connect_concave`

:func:`vert_connect_nonplanar`

:func:`vert_connect_path`

:func:`vertex_color_add`

:func:`vertex_color_remove`

:func:`vertices_smooth`

:func:`vertices_smooth_laplacian`

:func:`wireframe`

"""

import typing

def average_normals(average_type: str = 'CUSTOM_NORMAL', weight: int = 50, threshold: float = 0.01) -> None:

  """

  Average custom normals of selected vertices

  """

  ...

def beautify_fill(angle_limit: float = 3.14159) -> None:

  """

  Rearrange some faces to try to get less degenerated geometry

  """

  ...

def bevel(offset_type: str = 'OFFSET', offset: float = 0.0, profile_type: str = 'SUPERELLIPSE', offset_pct: float = 0.0, segments: int = 1, profile: float = 0.5, affect: str = 'EDGES', clamp_overlap: bool = False, loop_slide: bool = True, mark_seam: bool = False, mark_sharp: bool = False, material: int = -1, harden_normals: bool = False, face_strength_mode: str = 'NONE', miter_outer: str = 'SHARP', miter_inner: str = 'SHARP', spread: float = 0.1, vmesh_method: str = 'ADJ', release_confirm: bool = False) -> None:

  """

  Cut into selected items at an angle to create bevel or chamfer

  """

  ...

def bisect(plane_co: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), plane_no: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), use_fill: bool = False, clear_inner: bool = False, clear_outer: bool = False, threshold: float = 0.0001, xstart: int = 0, xend: int = 0, ystart: int = 0, yend: int = 0, flip: bool = False, cursor: int = 5) -> None:

  """

  Cut geometry along a plane (click-drag to define plane)

  """

  ...

def blend_from_shape(shape: str = '', blend: float = 1.0, add: bool = True) -> None:

  """

  Blend in shape from a shape key

  """

  ...

def bridge_edge_loops(type: str = 'SINGLE', use_merge: bool = False, merge_factor: float = 0.5, twist_offset: int = 0, number_cuts: int = 0, interpolation: str = 'PATH', smoothness: float = 1.0, profile_shape_factor: float = 0.0, profile_shape: str = 'SMOOTH') -> None:

  """

  Create a bridge of faces between two or more selected edge loops

  """

  ...

def colors_reverse() -> None:

  """

  Flip direction of vertex colors inside faces

  """

  ...

def colors_rotate(use_ccw: bool = False) -> None:

  """

  Rotate vertex colors inside faces

  """

  ...

def convex_hull(delete_unused: bool = True, use_existing_faces: bool = True, make_holes: bool = False, join_triangles: bool = True, face_threshold: float = 0.698132, shape_threshold: float = 0.698132, uvs: bool = False, vcols: bool = False, seam: bool = False, sharp: bool = False, materials: bool = False) -> None:

  """

  Enclose selected vertices in a convex polyhedron

  """

  ...

def customdata_custom_splitnormals_add() -> None:

  """

  Add a custom split normals layer, if none exists yet

  """

  ...

def customdata_custom_splitnormals_clear() -> None:

  """

  Remove the custom split normals layer, if it exists

  """

  ...

def customdata_mask_clear() -> None:

  """

  Clear vertex sculpt masking data from the mesh

  """

  ...

def customdata_skin_add() -> None:

  """

  Add a vertex skin layer

  """

  ...

def customdata_skin_clear() -> None:

  """

  Clear vertex skin layer

  """

  ...

def decimate(ratio: float = 1.0, use_vertex_group: bool = False, vertex_group_factor: float = 1.0, invert_vertex_group: bool = False, use_symmetry: bool = False, symmetry_axis: str = 'Y') -> None:

  """

  Simplify geometry by collapsing edges

  """

  ...

def delete(type: str = 'VERT') -> None:

  """

  Delete selected vertices, edges or faces

  """

  ...

def delete_edgeloop(use_face_split: bool = True) -> None:

  """

  Delete an edge loop by merging the faces on each side

  """

  ...

def delete_loose(use_verts: bool = True, use_edges: bool = True, use_faces: bool = False) -> None:

  """

  Delete loose vertices, edges or faces

  """

  ...

def dissolve_degenerate(threshold: float = 0.0001) -> None:

  """

  Dissolve zero area faces and zero length edges

  """

  ...

def dissolve_edges(use_verts: bool = True, use_face_split: bool = False) -> None:

  """

  Dissolve edges, merging faces

  """

  ...

def dissolve_faces(use_verts: bool = False) -> None:

  """

  Dissolve faces

  """

  ...

def dissolve_limited(angle_limit: float = 0.0872665, use_dissolve_boundaries: bool = False, delimit: typing.Set[str] = {'NORMAL'}) -> None:

  """

  Dissolve selected edges and vertices, limited by the angle of surrounding geometry

  """

  ...

def dissolve_mode(use_verts: bool = False, use_face_split: bool = False, use_boundary_tear: bool = False) -> None:

  """

  Dissolve geometry based on the selection mode

  """

  ...

def dissolve_verts(use_face_split: bool = False, use_boundary_tear: bool = False) -> None:

  """

  Dissolve vertices, merge edges and faces

  """

  ...

def dupli_extrude_cursor(rotate_source: bool = True) -> None:

  """

  Duplicate and extrude selected vertices, edges or faces towards the mouse cursor

  """

  ...

def duplicate(mode: int = 1) -> None:

  """

  Duplicate selected vertices, edges or faces

  """

  ...

def duplicate_move(MESH_OT_duplicate: MESH_OT_duplicate = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Duplicate mesh and move

  """

  ...

def edge_collapse() -> None:

  """

  Collapse isolated edge and face regions, merging data such as UV's and vertex colors. This can collapse edge-rings as well as regions of connected faces into vertices

  """

  ...

def edge_face_add() -> None:

  """

  Add an edge or face to selected

  """

  ...

def edge_rotate(use_ccw: bool = False) -> None:

  """

  Rotate selected edge or adjoining faces

  """

  ...

def edge_split(type: str = 'EDGE') -> None:

  """

  Split selected edges so that each neighbor face gets its own copy

  """

  ...

def edgering_select(extend: bool = False, deselect: bool = False, toggle: bool = False, ring: bool = True) -> None:

  """

  Select an edge ring

  """

  ...

def edges_select_sharp(sharpness: float = 0.523599) -> None:

  """

  Select all sharp enough edges

  """

  ...

def extrude_context(use_normal_flip: bool = False, use_dissolve_ortho_edges: bool = False, mirror: bool = False) -> None:

  """

  Extrude selection

  """

  ...

def extrude_context_move(MESH_OT_extrude_context: MESH_OT_extrude_context = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Extrude region together along the average normal

  """

  ...

def extrude_edges_indiv(use_normal_flip: bool = False, mirror: bool = False) -> None:

  """

  Extrude individual edges only

  """

  ...

def extrude_edges_move(MESH_OT_extrude_edges_indiv: MESH_OT_extrude_edges_indiv = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Extrude edges and move result

  """

  ...

def extrude_faces_indiv(mirror: bool = False) -> None:

  """

  Extrude individual faces only

  """

  ...

def extrude_faces_move(MESH_OT_extrude_faces_indiv: MESH_OT_extrude_faces_indiv = None, TRANSFORM_OT_shrink_fatten: TRANSFORM_OT_shrink_fatten = None) -> None:

  """

  Extrude each individual face separately along local normals

  """

  ...

def extrude_manifold(MESH_OT_extrude_region: MESH_OT_extrude_region = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Extrude, dissolves edges whose faces form a flat surface and intersect new edges

  """

  ...

def extrude_region(use_normal_flip: bool = False, use_dissolve_ortho_edges: bool = False, mirror: bool = False) -> None:

  """

  Extrude region of faces

  """

  ...

def extrude_region_move(MESH_OT_extrude_region: MESH_OT_extrude_region = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Extrude region and move result

  """

  ...

def extrude_region_shrink_fatten(MESH_OT_extrude_region: MESH_OT_extrude_region = None, TRANSFORM_OT_shrink_fatten: TRANSFORM_OT_shrink_fatten = None) -> None:

  """

  Extrude region together along local normals

  """

  ...

def extrude_repeat(steps: int = 10, offset: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale_offset: float = 1.0) -> None:

  """

  Extrude selected vertices, edges or faces repeatedly

  """

  ...

def extrude_vertices_move(MESH_OT_extrude_verts_indiv: MESH_OT_extrude_verts_indiv = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Extrude vertices and move result

  """

  ...

def extrude_verts_indiv(mirror: bool = False) -> None:

  """

  Extrude individual vertices only

  """

  ...

def face_make_planar(factor: float = 1.0, repeat: int = 1) -> None:

  """

  Flatten selected faces

  """

  ...

def face_set_extract(add_boundary_loop: bool = True, smooth_iterations: int = 4, apply_shrinkwrap: bool = True, add_solidify: bool = True) -> None:

  """

  Create a new mesh object from the selected Face Set

  """

  ...

def face_split_by_edges() -> None:

  """

  Weld loose edges into faces (splitting them into new faces)

  """

  ...

def faces_mirror_uv(direction: str = 'POSITIVE', precision: int = 3) -> None:

  """

  Copy mirror UV coordinates on the X axis based on a mirrored mesh

  """

  ...

def faces_select_linked_flat(sharpness: float = 0.0174533) -> None:

  """

  Select linked faces by angle

  """

  ...

def faces_shade_flat() -> None:

  """

  Display faces flat

  """

  ...

def faces_shade_smooth() -> None:

  """

  Display faces smooth (using vertex normals)

  """

  ...

def fill(use_beauty: bool = True) -> None:

  """

  Fill a selected edge loop with faces

  """

  ...

def fill_grid(span: int = 1, offset: int = 0, use_interp_simple: bool = False) -> None:

  """

  Fill grid from two loops

  """

  ...

def fill_holes(sides: int = 4) -> None:

  """

  Fill in holes (boundary edge loops)

  """

  ...

def flip_normals(only_clnors: bool = False) -> None:

  """

  Flip the direction of selected faces' normals (and of their vertices)

  """

  ...

def hide(unselected: bool = False) -> None:

  """

  Hide (un)selected vertices, edges or faces

  """

  ...

def inset(use_boundary: bool = True, use_even_offset: bool = True, use_relative_offset: bool = False, use_edge_rail: bool = False, thickness: float = 0.0, depth: float = 0.0, use_outset: bool = False, use_select_inset: bool = False, use_individual: bool = False, use_interpolate: bool = True, release_confirm: bool = False) -> None:

  """

  Inset new faces into selected faces

  """

  ...

def intersect(mode: str = 'SELECT_UNSELECT', separate_mode: str = 'CUT', threshold: float = 1e-06, solver: str = 'EXACT') -> None:

  """

  Cut an intersection into faces

  """

  ...

def intersect_boolean(operation: str = 'DIFFERENCE', use_swap: bool = False, use_self: bool = False, threshold: float = 1e-06, solver: str = 'EXACT') -> None:

  """

  Cut solid geometry from selected to unselected

  """

  ...

def knife_project(cut_through: bool = False) -> None:

  """

  Use other objects outlines and boundaries to project knife cuts

  """

  ...

def knife_tool(use_occlude_geometry: bool = True, only_selected: bool = False, xray: bool = True, visible_measurements: str = 'NONE', angle_snapping: str = 'NONE', angle_snapping_increment: float = 0.523599, wait_for_input: bool = True) -> None:

  """

  Cut new topology

  """

  ...

def loop_multi_select(ring: bool = False) -> None:

  """

  Select a loop of connected edges by connection type

  """

  ...

def loop_select(extend: bool = False, deselect: bool = False, toggle: bool = False, ring: bool = False) -> None:

  """

  Select a loop of connected edges

  """

  ...

def loop_to_region(select_bigger: bool = False) -> None:

  """

  Select region of faces inside of a selected loop of edges

  """

  ...

def loopcut(number_cuts: int = 1, smoothness: float = 0.0, falloff: str = 'INVERSE_SQUARE', object_index: int = -1, edge_index: int = -1, mesh_select_mode_init: typing.Tuple[bool, bool, bool] = (False, False, False)) -> None:

  """

  Add a new loop between existing loops

  """

  ...

def loopcut_slide(MESH_OT_loopcut: MESH_OT_loopcut = None, TRANSFORM_OT_edge_slide: TRANSFORM_OT_edge_slide = None) -> None:

  """

  Cut mesh loop and slide it

  """

  ...

def mark_freestyle_edge(clear: bool = False) -> None:

  """

  (Un)mark selected edges as Freestyle feature edges

  """

  ...

def mark_freestyle_face(clear: bool = False) -> None:

  """

  (Un)mark selected faces for exclusion from Freestyle feature edge detection

  """

  ...

def mark_seam(clear: bool = False) -> None:

  """

  (Un)mark selected edges as a seam

  """

  ...

def mark_sharp(clear: bool = False, use_verts: bool = False) -> None:

  """

  (Un)mark selected edges as sharp

  """

  ...

def merge(type: str = 'CENTER', uvs: bool = False) -> None:

  """

  Merge selected vertices

  """

  ...

def merge_normals() -> None:

  """

  Merge custom normals of selected vertices

  """

  ...

def mod_weighted_strength(set: bool = False, face_strength: str = 'MEDIUM') -> None:

  """

  Set/Get strength of face (used in Weighted Normal modifier)

  """

  ...

def normals_make_consistent(inside: bool = False) -> None:

  """

  Make face and vertex normals point either outside or inside the mesh

  """

  ...

def normals_tools(mode: str = 'COPY', absolute: bool = False) -> None:

  """

  Custom normals tools using Normal Vector of UI

  """

  ...

def offset_edge_loops(use_cap_endpoint: bool = False) -> None:

  """

  Create offset edge loop from the current selection

  """

  ...

def offset_edge_loops_slide(MESH_OT_offset_edge_loops: MESH_OT_offset_edge_loops = None, TRANSFORM_OT_edge_slide: TRANSFORM_OT_edge_slide = None) -> None:

  """

  Offset edge loop slide

  """

  ...

def paint_mask_extract(mask_threshold: float = 0.5, add_boundary_loop: bool = True, smooth_iterations: int = 4, apply_shrinkwrap: bool = True, add_solidify: bool = True) -> None:

  """

  Create a new mesh object from the current paint mask

  """

  ...

def paint_mask_slice(mask_threshold: float = 0.5, fill_holes: bool = True, new_object: bool = True) -> None:

  """

  Slices the paint mask from the mesh

  """

  ...

def point_normals(mode: str = 'COORDINATES', invert: bool = False, align: bool = False, target_location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), spherize: bool = False, spherize_strength: float = 0.1) -> None:

  """

  Point selected custom normals to specified Target

  """

  ...

def poke(offset: float = 0.0, use_relative_offset: bool = False, center_mode: str = 'MEDIAN_WEIGHTED') -> None:

  """

  Split a face into a fan

  """

  ...

def polybuild_delete_at_cursor(mirror: bool = False, use_proportional_edit: bool = False, proportional_edit_falloff: str = 'SMOOTH', proportional_size: float = 1.0, use_proportional_connected: bool = False, use_proportional_projected: bool = False, release_confirm: bool = False, use_accurate: bool = False) -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def polybuild_dissolve_at_cursor() -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def polybuild_extrude_at_cursor_move(MESH_OT_polybuild_transform_at_cursor: MESH_OT_polybuild_transform_at_cursor = None, MESH_OT_extrude_edges_indiv: MESH_OT_extrude_edges_indiv = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def polybuild_face_at_cursor(create_quads: bool = True, mirror: bool = False, use_proportional_edit: bool = False, proportional_edit_falloff: str = 'SMOOTH', proportional_size: float = 1.0, use_proportional_connected: bool = False, use_proportional_projected: bool = False, release_confirm: bool = False, use_accurate: bool = False) -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def polybuild_face_at_cursor_move(MESH_OT_polybuild_face_at_cursor: MESH_OT_polybuild_face_at_cursor = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def polybuild_split_at_cursor(mirror: bool = False, use_proportional_edit: bool = False, proportional_edit_falloff: str = 'SMOOTH', proportional_size: float = 1.0, use_proportional_connected: bool = False, use_proportional_projected: bool = False, release_confirm: bool = False, use_accurate: bool = False) -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def polybuild_split_at_cursor_move(MESH_OT_polybuild_split_at_cursor: MESH_OT_polybuild_split_at_cursor = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def polybuild_transform_at_cursor(mirror: bool = False, use_proportional_edit: bool = False, proportional_edit_falloff: str = 'SMOOTH', proportional_size: float = 1.0, use_proportional_connected: bool = False, use_proportional_projected: bool = False, release_confirm: bool = False, use_accurate: bool = False) -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def polybuild_transform_at_cursor_move(MESH_OT_polybuild_transform_at_cursor: MESH_OT_polybuild_transform_at_cursor = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def primitive_circle_add(vertices: int = 32, radius: float = 1.0, fill_type: str = 'NOTHING', calc_uvs: bool = True, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a circle mesh

  """

  ...

def primitive_cone_add(vertices: int = 32, radius1: float = 1.0, radius2: float = 0.0, depth: float = 2.0, end_fill_type: str = 'NGON', calc_uvs: bool = True, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a conic mesh

  """

  ...

def primitive_cube_add(size: float = 2.0, calc_uvs: bool = True, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a cube mesh

  """

  ...

def primitive_cube_add_gizmo(calc_uvs: bool = True, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), matrix: typing.Tuple[typing.Tuple[float, float, float, float], typing.Tuple[float, float, float, float], typing.Tuple[float, float, float, float], typing.Tuple[float, float, float, float]] = ((0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0))) -> None:

  """

  Construct a cube mesh

  """

  ...

def primitive_cylinder_add(vertices: int = 32, radius: float = 1.0, depth: float = 2.0, end_fill_type: str = 'NGON', calc_uvs: bool = True, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a cylinder mesh

  """

  ...

def primitive_grid_add(x_subdivisions: int = 10, y_subdivisions: int = 10, size: float = 2.0, calc_uvs: bool = True, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a grid mesh

  """

  ...

def primitive_ico_sphere_add(subdivisions: int = 2, radius: float = 1.0, calc_uvs: bool = True, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct an Icosphere mesh

  """

  ...

def primitive_monkey_add(size: float = 2.0, calc_uvs: bool = True, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a Suzanne mesh

  """

  ...

def primitive_plane_add(size: float = 2.0, calc_uvs: bool = True, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a filled planar mesh with 4 vertices

  """

  ...

def primitive_torus_add(align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), major_segments: int = 48, minor_segments: int = 12, mode: str = 'MAJOR_MINOR', major_radius: float = 1.0, minor_radius: float = 0.25, abso_major_rad: float = 1.25, abso_minor_rad: float = 0.75, generate_uvs: bool = True) -> None:

  """

  Construct a torus mesh

  """

  ...

def primitive_uv_sphere_add(segments: int = 32, ring_count: int = 16, radius: float = 1.0, calc_uvs: bool = True, enter_editmode: bool = False, align: str = 'WORLD', location: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), rotation: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), scale: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Construct a UV sphere mesh

  """

  ...

def quads_convert_to_tris(quad_method: str = 'BEAUTY', ngon_method: str = 'BEAUTY') -> None:

  """

  Triangulate selected faces

  """

  ...

def region_to_loop() -> None:

  """

  Select boundary edges around the selected faces

  """

  ...

def remove_doubles(threshold: float = 0.0001, use_unselected: bool = False, use_sharp_edge_from_normals: bool = False) -> None:

  """

  Merge vertices based on their proximity

  """

  ...

def reveal(select: bool = True) -> None:

  """

  Reveal all hidden vertices, edges and faces

  """

  ...

def rip(mirror: bool = False, use_proportional_edit: bool = False, proportional_edit_falloff: str = 'SMOOTH', proportional_size: float = 1.0, use_proportional_connected: bool = False, use_proportional_projected: bool = False, release_confirm: bool = False, use_accurate: bool = False, use_fill: bool = False) -> None:

  """

  Disconnect vertex or edges from connected geometry

  """

  ...

def rip_edge(mirror: bool = False, use_proportional_edit: bool = False, proportional_edit_falloff: str = 'SMOOTH', proportional_size: float = 1.0, use_proportional_connected: bool = False, use_proportional_projected: bool = False, release_confirm: bool = False, use_accurate: bool = False) -> None:

  """

  Extend vertices along the edge closest to the cursor

  """

  ...

def rip_edge_move(MESH_OT_rip_edge: MESH_OT_rip_edge = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Extend vertices and move the result

  """

  ...

def rip_move(MESH_OT_rip: MESH_OT_rip = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Rip polygons and move the result

  """

  ...

def screw(steps: int = 9, turns: int = 1, center: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), axis: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Extrude selected vertices in screw-shaped rotation around the cursor in indicated viewport

  """

  ...

def sculpt_vertex_color_add() -> None:

  """

  Add vertex color layer

  """

  ...

def sculpt_vertex_color_remove() -> None:

  """

  Remove vertex color layer

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  (De)select all vertices, edges or faces

  """

  ...

def select_axis(orientation: str = 'LOCAL', sign: str = 'POS', axis: str = 'X', threshold: float = 0.0001) -> None:

  """

  Select all data in the mesh on a single axis

  """

  ...

def select_face_by_sides(number: int = 4, type: str = 'EQUAL', extend: bool = True) -> None:

  """

  Select vertices or faces by the number of polygon sides

  """

  ...

def select_interior_faces() -> None:

  """

  Select faces where all edges have more than 2 face users

  """

  ...

def select_less(use_face_step: bool = True) -> None:

  """

  Deselect vertices, edges or faces at the boundary of each selection region

  """

  ...

def select_linked(delimit: typing.Set[str] = {'SEAM'}) -> None:

  """

  Select all vertices connected to the current selection

  """

  ...

def select_linked_pick(deselect: bool = False, delimit: typing.Set[str] = {'SEAM'}, object_index: int = -1, index: int = -1) -> None:

  """

  (De)select all vertices linked to the edge under the mouse cursor

  """

  ...

def select_loose(extend: bool = False) -> None:

  """

  Select loose geometry based on the selection mode

  """

  ...

def select_mirror(axis: typing.Set[str] = {'X'}, extend: bool = False) -> None:

  """

  Select mesh items at mirrored locations

  """

  ...

def select_mode(use_extend: bool = False, use_expand: bool = False, type: str = 'VERT', action: str = 'TOGGLE') -> None:

  """

  Change selection mode

  """

  ...

def select_more(use_face_step: bool = True) -> None:

  """

  Select more vertices, edges or faces connected to initial selection

  """

  ...

def select_next_item() -> None:

  """

  Select the next element (using selection order)

  """

  ...

def select_non_manifold(extend: bool = True, use_wire: bool = True, use_boundary: bool = True, use_multi_face: bool = True, use_non_contiguous: bool = True, use_verts: bool = True) -> None:

  """

  Select all non-manifold vertices or edges

  """

  ...

def select_nth(skip: int = 1, nth: int = 1, offset: int = 0) -> None:

  """

  Deselect every Nth element starting from the active vertex, edge or face

  """

  ...

def select_prev_item() -> None:

  """

  Select the previous element (using selection order)

  """

  ...

def select_random(ratio: float = 0.5, seed: int = 0, action: str = 'SELECT') -> None:

  """

  Randomly select vertices

  """

  ...

def select_similar(type: str = 'NORMAL', compare: str = 'EQUAL', threshold: float = 0.0) -> None:

  """

  Select similar vertices, edges or faces by property types

  """

  ...

def select_similar_region() -> None:

  """

  Select similar face regions to the current selection

  """

  ...

def select_ungrouped(extend: bool = False) -> None:

  """

  Select vertices without a group

  """

  ...

def separate(type: str = 'SELECTED') -> None:

  """

  Separate selected geometry into a new mesh

  """

  ...

def set_normals_from_faces(keep_sharp: bool = False) -> None:

  """

  Set the custom normals from the selected faces ones

  """

  ...

def shape_propagate_to_all() -> None:

  """

  Apply selected vertex locations to all other shape keys

  """

  ...

def shortest_path_pick(edge_mode: str = 'SELECT', use_face_step: bool = False, use_topology_distance: bool = False, use_fill: bool = False, skip: int = 0, nth: int = 1, offset: int = 0, index: int = -1) -> None:

  """

  Select shortest path between two selections

  """

  ...

def shortest_path_select(edge_mode: str = 'SELECT', use_face_step: bool = False, use_topology_distance: bool = False, use_fill: bool = False, skip: int = 0, nth: int = 1, offset: int = 0) -> None:

  """

  Selected shortest path between two vertices/edges/faces

  """

  ...

def smooth_normals(factor: float = 0.5) -> None:

  """

  Smooth custom normals based on adjacent vertex normals

  """

  ...

def solidify(thickness: float = 0.01) -> None:

  """

  Create a solid skin by extruding, compensating for sharp angles

  """

  ...

def sort_elements(type: str = 'VIEW_ZAXIS', elements: typing.Set[str] = {'VERT'}, reverse: bool = False, seed: int = 0) -> None:

  """

  The order of selected vertices/edges/faces is modified, based on a given method

  """

  ...

def spin(steps: int = 12, dupli: bool = False, angle: float = 1.5708, use_auto_merge: bool = True, use_normal_flip: bool = False, center: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), axis: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:

  """

  Extrude selected vertices in a circle around the cursor in indicated viewport

  """

  ...

def split() -> None:

  """

  Split off selected geometry from connected unselected geometry

  """

  ...

def split_normals() -> None:

  """

  Split custom normals of selected vertices

  """

  ...

def subdivide(number_cuts: int = 1, smoothness: float = 0.0, ngon: bool = True, quadcorner: str = 'STRAIGHT_CUT', fractal: float = 0.0, fractal_along_normal: float = 0.0, seed: int = 0) -> None:

  """

  Subdivide selected edges

  """

  ...

def subdivide_edgering(number_cuts: int = 10, interpolation: str = 'PATH', smoothness: float = 1.0, profile_shape_factor: float = 0.0, profile_shape: str = 'SMOOTH') -> None:

  """

  Subdivide perpendicular edges to the selected edge-ring

  """

  ...

def symmetrize(direction: str = 'NEGATIVE_X', threshold: float = 0.0001) -> None:

  """

  Enforce symmetry (both form and topological) across an axis

  """

  ...

def symmetry_snap(direction: str = 'NEGATIVE_X', threshold: float = 0.05, factor: float = 0.5, use_center: bool = True) -> None:

  """

  Snap vertex pairs to their mirrored locations

  """

  ...

def tris_convert_to_quads(face_threshold: float = 0.698132, shape_threshold: float = 0.698132, uvs: bool = False, vcols: bool = False, seam: bool = False, sharp: bool = False, materials: bool = False) -> None:

  """

  Join triangles into quads

  """

  ...

def unsubdivide(iterations: int = 2) -> None:

  """

  Un-subdivide selected edges and faces

  """

  ...

def uv_texture_add() -> None:

  """

  Add UV map

  """

  ...

def uv_texture_remove() -> None:

  """

  Remove UV map

  """

  ...

def uvs_reverse() -> None:

  """

  Flip direction of UV coordinates inside faces

  """

  ...

def uvs_rotate(use_ccw: bool = False) -> None:

  """

  Rotate UV coordinates inside faces

  """

  ...

def vert_connect() -> None:

  """

  Connect selected vertices of faces, splitting the face

  """

  ...

def vert_connect_concave() -> None:

  """

  Make all faces convex

  """

  ...

def vert_connect_nonplanar(angle_limit: float = 0.0872665) -> None:

  """

  Split non-planar faces that exceed the angle threshold

  """

  ...

def vert_connect_path() -> None:

  """

  Connect vertices by their selection order, creating edges, splitting faces

  """

  ...

def vertex_color_add() -> None:

  """

  Add vertex color layer

  """

  ...

def vertex_color_remove() -> None:

  """

  Remove vertex color layer

  """

  ...

def vertices_smooth(factor: float = 0.0, repeat: int = 1, xaxis: bool = True, yaxis: bool = True, zaxis: bool = True, wait_for_input: bool = True) -> None:

  """

  Flatten angles of selected vertices

  """

  ...

def vertices_smooth_laplacian(repeat: int = 1, lambda_factor: float = 1.0, lambda_border: float = 5e-05, use_x: bool = True, use_y: bool = True, use_z: bool = True, preserve_volume: bool = True) -> None:

  """

  Laplacian smooth of selected vertices

  """

  ...

def wireframe(use_boundary: bool = True, use_even_offset: bool = True, use_relative_offset: bool = False, use_replace: bool = True, thickness: float = 0.01, offset: float = 0.01, use_crease: bool = False, crease_weight: float = 0.01) -> None:

  """

  Create a solid wireframe from faces

  """

  ...
