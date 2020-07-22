import struct
from typing import Any, BinaryIO, List, Tuple

"""class BaseField:
    def read(self, data):
        raise NotImplementedError()

    def pack(self, value):
        raise NotImplementedError()

    def size(self):
        raise NotImplementedError()"""


"""class Field:
    def __init__(self, format):
        self.format = format

    def read(self, data):
        return struct.unpack_from(">" + self.format, data)

    def pack(self, value) -> bytes:
        return struct.pack(">" + self.format, value)

    def size(self):
        return struct.calcsize(">" + self.format)

    def format_str(self):
        return self.format

    def __add__(self, other):
        return Field(self.format + other.format)

    def __mul__(self, other):
        return Field(self.format * other)


uint8 = Field("B")
uint16 = Field("H")
uint32 = Field("I")
int8 = Field("b")
int16 = Field("h")
int32 = Field("i")
float16 = Field("e")
float32 = Field("f")

class AsciiText(Field):
    def __init__(self, length):
        super().__init__("c" * length)

    def read(self, data):
        char_bytes = super().read(data)
        return byte_str.decode

class Structure(Field):
    __fields__: List[Tuple[str,Field]] = []

    def __init__(self):
        super().__init__(self.format_str())

    def 

    def format_str(self):
        return sum(f[1].format_str() for f in self.__fields__)


class BitStreamReader:
    def __init__(self, bytes):
        self.bytes = bytes
        self.offset = 0

    def seek_abs(self, new_offset):
        self.offset = new_offset

    def read_field(self, field: Field) -> Any:
        new_offset = self.offset + field.size()
        data = self.bytes[self.offset:self.offset + field.size()]
        return field.read(data)
        """