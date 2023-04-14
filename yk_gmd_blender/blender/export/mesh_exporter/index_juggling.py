import array
from dataclasses import dataclass
from typing import List, Dict, Tuple, TypeVar, Callable, NewType

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDSkinnedMesh, GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer, GMDSkinnedVertexBuffer
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone

# Int alias representing indices into bpy.types.Mesh().loops
MeshLoopIdx = NewType("MeshLoopIdx", int)

# Alias representing a triangle indexed into bpy.types.Mesh().loops.
# Equivalent to (bpy.types.MeshLoopTriangle.loops) but doesn't need a blender import.
MeshLoopTri = NewType("MeshLoopTri", Tuple[MeshLoopIdx, MeshLoopIdx, MeshLoopIdx])

# Int alias representing offsets into material_vertices.
# When creating meshes, we first split them by material and generate a vertex buffer `material_vertices`
# with data for all loops associated with triangles associated with each material.
# This type represents an index into that vertex buffer.
MaterialVertIdx = NewType("MaterialVertIdx", int)

# Int alias representing offsets into the "deduped vertices" list.
# Once a vertex buffer has been created for each material,
# we "deduplicate" each buffer and create a canonical list deduped_verts: List[MaterialVertIdx]
# such that there are no two (i1, i2) in deduped_verts such that material_vertices[i1] == material_vertices[i2].
# This type represents an index into deduped_verts.
DedupedVertIdx = NewType("DedupedVertIdx", int)

# Int alias representing offsets into a submesh's vertices
# When splitting a mesh into submeshes, a subset of the total vertices are assigned to each submesh.
# The triangles for each submesh must use indices relative to that subset.
# This type represents an index into a submesh's vertex subset.
SubmeshVertIdx = NewType("SubmeshVertIdx", int)

# Alias representing a triangle indexed relative to a submesh
SubmeshTri = NewType("SubmeshTri", Tuple[SubmeshVertIdx, SubmeshVertIdx, SubmeshVertIdx])


def dedupe_loops(loops_with_dupes: List[MeshLoopIdx], vertex_bytes: List[bytes]) -> Tuple[
    List[MaterialVertIdx],
    Dict[MeshLoopIdx, DedupedVertIdx]
]:
    """
    Returns

    1. "deduped_verts" a list of indices into loops_with_dupes and vertex bytes, such that there are no two values
    (i1, i2) in the list where vertex_bytes[i1] == vertex_bytes[i2]
    2. a mapping of MeshLoopIdx -> index in exported_loops
    i.e. if vertex_bytes[0] == vertex_bytes[1] == vertex_bytes[2], and deduped_verts[x] == (0, 1, or 2)
    0, 1, and 2 map to x.
    This is useful because deduped_verts defines the layout of the final vertex buffer, so this mapping converts
    triangles in blender-index-space to per-material-index-space.
    """
    assert len(loops_with_dupes) == len(vertex_bytes)

    vertex_bytes_to_no_dupe_loop_idx: Dict[bytes, DedupedVertIdx] = {}

    deduped_verts: List[MaterialVertIdx] = []
    loop_idx_to_deduped_verts_idx: Dict[MeshLoopIdx, DedupedVertIdx] = {}
    for i, (loop_idx, vertex) in enumerate(zip(loops_with_dupes, vertex_bytes)):
        # See if this vertex data has already been encountered
        no_dupe_loop_idx = vertex_bytes_to_no_dupe_loop_idx.get(vertex)
        # If not, it's not a dupe - push it to deduped_verts and register in vertex_bytes_to...
        if no_dupe_loop_idx is None:
            no_dupe_loop_idx = DedupedVertIdx(len(deduped_verts))
            deduped_verts.append(MaterialVertIdx(i))
            vertex_bytes_to_no_dupe_loop_idx[vertex] = no_dupe_loop_idx
        # Either way, we now know where this mesh loop maps to inside deduped_verts
        loop_idx_to_deduped_verts_idx[loop_idx] = no_dupe_loop_idx

    return deduped_verts, loop_idx_to_deduped_verts_idx


@dataclass(frozen=True)
class Submesh:
    """
    A "submesh" - a minimally exportable chunk of a mesh.
    Contains at most 65536 "vertices".
    """

    # The material for the submesh
    attr_set: GMDAttributeSet
    # The buffer of all vertices for that material
    base_vertices: GMDVertexBuffer
    # Indices of the data to turn into vertices.
    verts: List[MaterialVertIdx]
    # Triangle definitions, with indexes *that index into self.meshloop_idxs*
    triangles: List[SubmeshTri]

    def __post_init__(self):
        if len(self.verts) > 65536:
            raise RuntimeError("Created a Submesh with more than 65536 vertices.")

    def build_unskinned(self) -> GMDMesh:
        vertices = self.base_vertices.copy_scatter(self.verts)

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


TSubmesh = TypeVar("TSubmesh", bound=Submesh)


