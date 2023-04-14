from typing import NewType, Tuple, List, Dict

# Int alias representing indices into bpy.types.Mesh().loops
MeshLoopIdx = NewType("MeshLoopIdx", int)

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
