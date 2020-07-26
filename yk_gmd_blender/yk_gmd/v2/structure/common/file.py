from dataclasses import dataclass
from enum import Enum
from typing import Type, Union, Tuple, List

from yk_gmd_blender.structurelib.base import StructureUnpacker, BaseUnpacker
from yk_gmd_blender.yk_gmd.v2.structure.common.array_pointer import ArrayPointer
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStr
from yk_gmd_blender.yk_gmd.v2.structure.common.header import GMDHeader
from yk_gmd_blender.yk_gmd.v2.structure.common.sized_pointer import SizedPointer


class PackType(Enum):
    Array = 0,
    Bytes = 1


@dataclass(repr=False)
class FileData_Common:
    magic: str
    file_endian_check: int
    vertex_endian_check: int
    version: int

    name: ChecksumStr

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
            "version",

            "name"
        ]


# TODO: Generics?
# TODO: Refactor to do typechecking for header_pointer_fields, header_fields_to_copy, including missing fields
class FilePacker(BaseUnpacker[FileData_Common]):
    header_packer: StructureUnpacker[GMDHeader]

    def __init__(self, filedata_type: Type[FileData_Common], header_packer: StructureUnpacker[GMDHeader]):
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

        header_size = self.header_packer.sizeof()
        collective_data = bytearray()

        def pack_data(name: str, packer: Union[Type[bytes], BaseUnpacker], collective_data: bytearray) -> Union[SizedPointer, ArrayPointer]:
            ptr = header_size + len(collective_data)

            attr: Union[bytes, list] = getattr(value, name)
            sized_pointer = SizedPointer(ptr=ptr, size=len(attr))
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
                for item in attr:
                    packer.pack(big_endian, item, collective_data)
                return ArrayPointer(sized_ptr=sized_pointer)
            else:
                raise TypeError(f"Unexpected packer type {packer}")

        header_copies = {}
        for name in self.python_type.header_fields_to_copy():
            header_copies[name] = getattr(value, name)

        element_pointers = {}
        for name, packer in self.python_type.header_pointer_fields():
            element_pointers[name] = pack_data(name, packer, collective_data)

        header = self.header_packer.python_type(
            **header_copies,
            **element_pointers,

            file_size=header_size + len(collective_data),
            padding=0
        )

        self.header_packer.pack(big_endian, header, append_to)
        append_to += collective_data

    def unpack(self, big_endian: bool, data: Union[bytes, bytearray], offset:int) -> Tuple[FileData_Common, int]:
        # Unpacking phases
            # 1. Unpack the header
                # No subclass intervention required as long as header_packer is set
            # 2. Unpack each set of contents
                # Requires subclass intervention - subclass needs to supply which fields to unpack

        header, offset = self.header_packer.unpack(big_endian, data, offset)

        def unpack_data(name: str, unpacker: Union[Type[bytes], BaseUnpacker]):
            attr = getattr(header, name)
            if unpacker is bytes:
                if not isinstance(attr, SizedPointer):
                    raise TypeError(f"Header field {name} was expected as SizedPointer but was {attr}. Reason: {self.python_type.__name__} specified it to be byte-packed")
                return attr.extract_bytes(data)
            elif isinstance(unpacker, BaseUnpacker):
                if not isinstance(attr, ArrayPointer):
                    raise TypeError(f"Header field {name} was expected as ArrayPointer but was {attr}. Reason: {self.python_type.__name__} specified it to be packed by {unpacker}")
                return attr.extract(unpacker, big_endian, data)
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

    def validate_value(self, value: FileData_Common) -> bool:
        raise NotImplementedError()

    # TODO: Better way of doing this would be to have sizeof relegated to BaseConstantSizeUnpacker?
    def sizeof(self):
        raise NotImplementedError("The size of GMD Files is not constant")


