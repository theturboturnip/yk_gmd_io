from dataclasses import dataclass
from typing import List, Tuple, Union, Type

import mathutils

from yk_gmd_blender.structurelib.base import BaseUnpacker
from yk_gmd_blender.yk_gmd.v2.structure.common.attribute import Attribute_Unpack, Attribute
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStr, ChecksumStr_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.common.file import FileData_Common, FilePacker
from yk_gmd_blender.yk_gmd.v2.structure.common.material_base import MaterialBase
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import Mesh_Unpack, Mesh
from yk_gmd_blender.yk_gmd.v2.structure.common.node import Node_Unpack, Node
from yk_gmd_blender.yk_gmd.v2.structure.yk1.bbox import BoundsData_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.header import GMDHeader_YK1_Unpack, UNK12_Unpack, UNK14_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.yk1.material import Material_YK1_Unpack, c_uint16
from yk_gmd_blender.yk_gmd.v2.structure.yk1.object import Object_YK1, Object_YK1_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.yk1.vertex_buffer_layout import VertexBufferLayout_YK1_Unpack, VertexBufferLayout_YK1


@dataclass(repr=False)
class FileData_YK1(FileData_Common):
    overall_bounds: BoundsData_YK1

    node_arr: List[Node]
    obj_arr: List[Object_YK1]
    mesh_arr: List[Mesh]
    attribute_arr: List[Attribute]
    material_arr: List[MaterialBase]
    matrix_arr: List[mathutils.Matrix]
    vertex_buffer_arr: List[VertexBufferLayout_YK1]
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
    finish: List[float]

    def __str__(self):
        s = "{\n"
        for f in self.header_fields_to_copy():
            s += f"\t{f} = {getattr(self, f)}\n"
        for f, _ in self.header_pointer_fields():
            s += f"\t{f} = array[{len(getattr(self, f))}]\n"
        s += "}"
        return s

    @classmethod
    def header_pointer_fields(cls) -> List[Tuple[str, Union[BaseUnpacker, Type[bytes]]]]:
        return FileData_Common.header_pointer_fields() + [
            ("node_arr", Node_Unpack),
            ("obj_arr", Object_YK1_Unpack),
            ("mesh_arr", Mesh_Unpack),
            ("attribute_arr", Attribute_Unpack),
            ("material_arr", Material_YK1_Unpack),
            ("matrix_arr", Mesh_Unpack),
            ("vertex_buffer_arr", VertexBufferLayout_YK1_Unpack),
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
            "finish"
        ]


FilePacker_YK1 = FilePacker(
    FileData_YK1,
    GMDHeader_YK1_Unpack
)