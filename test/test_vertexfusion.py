import array
from typing import List, Tuple

import pytest

from mathutils import Vector
from yk_gmd_blender.gmdlib.abstract.gmd_shader import GMDVertexBuffer, GMDVertexBufferLayout, VecStorage, \
    VecCompFmt
from yk_gmd_blender.meshlib.vertex_fusion import vertex_fusion, fuse_adjacent_vertices, \
    detect_fully_fused_triangles, decide_on_unfusions, solve_unfusion


def mock_vertex_buffer(pos: List[Vector]) -> GMDVertexBuffer:
    layout = GMDVertexBufferLayout.make_vertex_buffer_layout(
        assume_skinned=False,

        pos_storage=VecStorage(VecCompFmt.Float32, 3),
        weights_storage=None,
        bones_storage=None,
        normal_storage=None,
        tangent_storage=None,
        unk_storage=None,
        col0_storage=None,
        col1_storage=None,
        uv_storages=[],

        packing_flags=0,
    )
    return GMDVertexBuffer(
        layout=layout,

        pos=pos,

        weight_data=None,
        bone_data=None,
        normal=None,
        tangent=None,
        unk=None,
        col0=None,
        col1=None,
        uvs=[],
    )


def mock_idx_buffer(idx: List[int]) -> array.ArrayType:
    return array.array('H', idx)


def mock_unfused_fusion_data(n: int) -> Tuple[List[List[Tuple[int, int]]], List[List[int]], List[List[bool]]]:
    """
    Mocks fuse_adjacent_vertices for one vertex buffer of N vertices, where no fusions take place.
    """

    # List of [(i_buf, i_vtx)]
    fused_idx_to_buf_idx = [[(0, x)] for x in range(n)]
    buf_idx_to_fused_idx = [[x for x in range(n)]]
    is_fused = [[False for x in range(n)]]

    return fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused


def v(x, y, z) -> Vector:
    return Vector((x, y, z))


# Test the top-level vertex fusion function with a simple example.
# Consider the following mesh
#    -A-
#  /  |  \
#  B--CD--E
#  \  |  /
#    -F-
#
# Vertices C and D are in the same place, and for the sake of argument have the same normals,
# but connect to different halves of the mesh: C is only in triangles ABC, BCF; D is only in ADE, DEF.
# In Blender, this would result in C and D having different normals and pointing in different directions,
# because normals are determined by connected faces.
#
# We can resolve this through *vertex fusion*: in this example, we can combine C and D into a single vertex,
# and any differences in per-triangle data (e.g. UVs) won't be a problem, as the fused vertex G can make those values
# different for the different halves of the mesh.
#
# This test makes sure the above mesh results in C and D being fused.
@pytest.mark.order(1)
def test_vertex_fusion_hex_splitcenter():
    vtx_buf = mock_vertex_buffer([
        Vector((0, 1, 0)),  # A
        Vector((1, 0, 0)),  # B
        Vector((0, 0, 0)),  # C
        Vector((0, 0, 0)),  # D
        Vector((-1, 0, 0)),  # E
        Vector((0, -1, 0)),  # F
    ])
    idx_buf = mock_idx_buffer([
        0, 1, 2,  # ABC
        1, 2, 5,  # BCF
        0, 3, 4,  # ADE
        3, 4, 5,  # DEF
    ])

    fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused = vertex_fusion([idx_buf], [vtx_buf])

    assert fused_idx_to_buf_idx == [
        [(0, 0)],  # A indices
        [(0, 1)],  # B indices
        [(0, 2), (0, 3)],  # C + D indices
        [(0, 4)],  # E indices
        [(0, 5)],  # F indices
    ]
    assert len(buf_idx_to_fused_idx) == 1  # only one set of buffers was passed in, only one should be returned
    assert len(is_fused) == 1  # only one set of buffers was passed in, only one should be returned
    assert buf_idx_to_fused_idx == [[
        0,  # A wasn't fused
        1,  # B wasn't fused
        2,  # C wasn't fused (D was fused into C, not the other way around)
        2,  # D was fused into C
        3,  # E has its index shifted back because D doesn't take up a spot
        4,  # ditto for F
    ]]
    assert is_fused == [[
        False,  # A wasn't fused
        False,  # B wasn't fused
        False,  # C wasn't fused (D was fused into C, not the other way around)
        True,  # D was fused into C
        False,  # E wasn't fused
        False,  # F wasn't fused
    ]]


