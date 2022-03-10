import array
import collections
from dataclasses import dataclass
from typing import List, Tuple, Dict, Callable, Set, Union, Optional

import bpy
from bmesh.types import BMVert
from mathutils import Vector, Matrix

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDSkinnedMesh, GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer, GMDVertexBufferLayout, BoneWeight4, \
    BoneWeight, VecStorage
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter


@dataclass(frozen=True)
class PerLoopVertexData:
    normal: Optional[Vector]
    tangent: Optional[Vector]
    col0: Optional[Vector]
    col1: Optional[Vector]
    uvs: Tuple


class VertexFetcher:
    bm_vertices: List[BMVert]
    vertex_layout: GMDVertexBufferLayout
    transformation_position: Matrix
    transformation_direction: Matrix
    vertex_group_bone_index_map: Dict[int, int]
    mesh: bpy.types.Mesh

    # deform_layer: Optional[BMLayerItem]
    col0_layer: Optional[bpy.types.MeshLoopColorLayer]
    col1_layer: Optional[bpy.types.MeshLoopColorLayer]
    tangent_layer: Optional[bpy.types.MeshLoopColorLayer]
    tangent_w_layer: Optional[bpy.types.MeshLoopColorLayer]
    # Stores (component length, layer)
    uv_layers: List[Tuple[int, Optional[Union[bpy.types.MeshLoopColorLayer, bpy.types.MeshUVLoopLayer]]]]
    error: ErrorReporter

    def __init__(self,  # bm_vertices: List[BMVert],
                 mesh_name: str,
                 vertex_layout: GMDVertexBufferLayout,
                 transformation_position: Matrix,
                 transformation_direction: Matrix,
                 mesh: bpy.types.Mesh,
                 vertex_group_bone_index_map: Dict[int, int],
                 # deform_layer: Optional[BMLayerItem],
                 col0_layer: Optional[bpy.types.MeshLoopColorLayer],
                 col1_layer: Optional[bpy.types.MeshLoopColorLayer],
                 tangent_w_layer: Optional[bpy.types.MeshLoopColorLayer],
                 uv_primary: Optional[bpy.types.MeshUVLoopLayer],
                 uv_numbered: Dict[int, bpy.types.MeshLoopColorLayer],
                 error: ErrorReporter
                 ):
        self.vertex_layout = vertex_layout
        self.transformation_position = transformation_position
        self.transformation_direction = transformation_direction
        self.mesh = mesh
        self.vertex_group_bone_index_map = vertex_group_bone_index_map

        def verify_layer(storage, layer, name):
            if storage:
                if not layer:
                    error.info(f"Expected mesh {mesh_name} to have a {name} layer but got None")
                return layer
            elif layer:
                error.info(f"Mesh {mesh_name} has an unused {name} layer")

        self.col0_layer = verify_layer(vertex_layout.col0_storage, col0_layer, "Color0")
        self.col1_layer = verify_layer(vertex_layout.col1_storage, col1_layer, "Color1")
        self.tangent_w_layer = verify_layer(
            vertex_layout.tangent_storage in [VecStorage.Vec4Full, VecStorage.Vec4Fixed, VecStorage.Vec4Half],
            tangent_w_layer,
            "Tangent W Component"
        )
        # TODO - This "primary_uv_index" thing is icky
        self.primary_uv_i = vertex_layout.get_primary_uv_index()
        if self.primary_uv_i != -1 and self.primary_uv_i in uv_numbered:
            error.recoverable(
                f"VertexFetcher for mesh {mesh_name} given a primary uv index that refers to a numbered UV layer UV{self.primary_uv_i}. The primary UV will take precedence.")
        self.uv_layers = []
        for i, storage in enumerate(vertex_layout.uv_storages):
            if self.primary_uv_i == i:
                self.uv_layers.append((2, uv_primary))
            elif i in uv_numbered:
                layer = uv_numbered[i]
                self.uv_layers.append((VecStorage.component_count(storage), layer))
            else:
                error.info(f"VertexFetcher for mesh {mesh_name} didn't have a UV for layer {i}, values will be all-0")
                self.uv_layers.append((VecStorage.component_count(storage), None))

        self.error = error

    def normal_for(self, loop: bpy.types.MeshLoopTriangle, tri_index: int):  # , normal: Optional[Vector]
        # normal = (self.transformation_direction @ (normal if normal is not None else Vector(loop.split_normals[tri_index]))).resized(4)
        normal = (self.transformation_direction @ Vector(self.mesh.loops[loop.loops[tri_index]].normal)).resized(4)
        # if self.tangent_w_layer:
        #     # normals are stored [-1, 1] so convert from [0, 1] range
        #     normal.w = (self.tangent_w_layer.data[loop.loops[tri_index]].color[0] * 2) - 1
        # else:
        normal.w = 0
        return normal

    def tangent_for(self, loop: bpy.types.MeshLoopTriangle, tri_index: int):
        # if self.tangent_layer:
        #     tangent = Vector(self.tangent_layer.data[loop.loops[tri_index]].color)
        # else:
        #     tangent = Vector((0.5, 0.5, 0.5, 0.5))
        tangent = (self.transformation_direction @ Vector(self.mesh.loops[loop.loops[tri_index]].tangent)).resized(4)
        if self.tangent_w_layer:
            tangent.w = (self.tangent_w_layer.data[loop.loops[tri_index]].color[0] * 2) - 1
        else:
            tangent.w = 1
        return tangent

    def col0_for(self, loop: bpy.types.MeshLoopTriangle, tri_index: int):
        if self.col0_layer:
            return Vector(self.col0_layer.data[loop.loops[tri_index]].color)
        else:
            return Vector((1, 1, 1, 1))

    def col1_for(self, loop: bpy.types.MeshLoopTriangle, tri_index: int):
        if self.col1_layer:
            return Vector(self.col1_layer.data[loop.loops[tri_index]].color)
        else:
            return Vector((1, 1, 1, 1))

    def uv_for(self, uv_idx: int, loop: bpy.types.MeshLoopTriangle, tri_index: int):
        component_count, layer = self.uv_layers[uv_idx]
        if layer:
            # If component_count == 2 then we should be storing it in a UV layer. For backwards compatibility, check if the layer actually has a "uv" section
            if component_count == 2 and hasattr(layer.data[loop.loops[tri_index]], "uv"):
                blender_uv = layer.data[loop.loops[tri_index]].uv
                return Vector((blender_uv[0], 1 - blender_uv[1]))
            else:
                vec = Vector(layer.data[loop.loops[tri_index]].color).resized(component_count)
                if any(x < 0 or x > 1 for x in vec):
                    self.error.recoverable(
                        f"UV{uv_idx} has values outside of the storable range. Expected between 0 and 1, got {vec}")
                return Vector(layer.data[loop.loops[tri_index]].color).resized(component_count)
        else:
            return Vector([0] * component_count)

    def boneweights_for(self, i: int):
        # Get a list of (vertex group ID, weight) items sorted in descending order of weight
        # Take the top 4 elements, for the top 4 most deforming bones
        # Normalize the weights so they sum to 1
        b_weights = sorted(list(self.mesh.vertices[i].groups), key=lambda i: i.weight, reverse=True)
        b_weights = [(weight_pair.group, weight_pair.weight) for weight_pair in b_weights if
                     weight_pair.group in self.vertex_group_bone_index_map]
        if len(b_weights) > 4:
            b_weights = b_weights[:4]
        elif len(b_weights) < 4:
            # Add zeroed elements to b_weights so it's 4 elements long
            b_weights += [(0, 0.0)] * (4 - len(b_weights))
        weight_sum = sum(weight for (vtx, weight) in b_weights)
        if weight_sum < 0.0:
            self.error.fatal(f"Weights {b_weights} summed to negative number!")
        if weight_sum > 0:
            b_weights = [(vtx_group, weight / weight_sum) for (vtx_group, weight) in b_weights]
            # Convert the weights to the yk_gmd abstract BoneWeight format
            weights_list = [BoneWeight(bone=self.vertex_group_bone_index_map[vtx] if weight else 0, weight=weight) for
                            vtx, weight in
                            b_weights]
            return (
                weights_list[0],
                weights_list[1],
                weights_list[2],
                weights_list[3],
            )
        else:  # weight_sum == 0
            return (
                BoneWeight(bone=0, weight=0.0),
                BoneWeight(bone=0, weight=0.0),
                BoneWeight(bone=0, weight=0.0),
                BoneWeight(bone=0, weight=0.0),
            )

    def get_per_loop_data(self, loop: bpy.types.MeshLoopTriangle, tri_index: int):
        # The importer merges vertices with the same (position, boneweights, normal)
        # The position and boneweights should match exactly the GMD, so they will always be the same for fused vertices
        # However because Blender recalculates the normal it is also per-loop, so it might be different between fused vertices
        return PerLoopVertexData(
            normal=self.normal_for(loop, tri_index).freeze(),
            tangent=self.tangent_for(loop, tri_index).freeze(),
            col0=self.col0_for(loop, tri_index).freeze(),
            col1=self.col1_for(loop, tri_index).freeze(),
            uvs=tuple([self.uv_for(uv_idx, loop, tri_index).freeze() for uv_idx in range(len(self.uv_layers))])
        )

    def extract_vertex(self, vertex_buffer: GMDVertexBuffer, i: int, per_loop_data: PerLoopVertexData):
        if vertex_buffer.layout != self.vertex_layout:
            self.error.fatal(f"VertexFetcher told to fetch vertex for a buffer with a different layout")

        vertex_buffer.pos.append((self.transformation_position @ self.mesh.vertices[i].co).resized(4))
        if vertex_buffer.bone_weights is not None:
            vertex_buffer.bone_weights.append(self.boneweights_for(i))
        if vertex_buffer.normal is not None:
            vertex_buffer.normal.append(per_loop_data.normal)
        if vertex_buffer.tangent is not None:
            vertex_buffer.tangent.append(per_loop_data.tangent)
        if vertex_buffer.col0 is not None:
            vertex_buffer.col0.append(per_loop_data.col0)
        if vertex_buffer.col1 is not None:
            vertex_buffer.col1.append(per_loop_data.col1)
        for uv_idx in range(len(self.uv_layers)):
            vertex_buffer.uvs[uv_idx].append(per_loop_data.uvs[uv_idx])


