from dataclasses import dataclass
from enum import Enum
from typing import Type, Union, Tuple, List

from ....structurelib.base import StructureUnpacker, BaseUnpacker, PackingValidationError
from .array_pointer import ArrayPointerStruct
from .checksum_str import ChecksumStrStruct
from .header import GMDHeaderStruct
from .sized_pointer import SizedPointerStruct
from ..endianness import check_is_file_big_endian, check_are_vertices_big_endian
from ..version import VersionProperties, \
    get_combined_version_properties


class PackType(Enum):
    Array = 0,
    Bytes = 1


class FileUnpackError(Exception):
    pass


@dataclass(repr=False)
class FileData_Common:
    magic: str
    file_endian_check: int
    vertex_endian_check: int
    version_combined: int

    name: ChecksumStrStruct

    def file_is_big_endian(self):
        return check_is_file_big_endian(self.file_endian_check)

    def vertices_are_big_endian(self):
        return check_are_vertices_big_endian(self.vertex_endian_check)

    def parse_version(self) -> VersionProperties:
        return get_combined_version_properties(self.version_combined)

    @classmethod
    def header_pointer_fields(cls) -> List[Tuple[str, Union[BaseUnpacker, Type[bytes]]]]:
        """
        Returns a List of (header field name, packing type).

        Each element of the list is added to the file in the following way:
        If the packing type is bytes, the byte contents are added to the file data and the header field is set to a SizedPointer
        If the packing type is a BaseUnpacker, the packer is used to pack the data and the header field is set to an ArrayPointer
        """
        return []

    @classmethod
    def header_fields_to_copy(cls) -> List[str]:
        """
        Returns a list of fields to copy from the header into the FileData
        :return: a list of fields to copy from the header into the FileData
        """
        return [
            "magic",
            "file_endian_check",
            "vertex_endian_check",
            "version_combined",

            "name"
        ]


# TODO: Generics?
# TODO: Refactor to do typechecking for header_pointer_fields, header_fields_to_copy, including missing fields
class FilePacker(BaseUnpacker[FileData_Common]):
    header_packer: StructureUnpacker[GMDHeaderStruct]

    def __init__(self, filedata_type: Type[FileData_Common], header_packer: StructureUnpacker[GMDHeaderStruct]):
        super().__init__(filedata_type)
        self.header_packer = header_packer
        # TODO: Check python_type.packing_type() fields to ensure correctness

    def pack(self, big_endian: bool, value: FileData_Common, append_to: bytearray):
        # Packing phases
        # 1. Pack contents (NOT HEADER) into bytes to get addresses and sizes
        # Requires subclass intervention - subclass must be able to supply new data to be packed
        # addresses also depend on the size of the actual header - subclass supplies that
        # 2. Use these content addresses/sizes to fill the header
        # Requires subclass intervention - subclass needs to supply content addrs/sizes and the fields to fill them in
        # 3. Pack the header
        # No intervention required as long as header_packer is set
        # 4. Concatenate the bytes
        # No intervention required

        # TODO: Pad header_size to a constant value like the games do
        header_size = self.header_packer.sizeof()
        collective_data = bytearray()

        def pack_data(name: str, packer: Union[Type[bytes], BaseUnpacker], collective_data: bytearray) -> Union[
            SizedPointerStruct, ArrayPointerStruct]:
            ptr = header_size + len(collective_data)

            attr: Union[bytes, list] = getattr(value, name)
            sized_pointer = SizedPointerStruct(ptr=ptr, size=len(attr))
            if packer is bytes:
                if not isinstance(attr, bytes):
                    raise TypeError(
                        f"Value field {name} was expected to be bytes, because {self.python_type.__name__} specified it to be byte-packed")
                collective_data += attr
                return sized_pointer
            elif isinstance(packer, BaseUnpacker):
                if not isinstance(attr, list):
                    raise TypeError(
                        f"Header field {name} was expected as list, because {self.python_type.__name__} specified it to be packed by {packer}")
                for i, item in enumerate(attr):
                    try:
                        packer.pack(big_endian, item, collective_data)
                    except PackingValidationError as e:
                        raise PackingValidationError(f"Element {i}: {e}")
                return ArrayPointerStruct(sized_ptr=sized_pointer)
            else:
                raise TypeError(f"Unexpected packer type {packer}")

        header_copies = {}
        for name in self.python_type.header_fields_to_copy():
            header_copies[name] = getattr(value, name)

        element_pointers = {}
        for name, packer in self.python_type.header_pointer_fields():
            try:
                element_pointers[name] = pack_data(name, packer, collective_data)
            except PackingValidationError as e:
                raise PackingValidationError(f"File Element {name}: {e}")

        header = self.header_packer.python_type(
            **header_copies,
            **element_pointers,

            file_size=header_size + len(collective_data),
            padding=0
        )

        self.header_packer.pack(big_endian, header, append_to)
        append_to += collective_data

    def unpack(self, big_endian: bool, data: Union[bytes, bytearray], offset: int) -> Tuple[FileData_Common, int]:
        # Unpacking phases
        # 1. Unpack the header
        # No subclass intervention required as long as header_packer is set
        # 2. Unpack each set of contents
        # Requires subclass intervention - subclass needs to supply which fields to unpack

        header, offset = self.header_packer.unpack(big_endian, data, offset)

        def unpack_data(name: str, unpacker: Union[Type[bytes], BaseUnpacker]):
            attr = getattr(header, name)
            if unpacker is bytes:
                if not isinstance(attr, SizedPointerStruct):
                    raise TypeError(
                        f"Header field {name} was expected as SizedPointer but was {attr}. "
                        f"Reason: {self.python_type.__name__} specified it to be byte-packed")
                return attr.extract_bytes(data)
            elif isinstance(unpacker, BaseUnpacker):
                if not isinstance(attr, ArrayPointerStruct):
                    raise TypeError(
                        f"Header field {name} was expected as ArrayPointer but was {attr}. "
                        f"Reason: {self.python_type.__name__} specified it to be packed by {unpacker}")
                try:
                    return attr.extract(unpacker, big_endian, data)
                except Exception as e:
                    raise FileUnpackError(
                        f"Exception while unpacking field {name} from 0x{attr.ptr:x}[{attr.count}]: {e}")
            else:
                raise TypeError(f"Unexpected unpacker type {unpacker}")

        header_copies = {}
        for name in self.python_type.header_fields_to_copy():
            header_copies[name] = getattr(header, name)

        data_dict = {
            k: unpack_data(k, v)
            for k, v in self.python_type.header_pointer_fields()
        }

        file_data = self.python_type(
            **header_copies,
            **data_dict
        )

        return file_data, -1

    def validate_value(self, value: FileData_Common):
        raise NotImplementedError()

    # TODO: Better way of doing this would be to have sizeof relegated to BaseConstantSizeUnpacker?
    def sizeof(self):
        raise NotImplementedError("The size of GMD Files is not constant")
