"""


BMesh Operators (bmesh.ops)
***************************

This module gives access to low level bmesh operations.

Most operators take input and return output, they can be chained together
to perform useful operations.


Operator Example
================

This script shows how operators can be used to model a link of a chain.

.. code::

  # This script uses bmesh operators to make 2 links of a chain.

  import bpy
  import bmesh
  import math
  import mathutils

  # Make a new BMesh
  bm = bmesh.new()

  # Add a circle XXX, should return all geometry created, not just verts.
  bmesh.ops.create_circle(
      bm,
      cap_ends=False,
      radius=0.2,
      segments=8)


  # Spin and deal with geometry on side 'a'
  edges_start_a = bm.edges[:]
  geom_start_a = bm.verts[:] + edges_start_a
  ret = bmesh.ops.spin(
      bm,
      geom=geom_start_a,
      angle=math.radians(180.0),
      steps=8,
      axis=(1.0, 0.0, 0.0),
      cent=(0.0, 1.0, 0.0))
  edges_end_a = [ele for ele in ret["geom_last"]
                 if isinstance(ele, bmesh.types.BMEdge)]
  del ret


  # Extrude and create geometry on side 'b'
  ret = bmesh.ops.extrude_edge_only(
      bm,
      edges=edges_start_a)
  geom_extrude_mid = ret["geom"]
  del ret


  # Collect the edges to spin XXX, 'extrude_edge_only' could return this.
  verts_extrude_b = [ele for ele in geom_extrude_mid
                     if isinstance(ele, bmesh.types.BMVert)]
  edges_extrude_b = [ele for ele in geom_extrude_mid
                     if isinstance(ele, bmesh.types.BMEdge) and ele.is_boundary]
  bmesh.ops.translate(
      bm,
      verts=verts_extrude_b,
      vec=(0.0, 0.0, 1.0))


  # Create the circle on side 'b'
  ret = bmesh.ops.spin(
      bm,
      geom=verts_extrude_b + edges_extrude_b,
      angle=-math.radians(180.0),
      steps=8,
      axis=(1.0, 0.0, 0.0),
      cent=(0.0, 1.0, 1.0))
  edges_end_b = [ele for ele in ret["geom_last"]
                 if isinstance(ele, bmesh.types.BMEdge)]
  del ret


  # Bridge the resulting edge loops of both spins 'a & b'
  bmesh.ops.bridge_loops(
      bm,
      edges=edges_end_a + edges_end_b)


  # Now we have made a links of the chain, make a copy and rotate it
  # (so this looks something like a chain)

  ret = bmesh.ops.duplicate(
      bm,
      geom=bm.verts[:] + bm.edges[:] + bm.faces[:])
  geom_dupe = ret["geom"]
  verts_dupe = [ele for ele in geom_dupe if isinstance(ele, bmesh.types.BMVert)]
  del ret

  # position the new link
  bmesh.ops.translate(
      bm,
      verts=verts_dupe,
      vec=(0.0, 0.0, 2.0))
  bmesh.ops.rotate(
      bm,
      verts=verts_dupe,
      cent=(0.0, 1.0, 0.0),
      matrix=mathutils.Matrix.Rotation(math.radians(90.0), 3, 'Z'))

  # Done with creating the mesh, simply link it into the scene so we can see it

  # Finish up, write the bmesh into a new mesh
  me = bpy.data.meshes.new("Mesh")
  bm.to_mesh(me)
  bm.free()


  # Add the mesh to the scene
  obj = bpy.data.objects.new("Object", me)
  bpy.context.collection.objects.link(obj)

  # Select and make active
  bpy.context.view_layer.objects.active = obj
  obj.select_set(True)

:func:`smooth_vert`

:func:`smooth_laplacian_vert`

:func:`recalc_face_normals`

:func:`planar_faces`

:func:`region_extend`

:func:`rotate_edges`

:func:`reverse_faces`

:func:`bisect_edges`

:func:`mirror`

:func:`find_doubles`

:func:`remove_doubles`

:func:`collapse`

:func:`pointmerge_facedata`

:func:`average_vert_facedata`

:func:`pointmerge`

:func:`collapse_uvs`

:func:`weld_verts`

:func:`create_vert`

:func:`join_triangles`

:func:`contextual_create`

:func:`bridge_loops`

:func:`grid_fill`

:func:`holes_fill`

:func:`face_attribute_fill`

:func:`edgeloop_fill`

:func:`edgenet_fill`

:func:`edgenet_prepare`

:func:`rotate`

:func:`translate`

:func:`scale`

:func:`transform`

:func:`object_load_bmesh`

:func:`bmesh_to_mesh`

:func:`mesh_to_bmesh`

:func:`extrude_discrete_faces`

:func:`extrude_edge_only`

:func:`extrude_vert_indiv`

:func:`connect_verts`

:func:`connect_verts_concave`

:func:`connect_verts_nonplanar`

:func:`connect_vert_pair`

:func:`extrude_face_region`

:func:`dissolve_verts`

:func:`dissolve_edges`

:func:`dissolve_faces`

:func:`dissolve_limit`

:func:`dissolve_degenerate`

:func:`triangulate`

:func:`unsubdivide`

:func:`subdivide_edges`

:func:`subdivide_edgering`

:func:`bisect_plane`

:func:`delete`

:func:`duplicate`

:func:`split`

:func:`spin`

:func:`rotate_uvs`

:func:`reverse_uvs`

:func:`rotate_colors`

:func:`reverse_colors`

:func:`split_edges`

:func:`create_grid`

:func:`create_uvsphere`

:func:`create_icosphere`

:func:`create_monkey`

:func:`create_cone`

:func:`create_circle`

:func:`create_cube`

:func:`bevel`

:func:`beautify_fill`

:func:`triangle_fill`

:func:`solidify`

:func:`inset_individual`

:func:`inset_region`

:func:`offset_edgeloops`

:func:`wireframe`

:func:`poke`

:func:`convex_hull`

:func:`symmetrize`

"""

