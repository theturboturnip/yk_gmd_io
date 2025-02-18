import dataclasses
from typing import List, Tuple, Optional, Union, Set, Mapping

import numpy as np

import bpy
from ...common import AttribSetLayerNames
from ....gmdlib.abstract.gmd_attributes import GMDAttributeSet
from ....gmdlib.abstract.gmd_shader import GMDVertexBuffer, GMDSkinnedVertexBuffer, VecStorage, VecCompFmt
from ....gmdlib.errors.error_reporter import ErrorReporter
from ....meshlib.export_submeshing import MeshLoopIdx


def generate_vertex_byteslices(vertex_buffer: GMDVertexBuffer, big_endian: bool) -> List[bytes]:
    """
    Given a vertex buffer, generate packed bytes for each vertex.
    This can be used for easy (maybe not fast?) deduplication
    """
    # TODO we really should be able to reuse the packed bytes
    vertex_bytes = bytearray()
    vertex_buffer.layout.pack_into(big_endian, vertex_buffer, vertex_bytes)
    vertex_stride = vertex_buffer.layout.bytes_per_vertex()
    return [
        bytes(vertex_bytes[vertex_off:vertex_off + vertex_stride])
        for vertex_off in range(0, len(vertex_bytes), vertex_stride)
    ]


def loop_indices_for_material(mesh: bpy.types.Mesh, material_idx: int) -> List[MeshLoopIdx]:
    """
    Given a mesh and a material index, return a List of the mesh loop indices which are related to that material
    with index-based deduplication (i.e. index i does not appear twice in the list) but no data-based deduplication
    """
    loop_set: Set[MeshLoopIdx] = set()

    for t in mesh.loop_triangles:
        if t.material_index == material_idx:
            loop_set.add(MeshLoopIdx(t.loops[0]))
            loop_set.add(MeshLoopIdx(t.loops[1]))
            loop_set.add(MeshLoopIdx(t.loops[2]))

    return list(loop_set)


def extract_vertices_for_unskinned_material(mesh: bpy.types.Mesh, attr_set: GMDAttributeSet,
                                            loops: List[MeshLoopIdx],
                                            error: ErrorReporter) -> GMDVertexBuffer:
    assert not attr_set.shader.assume_skinned

    layer_names = AttribSetLayerNames.build_from(attr_set.shader.vertex_buffer_layout, is_skinned=False)
    layers = layer_names.try_retrieve_from(mesh, error)

    vertices = GMDVertexBuffer.build_empty(attr_set.shader.vertex_buffer_layout, len(loops))

    _extract_pos(loops, mesh, vertices.pos)
    if vertices.normal is not None:
        _extract_normals(loops, mesh, layers.normal_w_layer, vertices.normal)
    if vertices.tangent is not None:
        if layers.tangent_layer is not None:
            _extract_tangents_from_layer(loops, layers.tangent_layer, vertices.tangent)
        else:
            _extract_tangents_from_mesh(loops, mesh, layers.tangent_w_layer, vertices.tangent)
    # TODO loll we literally don't do anything for unk
    if vertices.unk is not None:
        error.recoverable(f"Mesh {mesh}/shader {attr_set.shader} uses an unknown vertex field. "
                          f"The exporter does not handle this field, and it will default to all zeros. "
                          f"If this is OK, disable Strict Export.")
    if vertices.bone_data is not None:
        _extract_bones_from_layer(loops, layers.bone_data_layer, vertices.bone_data)
    if vertices.weight_data is not None:
        _extract_from_color(loops, layers.weight_data_layer, vertices.weight_data)
    if vertices.col0 is not None:
        _extract_from_color(loops, layers.col0_layer, vertices.col0)
    if vertices.col1 is not None:
        _extract_from_color(loops, layers.col1_layer, vertices.col1)
    if len(vertices.uvs) != len(layers.uv_layers):
        error.recoverable(
            f"Shader {attr_set.shader} expected {len(vertices.uvs)} UV layers but found {len(layers.uv_layers)}. "
            f"Layers that were not found will be filled with 0, and extra layers will be ignored. "
            f"If this is OK, disable Strict Export")
    for (i, (comp_count, uv_layer)) in enumerate(layers.uv_layers):
        _extract_uv(loops, i, comp_count, uv_layer, vertices.uvs[i], error)

    return vertices


