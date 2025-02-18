from dataclasses import dataclass
from typing import List

from ....structurelib.base import StructureUnpacker, FixedSizeArrayUnpacker
from ....structurelib.primitives import c_uint16, c_int16, c_uint32, c_float32


@dataclass(frozen=True)
class TextureIndexStruct:
    tex_index: int
    padding: int = 0


# NOTE - this struct order needs calibration for Kenzan. most files like tex_index, padding,
# but others like the other way around. Need a way to settle this
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
    mesh_indices_start: int
    mesh_indices_count: int

    # The number of texture slots to initialize == the largest index of a set texture
    texture_init_count: int
    # Observed to be 0x0000, 0x0001, 0x2001, 0x8001
    flags: int

    texture_diffuse: TextureIndexStruct  # Usually has textures with _di postfix
    texture_refl: TextureIndexStruct  # Observed to have a cubemap texture for one eye-related material
    texture_multi: TextureIndexStruct
    # Never filled
    texture_rm: TextureIndexStruct
    texture_ts: TextureIndexStruct  # Only present in "rs" shaders
    texture_normal: TextureIndexStruct  # Usually has textures with _tn postfix
    texture_rt: TextureIndexStruct  # Usually has textures with _rt postfix
    texture_rd: TextureIndexStruct  # Usually has textures with _rd postfix

    extra_properties: List[float]  # Could be scale (x,y) pairs for the textures, although 0 is present a lot.

    unk1_always_1: int = 1
    unk2_always_0: int = 0
    unk3_always_0: int = 0


AttributeStruct_Unpack = StructureUnpacker(
    AttributeStruct,
    fields=[
        ("index", c_uint32),
        ("material_index", c_uint32),
        ("shader_index", c_uint32),
        ("mesh_indices_start", c_uint32),
        ("mesh_indices_count", c_uint32),
        ("texture_init_count", c_uint32),

        ("unk1_always_1", c_uint16),
        ("unk2_always_0", c_uint16),
        ("flags", c_uint16),
        ("unk3_always_0", c_uint16),  # This may be part of the flags block, and just unused in Kiwami

        ("texture_diffuse", TextureIndexStruct_Unpack),
        ("texture_refl", TextureIndexStruct_Unpack),
        ("texture_multi", TextureIndexStruct_Unpack),
        ("texture_rm", TextureIndexStruct_Unpack),
        ("texture_ts", TextureIndexStruct_Unpack),
        ("texture_normal", TextureIndexStruct_Unpack),
        ("texture_rt", TextureIndexStruct_Unpack),
        ("texture_rd", TextureIndexStruct_Unpack),

        ("extra_properties", FixedSizeArrayUnpacker(c_float32, 16))
    ]
)
