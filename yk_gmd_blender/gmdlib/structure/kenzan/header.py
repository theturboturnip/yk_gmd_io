from dataclasses import dataclass
from typing import List

import mathutils

from ....structurelib.base import StructureUnpacker, FixedSizeArrayUnpacker
from ....structurelib.primitives import c_uint32
from ..common.array_pointer import ArrayPointerStruct, ArrayPointerStruct_Unpack
from ..common.attribute import AttributeStruct
from ..common.checksum_str import ChecksumStrStruct
from ..common.header import GMDHeaderStruct, GMDHeaderStruct_Unpack
from ..common.mesh import MeshStruct
from ..common.node import NodeStruct
from ..common.sized_pointer import SizedPointerStruct, SizedPointerStruct_Unpack
from ..common.unks import Unk12Struct, Unk14Struct
from .bbox import BoundsDataStruct_Kenzan, BoundsDataStruct_Kenzan_Unpack
from .material import MaterialStruct_Kenzan
from .object import ObjectStruct_Kenzan
from .vertex_buffer_layout import VertexBufferLayoutStruct_Kenzan


@dataclass(frozen=True)
class GMDHeader_Kenzan(GMDHeaderStruct):
    node_arr: ArrayPointerStruct[NodeStruct]
    obj_arr: ArrayPointerStruct[ObjectStruct_Kenzan]
    mesh_arr: ArrayPointerStruct[MeshStruct]
    attribute_arr: ArrayPointerStruct[AttributeStruct]
    material_arr: ArrayPointerStruct[MaterialStruct_Kenzan]
    matrix_arr: ArrayPointerStruct[mathutils.Matrix]
    vertex_buffer_arr: ArrayPointerStruct[VertexBufferLayoutStruct_Kenzan]
    vertex_data: SizedPointerStruct  # byte data
    texture_arr: ArrayPointerStruct[ChecksumStrStruct]
    shader_arr: ArrayPointerStruct[ChecksumStrStruct]
    node_name_arr: ArrayPointerStruct[ChecksumStrStruct]
    index_data: ArrayPointerStruct[int]
    object_drawlist_bytes: SizedPointerStruct
    mesh_matrixlist_bytes: SizedPointerStruct

    overall_bounds: BoundsDataStruct_Kenzan

    unk12: ArrayPointerStruct[Unk12Struct]
    unk13: ArrayPointerStruct[int]
    unk14: ArrayPointerStruct[Unk14Struct]
    flags: List[int]


GMDHeader_Kenzan_Unpack = StructureUnpacker(
    GMDHeader_Kenzan,
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

        ("overall_bounds", BoundsDataStruct_Kenzan_Unpack),

        ("unk12", ArrayPointerStruct_Unpack),
        ("unk13", ArrayPointerStruct_Unpack),
        ("unk14", ArrayPointerStruct_Unpack),
        ("flags", FixedSizeArrayUnpacker(c_uint32, 6)),
    ],
    base_class_unpackers={
        GMDHeaderStruct: GMDHeaderStruct_Unpack
    }
)
