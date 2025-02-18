from pathlib import Path
from typing import Union, Tuple, cast

from ..structurelib.base import PackingValidationError
from .abstract.gmd_scene import GMDScene
from .converters.common.to_abstract import FileImportMode, VertexImportMode
from .converters.dragon.from_abstract import pack_abstract_contents_Dragon
from .converters.dragon.to_abstract import GMDAbstractor_Dragon
from .converters.kenzan.from_abstract import pack_abstract_contents_Kenzan
from .converters.kenzan.to_abstract import GMDAbstractor_Kenzan
from .converters.yk1.from_abstract import pack_abstract_contents_YK1
from .converters.yk1.to_abstract import GMDAbstractor_YK1
from .errors.error_classes import InvalidGMDFormatError
from .errors.error_reporter import ErrorReporter
from .structure.common.file import FileUnpackError, FileData_Common
from .structure.common.header import GMDHeaderStruct, GMDHeaderStruct_Unpack
from .structure.dragon.file import FilePacker_Dragon, FileData_Dragon
from .structure.dragon.header import GMDHeader_Dragon_Unpack
from .structure.endianness import check_is_file_big_endian
from .structure.kenzan.file import FileData_Kenzan, FilePacker_Kenzan
from .structure.kenzan.header import GMDHeader_Kenzan_Unpack
from .structure.version import GMDVersion, VersionProperties
from .structure.yk1.file import FileData_YK1, FilePacker_YK1
from .structure.yk1.header import GMDHeader_YK1_Unpack


def _get_file_data(data: Union[Path, str, bytes], error_reporter: ErrorReporter) -> bytes:
    if isinstance(data, (Path, str)):
        try:
            with open(data, "rb") as in_file:
                data = in_file.read()
            return data
        except FileNotFoundError as e:
            error_reporter.fatal(str(e))
    else:
        return data


def _extract_base_header(data: bytes) -> Tuple[bool, GMDHeaderStruct]:
    big_endian = True
    base_header, _ = GMDHeaderStruct_Unpack.unpack(big_endian, data=data, offset=0)
    big_endian = check_is_file_big_endian(base_header.file_endian_check)
    # Reimport the header with the correct endianness
    base_header, _ = GMDHeaderStruct_Unpack.unpack(big_endian, data=data, offset=0)
    return big_endian, base_header


def get_file_header(data: Union[Path, str, bytes], error_reporter: ErrorReporter) -> GMDHeaderStruct:
    data = _get_file_data(data, error_reporter)
    _, base_header = _extract_base_header(data)
    return base_header


def read_gmd_structures(data: Union[Path, str, bytes], error_reporter: ErrorReporter) -> \
        Tuple[VersionProperties, GMDHeaderStruct, Union[FileData_Kenzan, FileData_YK1]]:
    data = _get_file_data(data, error_reporter)
    big_endian, base_header = _extract_base_header(data)

    header: GMDHeaderStruct

    version_props = base_header.get_version_properties()
    if version_props.major_version == GMDVersion.Kiwami1:
        try:
            header, _ = GMDHeader_YK1_Unpack.unpack(big_endian, data=data, offset=0)
            contents, _ = FilePacker_YK1.unpack(big_endian, data=data, offset=0)

            return version_props, header, contents
        except FileUnpackError as e:
            error_reporter.fatal(str(e))
    elif version_props.major_version == GMDVersion.Kenzan:
        try:
            header, _ = GMDHeader_Kenzan_Unpack.unpack(big_endian, data=data, offset=0)
            contents, _ = FilePacker_Kenzan.unpack(big_endian, data=data, offset=0)

            return version_props, header, contents
        except FileUnpackError as e:
            error_reporter.fatal(str(e))
    elif version_props.major_version == GMDVersion.Dragon:
        try:
            header, _ = GMDHeader_Dragon_Unpack.unpack(big_endian, data=data, offset=0)
            contents, _ = FilePacker_Dragon.unpack(big_endian, data=data, offset=0)

            return version_props, header, contents
        except FileUnpackError as e:
            error_reporter.fatal(str(e))
    else:
        raise InvalidGMDFormatError(f"File format version {version_props.version_str} is not readable")


