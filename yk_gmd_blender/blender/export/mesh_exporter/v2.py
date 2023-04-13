import array
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set, TypeVar, NewType, Callable, Optional, Union
from typing import cast

import numpy as np

import bpy
from yk_gmd_blender.blender.common import AttribSetLayerNames
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDSkinnedMesh, GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer, GMDSkinnedVertexBuffer
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter


def split_skinned_blender_mesh_object(context: bpy.types.Context, object: bpy.types.Object,
                                      materials: List[GMDAttributeSet], bone_name_map: Dict[str, GMDBone],
                                      bone_limit: int,
                                      error: ErrorReporter) -> List[GMDSkinnedMesh]:
    mesh = prepare_mesh(context, object, check_needs_tangent(materials))
    # Apply all transformations - skinned objects are always located at (0,0,0)
    mesh.transform(object.matrix_world)

    vertex_group_mapping: Dict[int, GMDBone] = {
        i: bone_name_map[group.name]
        for i, group in enumerate(object.vertex_groups)
        if group.name in bone_name_map
    }

    error.debug("MESH", f"Exporting skinned meshes for {object.name}")
    per_mat_meshloop_lists_and_triangles = material_split_meshloops_and_triangles(mesh)
    bone_info = compute_vertex_4weights(mesh, relevant_vertex_groups=set(vertex_group_mapping.keys()), error=error)

    skinned_submeshes: List[SkinnedSubmesh] = []
    for (material_idx, (loops, triangles)) in per_mat_meshloop_lists_and_triangles.items():
        skinned_submeshes += convert_meshloop_tris_to_skinned_submeshes(mesh, loops, triangles, material_idx, bone_info,
                                                                        error, max_bones_per_submesh=bone_limit)

    return [s.build_skinned(mesh, bone_info, materials, error) for s in skinned_submeshes]


def split_unskinned_blender_mesh_object(context: bpy.types.Context, object: bpy.types.Object,
                                        materials: List[GMDAttributeSet], error: ErrorReporter) -> List[GMDMesh]:
    mesh = prepare_mesh(context, object, check_needs_tangent(materials))

    error.debug("MESH", f"Exporting unskinned meshes for {object.name}")
    per_mat_meshloop_lists_and_triangles = material_split_meshloops_and_triangles(mesh)
    submeshes: List[Submesh] = []
    for (material_idx, (loops, triangles)) in per_mat_meshloop_lists_and_triangles.items():
        submeshes += convert_meshloop_tris_to_unskinned_submeshes(loops, triangles, material_idx)

    return [s.build_unskinned(mesh, materials, error) for s in submeshes]


def prepare_mesh(context: bpy.types.Context, object: bpy.types.Object, needs_tangent: bool) -> bpy.types.Mesh:
    """
    Given an object with a bpy Mesh, make a copy of that mesh where
     1) all modifiers are applied
     2) the mesh has been triangulates
     3) split normals (and optionally tangents) have been calculated
     4) calc_loop_triangles() has been called, so can iterate over loops
    """

    # Apply the dependency graph to the mesh
    # https://blender.stackexchange.com/a/146911
    dg = context.evaluated_depsgraph_get()

    # Evaluate the dependency graph (creates a new mesh)
    bpy_mesh = cast(bpy.types.Mesh, object.evaluated_get(dg).data)

    # Now it's triangulated we can calculate tangents (TODO calc_normals_split may not be necessary anymore)
    bpy_mesh.calc_normals_split()
    if needs_tangent:
        bpy_mesh.calc_tangents()

    # TODO assuming this triangulates automatically
    bpy_mesh.calc_loop_triangles()

    return bpy_mesh


def check_needs_tangent(materials: List[GMDAttributeSet]) -> bool:
    return any(m.shader.vertex_buffer_layout.tangent_storage for m in materials)


MeshLoopIdx = NewType("MeshLoopIdx", int)


