import array
from dataclasses import dataclass
from typing import List, Tuple

from mathutils import Vector

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone


@dataclass(repr=False)
class GMDMesh:
    vertices_data: GMDVertexBuffer

    # TODO: Is List[int] any more convenient than array? If not, array is more compact and nicer
    triangle_indices: array.ArrayType
    triangle_strip_noreset_indices: array.ArrayType
    triangle_strip_reset_indices: array.ArrayType

    attribute_set: GMDAttributeSet

    def __post_init__(self):
        if not hasattr(self, "relevant_bones") and self.vertices_data.bone_weights:
            raise TypeError(f"GMDMesh {self} which is not skinned has vertices with bone weights")


@dataclass(repr=False)
class GMDSkinnedMesh(GMDMesh):
    relevant_bones: List[GMDBone]

    def __post_init__(self):
        super().__post_init__()
        referenced_bone_indices = {w.bone for ws in self.vertices_data.bone_weights for w in ws}
        if max(referenced_bone_indices) >= len(self.relevant_bones):
            raise Exception(f"Mesh uses {len(self.relevant_bones)} bones but references {referenced_bone_indices} in {len(self.vertices_data)} verts")