# Test the subfunction fuse_adjacent_vertices
# Simply generate a list of vertices where some have identical data, and assert they are fused
@pytest.mark.order(1)
def test_fuse_adjacent_vertices():
    A = Vector((0, 0, 0))
    B = Vector((0, 1, 0))
    C = Vector((1, 0, 0))
    D = Vector((0, 0, 1))
    vtx_buf = mock_vertex_buffer([
        A,  # 0
        A,  # 1
        B,  # 2
        C,  # 3
        C,  # 4
        D,  # 5
        B,  # 6
        D,  # 7
        D,  # 8
        A,  # 9
    ])

    fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused = fuse_adjacent_vertices([vtx_buf])

    assert fused_idx_to_buf_idx == [
        [(0, 0), (0, 1), (0, 9)],  # A indices
        [(0, 2), (0, 6)],  # B indices
        [(0, 3), (0, 4)],  # C indices
        [(0, 5), (0, 7), (0, 8)],  # D indices
    ]

    assert len(buf_idx_to_fused_idx) == 1  # only one set of buffers was passed in, only one should be returned
    assert len(is_fused) == 1  # only one set of buffers was passed in, only one should be returned
    assert buf_idx_to_fused_idx == [[
        0,
        0,
        1,
        2,
        2,
        3,
        1,
        3,
        3,
        0,
    ]]
    assert is_fused == [[
        False,  # First instance of A
        True,
        False,  # First instance of B
        False,  # First instance of C
        True,
        False,  # First instance of D
        True,
        True,
        True,
        True,
    ]]


@pytest.mark.order(1)
def test_detect_fully_fused_triangles_nofusion():
    idx_buf = mock_idx_buffer([
        0, 1, 2,
        1, 2, 3,
        2, 3, 4,
        3, 4, 5,
        5, 6, 7,
    ])

    fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused = mock_unfused_fusion_data(8)
    fused_dict = detect_fully_fused_triangles(
        [idx_buf],
        fused_idx_to_buf_idx,
        buf_idx_to_fused_idx
    )

    assert fused_dict == {}


@pytest.mark.order(1)
def test_detect_fully_fused_triangles_fusion():
    # Generate a set of vertices, making up four sets of triangles:
    #
    # 1) a single triangle ABC
    # 2) two triangles with vertices in the same points, on top of each other DEF, GHI
    # 3) three triangles with vertices in the same points, on top of each other JKL, MNO, PQR
    # 4) a single triangle STU, with extra unconnected vertices that match the positions of S, T, U

    vtx_buf = mock_vertex_buffer([
        # Set 1)
        Vector((0, 0, 0)),
        Vector((1, 0, 0)),
        Vector((1, 1, 0)),

        # Set 2)
        Vector((0, 0, 1)),
        Vector((1, 0, 1)),
        Vector((1, 1, 1)),
        # ---------------
        Vector((1, 0, 1)),
        Vector((0, 0, 1)),
        Vector((1, 1, 1)),

        # Set 3)
        Vector((0, 0, 2)),
        Vector((1, 0, 2)),
        Vector((1, 1, 2)),
        # ---------------
        Vector((1, 0, 2)),
        Vector((0, 0, 2)),
        Vector((1, 1, 2)),
        # ---------------
        Vector((1, 1, 2)),
        Vector((0, 0, 2)),
        Vector((1, 0, 2)),

        # Set 4)
        Vector((0, 0, 3)),
        Vector((1, 0, 3)),
        Vector((1, 1, 3)),
        Vector((0, 0, 3)),
        Vector((1, 0, 3)),
        Vector((1, 1, 3)),
    ])
    idx_buf = mock_idx_buffer([
        0, 1, 2,

        3, 4, 5,
        6, 7, 8,

        9, 10, 11,
        12, 13, 14,
        15, 16, 17,

        18, 19, 20
    ])

    # Assume the "adjacent" fusions are correct
    fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused = fuse_adjacent_vertices([vtx_buf])

    fused_dict = detect_fully_fused_triangles(
        [idx_buf],
        fused_idx_to_buf_idx,
        buf_idx_to_fused_idx
    )

    assert fused_dict == {
        # First set didn't have their verts fused with anything

        # Second set
        (3, 4, 5): [(0, (3, 4, 5)), (0, (6, 7, 8))],

        # Third set
        (6, 7, 8): [(0, (9, 10, 11)), (0, (12, 13, 14)), (0, (15, 16, 17))],

        # Fourth set - all of (18, 19, 20) from the original *were* fused with something,
        # but those fusions didn't create another triangle
        (9, 10, 11): [(0, (18, 19, 20))],
    }


