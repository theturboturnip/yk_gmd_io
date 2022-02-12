import array
import collections
from dataclasses import dataclass
from typing import List, Tuple, Dict, Callable, Set, Union, Optional, Generic, TypeVar

from bmesh.types import BMVert
from mathutils import Vector, Matrix

import bpy
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDSkinnedMesh, GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer_Generic, GMDVertexBufferLayout, BoneWeight4, \
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
        normal.normalize()
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

    def extract_vertex(self, vertex_buffer: GMDVertexBuffer_Generic, i: int, per_loop_data: PerLoopVertexData):
        if vertex_buffer.layout != self.vertex_layout:
            self.error.fatal(f"VertexFetcher told to fetch vertex for a buffer with a different layout")

        vertex_buffer.pos.append((self.transformation_position @ self.mesh.vertices[i].co).resized(4))
        # TODO refactor boneweights functionality - on an unskinned object extracting boneweights will be different
        boneweights = self.boneweights_for(i)
        if vertex_buffer.bone_data is not None:
            vertex_buffer.bone_data.append(Vector((boneweights[0].bone, boneweights[1].bone, boneweights[2].bone, boneweights[3].bone)))
        if vertex_buffer.weight_data is not None:
            vertex_buffer.weight_data.append(Vector((boneweights[0].weight, boneweights[1].weight, boneweights[2].weight, boneweights[3].weight)))
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
    Contains at most 65535 vertices.
    """

    vertices: GMDVertexBuffer_Generic
    triangles: List[Tuple[int, int, int]]
    blender_vid_to_this_vid: Dict[Tuple[int, 'PerLoopData'], int]
    # This could use a Set with hashing, but Vectors aren't hashable by default and there's at most like 5 per list
    per_loop_data_for_blender_vid: Dict[int, List['PerLoopData']]
    material_index: int

    def __init__(self, layout: GMDVertexBufferLayout, material_index: int):
        self.vertices = GMDVertexBuffer_Generic.build_empty(layout, 0)
        self.triangles = []
        self.blender_vid_to_this_vid = {}
        self.per_loop_data_for_blender_vid = collections.defaultdict(list)
        self.material_index = material_index

    # Try to add the three vertices needed for a triangle, and add a triangle with those indices
    # If can't add all of them (e.g. pushes indices over 65535), returns False, doesn't add any vertices, doesn't add a new triangle
    # Otherwise adds all required vertices and new triangles
    def add_triangle_vertices(self, blender_vids: Tuple[int,int,int], vertex_fetcher: 'VertexFetcher', blender_loop_tri: 'bpy.types.MeshLoopTriangle') -> bool:
        # Find the overall blender indices of each vertex
        # (including the per-loop-data, because vertices can differ between different 'loops' in Blender)
        overall_idxs = [
            (blender_vids[tri_index], vertex_fetcher.get_per_loop_data(blender_loop_tri, tri_index))
            for tri_index in range(3)
        ]

        # Check if we have enough spare vertices
        # If we have less than (65535 - 3) vertices, we don't need to check - we definitely have enough space
        if len(self.vertices) > (65535 - 3):
            # Otherwise, check beforehand how many we actually need to add
            new_idxs = [idx for idx in overall_idxs if idx not in self.blender_vid_to_this_vid]
            # If, by adding these vertices, we go overboard: return False, don't do anything
            if len(self.vertices) + len(new_idxs) > 65535:
                return False

        # We now guarantee we can add all vertices without going over
        def add_if_not_present(overall_blender_idx):
            blender_vid, per_loop_data = overall_blender_idx

            if overall_blender_idx not in self.blender_vid_to_this_vid:
                idx = self.add_anonymous_vertex(
                    lambda verts: vertex_fetcher.extract_vertex(verts, blender_vid, per_loop_data))
                self.blender_vid_to_this_vid[overall_blender_idx] = idx
                self.per_loop_data_for_blender_vid[blender_vid].append(per_loop_data)
                return idx
            return self.blender_vid_to_this_vid[overall_blender_idx]

        final_indices = (
            add_if_not_present(overall_idxs[0]),
            add_if_not_present(overall_idxs[1]),
            add_if_not_present(overall_idxs[2]),
        )

        self.add_triangle(final_indices)

        return True

    # Calls the function to add the vertex to the buffer and returns the index of the generated vertex.
    # This is anonymous, it will not be considered for per-loop duplication and will not be added to any vertex ID counts
    def add_anonymous_vertex(self, generate_vertex: Callable[[GMDVertexBuffer_Generic], None]) -> int:
        idx = len(self.vertices)
        if idx > 65535:
            raise RuntimeError("Trying to create >65535 anonymous vertices")
        generate_vertex(self.vertices)
        return idx

    # Add a triangle (tuple of three vertex IDs, corresponding to vertices in self.vertices)
    def add_triangle(self, t: Tuple[int, int, int]):
        triangle_index = len(self.triangles)
        self.triangles.append(t)
        return triangle_index

    # Build the triangle strip from self.triangles
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
                # Starting the strip
                triangle_strip_noreset.append(t0)
                triangle_strip_noreset.append(t1)
                triangle_strip_noreset.append(t2)
            elif (triangle_strip_noreset[-2] == t0 and
                  triangle_strip_noreset[-1] == t1):
                # Continue the strip
                triangle_strip_noreset.append(t2)
            else:
                # End previous strip, start new strip
                # Two extra verts to create a degenerate triangle, signalling the end of the strip
                triangle_strip_noreset.append(triangle_strip_noreset[-1])
                triangle_strip_noreset.append(t0)
                # Add the triangle as normal
                triangle_strip_noreset.append(t0)
                triangle_strip_noreset.append(t1)
                triangle_strip_noreset.append(t2)

            # If we can continue the strip, do so
            if not triangle_strip_reset:
                # Starting the strip
                triangle_strip_reset.append(t0)
                triangle_strip_reset.append(t1)
                triangle_strip_reset.append(t2)
            elif (triangle_strip_reset[-2] == t0 and
                  triangle_strip_reset[-1] == t1):
                # Continue the strip
                triangle_strip_reset.append(t2)
            else:
                # End previous strip, start new strip
                # Reset index signalling the end of the strip
                triangle_strip_reset.append(0xFFFF)
                # Add the triangle as normal
                triangle_strip_reset.append(t0)
                triangle_strip_reset.append(t1)
                triangle_strip_reset.append(t2)

        return triangle_list, triangle_strip_noreset, triangle_strip_reset

    # Build the vertex buffer + triangle strips from self.vertices and self.triangles
    def build_to_gmd(self, gmd_attribute_sets: List[GMDAttributeSet]):
        triangle_list, triangle_strip_noreset, triangle_strip_reset = self.build_triangles()

        return GMDMesh(
            empty=False,
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

    def boneweight_of_vertex(self, idx: int) -> BoneWeight4:
        # TODO - this is hella slow
        # I would need to refactor this more to get rid of the BoneWeight4 abstraction completely
        # Context: Before, we assumed all vertex buffers were skinned vertex buffers, and there was a bone_weights field
        # that just stored a 4-tuple of (bone: int, weight: float).
        # This is very convenient for skinned exporters.
        # However, we later separated bones and weights into different data fields - GMDVertexBuffer_Skinned exists,
        # but its bone_weights field doesn't synchronize with the other fields so we can't use it here.
        data = [
            BoneWeight(bone=int(bone), weight=weight)
            for bone, weight in zip(self.vertices.bone_data[idx], self.vertices.weight_data[idx])
        ]
        return (
            data[0],
            data[1],
            data[2],
            data[3]
        )

    # Override: when a vertex is added, adds it to weighted_bone_verts for all bones it references
    def add_anonymous_vertex(self, generate_vertex: Callable[[GMDVertexBuffer_Generic], None]) -> int:
        idx = super().add_anonymous_vertex(generate_vertex)
        # Register this vertex as a user of bone blah
        for bw in self.boneweight_of_vertex(idx):
            if bw.weight != 0:
                self.weighted_bone_verts[bw.bone].append(idx)
        return idx

    # Override: when a triangle is added, adds it to weighted_bone_faces for all bones it references
    def add_triangle(self, t: Tuple[int, int, int]):
        triangle_index = super().add_triangle(t)
        for bone in self.triangle_referenced_bones(triangle_index):
            self.weighted_bone_faces[bone].append(triangle_index)

    # TODO should be moved into add_anonymous_vertex, but I think it gets changed in v0.4 so won't do it now
    def update_bone_vtx_lists(self, new_vtx_weights: BoneWeight4, new_vtx_idx):
        for weight in new_vtx_weights:
            if weight.weight != 0:
                self.weighted_bone_verts[weight.bone].append(new_vtx_idx)

    def total_referenced_bones(self):
        return set(bone_id for bone_id, vs in self.weighted_bone_verts.items() if len(vs) > 0)

    def triangle_referenced_bones(self, tri_idx):
        return {weight.bone for vtx_idx in self.triangles[tri_idx] for weight in self.boneweight_of_vertex(vtx_idx) if
                weight.weight > 0}

    # This submesh builder was created with a set of relevant_bones
    # Remove references to any bones that are unused, and strip those bones out
    def reduce_to_used_bones(self):
        referenced_bone_indices = list(self.total_referenced_bones())
        # If the lengths are equal, the set of relevant bones hasn't changed and we don't need to remap
        if len(referenced_bone_indices) == len(self.relevant_gmd_bones):
            return

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
            old_weights = self.boneweight_of_vertex(i)
            new_weights = (
                remap_weight(old_weights[0]),
                remap_weight(old_weights[1]),
                remap_weight(old_weights[2]),
                remap_weight(old_weights[3]),
            )

            for weight in new_weights:
                if weight.weight != 0:
                    self.weighted_bone_verts[weight.bone].append(i)

            # Assign new_weights to vertex buffer
            self.vertices.bone_data[i] = Vector((new_weights[0].bone, new_weights[1].bone, new_weights[2].bone, new_weights[3].bone))
            self.vertices.weight_data[i] = Vector(
                (new_weights[0].weight, new_weights[1].weight, new_weights[2].weight, new_weights[3].weight))

        self.weighted_bone_faces = collections.defaultdict(list)
        for triangle_index in range(len(self.triangles)):
            for bone in self.triangle_referenced_bones(triangle_index):
                self.weighted_bone_faces[bone].append(triangle_index)

    def build_to_gmd(self, gmd_attribute_sets: List[GMDAttributeSet]) -> GMDSkinnedMesh:
        triangle_list, triangle_strip_noreset, triangle_strip_reset = self.build_triangles()

        return GMDSkinnedMesh(
            empty=False,
            attribute_set=gmd_attribute_sets[self.material_index],
            vertices_data=self.vertices.move_to_skinned(),
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


TSubmeshBuilder = TypeVar('TSubmeshBuilder', SubmeshBuilder, SkinnedSubmeshBuilder)
class MeshBuilder(Generic[TSubmeshBuilder]):
    """
    Class that holds a mapping of (attribute set index -> current builder for that index),
    and any filled-up builders (builders can only store 65536 vertices).

    It's a MeshBuilder because it holds all the SubmeshBuilders for a mesh!
    """
    mesh_name: str
    factory: Callable[[int], TSubmeshBuilder]
    error: ErrorReporter

    current_builders: Dict[int, TSubmeshBuilder]
    filled_builders: List[TSubmeshBuilder]

    def __init__(self, mesh_name: str, factory: Callable[[int], TSubmeshBuilder], error: ErrorReporter):
        self.mesh_name = mesh_name
        self.factory = factory
        self.error = error
        self.current_builders = {}
        self.filled_builders = []

    # Wrapper function for self.current_builders[i].add_triangle_vertices()
    # If that function returns False, that builder is removed from current_builders and pushed to filled_builders
    def add_triangle_vertices(self,
                              attr_set_i: int,
                              blender_vids: Tuple[int,int,int],
                              vertex_fetcher: 'VertexFetcher',
                              blender_loop_tri: 'bpy.types.MeshLoopTriangle'):
        # If we haven't added this builder yet, do so
        if attr_set_i not in self.current_builders:
            self.create_builder_for(attr_set_i)
        # Now, a builder definitely exists.
        # Try adding the new triangle to the builder
        if not self.current_builders[attr_set_i].add_triangle_vertices(blender_vids, vertex_fetcher, blender_loop_tri):
            self.error.debug("MESH", f"Mesh {self.mesh_name} filled out the SubmeshBuilder for material idx {attr_set_i}, creating a new submesh...")
            # Couldn't add more triangles to the current builder
            # => move the old builder into self.filled_builders, and make a new builder
            self.filled_builders.append(self.current_builders[attr_set_i])
            del self.current_builders[attr_set_i]
            self.create_builder_for(attr_set_i)
            # This new builder must not run out of space, if it does then hard crash
            if not self.current_builders[attr_set_i].add_triangle_vertices(blender_vids, vertex_fetcher,
                                                                           blender_loop_tri):
                self.error.fatal(f"Brand new {type(self.current_builders[attr_set_i]).__name__} couldn't add new triangle")

    # Internal function for creating a new builder in self.current_builders
    def create_builder_for(self, attr_set_i: int):
        assert attr_set_i not in self.current_builders
        self.current_builders[attr_set_i] = self.factory(attr_set_i)

    # List of references to non-empty submesh builders
    def get_nonempty_submesh_builders(self):
        return self.filled_builders + [b for b in self.current_builders.values() if len(b.vertices)]