def extract_vertices_for_skinned_material(mesh: bpy.types.Mesh, attr_set: GMDAttributeSet,
                                          loops: List[MeshLoopIdx],
                                          bone_info: Tuple[np.ndarray, np.ndarray, np.ndarray],
                                          error: ErrorReporter,
                                          bone_remapper: Optional[Mapping[int, int]] = None) -> GMDSkinnedVertexBuffer:
    assert attr_set.shader.assume_skinned

    layer_names = AttribSetLayerNames.build_from(attr_set.shader.vertex_buffer_layout, is_skinned=True)
    layers = layer_names.try_retrieve_from(mesh, error)

    if bone_remapper is None:
        # We may need to store more than 255 bone indices in this larger buffer.
        # => replace the bones layout with one that uses 16-bit uints.
        layout = dataclasses.replace(
            attr_set.shader.vertex_buffer_layout,
            bones_storage=VecStorage(VecCompFmt.U16, 4)
        )
    else:
        layout = attr_set.shader.vertex_buffer_layout

    vertices = GMDSkinnedVertexBuffer.build_empty(layout, len(loops))

    _extract_pos(loops, mesh, vertices.pos)
    if vertices.normal is not None:
        _extract_normals(loops, mesh, layers.normal_w_layer, vertices.normal)
    if vertices.tangent is not None:
        if layers.tangent_layer is not None:
            _extract_tangents_from_layer(loops, layers.tangent_layer, vertices.tangent)
        else:
            _extract_tangents_from_mesh(loops, mesh, layers.tangent_w_layer, vertices.tangent)
    # TODO loll we literally don't do anything for unk
    if vertices.unk is not None:
        error.recoverable(f"Mesh {mesh}/shader {attr_set.shader} uses an unknown vertex field. "
                          f"The exporter does not handle this field, and it will default to all zeros. "
                          f"If this is OK, disable Strict Export.")
    assert vertices.bone_data is not None
    assert vertices.weight_data is not None
    _extract_skinned_boneweights(loops, mesh, bone_info, bone_remapper, vertices.bone_data, vertices.weight_data)
    if vertices.col0 is not None:
        _extract_from_color(loops, layers.col0_layer, vertices.col0)
    if vertices.col1 is not None:
        _extract_from_color(loops, layers.col1_layer, vertices.col1)
    if len(vertices.uvs) != len(layers.uv_layers):
        error.recoverable(
            f"Shader {attr_set.shader} expected {len(vertices.uvs)} UV layers but found {len(layers.uv_layers)}. "
            f"Layers that were not found will be filled with 0, and extra layers will be ignored. "
            f"If this is OK, disable Strict Export")
    for (i, (comp_count, uv_layer)) in enumerate(layers.uv_layers):
        _extract_uv(loops, i, comp_count, uv_layer, vertices.uvs[i], error)

    return vertices


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

    # In very rare cases blender has spit out vertex groups where g.weight = 0.
    # Elsewhere we use .weight = 0 to imply "no group", so use a threshold value here to prevent this.
    MIN_WEIGHT = 1.0 / 255.0

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
                if g.group in relevant_vertex_groups and g.weight >= MIN_WEIGHT
            ],
            key=lambda g: g.weight,
            reverse=True
        )

        # Check if weights are greater than 1 or lower than 0
        if any(g.weight > 1 for g in v.groups) and not has_warned_about_weights_over_one:
            error.recoverable(f"Some weights in mesh {mesh.name} are greater than 1. "
                              f"These can't be exported - try normalizing your weights, or turn off Strict Export "
                              f"to clamp it to 1")
            has_warned_about_weights_over_one = True
        if any(g.weight < 0 for g in v.groups):
            error.fatal(f"Some weights in mesh {mesh.name} are smaller than 0 - this is impossible to export.")

        # For each of the top four elements of bws, push it into bones/weights
        for i in range(min(4, len(gs))):
            weights[v.index, i] = min(1.0, gs[i].weight)
            # Check after putting it in the ndarray that it still isn't 0, because it might have been rounded down
            # inside the precision of uint8.
            # This will ensure the invariant that weights[v.index, i] == 0 directly implies
            # - bones[v.index, i] = 0
            # - n_weights[v.index] <= i (i.e. iterating through range(n_weights[v.index]) will not produce i)
            if weights[v.index, i] > 0:
                bones[v.index, i] = gs[i].group
                n_weights[v.index] = i + 1

        # Sanity checks for meshes with more than 4 ""major"" influences.
        if len(gs) > 4 and any(g.weight > 0.1 for g in gs[4:]):
            error.recoverable(f"Some vertices in mesh {mesh.name} have more than 4 major influences. "
                              f"A major influence is a bone with weight greater than 0.1. "
                              f"The exporter can only export 4 influences per vertex, so animation on this model may "
                              f"look odd. Turn off Strict Export if this is acceptable.")

    return bones, weights, n_weights


def _extract_pos(loops: List[MeshLoopIdx], mesh: bpy.types.Mesh, data: np.ndarray):
    for (i, loop_idx) in enumerate(loops):
        pos = mesh.vertices[mesh.loops[loop_idx].vertex_index].co
        # Hardcoded (-x, z, y) transposition to go into GMD space
        data[i, 0] = -pos[0]
        data[i, 1] = pos[2]
        data[i, 2] = pos[1]
        # data[i, 3] = 0


def _extract_normals(loops: List[MeshLoopIdx], mesh: bpy.types.Mesh,
                     normal_w_layer: Optional[bpy.types.FloatColorAttribute],
                     data: np.ndarray):
    # Pull normal XYZ data out of the mesh loops
    for (i, loop_idx) in enumerate(loops):
        n = mesh.loops[loop_idx].normal
        # Hardcoded (-x, z, y) transposition to go into GMD space
        data[i, 0] = -n[0]
        data[i, 1] = n[2]
        data[i, 2] = n[1]
        # TODO the old version normalized the normals here?
        # If we have a W layer, pull the value out of that too. Otherwise it's zero-initialized
        if normal_w_layer:
            data[i, 3] = (normal_w_layer.data[loop_idx].color[0] * 2) - 1