@pytest.mark.order(1)
def test_decide_on_unfusions_twolayer_interior():
    # Create a large mesh, where the starred verts are duplicated (two layers).
    #   A  B  C
    #  D E* F* G
    # H I* J* L* M
    #  N O* P* Q
    #   R  S  T
    # The triangles between EFIJLOP should all be fused dupes.
    # The unfusion process should only try to unfuse J.

    vtx_buf = mock_vertex_buffer([
        v(-2, 2, 0), v(0, 2, 0), v(2, 2, 0),
        v(-3, 1, 0), v(-1, 1, 0), v(1, 1, 0), v(3, 1, 0),
        v(-4, 0, 0), v(-2, 0, 0), v(0, 0, 0), v(2, 0, 0), v(4, 0, 0),
        v(-3, -1, 0), v(-1, -1, 0), v(1, -1, 0), v(3, -1, 0),
        v(-2, -2, 0), v(0, -2, 0), v(2, -2, 0),

        # duplicates for starred
        v(-1, 1, 0), v(1, 1, 0),
        v(-2, 0, 0), v(0, 0, 0), v(2, 0, 0),
        v(-1, -1, 0), v(1, -1, 0),
    ])
    #     0   1   2
    #   3   4   5   6
    # 7   8   9  10  11
    #  12  13  14  15
    #    16  17  18
    #
    #      19  20
    #    21  22  23
    #      24  25
    idx_buf = mock_idx_buffer([
        # Top row of triangles
        0, 3, 4,
        0, 1, 4,
        1, 4, 5,
        1, 5, 2,
        2, 5, 6,

        # Second row
        3, 7, 8,
        3, 4, 8,
        4, 8, 9,  # fused
        4, 5, 9,  # fused
        5, 9, 10,  # fused
        5, 6, 10,
        6, 10, 11,

        # Third row
        7, 8, 12,
        8, 12, 13,
        8, 9, 13,  # fused
        9, 13, 14,  # fused
        9, 10, 14,  # fused
        10, 14, 15,
        10, 11, 15,

        # Bottom row
        12, 13, 16,
        13, 16, 17,
        13, 14, 17,
        14, 17, 18,
        14, 15, 18,

        # Duplicates
        19, 21, 22,
        19, 20, 22,
        20, 22, 23,
        21, 22, 24,
        22, 24, 25,
        22, 23, 25
    ])

    fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused = fuse_adjacent_vertices([vtx_buf])
    # original indices of duplicate verts: 19..25 inclusive
    # These should be merged with their counterparts
    assert fused_idx_to_buf_idx[4] == [(0, 4), (0, 19)]
    assert fused_idx_to_buf_idx[5] == [(0, 5), (0, 20)]
    assert fused_idx_to_buf_idx[8] == [(0, 8), (0, 21)]
    assert fused_idx_to_buf_idx[9] == [(0, 9), (0, 22)]
    assert fused_idx_to_buf_idx[10] == [(0, 10), (0, 23)]
    assert fused_idx_to_buf_idx[13] == [(0, 13), (0, 24)]
    assert fused_idx_to_buf_idx[14] == [(0, 14), (0, 25)]
    # All others should not be merged
    assert len(fused_idx_to_buf_idx) == 19
    for i, fused_verts in enumerate(fused_idx_to_buf_idx):
        if i not in [4, 5, 8, 9, 10, 13, 14]:
            assert len(fused_verts) == 1

    assert buf_idx_to_fused_idx[0][19] == 4
    assert buf_idx_to_fused_idx[0][20] == 5
    assert buf_idx_to_fused_idx[0][21] == 8
    assert buf_idx_to_fused_idx[0][22] == 9
    assert buf_idx_to_fused_idx[0][23] == 10
    assert buf_idx_to_fused_idx[0][24] == 13
    assert buf_idx_to_fused_idx[0][25] == 14

    assert is_fused == [([False] * 19 + [True] * 7)]

    fully_fused_tri_set = detect_fully_fused_triangles(
        [idx_buf],
        fused_idx_to_buf_idx,
        buf_idx_to_fused_idx
    )
    assert fully_fused_tri_set == {
        (4, 8, 9): [(0, (4, 8, 9)), (0, (19, 21, 22))],
        (4, 5, 9): [(0, (4, 5, 9)), (0, (19, 20, 22))],
        (5, 9, 10): [(0, (5, 9, 10)), (0, (20, 22, 23))],
        (8, 9, 13): [(0, (8, 9, 13)), (0, (21, 22, 24))],
        (9, 13, 14): [(0, (9, 13, 14)), (0, (22, 24, 25))],
        (9, 10, 14): [(0, (9, 10, 14)), (0, (22, 23, 25))],
    }

    unfusions = decide_on_unfusions(
        [idx_buf],
        fused_idx_to_buf_idx,
        fully_fused_tri_set
    )
    assert unfusions == {
        (0, 9): {(0, 22)},
        (0, 22): {(0, 9)},
    }


