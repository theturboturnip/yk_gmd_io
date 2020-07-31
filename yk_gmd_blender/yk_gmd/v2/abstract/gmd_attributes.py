import abc
from dataclasses import dataclass
from typing import List, Optional, Union

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDShader
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.material import MaterialStruct_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.version import GMDVersion
from yk_gmd_blender.yk_gmd.v2.structure.yk1.material import MaterialStruct_YK1

@dataclass(frozen=True)
class GMDVersionRestricted(abc.ABC):
    origin_version: GMDVersion

    def port_to_version(self, new_version: GMDVersion):
        raise NotImplementedError()


# TODO: Implement port_to_version
@dataclass(frozen=True)
class GMDMaterial(GMDVersionRestricted):
    """
    This consists of 64 bytes of data, and is not transferrable between engines.
    """
    origin_data: Union[MaterialStruct_YK1, MaterialStruct_Kenzan]


# TODO: Implement port_to_version
@dataclass(frozen=True)
class GMDUnk12(GMDVersionRestricted):
    """
    This consists of 16 floats, which may or may not be transferrable between engines
    We don't know how to edit them, so they are frozen.
    """
    float_data: List[float]

    @staticmethod
    def get_default() -> List[float]:
        pass


# TODO: Implement port_to_version
@dataclass(frozen=True)
class GMDUnk14(GMDVersionRestricted):
    """
    This consists of 16 uint32, which may or may not be transferrable between engines. They are mostly 0 in Kiwami 1 KiwamiBob.
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
    texture_unk1: Optional[str]
    texture_rs: Optional[str]
    texture_normal: Optional[str]
    texture_rt: Optional[str]
    texture_rd: Optional[str]

    material: GMDMaterial
    unk12: Optional[GMDUnk12]
    unk14: Optional[GMDUnk14]
    attr_extra_properties: List[float]
    attr_flags: int