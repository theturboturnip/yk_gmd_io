from dataclasses import dataclass
from typing import List, Optional

# TODO: I don't like depending on this
# Create a set of read-only dataclasses for Vector etc?
from mathutils import Vector, Quaternion, Matrix

from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType


@dataclass(init=False,repr=False)
class GMDNode:
    name: str
    node_type: NodeType

    pos: Vector
    rot: Quaternion
    scale: Vector

    matrix: Optional[Matrix]

    parent: Optional['GMDNode']
    children: List['GMDNode']

    def __init__(self, name: str, node_type: NodeType, pos: Vector, rot: Quaternion, scale: Vector, matrix: Optional[Matrix], parent: Optional['GMDNode']):
        self.name = name
        self.node_type = node_type

        self.pos = pos
        self.rot = rot
        self.scale = scale

        if matrix:
            self.matrix = matrix.copy()
            self.matrix.resize_4x4()
        else:
            self.matrix = None

        self.parent = parent
        self.children = []

        if self.parent:
            self.parent.children.append(self)

    def __repr__(self):
        return str(self)
    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name}, pos={self.pos}, rot={self.rot}, scale={self.scale}, parent={self.parent.name if self.parent else None}, children={[c.name for c in self.children]})"