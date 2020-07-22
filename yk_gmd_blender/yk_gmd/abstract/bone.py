from typing import List, Optional

from .vector import Vec3, Quat, Mat4


class GMDBone:
    id: int
    name: str

    parent: Optional['GMDBone']
    children: List['GMDBone']

    pos: Vec3
    rot: Quat
    scl: Vec3

    tail: Vec3

    matrix_world_to_local: Optional[Mat4]

    def __init__(self, id: int, name: str, pos: Vec3, rot: Quat, scl: Vec3):
        self.id = id
        self.name = name

        self.pos = pos
        self.rot = rot
        self.scl = scl

        self.matrix_world_to_local = None

    def set_matrix(self, matrix_world_to_local: Mat4):
        self.matrix_world_to_local = matrix_world_to_local

    def set_hierarchy_props(self, parent: Optional['GMDBone'], children: List['GMDBone']):
        self.parent = parent
        self.children = children

    #def __str__(self):
    #    return f"<Bone {self.id} '{self.name}': {self.ints}>"