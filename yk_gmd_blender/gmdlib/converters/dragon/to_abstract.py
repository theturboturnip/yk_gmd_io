import time

from ..common.to_abstract import GMDAbstractor_Common
from ...abstract.gmd_scene import HierarchyData, GMDScene
from ...structure.dragon.file import FileData_Dragon


class GMDAbstractor_Dragon(GMDAbstractor_Common[FileData_Dragon]):
    def make_abstract_scene(self) -> GMDScene:
        start_time = time.time()

        bytestrings_are_16bit = bool(self.file_data.flags[5] & 0x8000_0000)
        self.error.debug("BYTES", f"bytestrings are 16-bit? {bytestrings_are_16bit}")
        vertices_are_big_endian = self.file_data.vertices_are_big_endian()

        # TODO - thought on dragon engine normals - they're kinda weird
        #  they could be compressed into 2 floats and then the other ones used for other stuff? like the w component
        abstract_vertex_buffers, blendshape_buffers = self.build_vertex_buffers_from_structs(
            self.file_data.vertex_buffer_arr, self.file_data.vertex_data,
            blendshapes=(
                self.file_data.blendshapes[0],
                self.file_data.blendshapes[2]
            ) if self.file_data.blendshapes else None,
        )
        if self.file_data.blendshapes and not blendshape_buffers:
            self.error.recoverable("Found blendshapes in this file but didn't import them. "
                                   "Disable Strict Import to ignore this error.")
        if self.file_data.blendshapes:
            blendshape_names = [name.text for name in self.file_data.blendshapes[1]]
            if len(blendshape_names) != len(blendshape_buffers):
                self.error.recoverable(f"Found {len(blendshape_names)} blendshape names in the file but imported "
                                       f"{len(blendshape_buffers)} buffers. Will only use the fewer of the two. "
                                       f"Disable Strict Import to ignore this error.")
            blendshapes = {}
            for (name, buffer) in zip(blendshape_names, blendshape_buffers):
                if name in blendshapes:
                    self.error.recoverable(f"Found multiple blendshapes named '{name}' in this file. "
                                           f"Disable Strict Import to continue, only the first blendshape will be imported.")
                    continue
                blendshapes[name] = buffer
        else:
            blendshapes = {}

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
                                                         bytestrings_are_16bit,
                                                         blendshapes=blendshapes)

        self.error.debug("TIME", f"Time after build_meshes_from_structs: {time.time() - start_time}")

        object_drawlist_ptrs = [
            o.drawlist_rel_ptr
            for o in self.file_data.obj_arr
        ]
        self.connect_object_meshes(
            abstract_meshes, abstract_attributes, abstract_nodes,

            self.file_data.node_arr, object_drawlist_ptrs, self.file_data.object_drawlist_bytes
        )

        roots = [n for n in abstract_nodes.values() if not n.parent]
        return GMDScene(
            name=self.file_data.name.text,
            flags=tuple(self.file_data.flags),
            overall_hierarchy=HierarchyData(roots),
        )