@pytest.mark.order(1)
def test_decide_on_unfusions_twolayer_interior_twoseam():
    # Create a large mesh, where the starred verts are duplicated (two layers).
    #   A  B  C
    #  D E* F* G
    # H I* J* L* M
    #  N O* P* Q
    #   R  S  T
    # The triangles between EFIJLOP should all be fused dupes.
    # The unfusion process should only try to unfuse J.
    # Also, split the mesh into two buffers with a seam along the c--r diagonal

    vtx_buf_0 = mock_vertex_buffer([
        v(-2, 2, 0), v(0, 2, 0), v(2, 2, 0),
        v(-3, 1, 0), v(-1, 1, 0), v(1, 1, 0),  # v(3, 1, 0),
        v(-4, 0, 0), v(-2, 0, 0), v(0, 0, 0),  # v(2, 0, 0), v(4, 0, 0),
        v(-3, -1, 0), v(-1, -1, 0),  # v(1, -1, 0), v(3, -1, 0),
        v(-2, -2, 0),  # v(0, -2, 0), v(2, -2, 0),

        # duplicates for starred
        v(-1, 1, 0), v(1, 1, 0),
        v(-2, 0, 0), v(0, 0, 0),  # v(2, 0, 0),
        v(-1, -1, 0),  # v(1, -1, 0),
    ])
    vtx_buf_1 = mock_vertex_buffer([
        v(2, 2, 0),
        v(1, 1, 0), v(3, 1, 0),
        v(0, 0, 0), v(2, 0, 0), v(4, 0, 0),
        v(-1, -1, 0), v(1, -1, 0), v(3, -1, 0),
        v(-2, -2, 0), v(0, -2, 0), v(2, -2, 0),

        # duplicates for starred
        v(1, 1, 0),
        v(0, 0, 0), v(2, 0, 0),
        v(-1, -1, 0), v(1, -1, 0),
    ])
    #     0   1   2
    #   3   4   5   x
    # 6   7   8  xx  xx
    #   9  10  xx  xx
    #    11  xx  xx
    #
    #      12  13
    #    14  15  xx
    #      16  xx
    idx_buf_0 = mock_idx_buffer([
        # Top row of triangles
        0, 3, 4,
        0, 1, 4,
        1, 4, 5,
        1, 5, 2,

        # Second row
        3, 6, 7,
        3, 4, 7,
        4, 7, 8,  # fused
        4, 5, 8,  # fused

        # Third row
        6, 7, 9,
        7, 9, 10,
        7, 8, 10,  # fused

        # Bottom row
        9, 10, 11,

        # Duplicates
        12, 14, 15,
        12, 13, 15,
        14, 15, 16,
    ])
    #     x   x   0
    #   x   x   1   2
    # x   x   3   4   5
    #  xx   6   7   8
    #     9  10  11
    #
    #      xx  12
    #    xx  13  14
    #      15  16
    idx_buf_1 = mock_idx_buffer([
        # Top row of triangles
        0, 1, 2,

        # Second row
        1, 3, 4,  # fused
        1, 2, 4,
        2, 4, 5,

        # Third row
        3, 6, 7,  # fused
        3, 4, 7,  # fused
        4, 7, 8,
        4, 5, 8,

        # Bottom row
        6, 9, 10,
        6, 7, 10,
        7, 10, 11,
        7, 8, 11,

        # Duplicates
        12, 13, 14,
        13, 15, 16,
        13, 14, 16
    ])

    fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused = fuse_adjacent_vertices([vtx_buf_0, vtx_buf_1])
    # seam indices: (0, {2,5,8,10,11,13,15,16}), (1, {0,1,3,6,9,12,13,15}) should be fused with each other
    fusions = [
        # seam not including EFIJLOP: (0, {2,11}), (1, {0,9})
        [(0, 2), (1, 0)],
        [(0, 11), (1, 9)],
        # EFIJLOP: (0, {4,5,7,8,-,10,-}), (0, {12,13,14,15,-,16,-}), (1, {-,1,-,3,4,6,7}), (1, {-,12,-,13,14,15,16}) should be fused with each other
        [(0, 4), (0, 12)],
        [(0, 5), (0, 13), (1, 1), (1, 12)],
        [(0, 7), (0, 14)],
        [(0, 8), (0, 15), (1, 3), (1, 13)],
        [(1, 4), (1, 14)],
        [(0, 10), (0, 16), (1, 6), (1, 15)],
        [(1, 7), (1, 16)]
    ]
    # not-fused: (0, {0,1,3,6,9}), (1,{2,5,8,10,11})
    expected = sorted(fusions + [
        [(0, 0)],
        [(0, 1)],
        [(0, 3)],
        [(0, 6)],
        [(0, 9)],
        [(1, 2)],
        [(1, 5)],
        [(1, 8)],
        [(1, 10)],
        [(1, 11)],
    ], key=lambda x: x[0])
    assert fused_idx_to_buf_idx == expected

    # just assume these are right, i'm tired
    # assert buf_idx_to_fused_idx[0][19] == 4
    # assert buf_idx_to_fused_idx[0][20] == 5
    # assert buf_idx_to_fused_idx[0][21] == 8
    # assert buf_idx_to_fused_idx[0][22] == 9
    # assert buf_idx_to_fused_idx[0][23] == 10
    # assert buf_idx_to_fused_idx[0][24] == 13
    # assert buf_idx_to_fused_idx[0][25] == 14
    # assert is_fused == [([False] * 19 + [True] * 7)]

    fully_fused_tri_set = detect_fully_fused_triangles(
        [idx_buf_0, idx_buf_1],
        fused_idx_to_buf_idx,
        buf_idx_to_fused_idx
    )
    assert sorted(fully_fused_tri_set.values(), key=lambda x: x[0]) == [
        [(0, (4, 5, 8)), (0, (12, 13, 15))],
        [(0, (4, 7, 8)), (0, (12, 14, 15))],
        [(0, (7, 8, 10)), (0, (14, 15, 16))],
        [(1, (1, 3, 4)), (1, (12, 13, 14))],
        [(1, (3, 4, 7)), (1, (13, 14, 16))],
        [(1, (3, 6, 7)), (1, (13, 15, 16))],
    ]

    unfusions = decide_on_unfusions(
        [idx_buf_0, idx_buf_1],
        fused_idx_to_buf_idx,
        fully_fused_tri_set
    )
    assert unfusions == {
        (0, 8): {(0, 15)},
        (0, 15): {(0, 8)},
        (1, 3): {(1, 13)},
        (1, 13): {(1, 3)}
    }


