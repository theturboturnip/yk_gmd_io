from collections import defaultdict
from typing import List, Dict, Tuple, Set, DefaultDict

from mathutils import Vector
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer_Generic


def vertex_fusion(gmd_meshes: List[GMDMesh],
                  vertices: List[GMDVertexBuffer_Generic]) -> Tuple[List[List[int]], List[List[bool]]]:
    """
    Applies "vertex fusion" to a set of vertex buffers, returning a list of which vertices were "fused"
    and a mapping of (i_buf, i_vertex_in_buf) to fused index.

    Fuses "adjacent" vertices, where adjacent vertices have the same
    - position
    - normal
    - bone mapping
    - weight mapping

    :param vertices:
    :return:
    """

    vert_indices: Dict[Tuple[Vector, Vector, Vector, Vector], int] = {}
    # fused_idx_to_buf_idx[i] contains (i_buf, i_vertex_in_buf) indices that are all fused into vertex [i]
    # each element of this list defines an adjacency relation - all vertices in fused_idx_to_buf_idx[i] are "adjacent"
    fused_idx_to_buf_idx: List[List[Tuple[int, int]]] = []
    # buf_idx_to_fused_idx[i_buf][i_vertex_in_buf] contains the fused index
    buf_idx_to_fused_idx: List[List[int]] = [
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

    # fully_fused_verts[i_buf] = a list of triangle indices within mesh i_buf that are fully fused
    # i.e. all vertices are fused with other vertices
    fully_fused_tris: List[List[int]] = [
        []
        for _ in vertices
    ]
    # Maps each (remapped triangle indices) to a list of their (i_buf, (i_vtx0, i_vtx1, i_vtx2)) non-remapped triangles
    fully_fused_tri_set: DefaultDict[
        Tuple[int, int, int],
        List[
            Tuple[int, Tuple[int, int, int]]
        ]
    ] = defaultdict(list)

    def was_fused_to_anything(fused_idx: int) -> bool:
        return len(fused_idx_to_buf_idx[fused_idx]) > 1

    for i_buf, (gmd_mesh, buf) in enumerate(zip(gmd_meshes, vertices)):
        buf_idx_to_fused_idx_for_mesh = buf_idx_to_fused_idx[i_buf]
        for i_tri_start in range(0, len(gmd_mesh.triangle_indices), 3):
            non_remapped_tri: Tuple[int, int, int] = (
                gmd_mesh.triangle_indices[i_tri_start + 0],
                gmd_mesh.triangle_indices[i_tri_start + 1],
                gmd_mesh.triangle_indices[i_tri_start + 2],
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

    has_fully_fused_dupe_tris = any(len(fused_tris) > 1 for fused_tris in fully_fused_tri_set.values())

    if has_fully_fused_dupe_tris:
        verts_in_fully_fused_tris: Set[int]
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

        # Mapping of all fully-fused non-remapped triangles to the triangle they were fused into
        non_remapped_dupe_tris_to_fused_tris: Dict[Tuple[int, Tuple[int, int, int]], Tuple[int, int, int]] = {
            non_remapped_tri: fused_tri
            for fused_tri, fused_non_remapped_tris in fully_fused_tri_set.items()
            for non_remapped_tri in fused_non_remapped_tris
        }
        non_remapped_dupe_tris = set(non_remapped_dupe_tris_to_fused_tris.keys())

        # Set of all non-remapped vertices that are present in any entirely-fused triangle
        # These vertices will all be fused with at least one other vertex
        non_remapped_verts_in_dupe_tris = set(
            (i_buf, i_vtx)
            for i_buf, i_vtxs in non_remapped_dupe_tris
            for i_vtx in i_vtxs
        )

        # scan through all triangles again, to see if any of them have connections to non-remapped-verts
        non_remapped_tris_connected_to_verts_in_dupe_tris = set(
            (i_buf, tuple(gmd_mesh.triangle_indices[i_tri_start:i_tri_start + 3]))
            for i_buf, gmd_mesh in enumerate(gmd_meshes)  # foreach mesh
            for i_tri_start in range(0, len(gmd_mesh.triangle_indices), 3)  # foreach triangle in mesh
            # if any vertex in this triangle is included in a dupe triangle, include the triangle in the set
            if any(
                (i_buf, i_vtx) in non_remapped_verts_in_dupe_tris
                for i_vtx in gmd_mesh.triangle_indices[i_tri_start:i_tri_start + 3]
            )
        )

        # safety - all non-remapped-dupe-triangles are connected to verts in dupe tris
        assert non_remapped_tris_connected_to_verts_in_dupe_tris.issuperset(non_remapped_dupe_tris)

        interior_non_remapped_verts = set()
        for i_buf, i_vtx in non_remapped_verts_in_dupe_tris:
            connected_non_remapped_tris = set(
                (i_buf, i_vtxs)
                for (i_buf_tri, i_vtxs) in non_remapped_tris_connected_to_verts_in_dupe_tris
                if i_buf_tri == i_buf and (i_vtx in i_vtxs)
            )
            if connected_non_remapped_tris.issubset(non_remapped_dupe_tris):
                interior_non_remapped_verts.add((i_buf, i_vtx))

        unfuse_verts_with: DefaultDict[Tuple[int, int], Set[Tuple[int, int]]] = defaultdict(set)
        # TODO this can just iterate over fully_fused_tri_set, and avoid creating non_remapped_dupe_tris_to_fused_tris
        for i_buf, i_vtxs in non_remapped_dupe_tris:
            interior_verts = tuple(
                i_vtx
                for i_vtx in i_vtxs
                if (i_buf, i_vtx) in interior_non_remapped_verts
            )

            to_unfuse: Tuple[int, ...]
            if not interior_verts:
                # Mark all three as not-fused?
                to_unfuse = i_vtxs
            else:
                # Mark just the interior verts as not-fused
                to_unfuse = interior_verts

            # Unfuse each vertex by saying "this is no longer allowed to fuse with any vertices contained in the fused triangle this triangle is a part of"
            triangle_we_fused_into = non_remapped_dupe_tris_to_fused_tris[(i_buf, i_vtxs)]
            other_triangles_that_fused_into_ours = fully_fused_tri_set[triangle_we_fused_into]
            non_remapped_verts_in_fusions_with_this_tri = set(
                (i_f_buf, i_f_vtx)
                for (i_f_buf, i_f_vtxs) in other_triangles_that_fused_into_ours
                for i_f_vtx in i_f_vtxs
                if i_f_vtxs != i_vtxs
            )
            for i_unfuse_vtx in to_unfuse:
                unfuse_verts_with[(i_buf, i_unfuse_vtx)].update(non_remapped_verts_in_fusions_with_this_tri)

        # Last step - this is just for printing purposes
        # Reduce each unfuse_verts_with list to just things that are already fused with the vert
        for (i_buf, i_vtx), to_unfuse_with in sorted((x, y) for (x, y) in unfuse_verts_with.items()):
            fused_into = buf_idx_to_fused_idx[i_buf][i_vtx]
            new_to_unfuse_with = tuple(
                x
                for x in to_unfuse_with
                if x in fused_idx_to_buf_idx[fused_into] and x != (i_buf, i_vtx)
            )
            print(f"unfuse {(i_buf, i_vtx)} from {new_to_unfuse_with}")

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

    return buf_idx_to_fused_idx, is_fused
