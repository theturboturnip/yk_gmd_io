from dataclasses import dataclass
from typing import Optional, Tuple, List, Sized, Iterable, Set

import numpy as np

from ...meshlib.vertex_buffer import VecStorage, VecCompFmt
from ..errors.error_reporter import ErrorReporter


# Generic representation of a vertex buffer, that can contain "weights" and "bones" separately.
# Some unskinned objects use the "weights" and "bones" categories for different things, which this supports.
# This class should be used for all vertex buffer manipulation,
# then exported as a GMDVertexBuffer_Skinned if used in a Skinned mesh.
@dataclass(repr=False, eq=False)
class GMDVertexBuffer(Sized):
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
        def alloc_storage(storage: Optional[VecStorage]) -> Optional[np.ndarray]:
            if storage is None:
                return None
            return storage.preallocate(count)

        return GMDVertexBuffer(
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
                s.preallocate(count)
                for s in layout.uv_storages
            ],
        )

    def vertex_count(self):
        return len(self.pos)

    def __len__(self):
        return self.vertex_count()

    def copy_scatter(self, indices: Iterable[int]) -> 'GMDVertexBuffer':
        return GMDVertexBuffer(
            layout=self.layout,

            pos=self.pos[indices, :].copy(),

            bone_data=self.bone_data[indices, :].copy() if self.bone_data is not None else None,
            weight_data=self.weight_data[indices, :].copy() if self.weight_data is not None else None,
            normal=self.normal[indices, :].copy() if self.normal is not None else None,
            tangent=self.tangent[indices, :].copy() if self.tangent is not None else None,
            unk=self.unk[indices, :].copy() if self.unk is not None else None,
            col0=self.col0[indices, :].copy() if self.col0 is not None else None,
            col1=self.col1[indices, :].copy() if self.col1 is not None else None,
            uvs=[
                uv[indices, :].copy()
                for uv in self.uvs
            ],
        )

    def copy_as_generic(self, s: slice = slice(None)) -> 'GMDVertexBuffer':
        return GMDVertexBuffer(
            layout=self.layout,

            pos=self.pos[s].copy(),

            bone_data=self.bone_data[s].copy() if self.bone_data is not None else None,
            weight_data=self.weight_data[s].copy() if self.weight_data is not None else None,
            normal=self.normal[s].copy() if self.normal is not None else None,
            tangent=self.tangent[s].copy() if self.tangent is not None else None,
            unk=self.unk[s].copy() if self.unk is not None else None,
            col0=self.col0[s].copy() if self.col0 is not None else None,
            col1=self.col1[s].copy() if self.col1 is not None else None,
            uvs=[
                uv[s].copy()
                for uv in self.uvs
            ],
        )

    def copy_as_skinned(self, s: slice = slice(None)) -> 'GMDSkinnedVertexBuffer':
        assert self.bone_data is not None
        assert self.weight_data is not None
        return GMDSkinnedVertexBuffer(
            layout=self.layout,

            pos=self.pos[s].copy(),

            bone_data=self.bone_data[s].copy(),
            weight_data=self.weight_data[s].copy(),
            normal=self.normal[s].copy() if self.normal is not None else None,
            tangent=self.tangent[s].copy() if self.tangent is not None else None,
            unk=self.unk[s].copy() if self.unk is not None else None,
            col0=self.col0[s].copy() if self.col0 is not None else None,
            col1=self.col1[s].copy() if self.col1 is not None else None,
            uvs=[
                uv[s].copy()
                for uv in self.uvs
            ],
        )