class SubmeshBuilder:
    """
    Class used to accumulate vertices and faces while generating split meshes.
    """

    vertices: GMDVertexBuffer
    triangles: List[Tuple[int, int, int]]
    blender_vid_to_this_vid: Dict[Tuple[int, 'PerLoopData'], int]
    # This could use a Set with hashing, but Vectors aren't hashable by default and there's at most like 5 per list
    per_loop_data_for_blender_vid: Dict[int, List['PerLoopData']]
    material_index: int

    def __init__(self, layout: GMDVertexBufferLayout, material_index: int):
        self.vertices = GMDVertexBuffer.build_empty(layout, 0)
        self.triangles = []
        self.blender_vid_to_this_vid = {}
        self.per_loop_data_for_blender_vid = collections.defaultdict(list)
        self.material_index = material_index

    def add_vertex(self, blender_vid: int, vertex_fetcher: 'VertexFetcher', blender_loop_tri: 'bpy.types.MeshLoopTriangle', tri_index: int) -> int:
        per_loop_data = vertex_fetcher.get_per_loop_data(blender_loop_tri, tri_index)
        # Make sure to use a key based on the per_loop_data here, because otherwise if two vertices with equal blender_vid and unequal per_loop_data are reused, only one will get returned
        overall_blender_idx = (blender_vid, per_loop_data)
        if overall_blender_idx not in self.blender_vid_to_this_vid:
            idx = self.add_anonymous_vertex(lambda verts: vertex_fetcher.extract_vertex(verts, blender_vid, per_loop_data))
            self.blender_vid_to_this_vid[overall_blender_idx] = idx
            self.per_loop_data_for_blender_vid[blender_vid].append(per_loop_data)
            return idx

        return self.blender_vid_to_this_vid[overall_blender_idx]

    # Calls the function to add the vertex to the buffer and returns the index of the generated vertex.
    # This is anonymous, it will not be considered for per-loop duplication and will not be added to any vertex ID counts
    def add_anonymous_vertex(self, generate_vertex: Callable[[GMDVertexBuffer], None]) -> int:
        idx = len(self.vertices)
        generate_vertex(self.vertices)
        return idx

    def add_triangle(self, t: Tuple[int, int, int]):
        triangle_index = len(self.triangles)
        self.triangles.append(t)
        return triangle_index

    def build_triangles(self) -> Tuple[array.ArrayType, array.ArrayType, array.ArrayType]:
        triangle_list = array.array("H")
        triangle_strip_noreset = array.array("H")
        triangle_strip_reset = array.array("H")

        for t0, t1, t2 in self.triangles:
            triangle_list.append(t0)
            triangle_list.append(t1)
            triangle_list.append(t2)

            # If we can continue the strip, do so
            if not triangle_strip_noreset:
                # Add the triangle as normal
                triangle_strip_noreset.append(t0)
                triangle_strip_noreset.append(t1)
                triangle_strip_noreset.append(t2)
            elif (triangle_strip_noreset[-2] == t0 and
                  triangle_strip_noreset[-1] == t1):
                triangle_strip_noreset.append(t2)
            else:
                # Two extra verts to create a degenerate triangle, signalling the end of the strip
                triangle_strip_noreset.append(triangle_strip_noreset[-1])
                triangle_strip_noreset.append(t0)
                # Add the triangle as normal
                triangle_strip_noreset.append(t0)
                triangle_strip_noreset.append(t1)
                triangle_strip_noreset.append(t2)

            # If we can continue the strip, do so
            if not triangle_strip_reset:
                # Add the triangle as normal
                triangle_strip_reset.append(t0)
                triangle_strip_reset.append(t1)
                triangle_strip_reset.append(t2)
            elif (triangle_strip_reset[-2] == t0 and
                  triangle_strip_reset[-1] == t1):
                triangle_strip_reset.append(t2)
            else:
                # Reset index signalling the end of the strip
                triangle_strip_reset.append(0xFFFF)
                # Add the triangle as normal
                triangle_strip_reset.append(t0)
                triangle_strip_reset.append(t1)
                triangle_strip_reset.append(t2)

        return triangle_list, triangle_strip_noreset, triangle_strip_reset

    def build_to_gmd(self, gmd_attribute_sets: List[GMDAttributeSet]):
        triangle_list, triangle_strip_noreset, triangle_strip_reset = self.build_triangles()

        return GMDMesh(
            attribute_set=gmd_attribute_sets[self.material_index],
            vertices_data=self.vertices,
            triangle_indices=triangle_list,
            triangle_strip_noreset_indices=triangle_strip_noreset,
            triangle_strip_reset_indices=triangle_strip_reset,
        )


