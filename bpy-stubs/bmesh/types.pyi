"""


BMesh Types (bmesh.types)
*************************


Base Mesh Type
==============

:class:`BMesh`


Mesh Elements
=============

:class:`BMVert`

:class:`BMEdge`

:class:`BMFace`

:class:`BMLoop`


Sequence Accessors
==================

:class:`BMElemSeq`

:class:`BMVertSeq`

:class:`BMEdgeSeq`

:class:`BMFaceSeq`

:class:`BMLoopSeq`

:class:`BMIter`


Selection History
=================

:class:`BMEditSelSeq`

:class:`BMEditSelIter`


Custom-Data Layer Access
========================

:class:`BMLayerAccessVert`

:class:`BMLayerAccessEdge`

:class:`BMLayerAccessFace`

:class:`BMLayerAccessLoop`

:class:`BMLayerCollection`

:class:`BMLayerItem`


Custom-Data Layer Types
=======================

:class:`BMLoopUV`

:class:`BMDeformVert`

"""

import typing

import mathutils

class BMesh:

  """

  The BMesh data structure

  """

  def calc_loop_triangles(self) -> typing.List[typing.Tuple[BMLoop, ...]]:

    """

    Calculate triangle tessellation from quads/ngons.

    """

    ...

  def calc_volume(self, signed: bool = False) -> float:

    """

    Calculate mesh volume based on face normals.

    """

    ...

  def clear(self) -> None:

    """

    Clear all mesh data.

    """

    ...

  def copy(self) -> BMesh:

    ...

  def free(self) -> None:

    """

    Explicitly free the BMesh data from memory, causing exceptions on further access.

    Note: The BMesh is freed automatically, typically when the script finishes executing.
However in some cases its hard to predict when this will be and its useful to
explicitly free the data.

    """

    ...

  def from_mesh(self, mesh: Mesh, face_normals: typing.Any = True, use_shape_key: bool = False, shape_key_index: int = 0) -> None:

    """

    Initialize this bmesh from existing mesh datablock.

    Note: Multiple calls can be used to join multiple meshes.Custom-data layers are only copied from ``mesh`` on initialization.
Further calls will copy custom-data to matching layers, layers missing on the target mesh won't be added.

    """

    ...

  def from_object(self, object: Object, depsgraph: typing.Any, cage: bool = False, face_normals: bool = True) -> None:

    """

    Initialize this bmesh from existing object data-block (only meshes are currently supported).

    """

    ...

  def normal_update(self) -> None:

    """

    Update mesh normals.

    """

    ...

  def select_flush(self, select: bool) -> None:

    """

    Flush selection, independent of the current selection mode.

    """

    ...

  def select_flush_mode(self) -> None:

    """

    flush selection based on the current mode current :class:`BMesh.select_mode`.

    """

    ...

  def to_mesh(self, mesh: Mesh) -> None:

    """

    Writes this BMesh data into an existing Mesh datablock.

    """

    ...

  def transform(self, matrix: typing.Any, filter: typing.Set[typing.Any] = None) -> None:

    """

    Transform the mesh (optionally filtering flagged data only).

    """

    ...

  edges: BMEdgeSeq = ...

  """

  This meshes edge sequence (read-only).

  """

  faces: BMFaceSeq = ...

  """

  This meshes face sequence (read-only).

  """

  is_valid: bool = ...

  """

  True when this element is valid (hasn't been removed).

  """

  is_wrapped: bool = ...

  """

  True when this mesh is owned by blender (typically the editmode BMesh).

  """

  loops: BMLoopSeq = ...

  """

  This meshes loops (read-only).

  Note: Loops must be accessed via faces, this is only exposed for layer access.

  """

  select_history: BMEditSelSeq = ...

  """

  Sequence of selected items (the last is displayed as active).

  """

  select_mode: typing.Set[typing.Any] = ...

  """

  The selection mode, values can be {'VERT', 'EDGE', 'FACE'}, can't be assigned an empty set.

  """

  verts: BMVertSeq = ...

  """

  This meshes vert sequence (read-only).

  """