def material_split_meshloops_and_triangles(mesh: bpy.types.Mesh) -> Dict[int, Tuple[
    List[MeshLoopIdx],
    List[Tuple[int, int, int]]
]]:
    """
    Given a bpy Mesh, return a list of "unique" MeshLoop indices and the triangle indices *within that list*
    for the triangles for each material index.

    "unique" here means each each MeshLoop index maps directly to a single vertex in the final buffer.
    :param mesh:
    :return:
    """

    combined_meshloop_idxs_triangles: Dict[int, Tuple[
        List[MeshLoopIdx],
        List[Tuple[int, int, int]]
    ]] = defaultdict(lambda: ([], []))

    # Mapping of (material idx, vertex idx referenced by a smooth triangle) ->
    # (index of a matching "meshloop idx" in meshloop_idxs[material idx])
    smooth_vert_idxs: Dict[Tuple[int, int], int] = {}

    # Map (smooth meshloop idx) to (index of a matching "meshloop idx" in meshloop_idxs[material_idx]),
    # adding it if it isn't already there.
    # The meshloop idx may match a previously used smooth meshloop idx if they point to the same vertex.
    def add_or_reuse_smooth_meshloop_idx(material_idx: int, meshloop_idx: int) -> int:
        vert_data = (material_idx, mesh.loops[meshloop_idx].vertex_index)
        preexisting_idx = smooth_vert_idxs.get(vert_data)
        if preexisting_idx is None:
            meshloop_idxs = combined_meshloop_idxs_triangles[material_idx][0]
            new_idx = len(meshloop_idxs)
            smooth_vert_idxs[vert_data] = new_idx
            meshloop_idxs.append(MeshLoopIdx(meshloop_idx))
            return new_idx
        else:
            return preexisting_idx

    # Mapping of (material idx, vertex idx, normal referenced by not-smooth triangle) ->
    # (index of a matching "meshloop idx" in meshloop_idxs[material_idx])
    #
    # This is for the sake of deduping e.g. common vertices in a flat-shaded quad, NOT for deduping vertices that happen
    # to have identical data.
    hard_vert_idxs: Dict[Tuple[int, int, Tuple[float, float, float]], int] = {}

    # Map (flat meshloop idx) to (index of a matching "meshloop idx" in meshloop_idxs[material_idx]),
    # adding it if it isn't already there.
    # The meshloop idx may match a previously used flat meshloop idx if they point to the same vertex
    # and have the same normal.
    def add_or_reuse_flat_meshloop_idx(material_idx: int, meshloop_idx: int) -> int:
        loop = mesh.loops[meshloop_idx]
        vert_data = (material_idx, loop.vertex_index, loop.normal)
        preexisting_idx = hard_vert_idxs.get(vert_data)
        if preexisting_idx is None:
            meshloop_idxs = combined_meshloop_idxs_triangles[material_idx][0]
            new_idx = len(meshloop_idxs)
            hard_vert_idxs[vert_data] = new_idx
            meshloop_idxs.append(MeshLoopIdx(meshloop_idx))
            return new_idx
        else:
            return preexisting_idx

    for t in mesh.loop_triangles:
        material_idx = t.material_index
        triangles: List[Tuple[int, int, int]] = combined_meshloop_idxs_triangles[material_idx][1]
        if t.use_smooth:
            triangles.append((
                add_or_reuse_smooth_meshloop_idx(material_idx, t.loops[0]),
                add_or_reuse_smooth_meshloop_idx(material_idx, t.loops[1]),
                add_or_reuse_smooth_meshloop_idx(material_idx, t.loops[2]),
            ))
        else:
            triangles.append((
                add_or_reuse_flat_meshloop_idx(material_idx, t.loops[0]),
                add_or_reuse_flat_meshloop_idx(material_idx, t.loops[1]),
                add_or_reuse_flat_meshloop_idx(material_idx, t.loops[2]),
            ))

    return combined_meshloop_idxs_triangles


