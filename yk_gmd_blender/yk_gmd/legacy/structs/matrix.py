from ctypes import *

from yk_gmd_blender.yk_gmd.legacy.abstract.vector import Mat4, Vec4
from ._base.base_structure import BaseBigEndianStructure


class MatrixStruct(BaseBigEndianStructure):
    _fields_ = [
        ("matrix_colmaj", c_float * 16)
    ]

    def __str__(self):
        return str(",\n".join([f"{self[0]}", f"{self[1]}", f"{self[2]}", f"{self[3]}"]))

    def as_mat4(self) -> Mat4:
        return Mat4((self[0], self[1], self[2], self[3]))

    def set_from_mat4(self, matrix: Mat4):
        self.matrix_colmaj[0::4] = matrix.rows[0].as_array()
        self.matrix_colmaj[1::4] = matrix.rows[1].as_array()
        self.matrix_colmaj[2::4] = matrix.rows[2].as_array()
        self.matrix_colmaj[3::4] = matrix.rows[3].as_array()

    # Return the nth row
    def __getitem__(self, item) -> Vec4:
        if item < 0 or item > 3:
            raise IndexError()
        # Stored as column-major, so each element in the row is 4 units apart
        return Vec4(*self.matrix_colmaj[item::4])