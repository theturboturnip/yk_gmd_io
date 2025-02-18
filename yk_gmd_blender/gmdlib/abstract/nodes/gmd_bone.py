from dataclasses import dataclass
from typing import Optional, List

from mathutils import Vector, Quaternion, Matrix
from .gmd_node import GMDNode
from ...structure.common.node import NodeType


@dataclass(repr=False)
class GMDBone(GMDNode):
    matrix: Matrix  # World-to-local-space

    def __init__(self, name: str, node_type: NodeType, pos: Vector, rot: Quaternion, scale: Vector,
                 world_pos: Vector,
                 anim_axis: Vector,
                 matrix: Matrix,

                 # Empties in unskinned objects have non-bone parents
                 parent: Optional[GMDNode],
                 flags: List[int]):
        super().__init__(name, node_type, pos, rot, scale, world_pos, anim_axis, parent, flags)

        self.matrix = matrix.copy()
        self.matrix.resize_4x4()

        if self.node_type != NodeType.MatrixTransform:
            raise TypeError(f"GMDBone expected NodeType.MatrixTransform, got {self.node_type}")
