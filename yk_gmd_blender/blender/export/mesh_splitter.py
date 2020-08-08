import array
import collections
import re
from dataclasses import dataclass
from typing import List, Tuple, Dict, Callable, Set, overload, Union, cast, Optional
#
import bmesh
import bpy
from bmesh.types import BMLayerItem, BMVert, BMLoop

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDSkinnedMesh, GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer, GMDVertexBufferLayout, BoneWeight4, BoneWeight, VecStorage
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter

from mathutils import Vector, Matrix

class SubmeshBuilder:
    """
    Class used to accumulate vertices and faces while generating split meshes.
    """

    vertices: GMDVertexBuffer
    triangles: List[Tuple[int, int, int]]
    blender_vid_to_this_vid: Dict[int, int]
    material_index: int

    def __init__(self, layout: GMDVertexBufferLayout, material_index: int):
        self.vertices = GMDVertexBuffer.build_empty(layout, 0)
        self.triangles = []
        self.blender_vid_to_this_vid = {}
        self.material_index = material_index

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
        return {weight.bone for vtx_idx in self.triangles[tri_idx] for weight in self.vertices.bone_weights[vtx_idx] if
                weight.weight > 0}

    def reduce_to_used_bones(self):
        referenced_bone_indices = list(self.total_referenced_bones())
        new_relevant_bones = []
        bone_index_mapping = {}
        for new_bone_idx, old_bone_idx in enumerate(referenced_bone_indices):
            new_relevant_bones.append(self.relevant_gmd_bones[old_bone_idx])
            bone_index_mapping[old_bone_idx] = new_bone_idx

        print(bone_index_mapping)

        self.relevant_gmd_bones = new_relevant_bones

        def remap_weight(bone_weight: BoneWeight):
            # If the weight is 0 the bone is unused, so don't remap it.
            # It's usually 0, which is a valid remappable value, but if we remap it then BoneWeight(bone=0, weight=0) != BoneWeight(bone=remapped 0, weight=0)
            if bone_weight.weight == 0:
                return bone_weight
            else:
                return BoneWeight(bone_index_mapping[bone_weight.bone], bone_weight.weight)

        print(len(self.vertices))
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
        # TODO - This should remap bones in skinned submeshes
        sm = SkinnedSubmeshBuilder(self.base.vertices.layout, self.base.material_index, self.base.relevant_gmd_bones)
        vertex_remap = {}

        # TODO: Detect continuous ranges and copy those ranges across?
        # Copying each vertex individually will use more memory/take more time
        def add_vtx(vert_idx, vtx_buffer):
            vtx_buffer += self.base.vertices[vert_idx:vert_idx + 1]

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