def compute_vertex_4weights(
        mesh: bpy.types.Mesh,
        relevant_vertex_groups: Set[int],
        error: ErrorReporter
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Given a bpy Mesh, find the top 4 bones and weights of each vertex.
    Returns two ndarrays, one for bones and one for weights.
    bones[vertex][i] = 0 if weights[vertex][i] is 0, else = the index of a vertex group in relevant_vertex_groups.
    weights[vertex][i] = float in [0, 1].
    n_weights[vertex] = the number of active weights for the vertex (max 4).
    e.g. if n_weights[v] = 3, bones[v][3] == weights[v][3] == 0 but weights[v][0..2] are nonzero.
    bones[vertex] and weights[vertex] are sorted in descending weight e.g.
    bones[v] = [0, 1, 2, 3]
    weights[v] = [0.5, 0.3, 0.1, 0.1]

    :param relevant_vertex_groups: A set of relevant (mesh vertex group index) values. Weights for other groups are ignored.
    :return:
    """

    # Right now we store the bone indices (which can be 0..all bones that touch the mesh) inside a uint16.
    # Once they're split up into submeshes the max is 255 to fit into a uint8, but I *think* >255 bones per overall mesh
    # is accepted.
    # We should never need to up this limit unless RGG do something really dumb.
    if max(relevant_vertex_groups) > 65535:
        error.fatal(
            f"Mesh {mesh.name} has vertex group indices > 65535. This is not supported. Use fewer bones please.")
    bones = np.zeros((len(mesh.vertices), 4), np.uint16)
    weights = np.zeros((len(mesh.vertices), 4), np.float32)
    n_weights = np.zeros(len(mesh.vertices), np.uint8)

    has_warned_about_weights_over_one = False

    for v in mesh.vertices:
        # For each vertex: take all boneweights that are part of this armature,
        # sort them in descending order of weight,
        # do sanity checks for values > 1 and < 0,
        # and put the first 4 values into the bones/weights array.
        # If there are fewer than 4 values, the others default to 0.
        gs = sorted(
            [
                g
                for g in v.groups
                if g.group in relevant_vertex_groups
            ],
            key=lambda g: g.weight,
            reverse=True
        )

        # Check if weights are greater than 1 or lower than 0
        if gs and gs[0].weight > 1 and not has_warned_about_weights_over_one:
            error.recoverable(f"Some weights in mesh {mesh.name} are greater than 1. "
                              f"These can't be exported - try normalizing your weights, or turn off Strict Export "
                              f"to clamp it to 1")
            has_warned_about_weights_over_one = True
        if gs and gs[-1].weight < 0:
            error.fatal(f"Some weights in mesh {mesh.name} are smaller than 0 - this is impossible.")

        # For each of the top four elements of bws, push it into bones/weights
        v_n_weights = min(4, len(gs))
        n_weights[v.index] = v_n_weights
        for i in range(v_n_weights):
            bones[v.index][i] = gs[i].group if gs[i].weight else 0,
            weights[v.index][i] = min(1.0, gs[i].weight)
        # Sanity checks for meshes with more than 4 ""major"" influences.
        if len(gs) > 4 and any(g.weight > 0.1 for g in gs[4:]):
            error.recoverable(f"Some vertices in mesh {mesh.name} have more than 4 major influences. "
                              f"A major influence is a bone with weight greater than 0.1. "
                              f"The exporter can only export 4 influences per vertex, so animation on this model may "
                              f"look odd. Turn off Strict Export if this is acceptable.")

    return bones, weights, n_weights


@dataclass(frozen=True)
class Submesh:
    """
    A "submesh" - a minimally exportable chunk of a mesh.
    Contains at most 65536 "vertices".
    """

    # Indices of the meshloops to turn into vertices.
    loops: List[MeshLoopIdx]
    # Triangle definitions, with indexes *that index into self.meshloop_idxs*
    triangles: List[Tuple[int, int, int]]
    # The index of the material in the top-level blender mesh.
    material_idx: int

    def __post_init__(self):
        if len(self.loops) > 65536:
            raise RuntimeError("Created a Submesh with more than 65536 vertices.")

    def build_unskinned(self, mesh: bpy.types.Mesh, materials: List[GMDAttributeSet], error: ErrorReporter) -> GMDMesh:
        material = materials[self.material_idx]
        layer_names = AttribSetLayerNames.build_from(material.shader.vertex_buffer_layout, is_skinned=False)
        layers = layer_names.try_retrieve_from(mesh, error)

        vertices = GMDVertexBuffer.build_empty(material.shader.vertex_buffer_layout, len(self.loops))

        self._extract_pos(mesh, vertices.pos)
        if vertices.normal is not None:
            self._extract_normals(mesh, layers.normal_w_layer, vertices.normal)
        if vertices.tangent is not None:
            if layers.tangent_layer is not None:
                self._extract_tangents_from_layer(layers.tangent_layer, vertices.tangent)
            else:
                self._extract_tangents_from_mesh(mesh, layers.tangent_w_layer, vertices.tangent)
        # TODO loll we literally don't do anything for unk
        if vertices.unk is not None:
            error.recoverable(f"Mesh {mesh}/shader {material.shader} uses an unknown vertex field. "
                              f"The exporter does not handle this field, and it will default to all zeros. "
                              f"If this is OK, disable Strict Export.")
        if vertices.bone_data is not None:
            self._extract_bones_from_layer(layers.bone_data_layer, vertices.bone_data)
        if vertices.weight_data is not None:
            self._extract_from_color(layers.weight_data_layer, vertices.weight_data)
        if vertices.col0 is not None:
            self._extract_from_color(layers.col0_layer, vertices.col0)
        if vertices.col1 is not None:
            self._extract_from_color(layers.col1_layer, vertices.col1)
        if len(vertices.uvs) != len(layers.uv_layers):
            error.recoverable(
                f"Shader {material.shader} expected {len(vertices.uvs)} UV layers but found {len(layers.uv_layers)}. "
                f"Layers that were not found will be filled with 0, and extra layers will be ignored. "
                f"If this is OK, disable Strict Export")
        for (i, (comp_count, uv_layer)) in enumerate(layers.uv_layers):
            self._extract_uv(i, comp_count, uv_layer, vertices.uvs[i], error)

        triangle_list, triangle_strip_noreset, triangle_strip_reset = self._build_triangles()

        return GMDMesh(
            empty=False,
            vertices_data=vertices,
            triangle_indices=triangle_list,
            triangle_strip_noreset_indices=triangle_strip_noreset,
            triangle_strip_reset_indices=triangle_strip_reset,
            attribute_set=material
        )

    # Build the triangle strip from self.triangles
    def _build_triangles(self) -> Tuple[array.ArrayType, array.ArrayType, array.ArrayType]:
        triangle_list = array.array("H")
        triangle_strip_noreset = array.array("H")
        triangle_strip_reset = array.array("H")

        for t0, t1, t2 in self.triangles:
            triangle_list.append(t0)
            triangle_list.append(t1)
            triangle_list.append(t2)

            # If we can continue the strip, do so
            if not triangle_strip_noreset:
                # Starting the strip
                triangle_strip_noreset.append(t0)
                triangle_strip_noreset.append(t1)
                triangle_strip_noreset.append(t2)
            elif (triangle_strip_noreset[-2] == t0 and
                  triangle_strip_noreset[-1] == t1):
                # Continue the strip
                triangle_strip_noreset.append(t2)
            else:
                # End previous strip, start new strip
                # Two extra verts to create a degenerate triangle, signalling the end of the strip
                triangle_strip_noreset.append(triangle_strip_noreset[-1])
                triangle_strip_noreset.append(t0)
                # Add the triangle as normal
                triangle_strip_noreset.append(t0)
                triangle_strip_noreset.append(t1)
                triangle_strip_noreset.append(t2)

            # If we can continue the strip, do so
            if not triangle_strip_reset:
                # Starting the strip
                triangle_strip_reset.append(t0)
                triangle_strip_reset.append(t1)
                triangle_strip_reset.append(t2)
            elif (triangle_strip_reset[-2] == t0 and
                  triangle_strip_reset[-1] == t1):
                # Continue the strip
                triangle_strip_reset.append(t2)
            else:
                # End previous strip, start new strip
                # Reset index signalling the end of the strip
                triangle_strip_reset.append(0xFFFF)
                # Add the triangle as normal
                triangle_strip_reset.append(t0)
                triangle_strip_reset.append(t1)
                triangle_strip_reset.append(t2)

        return triangle_list, triangle_strip_noreset, triangle_strip_reset

    def _extract_pos(self, mesh: bpy.types.Mesh, data: np.ndarray):
        for (i, loop_idx) in enumerate(self.loops):
            pos = mesh.vertices[mesh.loops[loop_idx].vertex_index].co
            # Hardcoded (-x, z, y) transposition to go into GMD space
            data[i, 0] = -pos[0]
            data[i, 1] = pos[2]
            data[i, 2] = pos[1]
            # data[i, 3] = 0

    def _extract_normals(self, mesh: bpy.types.Mesh, normal_w_layer: Optional[bpy.types.FloatColorAttribute],
                         data: np.ndarray):
        # Pull normal XYZ data out of the mesh loops
        for (i, loop_idx) in enumerate(self.loops):
            n = mesh.loops[loop_idx].normal
            # Hardcoded (-x, z, y) transposition to go into GMD space
            data[i, 0] = -n[0]
            data[i, 1] = n[2]
            data[i, 2] = n[1]
            # TODO the old version normalized the normals here?
            # If we have a W layer, pull the value out of that too. Otherwise it's zero-initialized
            if normal_w_layer:
                data[i, 3] = (normal_w_layer.data[loop_idx].color[0] * 2) - 1

    def _extract_tangents_from_layer(self, tangent_layer: Optional[bpy.types.FloatColorAttribute], data: np.ndarray):
        if tangent_layer is None:
            return  # Data is zero-initialized

        # Copy raw data (in 0..1 range)
        for (i, loop_idx) in enumerate(self.loops):
            # TODO watch out for what happens if data[i] has <4 components
            data[i] = tangent_layer.data[loop_idx].color
        # Correct data for (-1..1) range
        data *= 2
        data -= 1

    def _extract_tangents_from_mesh(self, mesh: bpy.types.Mesh,
                                    tangent_w_layer: Optional[bpy.types.FloatColorAttribute], data: np.ndarray):
        # Pull normal XYZ data out of the mesh loops
        for (i, loop_idx) in enumerate(self.loops):
            t = mesh.loops[loop_idx].tangent
            # Hardcoded (-x, z, y) transposition to go into GMD space
            data[i, 0] = -t[0]
            data[i, 1] = t[2]
            data[i, 2] = t[1]
            # If we have a W layer, pull the value out of that too. Otherwise it's zero-initialized
            if tangent_w_layer:
                data[i, 3] = (tangent_w_layer.data[loop_idx].color[0] * 2) - 1

    def _extract_from_color(self, col_layer: Optional[bpy.types.FloatColorAttribute], data: np.ndarray):
        if col_layer is None:
            # Default colors to (1,1,1,1)
            data.fill(1)
        else:
            # Fill in the colors
            for (i, loop_idx) in enumerate(self.loops):
                # TODO watch out for what happens if data[i] has <4 components
                data[i] = col_layer.data[loop_idx].color

    def _extract_bones_from_layer(self, bone_data_layer: Optional[bpy.types.FloatColorAttribute], data: np.ndarray):
        if bone_data_layer is None:
            # Bone data will be zero inited
            return
        for (i, loop_idx) in enumerate(self.loops):
            # TODO this is a hack. This assumes the bonedata is always a byte-value.
            # We should change this so that self.layers actually looks at the associated storage and decides how to encode/decode to 0.1.
            # data[i] is of type uint8, => we have to premultiply to get into the 0..255 range before storing
            color = bone_data_layer.data[loop_idx].color
            data[i, 0] = color[0] * 255
            data[i, 1] = color[1] * 255
            data[i, 2] = color[2] * 255
            data[i, 3] = color[3] * 255

    def _extract_uv(self, uv_idx: int, comp_count: int,
                    uv_layer: Union[bpy.types.MeshUVLoopLayer, bpy.types.FloatColorAttribute], data: np.ndarray,
                    error: ErrorReporter):
        if uv_layer is None:
            return  # UVs default to 0
        # If component_count == 2 then we should be storing it in a UV layer.
        # For backwards compatibility, check if the layer actually has a "uv" section
        if comp_count == 2 and hasattr(uv_layer.data[0], "uv"):
            for (i, loop_idx) in enumerate(self.loops):
                data[i] = uv_layer.data[loop_idx].uv
            # Invert Y to go from blender -> GMD
            # NOTE this relies on storing the data as float32 - if it's stored as float16, we'd be doing (1 - f16(x))
            # instead of f16(1 - x), which is sometimes different.
            data[:, 1] = 1.0 - data[:, 1]
        else:
            for (i, loop_idx) in enumerate(self.loops):
                data[i] = uv_layer.data[loop_idx].color[:comp_count]
            if np.any((data < 0) | (data > 1)):
                error.recoverable(
                    f"UV{uv_idx} has values outside of 0 and 1. This should never happen.")


TSubmesh = TypeVar("TSubmesh", bound=Submesh)


def convert_meshloop_tris_to_tsubmeshes(
        loops: List[MeshLoopIdx],
        triangles: List[Tuple[int, int, int]],
        submesh_generator: Callable[
            [
                List[MeshLoopIdx],
                List[Tuple[int, int, int]]
            ],
            TSubmesh
        ]
) -> List[TSubmesh]:
    submeshes = []

    toplevel_vert_to_pending_vert_idx: Dict[MeshLoopIdx, int] = {}
    pending_loops: List[MeshLoopIdx] = []
    pending_tris: List[Tuple[int, int, int]] = []

    def get_or_insert_pending_vert(vert: MeshLoopIdx) -> int:
        nonlocal pending_loops, pending_tris, toplevel_vert_to_pending_vert_idx
        idx = toplevel_vert_to_pending_vert_idx.get(vert)
        if idx is None:
            idx = len(pending_loops)
            toplevel_vert_to_pending_vert_idx[vert] = idx
            pending_loops.append(vert)
        return idx

    def push_submesh_and_reset_pending():
        nonlocal pending_loops, pending_tris, toplevel_vert_to_pending_vert_idx
        submeshes.append(submesh_generator(pending_loops, pending_tris))
        pending_loops = []
        pending_tris = []
        toplevel_vert_to_pending_vert_idx = {}

    for t in triangles:
        # We have a maximum of 65536 vertices.
        # At most, adding a new triangle can only add 3 loops to the "pending" buffer.
        # also, adding a triangle may add 0 loops - if they're all used already.
        # So if we have 65533 loops, check to see how many we would add.
        if len(pending_loops) >= (65536 - 3):
            # We have to be careful, we might grow beyond the buffer
            num_to_add = 0
            if loops[t[0]] not in toplevel_vert_to_pending_vert_idx:
                num_to_add += 1
            if loops[t[1]] not in toplevel_vert_to_pending_vert_idx:
                num_to_add += 1
            if loops[t[2]] not in toplevel_vert_to_pending_vert_idx:
                num_to_add += 1
            if len(pending_loops) + num_to_add > 65536:
                # Push the current loops into a Submesh struct and reset the pending
                push_submesh_and_reset_pending()
        # We can add any triangle to the buffer, it's guaranteed to result in a buffer with <65536 loops
        pending_tris.append((
            get_or_insert_pending_vert(loops[t[0]]),
            get_or_insert_pending_vert(loops[t[1]]),
            get_or_insert_pending_vert(loops[t[2]]),
        ))

    if pending_loops or pending_tris:
        push_submesh_and_reset_pending()

    return submeshes


def convert_meshloop_tris_to_unskinned_submeshes(
        loops: List[MeshLoopIdx],
        triangles: List[Tuple[int, int, int]],
        material_idx: int
) -> List[Submesh]:
    return convert_meshloop_tris_to_tsubmeshes(
        loops,
        triangles,
        lambda loops, triangles: Submesh(loops, triangles, material_idx=material_idx)
    )


@dataclass(frozen=True)
class SkinnedSubmesh(Submesh):
    """
    A submesh with extra data for skinning e.g. vertex groups.
    """
    # A mapping of (blender vertex group) -> (local bone index).
    relevant_vertex_groups: Dict[int, int]

    def build_skinned(self, mesh: bpy.types.Mesh, bone_info: Tuple[np.ndarray, np.ndarray, np.ndarray],
                      materials: List[GMDAttributeSet], error: ErrorReporter) -> GMDSkinnedMesh:
        material = materials[self.material_idx]
        layer_names = AttribSetLayerNames.build_from(material.shader.vertex_buffer_layout, is_skinned=True)
        layers = layer_names.try_retrieve_from(mesh, error)

        vertices = GMDSkinnedVertexBuffer.build_empty(material.shader.vertex_buffer_layout, len(self.loops))

        if vertices.normal is not None:
            self._extract_normals(mesh, layers.normal_w_layer, vertices.normal)
        if vertices.tangent is not None:
            if layers.tangent_layer is not None:
                self._extract_tangents_from_layer(layers.tangent_layer, vertices.tangent)
            else:
                self._extract_tangents_from_mesh(mesh, layers.tangent_w_layer, vertices.tangent)
        # TODO loll we literally don't do anything for unk
        if vertices.unk is not None:
            error.recoverable(f"Mesh {mesh}/shader {material.shader} uses an unknown vertex field. "
                              f"The exporter does not handle this field, and it will default to all zeros. "
                              f"If this is OK, disable Strict Export.")
        assert vertices.bone_data is not None
        assert vertices.weight_data is not None
        self._extract_boneweights(bone_info, vertices.bone_data, vertices.weight_data)
        if vertices.col0 is not None:
            self._extract_from_color(layers.col0_layer, vertices.col0)
        if vertices.col1 is not None:
            self._extract_from_color(layers.col1_layer, vertices.col1)
        if len(vertices.uvs) != len(layers.uv_layers):
            error.recoverable(
                f"Shader {material.shader} expected {len(vertices.uvs)} UV layers but found {len(layers.uv_layers)}. "
                f"Layers that were not found will be filled with 0, and extra layers will be ignored. "
                f"If this is OK, disable Strict Export")
        for (i, (comp_count, uv_layer)) in enumerate(layers.uv_layers):
            self._extract_uv(i, comp_count, uv_layer, vertices.uvs[i], error)

        triangle_list, triangle_strip_noreset, triangle_strip_reset = self._build_triangles()

        return GMDSkinnedMesh(
            empty=False,
            vertices_data=vertices,
            triangle_indices=triangle_list,
            triangle_strip_noreset_indices=triangle_strip_noreset,
            triangle_strip_reset_indices=triangle_strip_reset,
            attribute_set=material
        )

    def _extract_boneweights(self, bone_info: Tuple[np.ndarray, np.ndarray, np.ndarray],
                             bone_data: np.ndarray, weight_data: np.ndarray):
        # See compute_vertex_4weights
        original_bones, weights, n_weights = bone_info
        weight_data[:] = weights.take(self.loops)
        for (i, loop_idx) in enumerate(self.loops):
            # Remap the bone only for the first N bones it uses.
            # All others are 0
            for b_i in range(n_weights[loop_idx]):
                bone_data[i, b_i] = self.relevant_vertex_groups[original_bones[loop_idx, b_i]]


def convert_meshloop_tris_to_skinned_submeshes(
        mesh: bpy.types.Mesh,
        loops: List[MeshLoopIdx],
        triangles: List[Tuple[int, int, int]],
        material_idx: int,
        bone_info: Tuple[np.ndarray, np.ndarray, np.ndarray],
        error: ErrorReporter,
        max_bones_per_submesh=32,
) -> List[SkinnedSubmesh]:
    if max_bones_per_submesh < 12:
        error.fatal(f"Specified MAX_BONES_PER_SUBMESH={max_bones_per_submesh}, which is impossible. "
                    f"A triangle can reference up to 12 bones (3 verts * 4 bones per vert).")

    vert_groups, weights, n_weights = bone_info

    def find_triangle_vertex_groups(t: Tuple[int, int, int]) -> Set[int]:
        v0 = mesh.loops[loops[t[0]]].vertex_index
        v1 = mesh.loops[loops[t[1]]].vertex_index
        v2 = mesh.loops[loops[t[2]]].vertex_index

        vgs = set(vert_groups[v0, 0:n_weights[v0]])
        vgs.update(vert_groups[v1, 0:n_weights[v1]])
        vgs.update(vert_groups[v2, 0:n_weights[v2]])
        return vgs

    # First, partition the triangles into groups that use at most max_bones_per_submesh bones.
    triangle_partitions: List[Tuple[
        List[Tuple[int, int, int]],  # A group of triangles
        Set[int]  # the vertex groups they reference
    ]] = []
    pending_tris: List[Tuple[int, int, int]] = []
    pending_vgs: Set[int] = set()
    for t in triangles:
        triangle_vgs = find_triangle_vertex_groups(t)
        combined_vgs = triangle_vgs.union(pending_vgs)

        if len(combined_vgs) > max_bones_per_submesh:
            triangle_partitions.append((pending_tris, pending_vgs))
            pending_tris = [t]
            pending_vgs = triangle_vgs
        else:
            pending_tris.append(t)
            pending_vgs = combined_vgs
    if pending_tris or pending_vgs:
        triangle_partitions.append((pending_tris, pending_vgs))

    skinned_submeshes: List[SkinnedSubmesh] = []
    for tri_partition, referenced_vgs in triangle_partitions:
        assert len(referenced_vgs) <= max_bones_per_submesh
        relevant_vertex_groups = {
            vg: i
            for (i, vg) in enumerate(referenced_vgs)
        }
        skinned_submeshes += convert_meshloop_tris_to_tsubmeshes(
            loops,
            tri_partition,
            lambda loops, triangles: SkinnedSubmesh(loops, triangles, material_idx=material_idx,
                                                    relevant_vertex_groups=relevant_vertex_groups)
        )

    return skinned_submeshes
