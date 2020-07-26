from dataclasses import dataclass
from typing import List, Dict

from yk_gmd_blender.yk_gmd.v2.structure.yk1.vertex_buffer_layout import VertexBufferLayout_YK1
from yk_gmd_blender.yk_gmd.abstract.bone import GMDBone
from yk_gmd_blender.yk_gmd.abstract.material import GMDMaterial
from yk_gmd_blender.yk_gmd.abstract.submesh import GMDSubmesh
from yk_gmd_blender.yk_gmd.abstract.vertices import GMDVertexBuffer, GMDVertexBufferLayout


@dataclass(repr=False)
class GMDScene:
    name: str

    bone_roots: List[GMDBone]
    bone_index_map: Dict[int, GMDBone]
    bone_name_map: Dict[str, GMDBone]

    vertex_buffers: List[GMDVertexBuffer]
    submeshes: List[GMDSubmesh]
    #parts: List[GMDPart]
    materials: List[GMDMaterial]

    abstract_vb_layout_to_struct: Dict[GMDVertexBufferLayout, VertexBufferLayout_YK1]

    def bones_in_order(self) -> List[GMDBone]:
        return sorted(self.bone_index_map.values(), key=lambda b: b.id)