class VertexFetcher:
    bm_vertices: List[BMVert]
    vertex_layout: GMDVertexBufferLayout
    transformation_position: Matrix
    transformation_direction: Matrix
    vertex_group_bone_index_map: Dict[int, int]
    mesh: bpy.types.Mesh

    #deform_layer: Optional[BMLayerItem]
    col0_layer: Optional[bpy.types.MeshLoopColorLayer]
    col1_layer: Optional[bpy.types.MeshLoopColorLayer]
    tangent_layer: Optional[bpy.types.MeshLoopColorLayer]
    normal_w_layer: Optional[bpy.types.MeshLoopColorLayer]
    # Stores (component length, layer)
    uv_layers: List[Tuple[int, Optional[Union[bpy.types.MeshLoopColorLayer, bpy.types.MeshUVLoopLayer]]]]
    error: ErrorReporter

    def __init__(self, #bm_vertices: List[BMVert],
                 mesh_name: str,
                 vertex_layout: GMDVertexBufferLayout,
                 transformation_position: Matrix,
                 transformation_direction: Matrix,
                 mesh: bpy.types.Mesh,
                 vertex_group_bone_index_map: Dict[int, int],
                 #deform_layer: Optional[BMLayerItem],
                 col0_layer: Optional[bpy.types.MeshLoopColorLayer],
                 col1_layer: Optional[bpy.types.MeshLoopColorLayer],
                 tangent_layer: Optional[bpy.types.MeshLoopColorLayer],
                 normal_w_layer: Optional[bpy.types.MeshLoopColorLayer],
                 uv_primary: Optional[bpy.types.MeshUVLoopLayer],
                 uv_numbered: Dict[int, bpy.types.MeshLoopColorLayer],
                 error: ErrorReporter
                 ):
        self.vertex_layout = vertex_layout
        self.transformation_position = transformation_position
        self.transformation_direction = transformation_direction
        self.mesh = mesh
        self.vertex_group_bone_index_map = vertex_group_bone_index_map

        self.col0_layer = None
        if vertex_layout.col0_storage:
            self.col0_layer = col0_layer

            if not self.col0_layer:
                error.info(f"VertexFetcher for mesh {mesh_name} expected a color0 layer but got None - colors will be all-white")
        elif col0_layer:
            error.info(f"VertexFetcher for mesh {mesh_name} given a layout that doesn't use col0, but also given a col0 layer")

        self.col1_layer = None
        if vertex_layout.col1_storage:
            self.col1_layer = col1_layer

            if not self.col1_layer:
                error.info(f"VertexFetcher for mesh {mesh_name} expected a color1 layer but got None - colors will be all-white")
        elif col1_layer:
            error.info(f"VertexFetcher for mesh {mesh_name} given a layout that doesn't use col1, but also given a col1 layer")

        self.tangent_layer = None
        if vertex_layout.tangent_storage:
            self.tangent_layer = tangent_layer

            if not self.tangent_layer:
                error.info(f"VertexFetcher for mesh {mesh_name} expected a tangent layer but got None - tangents will be (0.5, 0.5, 0.5, 0.5)")
        elif tangent_layer:
            error.info(f"VertexFetcher for mesh {mesh_name} given a layout that doesn't use tangent, but also given a tangent layer")

        self.normal_w_layer = None
        if vertex_layout.tangent_storage in [VecStorage.Vec4Full, VecStorage.Vec4Fixed, VecStorage.Vec4Half]:
            self.normal_w_layer = normal_w_layer

            if not self.normal_w_layer:
                error.info(
                    f"VertexFetcher for mesh {mesh_name} expected a normal W component layer but got None - normal.W will be 0.5")
        elif normal_w_layer:
            error.info(f"VertexFetcher for mesh {mesh_name} given a layout that doesn't use normals, but also given a normal_w_layer layer")

        self.primary_uv_i = vertex_layout.get_primary_uv_index()
        if self.primary_uv_i != -1 and self.primary_uv_i in uv_numbered:
            error.recoverable(
                f"VertexFetcher for mesh {mesh_name} given a primary uv index that overlaps with a UV layer. The primary UV will take precedence.")
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

    def extract_vertex(self, vertex_buffer: GMDVertexBuffer, i: int, normal: Optional[Vector], loop: bpy.types.MeshLoopTriangle, tri_index: int):
        if vertex_buffer.layout != self.vertex_layout:
            self.error.fatal(f"VertexFetcher told to fetch vertex for a buffer with a different layout")

        vertex_buffer.pos.append((self.transformation_position @ self.mesh.vertices[i].co).resized(4))
        if vertex_buffer.normal is not None:
            normal = (self.transformation_direction @ (normal if normal is not None else Vector(loop.split_normals[tri_index]))).resized(4)
            if self.normal_w_layer:
                # normals are stored [-1, 1] so convert from [0, 1] range
                normal.w = (self.normal_w_layer.data[loop.loops[tri_index]].color[0] * 2) - 1
            else:
                normal.w = 0.5
            vertex_buffer.normal.append(normal)
        if vertex_buffer.tangent is not None:
            if self.tangent_layer:
                tangent = Vector(self.tangent_layer.data[loop.loops[tri_index]].color)
            else:
                tangent = Vector((0.5, 0.5, 0.5, 0.5))
            vertex_buffer.tangent.append(tangent)
            #vertex_buffer.tangent.append((self.transformation_direction @ Vector(self.mesh.loops[loop.loops[tri_index]].tangent)).resized(4))

        if vertex_buffer.bone_weights is not None:
            #if self.deform_layer:
            # Get a list of (vertex group ID, weight) items sorted in descending order of weight
            # Take the top 4 elements, for the top 4 most deforming bones
            # Normalize the weights so they sum to 1
            b_weights = sorted(list(self.mesh.vertices[i].groups), key=lambda i: i.weight, reverse=True)
            b_weights = [(weight_pair.group, weight_pair.weight) for weight_pair in b_weights if weight_pair.group in self.vertex_group_bone_index_map]
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
                weights_list = [BoneWeight(bone=self.vertex_group_bone_index_map[vtx], weight=weight) for vtx, weight in
                                b_weights]
                vertex_buffer.bone_weights.append((
                    weights_list[0],
                    weights_list[1],
                    weights_list[2],
                    weights_list[3],
                ))
            else: # weight_sum == 0
                vertex_buffer.bone_weights.append((
                    BoneWeight(bone=0, weight=0.0),
                    BoneWeight(bone=0, weight=0.0),
                    BoneWeight(bone=0, weight=0.0),
                    BoneWeight(bone=0, weight=0.0),
                ))

        if vertex_buffer.col0 is not None:
            if self.col0_layer:
                vertex_buffer.col0.append(Vector(self.col0_layer.data[loop.loops[tri_index]].color))
            else:
                vertex_buffer.col0.append(Vector((1, 1, 1, 1)))

        if vertex_buffer.col1 is not None:
            if self.col1_layer:
                vertex_buffer.col1.append(Vector(self.col1_layer.data[loop.loops[tri_index]].color))
            else:
                vertex_buffer.col1.append(Vector((1, 1, 1, 1)))

        for i, (component_count, layer) in enumerate(self.uv_layers):
            if layer:
                if self.primary_uv_i == i:
                    blender_uv = layer.data[loop.loops[tri_index]].uv
                    value = Vector((blender_uv[0], 1 - blender_uv[1]))
                else:
                    value = Vector(layer.data[loop.loops[tri_index]].color).resized(component_count)
            else:
                value = Vector([0] * component_count)
            vertex_buffer.uvs[i].append(value)


