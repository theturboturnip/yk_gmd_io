import pytest

from yk_gmd_blender.structurelib.primitives import c_uint8, c_uint16, c_uint32, c_uint64, c_int8, c_int32, c_int64, \
    c_int16, c_unorm8, c_u8_Minus1_1


# This module tests the structurelib finite-range primitive types,
# specifically that they are self-consistent i.e. unpack(pack(d)) === d.
# "finite-range" = "don't store as floating-point"

@pytest.mark.order(2)
def test_prim_uint8_selfconsistent():
    start, end = 0, 255
    n_points = 10
    t = c_uint8

    datapoints = [
        start + ((end - start) * x // n_points)
        for x in range(n_points + 1)
    ]
    for d in datapoints:
        b = bytearray()
        t.pack(False, d, b)
        t.pack(True, d, b)

        off = 0
        d_out_little, off = t.unpack(False, b, off)
        d_out_big, off = t.unpack(True, b, off)

        assert d_out_little == d
        assert d_out_big == d


@pytest.mark.order(2)
def test_prim_uint16_selfconsistent():
    start, end = 0, 65535
    n_points = 10
    t = c_uint16

    datapoints = [
        start + ((end - start) * x // n_points)
        for x in range(n_points + 1)
    ]
    for d in datapoints:
        b = bytearray()
        t.pack(False, d, b)
        t.pack(True, d, b)

        off = 0
        d_out_little, off = t.unpack(False, b, off)
        d_out_big, off = t.unpack(True, b, off)

        assert d_out_little == d
        assert d_out_big == d


@pytest.mark.order(2)
def test_prim_uint32_selfconsistent():
    start, end = 0, 4_294_967_295
    n_points = 10
    t = c_uint32

    datapoints = [
        start + ((end - start) * x // n_points)
        for x in range(n_points + 1)
    ]
    for d in datapoints:
        b = bytearray()
        t.pack(False, d, b)
        t.pack(True, d, b)

        off = 0
        d_out_little, off = t.unpack(False, b, off)
        d_out_big, off = t.unpack(True, b, off)

        assert d_out_little == d
        assert d_out_big == d


@pytest.mark.order(2)
def test_prim_uint64_selfconsistent():
    start, end = 0, 18_446_744_073_709_551_615
    n_points = 10
    t = c_uint64

    datapoints = [
        start + ((end - start) * x // n_points)
        for x in range(n_points + 1)
    ]
    for d in datapoints:
        b = bytearray()
        t.pack(False, d, b)
        t.pack(True, d, b)

        off = 0
        d_out_little, off = t.unpack(False, b, off)
        d_out_big, off = t.unpack(True, b, off)

        assert d_out_little == d
        assert d_out_big == d


@pytest.mark.order(2)
def test_prim_int8_selfconsistent():
    start, end = -128, 127
    n_points = 10
    t = c_int8

    datapoints = [
        start + ((end - start) * x // n_points)
        for x in range(n_points + 1)
    ]
    for d in datapoints:
        b = bytearray()
        t.pack(False, d, b)
        t.pack(True, d, b)

        off = 0
        d_out_little, off = t.unpack(False, b, off)
        d_out_big, off = t.unpack(True, b, off)

        assert d_out_little == d
        assert d_out_big == d


@pytest.mark.order(2)
def test_prim_int16_selfconsistent():
    start, end = -32_768, 32_767
    n_points = 10
    t = c_int16

    datapoints = [
        start + ((end - start) * x // n_points)
        for x in range(n_points + 1)
    ]
    for d in datapoints:
        b = bytearray()
        t.pack(False, d, b)
        t.pack(True, d, b)

        off = 0
        d_out_little, off = t.unpack(False, b, off)
        d_out_big, off = t.unpack(True, b, off)

        assert d_out_little == d
        assert d_out_big == d


@pytest.mark.order(2)
def test_prim_int32_selfconsistent():
    start, end = -2_147_483_648, 2_147_483_647
    n_points = 10
    t = c_int32

    datapoints = [
        start + ((end - start) * x // n_points)
        for x in range(n_points + 1)
    ]
    for d in datapoints:
        b = bytearray()
        t.pack(False, d, b)
        t.pack(True, d, b)

        off = 0
        d_out_little, off = t.unpack(False, b, off)
        d_out_big, off = t.unpack(True, b, off)

        assert d_out_little == d
        assert d_out_big == d


@pytest.mark.order(2)
def test_prim_int64_selfconsistent():
    start, end = -9_223_372_036_854_775_808, 9_223_372_036_854_775_807
    n_points = 10
    t = c_int64

    datapoints = [
        start + ((end - start) * x // n_points)
        for x in range(n_points + 1)
    ]
    for d in datapoints:
        b = bytearray()
        t.pack(False, d, b)
        t.pack(True, d, b)

        off = 0
        d_out_little, off = t.unpack(False, b, off)
        d_out_big, off = t.unpack(True, b, off)

        assert d_out_little == d
        assert d_out_big == d


@pytest.mark.order(2)
def test_prim_unorm8_selfconsistent():
    t = c_unorm8
    datapoints = [
        x / 255.0
        for x in range(256)
    ]
    for d in datapoints:
        b = bytearray()
        t.pack(False, d, b)
        t.pack(True, d, b)

        off = 0
        d_out_little, off = t.unpack(False, b, off)
        d_out_big, off = t.unpack(True, b, off)

        assert d_out_little == d
        assert d_out_big == d


@pytest.mark.order(2)
def test_prim_unorm8_exhaustive_repack():
    t = c_unorm8
    # Foreach byte
    b = bytearray(range(256))
    b_prime = bytearray()
    for i in range(256):
        d, _ = t.unpack(False, b, i)
        t.pack(True, d, b_prime)
    assert b == b_prime


@pytest.mark.order(2)
def test_prim_u8_Minus1_1_selfconsistent():
    start, end = -1.0, 1.0
    t = c_u8_Minus1_1
    datapoints = [
        start + ((end - start) * x / 255)
        for x in range(256)
    ]
    for d in datapoints:
        b = bytearray()
        t.pack(False, d, b)
        t.pack(True, d, b)

        off = 0
        d_out_little, off = t.unpack(False, b, off)
        d_out_big, off = t.unpack(True, b, off)

        assert d_out_little == d
        assert d_out_big == d


@pytest.mark.order(2)
def test_prim_u8_Minus1_1_exhaustive_repack():
    t = c_u8_Minus1_1
    # Foreach byte
    b = bytearray(range(256))
    b_prime = bytearray()
    for i in range(256):
        d, _ = t.unpack(False, b, i)
        t.pack(True, d, b_prime)

    assert list(b_prime) == list(b)
