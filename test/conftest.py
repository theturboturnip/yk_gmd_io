import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--blender",
        help="Path to blender folder, in which to install <addon>",
    )
    parser.addoption(
        "--blender_ver",
        help="Blender version number (i.e. 3.2, 3.4) which is where to install the addon"
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
        "--isolate_blender",
        action="store_true",
        help="Should we isolate the blender install from the rest of the system & install the addon directly?"
    )
    parser.addoption(
        "--test_all_skinned",
        action="store_true",
        help="Should we test all methods for calculating skinned matrices"
    )
    parser.addoption(
        "--test_animation",
        action="store_true",
        help="Should animation import method be tested"
    )
    parser.addoption(
        "--blender_logging",
        help="Logging categories to enable. Can be empty."
    )


@dataclass(frozen=True)
class GMDTest:
    src: Path
    dst: Path
    animation: bool
    skinned_method: str
    logging: str

    def __str__(self):
        return f"{self.src.parent.name}/{self.src.name}" + \
               (
                   f"-skin{self.skinned_method}" if self.skinned_method else ""
               ) + (
                   f"-log{self.logging}" if self.logging else "-nolog"
               ) + (
                   f"-importanim" if self.animation else ""
               )


@pytest.fixture
def blender(request):
    return Path(request.config.getoption("blender"))


@pytest.fixture
def isolate_blender(request):
    return bool(request.config.getoption("--isolate_blender"))


def pytest_generate_tests(metafunc):
    if "gmdtest" in metafunc.fixturenames:
        model_root_dir = Path(metafunc.config.getoption("model_root_dir"))
        output_dir = Path(metafunc.config.getoption("output_dir"))
        logging = metafunc.config.getoption("blender_logging")
        test_all_skinned = metafunc.config.getoption("--test_all_skinned")
        test_animation = metafunc.config.getoption("--test_animation")

        assert model_root_dir
        assert output_dir

        gmdtests = []
        sys.stderr.write(f"Considering root {model_root_dir}\n")
        for model_dir in model_root_dir.iterdir():
            sys.stderr.write(f"Considering {model_dir}: (is_dir {model_dir.is_dir()})")
            if not model_dir.is_dir():
                continue
            skinned = "-Skinned" in model_dir.name
            for model in model_dir.iterdir():
                if not model.name.endswith(".gmd"):
                    continue
                if skinned:
                    gmdtests.append(GMDTest(
                        src=model,
                        dst=output_dir / model_dir.name / model.name,
                        skinned_method="CALCULATE",
                        animation=False,
                        logging=logging
                    ))
                    if test_all_skinned:
                        gmdtests.append(GMDTest(
                            src=model,
                            dst=output_dir / model_dir.name / model.name,
                            skinned_method="FROM_TARGET_FILE",
                            animation=False,
                            logging=logging
                        ))
                        gmdtests.append(GMDTest(
                            src=model,
                            dst=output_dir / model_dir.name / model.name,
                            skinned_method="FROM_ORIGINAL_GMD_IMPORT",
                            animation=False,
                            logging=logging
                        ))
                    if test_animation:
                        gmdtests.append(GMDTest(
                            src=model,
                            dst=output_dir / model_dir.name / model.name,
                            skinned_method="CALCULATE",
                            animation=True,
                            logging=logging
                        ))
                else:
                    gmdtests.append(GMDTest(
                        src=model,
                        dst=output_dir / model_dir.name / model.name,
                        skinned_method="",
                        animation=False,
                        logging=logging
                    ))
                    if test_animation:
                        gmdtests.append(GMDTest(
                            src=model,
                            dst=output_dir / model_dir.name / model.name,
                            skinned_method="",
                            animation=True,
                            logging=logging
                        ))

        # Sort by filesize, to get quick files out of the way first
        gmdtests.sort(key=lambda gmdtest: os.path.getsize(gmdtest.src))

        metafunc.parametrize("gmdtest", gmdtests, ids=str)


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    blender = Path(session.config.getoption("blender"))
    blender_ver = session.config.getoption("blender_ver")
    isolate_blender = bool(session.config.getoption("--isolate_blender"))
    addon = Path(session.config.getoption("addon"))

    if isolate_blender:
        if not blender_ver:
            raise RuntimeError("Can't figure out which folder to install the script in - set --blender_ver")
        # Extract the addon into Blender's addons directory
        addon_extract_path = blender / blender_ver / "scripts" / "addons"

        # Delete the old one first
        addon_output_path = (addon_extract_path / "yk_gmd_blender")
        if addon_output_path.is_dir():
            shutil.rmtree(addon_output_path)

        import zipfile
        with zipfile.ZipFile(addon, "r") as zip_ref:
            zip_ref.extractall(addon_extract_path)
    else:
        # Ask blender to install the addon itself
        SCRIPTLOC = os.path.dirname(__file__)
        env = os.environ.copy()
        env.update({
            "YKGMDIO_TEST_ADDON": str(addon)
        })
        subprocess.run([
            str(blender / "blender"),
            "-b",
            "--python-exit-code", "1",
            "-P", f"{SCRIPTLOC}/blender_install_addon.py"
        ], check=True, env=env)


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    blender = Path(session.config.getoption("blender"))
    blender_ver = session.config.getoption("blender_ver")
    isolate_blender = bool(session.config.getoption("--isolate_blender"))

    # Remove the addon
    if isolate_blender:
        if not blender_ver:
            raise RuntimeError("Can't figure out which folder to install the script in - set --blender_ver")
        addon_output_path = blender / blender_ver / "scripts" / "addons"
        if addon_output_path.is_dir():
            shutil.rmtree(addon_output_path)
    else:
        # Ask blender to uninstall the addon itself
        SCRIPTLOC = os.path.dirname(__file__)
        subprocess.run([
            str(blender / "blender"),
            "-b",
            "--python-exit-code", "1",
            "-P", f"{SCRIPTLOC}/blender_uninstall_addon.py"
        ], check=True)
