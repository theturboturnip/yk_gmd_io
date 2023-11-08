#!/usr/bin/env python
import os
import shutil
import subprocess
from pathlib import Path

import pytest

import compare
from conftest import GMDTest
from yk_gmd_blender.gmdlib.errors.error_reporter import LenientErrorReporter, StrictErrorReporter

# Filter out specific fatal errors for specific files
COMPARE_FILTER = {
    ("yk1_stage", "st_sera_dead.gmd"): [
        # box02 is a really weird mesh that has 5 vertices in the same place,
        # two of which participate in the same triangle (functionally a degenerate triangle)
        # and this message complains that some of those triangles don't survive. Boo hoo.
        "static > node000152 > node000150 > node000148 > node000140 > node000141 > box02 > attr set s_cnc_wxqi01_ig_d "
        "src (760 unique verts) and dst (636 unique verts) exact data differs",
        # these "line" meshes are overly detailed screws, with two instances of vertices that have
        # 1) different UVs 2) equal positions 3) share a triangle, which could never be visible because of 2) and 3).
        "static > node000152 > node000150 > node000148 > node000140 > node000141 > line0",
        # same base mesh
        "static > node000152 > node000150 > node000148 > node000140 > node000141 > object1570 > "
        "attr set s_met_plan05_ig_d src (292 unique verts) and dst (288 unique verts) exact data differs",
        "static > node000152 > node000150 > node000148 > node000140 > node000141 > object1571 > "
        "attr set s_met_plan05_ig_d src (292 unique verts) and dst (288 unique verts) exact data differs",
    ],
    ("y0-Skinned", "c_at_kiryu.gmd"): [
        # The leather shoes have the same issue as yk1 st_sera_dead - triangles that are effectively degenerate
        # whose vertices disappear
        "[l0]shoes_leather > attr set c_am_kiryu_shoes_di "
        "src (1202 unique verts) and dst (1192 unique verts) exact data differs"
    ]
}


@pytest.mark.order(10)
def test_gmd(gmdtest: GMDTest, blender: Path, isolate_blender: bool):
    if gmdtest.animation:
        gmd_importanim(gmdtest, blender, isolate_blender)
    else:
        gmd_importexport_comparelenient(gmdtest, blender, isolate_blender)


def gmd_importanim(gmdtest: GMDTest, blender: Path, isolate_blender: bool):
    # Set the src/dst for the import/export
    env = os.environ.copy()
    env.update({
        "YKGMDIO_TEST_SRC": str(gmdtest.src),
        "YKGMDIO_SKINNED": str(gmdtest.skinned_method),
        "YKGMDIO_LOGGING": gmdtest.logging,
    })

    SCRIPTLOC = os.path.dirname(__file__)

    # Run blender and import/export the file
    if isolate_blender:
        subprocess.run([
            str(blender / "blender"),
            "--factory-startup",
            "-b",
            "--python-exit-code", "1",
            "-P", f"{SCRIPTLOC}/blender_do_importanim.py"
        ], check=True, env=env)
    else:
        subprocess.run([
            str(blender / "blender"),
            "-b",
            "--python-exit-code", "1",
            "-P", f"{SCRIPTLOC}/blender_do_importanim.py"
        ], check=True, env=env)


def gmd_importexport_comparelenient(gmdtest: GMDTest, blender: Path, isolate_blender: bool):
    # Create subfolder in output for directory
    gmdtest.dst.parent.mkdir(parents=True, exist_ok=True)
    # Copy the file into the output - this should be overwritten by blender
    shutil.copyfile(gmdtest.src, gmdtest.dst)

    # Set the src/dst for the import/export
    env = os.environ.copy()
    env.update({
        "YKGMDIO_TEST_SRC": str(gmdtest.src),
        "YKGMDIO_TEST_DST": str(gmdtest.dst),
        "YKGMDIO_SKINNED": str(gmdtest.skinned_method),
        "YKGMDIO_LOGGING": gmdtest.logging,
    })

    SCRIPTLOC = os.path.dirname(__file__)

    # Run blender and import/export the file
    if isolate_blender:
        subprocess.run([
            str(blender / "blender"),
            "--factory-startup",
            "-b",
            "--python-exit-code", "1",
            "-P", f"{SCRIPTLOC}/blender_do_importexport.py"
        ], check=True, env=env)
    else:
        subprocess.run([
            str(blender / "blender"),
            "-b",
            "--python-exit-code", "1",
            "-P", f"{SCRIPTLOC}/blender_do_importexport.py"
        ], check=True, env=env)

    # Compare the import/export
    compare.compare_files(gmdtest.src, gmdtest.dst, bool(gmdtest.skinned_method), vertices=True,
                          error=LenientErrorReporter(allowed_categories=set()),
                          strict=False, mismatch_filter=COMPARE_FILTER.get((gmdtest.src.parent.name, gmdtest.src.name)))


@pytest.mark.order(20)
def test_gmd_compare_strict(gmdtest: GMDTest, blender: Path, isolate_blender: bool):
    compare.compare_files(gmdtest.src, gmdtest.dst, bool(gmdtest.skinned_method), vertices=True,
                          error=StrictErrorReporter(allowed_categories=set()),
                          strict=True, mismatch_filter=COMPARE_FILTER.get((gmdtest.src.parent.name, gmdtest.src.name)))
