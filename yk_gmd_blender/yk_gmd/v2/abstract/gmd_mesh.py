import array
from dataclasses import dataclass
from typing import List

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer_Generic, GMDVertexBuffer_Skinned
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone


@dataclass(repr=False)
class GMDMesh:
    empty: bool

    vertices_data: GMDVertexBuffer_Generic

    triangle_indices: array.ArrayType
    triangle_strip_noreset_indices: array.ArrayType
    triangle_strip_reset_indices: array.ArrayType

    attribute_set: GMDAttributeSet

    def __post_init__(self):
        if not self.empty and len(self.vertices_data) < 3:
            raise TypeError(f"GMDMesh {self} has <3 vertices, at least 3 are required for a visible mesh")


@dataclass(repr=False)
class GMDSkinnedMesh(GMDMesh):
    vertices_data: GMDVertexBuffer_Skinned
    relevant_bones: List[GMDBone]

    def __post_init__(self):
        super().__post_init__()
        referenced_bone_indices = {w.bone for ws in self.vertices_data.bone_weights for w in ws if w.weight > 0}
        if not self.empty and (not referenced_bone_indices or not self.relevant_bones):
            raise TypeError(
                f"Mesh is skinned but references no bones. "
                f"referenced_indices: {referenced_bone_indices}, relevant_bones: {self.relevant_bones}")
        if referenced_bone_indices and max(referenced_bone_indices) >= len(self.relevant_bones):
            raise Exception(
                f"Mesh uses {len(self.relevant_bones)} bones "
                f"but references {referenced_bone_indices} in {len(self.vertices_data)} verts")