def split_mesh_by_material(mesh_name: str, mesh: bpy.types.Mesh, object_blender_transformation: Matrix, attribute_sets: List[GMDAttributeSet], skinned: bool,
                           vertex_group_mapping: Dict[int, GMDBone], error: ErrorReporter) -> Union[
    List[SubmeshBuilder], List[SkinnedSubmeshBuilder]]:
    col0_layer = mesh.vertex_colors["Color0"] if "Color0" in mesh.vertex_colors else None
    col1_layer = mesh.vertex_colors["Color1"] if "Color1" in mesh.vertex_colors else None
    tangent_layer = mesh.vertex_colors["TangentStorage"] if "TangentStorage" in mesh.vertex_colors else None
    normal_w_layer = mesh.vertex_colors["NormalW"] if "NormalW" in mesh.vertex_colors else None

    uv_primary = "UV_Primary"
    uv_numbered_regex = re.compile(r'UV(\d+)')

    primary_uv_layer = mesh.uv_layers[uv_primary] if uv_primary in mesh.uv_layers else mesh.uv_layers.active
    numbered_uv_layers = {}
    if mesh.vertex_colors:
        for name, layer in mesh.vertex_colors.items():
            match = uv_numbered_regex.match(name)
            if match:
                numbered_uv_layers[int(match.group(1))] = layer

    if skinned:
        #deform_layer = bm.verts.layers.deform.active

        relevant_gmd_bones = []
        vertex_group_bone_index_map = {}
        for i, (vertex_group_idx, bone) in enumerate(vertex_group_mapping.items()):
            relevant_gmd_bones.append(bone)
            vertex_group_bone_index_map[vertex_group_idx] = i

        submesh_builders = [SkinnedSubmeshBuilder(attribute_set.shader.vertex_buffer_layout, i, relevant_gmd_bones)
                            for i, attribute_set in enumerate(attribute_sets)]
    else:
        #deform_layer = None
        vertex_group_bone_index_map = {}
        submesh_builders = [SubmeshBuilder(attribute_set.shader.vertex_buffer_layout, i)
                            for i, attribute_set in enumerate(attribute_sets)]

    # TODO Put these somewhere else
    transformation_direction = Matrix((
        Vector((-1, 0, 0, 0)),
        Vector((0, 0, 1, 0)),
        Vector((0, 1, 0, 0)),
        Vector((0, 0, 0, 1)),
    ))
    transformation_position = transformation_direction @ object_blender_transformation

    vertex_fetchers = []
    for attribute_set in attribute_sets:
        vertex_fetcher = VertexFetcher(mesh_name,
                                       attribute_set.shader.vertex_buffer_layout,
                                       transformation_position=transformation_position,
                                       transformation_direction=transformation_direction,
                                       vertex_group_bone_index_map=vertex_group_bone_index_map,
                                       mesh=mesh,

                                       #deform_layer=deform_layer,
                                       col0_layer=col0_layer,
                                       col1_layer=col1_layer,
                                       tangent_layer=tangent_layer,
                                       normal_w_layer=normal_w_layer,
                                       uv_primary=primary_uv_layer,
                                       uv_numbered=numbered_uv_layers,
                                       error=error)
        vertex_fetchers.append(vertex_fetcher)

    for tri_loops in mesh.loop_triangles:
        if not (0 <= tri_loops.material_index < len(attribute_sets)):
            error.recoverable(
                f"Mesh {mesh_name} has a face with out-of-bounds material index {l0.face.material_index}. It will be skipped!")
            continue

        builder = submesh_builders[tri_loops.material_index]
        vertex_fetcher = vertex_fetchers[tri_loops.material_index]

        def parse_loop_elem(i):
            # TODO - Reenable if smooth
            if tri_loops.use_smooth:
                # Smoothed vertices can be shared between different triangles that use them
                return builder.add_vertex(tri_loops.vertices[i],
                                          lambda vertex_buffer: vertex_fetcher.extract_vertex(vertex_buffer,
                                                                                              tri_loops.vertices[i], None, tri_loops, i))
            else:
                # Vertices on hard edges cannot be shared and must be duplicated per-face
                return builder.add_unique_vertex(
                    lambda vertex_buffer: vertex_fetcher.extract_vertex(vertex_buffer, tri_loops.vertices[i], Vector(tri_loops.normal), tri_loops, i))

        triangle = (
            parse_loop_elem(0),
            parse_loop_elem(1),
            parse_loop_elem(2),
        )
        builder.add_triangle(triangle)

    return [builder for builder in submesh_builders if len(builder.vertices)]