def convert_meshloop_tris_to_tsubmeshes(
        deduped_verts: List[MaterialVertIdx],
        loop_idx_to_deduped_verts_idx: Dict[MeshLoopIdx, DedupedVertIdx],
        triangles: List[MeshLoopTri],
        submesh_generator: Callable[
            [
                List[MaterialVertIdx],
                List[SubmeshTri]
            ],
            TSubmesh
        ]
) -> List[TSubmesh]:
    submeshes = []

    deduped_verts_idx_to_pending_vert_idx: Dict[DedupedVertIdx, SubmeshVertIdx] = {}
    pending_verts: List[MaterialVertIdx] = []
    pending_tris: List[SubmeshTri] = []

    def get_or_insert_pending_vert(deduped_verts_idx: DedupedVertIdx) -> SubmeshVertIdx:
        nonlocal pending_verts, pending_tris, deduped_verts_idx_to_pending_vert_idx
        # See if this deduped vertex has already appeared in the pending submesh
        pending_idx = deduped_verts_idx_to_pending_vert_idx.get(deduped_verts_idx)
        if pending_idx is None:
            # if it hasn't, push it to pending_verts...
            pending_idx = SubmeshVertIdx(len(pending_verts))
            pending_verts.append(deduped_verts[deduped_verts_idx])
            # ... and register its index
            deduped_verts_idx_to_pending_vert_idx[deduped_verts_idx] = pending_idx
        # Either way, the deduped vert is definitely in the pending submesh now.
        return pending_idx

    def push_submesh_and_reset_pending():
        nonlocal pending_verts, pending_tris, deduped_verts_idx_to_pending_vert_idx
        submeshes.append(submesh_generator(pending_verts, pending_tris))
        pending_verts = []
        pending_tris = []
        deduped_verts_idx_to_pending_vert_idx = {}

    for t in triangles:
        t_no_dupes = (
            loop_idx_to_deduped_verts_idx[t[0]],
            loop_idx_to_deduped_verts_idx[t[1]],
            loop_idx_to_deduped_verts_idx[t[2]],
        )

        # We have a maximum of 65536 vertices.
        # At most, adding a new triangle can only add 3 loops to the "pending" buffer.
        # also, adding a triangle may add 0 loops - if they're all used already.
        # So if we have 65533 loops, check to see how many we would add.
        if len(pending_verts) >= (65536 - 3):
            # We have to be careful, we might grow beyond the buffer
            num_to_add = 0
            if deduped_verts[t_no_dupes[0]] not in deduped_verts_idx_to_pending_vert_idx:
                num_to_add += 1
            if deduped_verts[t_no_dupes[1]] not in deduped_verts_idx_to_pending_vert_idx:
                num_to_add += 1
            if deduped_verts[t_no_dupes[2]] not in deduped_verts_idx_to_pending_vert_idx:
                num_to_add += 1
            if len(pending_verts) + num_to_add > 65536:
                # Push the current loops into a Submesh struct and reset the pending
                push_submesh_and_reset_pending()
        # We can add any triangle to the buffer, it's guaranteed to result in a buffer with <65536 loops
        pending_tris.append(SubmeshTri((
            get_or_insert_pending_vert(t_no_dupes[0]),
            get_or_insert_pending_vert(t_no_dupes[1]),
            get_or_insert_pending_vert(t_no_dupes[2]),
        )))

    if pending_verts or pending_tris:
        push_submesh_and_reset_pending()

    if len(submeshes) > 2:
        print(f"WOOOOOO MANY ({len(submeshes)}) SUBMESHES")

    return submeshes


def convert_meshloop_tris_to_unskinned_submeshes(
        attr_set: GMDAttributeSet,
        base_vertices: GMDVertexBuffer,
        deduped_verts: List[MaterialVertIdx],
        loop_idx_to_deduped_verts_idx: Dict[MeshLoopIdx, DedupedVertIdx],
        triangles: List[MeshLoopTri],
) -> List[Submesh]:
    return convert_meshloop_tris_to_tsubmeshes(
        deduped_verts,
        loop_idx_to_deduped_verts_idx,
        triangles,
        lambda loops, triangles: Submesh(attr_set, base_vertices, loops, triangles)
    )


@dataclass(frozen=True)
class SkinnedSubmesh(Submesh):
    """
    A submesh with extra data for skinning e.g. vertex groups.
    """
    # The base vertex buffer must be skinned
    base_vertices: GMDSkinnedVertexBuffer
    # A mapping of (blender vertex group) -> (local bone index).
    relevant_vertex_groups: Dict[int, int]
    # A mapping of (local bone index) -> (relevant GMD bone)
    relevant_bones: List[GMDBone]

    def build_skinned(self) -> GMDSkinnedMesh:
        # Copy vertices out of vertex buffer
        vertices = self.base_vertices.copy_scatter(self.verts)
        # Where vertices.weight_data > 0, remap vertices.bone_data with self.relevant_vertex_groups
        for i in range(len(vertices)):
            for j in range(4):
                if vertices.weight_data[i, j] > 0:
                    if vertices.bone_data[i, j] not in self.relevant_vertex_groups:
                        print(i, j,
                              self.verts[i], vertices.bone_data[i], vertices.weight_data[i],
                              self.base_vertices.bone_data[self.verts[i]],
                              self.base_vertices.weight_data[self.verts[i]],
                              list(self.relevant_vertex_groups.keys()))
                    vertices.bone_data[i, j] = self.relevant_vertex_groups[vertices.bone_data[i, j]]

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
