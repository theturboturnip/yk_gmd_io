import struct
from dataclasses import dataclass
from typing import Any, Union, Tuple, Type, Optional, TypeVar, Generic, List, get_type_hints, Dict, cast, Callable

__all__ = [
    "BaseUnpacker",
    "StructureUnpacker",
    "FixedSizeArrayUnpacker",
    "FixedSizeASCIIUnpacker",
    "ValueAdaptor",
    "structure_data",
]

T = TypeVar('T')
TPackable = TypeVar('TPackable', bound='BaseUnpackable')

class PackingValidationError(Exception):
    pass

class BaseUnpacker(Generic[T]):
    """ Base class for every type of field that can be packed. """
    python_type: Type[T]

    def __init__(self, python_type: Type[T]):
        if not isinstance(python_type, type):
            raise TypeError(f"python_type of Unpacker must be a type object, got {python_type}")
        self.python_type = python_type

    def unpack(self, big_endian: bool, data: Union[bytes, bytearray], offset:int) -> Tuple[T, int]:
        raise NotImplementedError()

    def pack(self, big_endian: bool, value: T, append_to: bytearray):
        raise NotImplementedError()

    def validate_value(self, value: T):
        raise NotImplementedError()

    def sizeof(self):
        raise NotImplementedError()

    def array_of(self: T, count) -> 'FixedSizeArrayUnpacker[T]':
        return FixedSizeArrayUnpacker(self, count)


TFrom = TypeVar('TFrom')
TTo = TypeVar('TTo')
class ValueAdaptor(Generic[TFrom, TTo], BaseUnpacker[TTo]):
    base_unpacker: BaseUnpacker[TFrom]
    forwards: Callable[[TFrom], TTo]
    backwards: Callable[[TTo], TFrom]

    def __init__(self, tto: Type[TTo], base_unpacker: BaseUnpacker[TFrom], forwards: Callable[[TFrom], TTo], backwards: Callable[[TTo], TFrom]):
        super().__init__(tto)
        self.base_unpacker = base_unpacker
        self.forwards = forwards
        self.backwards = backwards

    def unpack(self, big_endian: bool, data: Union[bytes, bytearray], offset:int) -> Tuple[TTo, int]:
        from_val, offset = self.base_unpacker.unpack(big_endian, data, offset)
        return self.forwards(from_val), offset

    def pack(self, big_endian: bool, value: TTo, append_to: bytearray):
        self.validate_value(value)
        from_val = self.backwards(value)
        self.base_unpacker.pack(big_endian, from_val, append_to)

    def validate_value(self, value: TTo):
        try:
            self.base_unpacker.validate_value(self.backwards(value))
        except Exception as e:
            print(self.python_type, self.base_unpacker.python_type)
            raise PackingValidationError(f"{self.python_type.__name__} adapted to {self.base_unpacker.python_type.__name__}: {e}")

    def sizeof(self):
        return self.base_unpacker.sizeof()


class BasePrimitive(BaseUnpacker[T]):
    struct_fmt: str
    be_struct_fmt: str
    le_struct_fmt: str

    def __init__(self, python_type: Type[T], struct_fmt: str):
        super().__init__(python_type)
        self.struct_fmt = struct_fmt
        self.be_struct_fmt = f">{struct_fmt}"
        self.le_struct_fmt = f"<{struct_fmt}"

    # TODO: Validate in unpack/pack? If not, standardize and decide why

    def unpack(self, big_endian: bool, data: Union[bytes, bytearray], offset:int) -> Tuple[T, int]:
        return struct.unpack_from(self.be_struct_fmt if big_endian else self.le_struct_fmt, data, offset)[0], offset+self.sizeof()

    def pack(self, big_endian: bool, value: T, append_to: bytearray):
        self.validate_value(value)
        append_to += struct.pack(self.be_struct_fmt if big_endian else self.le_struct_fmt, value)

    def validate_value(self, value: T):
        if not isinstance(value, self.python_type):
            raise PackingValidationError(f"Expected {self.python_type.__name__}, got {type(value).__name__}")

    def sizeof(self):
        # Assumed that be_struct_format is hte same size as le_struct_fmt
        return struct.calcsize(self.be_struct_fmt)


