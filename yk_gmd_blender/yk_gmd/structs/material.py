from ctypes import *
from ._base.base_structure import BaseBigEndianStructure


class PaddedTextureIndexStruct(BaseBigEndianStructure):
    _fields_ = [
        ("zero", c_uint16),
        ("tex_index", c_int16), # These are signed, as -1 is a sentinel value
    ]

    def __init__(self, tex_index):
        self.zero = 0
        self.tex_index = tex_index


class MaterialStruct(BaseBigEndianStructure):
    _fields_ = [
        ("id", c_uint32),
        ("unk1", c_uint32), # index in unk5?
        ("shader_index", c_uint32),
        ("first_connected_submesh", c_uint32), # index in unk13?
        ("num_connected_submeshes", c_uint32),
        ("unk4", c_uint32),

        ("unk5", c_uint16),
        ("unk6", c_uint16),
        ("flags", c_uint16),
        ("zero1", c_uint16), # This may be part of the flags block - it may be other flags left unused in Kiwami

        ("texture_diffuse", PaddedTextureIndexStruct), # Usually has textures with _di postfix
        ("texture_cubemap_maybe", PaddedTextureIndexStruct), # Observed to have a cubemap texture for one eye-related material
        ("texture_multi", PaddedTextureIndexStruct),
        ("texture_unk1", PaddedTextureIndexStruct),
        ("texture_unk2", PaddedTextureIndexStruct),
        ("texture_normal", PaddedTextureIndexStruct), # Usually has textures with _tn postfix
        ("texture_rt", PaddedTextureIndexStruct), # Usually has textures with _rt postfix
        ("texture_rd", PaddedTextureIndexStruct), # Usually has textures with _rd postfix

        #("zero2", c_uint8 * 16),

        ("fragment_properties", c_float * 16) # Could be scale (x,y) pairs for the textures, although 0 is present a lot.
    ]