class BMVert:

  """

  The BMesh vertex type

  """

  def calc_edge_angle(self, fallback: typing.Any = None) -> float:

    """

    Return the angle between this vert's two connected edges.

    """

    ...

  def calc_shell_factor(self) -> float:

    """

    Return a multiplier calculated based on the sharpness of the vertex.
Where a flat surface gives 1.0, and higher values sharper edges.
This is used to maintain shell thickness when offsetting verts along their normals.

    """

    ...

  def copy_from(self, other: typing.Any) -> None:

    """

    Copy values from another element of matching type.

    """

    ...

  def copy_from_face_interp(self, face: BMFace) -> None:

    """

    Interpolate the customdata from a face onto this loop (the loops vert should overlap the face).

    """

    ...

  def copy_from_vert_interp(self, vert_pair: BMVert, fac: typing.Any) -> None:

    """

    Interpolate the customdata from a vert between 2 other verts.

    """

    ...

  def hide_set(self, hide: bool) -> None:

    """

    Set the hide state.
This is different from the *hide* attribute because it updates the selection and hide state of associated geometry.

    """

    ...

  def normal_update(self) -> None:

    """

    Update vertex normal.

    """

    ...

  def select_set(self, select: bool) -> None:

    """

    Set the selection.
This is different from the *select* attribute because it updates the selection state of associated geometry.

    Note: Currently this only flushes down, so selecting a face will select all its vertices but de-selecting a vertex       won't de-select all the faces that use it, before finishing with a mesh typically flushing is still needed.

    """

    ...

  co: mathutils.Vector = ...

  """

  The coordinates for this vertex as a 3D, wrapped vector.

  """

  hide: bool = ...

  """

  Hidden state of this element.

  """

  index: int = ...

  """

  Index of this element.

  Note: This value is not necessarily valid, while editing the mesh it can become *dirty*.It's also possible to assign any number to this attribute for a scripts internal logic.To ensure the value is up to date - see :class:`BMElemSeq.index_update`.

  """

  is_boundary: bool = ...

  """

  True when this vertex is connected to boundary edges (read-only).

  """

  is_manifold: bool = ...

  """

  True when this vertex is manifold (read-only).

  """

  is_valid: bool = ...

  """

  True when this element is valid (hasn't been removed).

  """

  is_wire: bool = ...

  """

  True when this vertex is not connected to any faces (read-only).

  """

  link_edges: BMElemSeq = ...

  """

  Edges connected to this vertex (read-only).

  """

  link_faces: BMElemSeq = ...

  """

  Faces connected to this vertex (read-only).

  """

  link_loops: BMElemSeq = ...

  """

  Loops that use this vertex (read-only).

  """

  normal: mathutils.Vector = ...

  """

  The normal for this vertex as a 3D, wrapped vector.

  """

  select: bool = ...

  """

  Selected state of this element.

  """

  tag: bool = ...

  """

  Generic attribute scripts can use for own logic

  """

class BMEdge:

  """

  The BMesh edge connecting 2 verts

  """

  def calc_face_angle(self, fallback: typing.Any = None) -> float:

    ...

  def calc_face_angle_signed(self, fallback: typing.Any = None) -> float:

    ...

  def calc_length(self) -> float:

    ...

  def calc_tangent(self, loop: BMLoop) -> mathutils.Vector:

    """

    Return the tangent at this edge relative to a face (pointing inward into the face).
This uses the face normal for calculation.

    """

    ...

  def copy_from(self, other: typing.Any) -> None:

    """

    Copy values from another element of matching type.

    """

    ...

  def hide_set(self, hide: bool) -> None:

    """

    Set the hide state.
This is different from the *hide* attribute because it updates the selection and hide state of associated geometry.

    """

    ...

  def normal_update(self) -> None:

    """

    Update edges vertex normals.

    """

    ...

  def other_vert(self, vert: BMVert) -> BMVert:

    """

    Return the other vertex on this edge or None if the vertex is not used by this edge.

    """

    ...

  def select_set(self, select: bool) -> None:

    """

    Set the selection.
This is different from the *select* attribute because it updates the selection state of associated geometry.

    Note: Currently this only flushes down, so selecting a face will select all its vertices but de-selecting a vertex       won't de-select all the faces that use it, before finishing with a mesh typically flushing is still needed.

    """

    ...

  hide: bool = ...

  """

  Hidden state of this element.

  """

  index: int = ...

  """

  Index of this element.

  Note: This value is not necessarily valid, while editing the mesh it can become *dirty*.It's also possible to assign any number to this attribute for a scripts internal logic.To ensure the value is up to date - see :class:`BMElemSeq.index_update`.

  """

  is_boundary: bool = ...

  """

  True when this edge is at the boundary of a face (read-only).

  """

  is_contiguous: bool = ...

  """

  True when this edge is manifold, between two faces with the same winding (read-only).

  """

  is_convex: bool = ...

  """

  True when this edge joins two convex faces, depends on a valid face normal (read-only).

  """

  is_manifold: bool = ...

  """

  True when this edge is manifold (read-only).

  """

  is_valid: bool = ...

  """

  True when this element is valid (hasn't been removed).

  """

  is_wire: bool = ...

  """

  True when this edge is not connected to any faces (read-only).

  """

  link_faces: BMElemSeq = ...

  """

  Faces connected to this edge, (read-only).

  """

  link_loops: BMElemSeq = ...

  """

  Loops connected to this edge, (read-only).

  """

  seam: bool = ...

  """

  Seam for UV unwrapping.

  """

  select: bool = ...

  """

  Selected state of this element.

  """

  smooth: bool = ...

  """

  Smooth state of this element.

  """

  tag: bool = ...

  """

  Generic attribute scripts can use for own logic

  """

  verts: BMElemSeq = ...

  """

  Verts this edge uses (always 2), (read-only).

  """

