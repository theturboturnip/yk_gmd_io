from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, List, Sized, Iterable

from mathutils import Vector
from yk_gmd_blender.structurelib.base import FixedSizeArrayUnpacker, ValueAdaptor, BaseUnpacker
from yk_gmd_blender.structurelib.primitives import c_float32, c_float16, c_unorm8, c_uint8, RangeConverterPrimitive
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter
from yk_gmd_blender.yk_gmd.v2.structure.common.vector import Vec3Unpacker_of, Vec4Unpacker_of


# TODO: Rename to HLSL-style (ubyte4, float2, float3, float4, half2 etc.)
class VecStorage(Enum):
    Vec4Fixed = 1
    Vec2Full = 2
    Vec3Full = 3
    Vec4Full = 4
    Vec2Half = 5
    Vec3Half = 6
    Vec4Half = 7

    @staticmethod
    def component_count(val: 'VecStorage'):
        if val in [VecStorage.Vec4Half, VecStorage.Vec4Fixed, VecStorage.Vec4Full]:
            return 4
        elif val in [VecStorage.Vec3Half, VecStorage.Vec3Full]:
            return 3
        else:
            return 2


class FixedConvertMethod(Enum):
    To0_1 = 0
    ToMinus1_1 = 1
    ToByte = 2


vector_unpackers = {
    VecStorage.Vec2Full: ValueAdaptor(Vector, base_unpacker=FixedSizeArrayUnpacker(c_float32, 2), forwards=Vector,
                                      backwards=list),
    VecStorage.Vec3Full: Vec3Unpacker_of(c_float32),
    VecStorage.Vec4Full: Vec4Unpacker_of(c_float32),

    VecStorage.Vec2Half: ValueAdaptor(Vector, base_unpacker=FixedSizeArrayUnpacker(c_float16, 2), forwards=Vector,
                                      backwards=list),
    VecStorage.Vec3Half: Vec3Unpacker_of(c_float16),
    VecStorage.Vec4Half: Vec4Unpacker_of(c_float16),
}

vec4fixed_unpackers = {
    FixedConvertMethod.To0_1: Vec4Unpacker_of(c_unorm8),
    FixedConvertMethod.ToMinus1_1: Vec4Unpacker_of(
        RangeConverterPrimitive(base_unpack=c_uint8, from_range=(0, 255), to_range=(-1.0, 1.0))),
    # We store bone_data in a Vector, which stores components as floats
    # Just using Vec4Unpacker_of(c_uint8) requires the incoming data to be int
    # Instead, use an identity RangeConverterPrimitive to convert it to float without changing the underlying value.
    # Can still be cast to int if needed, as in BoneWeight.
    FixedConvertMethod.ToByte: Vec4Unpacker_of(
        RangeConverterPrimitive(base_unpack=c_uint8, from_range=(0, 255), to_range=(0., 255.0)))
}