# Test unfusion where one of the layers has a split vertex
@pytest.mark.order(1)
def test_decide_on_unfusions_twolayer_splitvtx():
    # Create a mesh like the final example in the decode_on_unfusions documentation
    #         -A---E
    #        B---CD--F
    #        | | | | |
    # 1|  -X-|-A'|-E'|
    # 0| Y---B'--C'--F'
    #   --------------
    #    0 1 2 3 4 5 6
    # Triangles: ABC, ACE, DEF, A'B'C', A'C'E', C'E'F', XYB', XA'B'
    # Fully fused triangles: ABC/A'B'C', ACE/A'C'E', DEF/C'E'F'
    # The triangles between ABCDEF should all be fused dupes.
    # The unfusion process should unfuse {C, C'}, {D, C'}, {E, E'}, {F, F'}

    vtx_buf = mock_vertex_buffer([
        # Top layer - 0..5 incl
        v(3, 1, 0),  # A  0
        v(2, 0, 0),  # B  1
        v(4, 0, 0),  # C  2
        v(4, 0, 0),  # D  3
        v(5, 1, 0),  # E  4
        v(6, 0, 0),  # F  5

        # Bottom layer - 6..10 incl
        v(3, 1, 0),  # A' 6
        v(2, 0, 0),  # B' 7
        v(4, 0, 0),  # C' 8
        v(5, 1, 0),  # E' 9
        v(6, 0, 0),  # F' 10

        # XY - 11, 12
        v(1, 1, 0),  # X  11
        v(0, 0, 0),  # Y  12
    ])
    idx_buf = mock_idx_buffer([
        0, 1, 2,  # ABC
        0, 2, 4,  # ACE
        3, 4, 5,  # DEF

        6, 7, 8,  # A'B'C'
        6, 8, 9,  # A'C'E'
        8, 9, 10,  # C'E'F'

        11, 12, 7,  # XYB'
        11, 6, 7,  # XA'B'
    ])

    fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused = fuse_adjacent_vertices([vtx_buf])
    # original indices of duplicate verts: 19..25 inclusive
    # These should be fused with their counterparts
    assert fused_idx_to_buf_idx[0] == [(0, 0), (0, 6)]
    assert fused_idx_to_buf_idx[1] == [(0, 1), (0, 7)]
    assert sorted(fused_idx_to_buf_idx[2]) == [(0, 2), (0, 3), (0, 8)]  # C, D, C' are adjacent
    assert fused_idx_to_buf_idx[3] == [(0, 4), (0, 9)]
    assert fused_idx_to_buf_idx[4] == [(0, 5), (0, 10)]
    # All others should not be fused with anything
    assert len(fused_idx_to_buf_idx) == 7
    for i, fused_verts in enumerate(fused_idx_to_buf_idx):
        if i not in range(5):
            assert len(fused_verts) == 1

    assert buf_idx_to_fused_idx == [[
        0,  # A
        1,  # B
        2,  # C
        2,  # D -> C
        3,  # E
        4,  # F

        0, 1, 2, 3, 4,  # A'..F' -> A..F

        5, 6  # X, Y
    ]]

    assert is_fused == [[
        False,  # A
        False,  # B
        False,  # C
        True,  # D -> C
        False,  # E
        False,  # F

        True, True, True, True, True,  # A'..F' -> A..F

        False, False  # X, Y
    ]]

    fully_fused_tri_set = detect_fully_fused_triangles(
        [idx_buf],
        fused_idx_to_buf_idx,
        buf_idx_to_fused_idx
    )
    # Fully fused triangles: ABC/A'B'C', ACE/A'C'E', DEF/C'E'F'
    assert fully_fused_tri_set == {
        # Fused ABC
        (0, 1, 2): [(0, (0, 1, 2)), (0, (6, 7, 8))],
        # Fused ACE
        (0, 2, 3): [(0, (0, 2, 4)), (0, (6, 8, 9))],
        # Fused CEF
        (2, 3, 4): [(0, (3, 4, 5)), (0, (8, 9, 10))],
    }

    unfusions = decide_on_unfusions(
        [idx_buf],
        fused_idx_to_buf_idx,
        fully_fused_tri_set
    )
    # The unfusion process should unfuse {C, C'}, {D, C'}, {E, E'}, {F, F'}
    assert unfusions == {
        (0, 2): {(0, 8)},  # C from C'
        (0, 3): {(0, 8)},  # D from C'
        (0, 4): {(0, 9)},  # E from E'
        (0, 5): {(0, 10)},  # F from F'
        (0, 8): {(0, 2), (0, 3)},  # C' from C, D
        (0, 9): {(0, 4)},  # E' from E
        (0, 10): {(0, 5)},  # F' from F
    }


