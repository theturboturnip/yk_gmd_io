from ctypes import *

from ._base.base_structure import BaseBigEndianStructure


class IndicesStruct(BaseBigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("index_cnt", c_uint32),
        ("index_start", c_uint32),
    ]

    def extract_range(self, indices):
        return indices[self.index_start:self.index_start+self.index_cnt]


class SubmeshStruct(BaseBigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("id", c_uint32),
        ("material_id", c_uint32),
        ("vertex_buffer_id", c_uint32),
        ("vertex_count", c_uint32),

        ("indices_triangle", IndicesStruct),
        ("indices_trianglestrip_1", IndicesStruct),
        ("indices_trianglestrip_2", IndicesStruct),

        ("bonelist_length", c_uint32), # Usually caps at 32.
        ("bonelist_start", c_uint32),

        # These don't matter to the game?
        ("part_bone_number", c_uint32), # Usually caps at the amount of bones in the mesh?
        ("part_number", c_uint32), # [0, 20] in Kiwami Bob, always 0 for generic dude. Fits in partstructs
        # in Kiwami bob, linked_l0_bone_maybe == linked_l0_number_maybe + 126 i.e. linked_l0_number_maybe is the index within the l0 space, linked_l0_bone_maybe is the actual index in the bones hierarchy

        ("zero", c_uint32), # All zero

        ("vertex_start", c_uint32), # The index of the first vertex used by this submesh
        # The vertices for this submesh are contained within the vertex buffer in the range [vertex_start, vertex_start + vertex_count).
        # The actual length of this array is dependent on the bytes_per_vertex for the given vertex buffer.
    ]

    def __str__(self):
        return " ".join(str(x) for x in [
            self.id,
            self.material_id,
            self.vertex_buffer_id,
            self.vertex_count,
            " ",
            self.indices_triangle.index_cnt,
            self.indices_triangle.index_start,
            self.indices_trianglestrip_1.index_cnt,
            self.indices_trianglestrip_1.index_start,
            self.indices_trianglestrip_2.index_cnt,
            self.indices_trianglestrip_2.index_start,
            " ",
            self.bonelist_length,
            self.bonelist_start,
            self.linked_l0_bone_maybe,
            self.linked_l0_number_maybe,
            self.zero,
            self.vertex_start
        ])