import abc
from ctypes import Structure, BigEndianStructure, LittleEndianStructure
from typing import Any, Type, Tuple, List, SupportsBytes
import textwrap


def value_str(value) -> str:
    if "_Array_" in type(value).__name__:
        if isinstance(value[0], float):
            return str(["{0:0.3f}".format(i) for i in value])
        return str(list(value))
    return str(value)


class StructureElementsMixin:
    #def __init__(self):
    #    for (attr, t) in self._fields_:
    #        getattr(self, attr).__str__ = value_str

    def elems(self) -> List[Tuple[str, Type[Any], Any]]:
        elems = []
        for (attr, t) in self._fields_:
            elems.append((attr, t, getattr(self, attr)))
        return elems

    def csv_str(self):
        return ", ".join(str(e[2]) for e in self.elems())

    def struct_str(self):
        s = "{\n"
        for (name, t, value) in self.elems():
            s += textwrap.indent(f".{name} = {value_str(value)};\n", '\t')
        s += "}"
        return s

    def __str__(self):
        return self.struct_str()


#class BaseStructure(Structure, StructureElementsMixin):
#    _pack_ = 1
#    pass


# TODO: Adding SupportsBytes to the list would help fix typing errors, but it breaks Python 3.7
class BaseBigEndianStructure(BigEndianStructure, StructureElementsMixin):
    _pack_ = 1
    pass


#class BaseLittleEndianStructure(LittleEndianStructure, StructureElementsMixin):
#    _pack_ = 1
#    pass