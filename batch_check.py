import argparse
import glob
import json
from pathlib import Path
from typing import List, Dict, Tuple, Union, Callable

from .yk_gmd_blender.structurelib.primitives import c_uint16
from .yk_gmd_blender.gmdlib.abstract.gmd_scene import GMDScene
from .yk_gmd_blender.gmdlib.abstract.nodes.gmd_object import GMDUnskinnedObject, GMDSkinnedObject
from .yk_gmd_blender.gmdlib.converters.common.to_abstract import VertexImportMode, FileImportMode
from .yk_gmd_blender.gmdlib.errors.error_classes import GMDImportExportError
from .yk_gmd_blender.gmdlib.errors.error_reporter import LenientErrorReporter
from .yk_gmd_blender.gmdlib.io import read_gmd_structures, read_abstract_scene_from_filedata_object
from .yk_gmd_blender.gmdlib.structure.common.node import NodeType
from .yk_gmd_blender.gmdlib.structure.kenzan.file import FileData_Kenzan
from .yk_gmd_blender.gmdlib.structure.yk1.file import FileData_YK1
from .yk_gmd_blender.gmdlib.structure.yk1.mesh import MeshStruct_YK1


def batch_process_files(args, f: Callable[[str, Union[FileData_Kenzan, FileData_YK1], GMDScene], None]):
    error_reporter = LenientErrorReporter(allowed_categories=set())
    for gmd_path in glob.iglob(str(args.glob_folder / "**" / "*.gmd"), recursive=True):
        skin_mode = FileImportMode.SKINNED if "-Skinned" in gmd_path else FileImportMode.UNSKINNED
        print(f"Parsing {gmd_path} as {skin_mode}")
        try:
            version_props, header, file_data = read_gmd_structures(gmd_path, error_reporter)
            scene = read_abstract_scene_from_filedata_object(version_props, skin_mode,
                                                             VertexImportMode.NO_VERTICES, file_data, error_reporter)
        except GMDImportExportError as ex:
            print(ex)
            continue
        f(gmd_path, file_data, scene)


def print_flags(args):
    file_flags = set()

    def process_file_flags(_, file_data, __):
        file_flags.add(tuple(file_data.flags))

    batch_process_files(args, process_file_flags)

    for flags in file_flags:
        print(list(flags))


def print_attrs(args):
    all_attrs = set()
    shader_unk1 = {}
    shader_texcount = {}

    def process_file_attrs(_, file_data, __):
        for attr in file_data.attribute_arr:
            # all_attrs.add((attr.unk1, attr.unk2, attr.flags, ))s
            shader_name = file_data.shader_arr[attr.shader_index].text
            # if shader_name in shader_unk1 and shader_unk1[shader_name] != attr.unk1:
            #     print(f"Shader {shader_name} has mismatched unk1: previous {shader_unk1[shader_name]} now {attr.unk1}")
            # shader_unk1[shader_name] = attr.unk1

            texcount = sum(
                1
                for texture_index in
                [attr.texture_diffuse, attr.texture_multi, attr.texture_normal, attr.texture_rd, attr.texture_refl,
                 attr.texture_rt, attr.texture_ts, attr.texture_unk1]
                if texture_index.tex_index != -1
            )
            # if shader_name in shader_texcount and shader_texcount[shader_name] != texcount:
            #     print(f"Shader {shader_name} has mismatched texcount: previous {shader_texcount[shader_name]} now {texcount}")
            # shader_texcount[shader_name] = texcount

            all_attrs.add((attr.flags, shader_name))

    batch_process_files(args, process_file_attrs)

    shader_name_pairs = [(name, unk1) for unk1, name in all_attrs]  # if "s_o1dzt" in name]
    shader_name_pairs.sort()  # key=lambda data: data[1])
    for name, flags in shader_name_pairs:
        # This works for most x_yNdzt shaders
        # extra_texture_names = ["[aref]", "[ref]", "[rs]", "[rt]", "[skin]", "[rd]", "[rdup]", "[hair]"]
        # guessed_texcount = 3 + sum(1 for extra_name in extra_texture_names if extra_name in name)
        # print(f"{unk1:4b} {texcount:2d} {guessed_texcount:2d} {name}")

        expected_flags = 0
        if "s_b" in name:
            expected_flags |= 1

        print(f"{flags:4x}h {expected_flags:4x}h {name}")

        # all_attrs.sort()
        # for x in all_attrs:
        #    print(f"{x}")
        # print("")
    # all_attrs = list(all_attrs)
    # all_attrs.sort(key=lambda attr_name_pair: (attr_name_pair[3], attr_name_pair[0]))
    #
    # for unk1, unk2, flags, name in all_attrs:
    #     print(f"{unk1:3d} 0x{unk2:5x} 0x{flags:04x} {name}")


