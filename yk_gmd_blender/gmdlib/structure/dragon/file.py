from dataclasses import dataclass
from typing import List, Optional, Tuple, Union, overload, TypeVar, Type

import mathutils

from .attribute import AttributeStruct_Dragon, AttributeStruct_Dragon_Unpack
from .blendshapes import BlendshapeSpec, BlendshapeSpec_Unpack
from .header import GMDHeader_Dragon_Unpack, GMDHeader_Dragon
from ..common.array_pointer import ArrayPointerStruct
from ..common.checksum_str import ChecksumStrStruct, ChecksumStrStruct_Unpack
from ..common.file import FileData_Common, FilePacker
from ..common.matrix import MatrixUnpacker
from ..common.node import NodeStruct, NodeStruct_Unpack
from ..common.sized_pointer import SizedPointerStruct
from ..common.unks import Unk12Struct, \
    Unk14Struct, Unk12Struct_Unpack, Unk14Struct_Unpack
from ..y3.material import MaterialStruct_Y3, MaterialStruct_Y3_Unpack
from ..y3.mesh import MeshStruct_Y3, MeshStruct_Y3_Unpack
from ..y3.vertex_buffer_layout import VertexBufferLayoutStruct_Y3, VertexBufferLayoutStruct_Y3_Unpack
from ..yk1.bbox import BoundsDataStruct_YK1
from ..yk1.object import ObjectStruct_YK1, ObjectStruct_YK1_Unpack
from ....structurelib.base import BaseUnpacker, PackingValidationError
from ....structurelib.primitives import c_uint16


@dataclass(repr=False)
class FileData_Dragon(FileData_Common):
    overall_bounds: BoundsDataStruct_YK1

    node_arr: List[NodeStruct]
    obj_arr: List[ObjectStruct_YK1]
    mesh_arr: List[MeshStruct_Y3]
    attribute_arr: List[AttributeStruct_Dragon]
    material_arr: List[MaterialStruct_Y3]
    matrix_arr: List[mathutils.Matrix]
    vertex_buffer_arr: List[VertexBufferLayoutStruct_Y3]
    vertex_data: bytes  # byte data
    texture_arr: List[ChecksumStrStruct]
    shader_arr: List[ChecksumStrStruct]
    node_name_arr: List[ChecksumStrStruct]
    index_data: List[int]
    object_drawlist_bytes: bytes
    mesh_matrixlist_bytes: bytes

    unk12: List[Unk12Struct]
    unk13: List[int]
    unk14: List[Unk14Struct]
    flags: List[int]

    # This filled in by the DragonFilePacker later, but the default packers don't touch it.
    blendshape: Optional[Tuple[BlendshapeSpec, ChecksumStrStruct, bytes]] = None

    def __str__(self):
        s = "{\n"
        for f in self.header_fields_to_copy():
            s += f"\t{f} = {getattr(self, f)}\n"
        for f, _ in self.header_pointer_fields():
            s += f"\t{f} = array[{len(getattr(self, f))}]\n"
        s += "}"
        return s

    @classmethod
    def header_pointer_fields(cls) -> List[Tuple[str, Union[BaseUnpacker, Type[bytes]]]]:
        return FileData_Common.header_pointer_fields() + [
            ("node_arr", NodeStruct_Unpack),
            ("obj_arr", ObjectStruct_YK1_Unpack),
            ("mesh_arr", MeshStruct_Y3_Unpack),
            ("attribute_arr", AttributeStruct_Dragon_Unpack),
            ("material_arr", MaterialStruct_Y3_Unpack),
            ("matrix_arr", MatrixUnpacker),
            ("vertex_buffer_arr", VertexBufferLayoutStruct_Y3_Unpack),
            ("vertex_data", bytes),
            ("texture_arr", ChecksumStrStruct_Unpack),
            ("shader_arr", ChecksumStrStruct_Unpack),
            ("node_name_arr", ChecksumStrStruct_Unpack),
            ("index_data", c_uint16),
            ("object_drawlist_bytes", bytes),
            ("mesh_matrixlist_bytes", bytes),
            ("unk12", Unk12Struct_Unpack),
            ("unk13", c_uint16),
            ("unk14", Unk14Struct_Unpack),
        ]

    @classmethod
    def header_fields_to_copy(cls) -> List[str]:
        return FileData_Common.header_fields_to_copy() + [
            "overall_bounds",
            "flags"
        ]


