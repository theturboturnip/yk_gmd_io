import time

from ...abstract.gmd_scene import HierarchyData, GMDScene
from ..common.to_abstract import GMDAbstractor_Common
from ...structure.yk1.file import FileData_YK1


class GMDAbstractor_YK1(GMDAbstractor_Common[FileData_YK1]):
    def make_abstract_scene(self) -> GMDScene:
        start_time = time.time()

        bytestrings_are_16bit = bool(self.file_data.flags[5] & 0x8000_0000)
        self.error.debug("BYTES", f"bytestrings are 16-bit? {bytestrings_are_16bit}")
        vertices_are_big_endian = self.file_data.vertices_are_big_endian()

        abstract_vertex_buffers = self.build_vertex_buffers_from_structs(
            self.file_data.vertex_buffer_arr, self.file_data.vertex_data,
        )
        self.error.debug("TIME", f"Time after build_vertex_buffers_from_structs: {time.time() - start_time}")

        abstract_shaders = self.build_shaders_from_structs(abstract_vertex_buffers,

                                                           self.file_data.mesh_arr, self.file_data.attribute_arr,
                                                           self.file_data.shader_arr)

        self.error.debug("TIME", f"Time after build_shaders_from_structs: {time.time() - start_time}")

        abstract_attributes = self.build_materials_from_structs(abstract_shaders,

                                                                self.file_data.attribute_arr,
                                                                self.file_data.material_arr,
                                                                self.file_data.unk12, self.file_data.unk14,
                                                                self.file_data.texture_arr)

        self.error.debug("TIME", f"Time after build_materials_from_structs: {time.time() - start_time}")

        object_bboxes = [
            o.bbox.abstractify()
            for o in self.file_data.obj_arr
        ]
        abstract_nodes = self.build_node_hierarchy_from_structs(self.file_data.node_arr,
                                                                self.file_data.node_name_arr,
                                                                self.file_data.matrix_arr,
                                                                object_bboxes)

        self.error.debug("TIME", f"Time after build_skeleton_bones_from_structs: {time.time() - start_time}")

        abstract_meshes = self.build_meshes_from_structs(abstract_attributes, abstract_vertex_buffers, abstract_nodes,

                                                         self.file_data.mesh_arr, self.file_data.index_data,
                                                         self.file_data.mesh_matrixlist_bytes,
                                                         bytestrings_are_16bit)

        self.error.debug("TIME", f"Time after build_meshes_from_structs: {time.time() - start_time}")

        object_drawlist_ptrs = [
            o.drawlist_rel_ptr
            for o in self.file_data.obj_arr
        ]
        self.connect_object_meshes(
            abstract_meshes, abstract_attributes, abstract_nodes,

            self.file_data.node_arr, object_drawlist_ptrs, self.file_data.object_drawlist_bytes
        )

        roots = [n for n in abstract_nodes if not n.parent]
        return GMDScene(
            name=self.file_data.name.text,
            flags=tuple(self.file_data.flags),
            overall_hierarchy=HierarchyData(roots),
        )
