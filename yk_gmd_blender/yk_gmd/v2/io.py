from pathlib import Path
from typing import Union, Tuple, cast

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.structure.common.header import GMDHeaderStruct, GMDHeaderStruct_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.endianness import check_is_file_big_endian
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.file import FileData_Kenzan, FilePacker_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.version import GMDVersion, VersionProperties
from yk_gmd_blender.yk_gmd.v2.structure.yk1.abstractor import read_abstract_contents_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.file import FileData_YK1, FilePacker_YK1


class InvalidGMDFormatError(Exception):
    pass


def _get_file_data(data: Union[Path, str, bytes]) -> bytes:
    if isinstance(data, (Path, str)):
        with open(data, "rb") as in_file:
            data = in_file.read()
        return data
    else:
        return data


def _extract_base_header(data: bytes) -> Tuple[bool, GMDHeaderStruct]:
    big_endian = True
    base_header, _ = GMDHeaderStruct_Unpack.unpack(big_endian, data=data, offset=0)
    big_endian = check_is_file_big_endian(base_header.file_endian_check)
    # Reimport the header with the correct endianness
    base_header, _ = GMDHeaderStruct_Unpack.unpack(big_endian, data=data, offset=0)
    return big_endian, base_header


def read_gmd_structures(data: Union[Path, str, bytes]) -> Tuple[VersionProperties, Union[FileData_Kenzan, FileData_YK1]]:
    data = _get_file_data(data)
    big_endian, base_header = _extract_base_header(data)

    version_props = base_header.get_version_properties()
    if version_props.major_version == GMDVersion.Kiwami1:
        contents, _ = FilePacker_YK1.unpack(big_endian, data=data, offset=0)

        return version_props, contents
    elif version_props.major_version == GMDVersion.Kenzan:
        contents, _ = FilePacker_Kenzan.unpack(big_endian, data=data, offset=0)

        return version_props, contents
    else:
        raise InvalidGMDFormatError(f"File format version {version_props.version_str} is not readable")


def read_abstract_scene_from_contents(version_props: VersionProperties, contents: Union[FileData_Kenzan, FileData_YK1]) -> GMDScene:
    if version_props.major_version == GMDVersion.Kiwami1:
        return read_abstract_contents_YK1(version_props, cast(FileData_YK1, contents))
    else:
        raise InvalidGMDFormatError(f"File format version {version_props.version_str} is not abstractable")

def read_abstract_scene_from_bytes(data: Union[Path, str, bytes]) -> GMDScene:
    data = _get_file_data(data)

    version_props, file_data = read_gmd_structures(data)
    return read_abstract_scene_from_contents(version_props, file_data)