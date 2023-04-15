import pytest

from yk_gmd_blender.meshlib.export_submeshing import MeshLoopIdx, dedupe_loops


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
    assert deduped_verts == [0, 1, 2, 3, 4, 5]
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
    assert deduped_verts == [0, 3]
    assert deduped_dict == {
        100: 0,
        101: 0,
        102: 0,
        103: 1,
        104: 1,
        105: 1,
    }