@pytest.mark.order(1)
def test_detect_fully_fused_triangles():
    # triangles that are "fully fused" i.e. cause issues with blender don't necessarily have all their vertices fused
    # e.g.
    #   -A
    #  B |\
    #  |-A'\
    #  B'--C
    # ABC and A'B'C can't be represented in blender if A/A' and B/B' are fused
    # because they resolve to the same fused vertices

    vtx_buf = mock_vertex_buffer([
        v(1, 1, 0),  # A  0
        v(0, 0, 0),  # B  1
        v(2, 0, 0),  # C  2
        v(1, 1, 0),  # A' 3
        v(0, 0, 0),  # B' 4
    ])
    idx_buf = mock_idx_buffer([
        0, 1, 2,  # ABC
        2, 3, 4,  # A'B'C
    ])

    fused_idx_to_buf_idx, buf_idx_to_fused_idx, is_fused = fuse_adjacent_vertices([vtx_buf])
    assert fused_idx_to_buf_idx == [
        [(0, 0), (0, 3)],  # A/A'
        [(0, 1), (0, 4)],  # B/B'
        [(0, 2)],  # C
    ]
    assert buf_idx_to_fused_idx == [[
        0,  # A
        1,  # B
        2,  # C
        0,  # A' -> A
        1,  # B' -> B
    ]]
    assert is_fused == [[
        False,
        False,
        False,
        True,
        True
    ]]

    fully_fused_tri_set = detect_fully_fused_triangles(
        [idx_buf],
        fused_idx_to_buf_idx,
        buf_idx_to_fused_idx
    )
    # Fully fused triangles: ABC/A'B'C
    assert fully_fused_tri_set == {
        (0, 1, 2): [(0, (0, 1, 2)), (0, (2, 3, 4))],
    }