def split_submesh_builder_by_bones(skinned_submesh_builder: SkinnedSubmeshBuilder, bone_limit: int, error: ErrorReporter) -> List[SkinnedSubmeshBuilder]:
    skinned_submesh_builder.reduce_to_used_bones()
    if len(skinned_submesh_builder.relevant_gmd_bones) <= bone_limit:
        return [skinned_submesh_builder]

    # Split SubmeshHelpers so that you never get >32 unique bones weighting a single submesh
    # This will always be possible, as any triangle can reference at most 12 bones (3 verts * 4 bones/vert)
    # so a naive solution of 2 triangles per SubmeshHelper will always reference at most 24 bones which is <32.

    x_too_many_bones = SkinnedSubmeshBuilderSubset.complete(skinned_submesh_builder)

    def bonesplit(x: SkinnedSubmeshBuilderSubset):
        bones = set()
        #print(x.referenced_triangles)
        for tri in x.referenced_triangles:
            tri_bones = x.base.triangle_referenced_bones(tri)
            if len(tri_bones) + len(bones) < bone_limit:
                bones = bones.union(tri_bones)

        x_withbones = SkinnedSubmeshBuilderSubset.empty(x.base)
        x_withoutbones = SkinnedSubmeshBuilderSubset.empty(x.base)
        for tri in x.referenced_triangles:
            tri_bones = x.base.triangle_referenced_bones(tri)
            if bones.issuperset(tri_bones):
                x_withbones.add_triangle(tri)
            else:
                x_withoutbones.add_triangle(tri)

        if len(x_withoutbones.referenced_triangles) == len(x.referenced_triangles):
            error.fatal("bonesplit() did not reduce triangle count!")

        return x_withbones, x_withoutbones

    # Start by selecting 32 bones.
    #   bones = {}
    #   for tri in submesh:
    #       tri_bones = tri.referenced_bones() (at max 24)
    #       if len(tri_bones) + len(bones) > 32
    #           break
    #       bones += tri_bones
    # This algorithm guarantees that at least one triangle uses ONLY those bones.
    # Then put all of the triangles that reference ONLY those bones in a new mesh.
    # Put the other triangles in a separate mesh. If they reference > 32 bones, apply the process again.
    # This splitting transformation bonesplit(x, bones) -> x_thosebones, x_otherbones will always produce x_otherbones with fewer triangles than x
    #   We know that at least one triangle uses only the selected bones
    #       => len(x_thosebones) >= 1
    #       len(x_otherbones) = len(x) - len(x_thosebones)
    #       => len(x_otherbones) <= len(x) - 1
    #       => len(x_otherbones) < len(x)
    # => applying bonesplit to x_otherbones recursively will definitely reduce the amount of triangles to 0
    # it will produce at maximum len(x) new meshes
    split_meshes = []
    while len(x_too_many_bones.referenced_triangles) > 0:
        new_submesh, x_too_many_bones = bonesplit(x_too_many_bones)
        split_meshes.append(new_submesh)

    # these can then be merged back together!!!!
    # TODO: Check if it's even worth it
    print(
        f"Mesh had >{bone_limit} bone references ({len(skinned_submesh_builder.relevant_gmd_bones)}) and was split into {len(split_meshes)} chunks")

    split_submeshes = []
    for split_mesh in split_meshes:
        print("\nSplitSubmeshSubset")
        print(f"ref-verts: {len(split_mesh.referenced_verts)} ref-tris: {len(split_mesh.referenced_triangles)}")
        split_submesh_builder = split_mesh.convert_to_submesh_builder()
        print("SplitSubmesh pre-reduce")
        print(f"ref-verts: {len(split_submesh_builder.vertices)} ref-tris: {len(split_submesh_builder.triangles)} ref-bones: {len(split_submesh_builder.relevant_gmd_bones)}")
        print("SplitSubmesh post-reduce")
        split_submesh_builder.reduce_to_used_bones()
        print(
            f"ref-verts: {len(split_submesh_builder.vertices)} ref-tris: {len(split_submesh_builder.triangles)} ref-bones: {len(split_submesh_builder.relevant_gmd_bones)}")
        print(split_submesh_builder.total_referenced_bones())
        split_submeshes.append(split_submesh_builder)
        print()

    return split_submeshes

