from dataclasses import dataclass
from typing import List, Tuple, Union, Type

import mathutils

from ....structurelib.base import BaseUnpacker
from ..common.checksum_str import ChecksumStrStruct, ChecksumStrStruct_Unpack
from ..common.file import FileData_Common, FilePacker
from ..common.matrix import MatrixUnpacker
from ..common.node import NodeStruct_Unpack, NodeStruct
from ..common.unks import Unk14Struct_Unpack, Unk12Struct_Unpack, Unk12Struct, \
    Unk14Struct
from .attribute import AttributeStruct_Dragon, AttributeStruct_Dragon_Unpack
from .header import GMDHeader_Dragon_Unpack
from ..yk1.bbox import BoundsDataStruct_YK1
from ..yk1.material import MaterialStruct_YK1_Unpack, c_uint16, MaterialStruct_YK1
from ..yk1.mesh import MeshStruct_YK1, MeshStruct_YK1_Unpack
from ..yk1.object import ObjectStruct_YK1, ObjectStruct_YK1_Unpack
from ..yk1.vertex_buffer_layout import VertexBufferLayoutStruct_YK1_Unpack, \
    VertexBufferLayoutStruct_YK1


@dataclass(repr=False)
class FileData_Dragon(FileData_Common):
    overall_bounds: BoundsDataStruct_YK1

    node_arr: List[NodeStruct]
    obj_arr: List[ObjectStruct_YK1]
    mesh_arr: List[MeshStruct_YK1]
    attribute_arr: List[AttributeStruct_Dragon]
    material_arr: List[MaterialStruct_YK1]
    matrix_arr: List[mathutils.Matrix]
    vertex_buffer_arr: List[VertexBufferLayoutStruct_YK1]
    vertex_data: bytes  # byte data
    texture_arr: List[ChecksumStrStruct]
    shader_arr: List[ChecksumStrStruct]
    node_name_arr: List[ChecksumStrStruct]
    index_data: List[int]
    object_drawlist_bytes: bytes
    mesh_matrixlist_bytes: bytes

    unk12: List[Unk12Struct]
    unk13: List[int]
    unk14: List[Unk14Struct]
    flags: List[int]

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
            ("node_arr", NodeStruct_Unpack),
            ("obj_arr", ObjectStruct_YK1_Unpack),
            ("mesh_arr", MeshStruct_YK1_Unpack),
            ("attribute_arr", AttributeStruct_Dragon_Unpack),
            ("material_arr", MaterialStruct_YK1_Unpack),
            ("matrix_arr", MatrixUnpacker),
            ("vertex_buffer_arr", VertexBufferLayoutStruct_YK1_Unpack),
            ("vertex_data", bytes),
            ("texture_arr", ChecksumStrStruct_Unpack),
            ("shader_arr", ChecksumStrStruct_Unpack),
            ("node_name_arr", ChecksumStrStruct_Unpack),
            ("index_data", c_uint16),
            ("object_drawlist_bytes", bytes),
            ("mesh_matrixlist_bytes", bytes),
            ("unk12", Unk12Struct_Unpack),
            ("unk13", c_uint16),
            ("unk14", Unk14Struct_Unpack),
        ]

    @classmethod
    def header_fields_to_copy(cls) -> List[str]:
        return FileData_Common.header_fields_to_copy() + [
            "overall_bounds",
            "flags"
        ]


FilePacker_Dragon = FilePacker(
    FileData_Dragon,
    GMDHeader_Dragon_Unpack
)
