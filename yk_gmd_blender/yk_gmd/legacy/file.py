import collections
import ctypes
import struct
from typing import List, Generic, TypeVar, Type, Dict, Tuple, Set

from yk_gmd_blender.yk_gmd.legacy.abstract.bone import GMDBone
from yk_gmd_blender.yk_gmd.legacy.abstract.material import GMDMaterial, GMDMaterialTextureIndex
from yk_gmd_blender.yk_gmd.legacy.abstract.submesh import GMDSubmesh, GMDPart
from yk_gmd_blender.yk_gmd.legacy.abstract.vector import Vec3, Quat, Vec4
from yk_gmd_blender.yk_gmd.legacy.abstract.vertices import GMDVertexBuffer, GMDVertexBufferLayout, GMDVertex, BoneWeight
from yk_gmd_blender.yk_gmd.legacy.structs import *
from .structs.submesh import IndicesStruct
from .structs.transform_12float import Transform12Float
from .structs.varlen_data_array_ptr import VarLenDataArrayPtrStruct
from yk_gmd_blender.yk_gmd.legacy.util import false_ranges_in

T = TypeVar('T')

# TODO: Refactor GMDArray/GMDVarLenArray and ArrayPtrStruct/VarLenDataArrayPtrStruct to two classes
# There should be one class for packing an array and making the pointer to that.
# A generic DataPtrCntStruct with alternate unpack/pack fields to be subclassed
# so then you have FixedLenArrayPtrStruct = DataPtrCntStruct that un/packs fixed length
# and VarLenArrayPtrStruct that un/packs fixed length
# Then you could just store the actual data as Lists and let the packing do the work?
class GMDArray(Generic[T]):
    items: List[T]

    def __init__(self, items: List[T]):
        self.items = items

    def elem_type(self) -> Type:
        return type(self.items[0])

    def get_bytes(self) -> bytes:
        bs = bytearray()
        for item in self.items:
            bs += bytes(item)
        return bytes(bs)

    def get_pointer(self, address) -> ArrayPtrStruct:
        return array_pointer_of(type(self.items[0]))(address, len(self.items))

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, item) -> T:
        return self.items[item]

    #def __setitem__(self, key, value):
    #    if not isinstance(value, type(self.items[0])):
    #        raise TypeError(f"Tried to put {type(value)} in GMDArray of {type(self.items[0])}")
    #    self.items[key] = value


class GMDVarLenArray(GMDArray[bytes]):
    def get_bytes(self):
        bs = bytearray()
        for item in self.items:
            if len(item) > 255:
                raise ValueError("Can't have a string > 255 bytes inside a variable length array!")
            bs += bytes([len(item)])
            bs += item
        # TODO: pad to 0x100 with zeroes for safety? some readers may be null-terminated?
        return bytes(bs)

    def get_pointer(self, address):
        return VarLenDataArrayPtrStruct.from_data(address, len(self.get_bytes()))

    def item_starting_at(self, start_addr:int):
        curr_addr = 0
        idx = 0
        while curr_addr < start_addr and idx < len(self.items):
            curr_addr += len(self.items[idx]) + 1
            idx += 1
        if curr_addr != start_addr:
            raise ValueError(f"This array doesn't contain a bytestring starting at {start_addr}")
        return self.items[idx]