class BMFace:

  """

  The BMesh face with 3 or more sides

  """

  def calc_area(self) -> float:

    """

    Return the area of the face.

    """

    ...

  def calc_center_bounds(self) -> mathutils.Vector:

    """

    Return bounds center of the face.

    """

    ...

  def calc_center_median(self) -> mathutils.Vector:

    """

    Return median center of the face.

    """

    ...

  def calc_center_median_weighted(self) -> mathutils.Vector:

    """

    Return median center of the face weighted by edge lengths.

    """

    ...

  def calc_perimeter(self) -> float:

    """

    Return the perimeter of the face.

    """

    ...

  def calc_tangent_edge(self) -> mathutils.Vector:

    """

    Return face tangent based on longest edge.

    """

    ...

  def calc_tangent_edge_diagonal(self) -> mathutils.Vector:

    """

    Return face tangent based on the edge farthest from any vertex.

    """

    ...

  def calc_tangent_edge_pair(self) -> mathutils.Vector:

    """

    Return face tangent based on the two longest disconnected edges.

    * Tris: Use the edge pair with the most similar lengths.

    * Quads: Use the longest edge pair.

    * NGons: Use the two longest disconnected edges.

    """

    ...

  def calc_tangent_vert_diagonal(self) -> mathutils.Vector:

    """

    Return face tangent based on the two most distant vertices.

    """

    ...

  def copy(self, verts: bool = True, edges: bool = True) -> BMFace:

    """

    Make a copy of this face.

    """

    ...

  def copy_from(self, other: typing.Any) -> None:

    """

    Copy values from another element of matching type.

    """

    ...

  def copy_from_face_interp(self, face: BMFace, vert: bool = True) -> None:

    """

    Interpolate the customdata from another face onto this one (faces should overlap).

    """

    ...

  def hide_set(self, hide: bool) -> None:

    """

    Set the hide state.
This is different from the *hide* attribute because it updates the selection and hide state of associated geometry.

    """

    ...

  def normal_flip(self) -> None:

    """

    Reverses winding of a face, which flips its normal.

    """

    ...

  def normal_update(self) -> None:

    """

    Update face's normal.

    """

    ...

  def select_set(self, select: bool) -> None:

    """

    Set the selection.
This is different from the *select* attribute because it updates the selection state of associated geometry.

    Note: Currently this only flushes down, so selecting a face will select all its vertices but de-selecting a vertex       won't de-select all the faces that use it, before finishing with a mesh typically flushing is still needed.

    """

    ...

  edges: BMElemSeq = ...

  """

  Edges of this face, (read-only).

  """

  hide: bool = ...

  """

  Hidden state of this element.

  """

  index: int = ...

  """

  Index of this element.

  Note: This value is not necessarily valid, while editing the mesh it can become *dirty*.It's also possible to assign any number to this attribute for a scripts internal logic.To ensure the value is up to date - see :class:`BMElemSeq.index_update`.

  """

  is_valid: bool = ...

  """

  True when this element is valid (hasn't been removed).

  """

  loops: BMElemSeq = ...

  """

  Loops of this face, (read-only).

  """

  material_index: int = ...

  """

  The face's material index.

  """

  normal: mathutils.Vector = ...

  """

  The normal for this face as a 3D, wrapped vector.

  """

  select: bool = ...

  """

  Selected state of this element.

  """

  smooth: bool = ...

  """

  Smooth state of this element.

  """

  tag: bool = ...

  """

  Generic attribute scripts can use for own logic

  """

  verts: BMElemSeq = ...

  """

  Verts of this face, (read-only).

  """

