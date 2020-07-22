from ctypes import *

from yk_gmd_blender.yk_gmd.structs.transform_12float import Transform12Float
from .varlen_data_array_ptr import VarLenDataArrayPtrStruct
from .array_pointer import array_pointer_of
from ._base.base_structure import BaseBigEndianStructure
from .id_string import IdStringStruct
from ._base.text import ascii_text
from .bone import BoneStruct
from .material import MaterialStruct
from .matrix import MatrixStruct
from .part import PartStruct
from .submesh import SubmeshStruct
from .unks import Unk12, Unk14, Unk5, Unk13
from .vertex_buffer_layout import VertexBufferLayoutStruct


#class HeaderFileSizeStruct(BaseBigEndianStructure):
#    _fields_ = [
#        ("file_size", c_uint32)
#    ]


class HeaderStruct(BaseBigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("magic_str", ascii_text(4)),
        ("endian_check", c_uint32),
        ("version_flags_maybe", c_uint32),
        ("file_size", c_uint32),

        ("name_checksum", c_uint16),
        ("name", ascii_text(30)),

        ("bones", array_pointer_of(BoneStruct)), # TODO: Rename to HierarchyStruct or something
        ("parts", array_pointer_of(PartStruct)),
        ("submeshes", array_pointer_of(SubmeshStruct)),
        ("materials", array_pointer_of(MaterialStruct)),
        ("unk5", array_pointer_of(Unk5)), # Probably Material
        ("matrices", array_pointer_of(MatrixStruct)),
        ("vertex_buffer_layouts", array_pointer_of(VertexBufferLayoutStruct)),
        ("vertex_data", array_pointer_of(c_uint8)),
        ("texture_names", array_pointer_of(IdStringStruct)),
        ("shader_names", array_pointer_of(IdStringStruct)),
        ("bone_names", array_pointer_of(IdStringStruct)),
        ("index_data", array_pointer_of(c_uint16)),
        ("unk10", array_pointer_of(c_uint8)),
        ("submesh_bone_lists", VarLenDataArrayPtrStruct),

        ("overall_bbox", Transform12Float),
        ("unk12", array_pointer_of(Unk12)),
        ("unk13", array_pointer_of(Unk13)), # Is sequence 00, 7C, 7D, 7E... 92 in Kiwami bob
        # 0x7C = 124
        # 0x92 = 146 => this is likely a bone address
        # 24 elements in total
        ("unk14", array_pointer_of(Unk14)),
        ("finish", c_float * 6)
    ]

    def set_field(self, name: str, data):
        field_names = [x[0] for x in self._fields_]
        if name not in field_names:
            raise AttributeError()
        setattr(self, name, data)
