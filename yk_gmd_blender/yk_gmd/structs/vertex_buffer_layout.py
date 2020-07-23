from ctypes import *

from yk_gmd_blender.yk_gmd.abstract.vertices import GMDVertexBufferLayout
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
            # 4 = Vector4
            # 3 = Vector3
            return 4
        elif vector_type == 1:
            # 2 = Vector4Half
            return 2
        else:
            # 1 = 4 * 8bit fixed point
            return 1

    def get_property_type(self, name):
        vertex_packing = int(self.vertex_packing)
        if name == "pos":
            pos_count = vertex_packing & 7
            if (vertex_packing >> 3) & 1:
                # 1 = Vector3Half (unlikely to be used)
                # 2 = Vector4Half
                return pos_count - 2
            else:
                # 3 = Vector3
                # 4 = Vector4
                return pos_count
        if name == "weights":
            return self.get_vector_type(7)
        if name == "bones":
            return 1
        if name == "normal":
            result = self.get_vector_type(0xB)
            return result if result != 4 else 3
        if name == "tangent":
            result = self.get_vector_type(0xE)
            return result if result != 4 else 3
        if name == "unk":
            result = self.get_vector_type(0x11)
            return result if result != 4 else 3
        if name == "diffuse":
            return self.get_vector_type(0x16)
        if name == "specular":
            return self.get_vector_type(0x19)
        if name == "uv":
            if not vertex_packing & (1 << 0x1B):
                # likely not to be UV
                # treat as Vector2
                return 1 << 16

            # this assumes that uv_count can't be greater than 2
            i = 0x1C
            result = 0
            uv_count = c_uint32(vertex_packing).value >> 0x1C
            while uv_count > 0:
                i += 4
                shift = (vertex_packing >> i) & 0xF
                if c_uint8(shift).value == 0xF:
                    continue
                uv_count -= 1
                shift = (vertex_packing >> (i + 2)) & 3
                if shift:
                    if shift != 1:
                        # add uv_count as index per type (highest comes first)
                        # each 0x1 is a 4 * 8bit fixed point
                        result += 1 + (uv_count << 4)
                        continue
                    # each 0x100 is a Vector2Half
                    result += (1 << 8) + (uv_count << 12)
                else:
                    # each 0x10000 is a Vector2
                    result += (1 << 16) + (uv_count << 20)
            return result

    def get_vertex_layout(self) -> GMDVertexBufferLayout:
        vertex_elems = {}
        vertex_layout_bits = [
            ("pos", 0x07),
            ("weights", 0x70),
            ("bones", 0x200),
            ("normal", 0x400),
            ("tangent", 0x2000),
            ("unk", 0x10000),
            ("diffuse", 0x0020_0000),
            ("specular", 0x0100_0000),
            ("uv",   0xf000_0000),
        ]

        for (name, bitmask) in vertex_layout_bits:
            vertex_elems[name] = 0 if int(self.vertex_packing) & bitmask else -1
        for (name) in vertex_elems:
            if vertex_elems[name] == -1:
                vertex_elems[name] = 0
                continue
            vertex_elems[name] = self.get_property_type(name)

        print(vertex_elems)

        return GMDVertexBufferLayout(
            pos_type=vertex_elems["pos"],
            weights_type=vertex_elems["weights"],
            bones_en=vertex_elems["bones"],
            normal_type=vertex_elems["normal"],
            tangent_type=vertex_elems["tangent"],
            unk_type=vertex_elems["unk"],
            diffuse_type=vertex_elems["diffuse"],
            specular_type=vertex_elems["specular"],
            uv_type=vertex_elems["uv"],
        )