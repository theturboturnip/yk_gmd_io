from dataclasses import dataclass
from typing import List, Optional, Iterable, Tuple

from mathutils import Vector, Quaternion, Matrix
from ..gmd_mesh import GMDMesh, GMDSkinnedMesh
from .gmd_node import GMDNode
from ...structure.common.node import NodeType


@dataclass()
class GMDBoundingBox:
    center: Vector
    sphere_radius: float
    aabb_extents: Vector

    @staticmethod
    def from_extents(center: Vector, aabb_extents: Vector) -> 'GMDBoundingBox':
        return GMDBoundingBox(
            center,
            sphere_radius=aabb_extents.length,
            aabb_extents=aabb_extents
        )

    @staticmethod
    def from_min_max(min: Vector, max: Vector) -> 'GMDBoundingBox':
        center = (max + min) / 2
        aabb_extents = (max - min) / 2
        return GMDBoundingBox(
            center,
            sphere_radius=aabb_extents.length,
            aabb_extents=aabb_extents
        )

    @staticmethod
    def from_points(ps: Iterable[Vector]) -> 'GMDBoundingBox':
        inf = float('inf')
        min_pos = Vector((inf, inf, inf))
        max_pos = Vector((-inf, -inf, -inf))

        for p in ps:
            min_pos.x = min(p.x, min_pos.x)
            min_pos.y = min(p.y, min_pos.y)
            min_pos.z = min(p.z, min_pos.z)

            max_pos.x = max(p.x, max_pos.x)
            max_pos.y = max(p.y, max_pos.y)
            max_pos.z = max(p.z, max_pos.z)

        return GMDBoundingBox.from_min_max(min_pos, max_pos)

    @staticmethod
    def combine(bounds: Iterable[Tuple['GMDBoundingBox', Vector]]) -> 'GMDBoundingBox':
        ps = []
        for bound, offset in bounds:
            ps.append(bound.center - bound.aabb_extents + offset)
            ps.append(bound.center + bound.aabb_extents + offset)
        return GMDBoundingBox.from_points(ps)


@dataclass(repr=False)
class GMDUnskinnedObject(GMDNode):
    mesh_list: List[GMDMesh]
    matrix: Matrix  # World-to-local-space
    bbox: GMDBoundingBox

    def __init__(self, name: str, node_type: NodeType,
                 pos: Vector, rot: Quaternion, scale: Vector,
                 world_pos: Vector, anim_axis: Vector,
                 parent: Optional[GMDNode],
                 matrix: Matrix,
                 flags: List[int],
                 bbox: GMDBoundingBox):
        super().__init__(name, node_type, pos, rot, scale, world_pos, anim_axis, parent, flags)
        self.mesh_list = []
        self.bbox = bbox

        self.matrix = matrix.copy()
        self.matrix.resize_4x4()

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
    bbox: GMDBoundingBox

    def __init__(self, name: str, node_type: NodeType,
                 pos: Vector, rot: Quaternion, scale: Vector,
                 world_pos: Vector, anim_axis: Vector,
                 parent: Optional[GMDNode],
                 flags: List[int],
                 bbox: GMDBoundingBox):
        super().__init__(name, node_type, pos, rot, scale, world_pos, anim_axis, parent=parent,
                         flags=flags)
        self.mesh_list = []
        self.bbox = bbox

        if self.node_type != NodeType.SkinnedMesh:
            raise TypeError(f"GMDSkinnedObject expected NodeType.SkinnedMesh, got {self.node_type}")

    def add_mesh(self, mesh: GMDSkinnedMesh):
        if not isinstance(mesh, GMDSkinnedMesh):
            raise TypeError(f"GMDSkinnedObject {self.name} got not-skinned-mesh {mesh}")
        self.mesh_list.append(mesh)
