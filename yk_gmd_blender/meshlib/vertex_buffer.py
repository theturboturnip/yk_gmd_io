from dataclasses import dataclass
from enum import Enum

import numpy as np

LITTLE_ENDIAN_U16 = np.dtype("<u2")
BIG_ENDIAN_U16 = np.dtype(">u2")
LITTLE_ENDIAN_F16 = np.dtype("<f2")
BIG_ENDIAN_F16 = np.dtype(">f2")
LITTLE_ENDIAN_F32 = np.dtype("<f4")
BIG_ENDIAN_F32 = np.dtype(">f4")


class VecCompFmt(Enum):
    Byte_0_1 = 0  # Fixed-point byte representation scaled between 0 and 1
    Byte_Minus1_1 = 1  # Fixed-point byte representation scaled between -1 and 1
    Byte_0_255 = 2  # Raw byte value, 0 to 255
    Float16 = 3  # 16-bit IEEE float
    Float32 = 4  # 32-bit IEEE float
    U16 = 5  # Unsigned 16-bit

    def native_size_bytes(self):
        if self in [VecCompFmt.Byte_0_1, VecCompFmt.Byte_Minus1_1, VecCompFmt.Byte_0_255]:
            return 1
        elif self in [VecCompFmt.Float16, VecCompFmt.U16]:
            return 2
        elif self == VecCompFmt.Float32:
            return 4
        raise RuntimeError(f"Nonexistent VecCompFmt called size_bytes: {self}")

    def numpy_native_dtype(self, big_endian: bool):
        if self in [VecCompFmt.Byte_0_1, VecCompFmt.Byte_Minus1_1, VecCompFmt.Byte_0_255]:
            return np.uint8
        elif self == VecCompFmt.U16:
            return BIG_ENDIAN_U16 if big_endian else LITTLE_ENDIAN_U16
        elif self == VecCompFmt.Float16:
            return BIG_ENDIAN_F16 if big_endian else LITTLE_ENDIAN_F16
        elif self == VecCompFmt.Float32:
            return BIG_ENDIAN_F32 if big_endian else LITTLE_ENDIAN_F32
        raise RuntimeError(f"Nonexistent VecCompFmt called numpy_native_dtype: {self}")

    def numpy_transformed_dtype(self):
        if self == VecCompFmt.Byte_0_255:
            return np.uint8
        elif self == VecCompFmt.U16:
            return np.uint16
        else:
            # Upgrade Float16 to Float32 so we can manipulate it without rounding error
            return np.float32


@dataclass(frozen=True)
class VecStorage:
    comp_fmt: VecCompFmt
    n_comps: int

    def __post_init__(self):
        assert 1 <= self.n_comps <= 4

    def native_size_bytes(self):
        return self.comp_fmt.native_size_bytes() * self.n_comps

    def numpy_native_dtype(self, big_endian: bool):
        return np.dtype((self.comp_fmt.numpy_native_dtype(big_endian), self.n_comps))

    def numpy_transformed_dtype(self):
        return np.dtype((self.comp_fmt.numpy_transformed_dtype(), self.n_comps))

    def preallocate(self, n_vertices: int) -> np.ndarray:
        return np.zeros(
            n_vertices,
            dtype=self.numpy_transformed_dtype(),
        )

    def transform_native_fmt_array(self, src: np.ndarray) -> np.ndarray:
        expected_dtype = self.comp_fmt.numpy_transformed_dtype()
        if self.comp_fmt in [VecCompFmt.Byte_0_255, VecCompFmt.U16, VecCompFmt.Float16, VecCompFmt.Float32]:
            # Always make a copy, even if the byte order is the same as we want.
            # The Blender side wants to do bone remapping etc. so we want a mutable version.
            # src is backed by `bytes` -> is immutable.
            # Float16 gets upgraded to float32 on transform to avoid rounding errors, so use same_kind instead of equiv
            return src.astype(expected_dtype, casting='same_kind', copy=True)
        elif self.comp_fmt == VecCompFmt.Byte_0_1:
            # src must have dtype == vector of uint8
            # it's always safe to cast uint8 -> float16 and float32, they can represent all values
            data = src.astype(expected_dtype, casting='safe')
            # (0, 255) -> (0, 1) by dividing by 255
            data = data / 255.0
            return data
        elif self.comp_fmt == VecCompFmt.Byte_Minus1_1:
            # src must have dtype == vector of uint8
            # it's always safe to cast uint8 -> float16 and float32, they can represent all values
            data = src.astype(expected_dtype, casting='safe')
            # (0, 255) -> (0, 1) by dividing by 255
            # (0, 1) -> (-1, 1) by multiplying by 2, subtracting 1
            data = ((data / 255.0) * 2.0) - 1.0
            return data
        raise RuntimeError(f"Invalid VecStorage called transform_native_fmt_array: {self}")

    def untransform_array(self, big_endian: bool, transformed: np.ndarray) -> np.ndarray:
        expected_dtype = self.comp_fmt.numpy_native_dtype(big_endian)
        if self.comp_fmt in [VecCompFmt.Byte_0_255, VecCompFmt.U16, VecCompFmt.Float16, VecCompFmt.Float32]:
            if transformed.dtype == expected_dtype:  # If the byte order is the same, passthru
                return transformed
            else:  # else make a copy with transformed byte order
                # Float16 is transformed as float32 to avoid rounding errors, so use same_kind instead of equiv
                return transformed.astype(expected_dtype, casting='same_kind')
        elif self.comp_fmt == VecCompFmt.Byte_0_1:
            # (0, 1) -> (0, 255) by multiplying by 255
            data = transformed * 255.0
            # Do rounding here because the cast doesn't do it right
            np.around(data, out=data)
            # storage = float, casting to int cannot preserve values -> use 'unsafe'
            return data.astype(expected_dtype, casting='unsafe')
        elif self.comp_fmt == VecCompFmt.Byte_Minus1_1:
            # (-1, 1) to (0, 1) by adding 1, dividing by 2
            # (0, 1) to (0, 255) by multiplying by 255
            data = ((transformed + 1.0) / 2.0) * 255.0
            # Do rounding here because the cast doesn't do it right
            np.around(data, out=data)
            # storage = float, casting to int cannot preserve values -> use 'unsafe'
            return data.astype(expected_dtype, casting='unsafe')
        raise RuntimeError(f"Invalid VecStorage called transform_native_fmt_array: {self}")