# @overload
# def submesh_builder_to_gmd(submesh_builder: SkinnedSubmeshBuilder) -> GMDSkinnedMesh:
#     pass
# def submesh_builder_to_gmd(submesh_builder: SubmeshBuilder) -> GMDMesh:
#     pass


#def prepare_mesh()

def split_skinned_blender_mesh_object(context: bpy.types.Context, object: bpy.types.Object, materials: List[GMDAttributeSet], bone_name_map: Dict[str, GMDBone], bone_limit: int,
                                      error: ErrorReporter) -> List[GMDSkinnedMesh]:
    # Apply the dependency graph to the mesh
    # https://blender.stackexchange.com/a/146911
    dg = context.evaluated_depsgraph_get()

    mesh = object.evaluated_get(dg).data
    mesh.calc_normals_split()
    mesh.calc_tangents()
    mesh.calc_loop_triangles()
    mesh.transform(object.matrix_world)
    # TODO: mesh.transform(object.matrix_world)

    # bm = bmesh.new()
    # bm.from_mesh(mesh)
    # bm.verts.ensure_lookup_table()
    # bm.verts.index_update()

    vertex_group_mapping = {
        i: bone_name_map[group.name]
        for i, group in enumerate(object.vertex_groups)
        if group.name in bone_name_map
    }

    submesh_builders = split_mesh_by_material(object.name, mesh, Matrix.Identity(4), materials, True,
                                              vertex_group_mapping, error=error)

    #bm.free()

    gmd_skinned_meshes = []
    for builder in submesh_builders:
        if not isinstance(builder, SkinnedSubmeshBuilder):
            error.fatal(f"split_mesh_by_material gave a {type(builder).__name__} when a SkinnedSubmeshBuilder was expected")
        for split_builder in split_submesh_builder_by_bones(builder, bone_limit, error):
            print(f"Adding skinned mesh of vert count {len(split_builder.vertices)}")
            gmd_skinned_meshes.append(split_builder.build_to_gmd(materials))

    return gmd_skinned_meshes


def split_unskinned_blender_mesh_object(context: bpy.types.Context, object: bpy.types.Object,
                                        materials: List[GMDAttributeSet], error: ErrorReporter) -> List[GMDMesh]:
    # Apply the dependency graph to the mesh
    # https://blender.stackexchange.com/a/146911
    dg = context.evaluated_depsgraph_get()

    # mesh = object.data#evaluated_get(dg).data
    # mesh.calc_normals_split()
    # mesh.calc_loop_triangles()

    dg = context.evaluated_depsgraph_get()

    mesh = object.evaluated_get(dg).data
    mesh.calc_normals_split()
    mesh.calc_tangents()
    mesh.calc_loop_triangles()
    mesh.transform(object.matrix_world)

    # bm = bmesh.new()
    # bm.from_mesh(mesh)
    # bm.verts.ensure_lookup_table()
    # bm.verts.index_update()

    submesh_builders = split_mesh_by_material(object.name, mesh, Matrix.Identity(4), materials, False, vertex_group_mapping={}, error=error)

    #bm.free()

    return [builder.build_to_gmd(materials) for builder in submesh_builders]