# Immutable version of GMDVertexBuffer that includes a bone_weights list
@dataclass(repr=False, eq=False)
class GMDSkinnedVertexBuffer(GMDVertexBuffer):
    # Individual bone, weight datas are still here, but must not be None
    weight_data: np.ndarray
    bone_data: np.ndarray

    @staticmethod
    def build_empty(layout: 'GMDVertexBufferLayout', count: int):
        assert layout.weights_storage is not None
        assert layout.bones_storage is not None

        as_generic = GMDVertexBuffer.build_empty(layout, count)
        assert as_generic.weight_data is not None
        assert as_generic.bone_data is not None

        return GMDSkinnedVertexBuffer(
            layout=layout,

            pos=as_generic.pos,
            weight_data=as_generic.weight_data,
            bone_data=as_generic.bone_data,
            normal=as_generic.normal,
            tangent=as_generic.tangent,
            unk=as_generic.unk,
            col0=as_generic.col0,
            col1=as_generic.col1,
            uvs=as_generic.uvs,
        )

    def copy_scatter(self, indices: Iterable[int]) -> 'GMDSkinnedVertexBuffer':
        return GMDSkinnedVertexBuffer(
            layout=self.layout,

            pos=self.pos[indices, :].copy(),

            bone_data=self.bone_data[indices, :].copy(),
            weight_data=self.weight_data[indices, :].copy(),
            normal=self.normal[indices, :].copy() if self.normal is not None else None,
            tangent=self.tangent[indices, :].copy() if self.tangent is not None else None,
            unk=self.unk[indices, :].copy() if self.unk is not None else None,
            col0=self.col0[indices, :].copy() if self.col0 is not None else None,
            col1=self.col1[indices, :].copy() if self.col1 is not None else None,
            uvs=[
                uv[indices, :].copy()
                for uv in self.uvs
            ],
        )


# VertexBufferLayouts are external dependencies (shaders have a fixed layout, which we can't control) so they are frozen
@dataclass(frozen=True, init=True)
class GMDVertexBufferLayout:
    assume_skinned: bool

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
        curr_offset = self.pos_storage.native_size_bytes()

        def register_storage(name: str, storage: Optional[VecStorage]):
            nonlocal curr_offset
            if storage:
                names.append(name)
                formats.append(storage.numpy_native_dtype(big_endian))
                offsets.append(curr_offset)
                curr_offset += storage.native_size_bytes()

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
                    data: bytes, offset: int) -> Tuple[GMDVertexBuffer, int]:
        numpy_dtype = self.numpy_dtype(big_endian)
        vertices_np = np.frombuffer(data, numpy_dtype, count=vertex_count, offset=offset)
        offset += vertex_count * numpy_dtype.itemsize

        def transform_storage_array(name: str, storage: Optional[VecStorage]):
            nonlocal vertices_np
            if storage is None:
                return None
            return storage.transform_native_fmt_array(vertices_np[name])

        vertices = GMDVertexBuffer(
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

    def pack_into(self, big_endian: bool, vertices: GMDVertexBuffer, append_to: bytearray):
        numpy_dtype = self.numpy_dtype(big_endian)
        vertices_np = np.zeros(len(vertices), numpy_dtype)

        def store_data(name: str, storage: Optional[VecStorage], data: Optional[np.ndarray]):
            nonlocal vertices_np
            if storage is None or data is None:
                if (storage is None) != (data is None):
                    print(f"Whoopsie! Tried to pack_into where field {name} had storage {storage} but data {data}")
                return None
            vertices_np[name] = storage.untransform_array(big_endian, data)

        store_data("pos", self.pos_storage, vertices.pos)
        store_data("weights", self.weights_storage, vertices.weight_data)
        store_data("bones", self.bones_storage, vertices.bone_data)
        store_data("normal", self.normal_storage, vertices.normal)
        store_data("tangent", self.tangent_storage, vertices.tangent)
        store_data("unk", self.unk_storage, vertices.unk)
        store_data("col0", self.col0_storage, vertices.col0)
        store_data("col1", self.col1_storage, vertices.col1)
        for (i, (s, d)) in enumerate(zip(self.uv_storages, vertices.uvs)):
            store_data(f"uv{i}", s, d)

        append_to += vertices_np.tobytes()


# Shaders are external dependencies, so they are frozen. You can't change the name of a shader, for example.
@dataclass(frozen=True)
class GMDShader:
    name: str
    vertex_buffer_layout: GMDVertexBufferLayout
    assume_skinned: bool
