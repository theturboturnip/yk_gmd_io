from dataclasses import dataclass
from typing import List

from ....structurelib.base import StructureUnpacker, FixedSizeArrayUnpacker
from ....structurelib.primitives import c_uint16, c_int16, c_uint32, c_float32, Optional, c_uint64


@dataclass(frozen=True)
class TextureIndexStruct_Dragon:
    tex_index: int
    padding: int = 0


TextureIndexStruct_Dragon_Unpack = StructureUnpacker(
    TextureIndexStruct_Dragon,
    fields=[
        ("tex_index", c_int16),
        ("padding", c_uint16),
    ]
)


@dataclass(frozen=True)
class AttributeStruct_Dragon:
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

    texture_diffuse: TextureIndexStruct_Dragon  # Usually has textures with _di postfix
    texture_multi: TextureIndexStruct_Dragon
    texture_normal: TextureIndexStruct_Dragon  # Usually has textures with _tn postfix
    texture_rd: TextureIndexStruct_Dragon  # Usually has textures with _rd postfix
    # Never filled
    texture_rm: TextureIndexStruct_Dragon
    texture_rt: TextureIndexStruct_Dragon  # Usually has textures with _rt postfix
    texture_ts: TextureIndexStruct_Dragon  # Only present in "rs" shaders
    texture_refl: TextureIndexStruct_Dragon  # Observed to have a cubemap texture for one eye-related material

    extra_properties: List[float]  # Could be scale (x,y) pairs for the textures, although 0 is present a lot.

    unk1_always_1: int = 1
    unk2_always_0: int = 0
    unk3_always_0: int = 0

    @staticmethod
    def calculate_texture_count(texture_diffuse: Optional,
                                texture_multi: Optional,
                                texture_normal: Optional,
                                # Never filled
                                texture_rd: Optional,
                                texture_rm: Optional,
                                texture_rt: Optional,
                                texture_ts: Optional,
                                texture_refl: Optional,
                                ):
        count = 0
        if texture_diffuse:
            count = 1
        if texture_multi:
            count = 2
        if texture_normal:
            count = 3
        if texture_rd:
            count = 4
        if texture_rm:
            count = 5
        if texture_rt:
            count = 6
        if texture_ts:
            count = 7
        if texture_refl:
            count = 8
        return count


AttributeStruct_Dragon_Unpack = StructureUnpacker(
    AttributeStruct_Dragon,
    fields=[
        ("index", c_uint32),
        ("material_index", c_uint32),
        ("shader_index", c_uint32),
        ("mesh_indices_start", c_uint32),
        ("mesh_indices_count", c_uint32),
        ("texture_init_count", c_uint32),

        ("flags", c_uint64),

        ("texture_diffuse", TextureIndexStruct_Dragon_Unpack),
        ("texture_multi", TextureIndexStruct_Dragon_Unpack),
        ("texture_normal", TextureIndexStruct_Dragon_Unpack),
        ("texture_rd", TextureIndexStruct_Dragon_Unpack),
        ("texture_rm", TextureIndexStruct_Dragon_Unpack),
        ("texture_rt", TextureIndexStruct_Dragon_Unpack),
        ("texture_ts", TextureIndexStruct_Dragon_Unpack),
        ("texture_refl", TextureIndexStruct_Dragon_Unpack),

        # diffuse
        # multi
        # normal
        # rd
        # rm?
        # rt
        # ts
        # refl?

        ("extra_properties", FixedSizeArrayUnpacker(c_float32, 16))
    ]
)
