"""


Paint Operators
***************

:func:`add_simple_uvs`

:func:`add_texture_paint_slot`

:func:`brush_colors_flip`

:func:`brush_select`

:func:`face_select_all`

:func:`face_select_hide`

:func:`face_select_linked`

:func:`face_select_linked_pick`

:func:`face_select_reveal`

:func:`grab_clone`

:func:`hide_show`

:func:`image_from_view`

:func:`image_paint`

:func:`mask_box_gesture`

:func:`mask_flood_fill`

:func:`mask_lasso_gesture`

:func:`mask_line_gesture`

:func:`project_image`

:func:`sample_color`

:func:`texture_paint_toggle`

:func:`vert_select_all`

:func:`vert_select_ungrouped`

:func:`vertex_color_brightness_contrast`

:func:`vertex_color_dirt`

:func:`vertex_color_from_weight`

:func:`vertex_color_hsv`

:func:`vertex_color_invert`

:func:`vertex_color_levels`

:func:`vertex_color_set`

:func:`vertex_color_smooth`

:func:`vertex_paint`

:func:`vertex_paint_toggle`

:func:`weight_from_bones`

:func:`weight_gradient`

:func:`weight_paint`

:func:`weight_paint_toggle`

:func:`weight_sample`

:func:`weight_sample_group`

:func:`weight_set`

"""

import typing

def add_simple_uvs() -> None:

  """

  Add cube map uvs on mesh

  """

  ...

def add_texture_paint_slot(type: str = 'BASE_COLOR', name: str = 'Untitled', width: int = 1024, height: int = 1024, color: typing.Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0), alpha: bool = True, generated_type: str = 'BLANK', float: bool = False) -> None:

  """

  Add a texture paint slot

  """

  ...

def brush_colors_flip() -> None:

  """

  Swap primary and secondary brush colors

  """

  ...

def brush_select(sculpt_tool: str = 'DRAW', vertex_tool: str = 'DRAW', weight_tool: str = 'DRAW', image_tool: str = 'DRAW', gpencil_tool: str = 'DRAW', gpencil_vertex_tool: str = 'DRAW', gpencil_sculpt_tool: str = 'SMOOTH', gpencil_weight_tool: str = 'WEIGHT', toggle: bool = False, create_missing: bool = False) -> None:

  """

  Select a paint mode's brush by tool type

  """

  ...

def face_select_all(action: str = 'TOGGLE') -> None:

  """

  Change selection for all faces

  """

  ...

def face_select_hide(unselected: bool = False) -> None:

  """

  Hide selected faces

  """

  ...

def face_select_linked() -> None:

  """

  Select linked faces

  """

  ...

def face_select_linked_pick(deselect: bool = False) -> None:

  """

  Select linked faces under the cursor

  """

  ...

def face_select_reveal(select: bool = True) -> None:

  """

  Reveal hidden faces

  """

  ...

def grab_clone(delta: typing.Tuple[float, float] = (0.0, 0.0)) -> None:

  """

  Move the clone source image

  """

  ...

def hide_show(action: str = 'HIDE', area: str = 'INSIDE', xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True) -> None:

  """

  Hide/show some vertices

  """

  ...

def image_from_view(filepath: str = '') -> None:

  """

  Make an image from biggest 3D view for reprojection

  """

  ...

def image_paint(stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, mode: str = 'NORMAL') -> None:

  """

  Paint a stroke into the image

  """

  ...

def mask_box_gesture(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, use_front_faces_only: bool = False, use_limit_to_segment: bool = False, mode: str = 'VALUE', value: float = 1.0) -> None:

  """

  Add mask within the box as you move the brush

  """

  ...

def mask_flood_fill(mode: str = 'VALUE', value: float = 0.0) -> None:

  """

  Fill the whole mask with a given value, or invert its values

  """

  ...

def mask_lasso_gesture(path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None, use_front_faces_only: bool = False, use_limit_to_segment: bool = False, mode: str = 'VALUE', value: float = 1.0) -> None:

  """

  Add mask within the lasso as you move the brush

  """

  ...

def mask_line_gesture(xstart: int = 0, xend: int = 0, ystart: int = 0, yend: int = 0, flip: bool = False, cursor: int = 5, use_front_faces_only: bool = False, use_limit_to_segment: bool = False, mode: str = 'VALUE', value: float = 1.0) -> None:

  """

  Add mask to the right of a line as you move the brush

  """

  ...

def project_image(image: str = '') -> None:

  """

  Project an edited render from the active camera back onto the object

  """

  ...

def sample_color(location: typing.Tuple[int, int] = (0, 0), merged: bool = False, palette: bool = False) -> None:

  """

  Use the mouse to sample a color in the image

  """

  ...

def texture_paint_toggle() -> None:

  """

  Toggle texture paint mode in 3D view

  """

  ...

def vert_select_all(action: str = 'TOGGLE') -> None:

  """

  Change selection for all vertices

  """

  ...

def vert_select_ungrouped(extend: bool = False) -> None:

  """

  Select vertices without a group

  """

  ...

def vertex_color_brightness_contrast(brightness: float = 0.0, contrast: float = 0.0) -> None:

  """

  Adjust vertex color brightness/contrast

  """

  ...

def vertex_color_dirt(blur_strength: float = 1.0, blur_iterations: int = 1, clean_angle: float = 3.14159, dirt_angle: float = 0.0, dirt_only: bool = False, normalize: bool = True) -> None:

  """

  Generate a dirt map gradient based on cavity

  """

  ...

def vertex_color_from_weight() -> None:

  """

  Convert active weight into gray scale vertex colors

  """

  ...

def vertex_color_hsv(h: float = 0.5, s: float = 1.0, v: float = 1.0) -> None:

  """

  Adjust vertex color HSV values

  """

  ...

def vertex_color_invert() -> None:

  """

  Invert RGB values

  """

  ...

def vertex_color_levels(offset: float = 0.0, gain: float = 1.0) -> None:

  """

  Adjust levels of vertex colors

  """

  ...

def vertex_color_set() -> None:

  """

  Fill the active vertex color layer with the current paint color

  """

  ...

def vertex_color_smooth() -> None:

  """

  Smooth colors across vertices

  """

  ...

def vertex_paint(stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, mode: str = 'NORMAL') -> None:

  """

  Paint a stroke in the active vertex color layer

  """

  ...

def vertex_paint_toggle() -> None:

  """

  Toggle the vertex paint mode in 3D view

  """

  ...

def weight_from_bones(type: str = 'AUTOMATIC') -> None:

  """

  Set the weights of the groups matching the attached armature's selected bones, using the distance between the vertices and the bones

  """

  ...

def weight_gradient(type: str = 'LINEAR', xstart: int = 0, xend: int = 0, ystart: int = 0, yend: int = 0, flip: bool = False, cursor: int = 5) -> None:

  """

  Draw a line to apply a weight gradient to selected vertices

  """

  ...

def weight_paint(stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, mode: str = 'NORMAL') -> None:

  """

  Paint a stroke in the current vertex group's weights

  """

  ...

def weight_paint_toggle() -> None:

  """

  Toggle weight paint mode in 3D view

  """

  ...

def weight_sample() -> None:

  """

  Use the mouse to sample a weight in the 3D view

  """

  ...

def weight_sample_group(group: str = 'DEFAULT') -> None:

  """

  Select one of the vertex groups available under current mouse position

  """

  ...

def weight_set() -> None:

  """

  Fill the active vertex group with the current paint weight

  """

  ...