def _extract_tangents_from_layer(loops: List[MeshLoopIdx], tangent_layer: Optional[bpy.types.FloatColorAttribute],
                                 data: np.ndarray):
    if tangent_layer is None:
        return  # Data is zero-initialized

    # Copy raw data (in 0..1 range)
    for (i, loop_idx) in enumerate(loops):
        # TODO watch out for what happens if data[i] has <4 components
        data[i] = tangent_layer.data[loop_idx].color
    # Correct data for (-1..1) range
    data *= 2
    data -= 1


def _extract_tangents_from_mesh(loops: List[MeshLoopIdx], mesh: bpy.types.Mesh,
                                tangent_w_layer: Optional[bpy.types.FloatColorAttribute], data: np.ndarray):
    # Pull normal XYZ data out of the mesh loops
    for (i, loop_idx) in enumerate(loops):
        t = mesh.loops[loop_idx].tangent
        # Hardcoded (-x, z, y) transposition to go into GMD space
        data[i, 0] = -t[0]
        data[i, 1] = t[2]
        data[i, 2] = t[1]
        # If we have a W layer, pull the value out of that too. Otherwise it's zero-initialized
        if tangent_w_layer:
            data[i, 3] = (tangent_w_layer.data[loop_idx].color[0] * 2) - 1


def _extract_from_color(loops: List[MeshLoopIdx], col_layer: Optional[bpy.types.FloatColorAttribute], data: np.ndarray):
    if col_layer is None:
        # Default colors to (1,1,1,1)
        data.fill(1)
    else:
        # Fill in the colors
        for (i, loop_idx) in enumerate(loops):
            # TODO watch out for what happens if data[i] has <4 components
            data[i] = col_layer.data[loop_idx].color


def _extract_bones_from_layer(loops: List[MeshLoopIdx], bone_data_layer: Optional[bpy.types.FloatColorAttribute],
                              data: np.ndarray):
    if bone_data_layer is None:
        # Bone data will be zero inited
        return
    for (i, loop_idx) in enumerate(loops):
        # TODO this is a hack. This assumes the bonedata is always a byte-value.
        # We should change this so that self.layers actually looks at the associated storage and decides how to encode/decode to 0.1.
        # data[i] is of type uint8, => we have to premultiply to get into the 0..255 range before storing
        color = bone_data_layer.data[loop_idx].color
        data[i, 0] = color[0] * 255
        data[i, 1] = color[1] * 255
        data[i, 2] = color[2] * 255
        data[i, 3] = color[3] * 255


def _extract_uv(loops: List[MeshLoopIdx], uv_idx: int, comp_count: int,
                uv_layer: Union[bpy.types.MeshUVLoopLayer, bpy.types.FloatColorAttribute], data: np.ndarray,
                error: ErrorReporter):
    if uv_layer is None:
        return  # UVs default to 0
    # If component_count == 2 then we should be storing it in a UV layer.
    # For backwards compatibility, check if the layer actually has a "uv" section
    if comp_count == 2 and hasattr(uv_layer.data[0], "uv"):
        for (i, loop_idx) in enumerate(loops):
            data[i] = uv_layer.data[loop_idx].uv
        # Invert Y to go from blender -> GMD
        # NOTE this relies on storing the data as float32 - if it's stored as float16, we'd be doing (1 - f16(x))
        # instead of f16(1 - x), which is sometimes different.
        data[:, 1] = 1.0 - data[:, 1]
    else:
        for (i, loop_idx) in enumerate(loops):
            data[i] = uv_layer.data[loop_idx].color[:comp_count]
        if np.any((data < 0) | (data > 1)):
            error.recoverable(
                f"UV{uv_idx} has values outside of 0 and 1. This should never happen.")


def _extract_skinned_boneweights(loops: List[MeshLoopIdx], mesh: bpy.types.Mesh,
                                 bone_info: Tuple[np.ndarray, np.ndarray, np.ndarray],
                                 bone_remapper: Optional[Mapping[int, int]],
                                 bone_data: np.ndarray, weight_data: np.ndarray):
    bones, weights, n_weights = bone_info

    vertices = [mesh.loops[l].vertex_index for l in loops]
    weight_data[:] = weights[vertices, :]
    unmapped_bones = bones[vertices, :]
    if bone_remapper is None:
        np.copyto(bone_data, unmapped_bones, casting="safe")
    else:
        # Where vertices.weight_data > 0, remap vertices.bone_data with self.relevant_vertex_groups
        for i in range(len(vertices)):
            for j in range(4):
                if weight_data[i, j] > 0:
                    bone_data[i, j] = bone_remapper[unmapped_bones[i, j]]
                # Other bone_data elements are 0-initialized