class BMLoop:

  """

  This is normally accessed from :class:`BMFace.loops` where each face loop represents a corner of the face.

  """

  def calc_angle(self) -> float:

    """

    Return the angle at this loops corner of the face.
This is calculated so sharper corners give lower angles.

    """

    ...

  def calc_normal(self) -> mathutils.Vector:

    """

    Return normal at this loops corner of the face.
Falls back to the face normal for straight lines.

    """

    ...

  def calc_tangent(self) -> mathutils.Vector:

    """

    Return the tangent at this loops corner of the face (pointing inward into the face).
Falls back to the face normal for straight lines.

    """

    ...

  def copy_from(self, other: typing.Any) -> None:

    """

    Copy values from another element of matching type.

    """

    ...

  def copy_from_face_interp(self, face: BMFace, vert: bool = True, multires: bool = True) -> None:

    """

    Interpolate the customdata from a face onto this loop (the loops vert should overlap the face).

    """

    ...

  edge: BMEdge = ...

  """

  The loop's edge (between this loop and the next), (read-only).

  """

  face: BMFace = ...

  """

  The face this loop makes (read-only).

  """

  index: int = ...

  """

  Index of this element.

  Note: This value is not necessarily valid, while editing the mesh it can become *dirty*.It's also possible to assign any number to this attribute for a scripts internal logic.To ensure the value is up to date - see :class:`BMElemSeq.index_update`.

  """

  is_convex: bool = ...

  """

  True when this loop is at the convex corner of a face, depends on a valid face normal (read-only).

  """

  is_valid: bool = ...

  """

  True when this element is valid (hasn't been removed).

  """

  link_loop_next: BMLoop = ...

  """

  The next face corner (read-only).

  """

  link_loop_prev: BMLoop = ...

  """

  The previous face corner (read-only).

  """

  link_loop_radial_next: BMLoop = ...

  """

  The next loop around the edge (read-only).

  """

  link_loop_radial_prev: BMLoop = ...

  """

  The previous loop around the edge (read-only).

  """

  link_loops: BMElemSeq = ...

  """

  Loops connected to this loop, (read-only).

  """

  tag: bool = ...

  """

  Generic attribute scripts can use for own logic

  """

  vert: BMVert = ...

  """

  The loop's vertex (read-only).

  """

class BMElemSeq:

  """

  General sequence type used for accessing any sequence of
:class:`BMVert`, :class:`BMEdge`, :class:`BMFace`, :class:`BMLoop`.

  When accessed via :class:`BMesh.verts`, :class:`BMesh.edges`, :class:`BMesh.faces`
there are also functions to create/remove items.

  """

  def index_update(self) -> None:

    """

    Initialize the index values of this sequence.

    This is the equivalent of looping over all elements and assigning the index values.

    .. code:: python

      for index, ele in enumerate(sequence):
          ele.index = index

    Note: Running this on sequences besides :class:`BMesh.verts`, :class:`BMesh.edges`, :class:`BMesh.faces`
works but won't result in each element having a valid index, instead its order in the sequence will be set.

    """

    ...

