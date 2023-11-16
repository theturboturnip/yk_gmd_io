import cProfile
import pstats
from typing import TypeVar, Callable

import bpy

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
        stats.print_stats(100)
    return retval


profile(
    bpy.ops.import_scene.gmd_skinned,
    filepath="..."
)
