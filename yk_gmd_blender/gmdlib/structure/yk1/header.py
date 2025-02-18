from dataclasses import dataclass
from typing import List

import mathutils

from ....structurelib.base import FixedSizeArrayUnpacker
from ....structurelib.primitives import c_uint32
from ..common.array_pointer import ArrayPointerStruct, ArrayPointerStruct_Unpack
from ..common.attribute import AttributeStruct
from ..common.checksum_str import ChecksumStrStruct
from ..common.header import GMDHeaderStruct, StructureUnpacker, GMDHeaderStruct_Unpack
from ..common.mesh import MeshStruct
from ..common.node import NodeStruct
from ..common.sized_pointer import SizedPointerStruct_Unpack, SizedPointerStruct
from ..common.unks import Unk12Struct, Unk14Struct
from ..kenzan.object import ObjectStruct_Kenzan
from .bbox import BoundsDataStruct_YK1, BoundsData_YK1_Unpack
from .material import MaterialStruct_YK1
from .vertex_buffer_layout import VertexBufferLayoutStruct_YK1


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
    object_drawlist_bytes: SizedPointerStruct
    mesh_matrixlist_bytes: SizedPointerStruct

    overall_bounds: BoundsDataStruct_YK1

    unk12: ArrayPointerStruct[Unk12Struct]  # Material properties
    unk13: ArrayPointerStruct[int]  # List of root node indices - those without parents
    unk14: ArrayPointerStruct[Unk14Struct]  # Material properties
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
        ("object_drawlist_bytes", SizedPointerStruct_Unpack),
        ("mesh_matrixlist_bytes", SizedPointerStruct_Unpack),

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