class GMDStructs:
    # Header Components
    magic_str: str = "GSGM"
    endian_check: ctypes.c_uint32
    version_flags_maybe: ctypes.c_uint32
    name: str
    bbox_maybe: Transform12Float
    finish: ctypes.c_float * 6

    # File data components
    bones: GMDArray[BoneStruct]
    parts: GMDArray[PartStruct]
    submeshes: GMDArray[SubmeshStruct]
    materials: GMDArray[MaterialStruct]
    matrices: GMDArray[MatrixStruct]
    vertex_buffer_layouts: GMDArray[VertexBufferLayoutStruct]

    vertex_data: GMDArray[ctypes.c_uint8]
    index_data: GMDArray[ctypes.c_uint16]

    texture_names: GMDArray[IdStringStruct]
    shader_names: GMDArray[IdStringStruct]
    bone_names: GMDArray[IdStringStruct]

    unk5: GMDArray[Unk5]
    unk10: GMDArray[ctypes.c_uint8]
    submesh_bone_lists: GMDVarLenArray
    unk12: GMDArray[Unk12]
    unk13: GMDArray[Unk13]
    unk14: GMDArray[Unk14]

    def __init__(self,
                 endian_check: ctypes.c_uint32,
                 version_flags_maybe: ctypes.c_uint32,

                 name: str,
                 bbox_maybe: Transform12Float,
                 finish: ctypes.c_float * 6,

                 # File data components
                 bones: List[BoneStruct],
                 parts: List[PartStruct],
                 submeshes: List[SubmeshStruct],
                 materials: List[MaterialStruct],
                 matrices: List[MatrixStruct],
                 vertex_buffer_layouts: List[VertexBufferLayoutStruct],

                 vertex_data: List[ctypes.c_uint8],
                 index_data: List[ctypes.c_uint16],

                 texture_names: List[IdStringStruct],
                 shader_names: List[IdStringStruct],
                 bone_names: List[IdStringStruct],

                 unk5: List[Unk5],
                 unk10: List[ctypes.c_uint8],
                 submesh_bone_lists: List[bytes],
                 unk12: List[Unk12],
                 unk13: List[Unk13],
                 unk14: List[Unk14],
                 ):
        self.endian_check = endian_check
        self.version_flags_maybe = version_flags_maybe
        self.name = name
        self.bbox_maybe = bbox_maybe
        self.finish = finish

        # File data components
        self.bones = GMDArray[BoneStruct](bones)
        self.parts = GMDArray[PartStruct](parts)
        self.submeshes = GMDArray[SubmeshStruct](submeshes)
        self.materials = GMDArray[MaterialStruct](materials)
        self.matrices = GMDArray[MatrixStruct](matrices)
        self.vertex_buffer_layouts = GMDArray[VertexBufferLayoutStruct](vertex_buffer_layouts)

        self.vertex_data = GMDArray[ctypes.c_uint8](vertex_data)
        self.index_data = GMDArray[ctypes.c_uint16](index_data)

        self.texture_names = GMDArray[IdStringStruct](texture_names)
        self.shader_names = GMDArray[IdStringStruct](shader_names)
        self.bone_names = GMDArray[IdStringStruct](bone_names)

        self.unk5 = GMDArray[Unk5](unk5)
        self.unk10 = GMDArray[ctypes.c_uint8](unk10)
        self.submesh_bone_lists = GMDVarLenArray(submesh_bone_lists)
        self.unk12 = GMDArray[Unk12](unk12)
        self.unk13 = GMDArray[Unk13](unk13)
        self.unk14 = GMDArray[Unk14](unk14)

    def make_bytes(self) -> bytes:
        # Mapping of "name in header field" to data
        data_segments: Dict[str, GMDArray] = {
            "bones": self.bones,
            "parts": self.parts,
            "submeshes": self.submeshes,
            "materials": self.materials,
            "matrices": self.matrices,
            "vertex_buffer_layouts": self.vertex_buffer_layouts,

            "vertex_data": self.vertex_data,
            "index_data": self.index_data,

            "texture_names": self.texture_names,
            "shader_names": self.shader_names,
            "bone_names": self.bone_names,

            "unk5": self.unk5,
            "unk10": self.unk10,
            "submesh_bone_lists": self.submesh_bone_lists,
            "unk12": self.unk12,
            "unk13": self.unk13,
            "unk14": self.unk14,
        }

        # Build up the bytes in the data segment of the file, and find the pointers
        data_pointers: Dict[str, ArrayPtrStruct] = {}
        segment_bytes = bytearray()
        # Start at the end of the header
        current_size = ctypes.sizeof(HeaderStruct)
        for (field, data_array) in data_segments.items():
            data_pointers[field] = data_array.get_pointer(current_size)
            data_bytes = data_array.get_bytes()
            segment_bytes += data_bytes
            current_size += len(data_bytes)

        # pad the length out to a multiple of 0x1000
        final_length = (((current_size // 0x1000) + 1) * 0x1000)
        padding_length = final_length - current_size
        segment_bytes += b'\0' * padding_length

        # Make the header
        header = HeaderStruct()
        header.magic_str = self.magic_str.encode('ascii')
        header.endian_check = self.endian_check
        header.version_flags_maybe = self.version_flags_maybe
        header.file_size = final_length

        header.name_checksum = sum(self.name.encode('ascii'))
        header.name = self.name.encode('ascii')

        header.bbox_maybe = self.bbox_maybe
        header.finish = self.finish

        for (field, data_ptr) in data_pointers.items():
            header.set_field(field, data_ptr)

        segment_bytes[0:0] = bytes(header)
        return bytes(segment_bytes)


class GMDFile:
    data: bytes
    header: HeaderStruct
    structs: GMDStructs

    def __init__(self, data: bytes):
        self.data = data
        self.header = HeaderStruct.from_buffer_copy(self.data, 0)

        self.structs = GMDStructs(
            self.header.endian_check,
            self.header.version_flags_maybe,
            self.header.name.decode('ascii'),
            self.header.overall_bbox,
            self.header.finish,

            self.header.bones.extract(self.data),
            self.header.parts.extract(self.data),
            self.header.submeshes.extract(self.data),
            self.header.materials.extract(self.data),
            self.header.matrices.extract(self.data),
            self.header.vertex_buffer_layouts.extract(self.data),

            self.header.vertex_data.extract(self.data),
            self.header.index_data.extract(self.data),

            self.header.texture_names.extract(self.data),
            self.header.shader_names.extract(self.data),
            self.header.bone_names.extract(self.data),

            self.header.unk5.extract(self.data),
            self.header.unk10.extract(self.data),
            self.header.submesh_bone_lists.extract_strings(self.data),
            self.header.unk12.extract(self.data),
            self.header.unk13.extract(self.data),
            self.header.unk14.extract(self.data),
        )

        # This is actually in arrays of 4 bigendian-uint16_t, but the top bytes are usually 0
        self.part_unk10_bytechunks = []
        for start,end in zip([p.unk3 for p in self.structs.parts], [p.unk3 for p in self.structs.parts[1:]] + [self.header.unk10.cnt]):
            self.part_unk10_bytechunks.append([x.value for x in self.structs.unk10[start+1:end:2]])
        #self.unk10_ints = [x.value for x in self.structs.unk10]
        #self.unk10_chunks = [[x.value for x in self.structs.unk10[i*8+1:i*8+8:2]] for i in range(len(self.structs.parts))]

        #self.analyse_coverage()

    def analyse_coverage(self):
        coverage = [False] * len(self.data)
        coverage[0:ctypes.sizeof(HeaderStruct)] = [True] * ctypes.sizeof(HeaderStruct)
        for (name, f) in self.header._fields_:
            array_ptr = getattr(self.header, name)
            if isinstance(array_ptr, ArrayPtrStruct):
                if array_ptr.elem_type is not None:
                    length = array_ptr.cnt * ctypes.sizeof(array_ptr.elem_type)
                else:
                    length = array_ptr.cnt
                coverage[array_ptr.ptr:array_ptr.ptr + length] = [True] * (length)

        untouched_ranges = false_ranges_in(coverage)
        for (ra, rb) in untouched_ranges:
            print(f"[0x{ra:06x}...0x{rb:06x})")

        uncovered = set()
        for (covered, val) in zip(coverage, self.data):
            if not covered:
                uncovered.add(val)
        print(f"Values in uncovered areas: {uncovered}")


class GMDFileIOAbstraction:
    _bone_roots: List[GMDBone]
    _bone_map: Dict[int, GMDBone]
    _bone_name_map: Dict[str, GMDBone]
    _vertex_buffers: List[GMDVertexBuffer]
    _vertex_buffer_layouts: Dict[GMDVertexBufferLayout, VertexBufferLayoutStruct]
    _submeshes: List[GMDSubmesh]
    _parts: List[GMDPart]
    _materials: List[GMDMaterial]

    @property
    def bone_roots(self) -> List[GMDBone]:
        return self._bone_roots[:]
    #def update_bone_transform(self, pos: Vec3, rot: Quat, scl: Vec3, matrix: Optional[Mat4]):
    #    # TODO: autocalculate the matrix?
    #    raise NotImplementedError("Should be implemented but isn't yet")
    #    pass

    @property
    def bones_in_order(self) -> List[GMDBone]:
        return sorted(self._bone_map.values(), key= lambda b: b.id)

    def bone_id_from_name(self, name: str) -> int:
        return self._bone_name_map[name].id

    @property
    def materials(self) -> List[GMDMaterial]:
        return self._materials[:]

    @property
    def submeshes(self) -> List[GMDSubmesh]:
       return self._submeshes[:]
    @submeshes.setter
    def submeshes(self, submeshes: List[GMDSubmesh]):
       self._submeshes = submeshes

    @property
    def texture_names(self):
        return self._texture_names[:]
    @texture_names.setter
    def texture_names(self, new_texture_names):
        self._texture_names = new_texture_names
    # @property
    # def parts(self) -> List[GMDPart]:
    #     return self._parts[:]
    # @parts.setter
    # def parts(self, new_parts: List[GMDPart]):
    #     # TODO: Check if materials used are in our _materials list?
    #     new_submeshes = sum([p.submeshes for p in new_parts], [])
    #     self._parts = new_parts
    #     self._submeshes = new_submeshes

    @property
    def name(self):
        return self.structs.name

    def __init__(self, structs: GMDStructs):
        self.structs = structs

        self.build_abstract_bone_hierarchy()
        self.build_abstract_vertex_buffers()
        self.build_abstract_materials()
        self.build_abstract_parts_and_submeshes()
        self._texture_names = [t.text for t in self.structs.texture_names]

        #self.unk10_strs = self.header.unk10.extract_strings(self.data)
        #self.submesh_bone_lists = self.header.submesh_bone_lists.extract_strings(self.data)

    def repack_into_bytes(self) -> bytes:
        # Update bone hierarchy values
        # for (id, bone) in self._bone_map.items():
        #     self.structs.bones[id].pos[:] = [bone.pos.x, bone.pos.y, bone.pos.z, 0]
        #     self.structs.bones[id].rot[:] = [bone.rot.x, bone.rot.y, bone.rot.z, bone.rot.w]
        #     self.structs.bones[id].scl[:] = [bone.scl.x, bone.scl.y, bone.scl.z, 0]
        #
        #     #if self.structs.bones[id].matrix_id_maybe < len(self.structs.matrices):
        #     #    self.structs.matrices[self.structs.bones[id].matrix_id_maybe].set_from_mat4(bone.matrix_world_to_local)
        #     pass

        # total_parts = self._parts[:]
        total_submeshes = self._submeshes[:]

        # Add a null submesh for each material so each material is used
        null_part = GMDPart(
            name="Null",
            submeshes=[]
        )
        v = GMDVertex()
        v.pos = Vec3(0,0,0)
        v.normal = v.tangent = Vec4(0,0,0,1)
        v.uv = (0,0)
        v.col0 = Vec4(0,0,0,0)
        v.col1 = Vec4(0,0,0,0)
        v.weights = (
            BoneWeight(bone=0, weight=1.0),
            BoneWeight(bone=0, weight=0.0),
            BoneWeight(bone=0, weight=0.0),
            BoneWeight(bone=0, weight=0.0),
        )
        for material in self._materials:
            if len([s for s in total_submeshes if s.material.id == material.id]) > 0:
                # A submesh already exists for this, so don't make a new one
                continue
                #pass
            sm = GMDSubmesh(
                material=material,
                relevant_bones=[0],
                vertices=[v,v,v],
                triangle_indices=[0,1,2],
                triangle_strip_indices1=[0,1,2],
                triangle_strip_indices2=[0,1,2],
                #parent_part=null_part
            )
            null_part.submeshes.append(sm)
            total_submeshes.append(sm)

        # TODO: Check sort order for when multiple layouts are present - vertex buffers should be arranged according to material layout.
        list.sort(total_submeshes, key=lambda s: s.material.id)

        # Update Part buffers
        # bone_structs = [b for b in self.structs.bones if b.part_id_maybe == -1]
        # part_structs = []
        # for part in total_parts:
        #     part_struct = PartStruct()
        #     part_struct.id =

        # Update Vertex/Index Buffers
        # Sort the submeshes by vertex buffer layouts
        vb_layouts: Set[GMDVertexBufferLayout] = {s.material.vertex_buffer_layout for s in total_submeshes}
        vb_layout_submeshes: List[Tuple[GMDVertexBufferLayout, List[GMDSubmesh]]] = []
        for layout in vb_layouts:
            vb_submeshes = [s for s in total_submeshes if s.material.vertex_buffer_layout == layout]
            vb_layout_submeshes.append((layout, vb_submeshes))
            pass

        vertex_buffer_layout_structs: List[VertexBufferLayoutStruct] = []
        overall_vertex_buffer_data = bytearray()
        overall_index_buffer_data: List[int] = []
        submesh_structs: List[SubmeshStruct] = []
        submesh_bonelists: List[bytes] = []

        # TODO: Find a better way to load/store indices as reversed endian
        reverse_endian = lambda x: ((x&0xFF) << 8) | ((x>>8)&0xFF)

        for (layout, vb_submeshes) in vb_layout_submeshes:
            # Create a copy of the correct layout structure, in case we've reordered it or something
            layout_struct = VertexBufferLayoutStruct.from_buffer_copy(bytes(self._vertex_buffer_layouts[layout]))
            layout_struct.id = len(vertex_buffer_layout_structs)
            layout_struct.vertex_count = sum(len(s.vertices) for s in vb_submeshes)
            layout_struct.vertex_data_start = len(overall_vertex_buffer_data)
            layout_struct.vertex_data_length = layout_struct.vertex_count * layout_struct.bytes_per_vertex
            vertex_buffer_layout_structs.append(layout_struct)

            vertex_buffer_data = bytearray()
            current_vertex_count = 0

            for s in vb_submeshes:
                submesh_struct = SubmeshStruct()
                submesh_struct.id = len(submesh_structs)
                submesh_struct.material_id = s.material.id
                submesh_struct.vertex_buffer_id = layout_struct.id
                submesh_struct.vertex_count = len(s.vertices)

                # Set up the pointer for the next set of vertices
                submesh_struct.vertex_start = current_vertex_count
                # then add the data
                vertex_buffer_data += layout.pack_vertices(s.vertices)
                current_vertex_count += len(s.vertices)

                pack_index = lambda x:0xFFFF if x == 0xFFFF else reverse_endian(x + submesh_struct.vertex_start)

                # Set up the pointer for the next set of indices
                submesh_struct.indices_triangle = IndicesStruct()
                submesh_struct.indices_triangle.index_cnt = len(s.triangle_indices)
                submesh_struct.indices_triangle.index_start = len(overall_index_buffer_data)
                # then add them to the data
                overall_index_buffer_data += [pack_index(x) for x in s.triangle_indices]

                # Set up the pointer for the next set of indices
                submesh_struct.indices_trianglestrip_1 = IndicesStruct()
                submesh_struct.indices_trianglestrip_1.index_cnt = len(s.triangle_strip_indices1)
                submesh_struct.indices_trianglestrip_1.index_start = len(overall_index_buffer_data)
                # then add them to the data
                overall_index_buffer_data += [pack_index(x) for x in s.triangle_strip_indices1]

                # Set up the pointer for the next set of indices
                submesh_struct.indices_trianglestrip_2 = IndicesStruct()
                submesh_struct.indices_trianglestrip_2.index_cnt = len(s.triangle_strip_indices2)
                submesh_struct.indices_trianglestrip_2.index_start = len(overall_index_buffer_data)
                # then add them to the data
                overall_index_buffer_data += [pack_index(x) for x in s.triangle_strip_indices2]

                # Set up the pointer for the next list of bones
                submesh_struct.bonelist_length = len(s.relevant_bones)
                submesh_struct.bonelist_start = sum(len(x)+1 for x in submesh_bonelists)
                # then add them to the data
                # TODO: Check that at least one bone is assigned?
                # TODO: The actual engine reuses strings, that might be cool here?
                submesh_bonelists.append(bytes(s.relevant_bones))

                # TODO: This isn't technically right, but it doesn't destroy anything?
                submesh_struct.linked_l0_bone_maybe = 126
                submesh_struct.linked_l0_number_maybe = 0

                submesh_struct.zero = 0

                submesh_structs.append(submesh_struct)

            overall_vertex_buffer_data += vertex_buffer_data

        # Update material structs
        for material in self.structs.materials:
            # TODO: It seems that this doesn't matter
            indices_using_mat = [i for i,s in enumerate(total_submeshes) if s.material.id == material.id]
            material.first_connected_submesh = indices_using_mat[0]
            material.num_connected_submeshes = len(indices_using_mat)
            pass

        #vertex_buffer_layout_structs: List[VertexBufferLayoutStruct] = []
        #overall_vertex_buffer_data = bytearray()
        #overall_index_buffer_data: List[int] = []
        #submesh_structs: List[SubmeshStruct] = []
        #submesh_bonelists: List[bytes] = []
        self.structs.vertex_buffer_layouts = GMDArray[VertexBufferLayoutStruct](vertex_buffer_layout_structs)
        self.structs.vertex_data = GMDArray[ctypes.c_uint8]([ctypes.c_uint8(x) for x in overall_vertex_buffer_data])
        # Find the index type because it could be big endian or little
        index_type = self.structs.index_data.elem_type()
        print(type(overall_index_buffer_data[0]))
        correctly_typed_index_data = [index_type(x) for x in overall_index_buffer_data]
        self.structs.index_data = GMDArray[ctypes.c_uint16](correctly_typed_index_data)
        self.structs.submeshes = GMDArray[SubmeshStruct](submesh_structs)
        print(sorted(self.structs.submesh_bone_lists.items))
        print(sorted(submesh_bonelists))
        self.structs.submesh_bone_lists = GMDVarLenArray(submesh_bonelists)

        # Delete all "parts" except for the first
        self.structs.parts.items = self.structs.parts.items[:1]
        # This first part will always use the first unk10 entry for draw lists, so we can replace the whole unk10 area
        # Unk10 = set of big-endian uint16s
        new_unk10 = [len(self.structs.submeshes), 0]
        for submesh_struct in self.structs.submeshes:
            new_unk10.append(submesh_struct.material_id)
            new_unk10.append(submesh_struct.id)
        new_unk10_bytes = bytearray()
        for item in new_unk10:
            new_unk10_bytes += struct.pack(">H", item)
        self.structs.unk10.items = [ctypes.c_uint8(x) for x in new_unk10_bytes]
        print(self.structs.unk10.items)

        for (i,t) in enumerate(self._texture_names):
            encoded_bytes = bytearray(t.encode("ascii"))
            if len(encoded_bytes) < 30:
                encoded_bytes += bytearray([0] * (30 - len(encoded_bytes)))
            print(encoded_bytes)
            print(bytes(encoded_bytes))
            self.structs.texture_names.items[i] = IdStringStruct()
            self.structs.texture_names.items[i].text_internal = bytes(encoded_bytes)
            print(self.structs.texture_names.items[i].text_internal)
            self.structs.texture_names.items[i].id = sum(encoded_bytes)
        print(self.structs.texture_names.items)

        # Packing into a file should
            # - Update vertex buffers
            # - Update index buffers
            # - Update vertex buffer counts etc. without changing layout
            # - Update submeshes
            # - Update submesh bone lists
            # - CANNOT update texture names - IDs are important too, and we don't know how to change them
                # TODO - ask in the discord how texture modding is usually done
            # - Update bone transforms and matrices
            # everything else should remain intact
        return self.structs.make_bytes()

    def build_abstract_materials(self):
        materials = []
        shader_vb_layouts = {}

        for material_struct in self.structs.materials:
            shader_name = self.structs.shader_names[material_struct.shader_index].text
            textures = {
                GMDMaterialTextureIndex.Diffuse: self.structs.texture_names[material_struct.texture_diffuse.tex_index].text,
                GMDMaterialTextureIndex.Normal: self.structs.texture_names[material_struct.texture_normal.tex_index].text
            }
            # To find the vertex buffer layout, check to see which submeshes use the mateiral and then see what layout is used.
            # Assumed that each shader requires a specific layout.
            if shader_name not in shader_vb_layouts:
                for submesh_struct in self.structs.submeshes:
                    if submesh_struct.material_id == material_struct.id:
                        shader_vb_layouts[shader_name] = self._vertex_buffers[submesh_struct.vertex_buffer_id].layout
            vertex_buffer_layout = shader_vb_layouts.get(shader_name, None)

            materials.append(GMDMaterial(
                id=material_struct.id,
                shader_name=shader_name,
                texture_names=textures,
                vertex_buffer_layout=vertex_buffer_layout
            ))

        self._materials = materials

    def build_abstract_parts_and_submeshes(self):
        # Build initial parts
        parts = []
        part_index_to_gmdpart = {}
        for i,part_struct in enumerate(self.structs.parts):
            name = self._bone_map[part_struct.bone_id_1].name
            submeshes = []
            part = GMDPart(
                name=name,
                submeshes=submeshes
            )
            parts.append(part)
            part_index_to_gmdpart[i] = part

        # Connect submeshes to part
        reverse_endian = lambda x: ((x&0xFF) << 8) | ((x>>8)&0xFF)
        for submesh_struct in self.structs.submeshes:
            material = self._materials[submesh_struct.material_id]
            relevant_bones = [
                int(x) for x in self.structs.submesh_bone_lists.item_starting_at(submesh_struct.bonelist_start)
            ]
            if len(relevant_bones) != submesh_struct.bonelist_length:
                pass # TODO: Raise some error about length mismatches?
            vtx_buffer = self._vertex_buffers[submesh_struct.vertex_buffer_id]
            start = submesh_struct.vertex_start
            cnt = submesh_struct.vertex_count
            vertices = vtx_buffer.vertices[start:start+cnt]

            parse_index = lambda x: 0xFFFF if x == 0xFFFF else reverse_endian(x) - start

            #print(submesh_struct.indices_triangle.extract_range(self.structs.index_data))
            triangle_indices = [parse_index(x.value) for x in submesh_struct.indices_triangle.extract_range(self.structs.index_data)]
            triangle_strip_indices1 = [parse_index(x.value) for x in submesh_struct.indices_trianglestrip_1.extract_range(self.structs.index_data)]
            triangle_strip_indices2 = [parse_index(x.value) for x in submesh_struct.indices_trianglestrip_2.extract_range(self.structs.index_data)]

            parent_part = part_index_to_gmdpart[submesh_struct.part_number]

            submesh = GMDSubmesh(
                material=material,
                relevant_bones=relevant_bones,
                vertices=vertices,
                triangle_indices=triangle_indices,
                triangle_strip_noreset_indices=triangle_strip_indices1,
                triangle_strip_reset_indices=triangle_strip_indices2,
                #parent_part=parent_part
            )

            parent_part.submeshes.append(submesh)

        # Use the setter here to set both _submeshes and _parts
        #self.parts = parts
        self._submeshes = sum((p.submeshes for p in parts), [])

    def build_abstract_bone_hierarchy(self):
        # Make hierarchy
        root_ids = []
        child_list_dict = collections.defaultdict(lambda: [])
        child_to_parent = {}#collections.defaultdict(lambda: None)
        for bone_info in self.structs.bones:
            #if bone_info.part_id != -1:
            #    continue #

            if bone_info.parent_of >= 0:
                child_list_dict[bone_info.id] = [bone_info.parent_of]
                child_to_parent[bone_info.parent_of] = bone_info.id

            if bone_info.sibling_of >= 0:
                # Look up our parent
                parent_id = child_to_parent[bone_info.id]
                # Add our sibling to the child_list_dict
                child_list_dict[parent_id].append(bone_info.sibling_of)
                # Add the mapping for our sibling to the child_to_parent mapping
                child_to_parent[bone_info.sibling_of] = parent_id

            if bone_info.id not in child_to_parent:
                root_ids.append(bone_info.id)

        # Build basic abstract bones
        abstract_bones = {}
        for bone_struct in self.structs.bones:
            name = self.structs.bone_names[bone_struct.name_string].text
            pos = Vec3(*bone_struct.pos[:3])
            rot = Quat(*bone_struct.rot[:])
            scl = Vec3(*bone_struct.scl[:3])
            #raise Exception(f"{dir(bone_struct)} {bone_struct.__class__.__name__}")
            #tail = Vec3(*bone_struct.tail[:3])# + pos
            bone = GMDBone(bone_struct.id, name, pos, rot, scl)

            # TODO: This doesn't make sense, if there's a matrix why would it have a valid ID?
            if 0 <= bone_struct.matrix_id_maybe < len(self.structs.matrices):
                bone.set_matrix(self.structs.matrices[bone_struct.matrix_id_maybe].as_mat4())

            abstract_bones[bone_struct.id] = bone

        # Attach the hierarchy data to the abstract bone
        for abstract_bone in abstract_bones.values():
            if abstract_bone.id in child_to_parent:
                abstract_parent = abstract_bones[child_to_parent[abstract_bone.id]]
            else:
                abstract_parent = None
            abstract_children = [abstract_bones[x] for x in child_list_dict[abstract_bone.id]]
            abstract_bone.set_hierarchy_props(abstract_parent, abstract_children)

        self._bone_roots = [abstract_bones[x] for x in root_ids]
        self._bone_map = abstract_bones
        self._bone_name_map = {b.name:b for b in self._bone_map.values()}

    def build_abstract_vertex_buffers(self):
        self._vertex_buffers = []
        self._vertex_buffer_layouts = {}
        vertex_bytes = self.structs.vertex_data.get_bytes()
        for layout in self.structs.vertex_buffer_layouts:
            abstract_layout = layout.get_vertex_layout()

            if abstract_layout.calc_bytes_per_vertex() != layout.bytes_per_vertex:
                print(f"BPV mismatch: {abstract_layout.calc_bytes_per_vertex()} != layout BPV {layout.bytes_per_vertex}")

            print(abstract_layout)
            if layout.vertex_count > 2 ** 20:
                print(f"Not going to try and allocate {layout.vertex_count} verts, too big")
            else:
                abstract_buffer = GMDVertexBuffer(
                    layout.id,
                    layout=abstract_layout,
                    vertices=abstract_layout.unpack_vertices(layout.vertex_count, vertex_bytes, layout.vertex_data_start),
                )
                self._vertex_buffers.append(abstract_buffer)

            if abstract_layout in self._vertex_buffer_layouts:
                raise ValueError("Found multiple layout structs that map to the same vertex layout")
            self._vertex_buffer_layouts[abstract_layout] = layout
