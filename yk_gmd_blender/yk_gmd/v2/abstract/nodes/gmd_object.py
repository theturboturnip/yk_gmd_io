from dataclasses import dataclass
from typing import List, Optional

from mathutils import Vector, Quaternion, Matrix

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType


@dataclass(repr=False)
class GMDUnskinnedObject(GMDNode):
    mesh_list: List[GMDMesh]

    def __init__(self, name: str, node_type: NodeType,
                 pos: Vector, rot: Quaternion, scale: Vector,
                 world_pos: Vector, anim_axis: Vector,
                 parent: Optional[GMDNode],
                 matrix: Matrix,
                 flags: List[int]):
        super().__init__(name, node_type, pos, rot, scale, world_pos, anim_axis, matrix, parent, flags)
        self.mesh_list = []

        if self.node_type != NodeType.UnskinnedMesh:
            raise TypeError(f"GMDUnskinnedObject {name} expected NodeType.UnskinnedMesh, got {self.node_type}")

    def add_mesh(self, mesh: GMDMesh):
        if isinstance(mesh, GMDSkinnedMesh):
            raise TypeError(f"GMDUnskinnedObject {self.name} got skinned mesh {mesh}")
        self.mesh_list.append(mesh)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return self.__str__()


@dataclass(repr=False)
class GMDSkinnedObject(GMDNode):
    mesh_list: List[GMDSkinnedMesh]

    def __init__(self, name: str, node_type: NodeType,
                 pos: Vector, rot: Quaternion, scale: Vector,
                 world_pos: Vector, anim_axis: Vector,
                 parent: Optional[GMDNode],
                 flags: List[int]):
        super().__init__(name, node_type, pos, rot, scale, world_pos, anim_axis, matrix=None, parent=parent, flags=flags)
        self.mesh_list = []

        if self.node_type != NodeType.SkinnedMesh:
            raise TypeError(f"GMDSkinnedObject expected NodeType.SkinnedMesh, got {self.node_type}")

    def add_mesh(self, mesh: GMDSkinnedMesh):
        if not isinstance(mesh, GMDSkinnedMesh):
            raise TypeError(f"GMDSkinnedObject {self.name} got not-skinned-mesh {mesh}")
        self.mesh_list.append(mesh)