import typing

import mathutils

import bpy

import bmesh

def smooth_vert(bm: bmesh.types.BMesh, verts: typing.List[typing.Any], factor: float, mirror_clip_x: bool, mirror_clip_y: bool, mirror_clip_z: bool, clip_dist: float, use_axis_x: bool, use_axis_y: bool, use_axis_z: bool) -> None:

  """

  Vertex Smooth.

  Smooths vertices by using a basic vertex averaging scheme.

  """

  ...

def smooth_laplacian_vert(bm: bmesh.types.BMesh, verts: typing.List[typing.Any], lambda_factor: float, lambda_border: float, use_x: bool, use_y: bool, use_z: bool, preserve_volume: bool) -> None:

  """

  Vertex Smooth Laplacian.

  Smooths vertices by using Laplacian smoothing propose by.
Desbrun, et al. Implicit Fairing of Irregular Meshes using Diffusion and Curvature Flow.

  """

  ...

def recalc_face_normals(bm: bmesh.types.BMesh, faces: typing.List[typing.Any]) -> None:

  """

  Right-Hand Faces.

  Computes an "outside" normal for the specified input faces.

  """

  ...

def planar_faces(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], iterations: int, factor: float) -> typing.Dict[str, typing.Any]:

  """

  Planar Faces.

  Iteratively flatten faces.

  """

  ...

def region_extend(bm: bmesh.types.BMesh, geom: typing.List[typing.Any], use_contract: bool, use_faces: bool, use_face_step: bool) -> typing.Dict[str, typing.Any]:

  """

  Region Extend.

  used to implement the select more/less tools.
this puts some geometry surrounding regions of
geometry in geom into geom.out.

  if use_faces is 0 then geom.out spits out verts and edges,
otherwise it spits out faces.

  """

  ...

def rotate_edges(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], use_ccw: bool) -> typing.Dict[str, typing.Any]:

  """

  Edge Rotate.

  Rotates edges topologically.  Also known as "spin edge" to some people.
Simple example: *[/] becomes [|] then []*.

  """

  ...

def reverse_faces(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], flip_multires: bool) -> None:

  """

  Reverse Faces.

  Reverses the winding (vertex order) of faces.
This has the effect of flipping the normal.

  """

  ...

def bisect_edges(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], cuts: int, edge_percents: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:

  """

  Edge Bisect.

  Splits input edges (but doesn't do anything else).
This creates a 2-valence vert.

  """

  ...