T = TypeVar('T')


@overload
def pack_array(
        big_endian: bool,
        name: str,
        data: List[T],
        packer: BaseUnpacker[T],
        append_to: bytearray
) -> ArrayPointerStruct[T]:
    ...


@overload
def pack_array(big_endian: bool, name: str, data: bytes, packer: Type[bytes],
               append_to: bytearray) -> SizedPointerStruct: ...


def pack_array(big_endian: bool, name: str, data: Union[List[T], bytes], packer: Union[BaseUnpacker[T], Type[bytes]],
               append_to: bytearray) -> Union[ArrayPointerStruct[T], SizedPointerStruct]:
    sized_pointer = SizedPointerStruct(ptr=len(append_to), size=len(data))
    if packer is bytes:
        if not isinstance(data, bytes):
            raise TypeError(
                f"Value field {name} was expected to be byte-packed")
        append_to += data
        return sized_pointer
    elif isinstance(packer, BaseUnpacker):
        if not isinstance(data, list):
            raise TypeError(
                f"Header field {name} was expected as list, packed by {packer}")
        for i, item in enumerate(data):
            try:
                packer.pack(big_endian, item, append_to)
            except PackingValidationError as e:
                raise PackingValidationError(f"Element {i} of {name}: {e}")
        return ArrayPointerStruct(sized_ptr=sized_pointer)
    else:
        raise TypeError(f"Unexpected packer type {packer}")


