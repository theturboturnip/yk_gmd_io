import array
from collections import defaultdict
from typing import List, Dict, Tuple, Set, DefaultDict, Iterable

from mathutils import Vector
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer_Generic

# Type Aliases
VertIdx = int
NotRemappedVertIdx = Tuple[int, VertIdx]  # originating mesh index + vertex index
Tri = Tuple[VertIdx, VertIdx, VertIdx]  # 3 vertex indices
NotRemappedTri = Tuple[int, Tri]  # originating mesh index + 3 vertex indices


def fuse_adjacent_vertices(
        vertices: List[GMDVertexBuffer_Generic]
) -> Tuple[List[List[NotRemappedVertIdx]], List[List[VertIdx]], List[List[bool]]]:
    """
    Given a set of vertices, fuse those that are "adjacent" (see vertex_fusion() docs for definition).
    Returns data on the vertices that need to be fused.

    :param vertices: Vertex buffers
    :return: (fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused)
    """

    vert_indices: Dict[Tuple[Vector, Vector, Vector, Vector], int] = {}
    # fused_idx_to_buf_idx[i] contains (i_buf, i_vertex_in_buf) indices that are all fused into vertex [i]
    # each element of this list defines an adjacency relation - all vertices in fused_idx_to_buf_idx[i] are "adjacent"
    fused_idx_to_buf_idx: List[List[NotRemappedVertIdx]] = []
    # buf_idx_to_fused_idx[i_buf][i_vertex_in_buf] contains the fused index
    buf_idx_to_fused_idx: List[List[VertIdx]] = [
        [-1] * len(buf)
        for buf in vertices
    ]
    # is_fused[i_buf][i_vertex_in_buf] = was that vertex fused into a previous vertex, or did it create a new one.
    # NOTE: is_fused will be FALSE for the first vertex in a fusion
    # i.e. if vertices [0, 1, 2] are fused into a single vertex, is_fused[0] will be FALSE because vertex 0 was not fused into anything before it.
    is_fused: List[List[bool]] = [
        [False] * len(buf)
        for buf in vertices
    ]

    for i_buf, buf in enumerate(vertices):
        for i in range(len(buf)):
            vert_info = (
                buf.pos[i].xyz.copy().freeze(),
                buf.normal[i].xyz.copy().freeze() if buf.normal else None,
                buf.bone_data[i].copy().freeze() if buf.bone_data else None,
                buf.weight_data[i].copy().freeze() if buf.weight_data else None,
            )
            if vert_info in vert_indices:
                # Fuse this into a previous vertex
                fusion_idx = vert_indices[vert_info]
                fused_idx_to_buf_idx[fusion_idx].append((i_buf, i))
                buf_idx_to_fused_idx[i_buf][i] = fusion_idx
                is_fused[i_buf][i] = True
            else:
                fusion_idx = len(fused_idx_to_buf_idx)
                vert_indices[vert_info] = fusion_idx
                fused_idx_to_buf_idx.append([(i_buf, i)])
                buf_idx_to_fused_idx[i_buf][i] = fusion_idx
                is_fused[i_buf][i] = False

    return fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused


def detect_fully_fused_triangles(
        idx_bufs: List[array.ArrayType],
        fused_idx_to_buf_idx: List[List[NotRemappedVertIdx]],
        buf_idx_to_fused_idx: List[List[VertIdx]]
) -> DefaultDict[Tri, List[NotRemappedTri]]:
    """
    Given a set of fused vertices and the meshes they came from, determine which triangles are "fully fused"
    i.e. each of their indices are fully fused.

    These are only important in the case of dupes (two fully fused triangles which result in the same fused triangle).
    Fully fused dupe triangles cannot be represented in Blender, because it cannot represent
    two triangles between the same three vertices.

    :param idx_bufs: Index buffers in triangle format (not triangle strips) for the meshes.
    :param fused_idx_to_buf_idx: Mapping of (fused vertex index) to list(raw indices that were fused)
    :param buf_idx_to_fused_idx: Mapping of (raw vertex index) to (index in overall fused buffer). Should be inverse of fused_idx_to_buf_idx.
    :return: Mapping of (triangle with fused indices T) to (triangles of raw indices which result in T after fusion).
    """

    # Maps each (remapped triangle indices) to a list of their (i_buf, (i_vtx0, i_vtx1, i_vtx2)) non-remapped triangles
    fully_fused_tri_set: DefaultDict[Tri, List[NotRemappedTri]] = defaultdict(list)

    def was_fused_to_anything(fused_idx: int) -> bool:
        return len(fused_idx_to_buf_idx[fused_idx]) > 1

    for i_buf, tri_idxs in enumerate(idx_bufs):
        buf_idx_to_fused_idx_for_mesh = buf_idx_to_fused_idx[i_buf]
        for i_tri_start in range(0, len(tri_idxs), 3):
            non_remapped_tri: Tuple[int, int, int] = (
                tri_idxs[i_tri_start + 0],
                tri_idxs[i_tri_start + 1],
                tri_idxs[i_tri_start + 2],
            )
            remapped_tri = (
                buf_idx_to_fused_idx_for_mesh[non_remapped_tri[0]],
                buf_idx_to_fused_idx_for_mesh[non_remapped_tri[1]],
                buf_idx_to_fused_idx_for_mesh[non_remapped_tri[2]],
            )
            remapped_tri = tuple(sorted(remapped_tri))

            if (was_fused_to_anything(remapped_tri[0]) and
                    was_fused_to_anything(remapped_tri[1]) and
                    was_fused_to_anything(remapped_tri[2])):
                fully_fused_tri_set[remapped_tri].append((i_buf, non_remapped_tri))

    return fully_fused_tri_set


