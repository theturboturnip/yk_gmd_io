import argparse
import math
from pathlib import Path

from mathutils import Quaternion, Matrix, Vector
from .yk_gmd_blender.structurelib.primitives import c_uint16
from .yk_gmd_blender.gmdlib.abstract.nodes.gmd_bone import GMDBone
from .yk_gmd_blender.gmdlib.converters.common.to_abstract import FileImportMode, VertexImportMode
from .yk_gmd_blender.gmdlib.errors.error_reporter import LenientErrorReporter
from .yk_gmd_blender.gmdlib.io import read_gmd_structures, read_abstract_scene_from_filedata_object
from .yk_gmd_blender.gmdlib.structure.common.file import FileData_Common
from .yk_gmd_blender.gmdlib.structure.common.node import NodeType


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


def round_vec(v, n=2):
    return tuple(round(x, n) for x in v)


def round_mat(m, n=2):
    s = f"Matrix\n"
    for r in m.row:
        s += f"\t{round_vec(r, n)}\n"
    return s


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

    # if args.skinned:
    for node in scene.overall_hierarchy:
        node: GMDBone = node
        print(f" ---- BONE {node.name} ---- PARENT {node.parent.name if node.parent is not None else None}")
        print("pos", round_vec(node.pos))
        print("rot", f"Quat({round_vec(node.rot)})")
        print("rot angle/axis", node.rot.angle, round_vec(node.rot.axis))
        print("scale", round_vec(node.scale))
        if node.node_type == NodeType.MatrixTransform:
            print("world pos", round_vec(node.world_pos))
            print("anim axis", round_vec(node.anim_axis))
            print(f"anim axis deconstructed? {round_vec(node.anim_axis.xyz.normalized())} / {node.anim_axis.w}")
        parent_mat = node.parent.matrix if node.parent is not None else Matrix.Identity(4)

        # pos = node.world_pos.to_3d()
        pos = node.pos.to_3d()

        # inv(parent matrix) * local position = bone_postion (world position)
        if node.node_type == NodeType.MatrixTransform:
            expected_world = parent_mat.inverted_safe() @ node.pos.to_3d()
            gmd_world = node.world_pos.to_3d()
            print("world pos comparison", round_vec(expected_world), round_vec(gmd_world))
            if (expected_world - gmd_world).magnitude > 0.1:
                print("mismatching world pos")
                break

        has_matrix = node.node_type != NodeType.SkinnedMesh
        if has_matrix:
            inv_t = Matrix.Translation(-pos)
            inv_r = node.rot.inverted().to_matrix().to_4x4()
            r = node.rot.to_matrix().to_4x4()
            inv_s = Matrix.Diagonal(Vector((1 / node.scale.x, 1 / node.scale.y, 1 / node.scale.z))).to_4x4()
            overall_mat = inv_s @ inv_r @ inv_t @ parent_mat

            print("mat real", round_mat(node.matrix))
            print("mat calc", round_mat(overall_mat))
            if sum([x * x for v in (overall_mat - node.matrix) for x in v]) > 0.1:
                print("DIFFERENCE")
                break

        if args.skinned and node.node_type == NodeType.MatrixTransform:
            # Attempt to calculate rot from bone_axis??

            pass