def mirror(bm: bmesh.types.BMesh, geom: typing.List[typing.Any], matrix: mathutils.Matrix, merge_dist: float, axis: str, mirror_u: bool, mirror_v: bool, mirror_udim: bool, use_shapekey: bool) -> typing.Dict[str, typing.Any]:

  """

  Mirror.

  Mirrors geometry along an axis.  The resulting geometry is welded on using
merge_dist.  Pairs of original/mirrored vertices are welded using the merge_dist
parameter (which defines the minimum distance for welding to happen).

  """

  ...

def find_doubles(bm: bmesh.types.BMesh, verts: typing.List[typing.Any], keep_verts: typing.List[typing.Any], dist: float) -> typing.Dict[str, typing.Any]:

  """

  Find Doubles.

  Takes input verts and find vertices they should weld to.
Outputs a mapping slot suitable for use with the weld verts bmop.

  If keep_verts is used, vertices outside that set can only be merged
with vertices in that set.

  """

  ...

def remove_doubles(bm: bmesh.types.BMesh, verts: typing.List[typing.Any], dist: float) -> None:

  """

  Remove Doubles.

  Finds groups of vertices closer than dist and merges them together,
using the weld verts bmop.

  """

  ...

def collapse(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], uvs: bool) -> None:

  """

  Collapse Connected.

  Collapses connected vertices

  """

  ...

def pointmerge_facedata(bm: bmesh.types.BMesh, verts: typing.List[typing.Any], vert_snap: bmesh.types.BMVert) -> None:

  """

  Face-Data Point Merge.

  Merge uv/vcols at a specific vertex.

  """

  ...

def average_vert_facedata(bm: bmesh.types.BMesh, verts: typing.List[typing.Any]) -> None:

  """

  Average Vertices Facevert Data.

  Merge uv/vcols associated with the input vertices at
the bounding box center. (I know, it's not averaging but
the vert_snap_to_bb_center is just too long).

  """

  ...

def pointmerge(bm: bmesh.types.BMesh, verts: typing.List[typing.Any], merge_co: typing.Union[mathutils.Vector, typing.Any]) -> None:

  """

  Point Merge.

  Merge verts together at a point.

  """

  ...

def collapse_uvs(bm: bmesh.types.BMesh, edges: typing.List[typing.Any]) -> None:

  """

  Collapse Connected UV's.

  Collapses connected UV vertices.

  """

  ...

def weld_verts(bm: bmesh.types.BMesh, targetmap: typing.Dict[str, typing.Any]) -> None:

  """

  Weld Verts.

  Welds verts together (kind-of like remove doubles, merge, etc, all of which
use or will use this bmop).  You pass in mappings from vertices to the vertices
they weld with.

  """

  ...

def create_vert(bm: bmesh.types.BMesh, co: typing.Union[mathutils.Vector, typing.Any]) -> typing.Dict[str, typing.Any]:

  """

  Make Vertex.

  Creates a single vertex; this bmop was necessary
for click-create-vertex.

  """

  ...

def join_triangles(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], cmp_seam: bool, cmp_sharp: bool, cmp_uvs: bool, cmp_vcols: bool, cmp_materials: bool, angle_face_threshold: float, angle_shape_threshold: float) -> typing.Dict[str, typing.Any]:

  """

  Join Triangles.

  Tries to intelligently join triangles according
to angle threshold and delimiters.

  """

  ...

def contextual_create(bm: bmesh.types.BMesh, geom: typing.List[typing.Any], mat_nr: int, use_smooth: bool) -> typing.Dict[str, typing.Any]:

  """

  Contextual Create.

  This is basically F-key, it creates
new faces from vertices, makes stuff from edge nets,
makes wire edges, etc.  It also dissolves faces.

  Three verts become a triangle, four become a quad.  Two
become a wire edge.

  """

  ...

def bridge_loops(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], use_pairs: bool, use_cyclic: bool, use_merge: bool, merge_factor: float, twist_offset: int) -> typing.Dict[str, typing.Any]:

  """

  Bridge edge loops with faces.

  """

  ...

def grid_fill(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], mat_nr: int, use_smooth: bool, use_interp_simple: bool) -> typing.Dict[str, typing.Any]:

  """

  Grid Fill.

  Create faces defined by 2 disconnected edge loops (which share edges).

  """

  ...

