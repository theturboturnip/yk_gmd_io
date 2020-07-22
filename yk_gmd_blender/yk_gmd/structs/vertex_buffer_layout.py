from ctypes import *

from yk_gmd_blender.yk_gmd.abstract.vertices import GMDVertexBufferLayout
from ._base.base_structure import BaseBigEndianStructure


class VertexBufferLayoutStruct(BaseBigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("id", c_uint32),
        ("vertex_count", c_uint32),

        ("zero", c_ubyte * 3),
        ("uv_flags", c_ubyte),
        ("vertex_packing", c_uint32),

        ("vertex_data_start", c_uint32),
        ("vertex_data_length", c_uint32), # length in bytes
        ("bytes_per_vertex", c_uint32),
        ("null", c_uint32),
    ]

    @property
    def flags(self):
        return [self.zero[0],self.zero[1],self.zero[3],self.uv_flags,
                (int(self.vertex_packing)>>24)&0xFF,
                (int(self.vertex_packing)>>16)&0xFF,
                (int(self.vertex_packing)>>8)&0xFF,
                (int(self.vertex_packing)>>0)&0xFF,
                ]

    def all_bits(self, data, bitmask):
        return (data & bitmask) == bitmask

    def get_vertex_layout(self) -> GMDVertexBufferLayout:
        vertex_layout_bits = [
            ("pos", 0x03),
            ("weights", 0x3c0),
            ("normal", 0x1c00),
            ("tangent", 0xe000),

            ("col0", 0x00e0_0000),
            ("col1", 0x0700_0000),
            ("uv",   0x1800_0000),
        ]
        overall_bitmask = 0
        vertex_elems = {}
        for (name, bitmask) in vertex_layout_bits:
            overall_bitmask = overall_bitmask | bitmask
            vertex_elems[name] = self.all_bits(int(self.vertex_packing), bitmask)
        # overall_bitmask should equal 0x1FE0_FFC3
        # there should also be no bits set outside of the bitmask

        uv_bytes = 0
        if self.uv_flags == 0x4:
            uv_bytes = 2
        elif self.uv_flags == 0x44:
            uv_bytes = 4

        print(vertex_elems)

        return GMDVertexBufferLayout(
            pos_en=vertex_elems["pos"],
            weights_en=vertex_elems["weights"],
            normal_en=vertex_elems["normal"],
            tangent_en=vertex_elems["tangent"],
            col0_en=vertex_elems["col0"],
            col1_en=vertex_elems["col1"],
            uv_en=vertex_elems["uv"],
            uv_elem_bytes=uv_bytes
        )