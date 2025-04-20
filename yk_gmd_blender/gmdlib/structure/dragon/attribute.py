from dataclasses import dataclass

from ..common.attribute import AttributeStruct, TextureIndexStruct
from ....structurelib.base import StructureUnpacker, FixedSizeArrayUnpacker
from ....structurelib.primitives import c_uint16, c_int16, c_uint32, c_float32, Optional, c_uint64

TextureIndexStruct_Dragon_Unpack = StructureUnpacker(
    TextureIndexStruct,
    fields=[
        ("tex_index", c_int16),
        ("padding", c_uint16),
    ]
)


@dataclass(frozen=True)
class AttributeStruct_Dragon(AttributeStruct):
    @staticmethod
    def calculate_texture_count(texture_diffuse: Optional[str],
                                texture_multi: Optional[str],
                                texture_normal: Optional[str],
                                # Never filled
                                texture_rd: Optional[str],
                                texture_rm: Optional[str],
                                texture_rt: Optional[str],
                                texture_ts: Optional[str],
                                texture_refl: Optional[str],
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
