import argparse
import math
from pathlib import Path

from yk_gmd_blender.structurelib.primitives import c_uint16
from yk_gmd_blender.yk_gmd.v2.converters.common.to_abstract import FileImportMode, VertexImportMode
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import LenientErrorReporter
from yk_gmd_blender.yk_gmd.v2.io import read_gmd_structures, read_abstract_scene_from_filedata_object, \
    pack_abstract_scene, pack_file_data
from mathutils import Quaternion

from yk_gmd_blender.yk_gmd.v2.structure.common.file import FileData_Common


def quaternion_to_euler_angle(q: Quaternion):
    ysqr = q.y * q.y

    t0 = +2.0 * (q.w * q.x + q.y * q.z)
    t1 = +1.0 - 2.0 * (q.x * q.x + ysqr)
    X = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (q.w * q.y - q.z * q.x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))

    t3 = +2.0 * (q.w * q.z + q.x * q.y)
    t4 = +1.0 - 2.0 * (ysqr + q.z * q.z)
    Z = math.degrees(math.atan2(t3, t4))

    return X, Y, Z

def csv_str(iter):
    return ", ".join(str(x) for x in iter)

def print_each(iter):
    for x in iter:
        print(x)


def unpack_drawlist_bytes(file_data: FileData_Common, obj):
    offset = obj.drawlist_rel_ptr
    big_endian = file_data.file_is_big_endian()
    drawlist_len, offset = c_uint16.unpack(big_endian, file_data.object_drawlist_bytes, offset)
    zero, offset = c_uint16.unpack(big_endian, file_data.object_drawlist_bytes, offset)
    data = [drawlist_len, zero]
    for i in range(drawlist_len):
        material_idx, offset = c_uint16.unpack(big_endian, file_data.object_drawlist_bytes, offset)
        mesh_idx, offset = c_uint16.unpack(big_endian, file_data.object_drawlist_bytes, offset)
        data.append(material_idx)
        data.append(mesh_idx)
    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser("GMD Poker")

    parser.add_argument("input_dir", type=Path)
    parser.add_argument("--output_dir", type=Path)
    parser.add_argument("file_to_poke", type=Path)

    args = parser.parse_args()

    error_reporter = LenientErrorReporter()

    version_props, header, file_data = read_gmd_structures(args.input_dir / args.file_to_poke, error_reporter)
    scene = read_abstract_scene_from_filedata_object(version_props, False, file_data, error_reporter)

    # for skinned_obj in scene.skinned_objects.depth_first_iterate():
    #     for mesh in skinned_obj.mesh_list:
    #         mesh.attribute_set.texture_diffuse = "dummy_white"

    # new_file_data = pack_abstract_contents_YK1(version_props, file_data.file_is_big_endian(), file_data.vertices_are_big_endian(), scene, error_reporter)
    # new_file_bytearray = bytearray()
    # FilePacker_YK1.pack(file_data.file_is_big_endian(), new_file_data, new_file_bytearray)
    unabstracted_file_data = pack_abstract_scene(version_props, file_data.file_is_big_endian(), file_data.vertices_are_big_endian(), scene, error_reporter)
    new_file_bytearray = pack_file_data(version_props, unabstracted_file_data, error_reporter)

    new_version_props, new_header, new_file_data = read_gmd_structures(bytes(new_file_bytearray), error_reporter)
    #print(version_props == new_version_props)
    #print(version_props)
    #print(new_version_props)
    new_scene = read_abstract_scene_from_filedata_object(new_version_props, FileImportMode.SKINNED, VertexImportMode.SKINNED, new_file_data, error_reporter)

    if args.output_dir:
        with open(args.output_dir / args.file_to_poke, "wb") as out_file:
            out_file.write(new_file_bytearray)

    #legacy_abstract_v2_struct_main(args)