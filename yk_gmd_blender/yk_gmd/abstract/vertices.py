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
    col0: Optional[Vec4]
    col1: Optional[Vec4]
    uv: Tuple[float, float]

    def __init__(self):
        self.pos = None
        self.weights = None
        self.normal = None
        self.tangent = None
        self.col0 = None
        self.col1 = None
        self.uv = None


@dataclass(frozen=True)
class GMDVertexBufferLayout:
    pos_en: bool
    weights_en: bool
    normal_en: bool
    tangent_en: bool
    col0_en: bool
    col1_en: bool
    uv_en: bool
    uv_elem_bytes: int  # uv components are 16 or 32 bit floating point

    def calc_bytes_per_vertex(self):
        bpv = 0
        if self.pos_en:
            # pos is 32 bit floats
            bpv += 4 * 3
        if self.weights_en:
            # bone id = 1 byte, weight = 1 byte fixed point
            # 4 weights
            bpv += 2 * 4
        if self.normal_en:
            # normal is 4 * 8bit fixed point
            bpv += 4
        if self.tangent_en:
            # tangent is 4 * 8bit fixed point
            bpv += 4
        if self.col0_en:
            # colors is 4 * 8bit fixed point
            bpv += 4
        if self.col1_en:
            # colors is 4 * 8bit fixed point
            bpv += 4
        if self.uv_en:
            bpv += 2 * self.uv_elem_bytes
        return bpv

    def unpack_vertices(self, vertex_count: int, data: bytes, start_offset=0) -> List[GMDVertex]:
        bpv = self.calc_bytes_per_vertex()

        vertices: List[GMDVertex] = [None] * vertex_count
        for i in range(vertex_count):
            vtx_data = data[start_offset + (i * bpv):start_offset + ((i + 1) * bpv)]

            vertex = GMDVertex()
            offset = 0
            if self.pos_en:
                vertex.pos = Vec3(*struct.unpack_from(">fff", vtx_data, offset=offset))
                offset += struct.calcsize(">fff")
            if self.weights_en:
                weight_bytes = struct.unpack_from(">BBBBBBBB", vtx_data, offset=offset)
                vertex.weights = (
                    BoneWeight(bone=weight_bytes[4 + 0], weight=weight_bytes[0] / 255.0),
                    BoneWeight(bone=weight_bytes[4 + 1], weight=weight_bytes[1] / 255.0),
                    BoneWeight(bone=weight_bytes[4 + 2], weight=weight_bytes[2] / 255.0),
                    BoneWeight(bone=weight_bytes[4 + 3], weight=weight_bytes[3] / 255.0),
                )
                offset += struct.calcsize(">BBBBBBBB")
            if self.normal_en:
                vertex.normal = Vec4(*[((x / 255.0) * 2 - 1) for x in struct.unpack_from(">BBBB", vtx_data, offset=offset)])
                offset += struct.calcsize(">BBBB")
            if self.tangent_en:
                vertex.tangent = Vec4(*[((x / 255.0) * 2 - 1) for x in struct.unpack_from(">BBBB", vtx_data, offset=offset)])
                offset += struct.calcsize(">BBBB")
            if self.col0_en:
                vertex.col0 = Vec4(*[x / 255.0 for x in struct.unpack_from(">BBBB", vtx_data, offset=offset)])
                offset += struct.calcsize(">BBBB")
            if self.col1_en:
                vertex.col1 = Vec4(*[x / 255.0 for x in struct.unpack_from(">BBBB", vtx_data, offset=offset)])
                offset += struct.calcsize(">BBBB")
            if self.uv_en:
                if self.uv_elem_bytes == 2:
                    fmt = ">ee"
                elif self.uv_elem_bytes == 4:
                    fmt = ">ff"
                vertex.uv = struct.unpack_from(fmt, vtx_data, offset=offset)
                offset += struct.calcsize(fmt)

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
