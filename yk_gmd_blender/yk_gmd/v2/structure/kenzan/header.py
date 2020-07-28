from dataclasses import dataclass
from typing import List

import mathutils

from yk_gmd_blender.structurelib.base import StructureUnpacker, FixedSizeArrayUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint32
from yk_gmd_blender.yk_gmd.v2.structure.common.array_pointer import ArrayPointer, ArrayPointerUnpack
from yk_gmd_blender.yk_gmd.v2.structure.common.attribute import Attribute
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.bbox import BoundsData_Kenzan, BoundsData_Kenzan_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStr
from yk_gmd_blender.yk_gmd.v2.structure.common.header import GMDHeader, GMDHeaderUnpack
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import Mesh
from yk_gmd_blender.yk_gmd.v2.structure.common.node import Node
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.object import Object_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.common.sized_pointer import SizedPointer, SizedPointerUnpack
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.material import Material_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.vertex_buffer_layout import VertexBufferLayout_Kenzan


@dataclass(frozen=True)
class GMDHeader_Kenzan(GMDHeader):
    node_arr: ArrayPointer[Node]
    obj_arr: ArrayPointer[Object_Kenzan]
    mesh_arr: ArrayPointer[Mesh]
    attribute_arr: ArrayPointer[Attribute]
    material_arr: ArrayPointer[Material_Kenzan]
    matrix_arr: ArrayPointer[mathutils.Matrix]
    vertex_buffer_arr: ArrayPointer[VertexBufferLayout_Kenzan]
    vertex_data: SizedPointer  # byte data
    texture_arr: ArrayPointer[ChecksumStr]
    shader_arr: ArrayPointer[ChecksumStr]
    node_name_arr: ArrayPointer[ChecksumStr]
    index_data: ArrayPointer[int]
    meshset_data: SizedPointer
    mesh_matrix_bytestrings: SizedPointer

    overall_bounds: BoundsData_Kenzan

    unk12: ArrayPointer[List[float]]
    unk13: ArrayPointer[int]
    unk14: ArrayPointer[List[int]]
    flags: List[int]


GMDHeader_Kenzan_Unpack = StructureUnpacker(
    GMDHeader_Kenzan,
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

        ("overall_bounds", BoundsData_Kenzan_Unpack),

        ("unk12", ArrayPointerUnpack),
        ("unk13", ArrayPointerUnpack),
        ("unk14", ArrayPointerUnpack),
        ("flags", FixedSizeArrayUnpacker(c_uint32, 6)),
    ],
    base_class_unpackers={
        GMDHeader: GMDHeaderUnpack
    }
)