from typing import List, Tuple, Iterable, Dict

import pytest

from yk_gmd_blender.meshlib.export_submeshing import MeshLoopIdx, dedupe_loops, convert_meshloop_tris_to_tsubmeshes, \
    DedupedVertIdx, MeshLoopTri, SubmeshTri


@pytest.mark.order(3)
def test_dedupe_with_no_dupes():
    loops_with_dupes = [
        MeshLoopIdx(0),
        MeshLoopIdx(1),
        MeshLoopIdx(2),
        MeshLoopIdx(3),
        MeshLoopIdx(4),
        MeshLoopIdx(5),
    ]
    vertices = [
        bytes([0]),
        bytes([1]),
        bytes([2]),
        bytes([3]),
        bytes([4]),
        bytes([5]),
    ]
    deduped_verts, deduped_dict = dedupe_loops(loops_with_dupes, vertices)
    assert deduped_verts == [0, 1, 2, 3, 4, 5]
    assert deduped_dict == {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
    }


@pytest.mark.order(3)
def test_dedupe_with_no_dupes_with_material_offsets():
    loops_with_dupes = [
        MeshLoopIdx(100),
        MeshLoopIdx(101),
        MeshLoopIdx(102),
        MeshLoopIdx(103),
        MeshLoopIdx(104),
        MeshLoopIdx(105),
    ]
    vertices = [
        bytes([0]),
        bytes([1]),
        bytes([2]),
        bytes([3]),
        bytes([4]),
        bytes([5]),
    ]
    deduped_verts, deduped_dict = dedupe_loops(loops_with_dupes, vertices)
    assert deduped_verts == [100, 101, 102, 103, 104, 105]
    assert deduped_dict == {
        100: 0,
        101: 1,
        102: 2,
        103: 3,
        104: 4,
        105: 5,
    }


@pytest.mark.order(3)
def test_dedupe_with_dupes_with_material_offsets():
    loops_with_dupes = [
        MeshLoopIdx(100),
        MeshLoopIdx(101),
        MeshLoopIdx(102),
        MeshLoopIdx(103),
        MeshLoopIdx(104),
        MeshLoopIdx(105),
    ]
    vertices = [
        bytes([0]),
        bytes([0]),
        bytes([0]),
        bytes([1]),
        bytes([1]),
        bytes([1]),
    ]
    deduped_verts, deduped_dict = dedupe_loops(loops_with_dupes, vertices)
    assert deduped_verts == [100, 103]
    assert deduped_dict == {
        100: 0,
        101: 0,
        102: 0,
        103: 1,
        104: 1,
        105: 1,
    }


def dummy_submesh(loops: List[MeshLoopIdx], tris: List[SubmeshTri]) -> Tuple[List[MeshLoopIdx], List[SubmeshTri]]:
    return loops, tris


def gen_triangles(tris: Iterable[Tuple[int, int, int]]) -> List[MeshLoopTri]:
    return [
        MeshLoopTri((MeshLoopIdx(a), MeshLoopIdx(b), MeshLoopIdx(c)))
        for a, b, c in tris
    ]


def gen_fake_deduped_verts(n_verts: int, n_dupes_per_vert: int) -> Tuple[
    List[MeshLoopIdx], Dict[MeshLoopIdx, DedupedVertIdx]
]:
    # Generates fake "deduped" verts as if the original data was `n_verts` duplicated `n_dupes_per_vert` times
    #
    # e.g. for n_verts = 4, n_dupes_per_vert = 2
    # deduped_verts = [0, 2, 4, 6]
    # deduped_map = { 0 -> 0, 1 -> 0, 2 -> 1, 3 -> 1, ... }
    deduped_verts = [MeshLoopIdx(i * n_dupes_per_vert) for i in range(n_verts)]
    deduped_map = {
        MeshLoopIdx(nondupe_loop_idx * n_dupes_per_vert + dupe_offset): DedupedVertIdx(nondupe_loop_idx)
        for nondupe_loop_idx in range(n_verts)
        for dupe_offset in range(n_dupes_per_vert)
    }
    return deduped_verts, deduped_map


@pytest.mark.order(3)
def test_submeshing_no_split():
    # The identity case: not enough vertices to hit the limit
    # Just make a long triangle strip
    deduped_verts, loop_idx_to_deduped_verts_idx = gen_fake_deduped_verts(n_verts=99, n_dupes_per_vert=1)
    triangles = gen_triangles(
        (i + 0, i + 1, i + 2)
        for i in range(97)
    )

    submeshes = convert_meshloop_tris_to_tsubmeshes(
        deduped_verts,
        loop_idx_to_deduped_verts_idx,
        triangles,
        dummy_submesh,
        max_verts_per_submesh=500,
    )
    assert len(submeshes) == 1

    out_loops, out_tris = submeshes[0]

    assert out_loops == deduped_verts
    assert out_tris == triangles


