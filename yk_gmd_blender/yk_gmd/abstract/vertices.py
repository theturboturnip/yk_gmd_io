import struct
from dataclasses import dataclass, field
from typing import Tuple, List, Optional

from .vector import Vec3, Vec4


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
    diffuse: Optional[Vec4]
    opacity: Optional[float]
    specular: Optional[Vec4]
    uv0: Tuple[float, float]
    uv1: Tuple[float, float]

    def __init__(self):
        self.pos = None
        self.weights = None
        self.normal = None
        self.tangent = None
        self.diffuse = None
        self.specular = None
        self.uv0 = None
        self.uv1 = None


@dataclass(frozen=True)
class GMDVertexBufferLayout:
    pos_type: int
    weights_type: int
    bones_en: int
    normal_type: int
    tangent_type: int
    unk_type: int
    diffuse_type: int
    specular_type: int
    uv_type: int


    def get_vector_format_string(self, value):
        format_string = ""
        for i in range(value):
            if value >= 3:
                format_string += "f"
            elif value == 2:
                format_string += "ee"
            else:
                format_string += "BBBB"
        return format_string

    def get_type_format_string(self, name):
        format_string = ">"
        if name == "pos":
            for i in range(self.pos_type):
                format_string += "f" if self.pos_type - 2 > 0 else "e"
        if name == "weights":
            format_string += self.get_vector_format_string(self.weights_type)
        if name == "bones":
            format_string += "BBBB"
        if name == "normal":
            format_string += self.get_vector_format_string(self.normal_type)
        if name == "tangent":
            format_string += self.get_vector_format_string(self.tangent_type)
        if name == "unk":
            format_string += self.get_vector_format_string(self.unk_type)
        if name == "diffuse":
            format_string += self.get_vector_format_string(self.diffuse_type)
        if name == "specular":
            format_string += self.get_vector_format_string(self.specular_type)
        if name == "uv":
            index = [(self.uv_type >> 4, 0), (self.uv_type >> 12, 1), (self.uv_type >> 20, 2)]
            index.sort(key=lambda tup: tup[0], reverse=True)
            for i in range(len(index)):
                if index[i][1] == 0:
                    for t in range(self.uv_type & 0x0F):
                        format_string += "BBxx"
                    format_string += "/"
                elif index[i][1] == 1:
                    for t in range((self.uv_type >> 8) & 0x0F):
                        format_string += "ee"
                    format_string += "/"
                else:
                    for t in range((self.uv_type >> 16) & 0x0F):
                        format_string += "ff"
                    format_string += "/"
        return format_string

    def calc_bytes_per_vertex(self):
        bpv = 0
        if self.pos_type:
            # pos can be 3 or 4 * 16bit or 32bit floats
            bpv += 4 * self.pos_type if self.pos_type != 1 else 6
        if self.weights_type:
            # weights can be 4 * 16bit or 32bit floats, or 4 * 8bit fixed point
            bpv += 4 * self.weights_type
        if self.bones_en:
            # bone ids are 4 * 1 byte
            bpv += 4 * self.bones_en
        if self.normal_type:
            # normal can be 4 * 16bit or 3 * 32bit floats, or 4 * 8bit fixed point
            bpv += 4 * self.normal_type
        if self.tangent_type:
            # tangent can be 4 * 16bit or 3 * 32bit floats, or 4 * 8bit fixed point
            bpv += 4 * self.tangent_type
        if self.unk_type:
            # unk can be 4 * 16bit or 3 * 32bit floats, or 4 * 8bit fixed point
            bpv += 4 * self.unk_type
        if self.diffuse_type:
            # diffuse can be 4 * 16bit or 32bit floats, or 4 * 8bit fixed point
            # last float is opacity
            bpv += 4 * self.diffuse_type
        if self.specular_type:
            # specular can be 4 * 16bit or 32bit floats, or 4 * 8bit fixed point
            # last float is always null
            bpv += 4 * self.specular_type
        if self.uv_type:
            # uv can be 2 * 16bit or 32bit floats, or 4 * 8bit fixed point
            # there can be multiple uv for a single vertex
            bpv += 4 * (self.uv_type & 0x0F)
            bpv += 4 * ((self.uv_type >> 8) & 0x0F)
            bpv += 8 * ((self.uv_type >> 16) & 0x0F)
        return bpv

    def unpack_vertices(self, vertex_count: int, data: bytes, start_offset=0) -> List[GMDVertex]:
        bpv = self.calc_bytes_per_vertex()

        vertices: List[GMDVertex] = [None] * vertex_count
        for i in range(vertex_count):
            vtx_data = data[start_offset + (i * bpv):start_offset + ((i + 1) * bpv)]

            vertex = GMDVertex()
            offset = 0
            if self.pos_type:
                format_string = self.get_type_format_string("pos")
                vertex.pos = Vec3(*struct.unpack_from(format_string, vtx_data, offset=offset))
                offset += struct.calcsize(format_string)
            if self.weights_type:
                format_string = self.get_type_format_string("weights")
                if "B" in format_string:
                    weight_bytes = Vec4(
                        *[x / 255.0 for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                else:
                    weight_bytes = Vec4(*[x for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                offset += struct.calcsize(format_string)
                bone_bytes = struct.unpack_from(">BBBB", vtx_data, offset=offset)
                vertex.weights = (
                    BoneWeight(bone=bone_bytes[0], weight=weight_bytes[0]),
                    BoneWeight(bone=bone_bytes[1], weight=weight_bytes[1]),
                    BoneWeight(bone=bone_bytes[2], weight=weight_bytes[2]),
                    BoneWeight(bone=bone_bytes[3], weight=weight_bytes[3]),
                )
                offset += struct.calcsize(">BBBB")
            if self.normal_type:
                format_string = self.get_type_format_string("normal")
                if "B" in format_string:
                    vertex.normal = Vec4(
                        *[((x / 255.0) * 2 - 1) for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                else:
                    vertex.normal = Vec4(
                        *[x for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                offset += struct.calcsize(format_string)
            if self.tangent_type:
                format_string = self.get_type_format_string("tangent")
                if "B" in format_string:
                    vertex.tangent = Vec4(
                        *[((x / 255.0) * 2 - 1) for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                else:
                    vertex.tangent = Vec4(
                        *[x for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                offset += struct.calcsize(format_string)
            if self.diffuse_type:
                format_string = self.get_type_format_string("diffuse")
                if "B" in format_string:
                    vertex.diffuse = Vec4(
                        *[x / 255.0 for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                else:
                    vertex.diffuse = Vec4(*[x for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                offset += struct.calcsize(format_string)
            if self.specular_type:
                format_string = self.get_type_format_string("specular")
                if "B" in format_string:
                    vertex.specular = Vec4(
                        *[x / 255.0 for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                else:
                    vertex.specular = Vec4(*[x for x in struct.unpack_from(format_string, vtx_data, offset=offset)])
                offset += struct.calcsize(format_string)
            if self.uv_type:
                format_string = self.get_type_format_string("uv")
                format_list = format_string.split("/")
                if "B" in format_list[1]:
                    vertex.uv0 = [x / 255.0 for x in struct.unpack_from(">" + format_list[1], vtx_data, offset=offset)]
                else:
                    vertex.uv0 = [x for x in struct.unpack_from(">" + format_list[1], vtx_data, offset=offset)]

                offset += struct.calcsize(format_list[1])
                vertex.uv1 = [0, 0]
                if len(format_list) > 2:
                    if "B" in format_list[2]:
                        vertex.uv1 = [x / 255.0 for x in
                                      struct.unpack_from(">" + format_list[2], vtx_data, offset=offset)]
                    else:
                        vertex.uv1 = [x for x in struct.unpack_from(">" + format_list[2], vtx_data, offset=offset)]
                    offset += struct.calcsize(">" + format_list[2])

            vertices[i] = vertex
        return vertices

    def pack_vertices(self, vertices: List[GMDVertex]) -> bytes:
        bs = bytearray()

        for vertex in vertices:
            if self.pos_en:
                bs += struct.pack(">fff", vertex.pos.x, vertex.pos.y, vertex.pos.z)
            if self.weights_en:
                bs += struct.pack(">BBBBBBBB",
                                  int(vertex.weights[0].weight * 255),
                                  int(vertex.weights[1].weight * 255),
                                  int(vertex.weights[2].weight * 255),
                                  int(vertex.weights[3].weight * 255),

                                  vertex.weights[0].bone,
                                  vertex.weights[1].bone,
                                  vertex.weights[2].bone,
                                  vertex.weights[3].bone,
                                  )
            if self.normal_en:
                # Normals are stored in the file with 0.5 at the midpoint i.e. 0 => -1, 0.5 => 0, 1 => 1
                bs += struct.pack(">BBBB",
                                  int((vertex.normal.x + 1)/2 * 255),
                                  int((vertex.normal.y + 1)/2 * 255),
                                  int((vertex.normal.z + 1)/2 * 255),
                                  int((vertex.normal.w + 1)/2 * 255),
                                  )
            if self.tangent_en:
                # Tangents are stored like normals
                bs += struct.pack(">BBBB",
                                  int((vertex.tangent.x + 1)/2 * 255),
                                  int((vertex.tangent.y + 1)/2 * 255),
                                  int((vertex.tangent.z + 1)/2 * 255),
                                  int((vertex.tangent.w + 1)/2 * 255),
                                  )
            if self.col0_en:
                bs += struct.pack(">BBBB",
                                  int(vertex.col0.x * 255),
                                  int(vertex.col0.y * 255),
                                  int(vertex.col0.z * 255),
                                  int(vertex.col0.w * 255),
                                  )
            if self.col1_en:
                bs += struct.pack(">BBBB",
                                  int(vertex.col1.x * 255),
                                  int(vertex.col1.y * 255),
                                  int(vertex.col1.z * 255),
                                  int(vertex.col1.w * 255),
                                  )
            if self.uv_en:
                if self.uv_elem_bytes == 2:
                    fmt = ">ee"
                elif self.uv_elem_bytes == 4:
                    fmt = ">ff"
                bs += struct.pack(fmt, vertex.uv[0], vertex.uv[1])

        return bytes(bs)


@dataclass(repr=False, frozen=True)
class GMDVertexBuffer:
    id: int
    layout: GMDVertexBufferLayout
    vertices: List[GMDVertex] = field(default_factory=list)
