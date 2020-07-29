from ctypes import *

from yk_gmd_blender.yk_gmd.legacy.abstract.vertices import GMDVertexBufferLayout, VecTypes
from ._base.base_structure import BaseBigEndianStructure


class VertexBufferLayoutStruct(BaseBigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("id", c_uint32),
        ("vertex_count", c_uint32),
        ("vertex_packing", c_uint64),
        ("vertex_data_start", c_uint32),
        ("vertex_data_length", c_uint32), # length in bytes
        ("bytes_per_vertex", c_uint32),
        ("null", c_uint32),
    ]

    @property
    def flags(self):
        return [(int(self.vertex_packing)>>52)&0xFF,
                (int(self.vertex_packing)>>48)&0xFF,
                (int(self.vertex_packing)>>40)&0xFF,
                (int(self.vertex_packing)>>32)&0xFF,
                (int(self.vertex_packing)>>24)&0xFF,
                (int(self.vertex_packing)>>16)&0xFF,
                (int(self.vertex_packing)>>8)&0xFF,
                (int(self.vertex_packing)>>0)&0xFF
                ]

    def get_vector_type(self, shift):
        vector_type = (int(self.vertex_packing) >> shift) & 3
        if vector_type == 0:
            return VecTypes.VECTOR4
        elif vector_type == 1:
            return VecTypes.VECTOR4_HALF
        else:
            return VecTypes.FIXED_POINT

    def get_property_type(self, name):
        vertex_packing = int(self.vertex_packing)
        if name == "pos":
            # pos can be (3 or 4) * (16bit or 32bit) floats
            pos_count = vertex_packing & 7
            if (vertex_packing >> 3) & 1:
                return VecTypes.VECTOR3_HALF if pos_count == 3 else VecTypes.VECTOR4_HALF
            else:
                return VecTypes.VECTOR3 if pos_count == 3 else VecTypes.VECTOR4
        if name == "weights":
            # weights can be 4 * 16bit or 32bit floats, or 4 * 8bit fixed point
            return self.get_vector_type(7)
        if name == "bones":
            # bone ids are 4 * 1 byte, not actually a vector
            return VecTypes.FIXED_POINT
        if name == "normal":
            # normal can be 4 * 16bit or 3 * 32bit floats, or 4 * 8bit fixed point
            result = self.get_vector_type(0xB)
            return result if result != VecTypes.VECTOR4 else VecTypes.VECTOR3
        if name == "tangent":
            # tangent uses the same format as normal
            result = self.get_vector_type(0xE)
            return result if result != VecTypes.VECTOR4 else VecTypes.VECTOR3
        if name == "unk":
            # unk uses the same format as normal
            result = self.get_vector_type(0x11)
            return result if result != VecTypes.VECTOR4 else VecTypes.VECTOR3
        if name == "col0":
            # col0 uses the same format as weights
            # col0 is diffuse and opacity for GMD versions up to 0x03000B
            return self.get_vector_type(0x16)
        if name == "col1":
            # col1 uses the same format as col0
            # col1 is specular for GMD versions up to 0x03000B
            return self.get_vector_type(0x19)
        if name in ["uv0", "uv1"]:
            # uv can be 2 * 16bit or 32bit floats, or 4 * 8bit fixed point
            # there can be multiple uv for a single vertex
            if name == "uv0":
                if not vertex_packing & (1 << 0x1B):
                    # likely not to be UV
                    # treat as Vector2
                    return VecTypes.VECTOR2
            # this assumes that uv_count can't be greater than 2
            i = 0 if name == "uv0" else 4
            uv_count = c_uint32(vertex_packing).value >> 0x1C
            if name == "uv1":
                uv_count -= 1
            if uv_count > 0:
                shift = (vertex_packing >> (0x20 + i)) & 0xF
                if c_uint8(shift).value == 0xF:
                    return 0
                shift = (vertex_packing >> (0x22 + i)) & 3
                if shift:
                    if shift != 1:
                        # 4 * 8bit fixed point
                        return VecTypes.FIXED_POINT
                    # Vector2Half
                    return VecTypes.VECTOR2_HALF
                else:
                    # Vector2
                    return VecTypes.VECTOR2
            return 0

    def get_vertex_layout(self) -> GMDVertexBufferLayout:
        vertex_elems = {}
        vertex_layout_bits = [
            ("pos", 0x07),
            ("weights", 0x70),
            ("bones", 0x200),
            ("normal", 0x400),
            ("tangent", 0x2000),
            ("unk", 0x1_0000),
            ("col0", 0x0020_0000),
            ("col1", 0x0100_0000),
            ("uv0", 0xf000_0000),
            ("uv1", 0xf000_0000),
        ]

        for name, bitmask in vertex_layout_bits:
            if int(self.vertex_packing) & bitmask:
                vertex_elems[name] = self.get_property_type(name)
            else:
                vertex_elems[name] = 0

        #print(vertex_elems)

        return GMDVertexBufferLayout(
            pos_type=vertex_elems["pos"],
            weights_type=vertex_elems["weights"],
            bones_type=vertex_elems["bones"],
            normal_type=vertex_elems["normal"],
            tangent_type=vertex_elems["tangent"],
            unk_type=vertex_elems["unk"],
            col0_type=vertex_elems["col0"],
            col1_type=vertex_elems["col1"],
            uv0_type=vertex_elems["uv0"],
            uv1_type=vertex_elems["uv1"],
        )