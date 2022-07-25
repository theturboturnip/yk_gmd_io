from dataclasses import dataclass
from typing import Optional, List

from mathutils import Vector, Quaternion, Matrix

from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType


@dataclass(repr=False)
class GMDBone(GMDNode):

    def __init__(self, name: str, node_type: NodeType, pos: Vector, rot: Quaternion, scale: Vector,
                 world_pos: Vector,
                 anim_axis: Vector,
                 matrix: Matrix,

                 parent: Optional['GMDBone'],
                 flags: List[int]):
        super().__init__(name, node_type, pos, rot, scale, world_pos, anim_axis, matrix, parent, flags)

        if self.node_type != NodeType.MatrixTransform:
            raise TypeError(f"GMDBone expected NodeType.MatrixTransform, got {self.node_type}")