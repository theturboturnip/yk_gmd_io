from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, List, Sized, Iterable, Set, overload

import numpy as np

from mathutils import Vector
from yk_gmd_blender.structurelib.base import FixedSizeArrayUnpacker, ValueAdaptor, BaseUnpacker
from yk_gmd_blender.structurelib.primitives import c_float32, c_float16, c_unorm8, U8ConverterPrimitive, \
    c_u8_Minus1_1
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter
from yk_gmd_blender.yk_gmd.v2.structure.common.vector import Vec3Unpacker_of, Vec4Unpacker_of

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

    def size_bytes(self):
        if self in [VecCompFmt.Byte_0_1, VecCompFmt.Byte_Minus1_1, VecCompFmt.Byte_0_255]:
            return 1
        elif self == VecCompFmt.Float16:
            return 2
        elif self == VecCompFmt.Float32:
            return 4
        raise RuntimeError(f"Nonexistent VecCompFmt called size_bytes: {self}")

    def numpy_native_dtype(self, big_endian: bool):
        if self in [VecCompFmt.Byte_0_1, VecCompFmt.Byte_Minus1_1, VecCompFmt.Byte_0_255]:
            return np.uint8
        elif self == VecCompFmt.Float16:
            return BIG_ENDIAN_F16 if big_endian else LITTLE_ENDIAN_F16
        elif self == VecCompFmt.Float32:
            return BIG_ENDIAN_F32 if big_endian else LITTLE_ENDIAN_F32
        raise RuntimeError(f"Nonexistent VecCompFmt called numpy_native_dtype: {self}")

    def numpy_transformed_dtype(self):
        if self == VecCompFmt.Byte_0_255:
            return np.uint8
        elif self == VecCompFmt.Float16:
            return np.float16
        else:
            return np.float32


@dataclass(frozen=True)
class VecStorage:
    comp_fmt: VecCompFmt
    n_comps: int

    def __post_init__(self):
        assert 1 <= self.n_comps <= 4

    def size_bytes(self):
        return self.comp_fmt.size_bytes() * self.n_comps

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
        if self.comp_fmt in [VecCompFmt.Byte_0_255, VecCompFmt.Float16, VecCompFmt.Float32]:
            if src.dtype == expected_dtype:  # If the byte order is the same, passthru
                return src
            else:  # else make a copy with transformed byte order
                return src.astype(expected_dtype, casting='equiv')
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
        if self.comp_fmt in [VecCompFmt.Byte_0_255, VecCompFmt.Float16, VecCompFmt.Float32]:
            if transformed.dtype == expected_dtype:  # If the byte order is the same, passthru
                return transformed
            else:  # else make a copy with transformed byte order
                return transformed.astype(expected_dtype, casting='equiv')
        elif self.comp_fmt == VecCompFmt.Byte_0_1:
            # (0, 1) -> (0, 255) by multiplying by 255
            data = transformed * 255.0
            # storage = float, casting to int cannot preserve values -> use 'unsafe'
            return data.astype(expected_dtype, casting='unsafe')
        elif self.comp_fmt == VecCompFmt.Byte_Minus1_1:
            # (-1, 1) to (0, 1) by adding 1, dividing by 2
            # (0, 1) to (0, 255) by multiplying by 255
            data = ((transformed + 1.0) / 2.0) * 255.0
            # storage = float, casting to int cannot preserve values -> use 'unsafe'
            return data.astype(expected_dtype, casting='unsafe')
        raise RuntimeError(f"Invalid VecStorage called transform_native_fmt_array: {self}")


