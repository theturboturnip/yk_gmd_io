import array
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
from typing import cast

import numpy as np

import bpy
from yk_gmd_blender.blender.export.mesh_exporter.extractor import compute_vertex_4weights, loop_indices_for_material, \
    extract_vertices_for_skinned_material, generate_vertex_byteslices, \
    extract_vertices_for_unskinned_material
from yk_gmd_blender.meshlib.export_submeshing import dedupe_loops, \
    convert_meshloop_tris_to_tsubmeshes, MeshLoopTri, \
    MeshLoopIdx, DedupedVertIdx, SubmeshTri
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDSkinnedMesh, GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDSkinnedVertexBuffer
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

    bone_info = compute_vertex_4weights(mesh, relevant_vertex_groups=set(vertex_group_mapping.keys()), error=error)

    error.debug("MESH", f"Exporting skinned meshes for {object.name}")
    skinned_submeshes: List[SkinnedSubmesh] = []

    for (attr_set_idx, attr_set) in enumerate(materials):
        # Get the set of MeshLoopIdxs that are related to this material
        loops_with_dupes = loop_indices_for_material(mesh, attr_set_idx)
        # Generate a vertex buffer with data for all of them
        # Set want_expanded so we get 16-bit bone buffers, which is necessary in case more than 255 bones are relevant
        base_vertices = extract_vertices_for_skinned_material(mesh, attr_set, loops_with_dupes, bone_info, error)
        # Convert them to bytes and deduplicate them
        vertex_bytes = generate_vertex_byteslices(base_vertices, big_endian=False)
        deduped_verts, loop_idx_to_deduped_verts_idx = dedupe_loops(loops_with_dupes, vertex_bytes)
        # Generate the submeshes
        skinned_submeshes += convert_meshloop_tris_to_skinned_submeshes(
            # Basic info included in every generated submesh
            attr_set,
            base_vertices,
            # The mesh, so it can determine the vertex groups for each triangle
            mesh,
            # Deduped verts and associated mapping from mesh loops
            deduped_verts,
            loop_idx_to_deduped_verts_idx,
            # Relevant triangles
            [MeshLoopTri(t.loops) for t in mesh.loop_triangles if t.material_index == attr_set_idx],
            # Per-mesh bone info TODO should use this instead of mesh
            bone_info,
            vertex_group_mapping,
            # Error reporting
            error,
            # Config
            max_bones_per_submesh=bone_limit
        )

    return [s.build_skinned(mesh, bone_info, error) for s in skinned_submeshes]


def split_unskinned_blender_mesh_object(context: bpy.types.Context, object: bpy.types.Object,
                                        materials: List[GMDAttributeSet], error: ErrorReporter) -> List[GMDMesh]:
    mesh = prepare_mesh(context, object, check_needs_tangent(materials))

    error.debug("MESH", f"Exporting unskinned meshes for {object.name}")
    submeshes: List[Submesh] = []
    for (attr_set_idx, attr_set) in enumerate(materials):
        # Get the set of MeshLoopIdxs that are related to this material
        loops_with_dupes = loop_indices_for_material(mesh, attr_set_idx)
        # Generate a vertex buffer with data for all of them
        base_vertices = extract_vertices_for_unskinned_material(mesh, attr_set, loops_with_dupes, error)
        # Convert them to bytes and deduplicate them
        vertex_bytes = generate_vertex_byteslices(base_vertices, big_endian=False)
        deduped_verts, loop_idx_to_deduped_verts_idx = dedupe_loops(loops_with_dupes, vertex_bytes)
        # Generate the submeshes
        submeshes += convert_meshloop_tris_to_unskinned_submeshes(
            attr_set,
            deduped_verts,
            loop_idx_to_deduped_verts_idx,
            [MeshLoopTri(t.loops) for t in mesh.loop_triangles if t.material_index == attr_set_idx],
        )

    return [s.build_unskinned(mesh, error) for s in submeshes]


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