class BMVertSeq:

  def ensure_lookup_table(self) -> None:

    """

    Ensure internal data needed for int subscription is initialized with verts/edges/faces, eg ``bm.verts[index]``.

    This needs to be called again after adding/removing data in this sequence.

    """

    ...

  def index_update(self) -> None:

    """

    Initialize the index values of this sequence.

    This is the equivalent of looping over all elements and assigning the index values.

    .. code:: python

      for index, ele in enumerate(sequence):
          ele.index = index

    Note: Running this on sequences besides :class:`BMesh.verts`, :class:`BMesh.edges`, :class:`BMesh.faces`
works but won't result in each element having a valid index, instead its order in the sequence will be set.

    """

    ...

  def new(self, co: float = (0.0, 0.0, 0.0), example: BMVert = None) -> BMVert:

    """

    Create a new vertex.

    """

    ...

  def remove(self, vert: typing.Any) -> None:

    """

    Remove a vert.

    """

    ...

  def sort(self, key: typing.Callable = None, reverse: bool = False) -> None:

    """

    Sort the elements of this sequence, using an optional custom sort key.
Indices of elements are not changed, BMElemeSeq.index_update() can be used for that.

    Note: When the 'key' argument is not provided, the elements are reordered following their current index value.
In particular this can be used by setting indices manually before calling this method.

    Warning: Existing references to the N'th element, will continue to point the data at that index.

    """

    ...

  layers: BMLayerAccessVert = ...

  """

  custom-data layers (read-only).

  """

class BMEdgeSeq:

  def ensure_lookup_table(self) -> None:

    """

    Ensure internal data needed for int subscription is initialized with verts/edges/faces, eg ``bm.verts[index]``.

    This needs to be called again after adding/removing data in this sequence.

    """

    ...

  def get(self, verts: BMVert, fallback: typing.Any = None) -> BMEdge:

    """

    Return an edge which uses the **verts** passed.

    """

    ...

  def index_update(self) -> None:

    """

    Initialize the index values of this sequence.

    This is the equivalent of looping over all elements and assigning the index values.

    .. code:: python

      for index, ele in enumerate(sequence):
          ele.index = index

    Note: Running this on sequences besides :class:`BMesh.verts`, :class:`BMesh.edges`, :class:`BMesh.faces`
works but won't result in each element having a valid index, instead its order in the sequence will be set.

    """

    ...

  def new(self, verts: typing.Tuple[BMVert, BMVert], example: BMEdge = None) -> BMEdge:

    """

    Create a new edge from a given pair of verts.

    """

    ...

  def remove(self, edge: typing.Any) -> None:

    """

    Remove an edge.

    """

    ...

  def sort(self, key: typing.Callable = None, reverse: bool = False) -> None:

    """

    Sort the elements of this sequence, using an optional custom sort key.
Indices of elements are not changed, BMElemeSeq.index_update() can be used for that.

    Note: When the 'key' argument is not provided, the elements are reordered following their current index value.
In particular this can be used by setting indices manually before calling this method.

    Warning: Existing references to the N'th element, will continue to point the data at that index.

    """

    ...

  layers: BMLayerAccessEdge = ...

  """

  custom-data layers (read-only).

  """

class BMFaceSeq:

  def ensure_lookup_table(self) -> None:

    """

    Ensure internal data needed for int subscription is initialized with verts/edges/faces, eg ``bm.verts[index]``.

    This needs to be called again after adding/removing data in this sequence.

    """

    ...

  def get(self, verts: BMVert, fallback: typing.Any = None) -> BMFace:

    """

    Return a face which uses the **verts** passed.

    """

    ...

  def index_update(self) -> None:

    """

    Initialize the index values of this sequence.

    This is the equivalent of looping over all elements and assigning the index values.

    .. code:: python

      for index, ele in enumerate(sequence):
          ele.index = index

    Note: Running this on sequences besides :class:`BMesh.verts`, :class:`BMesh.edges`, :class:`BMesh.faces`
works but won't result in each element having a valid index, instead its order in the sequence will be set.

    """

    ...

  def new(self, verts: BMVert, example: BMFace = None) -> BMFace:

    """

    Create a new face from a given set of verts.

    """

    ...

  def remove(self, face: typing.Any) -> None:

    """

    Remove a face.

    """

    ...

  def sort(self, key: typing.Callable = None, reverse: bool = False) -> None:

    """

    Sort the elements of this sequence, using an optional custom sort key.
Indices of elements are not changed, BMElemeSeq.index_update() can be used for that.

    Note: When the 'key' argument is not provided, the elements are reordered following their current index value.
In particular this can be used by setting indices manually before calling this method.

    Warning: Existing references to the N'th element, will continue to point the data at that index.

    """

    ...

  active: BMFace = ...

  """

  active face.

  """

  layers: BMLayerAccessFace = ...

  """

  custom-data layers (read-only).

  """

class BMLoopSeq:

  layers: BMLayerAccessLoop = ...

  """

  custom-data layers (read-only).

  """

