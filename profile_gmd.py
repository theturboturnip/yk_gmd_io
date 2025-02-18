import argparse
import cProfile
import pstats
from pathlib import Path
from typing import TypeVar, Callable

from .yk_gmd_blender.gmdlib.converters.common.to_abstract import FileImportMode, VertexImportMode
from .yk_gmd_blender.gmdlib.errors.error_reporter import LenientErrorReporter
from .yk_gmd_blender.gmdlib.io import read_gmd_structures, read_abstract_scene_from_filedata_object, \
    pack_abstract_scene, pack_file_data

T = TypeVar('T')


def profile(func: Callable[..., T], *args, **kwargs) -> T:
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        retval = func(*args, **kwargs)
    finally:
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats("cumtime")
        stats.print_stats(10)
    return retval


def import_file(path: Path, skinned: bool, error: LenientErrorReporter):
    version_props, header, file_data = read_gmd_structures(path, error)
    scene = read_abstract_scene_from_filedata_object(version_props,
                                                     FileImportMode.SKINNED if skinned else FileImportMode.UNSKINNED,
                                                     VertexImportMode.IMPORT_VERTICES,
                                                     file_data, error)

    return version_props, header, file_data, scene


def export_file(version_props, file_data, scene, error: LenientErrorReporter):
    unabstracted_file_data = pack_abstract_scene(version_props, file_data.file_is_big_endian(),
                                                 file_data.vertices_are_big_endian(), scene, file_data, error)
    return pack_file_data(version_props, unabstracted_file_data, error)


def main():
    parser = argparse.ArgumentParser("GMD Poker")

    parser.add_argument("to_profile", choices=["import", "export", "import_export"],
                        help="Choose whether to profile import, export, or both.")
    parser.add_argument("input_file", type=Path)
    parser.add_argument("--skinned", action="store_true")

    args = parser.parse_args()

    error = LenientErrorReporter()

    if args.to_profile in ["import", "import_export"]:
        version_props, header, file_data, scene = profile(import_file, args.input_file, args.skinned, error)
    else:
        version_props, header, file_data, scene = import_file(args.input_file, args.skinned, error)

    if args.to_profile in ["import_export", "export"]:
        profile(export_file, version_props, file_data, scene, error)


if __name__ == '__main__':
    main()