@dataclass(frozen=True)
class Submesh:
    """
    A "submesh" - a minimally exportable chunk of a mesh.
    Contains at most 65536 "vertices".
    """

    # The material for the submesh
    attr_set: GMDAttributeSet
    # Indices of the data to turn into vertices.
    verts: List[MeshLoopIdx]
    # Triangle definitions, with indexes *that index into self.meshloop_idxs*
    triangles: List[SubmeshTri]

    def __post_init__(self):
        if len(self.verts) > 65536:
            raise RuntimeError("Created a Submesh with more than 65536 vertices.")

    def build_unskinned(self, mesh: bpy.types.Mesh, error: ErrorReporter) -> GMDMesh:
        vertices = extract_vertices_for_unskinned_material(mesh, self.attr_set, self.verts, error)

        triangle_list, triangle_strip_noreset, triangle_strip_reset = self._build_triangles()

        return GMDMesh(
            empty=False,
            vertices_data=vertices,
            triangle_indices=triangle_list,
            triangle_strip_noreset_indices=triangle_strip_noreset,
            triangle_strip_reset_indices=triangle_strip_reset,
            attribute_set=self.attr_set
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


def convert_meshloop_tris_to_unskinned_submeshes(
        attr_set: GMDAttributeSet,
        deduped_verts: List[MeshLoopIdx],
        loop_idx_to_deduped_verts_idx: Dict[MeshLoopIdx, DedupedVertIdx],
        triangles: List[MeshLoopTri],
) -> List[Submesh]:
    return convert_meshloop_tris_to_tsubmeshes(
        deduped_verts,
        loop_idx_to_deduped_verts_idx,
        triangles,
        lambda loops, triangles: Submesh(attr_set, loops, triangles)
    )


@dataclass(frozen=True)
class SkinnedSubmesh(Submesh):
    """
    A submesh with extra data for skinning e.g. vertex groups.
    """
    # A mapping of (blender vertex group) -> (local bone index).
    relevant_vertex_groups: Dict[int, int]
    # A mapping of (local bone index) -> (relevant GMD bone)
    relevant_bones: List[GMDBone]

    def build_skinned(self, mesh: bpy.types.Mesh,
                      bone_info: Tuple[np.ndarray, np.ndarray, np.ndarray],
                      error: ErrorReporter, ) -> GMDSkinnedMesh:
        vertices = extract_vertices_for_skinned_material(mesh, self.attr_set, self.verts, bone_info, error,
                                                         bone_remapper=self.relevant_vertex_groups)

        triangle_list, triangle_strip_noreset, triangle_strip_reset = self._build_triangles()

        return GMDSkinnedMesh(
            empty=False,
            vertices_data=vertices,
            triangle_indices=triangle_list,
            triangle_strip_noreset_indices=triangle_strip_noreset,
            triangle_strip_reset_indices=triangle_strip_reset,
            attribute_set=self.attr_set,
            relevant_bones=self.relevant_bones
        )


def convert_meshloop_tris_to_skinned_submeshes(
        attr_set: GMDAttributeSet,
        base_vertices: GMDSkinnedVertexBuffer,
        mesh: bpy.types.Mesh,
        deduped_verts: List[MeshLoopIdx],
        loop_idx_to_deduped_verts_idx: Dict[MeshLoopIdx, DedupedVertIdx],
        triangles: List[MeshLoopTri],
        bone_info: Tuple[np.ndarray, np.ndarray, np.ndarray],
        vertex_group_mapping: Dict[int, GMDBone],
        error: ErrorReporter,
        max_bones_per_submesh=32,
) -> List[SkinnedSubmesh]:
    if max_bones_per_submesh < 12:
        error.fatal(f"Specified MAX_BONES_PER_SUBMESH={max_bones_per_submesh}, which is impossible. "
                    f"A triangle can reference up to 12 bones (3 verts * 4 bones per vert).")

    vert_groups, weights, n_weights = bone_info

    def find_triangle_vertex_groups(t: MeshLoopTri) -> Set[int]:
        v0 = mesh.loops[t[0]].vertex_index
        v1 = mesh.loops[t[1]].vertex_index
        v2 = mesh.loops[t[2]].vertex_index

        vgs = set(vert_groups[v0, 0:n_weights[v0]])
        vgs.update(vert_groups[v1, 0:n_weights[v1]])
        vgs.update(vert_groups[v2, 0:n_weights[v2]])
        return vgs

    # First, partition the triangles into groups that use at most max_bones_per_submesh bones.
    # Don't remap the triangle indices yet
    triangle_partitions: List[Tuple[
        List[MeshLoopTri],  # A group of raw Blender triangles
        Set[int]  # the vertex groups they reference
    ]] = []
    pending_tris: List[MeshLoopTri] = []
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
        # Second, find the relevant vertex groups and bones for each partition
        assert len(referenced_vgs) <= max_bones_per_submesh
        relevant_vertex_groups = {
            vg: i
            for (i, vg) in enumerate(referenced_vgs)
        }
        relevant_bones = [
            vertex_group_mapping[vg]
            for vg in referenced_vgs
        ]
        expected_vgs: Set[int] = set()
        for t in tri_partition:
            expected_vgs.update(find_triangle_vertex_groups(t))
        assert referenced_vgs == expected_vgs
        # Then run convert_meshloop_tris_to_tsubmeshes to split meshes over the 65535 limit
        # and normalize the blender triangles
        skinned_submeshes += convert_meshloop_tris_to_tsubmeshes(
            deduped_verts,
            loop_idx_to_deduped_verts_idx,
            tri_partition,
            lambda loops, triangles: SkinnedSubmesh(attr_set, loops, triangles,
                                                    relevant_vertex_groups=relevant_vertex_groups,
                                                    relevant_bones=relevant_bones)
        )

    return skinned_submeshes
