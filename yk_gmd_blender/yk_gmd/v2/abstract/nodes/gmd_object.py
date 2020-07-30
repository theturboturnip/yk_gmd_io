from dataclasses import dataclass
from typing import List

from mathutils import Vector, Quaternion, Matrix

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType


@dataclass
class GMDUnskinnedObject(GMDNode):
    mesh_list: List[GMDMesh]

    def __init__(self, name: str, node_type: NodeType, pos: Vector, rot: Quaternion, scale: Vector,
                 parent: GMDNode,
                 matrix: Matrix,
                 mesh_list: List[GMDMesh]):
        super().__init__(name, node_type, pos, rot, scale, matrix, parent)
        self.mesh_list = mesh_list

        if self.node_type != NodeType.UnskinnedMesh:
            raise TypeError(f"GMDUnskinnedObject expected NodeType.UnskinnedMesh, got {self.node_type}")


@dataclass
class GMDSkinnedObject(GMDNode):
    mesh_list: List[GMDMesh]

    def __init__(self, name: str, node_type: NodeType, pos: Vector, rot: Quaternion, scale: Vector,
                 parent: GMDNode,
                 mesh_list: List[GMDMesh]):
        super().__init__(name, node_type, pos, rot, scale, matrix=None, parent=parent)
        self.mesh_list = mesh_list

        if self.node_type != NodeType.SkinnedMesh:
            raise TypeError(f"GMDSkinnedObject expected NodeType.SkinnedMesh, got {self.node_type}")