def decide_on_unfusions(
        idx_bufs: List[array.ArrayType],
        fused_idx_to_buf_idx: List[List[NotRemappedVertIdx]],
        buf_idx_to_fused_idx: List[List[VertIdx]],
        fully_fused_tri_set: DefaultDict[Tri, List[NotRemappedTri]]
) -> DefaultDict[NotRemappedVertIdx, Set[NotRemappedVertIdx]]:
    """
    Given a set of fused vertices, the meshes they came from, and which triangles are "fully fused" with other triangles
    i.e. impossible to represent in Blender, decide which vertices to *un*-fuse to resolve the issue.

    :param idx_bufs: Index buffers in triangle format (not triangle strips) for the meshes.
    :param fused_idx_to_buf_idx: Mapping of (fused vertex index) to list(raw indices that were fused)
    :param buf_idx_to_fused_idx: Mapping of (raw vertex index) to (index in overall fused buffer). Should be inverse of fused_idx_to_buf_idx.
    :param fully_fused_tri_set: Mapping of (triangle with fused indices T) to (triangles of raw indices which result in T after fusion).
    :return: A dictionary mapping x -> ys, representing "x should not be merged with vertices ys".
    """

    # Mapping of all fully-fused non-remapped dupe triangles to the triangle they were fused into
    non_remapped_dupe_tris: Set[NotRemappedTri] = {
        non_remapped_tri
        for fused_tri, fused_non_remapped_tris in fully_fused_tri_set.items()
        for non_remapped_tri in fused_non_remapped_tris
        if len(fused_non_remapped_tris) > 1
    }

    # Set of all non-remapped vertices that are present in any entirely-fused triangle
    # These vertices will all be fused with at least one other vertex
    non_remapped_verts_in_dupe_tris = set(
        (i_buf, i_vtx)
        for i_buf, i_vtxs in non_remapped_dupe_tris
        for i_vtx in i_vtxs
    )

    # scan through all triangles again, to see if any of them have connections to non-remapped-verts
    non_remapped_tris_connected_to_verts_in_dupe_tris = set(
        (i_buf, tuple(tri_idxs[i_tri_start:i_tri_start + 3]))
        for i_buf, tri_idxs in enumerate(idx_bufs)  # foreach mesh
        for i_tri_start in range(0, len(tri_idxs), 3)  # foreach triangle in mesh
        # if any vertex in this triangle is included in a dupe triangle, include the triangle in the set
        if any(
            (i_buf, i_vtx) in non_remapped_verts_in_dupe_tris
            for i_vtx in tri_idxs[i_tri_start:i_tri_start + 3]
        )
    )

    # safety - all non-remapped-dupe-triangles are connected to verts in dupe tris
    assert non_remapped_tris_connected_to_verts_in_dupe_tris.issuperset(non_remapped_dupe_tris)

    # Decide which vertices are "interior" vs. "exterior" - interior vertices are only connected to other
    # fully-fused-dupe-triangles
    interior_non_remapped_verts = set()
    for i_buf, i_vtx in non_remapped_verts_in_dupe_tris:
        connected_non_remapped_tris = set(
            (i_buf, i_vtxs)
            for (i_buf_tri, i_vtxs) in non_remapped_tris_connected_to_verts_in_dupe_tris
            if i_buf_tri == i_buf and (i_vtx in i_vtxs)
        )
        if connected_non_remapped_tris.issubset(non_remapped_dupe_tris):
            interior_non_remapped_verts.add((i_buf, i_vtx))

    # Decide on the actual unfusions
    # This unfusion algorithm is targeting "layers" - where the same mesh and the same triangles are overlaid on each
    # other multiple times.
    # The reason we calculate "interior" vertices above, is we need to handle the case where only a subset of one mesh
    # is overlaid - the vertices on the "outside" of the copy can still be fused, and we want to fuse as many
    # as possible so that the output normals are most accurate.
    # Consider the below example:
    #      ---A--E
    #     B-----C---F
    #     |   | | | |
    #  -X-|---A'|-E'|
    # Y---B'----C'--F'
    # Here the triangles ABC, ACE, CEF have overlays with A',B',C',E',F'.
    # We *could* unfuse all of them from their counterparts, but it is more ideal to keep A/A' and B/B' fused for the sake of normals.
    # Here A' and B' are "exterior" vertices while the others are "interior".
    # We define this relationship by whether the vertices are connected to other not-fully-fused-dupe-triangles.
    # This is based on the fact that those other triangles may change the normals of the vertices A, B.
    # If vertices X and Y were not present, clearly A'/B' will have the same normals as A/B even if they aren't fused.
    #
    # So! We need to come up with an algorithm that decides to unfuse the B/B' pair, and the A/A' pair.
    # We also need to make sure this algorithm doesn't unfuse intra-layer split vertices, i.e.
    #      ---A---E
    #     B-----CD--F
    #     |   | | | |
    #  -X-|---A'|-E'|
    # Y---B'----C'--F'
    # Here the triangles are (ignoring XY) ABC, ACE, DEF, A'B'C', A'C'E', C'E'F'.
    # We should keep C and D merged, but the algorithm should still decide to unfuse C/C' AND D/C'.
    #
    # We handle these problem by considering unfusions per-fully-fused-dupe-triangle.
    #
    #       --A     A---E     E
    #     B-----C   | C |   D---F
    #     | --A'|   A'|-E'  | E'|
    #     B'----C'    C'    C'--F'
    #
    # For ABC/A'B'C', we know that A' and B' are exterior, so we don't unfuse A/A', B/B' and just unfuse C from C'.
    # For ACE/A'C'E', we know that A' is exterior, so we don't unfuse A/A' but do unfuse C/C' and E/E'.
    # For DEF/C'E'F', there are no exterior vertices, so we unfuse all of D/C', E/E', F/F'.
    # The result is unfusing C/C', D/C', E/E', F/F', which is exactly what we want.
    # Also, if we ever have a situation where all vertices are exterior
    #      --G--
    #     H-----I
    #   x-|--G'-|-x
    # x---H'----I'-x
    # Unfuse all of them. Technically you could only unfuse one, but then we'd have to decide which one.
    #
    # The algorithm pseudocode:
    # for each fully-fused-dupe-triangle
    #     for each corner set (i.e. {A, A'}, {B, B'}, {C, C'})
    #         if any element in the corner set is exterior
    #              mark corner set as exterior
    #     if all corner sets exterior:
    #         unfuse all corner sets
    #     else:
    #         unfuse not-exterior corner sets

    unfuse_verts_with: DefaultDict[NotRemappedVertIdx, Set[NotRemappedVertIdx]] = defaultdict(set)
    for fused_tri, not_remapped_tris in fully_fused_tri_set.items():
        # If this isn't a dupe, ignore it
        if len(not_remapped_tris) < 2:
            continue

        not_remapped_vtxs = [
            (i_buf, i_vtx)
            for i_buf, i_vtxs in not_remapped_tris
            for i_vtx in i_vtxs
        ]

        # First, build the corner sets
        # Three sets, each mapping to a corner of the fused triangle,
        # containing the un-remapped vtxs that map to that corner
        corner_sets = (
            [vtx for vtx in fused_idx_to_buf_idx[fused_tri[0]] if vtx in not_remapped_vtxs],
            [vtx for vtx in fused_idx_to_buf_idx[fused_tri[1]] if vtx in not_remapped_vtxs],
            [vtx for vtx in fused_idx_to_buf_idx[fused_tri[2]] if vtx in not_remapped_vtxs],
        )
        # Decide which corner sets are exterior
        is_exterior = (
            any((vtx not in interior_non_remapped_verts) for vtx in corner_sets[0]),
            any((vtx not in interior_non_remapped_verts) for vtx in corner_sets[1]),
            any((vtx not in interior_non_remapped_verts) for vtx in corner_sets[2]),
        )
        corners_to_unfuse: Iterable[List[Tuple[int, int]]]
        if all(is_exterior):
            # Unfuse all corner sets
            corners_to_unfuse = corner_sets
        else:
            # Unfuse only interior sets
            corners_to_unfuse = (
                corner_sets[i]
                for i in range(3)
                if not is_exterior[i]
            )

        # Set up unfusions:
        # for each corner to unfuse i.e. {D, C'}, {E, E'}, {F, F'}
        #     for each vtx  (D or C')
        #         unfuse_verts_with[vtx] += (D, C')
        #         (we remove the cases of "unfuse D from D" later)
        for corner_set in corners_to_unfuse:
            for vtx in corner_set:
                unfuse_verts_with[vtx].update(corner_set)

    for vtx in unfuse_verts_with.keys():
        unfuse_verts_with[vtx].remove(vtx)

    return unfuse_verts_with


