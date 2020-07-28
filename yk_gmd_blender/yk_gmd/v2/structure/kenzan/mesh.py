from dataclasses import dataclass

from yk_gmd_blender.structurelib.base import StructureUnpacker
from yk_gmd_blender.structurelib.primitives import c_uint32, c_uint64
from yk_gmd_blender.yk_gmd.v2.structure.common.mesh import Mesh, Indices_Unpack


@dataclass(frozen=True)
class Mesh_Kenzan(Mesh):
    padding: int = 0

    def check_padding(self):
        if self.padding:
            raise TypeError(f"Unexpected nonzero padding {self.padding}")


Mesh_Kenzan_Unpack = StructureUnpacker(
    Mesh_Kenzan,
    fields=[
        ("index", c_uint32),
        ("attribute_index", c_uint32),
        ("vertex_buffer_index", c_uint32),
        ("vertex_count", c_uint32),

        ("triangle_list_indices", Indices_Unpack),
        ("noreset_strip_indices", Indices_Unpack),
        ("reset_strip_indices", Indices_Unpack),

        ("matrixlist_length", c_uint32),
        ("matrixlist_offset", c_uint32),

        ("node_index", c_uint32),
        ("object_index", c_uint32),

        ("vertex_offset", c_uint32),

        ("padding", c_uint32) # Always 0
    ],
    load_validate=lambda m: m.check_padding()
)