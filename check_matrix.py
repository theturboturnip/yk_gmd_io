import argparse
import math
from pathlib import Path

from yk_gmd_blender.structurelib.primitives import c_uint16
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.converters.common.to_abstract import FileImportMode, VertexImportMode
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import LenientErrorReporter
from yk_gmd_blender.yk_gmd.v2.io import read_gmd_structures, read_abstract_scene_from_filedata_object, \
    pack_abstract_scene, pack_file_data
from mathutils import Quaternion, Matrix, Vector

from yk_gmd_blender.yk_gmd.v2.structure.common.file import FileData_Common
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType


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

    parser.add_argument("--skinned", action="store_true")
    parser.add_argument("file_to_poke", type=Path)

    args = parser.parse_args()

    error_reporter = LenientErrorReporter()

    print("loading " + str(args.file_to_poke))
    version_props, header, file_data = read_gmd_structures(args.file_to_poke, error_reporter)
    scene = read_abstract_scene_from_filedata_object(version_props,
                                                     FileImportMode.SKINNED if args.skinned else FileImportMode.UNSKINNED,
                                                     VertexImportMode.NO_VERTICES,
                                                     file_data, error_reporter)
    print(scene)

    if args.skinned:
        for node in scene.overall_hierarchy.depth_first_iterate():
            if node.node_type != NodeType.MatrixTransform:
                continue
            node: GMDBone = node
            print(f" ---- BONE {node.name} ---- PARENT {node.parent.name if node.parent is not None else None}")
            print("pos", node.pos)
            print("rot", node.rot)
            print("scale", node.scale)
            print("world pos", node.bone_pos)
            print("bone axis", node.bone_axis)
            parent_mat = node.parent.matrix if node.parent is not None else Matrix.Identity(4)

            # pos = node.bone_pos.to_3d()
            pos = node.pos.to_3d()

            # inv(parent matrix) * local position = bone_postion (world position)
            expected_world = parent_mat.inverted_safe() @ node.pos.to_3d()
            gmd_world = node.bone_pos.to_3d()
            print("world pos comparison", expected_world, gmd_world)
            if (expected_world - gmd_world).magnitude > 0.1:
                print("mismatching world pos")
                break


            inv_t = Matrix.Translation(-pos)
            t = Matrix.Translation(pos)
            inv_r = node.rot.inverted().to_matrix().to_4x4()
            r = node.rot.to_matrix().to_4x4()
            inv_s = Matrix.Diagonal(Vector((1/node.scale.x, 1/node.scale.y, 1/node.scale.z))).to_4x4()
            overall_mat = (parent_mat @ inv_s @ inv_r @ inv_t)
            # print(inv_t)
            # print(inv_r)
            print("mat real", node.matrix)
            print("mat calc",overall_mat)
            if sum([x*x for v in (overall_mat - node.matrix) for x in v]) > 0.1:
                print("DIFFERENCE")
                break
    else:
        for node in scene.overall_hierarchy.depth_first_iterate():
            print(f" ---- OBJECT {node.name} ---- PARENT {node.parent.name if node.parent is not None else None}")
            print(node.pos)
            print(node.rot)
            print(node.scale)
            print(node.matrix)
            inv_t = Matrix.Translation(-node.pos)
            inv_r = node.rot.inverted().to_matrix().to_4x4()
            inv_s = Matrix.Diagonal(Vector((1/node.scale.x, 1/node.scale.y, 1/node.scale.z))).to_4x4()
            parent_mat = node.parent.matrix if node.parent is not None else Matrix.Identity(4)
            print(inv_s @ inv_r @ inv_t @ parent_mat)


    # unabstracted_file_data = pack_abstract_scene(version_props, file_data.file_is_big_endian(), file_data.vertices_are_big_endian(), scene, error_reporter)
    # new_file_bytearray = pack_file_data(version_props, unabstracted_file_data, error_reporter)

    # new_version_props, new_header, new_file_data = read_gmd_structures(bytes(new_file_bytearray), error_reporter)
    # new_scene = read_abstract_scene_from_filedata_object(new_version_props, args, new_file_data, error_reporter)
