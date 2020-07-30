from dataclasses import dataclass
from typing import List

from mathutils import Vector, Quaternion, Matrix

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType


@dataclass(repr=False)
class GMDUnskinnedObject(GMDNode):
    mesh_list: List[GMDMesh]

    def __init__(self, name: str, node_type: NodeType, pos: Vector, rot: Quaternion, scale: Vector,
                 parent: GMDNode,
                 matrix: Matrix,
                 mesh_list: List[GMDMesh]):
        super().__init__(name, node_type, pos, rot, scale, matrix, parent)
        self.mesh_list = mesh_list
        for mesh in mesh_list:
            if isinstance(mesh, GMDSkinnedMesh):
                raise TypeError(f"GMDUnskinnedObject {name} got skinned mesh {mesh}")

        if self.node_type != NodeType.UnskinnedMesh:
            raise TypeError(f"GMDUnskinnedObject {name} expected NodeType.UnskinnedMesh, got {self.node_type}")

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return self.__str__()


@dataclass(repr=False)
class GMDSkinnedObject(GMDNode):
    mesh_list: List[GMDSkinnedMesh]

    def __init__(self, name: str, node_type: NodeType, pos: Vector, rot: Quaternion, scale: Vector,
                 parent: GMDNode,
                 mesh_list: List[GMDSkinnedMesh]):
        super().__init__(name, node_type, pos, rot, scale, matrix=None, parent=parent)
        self.mesh_list = mesh_list
        for mesh in mesh_list:
            if not isinstance(mesh, GMDSkinnedMesh):
                raise TypeError(f"GMDSkinnedObject {name} got not-skinned-mesh {mesh}")

        if self.node_type != NodeType.SkinnedMesh:
            raise TypeError(f"GMDSkinnedObject expected NodeType.SkinnedMesh, got {self.node_type}")