def vertex_fusion(idx_bufs: List[array.ArrayType],
                  vertices: List[GMDVertexBuffer_Generic]) -> Tuple[List[List[VertIdx]], List[List[bool]]]:
    """
    Calculates "vertex fusion" for a set of vertex buffers which will result in a single contiguous list of vertices.
    Returns a list of which vertices were "fused" and a mapping of (i_buf, i_vertex_in_buf) to fused index.

    Fuses "adjacent" vertices, where adjacent vertices have the same
    - position
    - normal
    - bone mapping
    - weight mapping

    :param idx_bufs: Index buffers in triangle format (not triangle strips) for the meshes.
    :param vertices: Vertex buffers mapping to the index buffers.
    :return: Tuple of (mapping of [i_buf][i_vtx] to fused vertex index, mapping of [i_buf][i_vtx] to whether it was fused with a previous vertex).
    """

    # First pass of simple fusion
    fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused = fuse_adjacent_vertices(vertices)

    # Detect fully fused triangles, and therefore fully fused duplicate triangles
    fully_fused_tri_set = detect_fully_fused_triangles(idx_bufs, fused_idx_to_buf_idx, buf_idx_to_fused_idx)
    has_fully_fused_dupe_tris = any(len(fused_tris) > 1 for fused_tris in fully_fused_tri_set.values())

    if has_fully_fused_dupe_tris:
        print(f"DEBUG special Mesh has fully fused duplicate triangles!")
        for remapped_tri, fused_tris in fully_fused_tri_set.items():
            if len(fused_tris) == 1:
                continue
            print(f"DEBUG special {len(fused_tris)} tris map to {remapped_tri}")

            # TODO could check if the data between the different tris is actually different - if they aren't, we can ignore the dupe

        # NOW: find islands of connected remapped triangles where len(fully_fused_tri_set[t]) > 1
        # This will produce one island per set of duplicate meshes
        # i.e. if you take a mesh, copy it into a vertex buffer twice, and run this code
        # that will be one island, containing all remapped duplicate triangles of that mesh,
        # and implicitly containing both sets of non-remapped triangles

        # TODO note - above doesn't sound necessary - the only thing it affects is the definition of "interior",
        # and I don't think the value of interior would actually change if you increased the search space

        # For each island
        #    define the "interior vertices" as *non-remapped* vertices that only connect to non-remapped triangles within this island
        #    for each non-remapped triangle in the island
        #        if no vertices are interior
        #            mark all three vertices as not-fused (TODO: mark a single vertex as not-fused? would have the same effect)
        #        else
        #            mark interior vertices as not-fused
        #        (TODO not-fused really means "can only be fused within this layer"? we don't define the concept of a layer yet)
        #        (TODO maybe not-fused means "cannot be fused with any vertex within this triangle's remapped version")
        #        (because if you prevented it from fusing at all, split vertices within a single "layer" wouldn't be rejoined even if they reasonably could.)
        #
        #
        # THE GOAL:
        #   A
        #  B C  <-- if there's only one duplicate-fused triangle, we have to split at least one vertex to create
        #
        #  x A B x
        # x C D E x
        #  x F G x   <-- if there's a vertex in the middle, just splitting that one would mean all the triangles get split, and it's more elegant than splitting the edge ones.
        #                it also means you get 100% equivalent normals - if you split A, for example, it wouldn't connect to the surrounding x vertices and blender would calculate different normals.
        #
        # The remaining problem:
        #    The above code outputs a set of constraints like (vertex v may not be fused with vertices vs').
        #    We want to solve this while maximizing the amount of fusions we still do?

        unfuse_verts_with = decide_on_unfusions(idx_bufs, fused_idx_to_buf_idx, buf_idx_to_fused_idx,
                                                fully_fused_tri_set)
        for (i_buf, i_vtx), to_unfuse_with in sorted((x, y) for (x, y) in unfuse_verts_with.items()):
            print(f"unfuse {(i_buf, i_vtx)} from {to_unfuse_with}")

    return buf_idx_to_fused_idx, is_fused
