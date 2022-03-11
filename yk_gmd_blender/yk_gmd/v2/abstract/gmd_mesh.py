import array
from dataclasses import dataclass
from typing import List

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone


@dataclass(repr=False)
class GMDMesh:
    vertices_data: GMDVertexBuffer

    triangle_indices: array.ArrayType
    triangle_strip_noreset_indices: array.ArrayType
    triangle_strip_reset_indices: array.ArrayType

    attribute_set: GMDAttributeSet

    def __post_init__(self):
        if len(self.vertices_data) < 3:
            raise TypeError(f"GMDMesh {self} has <3 vertices, at least 3 are required for a visible mesh")
        if not hasattr(self, "relevant_bones") and self.vertices_data.bone_weights:
            raise TypeError(f"GMDMesh {self} which is not skinned has vertices with bone weights")


@dataclass(repr=False)
class GMDSkinnedMesh(GMDMesh):
    relevant_bones: List[GMDBone]

    def __post_init__(self):
        super().__post_init__()
        referenced_bone_indices = {w.bone for ws in self.vertices_data.bone_weights for w in ws if w.weight > 0}
        if not referenced_bone_indices or not self.relevant_bones:
            raise TypeError(f"Mesh is skinned but references no bones. referenced_indices: {referenced_bone_indices}, relevant_bones: {self.relevant_bones}")
        if referenced_bone_indices and max(referenced_bone_indices) >= len(self.relevant_bones):
            raise Exception(f"Mesh uses {len(self.relevant_bones)} bones but references {referenced_bone_indices} in {len(self.vertices_data)} verts")