class BoundedPrimitiveUnpacker(BasePrimitive[T]):
    range: Tuple[T, T]

    def __init__(self, python_type: Type[T], struct_fmt: str, range: Tuple[T,T]):
        super().__init__(python_type, struct_fmt)
        self.range = range

    def validate_value(self, value: T):
        super().validate_value(value)
        if not (self.range[0] <= value <= self.range[1]):
            raise PackingValidationError(f"Value {value} not in range {self.range}")


class FixedSizeASCIIUnpacker(BaseUnpacker[str]):
    length: int
    encoding: str

    def __init__(self, length: int, encoding: str = "ascii"):
        super().__init__(str)
        self.length = length
        self.encoding = encoding

    def unpack(self, big_endian: bool, data: Union[bytes, bytearray], offset:int) -> Tuple[T, int]:
        str_data:bytes = data[offset:offset + self.length]
        return str_data.decode(self.encoding).rstrip('\x00'), offset + self.length

    def pack(self, big_endian: bool, value: T, append_to: bytearray):
        self.validate_value(value)
        str_data: bytes = value.encode(self.encoding)
        if len(str_data) < self.length:
            str_data += bytes([0] * (self.length - len(str_data)))
        append_to += str_data

    def validate_value(self, value: str):
        encoded = value.encode(self.encoding)
        if len(encoded) > self.length:
            raise PackingValidationError(f"Encoded string {encoded} is {len(encoded)}, must be <= {self.length}")

    def sizeof(self):
        return self.length


class FixedSizeArrayUnpacker(Generic[T], BaseUnpacker[List[T]]):
    elem_type: BaseUnpacker[T]
    count: int

    def __init__(self, elem_type: BaseUnpacker[T], count: int):
        super().__init__(list)
        self.elem_type = elem_type
        self.count = count

    def unpack(self, big_endian: bool, data: Union[bytes, bytearray], offset:int) -> Tuple[List[T],int]:
        value = []
        while len(value) < self.count:
            next_val, offset = self.elem_type.unpack(big_endian, data, offset)
            value.append(next_val)
        return value, offset

    def pack(self, big_endian: bool, value: List[TPackable], append_to: bytearray):
        self.validate_value(value)
        for item in value:
            self.elem_type.pack(big_endian=big_endian, value=item, append_to=append_to)

    def sizeof(self):
        return self.elem_type.sizeof() * self.count

    def validate_value(self, value: List[T]):
        elem_type = self.elem_type
        if len(value) != self.count:
            raise PackingValidationError(f"List has {len(value)} items, expected {self.count}")
        for i,item in enumerate(value):
            # Type checking for whether item is supported by elem_type is done in elem_type
            try:
                elem_type.validate_value(item)
            except Exception as e:
                raise PackingValidationError(f"Element {i}: {e}")
        return True


TDataclass = TypeVar("TDataclass")


def structure_data(**kwargs):
    return dataclass(**kwargs, frozen=True, init=True)


MaybeOptionalBaseUnpacker = Union[Type[T], Type[Optional[T]]]

