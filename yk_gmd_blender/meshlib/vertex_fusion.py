import array
from collections import defaultdict
from typing import List, Dict, Tuple, Set, DefaultDict, Iterable, Sequence

from mathutils import Vector
from ..gmdlib.abstract.gmd_mesh import GMDSkinnedMesh
from ..gmdlib.abstract.gmd_shader import GMDVertexBuffer, GMDSkinnedVertexBuffer
from ..gmdlib.abstract.nodes.gmd_bone import GMDBone

"""
This module handles vertex fusion - the process of deciding which vertices in a vertex buffer
are logically equivalent and can be "fused" into a single vertex without losing data.

## Motivation
The GMD file format is optimized for rendering, not content authoring.
As such, a single logical mesh/material pair can be split into many submeshes, with vertices duplicated between them,
where it is required (e.g. mesh/material pairs with >65535 vertices are split up because index buffers are 16-bit).
Additionally, many vertices may be duplicated for the sake of per-face data.
For example, a simple textured cylinder will have duplicated vertices at the texture seam, one with UV = 0 and another
with UV = 1.
For rendering this has no effect, any vertices with identical positions and normals will be look like they are
exactly the same vertex, but in Blender this causes issues.

Blender automatically calculates vertex normals based on what other vertices it is connected to, instead of letting 
users set normals manually. (You can try to use Split Normals, but I have not had good luck with this feature and 
it seems difficult to hand-author them from the Blender GUI.)
This means if two copies of the same vertex exist, both expected to have the same normals but connected to different
faces, Blender will calculate different normals for them.
Vertex fusion also makes it easier to manipulate vertices in the Blender GUI.

Our solution is Vertex Fusion, where before loading the model into Blender we examine the vertex buffers, decide on 
which vertices are logically equivalent, and "fuse" them into a single Blender-land vertex.
Blender stores most data (e.g. UVs) per-face-corner, so two vertices X,Y with different UVs can still be fused as long
as any face corners that originally referenced X use X's UV, and corners that referenced Y use Y's UV.
This (hopefully) creates a Blender mesh that is very similar to the source meshes the developers created for the game.

## Fusion
The first pass of vertex fusion is simple, using a heuristic of strict equality over (position, normal, boneweights)
to determine which vertices are equivalent (or "adjacent", to borrow a term from graph theory).
Adjacent vertices are fused into a single vertex, and all other vertices are untouched.
This heuristic is not perfect, though - it can over-fuse vertices to the point of losing data.

## Motivation - Unfusion
Consider two triangles ABC and DEF, where each vertex in ABC has an adjacent vertex in DEF.

    A
  B---C
  | | |  
  | D | 
  E---F

After the first pass of vertex fusion, each vertex of ABC will be fused with a vertex in DEF.
We can represent the resulting fused vertices as 
  - A,D -> X
  - B,E -> Y
  - C,F -> Z
ABC and DEF can be referred to as "fully-fused duplicates" - each vertex is the result of a fusion, and after fusion
they map to the same triangle XYZ.
Blender does not allow two triangles to exist between the same vertices.
There are two triangles worth of per-face-corner data to represent in ABC and DEF, which cannot be fully represented 
in the single triangle XYZ, so half the data will be lost after this fusion.
The solution? *Un*fuse some/all of those vertices to create two triangles XYZ and XYW, or XYZ and UVW, which can 
hold all of the per-face-corner data, while keeping as many vertices fused as possible to maintain correct normal data.

## Implementation
This process is implemented in four stages, with a fifth function combining the stages.

1. fuse_adjacent_vertices() does the first-pass fusion, deciding which vertices are adjacent and fusing them.
2. detect_fully_fused_triangles() builds a mapping of (fused tri) -> [(constituent pre-fusion tris)]
3. decide_on_unfusions() examines that mapping and decides which pairs of vertices should be *unfused* to resolve them
4. solve_unfusion() applies those unfusions to the previous first-pass fusion to decide on the final fusions.

vertex_fusion() applies stages 1 and 2, and if any fully-fused-duplicate-triangles are found it then applies 3 and 4.

See each function's documentation for details on each step.
decide_on_unfusions() has a comprehensive explanation of how it decides which vertices to unfuse.
"""