def holes_fill(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], sides: int) -> typing.Dict[str, typing.Any]:

  """

  Fill Holes.

  Fill boundary edges with faces, copying surrounding customdata.

  """

  ...

def face_attribute_fill(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], use_normals: bool, use_data: bool) -> typing.Dict[str, typing.Any]:

  """

  Face Attribute Fill.

  Fill in faces with data from adjacent faces.

  """

  ...

def edgeloop_fill(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], mat_nr: int, use_smooth: bool) -> typing.Dict[str, typing.Any]:

  """

  Edge Loop Fill.

  Create faces defined by one or more non overlapping edge loops.

  """

  ...

def edgenet_fill(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], mat_nr: int, use_smooth: bool, sides: int) -> typing.Dict[str, typing.Any]:

  """

  Edge Net Fill.

  Create faces defined by enclosed edges.

  """

  ...

def edgenet_prepare(bm: bmesh.types.BMesh, edges: typing.List[typing.Any]) -> typing.Dict[str, typing.Any]:

  """

  Edge-net Prepare.

  Identifies several useful edge loop cases and modifies them so
they'll become a face when edgenet_fill is called.  The cases covered are:

  * One single loop; an edge is added to connect the ends

  * Two loops; two edges are added to connect the endpoints (based on the
shortest distance between each endpoint).

  """

  ...

def rotate(bm: bmesh.types.BMesh, cent: typing.Union[mathutils.Vector, typing.Any], matrix: mathutils.Matrix, verts: typing.List[typing.Any], space: mathutils.Matrix, use_shapekey: bool) -> None:

  """

  Rotate.

  Rotate vertices around a center, using a 3x3 rotation matrix.

  """

  ...

def translate(bm: bmesh.types.BMesh, vec: typing.Union[mathutils.Vector, typing.Any], space: mathutils.Matrix, verts: typing.List[typing.Any], use_shapekey: bool) -> None:

  """

  Translate.

  Translate vertices by an offset.

  """

  ...

def scale(bm: bmesh.types.BMesh, vec: typing.Union[mathutils.Vector, typing.Any], space: mathutils.Matrix, verts: typing.List[typing.Any], use_shapekey: bool) -> None:

  """

  Scale.

  Scales vertices by an offset.

  """

  ...

def transform(bm: bmesh.types.BMesh, matrix: mathutils.Matrix, space: mathutils.Matrix, verts: typing.List[typing.Any], use_shapekey: bool) -> None:

  """

  Transform.

  Transforms a set of vertices by a matrix.  Multiplies
the vertex coordinates with the matrix.

  """

  ...

def object_load_bmesh(bm: bmesh.types.BMesh, scene: bpy.types.Scene, object: bpy.types.Object) -> None:

  """

  Object Load BMesh.

  Loads a bmesh into an object/mesh.  This is a "private"
bmop.

  """

  ...

def bmesh_to_mesh(bm: bmesh.types.BMesh, mesh: bpy.types.Mesh, object: bpy.types.Object) -> None:

  """

  BMesh to Mesh.

  Converts a bmesh to a Mesh.  This is reserved for exiting editmode.

  """

  ...

def mesh_to_bmesh(bm: bmesh.types.BMesh, mesh: bpy.types.Mesh, object: bpy.types.Object, use_shapekey: bool) -> None:

  """

  Mesh to BMesh.

  Load the contents of a mesh into the bmesh.  this bmop is private, it's
reserved exclusively for entering editmode.

  """

  ...

def extrude_discrete_faces(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], use_normal_flip: bool, use_select_history: bool) -> typing.Dict[str, typing.Any]:

  """

  Individual Face Extrude.

  Extrudes faces individually.

  """

  ...

def extrude_edge_only(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], use_normal_flip: bool, use_select_history: bool) -> typing.Dict[str, typing.Any]:

  """

  Extrude Only Edges.

  Extrudes Edges into faces, note that this is very simple, there's no fancy
winged extrusion.

  """

  ...

def extrude_vert_indiv(bm: bmesh.types.BMesh, verts: typing.List[typing.Any], use_select_history: bool) -> typing.Dict[str, typing.Any]:

  """

  Individual Vertex Extrude.

  Extrudes wire edges from vertices.

  """

  ...