class DragonFilePacker(FilePacker[FileData_Dragon, GMDHeader_Dragon]):
    def pack(self, big_endian: bool, value: FileData_Dragon) -> bytearray:
        data = bytearray()

        # Pad the data out with zeroes where the header and blendshape spec will go
        data += bytes().zfill(GMDHeader_Dragon_Unpack.sizeof())
        if value.blendshape:
            data += bytes().zfill(BlendshapeSpec_Unpack.sizeof())

        # Fill in the contents
        node_arr = pack_array(big_endian, "node_arr", value.node_arr, NodeStruct_Unpack, data)
        obj_arr = pack_array(big_endian, "obj_arr", value.obj_arr, ObjectStruct_YK1_Unpack, data)
        mesh_arr = pack_array(big_endian, "mesh_arr", value.mesh_arr, MeshStruct_Y3_Unpack, data)
        attribute_arr = pack_array(big_endian, "attribute_arr", value.attribute_arr, AttributeStruct_Dragon_Unpack,
                                   data)
        material_arr = pack_array(big_endian, "material_arr", value.material_arr, MaterialStruct_Y3_Unpack, data)
        matrix_arr = pack_array(big_endian, "matrix_arr", value.matrix_arr, MatrixUnpacker, data)
        vertex_buffer_arr = pack_array(big_endian, "vertex_buffer_arr", value.vertex_buffer_arr,
                                       VertexBufferLayoutStruct_Y3_Unpack, data)
        vertex_data = pack_array(big_endian, "vertex_data", value.vertex_data, bytes, data)
        texture_arr = pack_array(big_endian, "texture_arr", value.texture_arr, ChecksumStrStruct_Unpack, data)
        shader_arr = pack_array(big_endian, "shader_arr", value.shader_arr, ChecksumStrStruct_Unpack, data)
        node_name_arr = pack_array(big_endian, "node_name_arr", value.node_name_arr, ChecksumStrStruct_Unpack, data)
        index_data = pack_array(big_endian, "index_data", value.index_data, c_uint16, data)
        object_drawlist_bytes = pack_array(big_endian, "object_drawlist_bytes", value.object_drawlist_bytes, bytes,
                                           data)
        mesh_matrixlist_bytes = pack_array(big_endian, "mesh_matrixlist_bytes", value.mesh_matrixlist_bytes, bytes,
                                           data)
        unk12 = pack_array(big_endian, "unk12", value.unk12, Unk12Struct_Unpack, data)
        unk13 = pack_array(big_endian, "unk13", value.unk13, c_uint16, data)
        unk14 = pack_array(big_endian, "unk14", value.unk14, Unk14Struct_Unpack, data)

        if value.blendshape:
            blendshape_name_offset = pack_array(big_endian, "blendshape_name", [value.blendshape[1]],
                                                ChecksumStrStruct_Unpack, data).ptr
            blendshape_vertex_ptr = pack_array(big_endian, "blendshape_vertices", value.blendshape[2], bytes, data)

        # Go back and overwrite the start with the header and blendshape spec if necessary
        header_bytes = bytearray()
        GMDHeader_Dragon_Unpack.pack(big_endian, GMDHeader_Dragon(
            magic=value.magic,
            file_endian_check=value.file_endian_check,
            vertex_endian_check=value.vertex_endian_check,
            version_combined=value.version_combined,
            name=value.name,

            overall_bounds=value.overall_bounds,

            node_arr=node_arr,
            obj_arr=obj_arr,
            mesh_arr=mesh_arr,
            attribute_arr=attribute_arr,
            material_arr=material_arr,
            matrix_arr=matrix_arr,
            vertex_buffer_arr=vertex_buffer_arr,
            vertex_data=vertex_data,  # byte data
            texture_arr=texture_arr,
            shader_arr=shader_arr,
            node_name_arr=node_name_arr,
            index_data=index_data,
            object_drawlist_bytes=object_drawlist_bytes,
            mesh_matrixlist_bytes=mesh_matrixlist_bytes,

            unk12=unk12,
            unk13=unk13,
            unk14=unk14,
            flags=value.flags,

            file_size=len(data),
            padding=0,
        ), header_bytes)
        if value.blendshape:
            BlendshapeSpec_Unpack.pack(big_endian, BlendshapeSpec(
                n_blendshapes_always_one=1,

                # The offset in the file of the ChecksumStr indicating the name of the blendshape
                blendshape_name_offset=blendshape_name_offset,
                original_vertex_packing_flags=value.blendshape[0].original_vertex_packing_flags,
                blendshape_vertex_offset_packing_flags=value.blendshape[0].blendshape_vertex_offset_packing_flags,
                original_vertex_stride=value.blendshape[0].original_vertex_stride,
                blendshape_vertex_offset_stride=value.blendshape[0].blendshape_vertex_offset_stride,
                blendshape_vertex_offset_count=value.blendshape[0].blendshape_vertex_offset_count,
                blendshape_vertex_offset_data_offset=blendshape_vertex_ptr.ptr,
                blendshape_vertex_offset_data_size=blendshape_vertex_ptr.size,
            ), header_bytes)
        data[:len(header_bytes)] = header_bytes

        return data

    def unpack(self, big_endian: bool, data: Union[bytes, bytearray], offset: int) -> Tuple[FileData_Dragon, int]:
        value: FileData_Dragon
        value, end_offset = super().unpack(big_endian, data, offset)
        if value.flags[5] & 256:
            blendshape_spec, _ = BlendshapeSpec_Unpack.unpack(big_endian, data,
                                                              offset + GMDHeader_Dragon_Unpack.sizeof())
            blendshape_name, _ = ChecksumStrStruct_Unpack.unpack(big_endian, data,
                                                                 offset + blendshape_spec.blendshape_name_offset)
            voffset_start = offset + blendshape_spec.blendshape_vertex_offset_data_offset
            voffset_end = voffset_start + blendshape_spec.blendshape_vertex_offset_data_size
            blendshape_vertex_data = data[voffset_start:voffset_end]

            value.blendshape = (blendshape_spec, blendshape_name, blendshape_vertex_data)

        return value, end_offset


FilePacker_Dragon = DragonFilePacker(FileData_Dragon, GMDHeader_Dragon_Unpack)
