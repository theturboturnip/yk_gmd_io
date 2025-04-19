from dataclasses import dataclass

from ....structurelib.base import StructureUnpacker
from ....structurelib.primitives import c_uint32, c_uint64


@dataclass
class BlendshapeSpec:
    """
    Blendshape files have an extra entry directly after the header.
    This entry specifies
    1) how many blendshapes there are
    2) where the array of ChecksumStrStructs is for the blendshape names
    3) where the array of blendshape vertex buffers are

    There can be many blendshape vertex buffers, which all apply to the lone main vertex buffer in the file.
    Each blendshape vertex buffer encodes an offset in (position, normal, tangent) on that main vertex buffer,
    so uses a different vertex format than the main vertex buffer.
    There is only one "blendshape vertex format", but it will be different to the main vertex buffer format.
    """

    num_blendshapes: int

    # The offset in the file of the array of ChecksumStrs indicating blendshape names
    blendshape_name_array_ptr: int

    # The vertex format the main buffer should have
    original_vertex_packing_flags: int
    # The vertex format the blendshape buffers use
    blendshape_vertex_packing_flags: int

    # The bytes-per-vertex of the main buffer
    original_vertex_stride: int
    # The bytes-per-vertex of each blendshape buffer
    blendshape_vertex_stride: int

    # The number of vertices per blendshape buffer
    per_blendshape_vertex_count: int
    # The size in bytes of each blendshape buffer
    per_blendshape_vertex_buffer_size: int

    # The offset in the file of the array of blendshape buffers
    blendshape_vertex_buffer_array_ptr: int


BlendshapeSpec_Unpack = StructureUnpacker(
    BlendshapeSpec,
    fields=[
        ("num_blendshapes", c_uint32),

        ("blendshape_name_array_ptr", c_uint32),

        ("original_vertex_packing_flags", c_uint64),
        ("blendshape_vertex_packing_flags", c_uint64),

        ("original_vertex_stride", c_uint32),
        ("blendshape_vertex_stride", c_uint32),

        ("per_blendshape_vertex_count", c_uint32),
        ("per_blendshape_vertex_buffer_size", c_uint32),

        ("blendshape_vertex_buffer_array_ptr", c_uint32),
    ]
)