def connect_verts(bm: bmesh.types.BMesh, verts: typing.List[typing.Any], faces_exclude: typing.List[typing.Any], check_degenerate: bool) -> typing.Dict[str, typing.Any]:

  """

  Connect Verts.

  Split faces by adding edges that connect **verts**.

  """

  ...

def connect_verts_concave(bm: bmesh.types.BMesh, faces: typing.List[typing.Any]) -> typing.Dict[str, typing.Any]:

  """

  Connect Verts to form Convex Faces.

  Ensures all faces are convex **faces**.

  """

  ...

def connect_verts_nonplanar(bm: bmesh.types.BMesh, angle_limit: float, faces: typing.List[typing.Any]) -> typing.Dict[str, typing.Any]:

  """

  Connect Verts Across non Planer Faces.

  Split faces by connecting edges along non planer **faces**.

  """

  ...

def connect_vert_pair(bm: bmesh.types.BMesh, verts: typing.List[typing.Any], verts_exclude: typing.List[typing.Any], faces_exclude: typing.List[typing.Any]) -> typing.Dict[str, typing.Any]:

  """

  Connect Verts.

  Split faces by adding edges that connect **verts**.

  """

  ...

def extrude_face_region(bm: bmesh.types.BMesh, geom: typing.List[typing.Any], edges_exclude: typing.Set[typing.Any], use_keep_orig: bool, use_normal_flip: bool, use_normal_from_adjacent: bool, use_dissolve_ortho_edges: bool, use_select_history: bool) -> typing.Dict[str, typing.Any]:

  """

  Extrude Faces.

  Extrude operator (does not transform)

  """

  ...

def dissolve_verts(bm: bmesh.types.BMesh, verts: typing.List[typing.Any], use_face_split: bool, use_boundary_tear: bool) -> None:

  """

  Dissolve Verts.

  """

  ...

def dissolve_edges(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], use_verts: bool, use_face_split: bool) -> typing.Dict[str, typing.Any]:

  """

  Dissolve Edges.

  """

  ...

def dissolve_faces(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], use_verts: bool) -> typing.Dict[str, typing.Any]:

  """

  Dissolve Faces.

  """

  ...

def dissolve_limit(bm: bmesh.types.BMesh, angle_limit: float, use_dissolve_boundaries: bool, verts: typing.List[typing.Any], edges: typing.List[typing.Any], delimit: typing.Set[typing.Any]) -> typing.Dict[str, typing.Any]:

  """

  Limited Dissolve.

  Dissolve planar faces and co-linear edges.

  """

  ...

def dissolve_degenerate(bm: bmesh.types.BMesh, dist: float, edges: typing.List[typing.Any]) -> None:

  """

  Degenerate Dissolve.

  Dissolve edges with no length, faces with no area.

  """

  ...

def triangulate(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], quad_method: str, ngon_method: str) -> typing.Dict[str, typing.Any]:

  """

  Triangulate.

  """

  ...

def unsubdivide(bm: bmesh.types.BMesh, verts: typing.List[typing.Any], iterations: int) -> None:

  """

  Un-Subdivide.

  Reduce detail in geometry containing grids.

  """

  ...

def subdivide_edges(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], smooth: float, smooth_falloff: str, fractal: float, along_normal: float, cuts: int, seed: int, custom_patterns: typing.Dict[str, typing.Any], edge_percents: typing.Dict[str, typing.Any], quad_corner_type: str, use_grid_fill: bool, use_single_edge: bool, use_only_quads: bool, use_sphere: bool, use_smooth_even: bool) -> typing.Dict[str, typing.Any]:

  """

  Subdivide Edges.

  Advanced operator for subdividing edges
with options for face patterns, smoothing and randomization.

  """

  ...

def subdivide_edgering(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], interp_mode: str, smooth: float, cuts: int, profile_shape: str, profile_shape_factor: float) -> typing.Dict[str, typing.Any]:

  """

  Subdivide Edge-Ring.

  Take an edge-ring, and subdivide with interpolation options.

  """

  ...

def bisect_plane(bm: bmesh.types.BMesh, geom: typing.List[typing.Any], dist: float, plane_co: typing.Union[mathutils.Vector, typing.Any], plane_no: typing.Union[mathutils.Vector, typing.Any], use_snap_center: bool, clear_outer: bool, clear_inner: bool) -> typing.Dict[str, typing.Any]:

  """

  Bisect Plane.

  Bisects the mesh by a plane (cut the mesh in half).

  """

  ...

