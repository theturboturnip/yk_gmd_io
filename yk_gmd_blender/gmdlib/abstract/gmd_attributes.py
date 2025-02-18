import abc
from dataclasses import dataclass
from typing import List, Optional, Union, TypeVar

from .gmd_shader import GMDShader
from ..structure.kenzan.material import MaterialStruct_Kenzan
from ..structure.version import GMDVersion
from ..structure.yk1.material import MaterialStruct_YK1

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
    origin_data: Union[MaterialStruct_YK1, MaterialStruct_Kenzan]

    @staticmethod
    def target_struct_type(version: GMDVersion):
        if version in [GMDVersion.Kiwami1, GMDVersion.Dragon]:
            return MaterialStruct_YK1
        else:
            return MaterialStruct_Kenzan

    def port_to_version(self, new_version: GMDVersion) -> 'GMDMaterial':
        if self.target_struct_type(new_version) == self.target_struct_type(self.origin_version):
            return self
        if isinstance(self.origin_data, MaterialStruct_YK1) and new_version == GMDVersion.Kenzan:
            return GMDMaterial(
                origin_version=new_version,
                origin_data=MaterialStruct_Kenzan(
                    diffuse=self.origin_data.diffuse,
                    opacity=self.origin_data.opacity,
                    specular=self.origin_data.specular,
                    ambient=[0, 0, 0, 0],
                    emissive=0,
                    power=1,
                    intensity=1,

                    padding=0,
                )
            )
        elif isinstance(self.origin_data, MaterialStruct_Kenzan) and new_version in [GMDVersion.Kiwami1,
                                                                                     GMDVersion.Dragon]:
            return GMDMaterial(
                origin_version=new_version,
                origin_data=MaterialStruct_YK1(
                    diffuse=self.origin_data.diffuse,
                    opacity=int(self.origin_data.opacity * 255),
                    specular=self.origin_data.specular,
                    power=self.origin_data.power,
                    unk1=[0, 0],
                    unk2=[0, 0, 0, 0],
                )
            )


# TODO: Implement port_to_version properly?
@dataclass(frozen=True)
class GMDUnk12:
    """
    This consists of 16 floats, which may or may not be transferrable between engines
    We don't know how to edit them, so they are frozen.
    """
    float_data: List[float]

    @staticmethod
    def get_default() -> List[float]:
        pass

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
    This consists of 16 uint32, which may or may not be transferrable between engines.
    They are mostly 0 in Kiwami 1 KiwamiBob.
    We don't know how to edit them, so they are frozen.
    """
    int_data: List[int]

    @staticmethod
    def get_default() -> List[int]:
        pass


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
    unk12: Optional[GMDUnk12]
    unk14: Optional[GMDUnk14]
    attr_extra_properties: List[float]
    attr_flags: int
