from dataclasses import dataclass
from pathlib import Path
from typing import Union, Tuple, cast

from yk_gmd_blender.yk_gmd.abstract.scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.structure.common.file import FileData_Common


#@dataclass
#class ParsedScene:
#    scene: GMDScene
#    big_endian: bool
from yk_gmd_blender.yk_gmd.v2.structure.common.header import GMDHeaderUnpack, GMDHeader
from yk_gmd_blender.yk_gmd.v2.structure.endianness import check_is_file_big_endian
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.abstractor import convert_Kenzan_to_legacy_abstraction
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.file import FilePacker_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.version import GMDVersion
from yk_gmd_blender.yk_gmd.v2.structure.yk1.abstractor import convert_YK1_to_legacy_abstraction, \
    package_legacy_abstraction_to_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.file import FilePacker_YK1, FileData_YK1


def _get_file_data(data: Union[Path, str, bytes]) -> bytes:
    if isinstance(data, (Path, str)):
        with open(data, "rb") as in_file:
            data = in_file.read()
        return data
    else:
        return data


def _extract_base_header(data: bytes) -> Tuple[bool, GMDHeader]:
    big_endian = True
    base_header, _ = GMDHeaderUnpack.unpack(big_endian, data=data, offset=0)
    big_endian = check_is_file_big_endian(base_header.file_endian_check)
    # Reimport the header with the correct endianness
    base_header, _ = GMDHeaderUnpack.unpack(big_endian, data=data, offset=0)
    return big_endian, base_header


def can_read_from(data: Union[Path, str, bytes]) -> Tuple[bool, GMDHeader]:
    big_endian, base_header = _extract_base_header(_get_file_data(data))

    if base_header.get_version_properties().major_version in [GMDVersion.Kiwami1, GMDVersion.Kenzan]:
        return True, base_header
    return False, base_header


def read_to_legacy(data: Union[Path, str, bytes]) -> Tuple[FileData_Common, GMDScene]:
    data = _get_file_data(data)
    big_endian, base_header = _extract_base_header(data)

    version_props = base_header.get_version_properties()
    if version_props.major_version == GMDVersion.Kiwami1:
        contents, _ = FilePacker_YK1.unpack(big_endian, data=data, offset=0)
        scene = convert_YK1_to_legacy_abstraction(contents, version_props)

        return contents, scene
    elif version_props.major_version == GMDVersion.Kenzan:
        contents, _ = FilePacker_Kenzan.unpack(big_endian, data=data, offset=0)
        scene = convert_Kenzan_to_legacy_abstraction(contents, version_props)

        return contents, scene
    else:
        raise Exception(f"File format version {version_props.version_str} is unreadable")


def can_write_over(data: Union[Path, str, bytes]) -> Tuple[bool, GMDHeader]:
    big_endian, base_header = _extract_base_header(_get_file_data(data))

    if base_header.get_version_properties().major_version in [GMDVersion.Kiwami1, GMDVersion.Kenzan]:
        return True, base_header
    return False, base_header


def write_from_legacy(initial_data: FileData_Common, scene: GMDScene) -> bytes:
    # TODO: Attach to FileData as function as well?
    big_endian = check_is_file_big_endian(initial_data.file_endian_check)

    version = initial_data.parse_version()
    if version.major_version == GMDVersion.Kiwami1:
        new_filedata = package_legacy_abstraction_to_YK1(big_endian, version, cast(FileData_YK1, initial_data), scene)
        new_data = bytearray()
        FilePacker_YK1.pack(big_endian, new_filedata, new_data)
        return bytes(new_data)
    elif version.major_version == GMDVersion.Kenzan:
        # The only things that change between Kiwami1 and Kenzan are layouts, not data contents (except for bounds but those are just passed through)
        new_filedata = package_legacy_abstraction_to_YK1(big_endian, version, cast(FileData_YK1, initial_data), scene)
        new_data = bytearray()
        FilePacker_Kenzan.pack(big_endian, new_filedata, new_data)
        return bytes(new_data)
    else:
        raise Exception(f"File format {version} is unwritable")