# TODO more tests for solve_unfusion
@pytest.mark.order(1)
def test_complex_unfusion():
    # Test the case of four vertices which would be fused, but are really in two layers:
    #    AB
    #    |
    #   A'B'
    #
    # A/A' and B/B' should be unfused
    # The outcome should be two groups, where no groups have A and A' or B and B'
    vtx_buf = mock_vertex_buffer([
        v(0, 0, 0),  # A
        v(0, 0, 0),  # A'
        v(0, 0, 0),  # B
        v(0, 0, 0),  # B'
    ])
    old_fused_idx_to_buf_idx = [
        [(0, 0), (0, 1), (0, 2), (0, 3)]
    ]
    unfuse_verts_with = {
        (0, 0): {(0, 1)},
        (0, 1): {(0, 0)},
        (0, 2): {(0, 3)},
        (0, 3): {(0, 2)},
    }
    fused_idx_to_buf_idx, _, _ = solve_unfusion([vtx_buf], old_fused_idx_to_buf_idx, unfuse_verts_with)
    assert len(fused_idx_to_buf_idx) == 2
    for fused_vert_group in fused_idx_to_buf_idx:
        for vert in fused_vert_group:
            for vert_prime in unfuse_verts_with[vert]:
                assert vert_prime not in fused_vert_group
