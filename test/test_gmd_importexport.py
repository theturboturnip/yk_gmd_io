#!/usr/bin/env python
import os
import shutil
import subprocess
from pathlib import Path
from typing import NoReturn, List, Optional

import pytest

import compare
from conftest import GMDTest
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import LenientErrorReporter, StrictErrorReporter, ErrorReporter

# Filter out specific fatal errors for specific files
COMPARE_FILTER = {
    "st_sera_dead.gmd": [
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
    ]
}


class FilteredErrorReporter(ErrorReporter):
    error: ErrorReporter
    filtered_out_fatals: List[str]

    def __init__(self, error: ErrorReporter, filtered_out_fatals: Optional[List[str]]):
        self.error = error
        self.filtered_out_fatals = filtered_out_fatals or []

    def recoverable(self, msg: str):
        self.error.recoverable(msg)

    def fatal_exception(self, ex: Exception) -> NoReturn:
        self.error.fatal_exception(ex)

    def fatal(self, msg: str) -> NoReturn:
        if any(msg.startswith(x) for x in self.filtered_out_fatals):
            self.error.recoverable(f"Filtered out: {msg}")
        else:
            self.error.fatal(msg)

    def info(self, msg: str):
        self.error.info(msg)

    def debug(self, category: str, msg: str) -> bool:
        return self.error.debug(category, msg)


@pytest.mark.order(10)
def test_gmd_importexport_comparelenient(gmdtest: GMDTest, blender: Path, isolate_blender: bool):
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
                          error=FilteredErrorReporter(LenientErrorReporter(allowed_categories=set()),
                                                      COMPARE_FILTER.get(gmdtest.src.name)))


@pytest.mark.order(20)
def test_gmd_compare_strict(gmdtest: GMDTest, blender: Path, isolate_blender: bool):
    compare.compare_files(gmdtest.src, gmdtest.dst, bool(gmdtest.skinned_method), vertices=True,
                          error=FilteredErrorReporter(StrictErrorReporter(allowed_categories=set()),
                                                      COMPARE_FILTER.get(gmdtest.src.name)))
