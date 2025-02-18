from dataclasses import dataclass
from typing import List, Optional

# TODO: I don't like depending on this
# Create a set of read-only dataclasses for Vector etc?
from mathutils import Vector, Quaternion
from ...structure.common.node import NodeType


@dataclass(init=False, repr=False)
class GMDNode:
    name: str
    node_type: NodeType

    pos: Vector
    rot: Quaternion
    scale: Vector

    world_pos: Vector
    # Should be 0,0,0,0 or a valid quaternion
    anim_axis: Vector

    flags: List[int]

    parent: Optional['GMDNode']
    children: List['GMDNode']

    def __init__(self, name: str, node_type: NodeType,
                 pos: Vector, rot: Quaternion, scale: Vector,
                 world_pos: Vector, anim_axis: Vector,
                 parent: Optional['GMDNode'],
                 flags: List[int]):
        self.name = name
        self.node_type = node_type

        self.pos = pos
        self.rot = rot
        self.scale = scale

        self.world_pos = world_pos
        self.anim_axis = anim_axis

        self.flags = flags
        if len(self.flags) != 4:
            raise TypeError(f"GMDNode passed flags list {flags} which doesn't have 4 elements")

        self.parent = parent
        self.children = []

        if self.parent:
            self.parent.children.append(self)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name}, pos={self.pos}, rot={self.rot}, " \
               f"scale={self.scale}, parent={self.parent.name if self.parent else None}, " \
               f"children={[c.name for c in self.children]})"
