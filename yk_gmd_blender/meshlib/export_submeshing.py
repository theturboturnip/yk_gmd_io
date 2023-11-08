from typing import List, Dict, Tuple, TypeVar, Callable, NewType

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
    List[MeshLoopIdx],
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

    deduped_verts: List[MeshLoopIdx] = []
    loop_idx_to_deduped_verts_idx: Dict[MeshLoopIdx, DedupedVertIdx] = {}
    for i, (loop_idx, vertex) in enumerate(zip(loops_with_dupes, vertex_bytes)):
        # See if this vertex data has already been encountered
        no_dupe_loop_idx = vertex_bytes_to_no_dupe_loop_idx.get(vertex)
        # If not, it's not a dupe - push it to deduped_verts and register in vertex_bytes_to...
        if no_dupe_loop_idx is None:
            no_dupe_loop_idx = DedupedVertIdx(len(deduped_verts))
            deduped_verts.append(loop_idx)
            vertex_bytes_to_no_dupe_loop_idx[vertex] = no_dupe_loop_idx
        # Either way, we now know where this mesh loop maps to inside deduped_verts
        loop_idx_to_deduped_verts_idx[loop_idx] = no_dupe_loop_idx

    return deduped_verts, loop_idx_to_deduped_verts_idx


TSubmesh = TypeVar("TSubmesh")


def convert_meshloop_tris_to_tsubmeshes(
        deduped_verts: List[MeshLoopIdx],
        loop_idx_to_deduped_verts_idx: Dict[MeshLoopIdx, DedupedVertIdx],
        triangles: List[MeshLoopTri],
        submesh_generator: Callable[
            [
                List[MeshLoopIdx],
                List[SubmeshTri]
            ],
            TSubmesh
        ],
        max_verts_per_submesh=65536
) -> List[TSubmesh]:
    assert max_verts_per_submesh >= 3

    submeshes = []

    deduped_verts_idx_to_pending_vert_idx: Dict[DedupedVertIdx, SubmeshVertIdx] = {}
    pending_verts: List[MeshLoopIdx] = []
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

        # We have a maximum of `max_verts_per_submesh` vertices.
        # At most, adding a new triangle can only add 3 loops to the "pending" buffer.
        # also, adding a triangle may add 0 loops - if they're all used already.
        # So if we have `max_verts_per_submesh-3` loops, check to see how many we would add.
        if len(pending_verts) >= (max_verts_per_submesh - 3):
            # We have to be careful, we might grow beyond the buffer
            num_to_add = 0
            if deduped_verts[t_no_dupes[0]] not in deduped_verts_idx_to_pending_vert_idx:
                num_to_add += 1
            if deduped_verts[t_no_dupes[1]] not in deduped_verts_idx_to_pending_vert_idx:
                num_to_add += 1
            if deduped_verts[t_no_dupes[2]] not in deduped_verts_idx_to_pending_vert_idx:
                num_to_add += 1
            if len(pending_verts) + num_to_add > max_verts_per_submesh:
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

    return submeshes
