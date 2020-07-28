from dataclasses import dataclass
from typing import List, Tuple, Union, Type

import mathutils

from yk_gmd_blender.structurelib.base import BaseUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint16
from yk_gmd_blender.yk_gmd.v2.structure.common.attribute import Attribute_Unpack, Attribute
from yk_gmd_blender.yk_gmd.v2.structure.common.matrix import MatrixUnpacker
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.bbox import BoundsData_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStr_Unpack, ChecksumStr
from yk_gmd_blender.yk_gmd.v2.structure.common.file import FileData_Common, FilePacker
from yk_gmd_blender.yk_gmd.v2.structure.common.material_base import MaterialBase
from yk_gmd_blender.yk_gmd.v2.structure.common.node import Node_Unpack, Node
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.mesh import Mesh_Kenzan_Unpack, Mesh_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.object import Object_Kenzan_Unpack, Object_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.header import GMDHeader_Kenzan_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.material import Material_Kenzan_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.vertex_buffer_layout import VertexBufferLayout_Kenzan_Unpack, VertexBufferLayout_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.yk1.header import UNK14_Unpack, UNK12_Unpack


@dataclass(repr=False)
class FileData_Kenzan(FileData_Common):
    overall_bounds: BoundsData_Kenzan

    node_arr: List[Node]
    obj_arr: List[Object_Kenzan]
    mesh_arr: List[Mesh_Kenzan]
    attribute_arr: List[Attribute]
    material_arr: List[MaterialBase]
    matrix_arr: List[mathutils.Matrix]
    vertex_buffer_arr: List[VertexBufferLayout_Kenzan]
    vertex_data: bytes  # byte data
    texture_arr: List[ChecksumStr]
    shader_arr: List[ChecksumStr]
    node_name_arr: List[ChecksumStr]
    index_data: List[int]
    meshset_data: bytes
    mesh_matrix_bytestrings: bytes

    unk12: List[List[float]]
    unk13: List[int]  # Is sequence 00, 7C, 7D, 7E... 92 in Kiwami bob
    # # 0x7C = 124
    # # 0x92 = 146 => this is likely a bone address
    # # 24 elements in total
    unk14: List[List[int]]
    flags: List[int]

    @classmethod
    def header_pointer_fields(cls) -> List[Tuple[str, Union[BaseUnpacker, Type[bytes]]]]:
        return FileData_Common.header_pointer_fields() + [
            ("node_arr", Node_Unpack),
            ("obj_arr", Object_Kenzan_Unpack),
            ("mesh_arr", Mesh_Kenzan_Unpack),
            ("attribute_arr", Attribute_Unpack),
            ("material_arr", Material_Kenzan_Unpack),
            ("matrix_arr", MatrixUnpacker),
            ("vertex_buffer_arr", VertexBufferLayout_Kenzan_Unpack),
            ("vertex_data", bytes),
            ("texture_arr", ChecksumStr_Unpack),
            ("shader_arr", ChecksumStr_Unpack),
            ("node_name_arr", ChecksumStr_Unpack),
            ("index_data", c_uint16),
            ("meshset_data", bytes),
            ("mesh_matrix_bytestrings", bytes),
            ("unk12", UNK12_Unpack),
            ("unk13", c_uint16),
            ("unk14", UNK14_Unpack),
        ]

    @classmethod
    def header_fields_to_copy(cls) -> List[str]:
        return FileData_Common.header_fields_to_copy() + [
            "overall_bounds",
            "flags"
        ]

FilePacker_Kenzan = FilePacker(
    FileData_Kenzan,
    GMDHeader_Kenzan_Unpack
)