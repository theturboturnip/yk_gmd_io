from dataclasses import dataclass
from typing import Optional, List

from mathutils import Vector, Quaternion
from .gmd_node import GMDNode
from ...structure.common.node import NodeType


@dataclass(init=False, repr=False)
class GMDBlendShape(GMDNode):
    def __init__(self, name: str, node_type: NodeType,
                 pos: Vector, rot: Quaternion, scale: Vector,
                 world_pos: Vector, anim_axis: Vector,
                 parent: Optional[GMDNode],
                 flags: List[int],
                 is_in_relative_gmd: bool):
        super().__init__(name, node_type, pos, rot, scale, world_pos, anim_axis, parent=parent,
                         flags=flags)

        self.is_in_relative_gmd = is_in_relative_gmd

        if self.node_type != NodeType.BlendShape:
            raise TypeError(f"GMDBlendShape expected NodeType.BlendShape, got {self.node_type}")