@pytest.mark.order(3)
def test_submeshing_no_split_with_dupes():
    # The identity case: not enough vertices to hit the limit
    # Just make a long triangle strip
    # Generate 4 extra dupes for each vertex, and only use the first instance of each vert in the triangles
    deduped_verts, loop_idx_to_deduped_verts_idx = gen_fake_deduped_verts(n_verts=99, n_dupes_per_vert=5)
    triangles = gen_triangles(
        ((i + 0) * 5, (i + 1) * 5, (i + 2) * 5)
        for i in range(97)
    )

    submeshes = convert_meshloop_tris_to_tsubmeshes(
        deduped_verts,
        loop_idx_to_deduped_verts_idx,
        triangles,
        dummy_submesh,
        max_verts_per_submesh=500,
    )
    assert len(submeshes) == 1

    out_loops, out_tris = submeshes[0]

    assert out_loops == deduped_verts
    # The final triangles have been remapped
    assert out_tris == gen_triangles(
        ((i + 0), (i + 1), (i + 2))
        for i in range(97)
    )


@pytest.mark.order(3)
def test_submeshing_split_no_shared():
    # When you split a mesh such that no vertices are shared between the split
    # Easy example: two disconnected quads, split into one submesh per quad
    deduped_verts, loop_idx_to_deduped_verts_idx = gen_fake_deduped_verts(n_verts=8, n_dupes_per_vert=1)
    triangles = gen_triangles([
        (0, 1, 2),
        (1, 2, 3),

        (4, 5, 6),
        (5, 6, 7),
    ])

    submeshes = convert_meshloop_tris_to_tsubmeshes(
        deduped_verts,
        loop_idx_to_deduped_verts_idx,
        triangles,
        dummy_submesh,
        max_verts_per_submesh=4,
    )
    assert len(submeshes) == 2

    quad_1_loops, quad_1_tris = submeshes[0]
    assert quad_1_loops == deduped_verts[0:4]
    assert quad_1_tris == [
        (0, 1, 2),
        (1, 2, 3),
    ]

    quad_2_loops, quad_2_tris = submeshes[1]
    assert quad_2_loops == deduped_verts[4:8]
    # The tris have been remapped
    assert quad_2_tris == [
        (0, 1, 2),
        (1, 2, 3),
    ]


@pytest.mark.order(3)
def test_submeshing_split_shared():
    # When you split a mesh where vertices are shared between the split
    # Easy example: two connected tris, split into one submesh per tri
    deduped_verts, loop_idx_to_deduped_verts_idx = gen_fake_deduped_verts(n_verts=5, n_dupes_per_vert=1)
    triangles = gen_triangles([
        (0, 1, 2),
        (2, 3, 4),
    ])

    submeshes = convert_meshloop_tris_to_tsubmeshes(
        deduped_verts,
        loop_idx_to_deduped_verts_idx,
        triangles,
        dummy_submesh,
        max_verts_per_submesh=3,
    )
    assert len(submeshes) == 2

    # The first triangle is a single tri between verts 0,1,2
    tri_1_loops, tri_1_tris = submeshes[0]
    assert tri_1_loops == deduped_verts[0:3]
    assert tri_1_tris == [
        (0, 1, 2),
    ]

    # The second triangle has been split off, so will be between 2,3,4
    tri_2_loops, tri_2_tris = submeshes[1]
    assert tri_2_loops == deduped_verts[2:5]
    # The tris have been remapped
    assert tri_2_tris == [
        (0, 1, 2),
    ]


@pytest.mark.order(3)
def test_submeshing_split_shared_with_dupes():
    # When you split a mesh where vertices are shared between the split
    # Easy example: two connected tris, split into one submesh per tri
    # Generate an extra dupe for each vertex, and sometimes use those duplicates in the triangle
    deduped_verts, loop_idx_to_deduped_verts_idx = gen_fake_deduped_verts(n_verts=5, n_dupes_per_vert=2)
    triangles = gen_triangles([
        (
            0 * 2,  # original
            1 * 2 + 1,  # dupe
            2 * 2 + 1  # dupe
        ),
        (
            2 * 2 + 1,  # dupe
            3 * 2,  # original
            4 * 2  # original
        ),
    ])

    submeshes = convert_meshloop_tris_to_tsubmeshes(
        deduped_verts,
        loop_idx_to_deduped_verts_idx,
        triangles,
        dummy_submesh,
        max_verts_per_submesh=3,
    )
    assert len(submeshes) == 2

    # The first triangle is a single tri between verts 0,1,2
    tri_1_loops, tri_1_tris = submeshes[0]
    assert tri_1_loops == deduped_verts[0:3]
    assert tri_1_tris == [
        (0, 1, 2),
    ]

    # The second triangle has been split off, so will be between 2,3,4
    tri_2_loops, tri_2_tris = submeshes[1]
    assert tri_2_loops == deduped_verts[2:5]
    # The tris have been remapped
    assert tri_2_tris == [
        (0, 1, 2),
    ]
