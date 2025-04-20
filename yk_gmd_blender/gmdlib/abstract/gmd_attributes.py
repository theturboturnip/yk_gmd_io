import abc
from dataclasses import dataclass
from typing import List, Optional, Union, TypeVar, overload, Literal

from .gmd_shader import GMDShader
from ..structure.kenzan.material import MaterialStruct_Kenzan
from ..structure.version import GMDVersion
from ..structure.y3.material import MaterialStruct_Y3

T = TypeVar('T')


@dataclass(frozen=True)
class GMDVersionRestricted(abc.ABC):
    origin_version: GMDVersion

    def port_to_version(self: T, new_version: GMDVersion) -> T:
        raise NotImplementedError()


# TODO: Implement port_to_version properly?
@dataclass(frozen=True)
class GMDMaterial(GMDVersionRestricted):
    """
    This consists of 64 bytes of data, and is not transferrable between engines.
    """
    origin_data: Union[MaterialStruct_Y3, MaterialStruct_Kenzan]

    @staticmethod
    def target_struct_type(version: GMDVersion):
        if version == GMDVersion.Kenzan:
            return MaterialStruct_Kenzan
        else:
            return MaterialStruct_Y3

    @overload
    def origin_data_as_version(self, new_version: Literal[GMDVersion.Kenzan]) -> MaterialStruct_Kenzan:
        ...

    @overload
    def origin_data_as_version(
            self,
            new_version: Literal[GMDVersion.Yakuza3, GMDVersion.Kiwami1, GMDVersion.Dragon],
    ) -> MaterialStruct_Y3:
        ...

    @overload
    def origin_data_as_version(
            self,
            new_version: GMDVersion,
    ) -> Union[MaterialStruct_Y3, MaterialStruct_Kenzan]:
        ...

    def origin_data_as_version(self, new_version: GMDVersion) -> Union[MaterialStruct_Y3, MaterialStruct_Kenzan]:
        # There are exactly two permutations of MaterialStruct: MaterialStruct_Kenzan and MaterialStruct_Y3.
        # MaterialStruct_Kenzan is only used for GMDVersion.Kenzan
        if isinstance(self.origin_data, MaterialStruct_Y3) and new_version == GMDVersion.Kenzan:
            return MaterialStruct_Kenzan(
                diffuse=self.origin_data.diffuse,
                opacity=self.origin_data.opacity,
                specular=self.origin_data.specular,
                ambient=[0, 0, 0, 0],
                emissive=0,
                power=1,
                intensity=1,

                padding=0,
            )
        elif isinstance(self.origin_data, MaterialStruct_Kenzan) and new_version != GMDVersion.Kenzan:
            return MaterialStruct_Y3(
                diffuse=self.origin_data.diffuse,
                opacity=int(self.origin_data.opacity * 255),
                specular=self.origin_data.specular,
                power=self.origin_data.power,
                unk1=[0, 0],
                unk2=[0, 0, 0, 0],
            )
        else:
            return self.origin_data

    def port_to_version(self, new_version: GMDVersion) -> 'GMDMaterial':
        return GMDMaterial(
            origin_version=new_version,
            origin_data=self.origin_data_as_version(new_version)
        )


# TODO: Implement port_to_version properly?
@dataclass(frozen=True)
class GMDUnk12:
    """
    This consists of 32 floats, which may or may not be transferrable between engines
    We don't know how to edit them, so they are frozen.
    """
    float_data: List[float]

    # def port_to_version(self, new_version: GMDVersion):
    #     if new_version == self.origin_version:
    #         return self
    #     return GMDUnk12(
    #         origin_version=new_version,
    #         float_data=self.float_data
    #     )


# TODO: Implement port_to_version properly?
@dataclass(frozen=True)
class GMDUnk14:
    """
    This consists of 32 uint32, which may or may not be transferrable between engines.
    They are mostly 0 in Kiwami 1 KiwamiBob.
    We don't know how to edit them, so they are frozen.
    """
    int_data: List[int]


@dataclass
class GMDAttributeSet:
    shader: GMDShader

    texture_diffuse: Optional[str]
    texture_refl: Optional[str]
    texture_multi: Optional[str]
    texture_rm: Optional[str]
    texture_rs: Optional[str]
    texture_normal: Optional[str]
    texture_rt: Optional[str]
    texture_rd: Optional[str]

    material: GMDMaterial
    unk12: GMDUnk12
    unk14: GMDUnk14
    attr_extra_properties: List[float]
    attr_flags: int
