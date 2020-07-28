from enum import Enum


class FileEndianness(Enum):
    LittleEndian = 0
    BigEndian = 1


def check_is_file_big_endian(file_endian_check: int):
    return FileEndianness(file_endian_check) == FileEndianness.BigEndian


def check_are_vertices_big_endian(vertex_endian_check: int):
    # for unsigned v, big_endian = (v - 1 <= 2) or (v == 6)
    # i.e. v in [1,2,3,6] (not 0, as for unsigned numbers 0-1 = 0xFFFFFFFFF
    vertices_big_endian = vertex_endian_check in [1,2,3,6]
    return vertices_big_endian