def print_meshes(args):
    mesh_files: Dict[str, List[Tuple[str, MeshStruct_YK1]]] = {}

    def process_meshes(_, file_data: FileData_YK1, __):
        if any([m.flags_maybe for m in file_data.mesh_arr]):
            mesh_to_object_name = {}

            for object_idx, object in enumerate(file_data.obj_arr):
                drawlist_ptr = object.drawlist_rel_ptr
                offset = drawlist_ptr
                big_endian = file_data.file_is_big_endian()
                mesh_drawlists = file_data.object_drawlist_bytes
                drawlist_len, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
                zero, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
                for i in range(drawlist_len):
                    material_idx, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
                    mesh_idx, offset = c_uint16.unpack(big_endian, mesh_drawlists, offset)
                    mesh_to_object_name[mesh_idx] = file_data.node_name_arr[
                        file_data.node_arr[object.node_index_1].name_index].text

            mesh_files[file_data.name.text] = [(mesh_to_object_name[mesh_idx], mesh) for mesh_idx, mesh in
                                               enumerate(file_data.mesh_arr)]

    batch_process_files(args, process_meshes)

    # for name in sorted(mesh_files.keys()):
    #     print(f"{name}")
    #     for mesh_name, mesh in mesh_files[name]:
    #         print(f"\t{mesh.vertex_buffer_index:5d}\t{mesh.vertex_offset:6d}\t{mesh.vertex_count:6d}\t\t{mesh.flags_maybe:04x}\t{mesh_name}")

    print(f"Mesh files with flags: {len(mesh_files)}")
    for name in sorted(mesh_files.keys()):
        print(f"{name}")
        flag_vals = set()
        for _, mesh in mesh_files[name]:
            flag_vals.add(mesh.flags_maybe)
        print(f"\t{[hex(x) for x in flag_vals]}")


def check_vertex_layouts(args):
    # mesh_files: Dict[str, List[Tuple[str, MeshStruct_YK1]]] = {}
    relevant_files = []

    # vertex_buffer_layouts = set()

    def process_meshes(_, file_data: FileData_YK1, scene: GMDScene):
        for node in scene.overall_hierarchy:
            if node.node_type == NodeType.UnskinnedMesh and isinstance(node, GMDUnskinnedObject):
                for mesh in node.mesh_list:
                    vbl = mesh.attribute_set.shader.vertex_buffer_layout
                    if bool(vbl.bones_storage) or bool(vbl.weights_storage):
                        relevant_files.append(file_data.name)
                        print(file_data.name)

    batch_process_files(args, process_meshes)

    # for vbl in vertex_buffer_layouts:
    #     if
    print(relevant_files)


def check_bonecounts(args):
    file_max_bonecounts = {}

    def process_meshes(path: str, file_data: FileData_YK1, scene: GMDScene):
        max_bonecount = 0
        for node in scene.overall_hierarchy:
            if node.node_type == NodeType.SkinnedMesh and isinstance(node, GMDSkinnedObject):
                for mesh in node.mesh_list:
                    if len(mesh.relevant_bones) > max_bonecount:
                        max_bonecount = len(mesh.relevant_bones)
        file_max_bonecounts[path] = max_bonecount

    batch_process_files(args, process_meshes)
    print(json.dumps(file_max_bonecounts, indent=4))


# "D:\Games\SteamLibrary\steamapps\common\Yakuza Kiwami\media\data\stage"
# "D:\Games\SteamLibrary\steamapps\common\Yakuza Kiwami 2\data\stage_lexus2\st_o_grand.par.unpack\stage\file_common\common\"
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("glob_folder", type=Path)
    parser.add_argument("--skinned", action="store_true")

    args = parser.parse_args()

    # check_vertex_layouts(args)
    check_bonecounts(args)