class SkinnedSubmeshBuilder(SubmeshBuilder):
    """
    Class used to accumulate vertices and faces while generating split meshes.
    Keeps track of which vertices use which bones, in case they need to be split up to keep bone limits in check.
    """

    # Generated vertices must have bone weights that index in this list.
    relevant_gmd_bones: List[GMDBone]
    # Maps GMD bone index-> verts which use that ID
    weighted_bone_verts: Dict[int, List[int]]
    # Maps GMD bone index -> face indexes which use that ID
    weighted_bone_faces: Dict[int, List[int]]

    def __init__(self, layout: GMDVertexBufferLayout, material_index: int, relevant_gmd_bones: List[GMDBone]):
        super().__init__(layout, material_index)
        self.weighted_bone_verts = collections.defaultdict(list)
        self.weighted_bone_faces = collections.defaultdict(list)
        self.relevant_gmd_bones = relevant_gmd_bones

    def add_anonymous_vertex(self, generate_vertex: Callable[[GMDVertexBuffer], None]) -> int:
        idx = super().add_anonymous_vertex(generate_vertex)
        self.update_bone_vtx_lists(self.vertices.bone_weights[idx], idx)
        return idx

    def update_bone_vtx_lists(self, new_vtx_weights: BoneWeight4, new_vtx_idx):
        for weight in new_vtx_weights:
            if weight.weight != 0:
                self.weighted_bone_verts[weight.bone].append(new_vtx_idx)

    def add_triangle(self, t: Tuple[int, int, int]):
        triangle_index = super().add_triangle(t)
        for bone in self.triangle_referenced_bones(triangle_index):
            self.weighted_bone_faces[bone].append(triangle_index)

    def total_referenced_bones(self):
        return set(bone_id for bone_id, vs in self.weighted_bone_verts.items() if len(vs) > 0)

    def triangle_referenced_bones(self, tri_idx):
        return {weight.bone for vtx_idx in self.triangles[tri_idx] for weight in self.vertices.bone_weights[vtx_idx] if
                weight.weight > 0}

    def reduce_to_used_bones(self):
        referenced_bone_indices = list(self.total_referenced_bones())
        new_relevant_bones = []
        bone_index_mapping = {}
        for new_bone_idx, old_bone_idx in enumerate(referenced_bone_indices):
            new_relevant_bones.append(self.relevant_gmd_bones[old_bone_idx])
            bone_index_mapping[old_bone_idx] = new_bone_idx

        self.relevant_gmd_bones = new_relevant_bones

        def remap_weight(bone_weight: BoneWeight):
            # If the weight is 0 the bone is unused, so don't remap it.
            # It's usually 0, which is a valid remappable value, but if we remap it then BoneWeight(bone=0, weight=0) != BoneWeight(bone=remapped 0, weight=0)
            if bone_weight.weight == 0:
                return bone_weight
            else:
                return BoneWeight(bone_index_mapping[bone_weight.bone], bone_weight.weight)

        self.weighted_bone_verts = collections.defaultdict(list)
        for i in range(len(self.vertices)):
            old_weights = self.vertices.bone_weights[i]
            self.vertices.bone_weights[i] = (
                remap_weight(old_weights[0]),
                remap_weight(old_weights[1]),
                remap_weight(old_weights[2]),
                remap_weight(old_weights[3]),
            )

            for weight in self.vertices.bone_weights[i]:
                if weight.weight != 0:
                    self.weighted_bone_verts[weight.bone].append(i)
        self.weighted_bone_faces = collections.defaultdict(list)
        for triangle_index in range(len(self.triangles)):
            for bone in self.triangle_referenced_bones(triangle_index):
                self.weighted_bone_faces[bone].append(triangle_index)


    def build_to_gmd(self, gmd_attribute_sets: List[GMDAttributeSet]) -> GMDSkinnedMesh:
        triangle_list, triangle_strip_noreset, triangle_strip_reset = self.build_triangles()

        return GMDSkinnedMesh(
            attribute_set=gmd_attribute_sets[self.material_index],
            vertices_data=self.vertices,
            triangle_indices=triangle_list,
            triangle_strip_noreset_indices=triangle_strip_noreset,
            triangle_strip_reset_indices=triangle_strip_reset,

            relevant_bones=self.relevant_gmd_bones
        )


