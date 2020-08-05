import collections
from dataclasses import dataclass
from typing import List, Tuple, Dict, Callable, Set, overload, Union

import bpy

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDSkinnedMesh, GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer, GMDVertexBufferLayout, BoneWeight4
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone


class SubmeshBuilder:
    """
    Class used to accumulate vertices and faces while generating split meshes.
    """

    vertices: GMDVertexBuffer
    triangles: List[Tuple[int,int,int]]
    blender_vid_to_this_vid: Dict[int, int]

    def __init__(self, layout: GMDVertexBufferLayout):
        self.vertices = GMDVertexBuffer.build_empty(layout, 0)
        self.triangles = []
        self.blender_vid_to_this_vid = {}

    # Adds the vertex if not already present
    # Used for smooth faces, where the vertex is reused in other faces as well
    def add_vertex(self, blender_vid, generate_vertex: Callable[[GMDVertexBuffer], None]) -> int:
        if blender_vid not in self.blender_vid_to_this_vid:
            self.blender_vid_to_this_vid[blender_vid] = self.add_unique_vertex(generate_vertex)

        return self.blender_vid_to_this_vid[blender_vid]

    # Adds a unique vertex, which we assume is never duplicated
    # Used for hard edges
    def add_unique_vertex(self, generate_vertex: Callable[[GMDVertexBuffer], None]) -> int:
        idx = len(self.vertices)
        generate_vertex(self.vertices)
        return idx

    def add_triangle(self, t:Tuple[int,int,int]):
        triangle_index = len(self.triangles)
        self.triangles.append(t)
        return triangle_index


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

    def __init__(self, layout: GMDVertexBufferLayout, relevant_gmd_bones: List[GMDBone]):
        super().__init__(layout)
        self.weighted_bone_verts = collections.defaultdict(list)
        self.weighted_bone_faces = collections.defaultdict(list)
        self.relevant_gmd_bones = relevant_gmd_bones

    def add_unique_vertex(self, generate_vertex: Callable[[GMDVertexBuffer], None]) -> int:
        idx = super().add_unique_vertex(generate_vertex)
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
        return {weight.bone for vtx_idx in self.triangles[tri_idx] for weight in self.vertices.bone_weights[vtx_idx] if weight.weight > 0}


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

    def add_triangle(self, tri_idx:int):
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
        # TODO - This should remap bones in skinned submeshes
        sm = SkinnedSubmeshBuilder(self.base.vertices.layout, self.base.relevant_gmd_bones)
        vertex_remap = {}
        # TODO: Detect continuous ranges and copy those ranges across?
        # Copying each vertex individually will use more memory/take more time
        def add_vtx(vert_idx, vtx_buffer):
            vtx_buffer += self.base.vertices[vert_idx:vert_idx+1]
        for vert_idx in sorted(self.referenced_verts):
            new_idx = sm.add_unique_vertex(lambda vtx_buffer: add_vtx(vert_idx, vtx_buffer))
            vertex_remap[vert_idx] = new_idx
        for tri_idx in self.referenced_triangles:
            sm.add_triangle((
                vertex_remap[self.base.triangles[tri_idx][0]],
                vertex_remap[self.base.triangles[tri_idx][1]],
                vertex_remap[self.base.triangles[tri_idx][2]],
            ))
        return sm

def split_mesh_by_material(mesh: bpy.types.Mesh, skinned: bool) -> Union[List[SubmeshBuilder], List[SkinnedSubmeshBuilder]]:
    pass

def split_submesh_builder_by_bones(skinned_submesh_builder: SkinnedSubmeshBuilder) -> List[SkinnedSubmeshBuilder]:
    pass

@overload
def submesh_builder_to_gmd(submesh_builder: SkinnedSubmeshBuilder) -> GMDSkinnedMesh:
    pass
def submesh_builder_to_gmd(submesh_builder: SubmeshBuilder) -> GMDMesh:
    pass


def split_skinned_blender_mesh_object(object: bpy.types.Object, bone_limit: int) -> List[GMDSkinnedMesh]:
    pass
def split_unskinned_blender_mesh_object(object: bpy.types.Object) -> List[GMDMesh]:
    pass