from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ComponentType(Enum):
    Fixed = 'B',
    Half = 'e',
    Full = 'f',


@dataclass(frozen=True)
class VectorLayout:
    type: ComponentType
    length: int

    def get_format_string(self):
        return self.type.value * self.length


# VertexBufferLayouts are external dependencies (shaders have a fixed layout, which we can't control) so they are frozen
@dataclass(frozen=True)
class GMDVertexBufferLayout:
    pos_type: VectorLayout
    weights_type: VectorLayout
    bones_type: VectorLayout
    normal_type: Optional[VectorLayout]
    tangent_type: Optional[VectorLayout]
    unk_type: Optional[VectorLayout]
    col0_type: Optional[VectorLayout]
    col1_type: Optional[VectorLayout]
    uv0_type: Optional[VectorLayout]
    uv1_type: Optional[VectorLayout]

    #def get_packing_order

    # TODO: Pack/unpack functions using the VectorLayouts

# Shaders are external dependencies, so they are frozen. You can't change the name of a shader, for example.
@dataclass(frozen=True)
class GMDShader:
    name: str
    vertex_buffer_layout: GMDVertexBufferLayout