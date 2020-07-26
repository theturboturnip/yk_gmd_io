import struct
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Tuple, List, Optional

from .vector import Vec3, Vec4


class VecTypes(IntEnum):
    FIXED_POINT = 1
    VECTOR2 = 2
    VECTOR3 = 3
    VECTOR4 = 4
    VECTOR2_HALF = 5
    VECTOR3_HALF = 6
    VECTOR4_HALF = 7


@dataclass
class BoneWeight:
    bone: int
    weight: float


@dataclass(init=False)
class GMDVertex:
    pos: Vec3
    weights: Tuple[BoneWeight, BoneWeight, BoneWeight, BoneWeight]
    normal: Optional[Vec4]
    tangent: Optional[Vec4]
    col0: Optional[Vec4]
    col1: Optional[Vec4]
    uv0: Tuple[float, float]
    uv1: Tuple[float, float]

    def __init__(self):
        self.pos = None
        self.weights = None
        self.normal = None
        self.tangent = None
        self.col0 = None
        self.col1 = None
        self.uv0 = None
        self.uv1 = None


@dataclass(frozen=True)
class GMDVertexBufferLayout:
    pos_type: int
    weights_type: int
    bones_type: int
    normal_type: int
    tangent_type: int
    unk_type: int
    col0_type: int
    col1_type: int
    uv0_type: int
    uv1_type: int

    @staticmethod
    def get_vector_format_string(value):
        if value == VecTypes.FIXED_POINT:
            return "BBBB"
        if value == VecTypes.VECTOR2:
            return "ff"
        if value == VecTypes.VECTOR3:
            return "fff"
        if value == VecTypes.VECTOR4:
            return "ffff"
        if value == VecTypes.VECTOR2_HALF:
            return "ee"
        if value == VecTypes.VECTOR3_HALF:
            return "eee"
        if value == VecTypes.VECTOR4_HALF:
            return "eeee"
        return ""

    def get_type_format_string(self, name):
        if name == "pos":
            return self.get_vector_format_string(int(self.pos_type))
        if name == "weights":
            return self.get_vector_format_string(int(self.weights_type))
        if name == "bones":
            return self.get_vector_format_string(int(self.bones_type))
        if name == "normal":
            return self.get_vector_format_string(int(self.normal_type))
        if name == "tangent":
            return self.get_vector_format_string(int(self.tangent_type))
        if name == "unk":
            return self.get_vector_format_string(int(self.unk_type))
        if name == "col0":
            return self.get_vector_format_string(int(self.col0_type))
        if name == "col1":
            return self.get_vector_format_string(int(self.col1_type))
        if name == "uv0":
            return self.get_vector_format_string(int(self.uv0_type))
        if name == "uv1":
            return self.get_vector_format_string(int(self.uv1_type))
        return ""

    def calc_bytes_per_vertex(self):
        bpv = 0
        for vec_type in vars(self).values():
            if vec_type:
                bpv += struct.calcsize(">" + self.get_vector_format_string(int(vec_type)))
        return bpv

    def unpack_vertices(self, vertex_count: int, data: bytes, start_offset=0) -> List[GMDVertex]:
        bpv = self.calc_bytes_per_vertex()
        format_strings = {}
        for name in ["pos", "weights", "normal", "tangent", "col0", "col1", "uv0", "uv1"]:
            # TODO change ">" to account for different endianness
            format_strings[name] = ">" + self.get_type_format_string(name)

        vertices: List[GMDVertex] = [None] * vertex_count
        for i in range(vertex_count):
            vtx_data = data[start_offset + (i * bpv):start_offset + ((i + 1) * bpv)]

            vertex = GMDVertex()
            offset = 0
            if self.pos_type:
                format_string = format_strings["pos"]
                vertex.pos = Vec3(*struct.unpack_from(format_string, vtx_data, offset=offset))
                offset += struct.calcsize(format_string)
            if self.weights_type:
                format_string = format_strings["weights"]
                if "B" in format_string:
                    weight_bytes = Vec4(
                        *[x / 255.0 for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                else:
                    weight_bytes = Vec4(*[x for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                offset += struct.calcsize(format_string)

                # this assumes that bones are present whenever weights are
                bone_bytes = struct.unpack_from(">BBBB", vtx_data, offset=offset)
                vertex.weights = (
                    BoneWeight(bone=bone_bytes[0], weight=weight_bytes[0]),
                    BoneWeight(bone=bone_bytes[1], weight=weight_bytes[1]),
                    BoneWeight(bone=bone_bytes[2], weight=weight_bytes[2]),
                    BoneWeight(bone=bone_bytes[3], weight=weight_bytes[3]),
                )
                offset += struct.calcsize(">BBBB")
            if self.normal_type:
                format_string = format_strings["normal"]
                if "B" in format_string:
                    vertex.normal = Vec4(
                        *[((x / 255.0) * 2 - 1) for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                else:
                    vertex.normal = Vec4(
                        *[x for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                offset += struct.calcsize(format_string)
            if self.tangent_type:
                format_string = format_strings["tangent"]
                if "B" in format_string:
                    vertex.tangent = Vec4(
                        *[((x / 255.0) * 2 - 1) for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                else:
                    vertex.tangent = Vec4(
                        *[x for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                offset += struct.calcsize(format_string)
            if self.col0_type:
                format_string = format_strings["col0"]
                if "B" in format_string:
                    vertex.col0 = Vec4(*[x / 255.0 for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                else:
                    vertex.col0 = Vec4(*[x for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                offset += struct.calcsize(format_string)
            if self.col1_type:
                format_string = format_strings["col1"]
                if "B" in format_string:
                    vertex.col1 = Vec4(*[x / 255.0 for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                else:
                    vertex.col1 = Vec4(*[x for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                offset += struct.calcsize(format_string)
            if self.uv0_type:
                format_string = format_strings["uv0"]
                if "B" in format_string:
                    vertex.uv0 = [x / 255.0 for x in struct.unpack_from(format_string, vtx_data, offset=offset)]
                else:
                    vertex.uv0 = [x for x in struct.unpack_from(format_string, vtx_data, offset=offset)]
                offset += struct.calcsize(format_string)
            if self.uv1_type:
                format_string = format_strings["uv1"]
                if "B" in format_string:
                    vertex.uv1 = [x / 255.0 for x in struct.unpack_from(format_string, vtx_data, offset=offset)]
                else:
                    vertex.uv1 = [x for x in struct.unpack_from(format_string, vtx_data, offset=offset)]
                offset += struct.calcsize(format_string)

            vertices[i] = vertex
        return vertices

    def pack_vertices(self, vertices: List[GMDVertex]) -> bytes:
        bs = bytearray()
        format_strings = {}
        for name in ["pos", "weights", "normal", "tangent", "col0", "col1", "uv0", "uv1"]:
            # TODO change ">" to account for different endianness
            format_strings[name] = ">" + self.get_type_format_string(name)

        for vertex in vertices:
            if self.pos_type:
                format_string = format_strings["pos"]
                bs += struct.pack(format_string, vertex.pos.x, vertex.pos.y, vertex.pos.z)
            if self.weights_type:
                format_string = format_strings["weights"]
                if "B" in format_string:
                    bs += struct.pack(format_string,
                                      int(vertex.weights[0].weight * 255),
                                      int(vertex.weights[1].weight * 255),
                                      int(vertex.weights[2].weight * 255),
                                      int(vertex.weights[3].weight * 255),
                                      )
                else:
                    bs += struct.pack(format_string,
                                      vertex.weights[0].weight,
                                      vertex.weights[1].weight,
                                      vertex.weights[2].weight,
                                      vertex.weights[3].weight,
                                      )
                bs += struct.pack(">BBBB",
                                  vertex.weights[0].bone,
                                  vertex.weights[1].bone,
                                  vertex.weights[2].bone,
                                  vertex.weights[3].bone,
                                  )
            if self.normal_type:
                format_string = format_strings["normal"]
                if "B" in format_string:
                    normal = vertex.normal.as_fixed_point(is_normal=True)
                    bs += struct.pack(">BBBB", normal[0], normal[1], normal[2], normal[3])
                else:
                    bs += struct.pack(format_string, vertex.normal.x, vertex.normal.y, vertex.normal.z,
                                      vertex.normal.w)
            if self.tangent_type:
                format_string = format_strings["tangent"]
                if "B" in format_string:
                    tangent = vertex.tangent.as_fixed_point(is_normal=True)
                    bs += struct.pack(">BBBB", tangent[0], tangent[1], tangent[2], tangent[3])
                else:
                    bs += struct.pack(format_string, vertex.tangent.x, vertex.tangent.y, vertex.tangent.z,
                                      vertex.tangent.w)
            if self.col0_type:
                format_string = format_strings["col0"]
                if "B" in format_string:
                    col0 = vertex.col0.as_fixed_point(is_normal=False)
                    bs += struct.pack(">BBBB", col0[0], col0[1], col0[2], col0[3])
                else:
                    bs += struct.pack(format_string, vertex.col0.x, vertex.col0.y, vertex.col0.z,
                                      vertex.col0.w)
            if self.col1_type:
                format_string = format_strings["col1"]
                if "B" in format_string:
                    col1 = vertex.col1.as_fixed_point(is_normal=False)
                    bs += struct.pack(">BBBB", col1[0], col1[1], col1[2], col1[3])
                else:
                    bs += struct.pack(format_string, vertex.col1.x, vertex.col1.y, vertex.col1.z,
                                      vertex.col1.w)
            if self.uv0_type:
                format_string = format_strings["uv0"]
                if "B" in format_string:
                    bs += struct.pack(format_string, int(vertex.uv0[0] * 255), int(vertex.uv0[1] * 255))
                else:
                    bs += struct.pack(format_string, vertex.uv0[0], vertex.uv0[1])
            if self.uv1_type:
                format_string = format_strings["uv1"]
                if "B" in format_string:
                    bs += struct.pack(format_string, int(vertex.uv1[0] * 255), int(vertex.uv1[1] * 255))
                else:
                    bs += struct.pack(format_string, vertex.uv1[0], vertex.uv1[1])
        return bytes(bs)


@dataclass(repr=False, frozen=True)
class GMDVertexBuffer:
    id: int
    layout: GMDVertexBufferLayout
    vertices: List[GMDVertex] = field(default_factory=list)