def delete(bm: bmesh.types.BMesh, geom: typing.List[typing.Any], context: str) -> None:

  """

  Delete Geometry.

  Utility operator to delete geometry.

  """

  ...

def duplicate(bm: bmesh.types.BMesh, geom: typing.List[typing.Any], dest: bmesh.types.BMesh, use_select_history: bool, use_edge_flip_from_face: bool) -> typing.Dict[str, typing.Any]:

  """

  Duplicate Geometry.

  Utility operator to duplicate geometry,
optionally into a destination mesh.

  """

  ...

def split(bm: bmesh.types.BMesh, geom: typing.List[typing.Any], dest: bmesh.types.BMesh, use_only_faces: bool) -> typing.Dict[str, typing.Any]:

  """

  Split Off Geometry.

  Disconnect geometry from adjacent edges and faces,
optionally into a destination mesh.

  """

  ...

def spin(bm: bmesh.types.BMesh, geom: typing.List[typing.Any], cent: typing.Union[mathutils.Vector, typing.Any], axis: typing.Union[mathutils.Vector, typing.Any], dvec: typing.Union[mathutils.Vector, typing.Any], angle: float, space: mathutils.Matrix, steps: int, use_merge: bool, use_normal_flip: bool, use_duplicate: bool) -> typing.Dict[str, typing.Any]:

  """

  Spin.

  Extrude or duplicate geometry a number of times,
rotating and possibly translating after each step

  """

  ...

def rotate_uvs(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], use_ccw: bool) -> None:

  """

  UV Rotation.

  Cycle the loop UV's

  """

  ...

def reverse_uvs(bm: bmesh.types.BMesh, faces: typing.List[typing.Any]) -> None:

  """

  UV Reverse.

  Reverse the UV's

  """

  ...

def rotate_colors(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], use_ccw: bool) -> None:

  """

  Color Rotation.

  Cycle the loop colors

  """

  ...

def reverse_colors(bm: bmesh.types.BMesh, faces: typing.List[typing.Any]) -> None:

  """

  Color Reverse

  Reverse the loop colors.

  """

  ...

def split_edges(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], verts: typing.List[typing.Any], use_verts: bool) -> typing.Dict[str, typing.Any]:

  """

  Edge Split.

  Disconnects faces along input edges.

  """

  ...

def create_grid(bm: bmesh.types.BMesh, x_segments: int, y_segments: int, size: float, matrix: mathutils.Matrix, calc_uvs: bool) -> typing.Dict[str, typing.Any]:

  """

  Create Grid.

  Creates a grid with a variable number of subdivisions

  """

  ...

def create_uvsphere(bm: bmesh.types.BMesh, u_segments: int, v_segments: int, radius: float, matrix: mathutils.Matrix, calc_uvs: bool) -> typing.Dict[str, typing.Any]:

  """

  Create UV Sphere.

  Creates a grid with a variable number of subdivisions

  """

  ...

def create_icosphere(bm: bmesh.types.BMesh, subdivisions: int, radius: float, matrix: mathutils.Matrix, calc_uvs: bool) -> typing.Dict[str, typing.Any]:

  """

  Create Ico-Sphere.

  Creates a grid with a variable number of subdivisions

  """

  ...

def create_monkey(bm: bmesh.types.BMesh, matrix: mathutils.Matrix, calc_uvs: bool) -> typing.Dict[str, typing.Any]:

  """

  Create Suzanne.

  Creates a monkey (standard blender primitive).

  """

  ...

def create_cone(bm: bmesh.types.BMesh, cap_ends: bool, cap_tris: bool, segments: int, radius1: float, radius2: float, depth: float, matrix: mathutils.Matrix, calc_uvs: bool) -> typing.Dict[str, typing.Any]:

  """

  Create Cone.

  Creates a cone with variable depth at both ends

  """

  ...

def create_circle(bm: bmesh.types.BMesh, cap_ends: bool, cap_tris: bool, segments: int, radius: float, matrix: mathutils.Matrix, calc_uvs: bool) -> typing.Dict[str, typing.Any]:

  """

  Creates a Circle.

  """

  ...

