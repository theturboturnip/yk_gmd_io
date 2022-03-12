"""


Image Operators
***************

:func:`add_render_slot`

:func:`change_frame`

:func:`clear_render_border`

:func:`clear_render_slot`

:func:`curves_point_set`

:func:`cycle_render_slot`

:func:`external_edit`

:func:`flip`

:func:`invert`

:func:`match_movie_length`

:func:`new`

:func:`open`

:func:`pack`

:func:`project_apply`

:func:`project_edit`

:func:`read_viewlayers`

:func:`reload`

:func:`remove_render_slot`

:func:`render_border`

:func:`replace`

:func:`resize`

:func:`sample`

:func:`sample_line`

:func:`save`

:func:`save_all_modified`

:func:`save_as`

:func:`save_sequence`

:func:`tile_add`

:func:`tile_fill`

:func:`tile_remove`

:func:`unpack`

:func:`view_all`

:func:`view_center_cursor`

:func:`view_cursor_center`

:func:`view_ndof`

:func:`view_pan`

:func:`view_selected`

:func:`view_zoom`

:func:`view_zoom_border`

:func:`view_zoom_in`

:func:`view_zoom_out`

:func:`view_zoom_ratio`

"""

import typing

def add_render_slot() -> None:

  """

  Add a new render slot

  """

  ...

def change_frame(frame: int = 0) -> None:

  """

  Interactively change the current frame number

  """

  ...

def clear_render_border() -> None:

  """

  Clear the boundaries of the render region and disable render region

  """

  ...

def clear_render_slot() -> None:

  """

  Clear the currently selected render slot

  """

  ...

def curves_point_set(point: str = 'BLACK_POINT', size: int = 1) -> None:

  """

  Set black point or white point for curves

  """

  ...

def cycle_render_slot(reverse: bool = False) -> None:

  """

  Cycle through all non-void render slots

  """

  ...

def external_edit(filepath: str = '') -> None:

  """

  Edit image in an external application

  """

  ...

def flip(use_flip_x: bool = False, use_flip_y: bool = False) -> None:

  """

  Flip the image

  """

  ...

def invert(invert_r: bool = False, invert_g: bool = False, invert_b: bool = False, invert_a: bool = False) -> None:

  """

  Invert image's channels

  """

  ...

def match_movie_length() -> None:

  """

  Set image's user's length to the one of this video

  """

  ...

def new(name: str = 'Untitled', width: int = 1024, height: int = 1024, color: typing.Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0), alpha: bool = True, generated_type: str = 'BLANK', float: bool = False, use_stereo_3d: bool = False, tiled: bool = False) -> None:

  """

  Create a new image

  """

  ...

def open(filepath: str = '', directory: str = '', files: typing.Union[typing.Sequence[OperatorFileListElement], typing.Mapping[str, OperatorFileListElement], bpy.types.bpy_prop_collection] = None, hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = True, filter_movie: bool = True, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '', use_sequence_detection: bool = True, use_udim_detecting: bool = True) -> None:

  """

  Open image

  """

  ...

def pack() -> None:

  """

  Pack an image as embedded data into the .blend file

  """

  ...

def project_apply() -> None:

  """

  Project edited image back onto the object

  """

  ...

def project_edit() -> None:

  """

  Edit a snapshot of the 3D Viewport in an external image editor

  """

  ...

def read_viewlayers() -> None:

  """

  Read all the current scene's view layers from cache, as needed

  """

  ...

def reload() -> None:

  """

  Reload current image from disk

  """

  ...

def remove_render_slot() -> None:

  """

  Remove the current render slot

  """

  ...

def render_border(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True) -> None:

  """

  Set the boundaries of the render region and enable render region

  """

  ...

def replace(filepath: str = '', hide_props_region: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = True, filter_movie: bool = True, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Replace current image by another one from disk

  """

  ...

def resize(size: typing.Tuple[int, int] = (0, 0)) -> None:

  """

  Resize the image

  """

  ...

def sample(size: int = 1) -> None:

  """

  Use mouse to sample a color in current image

  """

  ...

def sample_line(xstart: int = 0, xend: int = 0, ystart: int = 0, yend: int = 0, flip: bool = False, cursor: int = 5) -> None:

  """

  Sample a line and show it in Scope panels

  """

  ...

def save() -> None:

  """

  Save the image with current name and settings

  """

  ...

def save_all_modified() -> None:

  """

  Save all modified images

  """

  ...

def save_as(save_as_render: bool = False, copy: bool = False, filepath: str = '', check_existing: bool = True, filter_blender: bool = False, filter_backup: bool = False, filter_image: bool = True, filter_movie: bool = True, filter_python: bool = False, filter_font: bool = False, filter_sound: bool = False, filter_text: bool = False, filter_archive: bool = False, filter_btx: bool = False, filter_collada: bool = False, filter_alembic: bool = False, filter_usd: bool = False, filter_volume: bool = False, filter_folder: bool = True, filter_blenlib: bool = False, filemode: int = 9, relative_path: bool = True, show_multiview: bool = False, use_multiview: bool = False, display_type: str = 'DEFAULT', sort_method: str = '') -> None:

  """

  Save the image with another name and/or settings

  """

  ...

def save_sequence() -> None:

  """

  Save a sequence of images

  """

  ...

def tile_add(number: int = 1002, count: int = 1, label: str = '', fill: bool = True, color: typing.Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0), generated_type: str = 'BLANK', width: int = 1024, height: int = 1024, float: bool = False, alpha: bool = True) -> None:

  """

  Adds a tile to the image

  """

  ...

def tile_fill(color: typing.Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0), generated_type: str = 'BLANK', width: int = 1024, height: int = 1024, float: bool = False, alpha: bool = True) -> None:

  """

  Fill the current tile with a generated image

  """

  ...

def tile_remove() -> None:

  """

  Removes a tile from the image

  """

  ...

def unpack(method: str = 'USE_LOCAL', id: str = '') -> None:

  """

  Save an image packed in the .blend file to disk

  """

  ...

def view_all(fit_view: bool = False) -> None:

  """

  View the entire image

  """

  ...

def view_center_cursor() -> None:

  """

  Center the view so that the cursor is in the middle of the view

  """

  ...

def view_cursor_center(fit_view: bool = False) -> None:

  """

  Set 2D Cursor To Center View location

  """

  ...

def view_ndof() -> None:

  """

  Use a 3D mouse device to pan/zoom the view

  """

  ...

def view_pan(offset: typing.Tuple[float, float] = (0.0, 0.0)) -> None:

  """

  Pan the view

  """

  ...

def view_selected() -> None:

  """

  View all selected UVs

  """

  ...

def view_zoom(factor: float = 0.0, use_cursor_init: bool = True) -> None:

  """

  Zoom in/out the image

  """

  ...

def view_zoom_border(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, zoom_out: bool = False) -> None:

  """

  Zoom in the view to the nearest item contained in the border

  """

  ...

def view_zoom_in(location: typing.Tuple[float, float] = (0.0, 0.0)) -> None:

  """

  Zoom in the image (centered around 2D cursor)

  """

  ...

def view_zoom_out(location: typing.Tuple[float, float] = (0.0, 0.0)) -> None:

  """

  Zoom out the image (centered around 2D cursor)

  """

  ...

def view_zoom_ratio(ratio: float = 0.0) -> None:

  """

  Set zoom ratio of the view

  """

  ...