class BMIter:

  """

  Internal BMesh type for looping over verts/faces/edges,
used for iterating over :class:`BMElemSeq` types.

  """

  ...

class BMEditSelSeq:

  def add(self, element: typing.Any) -> None:

    """

    Add an element to the selection history (no action taken if its already added).

    """

    ...

  def clear(self) -> None:

    """

    Empties the selection history.

    """

    ...

  def discard(self, element: typing.Any) -> None:

    """

    Discard an element from the selection history.

    Like remove but doesn't raise an error when the elements not in the selection list.

    """

    ...

  def remove(self, element: typing.Any) -> None:

    """

    Remove an element from the selection history.

    """

    ...

  def validate(self) -> None:

    """

    Ensures all elements in the selection history are selected.

    """

    ...

  active: BMVert = ...

  """

  The last selected element or None (read-only).

  """

class BMEditSelIter:

  ...

class BMLayerAccessVert:

  """

  Exposes custom-data layer attributes.

  """

  bevel_weight: BMLayerCollection = ...

  """

  Bevel weight float in [0 - 1].

  """

  color: typing.Any = ...

  """

  Generic RGBA color with 8-bit precision custom-data layer.

  type: :class:`BMLayerCollection`

  """

  deform: typing.Any = ...

  """

  Vertex deform weight :class:`BMDeformVert` (TODO).

  type: :class:`BMLayerCollection`

  """

  float: typing.Any = ...

  """

  Generic float custom-data layer.

  type: :class:`BMLayerCollection`

  """

  float_color: typing.Any = ...

  """

  Generic RGBA color with float precision custom-data layer.

  type: :class:`BMLayerCollection`

  """

  float_vector: typing.Any = ...

  """

  Generic 3D vector with float precision custom-data layer.

  type: :class:`BMLayerCollection`

  """

  int: typing.Any = ...

  """

  Generic int custom-data layer.

  type: :class:`BMLayerCollection`

  """

  paint_mask: typing.Any = ...

  """

  Accessor for paint mask layer.

  type: :class:`BMLayerCollection`

  """

  shape: BMLayerCollection = ...

  """

  Vertex shapekey absolute location (as a 3D Vector).

  """

  skin: typing.Any = ...

  """

  Accessor for skin layer.

  type: :class:`BMLayerCollection`

  """

  string: typing.Any = ...

  """

  Generic string custom-data layer (exposed as bytes, 255 max length).

  type: :class:`BMLayerCollection`

  """

class BMLayerAccessEdge:

  """

  Exposes custom-data layer attributes.

  """

  bevel_weight: BMLayerCollection = ...

  """

  Bevel weight float in [0 - 1].

  """

  color: typing.Any = ...

  """

  Generic RGBA color with 8-bit precision custom-data layer.

  type: :class:`BMLayerCollection`

  """

  crease: BMLayerCollection = ...

  """

  Edge crease for subdivision surface - float in [0 - 1].

  """

  float: typing.Any = ...

  """

  Generic float custom-data layer.

  type: :class:`BMLayerCollection`

  """

  float_color: typing.Any = ...

  """

  Generic RGBA color with float precision custom-data layer.

  type: :class:`BMLayerCollection`

  """

  float_vector: typing.Any = ...

  """

  Generic 3D vector with float precision custom-data layer.

  type: :class:`BMLayerCollection`

  """

  freestyle: typing.Any = ...

  """

  Accessor for Freestyle edge layer.

  type: :class:`BMLayerCollection`

  """

  int: typing.Any = ...

  """

  Generic int custom-data layer.

  type: :class:`BMLayerCollection`

  """

  string: typing.Any = ...

  """

  Generic string custom-data layer (exposed as bytes, 255 max length).

  type: :class:`BMLayerCollection`

  """

class BMLayerAccessFace:

  """

  Exposes custom-data layer attributes.

  """

  color: typing.Any = ...

  """

  Generic RGBA color with 8-bit precision custom-data layer.

  type: :class:`BMLayerCollection`

  """

  face_map: typing.Any = ...

  """

  FaceMap custom-data layer.

  type: :class:`BMLayerCollection`

  """

  float: typing.Any = ...

  """

  Generic float custom-data layer.

  type: :class:`BMLayerCollection`

  """

  float_color: typing.Any = ...

  """

  Generic RGBA color with float precision custom-data layer.

  type: :class:`BMLayerCollection`

  """

  float_vector: typing.Any = ...

  """

  Generic 3D vector with float precision custom-data layer.

  type: :class:`BMLayerCollection`

  """

  freestyle: typing.Any = ...

  """

  Accessor for Freestyle face layer.

  type: :class:`BMLayerCollection`

  """

  int: typing.Any = ...

  """

  Generic int custom-data layer.

  type: :class:`BMLayerCollection`

  """

  string: typing.Any = ...

  """

  Generic string custom-data layer (exposed as bytes, 255 max length).

  type: :class:`BMLayerCollection`

  """