vector_unpackers = {
    (2, VecCompFmt.Float32): ValueAdaptor(Vector, base_unpacker=FixedSizeArrayUnpacker(c_float32, 2), forwards=Vector,
                                          backwards=list),
    (3, VecCompFmt.Float32): Vec3Unpacker_of(c_float32),
    (4, VecCompFmt.Float32): Vec4Unpacker_of(c_float32),

    (2, VecCompFmt.Float16): ValueAdaptor(Vector, base_unpacker=FixedSizeArrayUnpacker(c_float16, 2), forwards=Vector,
                                          backwards=list),
    (3, VecCompFmt.Float16): Vec3Unpacker_of(c_float16),
    (4, VecCompFmt.Float16): Vec4Unpacker_of(c_float16),

    (4, VecCompFmt.Byte_0_1): Vec4Unpacker_of(c_unorm8),
    (4, VecCompFmt.Byte_Minus1_1): Vec4Unpacker_of(c_u8_Minus1_1),
    # We store bone_data in a Vector, which stores components as floats
    # Just using Vec4Unpacker_of(c_uint8) requires the incoming data to be int
    # Instead, use an identity RangeConverterPrimitive to convert it to float without changing the underlying value.
    # Can still be cast to int if needed, as in BoneWeight.
    (4, VecCompFmt.Byte_0_255): Vec4Unpacker_of(U8ConverterPrimitive(to_range=(0., 255.0)))
}


@overload
def make_vector_unpacker(vec_type: VecStorage) -> BaseUnpacker[Vector]: ...


@overload
def make_vector_unpacker(vec_type: None) -> None: ...


def make_vector_unpacker(vec_type: Optional[VecStorage]) -> Optional[BaseUnpacker[Vector]]:
    if vec_type is None:
        return None
    return vector_unpackers[(vec_type.n_comps, vec_type.comp_fmt)]


# This is effectively a primitive
@dataclass(frozen=True)
class BoneWeight:
    bone: int
    weight: float


BoneWeight4 = Tuple[BoneWeight, BoneWeight, BoneWeight, BoneWeight]


