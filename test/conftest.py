import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


def pytest_addoption(parser):
    parser.addoption(
        "--blender",
        help="Path to blender folder, in which to install <addon>",
    )
    parser.addoption(
        "--addon",
        help="Path of addon ZIP",
    )
    parser.addoption(
        "--model_root_dir",
        help="Path to models folder, containing folders of GMDs",
    )
    parser.addoption(
        "--output_dir",
        help="Path to output directory, including re-exported GMDs"
    )
    parser.addoption(
        "--isolate-blender",
        action="store_true",
        help="Should we isolate the blender install from the rest of the system & install the addon directly?"
    )


@dataclass(frozen=True)
class GMDTest:
    src: Path
    dst: Path
    skinned: bool


def pytest_generate_tests(metafunc):
    assert metafunc.config.getoption("blender")
    blender = Path(metafunc.config.getoption("blender"))
    isolate_blender = bool(metafunc.config.getoption("--isolate-blender"))
    model_root_dir = Path(metafunc.config.getoption("model_root_dir"))
    output_dir = Path(metafunc.config.getoption("output_dir"))

    gmdtests = []
    for model_dir in model_root_dir.iterdir():
        if not model_dir.is_dir():
            continue
        skinned = "-Skinned" in model_dir.name
        for model in model_dir.iterdir():
            if not model.name.endswith(".gmd"):
                continue
            gmdtests.append(GMDTest(
                src=model,
                dst=output_dir / model_dir.name / model.name,
                skinned=skinned
            ))
    metafunc.parametrize("blender", [blender], ids=[""])
    metafunc.parametrize("isolate_blender", [isolate_blender], ids=[""])
    metafunc.parametrize("gmdtest", gmdtests, ids=lambda gmdtest: gmdtest.src.name)


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    blender = Path(session.config.getoption("blender"))
    isolate_blender = bool(session.config.getoption("--isolate-blender"))
    addon = Path(session.config.getoption("addon"))

    if isolate_blender:
        # Extract the addon into Blender's addons directory
        addon_extract_path = blender / "3.2" / "scripts" / "addons"

        # Delete the old one first
        addon_output_path = (addon_extract_path / "yk_gmd_blender")
        if addon_output_path.is_dir():
            shutil.rmtree(addon_output_path)

        import zipfile
        with zipfile.ZipFile(addon, "r") as zip_ref:
            zip_ref.extractall(addon_extract_path)
    else:
        # Ask blender to install the addon itself
        subprocess.run([
            str(blender / "blender"),
            "-b",
            "--python-exit-code", "1",
            "--python-expr", f"import bpy; bpy.ops.preferences.addon_install(filepath='{str(addon)}')"
        ], check=True)


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    blender = Path(session.config.getoption("blender"))
    isolate_blender = bool(session.config.getoption("--isolate-blender"))

    # Remove the addon
    if isolate_blender:
        addon_output_path = blender / "3.2" / "scripts" / "addons" / "yk_gmd_blender"
        if addon_output_path.is_dir():
            shutil.rmtree(addon_output_path)
    else:
        # Ask blender to uninstall the addon itself
        uninstall_py = f"import bpy\n" \
                       f"with bpy.context.temp_override(area=bpy.data.screens[\"Layout\"].areas[0]):\n" \
                       f"    bpy.ops.preferences.addon_remove(module='yk_gmd_blender')"
        subprocess.run([
            str(blender / "blender"),
            "-b",
            "--python-exit-code", "1",
            "--python-expr", uninstall_py
        ], check=True)