def make_vector_unpacker(vec_type: VecStorage, byte_convert: Optional[FixedConvertMethod] = None) \
        -> BaseUnpacker[Vector]:
    if vec_type == VecStorage.Vec4Fixed:
        if not byte_convert:
            print(f"Field had vec_type = Vec4Fixed but gave no byte_convert, assuming ToByte")
            byte_convert = FixedConvertMethod.ToByte
        return vec4fixed_unpackers[byte_convert]
    else:
        return vector_unpackers[vec_type]


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

    pos: List[Vector]
    weight_data: Optional[List[Vector]]
    bone_data: Optional[List[Vector]]
    normal: Optional[List[Vector]]
    tangent: Optional[List[Vector]]
    unk: Optional[List[Vector]]
    col0: Optional[List[Vector]]
    col1: Optional[List[Vector]]
    uvs: List[List[Vector]]

    @staticmethod
    def build_empty(layout: 'GMDVertexBufferLayout', count: int):
        # TODO: Right now, this pre-allocates lists of None-s which are filled in with Vector-s later.
        # This prevents constant re-allocating when we grow the list.
        # This is still inefficient tho, as each Vector we create is a heap allocation (potentially with a C FFI?)
        # Unfortunately, because we're using the super-generic unpacking setup we can't resolve this easily.
        # This should be changed to use numpy or similar for a big performance boost, but this is out-of-scope for now.
        alloc_for_type = lambda field_type: [None] * count if field_type else None
        return GMDVertexBuffer_Generic(
            layout=layout,

            pos=[None] * count,

            weight_data=alloc_for_type(layout.weights_unpacker),
            bone_data=alloc_for_type(layout.bones_unpacker),
            normal=alloc_for_type(layout.normal_unpacker),
            tangent=alloc_for_type(layout.tangent_unpacker),
            unk=alloc_for_type(layout.unk_unpacker),
            col0=alloc_for_type(layout.col0_unpacker),
            col1=alloc_for_type(layout.col1_unpacker),
            uvs=[
                [None] * count
                for t in layout.uv_unpackers
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

        self.pos = []
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
    weight_data: List[Vector]
    bone_data: List[Vector]

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

    def __post_init__(self):
        if not self.pos_unpacker:
            raise TypeError(f"VertexBufferLayout claims to not have vertex positions!")

    def __str__(self):
        return f"GMDVertexBufferLayout(\n" \
               f"assume_skinned: {self.assume_skinned},\n" \
               f"packing_flags: {self.packing_flags:x},\n" \
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
            touched_packing_bits = set()

            def touch_bits(bit_indices: Iterable[int]):
                touched_bits = set(bit_indices)
                if touched_bits.intersection(touched_packing_bits):
                    error.recoverable(f"Retouching bits {touched_bits.intersection(touched_packing_bits)}")
                touched_packing_bits.update(touched_bits)
        else:
            def touch_bits(bit_indices: Iterable[int]):
                pass

        def extract_bits(start, length):
            touch_bits(range(start, start + length))

            # Extract bits by shifting down to start and generating a mask of `length` 1's in binary
            return (vertex_packing_flags >> start) & int('1' * length, 2)

        def extract_bitmask(bitmask):
            touch_bits([i for i in range(32) if ((bitmask >> i) & 1)])

            return vertex_packing_flags & bitmask

        def extract_vector_type(en: bool, start: int, expected_full_precision: VecStorage) -> Optional[VecStorage]:
            bits = extract_bits(start, 2)
            if en:
                if bits == 0:
                    return expected_full_precision
                elif bits == 1:
                    return VecStorage.Vec4Half
                else:
                    return VecStorage.Vec4Fixed
            else:
                return None

        # pos can be (3 or 4) * (half or full) floats
        pos_count = extract_bits(0, 3)
        pos_precision = extract_bits(3, 1)
        if pos_precision == 1:
            pos_storage = VecStorage.Vec3Half if pos_count == 3 else VecStorage.Vec4Half
        else:
            pos_storage = VecStorage.Vec3Full if pos_count == 3 else VecStorage.Vec4Full

        weight_en = extract_bitmask(0x70)
        weights_storage = extract_vector_type(weight_en, 7, expected_full_precision=VecStorage.Vec4Full)

        bones_en = extract_bitmask(0x200)
        bones_storage = VecStorage.Vec4Fixed if bones_en else None

        normal_en = extract_bitmask(0x400)
        normal_storage = extract_vector_type(normal_en, 11, expected_full_precision=VecStorage.Vec3Full)

        tangent_en = extract_bitmask(0x2000)
        tangent_storage = extract_vector_type(tangent_en, 14, expected_full_precision=VecStorage.Vec3Full)

        unk_en = extract_bitmask(0x0001_0000)
        unk_storage = extract_vector_type(unk_en, 17, expected_full_precision=VecStorage.Vec3Full)

        # TODO: Are we sure these bits aren't used for something?
        touch_bits((19, 20))

        # col0 is diffuse and opacity for GMD versions up to 0x03000B
        col0_en = extract_bitmask(0x0020_0000)
        col0_storage = extract_vector_type(col0_en, 22, expected_full_precision=VecStorage.Vec4Full)

        # col1 is specular for GMD versions up to 0x03000B
        col1_en = extract_bitmask(0x0100_0000)
        col1_storage = extract_vector_type(col1_en, 25, expected_full_precision=VecStorage.Vec4Full)

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

                    format_bits = (uv_slot_bits >> 2) & 0b11
                    if format_bits in [2, 3]:
                        # This should be formatted as a [-1, 1] range thing
                        # This is currently set in gmd_shader.py, although really it should be set in here
                        # TODO: shift make_vector_unpacker logic out of abstract/gmd_shader and into here
                        uv_storages.append(VecStorage.Vec4Fixed)
                    else:
                        bit_count_idx = uv_slot_bits & 0b11
                        bit_count = (2, 3, 4, 1)[bit_count_idx]

                        if bit_count == 1:
                            error.fatal(f"UV with 1 element encountered - unsure how to proceed")
                        elif bit_count == 2:
                            uv_storages.append(VecStorage.Vec2Half if format_bits else VecStorage.Vec2Full)
                        elif bit_count == 3:
                            uv_storages.append(VecStorage.Vec3Half if format_bits else VecStorage.Vec3Full)
                        elif bit_count == 4:
                            uv_storages.append(VecStorage.Vec4Half if format_bits else VecStorage.Vec4Full)

                    if len(uv_storages) == uv_count:
                        # Touch the rest of the bits
                        touch_bits(range(32 + ((i + 1) * 4), 64))
                        break

                if len(uv_storages) != uv_count:
                    error.recoverable(
                        f"Layout Flags {vertex_packing_flags:016x} claimed to have {uv_count} UVs but specified {len(uv_storages)}")
            else:
                # Touch all of the uv bits, without doing anything with them
                touch_bits(range(32, 64))
                # TODO: Raise here? This is an unknown item
                uv_storages = [VecStorage.Vec2Full] * uv_count
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
            weights_unpacker=make_vector_unpacker(weights_storage,
                                                  FixedConvertMethod.To0_1) if weights_storage else None,
            bones_unpacker=make_vector_unpacker(bones_storage, FixedConvertMethod.ToByte) if bones_storage else None,
            normal_unpacker=make_vector_unpacker(normal_storage,
                                                 FixedConvertMethod.ToMinus1_1) if normal_storage else None,
            # Previously this was unpacked with 0_1 because it was arbitrary data.
            # We interpret it as [-1,1] here, and assume it's always equal to the actual tangent.
            # This is usually a good assumption because basically everything needs normal maps, especially character models
            tangent_unpacker=make_vector_unpacker(tangent_storage,
                                                  FixedConvertMethod.ToMinus1_1) if tangent_storage else None,
            unk_unpacker=make_vector_unpacker(unk_storage) if unk_storage else None,
            col0_unpacker=make_vector_unpacker(col0_storage, FixedConvertMethod.To0_1) if col0_storage else None,
            col1_unpacker=make_vector_unpacker(col1_storage, FixedConvertMethod.To0_1) if col1_storage else None,
            uv_unpackers=tuple([make_vector_unpacker(s, FixedConvertMethod.To0_1) for s in uv_storages]),

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

    def bytes_per_vertex(self) -> int:
        size = 0
        size += self.pos_unpacker.sizeof()
        if self.weights_unpacker:
            size += self.weights_unpacker.sizeof()
        if self.bones_unpacker:
            size += self.bones_unpacker.sizeof()
        if self.normal_unpacker:
            size += self.normal_unpacker.sizeof()
        if self.tangent_unpacker:
            size += self.tangent_unpacker.sizeof()
        if self.unk_unpacker:
            size += self.unk_unpacker.sizeof()
        if self.col0_unpacker:
            size += self.col0_unpacker.sizeof()
        if self.col1_unpacker:
            size += self.col1_unpacker.sizeof()
        for uv_unpacker in self.uv_unpackers:
            size += uv_unpacker.sizeof()
        return size

    def unpack_from(self, big_endian: bool, vertex_count: int,
                    data: bytes, offset: int) -> Tuple[GMDVertexBuffer_Generic, int]:
        vertices: GMDVertexBuffer_Generic = GMDVertexBuffer_Generic.build_empty(self, vertex_count)

        for i in range(vertex_count):
            # unpack() returns the unpacked value and offset + size, so incrementing offset is done in one line
            vertices.pos[i], offset = self.pos_unpacker.unpack(big_endian, data, offset)
            if self.weights_unpacker:
                vertices.weight_data[i], offset = self.weights_unpacker.unpack(big_endian, data, offset)
            if self.bones_unpacker:
                vertices.bone_data[i], offset = self.bones_unpacker.unpack(big_endian, data, offset)
            if self.normal_unpacker:
                vertices.normal[i], offset = self.normal_unpacker.unpack(big_endian, data, offset)
            if self.tangent_unpacker:
                vertices.tangent[i], offset = self.tangent_unpacker.unpack(big_endian, data, offset)
            if self.unk_unpacker:
                vertices.unk[i], offset = self.unk_unpacker.unpack(big_endian, data, offset)
            if self.col0_unpacker:
                vertices.col0[i], offset = self.col0_unpacker.unpack(big_endian, data, offset)
            if self.col1_unpacker:
                vertices.col1[i], offset = self.col1_unpacker.unpack(big_endian, data, offset)
            for uv_idx, uv_unpacker in enumerate(self.uv_unpackers):
                vertices.uvs[uv_idx][i], offset = uv_unpacker.unpack(big_endian, data, offset)

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
