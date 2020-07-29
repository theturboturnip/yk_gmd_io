from dataclasses import dataclass

from yk_gmd_blender.structurelib.base import StructureUnpacker, FixedSizeArrayUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint16, c_int16, c_uint32, c_float32

from typing import List

from yk_gmd_blender.yk_gmd.legacy.abstract.material import GMDMaterialTextureIndex, GMDMaterial
from yk_gmd_blender.yk_gmd.legacy.abstract.vertices import GMDVertexBuffer
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStrStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import MeshStruct


@dataclass(frozen=True)
class TextureIndexStruct:
    tex_index: int
    padding: int = 0


TextureIndexStruct_Unpack = StructureUnpacker(
    TextureIndexStruct,
    fields=[
        ("padding", c_uint16),
        ("tex_index", c_int16)
    ]
)


@dataclass(frozen=True)
class AttributeStruct:
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

    texture_diffuse: TextureIndexStruct  # Usually has textures with _di postfix
    texture_refl: TextureIndexStruct  # Observed to have a cubemap texture for one eye-related material
    texture_multi: TextureIndexStruct
    # Never filled
    texture_unk1: TextureIndexStruct
    texture_ts: TextureIndexStruct # Only present in "rs" shaders
    texture_normal: TextureIndexStruct  # Usually has textures with _tn postfix
    texture_rt: TextureIndexStruct  # Usually has textures with _rt postfix
    texture_rd: TextureIndexStruct  # Usually has textures with _rd postfix

    extra_properties: List[float]  # Could be scale (x,y) pairs for the textures, although 0 is present a lot.

    padding: int = 0


AttributeStruct_Unpack = StructureUnpacker(
    AttributeStruct,
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

        ("texture_diffuse", TextureIndexStruct_Unpack),
        ("texture_refl_cubemap", TextureIndexStruct_Unpack),
        ("texture_multi", TextureIndexStruct_Unpack),
        ("texture_unk1", TextureIndexStruct_Unpack),
        ("texture_unk2", TextureIndexStruct_Unpack),
        ("texture_normal", TextureIndexStruct_Unpack),
        ("texture_rt", TextureIndexStruct_Unpack),
        ("texture_rd", TextureIndexStruct_Unpack),

        ("extra_properties", FixedSizeArrayUnpacker(c_float32, 16))
    ]
)