def create_cube(bm: bmesh.types.BMesh, size: float, matrix: mathutils.Matrix, calc_uvs: bool) -> typing.Dict[str, typing.Any]:

  """

  Create Cube

  Creates a cube.

  """

  ...

def bevel(bm: bmesh.types.BMesh, geom: typing.List[typing.Any], offset: float, offset_type: str, profile_type: str, segments: int, profile: float, affect: str, clamp_overlap: bool, material: int, loop_slide: bool, mark_seam: bool, mark_sharp: bool, harden_normals: bool, face_strength_mode: str, miter_outer: str, miter_inner: str, spread: float, smoothresh: float, custom_profile: bpy.types.bpy_struct, vmesh_method: str) -> typing.Dict[str, typing.Any]:

  """

  Bevel.

  Bevels edges and vertices

  """

  ...

def beautify_fill(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], edges: typing.List[typing.Any], use_restrict_tag: bool, method: str) -> typing.Dict[str, typing.Any]:

  """

  Beautify Fill.

  Rotate edges to create more evenly spaced triangles.

  """

  ...

def triangle_fill(bm: bmesh.types.BMesh, use_beauty: bool, use_dissolve: bool, edges: typing.List[typing.Any], normal: typing.Union[mathutils.Vector, typing.Any]) -> typing.Dict[str, typing.Any]:

  """

  Triangle Fill.

  Fill edges with triangles

  """

  ...

def solidify(bm: bmesh.types.BMesh, geom: typing.List[typing.Any], thickness: float) -> typing.Dict[str, typing.Any]:

  """

  Solidify.

  Turns a mesh into a shell with thickness

  """

  ...

def inset_individual(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], thickness: float, depth: float, use_even_offset: bool, use_interpolate: bool, use_relative_offset: bool) -> typing.Dict[str, typing.Any]:

  """

  Face Inset (Individual).

  Insets individual faces.

  """

  ...

def inset_region(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], faces_exclude: typing.List[typing.Any], use_boundary: bool, use_even_offset: bool, use_interpolate: bool, use_relative_offset: bool, use_edge_rail: bool, thickness: float, depth: float, use_outset: bool) -> typing.Dict[str, typing.Any]:

  """

  Face Inset (Regions).

  Inset or outset face regions.

  """

  ...

def offset_edgeloops(bm: bmesh.types.BMesh, edges: typing.List[typing.Any], use_cap_endpoint: bool) -> typing.Dict[str, typing.Any]:

  """

  Edge-loop Offset.

  Creates edge loops based on simple edge-outset method.

  """

  ...

def wireframe(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], thickness: float, offset: float, use_replace: bool, use_boundary: bool, use_even_offset: bool, use_crease: bool, crease_weight: float, use_relative_offset: bool, material_offset: int) -> typing.Dict[str, typing.Any]:

  """

  Wire Frame.

  Makes a wire-frame copy of faces.

  """

  ...

def poke(bm: bmesh.types.BMesh, faces: typing.List[typing.Any], offset: float, center_mode: str, use_relative_offset: bool) -> typing.Dict[str, typing.Any]:

  """

  Pokes a face.

  Splits a face into a triangle fan.

  """

  ...

def convex_hull(bm: bmesh.types.BMesh, input: typing.List[typing.Any], use_existing_faces: bool) -> typing.Dict[str, typing.Any]:

  """

  Convex Hull

  Builds a convex hull from the vertices in 'input'.

  If 'use_existing_faces' is true, the hull will not output triangles
that are covered by a pre-existing face.

  All hull vertices, faces, and edges are added to 'geom.out'. Any
input elements that end up inside the hull (i.e. are not used by an
output face) are added to the 'interior_geom' slot. The
'unused_geom' slot will contain all interior geometry that is
completely unused. Lastly, 'holes_geom' contains edges and faces
that were in the input and are part of the hull.

  """

  ...

def symmetrize(bm: bmesh.types.BMesh, input: typing.List[typing.Any], direction: str, dist: float, use_shapekey: bool) -> typing.Dict[str, typing.Any]:

  """

  Symmetrize.

  Makes the mesh elements in the "input" slot symmetrical. Unlike
normal mirroring, it only copies in one direction, as specified by
the "direction" slot. The edges and faces that cross the plane of
symmetry are split as needed to enforce symmetry.

  All new vertices, edges, and faces are added to the "geom.out" slot.

  """

  ...
