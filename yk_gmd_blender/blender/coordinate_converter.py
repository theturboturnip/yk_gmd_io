from typing import Tuple

from mathutils import Vector, Quaternion, Matrix


def transform_position_gmd_to_blender(pos: Vector) -> Vector:
    return Vector((-pos.x, pos.z, pos.y))


def transform_rotation_gmd_to_blender(rot: Quaternion) -> Quaternion:
    return Quaternion((rot.w, -rot.x, rot.z, rot.y))


def transform_gmd_to_blender(pos: Vector, rot: Quaternion, scale: Vector) -> Tuple[Vector, Quaternion, Vector]:
    pos = Vector((-pos.x, pos.z, pos.y))
    rot = Quaternion((rot.w, -rot.x, rot.z, rot.y))
    scale = scale.xzy

    return pos, rot, scale


def transform_blender_to_gmd(pos: Vector, rot: Quaternion, scale: Vector) -> Tuple[Vector, Quaternion, Vector]:
    # The transformation is symmetrical
    return transform_gmd_to_blender(pos, rot, scale)


def transform_matrix_gmd_to_blender(matrix: Matrix) -> Matrix:
    pos, rot, scale = matrix.decompose()
    pos, rot, scale = transform_gmd_to_blender(pos, rot, scale)
    return transform_to_matrix(pos, rot, scale)


def transform_matrix_blender_to_gmd(matrix: Matrix) -> Matrix:
    pos, rot, scale = matrix.decompose()
    pos, rot, scale = transform_blender_to_gmd(pos, rot, scale)
    return transform_to_matrix(pos, rot, scale)


def transform_to_matrix(pos: Vector, rot: Quaternion, scale: Vector) -> Matrix:
    scale_matrix = Matrix.Diagonal(scale)
    scale_matrix.resize_4x4()
    rot_matrix = rot.to_matrix()
    rot_matrix.resize_4x4()
    pos_matrix = Matrix.Translation(pos.xyz)
    pos_matrix.resize_4x4()
    return pos_matrix @ rot_matrix @ scale_matrix


def invert_transformation_matrix(mat: Matrix) -> Matrix:
    # https://math.stackexchange.com/a/152686
    p = mat.to_3x3()
    p_inv = p.inverted()
    v = mat.col[3][0:2]

    # This should be 3x3 @ 3x1
    neg_p_inv_v = -(p_inv @ Vector(v))

    m_inv = p_inv.to_4x4()
    m_inv.col[3] = list(neg_p_inv_v[0:2]) + [1]

    return m_inv