class BMLayerAccessLoop:

  """

  Exposes custom-data layer attributes.

  """

  color: typing.Any = ...

  """

  Generic RGBA color with 8-bit precision custom-data layer.

  type: :class:`BMLayerCollection`

  """

  float: typing.Any = ...

  """

  Generic float custom-data layer.

  type: :class:`BMLayerCollection`

  """

  float_color: typing.Any = ...

  """

  Generic RGBA color with float precision custom-data layer.

  type: :class:`BMLayerCollection`

  """

  float_vector: typing.Any = ...

  """

  Generic 3D vector with float precision custom-data layer.

  type: :class:`BMLayerCollection`

  """

  int: typing.Any = ...

  """

  Generic int custom-data layer.

  type: :class:`BMLayerCollection`

  """

  string: typing.Any = ...

  """

  Generic string custom-data layer (exposed as bytes, 255 max length).

  type: :class:`BMLayerCollection`

  """

  uv: typing.Any = ...

  """

  Accessor for :class:`BMLoopUV` UV (as a 2D Vector).

  type: :class:`BMLayerCollection`

  """

class BMLayerCollection:

  """

  Gives access to a collection of custom-data layers of the same type and behaves like python dictionaries, except for the ability to do list like index access.

  """

  def get(self, key: str, default: typing.Any = None) -> None:

    """

    Returns the value of the layer matching the key or default
when not found (matches pythons dictionary function of the same name).

    """

    ...

  def items(self) -> typing.List[typing.Tuple[typing.Any, ...]]:

    """

    Return the identifiers of collection members
(matching pythons dict.items() functionality).

    """

    ...

  def keys(self) -> typing.List[str]:

    """

    Return the identifiers of collection members
(matching pythons dict.keys() functionality).

    """

    ...

  def new(self, name: str) -> BMLayerItem:

    """

    Create a new layer

    """

    ...

  def remove(self, layer: BMLayerItem) -> None:

    """

    Remove a layer

    """

    ...

  def values(self) -> typing.List[typing.Any]:

    """

    Return the values of collection
(matching pythons dict.values() functionality).

    """

    ...

  def verify(self) -> BMLayerItem:

    """

    Create a new layer or return an existing active layer

    """

    ...

  active: BMLayerItem = ...

  """

  The active layer of this type (read-only).

  """

  is_singleton: bool = ...

  """

  True if there can exists only one layer of this type (read-only).

  """

class BMLayerItem:

  """

  Exposes a single custom data layer, their main purpose is for use as item accessors to custom-data when used with vert/edge/face/loop data.

  """

  def copy_from(self, other: typing.Any) -> None:

    """

    Return a copy of the layer

    """

    ...

  name: str = ...

  """

  The layers unique name (read-only).

  """

class BMLoopUV:

  pin_uv: bool = ...

  """

  UV pin state.

  """

  select: bool = ...

  """

  UV select state.

  """

  uv: mathutils.Vector = ...

  """

  Loops UV (as a 2D Vector).

  """

class BMDeformVert:

  """"""

  def clear(self) -> None:

    """

    Clears all weights.

    """

    ...

  def get(self, key: int, default: typing.Any = None) -> None:

    """

    Returns the deform weight matching the key or default
when not found (matches pythons dictionary function of the same name).

    """

    ...

  def items(self) -> typing.List[typing.Tuple[typing.Any, ...]]:

    """

    Return (group, weight) pairs for this vertex
(matching pythons dict.items() functionality).

    """

    ...

  def keys(self) -> typing.List[int]:

    """

    Return the group indices used by this vertex
(matching pythons dict.keys() functionality).

    """

    ...

  def values(self) -> typing.List[float]:

    """

    Return the weights of the deform vertex
(matching pythons dict.values() functionality).

    """

    ...
