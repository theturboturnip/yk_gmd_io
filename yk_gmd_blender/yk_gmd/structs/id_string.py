from ctypes import *

from ._base.base_structure import BaseBigEndianStructure
from ._base.text import ascii_text


class IdStringStruct(BaseBigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("id", c_uint16),
        ("text_internal", ascii_text(30))
    ]

    @property
    def text(self):
        return self.text_internal.decode('ascii')

    def __str__(self):
        return f"({self.id}:{self.text})"
    def __repr__(self):
        return f"({self.id}:{self.text_internal})"