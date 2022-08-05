import array
from typing import List, Tuple

import pytest

from mathutils import Vector
from yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer_Generic, GMDVertexBufferLayout, VecStorage
from yk_gmd_blender.blender.importer.mesh.vertex_fusion import vertex_fusion, fuse_adjacent_vertices, \
    detect_fully_fused_triangles, decide_on_unfusions


def mock_vertex_buffer(pos: List[Vector]) -> GMDVertexBuffer_Generic:
    layout = GMDVertexBufferLayout.make_vertex_buffer_layout(
        assume_skinned=False,

        pos_storage=VecStorage.Vec3Full,
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
    return GMDVertexBuffer_Generic(
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

    buf_idx_to_fused_idx, is_fused = vertex_fusion([idx_buf], [vtx_buf])

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
def test_decide_on_unfusions_twolayerinterior():
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
        buf_idx_to_fused_idx,
        fully_fused_tri_set
    )
    assert unfusions == {
        (0, 9): ((0, 22),),
        (0, 22): ((0, 9),),
    }

# TODO test unfusion where one of the layers has a split vertex