# TODO: Handle inheritance?
class StructureUnpacker(BaseUnpacker[TDataclass]):
    _fields: List[Tuple[str, BaseUnpacker]]
    _exported_fields: Dict[str, BaseUnpacker]
    _load_validate: Optional[Callable[[TDataclass], None]]

    def __init__(self, python_type: Type[TDataclass], fields: List[Tuple[str, BaseUnpacker]], base_class_unpackers: Dict[Type, 'StructureUnpacker'] = None, load_validate: Optional[Callable[[TDataclass], None]] = None):
        super().__init__(python_type)

        if base_class_unpackers is None:
            base_class_unpackers = {}

        # Follow the baseclasses up the chain
        def recursive_base_check(current: type, fields: List[Tuple[str, BaseUnpacker]]):
            data_bases = [base for base in current.__bases__ if get_type_hints(base)]

            # Check we don't have multiple inheritance from dataclasses
            if len(data_bases) > 1:
                raise TypeError(f"Structure dataclass {current.__name__} inherits from multiple dataclass bases {[b.__name__ for b in data_bases]} at the same level. This is not supported.")

            for base in data_bases:
                if base in base_class_unpackers:
                    # Add the base class fields first, as they come before the others
                    fields = base_class_unpackers[base]._fields + fields
                    fields = recursive_base_check(base, fields)
                #else:
                #    raise TypeError(f"{python_type.__name__} has a base class {base.__name__} with no corresponding unpacker")

            return fields

        fields = recursive_base_check(python_type, fields)

        _exported_fields = {}
        named_field_unpackers: Dict[str, BaseUnpacker] = {k: v for (k, v) in fields}
        dataclass_field_hints: Dict[str, MaybeOptionalBaseUnpacker] = get_type_hints(python_type)

        # Check all unpackers have a field, and make sure all unpackers are actually unpackers
        for field_name, field_unpacker in named_field_unpackers.items():
            if field_name not in dataclass_field_hints:
                raise TypeError(f"Unpacker {field_name} doesn't have corresponding field in {python_type.__name__}")
            if not isinstance(field_unpacker, BaseUnpacker):
                raise TypeError(f"Unpacker {field_name} is {field_unpacker}, not a BaseUnpacker instance")

        for field_name, field_type in dataclass_field_hints.items():
            # If the name isn't unpacked, and the field isn't optional, error
            if field_name not in named_field_unpackers:
                if hasattr(python_type, field_name):
                    # Name has a default value (assumes dataclass.field() always allows the field to be optional)
                    continue
                else:
                    raise TypeError(f"Field {python_type.__name__}.{field_name} doesn't have an unpacker and doesn't have a default value")

            unpacked_type = named_field_unpackers[field_name].python_type
            if field_type is not unpacked_type:
                # Allow generics from the same origin to be represented by the same packer
                # i.e. ArrayPointer[float] and ArrayPointer[int] can both be unpacked by an unpacker for ArrayPointer
                if not (hasattr(field_type, "__origin__") and field_type.__origin__ is unpacked_type):
                    raise TypeError(
                        f"Field {python_type.__name__}.{field_name} expects {field_type} but is unpacked as {unpacked_type}")

            _exported_fields[field_name] = named_field_unpackers[field_name]

        self._fields = fields
        self._exported_fields = _exported_fields
        self._load_validate = load_validate

    def unpack(self, big_endian: bool, data: Union[bytes, bytearray], offset: int) -> Tuple[TDataclass, int]:
        items_dict = {}
        for field_name, field_unpacker in self._fields:
            value, offset = field_unpacker.unpack(big_endian, data, offset)
            if field_name in self._exported_fields:
                items_dict[field_name] = value

        value = self.python_type(**items_dict)
        if self._load_validate:
            self._load_validate(value)
        return value, offset

    def pack(self, big_endian: bool, value: TDataclass, append_to: bytearray):
        self.validate_value(value)
        for field_name, field_unpacker in self._fields:
            field_unpacker.pack(big_endian, getattr(value, field_name), append_to)

    def validate_value(self, value: TDataclass) -> bool:
        if not isinstance(value, self.python_type):
            raise PackingValidationError(f"Incorrect value type - expected {self.python_type} got {type(value)}")

        for field_name, field_unpacker in self._exported_fields.items():
            try:
                field_unpacker.validate_value(getattr(value, field_name))
            except PackingValidationError as e:
                raise PackingValidationError(f"Field {field_name}: {e}")
        return True

    def sizeof(self):
        return sum(unpacker.sizeof() for _,unpacker in self._fields)