# Generic representation of a vertex buffer, that can contain "weights" and "bones" separately.
# Some unskinned objects use the "weights" and "bones" categories for different things, which this supports.
# This class should be used for all vertex buffer manipulation,
# then exported as a GMDVertexBuffer_Skinned if used in a Skinned mesh.
@dataclass(repr=False)
class GMDVertexBuffer_Generic(Sized):
    layout: 'GMDVertexBufferLayout'

    pos: np.ndarray
    weight_data: Optional[np.ndarray]
    bone_data: Optional[np.ndarray]
    normal: Optional[np.ndarray]
    tangent: Optional[np.ndarray]
    unk: Optional[np.ndarray]
    col0: Optional[np.ndarray]
    col1: Optional[np.ndarray]
    uvs: List[np.ndarray]

    @staticmethod
    def build_empty(layout: 'GMDVertexBufferLayout', count: int):
        alloc_storage = lambda storage: storage.preallocate(count) if storage else None
        return GMDVertexBuffer_Generic(
            layout=layout,

            pos=layout.pos_storage.preallocate(count),

            weight_data=alloc_storage(layout.weights_storage),
            bone_data=alloc_storage(layout.bones_storage),
            normal=alloc_storage(layout.normal_storage),
            tangent=alloc_storage(layout.tangent_storage),
            unk=alloc_storage(layout.unk_storage),
            col0=alloc_storage(layout.col0_storage),
            col1=alloc_storage(layout.col1_storage),
            uvs=[
                alloc_storage(s)
                for s in layout.uv_storages
            ],
        )

    def vertex_count(self):
        return len(self.pos)

    def __len__(self):
        return self.vertex_count()

    def __iadd__(self, other: 'GMDVertexBuffer_Generic') -> 'GMDVertexBuffer_Generic':
        if other.layout != self.layout:
            raise TypeError("Tried to combine two vertex buffers which used different layouts")

        self.pos += other.pos
        if self.weight_data is not None:
            self.weight_data += other.weight_data
        if self.bone_data is not None:
            self.bone_data += other.bone_data
        if self.normal is not None:
            self.normal += other.normal
        if self.tangent is not None:
            self.tangent += other.tangent
        if self.unk is not None:
            self.unk += other.unk
        if self.col0 is not None:
            self.col0 += other.col0
        if self.col1 is not None:
            self.col1 += other.col1
        for i, uv in enumerate(self.uvs):
            uv += other.uvs[i]

        return self

    def extract_as_generic(self, item: slice) -> 'GMDVertexBuffer_Generic':
        if not isinstance(item, slice):
            raise IndexError(f"GMDVertexBuffer_Generic.extract_as got {item} but expected slice")

        return GMDVertexBuffer_Generic(
            layout=self.layout,

            pos=self.pos[item],

            weight_data=self.weight_data[item] if self.weight_data is not None else None,
            bone_data=self.bone_data[item] if self.bone_data is not None else None,
            normal=self.normal[item] if self.normal is not None else None,
            tangent=self.tangent[item] if self.tangent is not None else None,
            unk=self.unk[item] if self.unk is not None else None,
            col0=self.col0[item] if self.col0 is not None else None,
            col1=self.col1[item] if self.col1 is not None else None,
            uvs=[
                uv[item]
                for uv in self.uvs
            ],
        )

    def __getitem__(self, item) -> 'GMDVertexBuffer_Generic':
        return self.extract_as_generic(item)

    # This doesn't copy the lists and vertices, rather just moves them
    # TODO - add a moved_out field to this class so we can detect use-after-move?
    def move_to_skinned(self) -> 'GMDVertexBuffer_Skinned':
        if not self.layout.assume_skinned:
            raise RuntimeError("Vertex Layout not built with assume_skinned, cannot convert to skinned")
        if self.weight_data is None or self.bone_data is None:
            raise RuntimeError("Bone-weight data for buffer is incomplete, cannot convert to skinned")

        bone_weights = [(
            BoneWeight(bone=int(bones[0]), weight=weights[0]),
            BoneWeight(bone=int(bones[1]), weight=weights[1]),
            BoneWeight(bone=int(bones[2]), weight=weights[2]),
            BoneWeight(bone=int(bones[3]), weight=weights[3]),
        ) for bones, weights in zip(self.bone_data, self.weight_data)]

        skinned = GMDVertexBuffer_Skinned(
            layout=self.layout,

            pos=self.pos,

            bone_weights=bone_weights,
            bone_data=self.bone_data,
            weight_data=self.weight_data,
            normal=self.normal if self.normal is not None else None,
            tangent=self.tangent if self.tangent is not None else None,
            unk=self.unk if self.unk is not None else None,
            col0=self.col0 if self.col0 is not None else None,
            col1=self.col1 if self.col1 is not None else None,
            uvs=[
                uv
                for uv in self.uvs
            ],
        )

        self.pos = np.asarray([])
        self.bone_data = None
        self.weight_data = None
        self.normal = None
        self.tangent = None
        self.unk = None
        self.col0 = None
        self.col1 = None
        self.uvs = []

        return skinned

    def extract_as_skinned(self, item: slice) -> 'GMDVertexBuffer_Skinned':
        return self.extract_as_generic(item).move_to_skinned()


# Immutable version of GMDVertexBuffer that includes a bone_weights list
@dataclass(repr=False)
class GMDVertexBuffer_Skinned(GMDVertexBuffer_Generic):
    layout: 'GMDVertexBufferLayout'

    bone_weights: List[BoneWeight4]
    # Individual bone,weight datas are still here, but must not be None
    weight_data: np.ndarray
    bone_data: np.ndarray

    def copy_as_generic(self) -> GMDVertexBuffer_Generic:
        return GMDVertexBuffer_Generic(
            layout=self.layout,

            pos=self.pos[:],

            bone_data=self.bone_data[:],
            weight_data=self.weight_data[:],
            normal=self.normal[:] if self.normal is not None else None,
            tangent=self.tangent[:] if self.tangent is not None else None,
            unk=self.unk[:] if self.unk is not None else None,
            col0=self.col0[:] if self.col0 is not None else None,
            col1=self.col1[:] if self.col1 is not None else None,
            uvs=[
                uv[:]
                for uv in self.uvs
            ],
        )

    def __iadd__(self, other: 'GMDVertexBuffer_Generic') -> 'GMDVertexBuffer_Generic':
        raise NotImplementedError()

    def extract_as_generic(self, item: slice) -> 'GMDVertexBuffer_Generic':
        raise NotImplementedError()

    def move_to_skinned(self) -> 'GMDVertexBuffer_Skinned':
        raise NotImplementedError()

    def extract_as_skinned(self, item: slice) -> 'GMDVertexBuffer_Skinned':
        raise NotImplementedError()

    def __getitem__(self, item) -> 'GMDVertexBuffer_Skinned':
        return GMDVertexBuffer_Skinned(
            layout=self.layout,

            pos=self.pos[item],

            bone_weights=self.bone_weights[item],
            bone_data=self.bone_data[item],
            weight_data=self.weight_data[item],
            normal=self.normal[item] if self.normal is not None else None,
            tangent=self.tangent[item] if self.tangent is not None else None,
            unk=self.unk[item] if self.unk is not None else None,
            col0=self.col0[item] if self.col0 is not None else None,
            col1=self.col1[item] if self.col1 is not None else None,
            uvs=[
                uv[item]
                for uv in self.uvs
            ],
        )


