import argparse
import glob
from pathlib import Path

from yk_gmd_blender.yk_gmd.v2.io import read_gmd_structures

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("glob_folder", type=Path)

    args = parser.parse_args()

    all_attrs = set()
    shader_unk1 = {}
    shader_texcount = {}

    file_flags = set()

    for gmd_path in glob.iglob(str(args.glob_folder / "**" / "*.gmd"), recursive=True):
        version_props, file_data = read_gmd_structures(gmd_path)

        file_flags.add(tuple(file_data.flags))

    for flags in file_flags:
        print(list(flags))

    #     for attr in file_data.attribute_arr:
    #         # all_attrs.add((attr.unk1, attr.unk2, attr.flags, ))s
    #         shader_name = file_data.shader_arr[attr.shader_index].text
    #         # if shader_name in shader_unk1 and shader_unk1[shader_name] != attr.unk1:
    #         #     print(f"Shader {shader_name} has mismatched unk1: previous {shader_unk1[shader_name]} now {attr.unk1}")
    #         # shader_unk1[shader_name] = attr.unk1
    #
    #         texcount = sum(
    #             1
    #             for texture_index in [attr.texture_diffuse, attr.texture_multi, attr.texture_normal, attr.texture_rd, attr.texture_refl, attr.texture_rt, attr.texture_ts, attr.texture_unk1]
    #             if texture_index.tex_index != -1
    #         )
    #         # if shader_name in shader_texcount and shader_texcount[shader_name] != texcount:
    #         #     print(f"Shader {shader_name} has mismatched texcount: previous {shader_texcount[shader_name]} now {texcount}")
    #         # shader_texcount[shader_name] = texcount
    #
    #         all_attrs.add((attr.flags, shader_name))
    #
    # shader_name_pairs = [(name, unk1) for unk1, name in all_attrs]# if "s_o1dzt" in name]
    # shader_name_pairs.sort()#key=lambda data: data[1])
    # for name, flags in shader_name_pairs:
    #     # This works for most x_yNdzt shaders
    #     # extra_texture_names = ["[aref]", "[ref]", "[rs]", "[rt]", "[skin]", "[rd]", "[rdup]", "[hair]"]
    #     # guessed_texcount = 3 + sum(1 for extra_name in extra_texture_names if extra_name in name)
    #     # print(f"{unk1:4b} {texcount:2d} {guessed_texcount:2d} {name}")
    #
    #     expected_flags = 0
    #     if "s_b" in name:
    #         expected_flags |= 1
    #
    #     print(f"{flags:4x}h {expected_flags:4x}h {name}")
    #
    #     #all_attrs.sort()
    #     #for x in all_attrs:
    #     #    print(f"{x}")
    #     #print("")
    # # all_attrs = list(all_attrs)
    # # all_attrs.sort(key=lambda attr_name_pair: (attr_name_pair[3], attr_name_pair[0]))
    # #
    # # for unk1, unk2, flags, name in all_attrs:
    # #     print(f"{unk1:3d} 0x{unk2:5x} 0x{flags:04x} {name}")