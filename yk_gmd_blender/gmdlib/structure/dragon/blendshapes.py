from dataclasses import dataclass

from ....structurelib.base import StructureUnpacker
from ....structurelib.primitives import c_uint32, c_uint64


@dataclass
class BlendshapeSpec:
    n_blendshapes_always_one: int  # always 1

    # The offset in the file of the ChecksumStr indicating the name of the blendshape
    blendshape_name_offset: int
    original_vertex_packing_flags: int
    blendshape_vertex_offset_packing_flags: int
    original_vertex_stride: int
    blendshape_vertex_offset_stride: int
    blendshape_vertex_offset_count: int
    blendshape_vertex_offset_data_offset: int
    blendshape_vertex_offset_data_size: int


BlendshapeSpec_Unpack = StructureUnpacker(
    BlendshapeSpec,
    fields=[
        ("n_blendshapes_always_one", c_uint32),
        ("blendshape_name_offset", c_uint32),
        ("original_vertex_packing_flags", c_uint64),
        ("blendshape_vertex_offset_packing_flags", c_uint64),
        ("original_vertex_stride", c_uint32),
        ("blendshape_vertex_offset_stride", c_uint32),
        ("blendshape_vertex_offset_count", c_uint32),
        ("blendshape_vertex_offset_data_size", c_uint32),
        ("blendshape_vertex_offset_data_offset", c_uint32),
    ]
)