class SkinnedSubmeshBuilderSubset:
    """
    Represents a subset of the vertices and faces in a SkinnedSubmeshBuilder, for splitting on bones.
    """

    base: SkinnedSubmeshBuilder
    referenced_triangles: Set[int]
    referenced_verts: Set[int]

    def __init__(self, base: SkinnedSubmeshBuilder, referenced_triangles, referenced_verts):
        self.base = base
        self.referenced_triangles = referenced_triangles
        self.referenced_verts = referenced_verts

    def add_triangle(self, tri_idx: int):
        self.referenced_triangles.add(tri_idx)
        for vert_idx in self.base.triangles[tri_idx]:
            self.referenced_verts.add(vert_idx)

    @staticmethod
    def empty(base: SkinnedSubmeshBuilder):
        return SkinnedSubmeshBuilderSubset(base, set([]), set([]))

    @staticmethod
    def complete(base: SkinnedSubmeshBuilder):
        return SkinnedSubmeshBuilderSubset(base, set(range(len(base.triangles))), set(range(len(base.vertices))))

    def convert_to_submesh_builder(self) -> SkinnedSubmeshBuilder:
        # TODO - This should remap bones in skinned submeshes, instead of making the base SkinnedSubmeshBuilder remap them later?
        sm = SkinnedSubmeshBuilder(self.base.vertices.layout, self.base.material_index, self.base.relevant_gmd_bones)
        vertex_remap = {}

        # TODO: Detect continuous ranges and copy those ranges across?
        # Copying each vertex individually will use more memory/take more time
        def add_vtx(vert_idx, vtx_buffer):
            vtx_buffer += self.base.vertices[vert_idx:vert_idx + 1]

        for vert_idx in sorted(self.referenced_verts):
            new_idx = sm.add_anonymous_vertex(lambda vtx_buffer: add_vtx(vert_idx, vtx_buffer))
            vertex_remap[vert_idx] = new_idx
        for tri_idx in self.referenced_triangles:
            sm.add_triangle((
                vertex_remap[self.base.triangles[tri_idx][0]],
                vertex_remap[self.base.triangles[tri_idx][1]],
                vertex_remap[self.base.triangles[tri_idx][2]],
            ))
        return sm
