import collections
import functools
import math
from dataclasses import dataclass
from typing import Tuple, Union, List


@dataclass
class Vec3:
    x: float
    y: float
    z: float

    def as_array(self) -> List[float]:
        return [self.x, self.y, self.z]

    def __getitem__(self, item) -> float:
        return [self.x, self.y, self.z][item]

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return self + (-other)

    def magnitude(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def min(self, other):
        return Vec3(min(self.x, other.x), min(self.y, other.y), min(self.z, other.z))
    def max(self, other):
        return Vec3(max(self.x, other.x), max(self.y, other.y), max(self.z, other.z))

    @staticmethod
    def bounds_of(xs: List['Vec3']) -> Tuple['Vec3', 'Vec3']:
        return (
            functools.reduce(Vec3.min, xs[1:], xs[0]),
            functools.reduce(Vec3.max, xs[1:], xs[0]),
        )


@dataclass
class Vec4(Vec3):
    w: float

    @property
    def xyz(self):
        return Vec3(self.x, self.y, self.z)

    def as_array(self) -> List[float]:
        return [self.x, self.y, self.z, self.w]

    def __getitem__(self, item) -> float:
        return [self.x, self.y, self.z, self.w][item]

    def min(self, other):
        return Vec4(min(self.x, other.x), min(self.y, other.y), min(self.z, other.z), min(self.w, other.w))

    def max(self, other):
        return Vec4(max(self.x, other.x), max(self.y, other.y), max(self.z, other.z), min(self.w, other.w))


@dataclass
class Quat(Vec4):
    pass


@dataclass
class Mat4:
    rows: Tuple[Vec4, Vec4, Vec4, Vec4]

    def __getitem__(self, item) -> Vec4:
        return self.rows[item]

    def as_tuple(self):
        return (
            (self.rows[0].x, self.rows[0].y, self.rows[0].z, self.rows[0].w),
            (self.rows[1].x, self.rows[1].y, self.rows[1].z, self.rows[1].w),
            (self.rows[2].x, self.rows[2].y, self.rows[2].z, self.rows[2].w),
            (self.rows[3].x, self.rows[3].y, self.rows[3].z, self.rows[3].w),
        )

    @staticmethod
    def from_tuple(row0, row1, row2, row3):
        return Mat4((
            Vec4(row0[0], row0[1], row0[2], row0[3]),
            Vec4(row1[0], row1[1], row1[2], row1[3]),
            Vec4(row2[0], row2[1], row2[2], row2[3]),
            Vec4(row3[0], row3[1], row3[2], row3[3]),
        ))

    def __mul__(self, other: Union[Vec3, Vec4, 'Mat4']):
        if isinstance(other, Mat4):
            res_single = lambda i,j: sum(self.rows[i][x] * other.rows[x][j] for x in range(4))
            res_row = lambda i: Vec4(*[res_single(i,j) for j in range(4)])
            return Mat4((res_row(0), res_row(1), res_row(2), res_row(3)))

        if isinstance(other, Vec3):
            other = Vec4(*other, 1)

        # other should now be a Vec4
        if isinstance(other, Vec4):
            res_single = lambda i: sum(self.rows[i][x] * other[x] for x in range(4))
            return Vec4(*[res_single(i) for i in range(4)])

        raise TypeError(f"Tried to multiply Mat4 by a {type(other).__name__}")

    @staticmethod
    def translation(trans: Union[Vec3, Vec4]) -> 'Mat4':
        return Mat4((
            Vec4(1, 0, 0, trans.x),
            Vec4(0, 1, 0, trans.y),
            Vec4(0, 0, 1, trans.z),
            Vec4(0, 0, 0,       1),
        ))

    @staticmethod
    def scale(scale: Union[Vec3, Vec4]) -> 'Mat4':
        return Mat4((
            Vec4(scale.x, 0, 0, 0),
            Vec4(0, scale.y, 0, 0),
            Vec4(0, 0, scale.z, 0),
            Vec4(0, 0, 0, 1),
        ))

    # https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/index.htm
    @staticmethod
    def rotation(q: Quat) -> 'Mat4':
        return Mat4((
            Vec4(1 - 2*q.y*q.y - 2*q.z*q.z, 2*q.x*q.y - 2*q.z*q.w, 2*q.x*q.z + 2*q.y*q.w, 0),
            Vec4(2*q.x*q.y+2*q.z*q.w, 1 - 2*q.x*q.x - 2*q.z*q.z, 2*q.y*q.z - 2*q.x*q.w, 0),
            Vec4(2*q.x*q.z - 2*q.y*q.w, 2*q.y*q.z + 2*q.x*q.w, 1 - 2*q.x*q.x - 2*q.y*q.y, 0),
            Vec4(0, 0, 0, 1),
        ))

    @staticmethod
    def transformation(trans: Vec3, rot: Quat, scl: Vec3) -> 'Mat4':
        return Mat4.scale(scl) * Mat4.rotation(rot) * Mat4.translation(trans)
