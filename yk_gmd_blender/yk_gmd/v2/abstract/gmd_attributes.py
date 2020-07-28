import abc
from dataclasses import dataclass
from typing import List

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDShader
from yk_gmd_blender.yk_gmd.v2.structure.version import GMDVersion


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
    origin_data: List[int]


# TODO: Implement port_to_version
@dataclass(frozen=True)
class GMDUnk12(GMDVersionRestricted):
    """
    This consists of 16 floats, which may or may not be transferrable between engines
    We don't know how to edit them, so they are frozen.
    """
    float_data: List[float]


# TODO: Implement port_to_version
@dataclass(frozen=True)
class GMDUnk14(GMDVersionRestricted):
    """
    This consists of 16 uint32, which may or may not be transferrable between engines. They are mostly 0 in Kiwami 1 KiwamiBob.
    We don't know how to edit them, so they are frozen.
    """
    float_data: List[int]


@dataclass
class GMDAttributes:
    shader: GMDShader

    texture_diffuse: str
    texture_refl: str
    texture_multi: str
    texture_rs: str
    texture_tn: str
    texture_rt: str
    texture_rd: str

    material: GMDMaterial
    unk12: GMDUnk12
    unk14: GMDUnk14