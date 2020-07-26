from dataclasses import dataclass
from typing import List

import mathutils

from yk_gmd_blender.structurelib.base import FixedSizeArrayUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint32, c_float32
from yk_gmd_blender.yk_gmd.v2.structure.common.array_pointer import ArrayPointer, ArrayPointerUnpack
from yk_gmd_blender.yk_gmd.v2.structure.common.attribute import Attribute
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStr
from yk_gmd_blender.yk_gmd.v2.structure.common.header import GMDHeader, StructureUnpacker, GMDHeaderUnpack
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import Mesh
from yk_gmd_blender.yk_gmd.v2.structure.common.node import Node
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.object import Object_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.common.sized_pointer import SizedPointerUnpack, SizedPointer
from yk_gmd_blender.yk_gmd.v2.structure.yk1.bbox import BoundsData_YK1, BoundsData_YK1_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.yk1.material import Material_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.vertex_buffer_layout import VertexBufferLayout_YK1


UNK12_Unpack = FixedSizeArrayUnpacker(c_float32, 32)
UNK14_Unpack = FixedSizeArrayUnpacker(c_uint32, 32)

@dataclass(frozen=True)
class GMDHeader_YK1(GMDHeader):
    node_arr: ArrayPointer[Node]
    obj_arr: ArrayPointer[Object_Kenzan]
    mesh_arr: ArrayPointer[Mesh]
    attribute_arr: ArrayPointer[Attribute]
    material_arr: ArrayPointer[Material_YK1]
    matrix_arr: ArrayPointer[mathutils.Matrix]
    vertex_buffer_arr: ArrayPointer[VertexBufferLayout_YK1]
    vertex_data: SizedPointer  # byte data
    texture_arr: ArrayPointer[ChecksumStr]
    shader_arr: ArrayPointer[ChecksumStr]
    node_name_arr: ArrayPointer[ChecksumStr]
    index_data: ArrayPointer[int]
    meshset_data: SizedPointer
    mesh_matrix_bytestrings: SizedPointer

    overall_bounds: BoundsData_YK1

    unk12: ArrayPointer[List[float]]
    unk13: ArrayPointer[int]  # Is sequence 00, 7C, 7D, 7E... 92 in Kiwami bob
    # # 0x7C = 124
    # # 0x92 = 146 => this is likely a bone address
    # # 24 elements in total
    unk14: ArrayPointer[List[int]]
    finish: List[float]


GMDHeader_YK1_Unpack = StructureUnpacker(
    GMDHeader_YK1,
    fields=[
        ("node_arr", ArrayPointerUnpack),
        ("obj_arr", ArrayPointerUnpack),
        ("mesh_arr", ArrayPointerUnpack),
        ("attribute_arr", ArrayPointerUnpack),
        ("material_arr", ArrayPointerUnpack),
        ("matrix_arr", ArrayPointerUnpack),

        ("vertex_buffer_arr", ArrayPointerUnpack),
        ("vertex_data", SizedPointerUnpack),

        ("texture_arr", ArrayPointerUnpack),
        ("shader_arr", ArrayPointerUnpack),
        ("node_name_arr", ArrayPointerUnpack),

        ("index_data", ArrayPointerUnpack),
        ("meshset_data", SizedPointerUnpack),
        ("mesh_matrix_bytestrings", SizedPointerUnpack),

        ("overall_bounds", BoundsData_YK1_Unpack),

        ("unk12", ArrayPointerUnpack),
        ("unk13", ArrayPointerUnpack),
        ("unk14", ArrayPointerUnpack),
        ("finish", FixedSizeArrayUnpacker(c_float32, 6)),
    ],
    base_class_unpackers={
        GMDHeader: GMDHeaderUnpack
    }
)