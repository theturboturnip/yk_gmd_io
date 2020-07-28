import array
from dataclasses import dataclass
from typing import List, Tuple

from mathutils import Vector

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDMaterial
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_node import GMDBone


@dataclass
class GMDMesh:
    relevant_bones: List[GMDBone]

    vertices_data: List[GMDVertex]

    # TODO: Is List[int] any more convenient than array? If not, array is more compact and nicer
    triangle_indices: array.ArrayType
    triangle_strip_noreset_indices: array.ArrayType
    triangle_strip_reset_indices: array.ArrayType

    material: GMDMaterial