# VertexBufferLayouts are external dependencies (shaders have a fixed layout, which we can't control) so they are frozen
@dataclass(frozen=True, init=True)
class GMDVertexBufferLayout:
    assume_skinned: bool

    pos_unpacker: BaseUnpacker[Vector]
    # For skinned objects, this is for bone weights.
    # For unskinned objects, this is a generic component.
    weights_unpacker: Optional[BaseUnpacker[Vector]]
    # As above, this is bone weights for skinned objects but a generic component on unskinned objects.
    bones_unpacker: Optional[BaseUnpacker[Vector]]
    normal_unpacker: Optional[BaseUnpacker[Vector]]
    tangent_unpacker: Optional[BaseUnpacker[Vector]]
    unk_unpacker: Optional[BaseUnpacker[Vector]]
    col0_unpacker: Optional[BaseUnpacker[Vector]]
    col1_unpacker: Optional[BaseUnpacker[Vector]]
    uv_unpackers: Tuple[BaseUnpacker[Vector], ...]

    pos_storage: VecStorage
    weights_storage: Optional[VecStorage]
    bones_storage: Optional[VecStorage]
    normal_storage: Optional[VecStorage]
    tangent_storage: Optional[VecStorage]
    unk_storage: Optional[VecStorage]
    col0_storage: Optional[VecStorage]
    col1_storage: Optional[VecStorage]
    uv_storages: Tuple[VecStorage, ...]

    packing_flags: int

    def __str__(self):
        return f"GMDVertexBufferLayout(\n" \
               f"big_endian: {self.big_endian},\n" \
               f"assume_skinned: {self.assume_skinned},\n" \
               f"packing_flags: {self.packing_flags:016x},\n" \
               f"\n" \
               f"pos: {self.pos_storage},\n" \
               f"weights: {self.weights_storage},\n" \
               f"bones: {self.bones_storage},\n" \
               f"normal: {self.normal_storage},\n" \
               f"tangent: {self.tangent_storage},\n" \
               f"unk: {self.unk_storage},\n" \
               f"col0: {self.col0_storage},\n" \
               f"col1: {self.col1_storage},\n" \
               f"uv: {self.uv_storages}\n" \
               f")"

    @staticmethod
    def build_vertex_buffer_layout_from_flags(vertex_packing_flags: int, assume_skinned: bool,
                                              error: ErrorReporter, checked: bool = True) -> 'GMDVertexBufferLayout':
        # This derived from the 010 template
        # Bit-checking logic - keep track of the bits we examine, to ensure we don't miss anything
        if checked:
            touched_packing_bits: Set[int] = set()

            def touch_bits(bit_indices: Iterable[int]):
                touched_bits = set(bit_indices)
                if touched_bits.intersection(touched_packing_bits):
                    error.recoverable(f"Retouching bits {touched_bits.intersection(touched_packing_bits)}")
                touched_packing_bits.update(touched_bits)
        else:
            def touch_bits(bit_indices: Iterable[int]):
                pass

        # Helper for extracting a bitrange start:length and marking those bits as touched.
        def extract_bits(start, length):
            touch_bits(range(start, start + length))

            # Extract bits by shifting down to start and generating a mask of `length` 1's in binary
            # TODO that is the worst possible way to generate that mask.
            return (vertex_packing_flags >> start) & int('1' * length, 2)

        # Helper for extracting a bitmask and marking those bits as touched.
        def extract_bitmask(bitmask):
            touch_bits([i for i in range(32) if ((bitmask >> i) & 1)])

            return vertex_packing_flags & bitmask

        # If the given vector type is `en`abled, extract the bits start:start+2 and find the VecStorage they refer to.
        # If the vector uses full-precision float components, the length is set by `full_precision_n_comps`.
        # If the vector uses byte-size components, the format of those bytes is set by `byte_fmt`.
        def extract_vector_type(en: bool, start: int,
                                full_precision_n_comps: int, byte_fmt: VecCompFmt) -> Optional[VecStorage]:
            bits = extract_bits(start, 2)
            if en:
                if bits == 0:
                    # Float32
                    comp_fmt = VecCompFmt.Float32
                    n_comps = full_precision_n_comps
                elif bits == 1:
                    # Float16
                    comp_fmt = VecCompFmt.Float16
                    n_comps = 4
                else:
                    # Some kind of fixed
                    comp_fmt = byte_fmt
                    n_comps = 4
                return VecStorage(comp_fmt, n_comps)
            else:
                return None

        # pos can be (3 or 4) * (half or full) floats
        pos_count = extract_bits(0, 3)
        pos_precision = extract_bits(3, 1)
        pos_storage = VecStorage(
            comp_fmt=VecCompFmt.Float16 if pos_precision == 1 else VecCompFmt.Float32,
            n_comps=3 if pos_count == 3 else 4
        )

        weight_en = extract_bitmask(0x70)
        weights_storage = extract_vector_type(weight_en, 7, full_precision_n_comps=4, byte_fmt=VecCompFmt.Byte_0_1)

        bones_en = extract_bitmask(0x200)
        bones_storage = VecStorage(VecCompFmt.Byte_0_255, 4) if bones_en else None

        normal_en = extract_bitmask(0x400)
        normal_storage = extract_vector_type(normal_en, 11, full_precision_n_comps=3,
                                             byte_fmt=VecCompFmt.Byte_Minus1_1)

        tangent_en = extract_bitmask(0x2000)
        # Previously this was unpacked with 0_1 because it was arbitrary data.
        # We interpret it as [-1,1] here, and assume it's always equal to the actual tangent.
        # This is usually a good assumption because basically everything needs normal maps, especially character models
        tangent_storage = extract_vector_type(tangent_en, 14, full_precision_n_comps=3,
                                              byte_fmt=VecCompFmt.Byte_Minus1_1)

        unk_en = extract_bitmask(0x0001_0000)
        unk_storage = extract_vector_type(unk_en, 17, full_precision_n_comps=3, byte_fmt=VecCompFmt.Byte_0_1)

        # TODO: Are we sure these bits aren't used for something?
        touch_bits((19, 20))

        # col0 is diffuse and opacity for GMD versions up to 0x03000B
        col0_en = extract_bitmask(0x0020_0000)
        col0_storage = extract_vector_type(col0_en, 22, full_precision_n_comps=4, byte_fmt=VecCompFmt.Byte_0_1)

        # col1 is specular for GMD versions up to 0x03000B
        col1_en = extract_bitmask(0x0100_0000)
        col1_storage = extract_vector_type(col1_en, 25, full_precision_n_comps=4, byte_fmt=VecCompFmt.Byte_0_1)

        # Extract the uv_enable and uv_count bits, to fill out the first 32 bits of the flags
        uv_en = extract_bits(27, 1)
        uv_count = extract_bits(28, 4)
        uv_storages = []
        if uv_count:
            if uv_en:
                # Iterate over all uv bits, checking for active UV slots
                for i in range(8):
                    uv_slot_bits = extract_bits(32 + (i * 4), 4)
                    if uv_slot_bits == 0xF:
                        continue

                    # format_bits is a value between 0 and 3
                    format_bits = (uv_slot_bits >> 2) & 0b11
                    if format_bits in [2, 3]:
                        uv_storages.append(VecStorage(VecCompFmt.Byte_0_1, 4))
                    else:  # format_bits are 0 or 1
                        bit_count_idx = uv_slot_bits & 0b11
                        bit_count = (2, 3, 4, 1)[bit_count_idx]

                        # Component format is float16 or float32
                        uv_comp_fmt = VecCompFmt.Float16 if format_bits else VecCompFmt.Float32

                        if bit_count == 1:
                            error.fatal(f"UV with 1 element encountered - unsure how to proceed")
                        else:
                            uv_storages.append(VecStorage(uv_comp_fmt, n_comps=bit_count))

                    if len(uv_storages) == uv_count:
                        # Touch the rest of the bits
                        touch_bits(range(32 + ((i + 1) * 4), 64))
                        break

                if len(uv_storages) != uv_count:
                    error.recoverable(
                        f"Layout Flags {vertex_packing_flags:016x} claimed to have {uv_count} UVs "
                        f"but specified {len(uv_storages)}")
            else:
                # Touch all of the uv bits, without doing anything with them
                touch_bits(range(32, 64))
                error.fatal(
                    f"Layout Flags {vertex_packing_flags:016x} claimed to have {uv_count} UVs "
                    f"but UVs are disabled")
        else:
            # No UVs at all
            touch_bits(range(32, 64))
            uv_storages = []
            pass

        # print(uv_storages)

        if checked:
            expected_touched_bits = {x for x in range(64)}
            if touched_packing_bits != expected_touched_bits:
                error.recoverable(
                    f"Incomplete vertex format parse - "
                    f"bits {expected_touched_bits - touched_packing_bits} were not touched")

        error.debug("BYTES", f"packing-flags: {vertex_packing_flags:x}")

        return GMDVertexBufferLayout.make_vertex_buffer_layout(
            assume_skinned=assume_skinned,

            pos_storage=pos_storage,
            weights_storage=weights_storage,
            bones_storage=bones_storage,
            normal_storage=normal_storage,
            tangent_storage=tangent_storage,
            unk_storage=unk_storage,
            col0_storage=col0_storage,
            col1_storage=col1_storage,
            uv_storages=uv_storages,

            packing_flags=vertex_packing_flags,
        )

    @staticmethod
    def make_vertex_buffer_layout(
            assume_skinned: bool,

            pos_storage: VecStorage,
            weights_storage: Optional[VecStorage],
            bones_storage: Optional[VecStorage],
            normal_storage: Optional[VecStorage],
            tangent_storage: Optional[VecStorage],
            unk_storage: Optional[VecStorage],
            col0_storage: Optional[VecStorage],
            col1_storage: Optional[VecStorage],
            uv_storages: List[VecStorage],

            packing_flags: int,
    ):

        return GMDVertexBufferLayout(
            assume_skinned=assume_skinned,

            pos_unpacker=make_vector_unpacker(pos_storage),
            weights_unpacker=make_vector_unpacker(weights_storage),
            bones_unpacker=make_vector_unpacker(bones_storage),
            normal_unpacker=make_vector_unpacker(normal_storage),
            tangent_unpacker=make_vector_unpacker(tangent_storage),
            unk_unpacker=make_vector_unpacker(unk_storage),
            col0_unpacker=make_vector_unpacker(col0_storage),
            col1_unpacker=make_vector_unpacker(col1_storage),
            uv_unpackers=tuple([make_vector_unpacker(s) for s in uv_storages]),

            pos_storage=pos_storage,
            weights_storage=weights_storage,
            bones_storage=bones_storage,
            normal_storage=normal_storage,
            tangent_storage=tangent_storage,
            unk_storage=unk_storage,
            col0_storage=col0_storage,
            col1_storage=col1_storage,
            uv_storages=tuple(uv_storages),

            packing_flags=packing_flags,
        )

    def numpy_dtype(self, big_endian: bool) -> np.dtype:
        names = ["pos"]
        formats = [self.pos_storage.numpy_native_dtype(big_endian)]
        offsets = [0]
        curr_offset = self.pos_storage.size_bytes()

        def register_storage(name: str, storage: Optional[VecStorage]):
            nonlocal curr_offset
            if storage:
                names.append(name)
                formats.append(storage.numpy_native_dtype(big_endian))
                offsets.append(curr_offset)
                curr_offset += storage.size_bytes()

        register_storage("weights", self.weights_storage)
        register_storage("bones", self.bones_storage)
        register_storage("normal", self.normal_storage)
        register_storage("tangent", self.tangent_storage)
        register_storage("unk", self.unk_storage)
        register_storage("col0", self.col0_storage)
        register_storage("col1", self.col1_storage)
        for i, uv_storage in enumerate(self.uv_storages):
            register_storage(f"uv{i}", uv_storage)

        return np.dtype({
            "names": names,
            "formats": formats,
            "offsets": offsets
        })

    def bytes_per_vertex(self) -> int:
        return self.numpy_dtype(False).itemsize

    def unpack_from(self, big_endian: bool, vertex_count: int,
                    data: bytes, offset: int) -> Tuple[GMDVertexBuffer_Generic, int]:
        numpy_dtype = self.numpy_dtype(big_endian)
        vertices_np = np.frombuffer(data, numpy_dtype, count=vertex_count, offset=offset)
        offset += vertex_count * numpy_dtype.itemsize

        def transform_storage_array(name: str, storage: Optional[VecStorage]):
            nonlocal vertices_np
            if storage is None:
                return None
            return storage.transform_native_fmt_array(vertices_np[name])

        vertices: GMDVertexBuffer_Generic = GMDVertexBuffer_Generic(
            layout=self,

            pos=self.pos_storage.transform_native_fmt_array(vertices_np["pos"]),
            weight_data=transform_storage_array("weights", self.weights_storage),
            bone_data=transform_storage_array("bones", self.bones_storage),
            normal=transform_storage_array("normal", self.normal_storage),
            tangent=transform_storage_array("tangent", self.tangent_storage),
            unk=transform_storage_array("unk", self.unk_storage),
            col0=transform_storage_array("col0", self.col0_storage),
            col1=transform_storage_array("col1", self.col1_storage),
            uvs=[
                transform_storage_array(f"uv{i}", s)
                for (i, s) in enumerate(self.uv_storages)
            ]
        )

        return vertices, offset

    def pack_into(self, big_endian: bool, vertices: GMDVertexBuffer_Generic, append_to: bytearray):
        # TODO: Validate that all ranges exist for what we want
        # TODO: Fill in default data if stuff is missing?

        for i in range(vertices.vertex_count()):
            self.pos_unpacker.pack(big_endian, vertices.pos[i], append_to=append_to)
            if self.weights_unpacker:
                self.weights_unpacker.pack(big_endian, vertices.weight_data[i], append_to=append_to)
            if self.bones_unpacker:
                self.bones_unpacker.pack(big_endian, vertices.bone_data[i], append_to=append_to)
            if self.normal_unpacker:
                self.normal_unpacker.pack(big_endian, vertices.normal[i], append_to=append_to)
            if self.tangent_unpacker:
                self.tangent_unpacker.pack(big_endian, vertices.tangent[i], append_to=append_to)
            if self.unk_unpacker:
                self.unk_unpacker.pack(big_endian, vertices.unk[i], append_to=append_to)
            if self.col0_unpacker:
                self.col0_unpacker.pack(big_endian, vertices.col0[i], append_to=append_to)
            if self.col1_unpacker:
                self.col1_unpacker.pack(big_endian, vertices.col1[i], append_to=append_to)
            for uv_data, uv_packer in zip(vertices.uvs, self.uv_unpackers):
                uv_packer.pack(big_endian, uv_data[i], append_to=append_to)


# Shaders are external dependencies, so they are frozen. You can't change the name of a shader, for example.
@dataclass(frozen=True)
class GMDShader:
    name: str
    vertex_buffer_layout: GMDVertexBufferLayout
    assume_skinned: bool
