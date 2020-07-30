from dataclasses import dataclass
from typing import List, Optional

# TODO: I don't like depending on this
# Create a set of read-only dataclasses for Vector etc?
from mathutils import Vector, Quaternion, Matrix

from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType


@dataclass(init=False)
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

        self.matrix = matrix

        self.parent = parent
        self.children = []

        if self.parent:
            self.parent.children.append(self)
