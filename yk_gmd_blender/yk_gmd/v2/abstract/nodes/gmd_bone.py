from dataclasses import dataclass
from typing import Optional

from mathutils import Vector, Quaternion, Matrix

from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType


@dataclass(repr=False)
class GMDBone(GMDNode):
    bone_pos: Vector
    bone_axis: Vector

    def __init__(self, name: str, node_type: NodeType, pos: Vector, rot: Quaternion, scale: Vector,
                 bone_pos: Vector,
                 bone_axis: Vector,
                 matrix: Matrix,

                 parent: Optional['GMDBone']):
        super().__init__(name, node_type, pos, rot, scale, matrix, parent)

        self.bone_pos = bone_pos
        self.bone_axis = bone_axis

        if self.node_type != NodeType.MatrixTransform:
            raise TypeError(f"GMDBone expected NodeType.MatrixTransform, got {self.node_type}")