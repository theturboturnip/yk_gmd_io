#!/usr/bin/env python
import os
import shutil
import subprocess
from pathlib import Path

import pytest

import compare
from conftest import GMDTest
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import LenientErrorReporter, StrictErrorReporter


@pytest.mark.order(1)
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
        "YKGMDIO_SKINNED": str(gmdtest.skinned),
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
    compare.compare_files(gmdtest.src, gmdtest.dst, gmdtest.skinned, vertices=True,
                          error=LenientErrorReporter(allowed_categories=set()))


@pytest.mark.order(2)
def test_gmd_compare_strict(gmdtest: GMDTest, blender: Path, isolate_blender: bool):
    compare.compare_files(gmdtest.src, gmdtest.dst, gmdtest.skinned, vertices=True,
                          error=StrictErrorReporter(allowed_categories=set()))
