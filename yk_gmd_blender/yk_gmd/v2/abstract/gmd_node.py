from dataclasses import dataclass
from typing import List, Optional

# TODO: I don't like depending on this
# Create a set of read-only dataclasses for Vector etc?
from mathutils import Vector, Quaternion, Matrix

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType


@dataclass(init=False)
class GMDNode:
    name: str
    node_type: NodeType

    pos: Vector
    rot: Quaternion
    scale: Vector

    parent: Optional['GMDNode']
    children: List['GMDNode']

    def __init__(self, name: str, node_type: NodeType, pos: Vector, rot: Quaternion, scale: Vector, parent: Optional['GMDNode']):
        self.name = name
        self.node_type = node_type

        self.pos = pos
        self.rot = rot
        self.scale = scale

        self.parent = parent
        self.children = []


class GMDBone(GMDNode):
    bone_pos: Vector
    bone_axis: Quaternion

    matrix: Matrix

    def __init__(self, name: str, node_type: NodeType, pos: Vector, rot: Quaternion, scale: Vector,
                 bone_pos: Vector,
                 bone_axis: Quaternion,
                 matrix: Matrix,

                 parent: Optional['GMDBone']):
        super().__init__(name, node_type, pos, rot, scale, parent)

        self.bone_pos = bone_pos
        self.bone_axis = bone_axis
        self.matrix = matrix


class GMDObject(GMDNode):
    mesh_list: List[GMDMesh]

    def __init__(self, name: str, node_type: NodeType, pos: Vector, rot: Quaternion, scale: Vector,
                 parent: GMDNode,
                 mesh_list: List[GMDMesh]):
        super().__init__(name, node_type, pos, rot, scale, parent)
        self.mesh_list = mesh_list