def read_abstract_scene_from_filedata_object(version_props: VersionProperties, file_import_mode: FileImportMode,
                                             vertex_import_mode: VertexImportMode,
                                             contents: Union[FileData_Kenzan, FileData_YK1],
                                             error_reporter: ErrorReporter) -> GMDScene:
    if version_props.major_version == GMDVersion.Kiwami1:
        return GMDAbstractor_YK1(version_props, file_import_mode, vertex_import_mode, cast(FileData_YK1, contents),
                                 error_reporter).make_abstract_scene()
    elif version_props.major_version == GMDVersion.Dragon:
        return GMDAbstractor_Dragon(version_props, file_import_mode, vertex_import_mode,
                                    cast(FileData_Dragon, contents), error_reporter).make_abstract_scene()
    elif version_props.major_version == GMDVersion.Kenzan:
        return GMDAbstractor_Kenzan(version_props, file_import_mode, vertex_import_mode,
                                    cast(FileData_Kenzan, contents),
                                    error_reporter).make_abstract_scene()
    else:
        raise InvalidGMDFormatError(f"File format version {version_props.version_str} is not abstractable")


def check_version_writeable(version_props: VersionProperties, error_reporter: ErrorReporter):
    if version_props.major_version == GMDVersion.Kiwami1:
        return
    elif version_props.major_version == GMDVersion.Dragon:
        return
    elif version_props.major_version == GMDVersion.Kenzan:
        return
    else:
        error_reporter.fatal(f"File format version {version_props.version_str} is not writeable")


def pack_abstract_scene(version_props: VersionProperties, file_is_big_endian: bool, vertices_are_big_endian: bool,
                        scene: GMDScene, old_file_contents: Union[FileData_Kenzan, FileData_YK1, FileData_Dragon],
                        error_reporter: ErrorReporter) -> FileData_Common:
    if version_props.major_version == GMDVersion.Kiwami1:
        file_data = pack_abstract_contents_YK1(version_props, file_is_big_endian, vertices_are_big_endian, scene,
                                               error_reporter)
        return file_data
    elif version_props.major_version == GMDVersion.Dragon:
        file_data = pack_abstract_contents_Dragon(version_props, file_is_big_endian, vertices_are_big_endian, scene,
                                                  old_file_contents,
                                                  error_reporter)
        return file_data
    elif version_props.major_version == GMDVersion.Kenzan:
        file_data = pack_abstract_contents_Kenzan(version_props, file_is_big_endian, vertices_are_big_endian, scene,
                                                  error_reporter)
        return file_data
    else:
        raise InvalidGMDFormatError(f"File format version {version_props.version_str} is not packable")


def pack_file_data(version_props: VersionProperties, file_data: FileData_Common,
                   error_reporter: ErrorReporter) -> bytearray:
    if version_props.major_version == GMDVersion.Kiwami1:
        data_bytearray = bytearray()
        try:
            FilePacker_YK1.pack(file_data.file_is_big_endian(), file_data, data_bytearray)
        except PackingValidationError as e:
            error_reporter.fatal(str(e))
        return data_bytearray
    elif version_props.major_version == GMDVersion.Dragon:
        data_bytearray = bytearray()
        try:
            FilePacker_Dragon.pack(file_data.file_is_big_endian(), file_data, data_bytearray)
        except PackingValidationError as e:
            error_reporter.fatal(str(e))
        return data_bytearray
    elif version_props.major_version == GMDVersion.Kenzan:
        data_bytearray = bytearray()
        try:
            FilePacker_Kenzan.pack(file_data.file_is_big_endian(), file_data, data_bytearray)
        except PackingValidationError as e:
            error_reporter.fatal(str(e))
        return data_bytearray
    else:
        raise InvalidGMDFormatError(f"File format version {version_props.version_str} is not packable")


def write_abstract_scene_out(version_props: VersionProperties, file_is_big_endian: bool, vertices_are_big_endian: bool,
                             scene: GMDScene, old_file_contents: Union[FileData_Kenzan, FileData_YK1, FileData_Dragon],
                             path: Union[Path, str], error_reporter: ErrorReporter):
    file_data = pack_abstract_scene(version_props, file_is_big_endian, vertices_are_big_endian, scene,
                                    old_file_contents, error_reporter)
    data_bytearray = pack_file_data(version_props, file_data, error_reporter)
    try:
        with open(path, "wb") as out_file:
            out_file.write(data_bytearray)
    except IOError as e:
        error_reporter.fatal(str(e))
