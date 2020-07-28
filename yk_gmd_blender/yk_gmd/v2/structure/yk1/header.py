from dataclasses import dataclass
from typing import List

import mathutils

from yk_gmd_blender.structurelib.base import FixedSizeArrayUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint32, c_float32
from yk_gmd_blender.yk_gmd.v2.structure.common.array_pointer import ArrayPointerStruct, ArrayPointerStruct_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.common.attributestruct import AttributeStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStrStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.header import GMDHeaderStruct, StructureUnpacker, GMDHeaderStruct_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import MeshStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeStruct
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.object import ObjectStruct_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.common.sized_pointer import SizedPointerStruct_Unpack, SizedPointerStruct
from yk_gmd_blender.yk_gmd.v2.structure.yk1.bbox import BoundsDataStruct_YK1, BoundsData_YK1_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.yk1.material import MaterialStruct_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.vertex_buffer_layout import VertexBufferLayoutStruct_YK1


UNK12_Unpack = FixedSizeArrayUnpacker(c_float32, 32)
UNK14_Unpack = FixedSizeArrayUnpacker(c_uint32, 32)

@dataclass(frozen=True)
class GMDHeader_YK1(GMDHeaderStruct):
    node_arr: ArrayPointerStruct[NodeStruct]
    obj_arr: ArrayPointerStruct[ObjectStruct_Kenzan]
    mesh_arr: ArrayPointerStruct[MeshStruct]
    attribute_arr: ArrayPointerStruct[AttributeStruct]
    material_arr: ArrayPointerStruct[MaterialStruct_YK1]
    matrix_arr: ArrayPointerStruct[mathutils.Matrix]
    vertex_buffer_arr: ArrayPointerStruct[VertexBufferLayoutStruct_YK1]
    vertex_data: SizedPointerStruct  # byte data
    texture_arr: ArrayPointerStruct[ChecksumStrStruct]
    shader_arr: ArrayPointerStruct[ChecksumStrStruct]
    node_name_arr: ArrayPointerStruct[ChecksumStrStruct]
    index_data: ArrayPointerStruct[int]
    meshset_data: SizedPointerStruct
    mesh_matrix_bytestrings: SizedPointerStruct

    overall_bounds: BoundsDataStruct_YK1

    unk12: ArrayPointerStruct[List[float]]
    unk13: ArrayPointerStruct[int]  # Is sequence 00, 7C, 7D, 7E... 92 in Kiwami bob
    # # 0x7C = 124
    # # 0x92 = 146 => this is likely a bone address
    # # 24 elements in total
    unk14: ArrayPointerStruct[List[int]]
    flags: List[int]


GMDHeader_YK1_Unpack = StructureUnpacker(
    GMDHeader_YK1,
    fields=[
        ("node_arr", ArrayPointerStruct_Unpack),
        ("obj_arr", ArrayPointerStruct_Unpack),
        ("mesh_arr", ArrayPointerStruct_Unpack),
        ("attribute_arr", ArrayPointerStruct_Unpack),
        ("material_arr", ArrayPointerStruct_Unpack),
        ("matrix_arr", ArrayPointerStruct_Unpack),

        ("vertex_buffer_arr", ArrayPointerStruct_Unpack),
        ("vertex_data", SizedPointerStruct_Unpack),

        ("texture_arr", ArrayPointerStruct_Unpack),
        ("shader_arr", ArrayPointerStruct_Unpack),
        ("node_name_arr", ArrayPointerStruct_Unpack),

        ("index_data", ArrayPointerStruct_Unpack),
        ("meshset_data", SizedPointerStruct_Unpack),
        ("mesh_matrix_bytestrings", SizedPointerStruct_Unpack),

        ("overall_bounds", BoundsData_YK1_Unpack),

        ("unk12", ArrayPointerStruct_Unpack),
        ("unk13", ArrayPointerStruct_Unpack),
        ("unk14", ArrayPointerStruct_Unpack),
        ("flags", FixedSizeArrayUnpacker(c_uint32, 6)),
    ],
    base_class_unpackers={
        GMDHeaderStruct: GMDHeaderStruct_Unpack
    }
)