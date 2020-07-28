from dataclasses import dataclass

from yk_gmd_blender.structurelib.base import StructureUnpacker, FixedSizeArrayUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint16, c_int16, c_uint32, c_float32

from typing import List

from yk_gmd_blender.yk_gmd.abstract.material import GMDMaterialTextureIndex, GMDMaterial
from yk_gmd_blender.yk_gmd.abstract.vertices import GMDVertexBuffer
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStr
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import Mesh


@dataclass(frozen=True)
class TextureIndex_YK1:
    tex_index: int
    padding: int = 0


TextureIndex_YK1_Unpack = StructureUnpacker(
    TextureIndex_YK1,
    fields=[
        ("padding", c_uint16),
        ("tex_index", c_int16)
    ]
)


@dataclass(frozen=True)
class Attribute:
    index: int
    material_index: int
    shader_index: int

    # Which meshes use this material - offsets in the Mesh_YK1 array
    meshset_start: int
    meshset_count: int

    # Always one of {6,7,8} for kiwami bob
    unk1: int
    # Always 0x00_01_00_00
    unk2: int
    # Observed to be 0x0000, 0x0001, 0x2001, 0x8001
    flags: int

    texture_diffuse: TextureIndex_YK1  # Usually has textures with _di postfix
    texture_refl_cubemap: TextureIndex_YK1  # Observed to have a cubemap texture for one eye-related material
    texture_multi: TextureIndex_YK1
    # Never filled
    texture_unk1: TextureIndex_YK1
    texture_unk2: TextureIndex_YK1
    texture_normal: TextureIndex_YK1  # Usually has textures with _tn postfix
    texture_rt: TextureIndex_YK1  # Usually has textures with _rt postfix
    texture_rd: TextureIndex_YK1  # Usually has textures with _rd postfix

    extra_properties: List[float]  # Could be scale (x,y) pairs for the textures, although 0 is present a lot.

    padding: int = 0


Attribute_Unpack = StructureUnpacker(
    Attribute,
    fields=[
        ("index", c_uint32),
        ("material_index", c_uint32),
        ("shader_index", c_uint32),
        ("meshset_start", c_uint32),
        ("meshset_count", c_uint32),
        ("unk1", c_uint32),
        ("unk2", c_uint32),

        ("flags", c_uint16),
        ("padding", c_uint16),  # This may be part of the flags block - it may be other flags left unused in Kiwami

        ("texture_diffuse", TextureIndex_YK1_Unpack),
        ("texture_refl_cubemap", TextureIndex_YK1_Unpack),
        ("texture_multi", TextureIndex_YK1_Unpack),
        ("texture_unk1", TextureIndex_YK1_Unpack),
        ("texture_unk2", TextureIndex_YK1_Unpack),
        ("texture_normal", TextureIndex_YK1_Unpack),
        ("texture_rt", TextureIndex_YK1_Unpack),
        ("texture_rd", TextureIndex_YK1_Unpack),

        ("extra_properties", FixedSizeArrayUnpacker(c_float32, 16))
    ]
)