# Type Aliases
VertIdx = int
NotRemappedVertIdx = Tuple[int, VertIdx]  # originating mesh index + vertex index
Tri = Tuple[VertIdx, VertIdx, VertIdx]  # 3 vertex indices
NotRemappedTri = Tuple[int, Tri]  # originating mesh index + 3 vertex indices


def make_bone_indices_consistent(
        gmd_meshes: List[GMDSkinnedMesh],
) -> Tuple[List[GMDBone], List[GMDSkinnedVertexBuffer]]:
    """
    Creates a list of vertex buffers with consistent bone indices
    i.e. vertices in different buffers use the same indices to refer to the same bones.
    Returns the overall list of bones and a list of the new vertex buffers.
    The first vertex buffer is NOT copied, because it doesn't need to be remapped

    :param gmd_meshes:
    :return:
    """

    # Fix up bone mappings if the meshes are skinned

    # Build a list of references bones
    # All vertex buffers will have their data remapped to indexes into this list.
    # Start from the first mesh's bone list, then grow from there
    remapped_vertices = [gmd_meshes[0].vertices_data]
    relevant_bones = gmd_meshes[0].relevant_bones[:]
    # The first mesh doesn't need remapping, because we start from its bone list, but subsequent ones do
    for i_mesh in range(1, len(gmd_meshes)):
        gmd_mesh = gmd_meshes[i_mesh]

        # Mapping of gmd_meshes[i] bone indices to relevant_bones indices
        bone_index_mapping = {}
        for i, bone in enumerate(gmd_mesh.relevant_bones):
            if bone not in relevant_bones:
                relevant_bones.append(bone)
            bone_index_mapping[i] = relevant_bones.index(bone)

        def remap_weight(bone: int, weight: float) -> int:
            # If the weight is 0 the bone is unused, so map it to a consistent 0.
            if weight == 0:
                return 0
            else:
                return bone_index_mapping[bone]

        # Copy the vertex buffer
        verts_to_remap = gmd_mesh.vertices_data.copy_as_skinned()
        # Remap the bones in the vertices
        for i_vtx in range(len(verts_to_remap)):
            old_weights = verts_to_remap.weight_data[i_vtx]
            old_bones = verts_to_remap.bone_data[i_vtx]
            new_bones = (
                remap_weight(old_bones[0], old_weights[0]),
                remap_weight(old_bones[1], old_weights[1]),
                remap_weight(old_bones[2], old_weights[2]),
                remap_weight(old_bones[3], old_weights[3]),
            )
            verts_to_remap.bone_data[i_vtx] = Vector(new_bones)
        remapped_vertices.append(verts_to_remap)

    # Done, return the full list of relevant bones.
    return relevant_bones, remapped_vertices


