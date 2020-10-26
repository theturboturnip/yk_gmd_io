import array
import collections
from typing import List, Tuple, Dict, Callable, Set

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDSkinnedMesh, GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer, GMDVertexBufferLayout, BoneWeight4, BoneWeight
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone

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


    # Adds the vertex if not already present
    # Used for smooth faces, where the vertex is reused in other faces as well
    # def add_vertex(self, blender_vid, generate_vertex: Callable[[GMDVertexBuffer], None]) -> int:
    #     if blender_vid not in self.blender_vid_to_this_vid:
    #         self.blender_vid_to_this_vid[blender_vid] = self.add_unique_vertex(generate_vertex)
    #
    #     return self.blender_vid_to_this_vid[blender_vid]
    #
    # # Adds a unique vertex, which we assume is never duplicated
    # # Used for hard edges
    # def add_unique_vertex(self, generate_vertex: Callable[[GMDVertexBuffer], None]) -> int:
    #     idx = len(self.vertices)
    #     generate_vertex(self.vertices)
    #     return idx

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
