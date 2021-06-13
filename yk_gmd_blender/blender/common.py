from typing import Tuple, Iterable, Union

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene

def uv_yk_to_blender_space(uv: Tuple[float, float]):
    return (uv[0], 1 - uv[1])

def uv_make_01(x):
    # Could be done with math.fmod(x, 1.0) but IDK if that would work right with negative numbers
    while x < 0.0:
        x += 1.0
    while x > 1.0:
        x -= 1.0
    return x

def uv_blender_to_yk_space(uv: Tuple[float, float]):
    return (uv_make_01(uv[0]), uv_make_01(1 - uv[1]))

def root_name_for_gmd_file(gmd_file: GMDScene):
    return f"{gmd_file.name}"

def armature_name_for_gmd_file(gmd_file: Union[GMDScene, str]):
    if isinstance(gmd_file, GMDScene):
        return f"{gmd_file.name}_armature"
    else:
        return f"{gmd_file}_armature"
#
# def material_name(material: GMDMaterial):
#     return f"yakuza{material.id:02d}_{material.shader_name}"

def arithmetic_mean(items: Iterable, sum_start=0):
    count = 0
    s = sum_start
    for i in items:
        s += i
        count += 1
    return s / count