def fuse_adjacent_vertices(
        vertices: Sequence[GMDVertexBuffer]
) -> Tuple[List[List[NotRemappedVertIdx]], List[List[VertIdx]], List[List[bool]]]:
    """
    Given a set of vertices, fuse those that are "adjacent" (see vertex_fusion() docs for definition).
    Returns data on the vertices that need to be fused.

    :param vertices: Vertex buffers
    :return: (fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused)
    """

    vert_indices: Dict[Tuple[Vector, Vector, Vector, Vector], VertIdx] = {}
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
                Vector(buf.pos[i][:3]).freeze(),
                Vector(buf.normal[i][:3]).freeze() if buf.normal is not None else None,
                Vector(buf.bone_data[i]).freeze() if buf.bone_data is not None else None,
                Vector(buf.weight_data[i]).freeze() if buf.weight_data is not None else None,
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
) -> Dict[Tri, List[NotRemappedTri]]:
    """
    Given a set of fused vertices and the meshes they came from, determine which triangles are "fully fused"
    i.e. each of their indices are fully fused, or it resolves to the same post-fusion triangle as another triangle.

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
            fully_fused_tri_set[remapped_tri].append((i_buf, non_remapped_tri))

    return {remapped_tri: tri_set for (remapped_tri, tri_set) in fully_fused_tri_set.items() if
            len(tri_set) > 1 or (was_fused_to_anything(remapped_tri[0]) and
                                 was_fused_to_anything(remapped_tri[1]) and
                                 was_fused_to_anything(remapped_tri[2]))}


def decide_on_unfusions(
        idx_bufs: List[array.ArrayType],
        fused_idx_to_buf_idx: List[List[NotRemappedVertIdx]],
        fully_fused_tri_set: Dict[Tri, List[NotRemappedTri]]
) -> Dict[NotRemappedVertIdx, Set[NotRemappedVertIdx]]:
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

    # Set of triangles that connect to vertices in our fully-fused-dupe-triangles
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

    # Decide which vertices are "interior" vs. "exterior"
    # interior vertices are only connected to other fully-fused-dupe-triangles
    interior_non_remapped_verts = set()
    # Foreach vertex in our fully-fused-dupe-triangles
    for i_buf, i_vtx in non_remapped_verts_in_dupe_tris:
        # Find the triangles that connect to it
        connected_non_remapped_tris = set(
            (i_buf, i_vtxs)
            for (i_buf_tri, i_vtxs) in non_remapped_tris_connected_to_verts_in_dupe_tris
            if i_buf_tri == i_buf and (i_vtx in i_vtxs)
        )
        # If all of those triangles are fully-fused-dupe-triangles...
        if connected_non_remapped_tris.issubset(non_remapped_dupe_tris):
            # ... this vertex is an interior vertex.
            interior_non_remapped_verts.add((i_buf, i_vtx))

    # The unfusion algorithm targets "layers" - where the same mesh and the same triangles are overlaid on each
    # other at least once.
    # The reason we calculate "interior" vertices above, is we need to handle the case where only a subset of one mesh
    # is overlaid - the vertices on the "outside" of the copy can still be fused, and we want to fuse as many
    # as possible so that the output normals are most accurate.
    # Consider this triangle strip with an overlaid subset:
    #      ---A---E
    #     B-----C---F
    #     |   | | | |
    #  -X-|---A'|-E'|
    # Y---B'----C'--F'
    # Here the vertices ABCEF have overlays with A'B'C'E'F'.
    # Fusing them all would create three sets of fully-fused duplicate triangles:
    #    {ABC, A'B'C'},  {ACE, A'C'E'},  {CEF, C'E'F'}.
    # We *could* unfuse all the vertices from their counterparts,
    # but it is more ideal to keep A/A' and B/B' fused for the sake of normals.
    #
    # Here A' and B' are "exterior" vertices while the others are "interior".
    # We define this relationship by whether the vertices are connected to other not-fully-fused-dupe-triangles.
    # This is based on the fact that those other triangles may change the normals of the vertices A, B.
    # If vertices X and Y were not present, clearly A'/B' will have the same normals as A/B even if they aren't fused.
    #
    # So! We need to come up with an algorithm that unfuses C/C', E/E', F/F', but *not* A/A' and B/B'.
    # We also need to make sure this algorithm doesn't unfuse intra-layer split vertices.
    # Consider the case if we add a vertex D:
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
    #
    # Also, if we ever have a situation where all vertices are exterior:
    #      --G--
    #     H-----I
    #   x-|--G'-|-x
    # x---H'----I'-x
    # We unfuse all of them. Technically you could choose to unfuse one, but then we'd have to decide which one.
    #
    # Consider the case if we add a seam:
    #      ---A---EG
    #     B-----CD----F
    #     |   | | |   |
    #  -X-|---A'|-E'G'|
    # Y---B'----C'D'--F'
    # Here the triangles are (ignoring XY) ABC, ACE, DGF, A'B'C', A'C'E', D'G'F'.
    # We should keep C and D merged, but the algorithm should still decide to unfuse {C/C', D/D'}
    # We should keep E and G merged, but the algorithm should still decide to unfuse {E/E', G/G'}
    #
    # For ABC/A'B'C', we know that A' and B' are exterior, so we don't unfuse A/A', B/B' and just unfuse C from C'.
    # For ACE/A'C'E', we know that A' is exterior, so we don't unfuse A/A' but do unfuse C/C' and E/E'.
    # For DGF/D'G'F', there are no exterior vertices, so we unfuse all of D/D', G/E', F/F'.
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

        # List of not-remapped vertices within this fused triangle
        not_remapped_vtxs = [
            (i_buf, i_vtx)
            for i_buf, i_vtxs in not_remapped_tris
            for i_vtx in i_vtxs
        ]

        # First, build the corner sets
        # Three sets, each mapping to a corner of the fused triangle,
        # containing the un-remapped vtxs from this triangle that were fused into that corner
        corner_sets = (
            [
                # Each vertex that fuses into this corner
                vtx for vtx in fused_idx_to_buf_idx[fused_tri[0]]
                # If it is contained in one of our fully-fused-dupe-triangles.
                if vtx in not_remapped_vtxs
            ],
            [vtx for vtx in fused_idx_to_buf_idx[fused_tri[1]] if vtx in not_remapped_vtxs],
            [vtx for vtx in fused_idx_to_buf_idx[fused_tri[2]] if vtx in not_remapped_vtxs],
        )
        # Decide which corner sets are exterior
        is_exterior = (
            any((vtx not in interior_non_remapped_verts) for vtx in corner_sets[0]),
            any((vtx not in interior_non_remapped_verts) for vtx in corner_sets[1]),
            any((vtx not in interior_non_remapped_verts) for vtx in corner_sets[2]),
        )
        # Decide which corners to unfuse
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


def solve_unfusion(
        vert_bufs: Sequence[GMDVertexBuffer],
        old_fused_idx_to_buf_idx: List[List[NotRemappedVertIdx]],
        unfuse_verts_with: Dict[NotRemappedVertIdx, Set[NotRemappedVertIdx]]
) -> Tuple[List[List[NotRemappedVertIdx]], List[List[VertIdx]], List[List[bool]]]:
    """
    Given a set of previous vertex fusions F and a set of vertex *un*fusions U,
    return a new set of fusions F' taking all fusions in F except for those prevented by U

    :param vert_bufs: Vertex buffers, used to iterate over buffer/vertex indices. Not modified or read directly.
    :param old_fused_idx_to_buf_idx: Fused index -> original index mapping representing the previous fusions F.
    :param unfuse_verts_with: The set of vertex unfusions U
    :return: (fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused) representing F' = F - U.
    """

    # Create a set of "vertices this is fused with" for each vertex
    # fusion_group_for[v] always contains v - it may just be [v] if no fusion is performed.
    fusion_group_for: Dict[NotRemappedVertIdx, Tuple[NotRemappedVertIdx, ...]] = {}
    for fused_verts in old_fused_idx_to_buf_idx:
        # Each not-remapped vert appears exactly once in fused_idx_to_buf_idx
        # Each bucket will contain at least one vertex
        # Overall, all vertices in fused_verts will appear in buckets exactly once
        buckets: List[List[NotRemappedVertIdx]] = []
        for vert in fused_verts:
            # Each vertex should be in a fusion group with
            # (1) the vertices F said they should be fused with
            # (2) except the vertices U says it *shouldn't* be fused with
            # (3) except some other vertices in group F that U says shouldn't be fused together

            # Before, we just evaluated (1) and (2) with
            # fusion_group_for[vert] = tuple(
            #     v for v in fused_verts  # (1)
            #     if v not in unfuse_verts_with[vert]  # (2)
            # )

            # This is guaranteed to be "consistent" i.e. for all v' in fusion_group_for[v], fusion_group_for[v'] contains v
            # IF AND ONLY IF unfuse_verts_with is consistent, i.e. for all v' in unfuse_verts_with[v], unfuse_verts_with[v'] contains v
            # BUT it isn't guaranteed to be *correct* i.e. no fusions prevented by U are present
            # Consider: AB
            #           |
            #          A'B'
            # fused_verts = [A, B, A', B']
            # unfuse_verts_with = [A/A', A'/A, B/B', B'/B]
            # fusion_group_for = [
            #     A -> (A, B, B'),
            #     A' -> (A', B, B'),
            #     B -> (A, A', B),
            #     B' -> (A, A', B'),
            # ]

            # New version: greedy bucketing
            # Maintain a list of buckets for each group of previously-fused verts
            # Foreach previously-fused vert, add to the first bucket without any conflicts
            #    if all the buckets have conflicts i.e. they have vertices that we can't be fused with...
            #        create a new bucket!
            # Then once we have the buckets construct fusion_group_for[v] based on the buckets
            # This is guarantees to be correct, i.e. no fusions prevents by U are present,
            # but I don't think it's guaranteed to be *minimal*

            relevant_U = unfuse_verts_with[vert]
            placed_in_bucket = False
            for b in buckets:
                # If we aren't allowed to be with any vertex already in this bucket...
                if any(b_v in relevant_U for b_v in b):
                    # ...skip this bucket
                    continue
                # else, take this bucket!
                b.append(vert)
                placed_in_bucket = True
                # (and only take this bucket, don't take any other buckets)
                break
            # If we couldn't find a bucket, create a new one
            if not placed_in_bucket:
                buckets.append([vert])
        # Create the fusion_group_for entries for each vertex now the fusion groups are complete
        for b in buckets:
            b_t = tuple(b)
            for v in b_t:
                # consistency check
                assert not any(b_v in unfuse_verts_with[v] for b_v in b_t)
                fusion_group_for[v] = b_t

    # TODO - consistency check?

    # We can now turn "vertices this is fused with" into a full definition of the fusions

    # Map a fusion group to the fused vertex index it has
    encountered_fusion_groups: Dict[Tuple[NotRemappedVertIdx, ...], int] = {}
    fused_idx_to_buf_idx: List[List[NotRemappedVertIdx]] = []
    buf_idx_to_fused_idx: List[List[VertIdx]] = [
        [-1] * len(buf)
        for buf in vert_bufs
    ]
    is_fused: List[List[bool]] = [
        [False] * len(buf)
        for buf in vert_bufs
    ]

    for i_buf, buf in enumerate(vert_bufs):
        for i_vtx in range(len(buf)):
            vert = (i_buf, i_vtx)
            fusion_group = fusion_group_for[vert]

            # If we should be fused to a previous vertex,
            if fusion_group in encountered_fusion_groups:
                # This has been fused into a previous vertex (fused_idx_to_buf_idx has already been set to the full group)
                fusion_idx = encountered_fusion_groups[fusion_group]
                buf_idx_to_fused_idx[i_buf][i_vtx] = fusion_idx
                is_fused[i_buf][i_vtx] = True
            else:
                fusion_idx = len(fused_idx_to_buf_idx)
                encountered_fusion_groups[fusion_group] = fusion_idx
                fused_idx_to_buf_idx.append(sorted(fusion_group))
                buf_idx_to_fused_idx[i_buf][i_vtx] = fusion_idx
                is_fused[i_buf][i_vtx] = False

    return fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused


def vertex_fusion(
        idx_bufs: List[array.ArrayType],
        vertices: Sequence[GMDVertexBuffer]
) -> Tuple[List[List[NotRemappedVertIdx]], List[List[VertIdx]], List[List[bool]]]:
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
    # There may be triangles where each vertex was fused, but that didn't result in a duplicate or loss of data.
    # => check if any of the sets of (triangles that were fully-fused into one fused triangle) have >2 elements.
    has_fully_fused_dupe_tris = any(len(fused_tris) > 1 for fused_tris in fully_fused_tri_set.values())

    if has_fully_fused_dupe_tris:
        # Decide which vertices to unfuse to resolve the fully-fused-dupe-tris
        unfuse_verts_with = decide_on_unfusions(
            idx_bufs,
            fused_idx_to_buf_idx,
            fully_fused_tri_set
        )
        # Actually perform the unfusion
        fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused = solve_unfusion(
            vertices,
            fused_idx_to_buf_idx,
            unfuse_verts_with
        )

    return fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused
