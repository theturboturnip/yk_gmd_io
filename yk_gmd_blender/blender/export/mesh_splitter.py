import array
import collections
import re
from dataclasses import dataclass
from typing import List, Tuple, Dict, Callable, Set, overload, Union, cast, Optional

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

        self.relevant_gmd_bones = new_relevant_bones

        def remap_weight(bone_weight: BoneWeight):
            # If the weight is 0 the bone is unused, so don't remap it.
            # It's usually 0, which is a valid remappable value, but if we remap it then BoneWeight(bone=0, weight=0) != BoneWeight(bone=remapped 0, weight=0)
            if bone_weight.weight == 0:
                return bone_weight
            else:
                return BoneWeight(bone_index_mapping[bone_weight.bone], bone_weight.weight)

        for i in range(len(self.vertices)):
            old_weights = self.vertices.bone_weights[i]
            self.vertices.bone_weights[i] = (
                remap_weight(old_weights[0]),
                remap_weight(old_weights[1]),
                remap_weight(old_weights[2]),
                remap_weight(old_weights[3]),
            )

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

    deform_layer: Optional[BMLayerItem]
    col0_layer: Optional[BMLayerItem]
    col1_layer: Optional[BMLayerItem]
    # Stores (component length, layer)
    uv_layers: List[Tuple[int, Optional[BMLayerItem]]]
    error: ErrorReporter

    def __init__(self, bm_vertices: List[BMVert],
                 vertex_layout: GMDVertexBufferLayout,
                 transformation_position: Matrix,
                 transformation_direction: Matrix,
                 vertex_group_bone_index_map: Dict[int, int],
                 deform_layer: Optional[BMLayerItem],
                 col0_layer: Optional[BMLayerItem],
                 col1_layer: Optional[BMLayerItem],
                 uv_primary: Optional[BMLayerItem],
                 uv_numbered: Dict[int, BMLayerItem],
                 error: ErrorReporter
                 ):
        self.bm_vertices = bm_vertices
        self.vertex_layout = vertex_layout
        self.transformation_position = transformation_position
        self.transformation_direction = transformation_direction
        self.vertex_group_bone_index_map = vertex_group_bone_index_map

        self.deform_layer = None
        if vertex_layout.weights_storage:
            self.deform_layer = deform_layer

            if not self.deform_layer:
                error.recoverable(f"VertexFetcher expected a deform layer but got None - weights will be all-zero")
        elif deform_layer:
            # TODO - error reporter log
            print(f"VertexFetcher given a layout that doesn't use weights, but also given a deform layer")

        self.col0_layer = None
        if vertex_layout.col0_storage:
            self.col0_layer = col0_layer

            if not self.col0_layer:
                error.recoverable(f"VertexFetcher expected a color0 layer but got None - colors will be all-white")
        elif deform_layer:
            # TODO - error reporter log
            print(f"VertexFetcher given a layout that doesn't use col0, but also given a col0 layer")

        self.col1_layer = None
        if vertex_layout.col1_storage:
            self.col1_layer = col1_layer

            if not self.col1_layer:
                error.recoverable(f"VertexFetcher expected a color1 layer but got None - colors will be all-white")
        elif deform_layer:
            # TODO - error reporter log
            print(f"VertexFetcher given a layout that doesn't use col1, but also given a col1 layer")

        self.primary_uv_i = vertex_layout.get_primary_uv_index()
        if self.primary_uv_i != -1 and self.primary_uv_i in uv_numbered:
            error.recoverable(
                f"VertexFetcher given a primary uv index that overlaps with a UV layer. The primary UV will take precedence.")
        self.uv_layers = []
        for i, storage in enumerate(vertex_layout.uv_storages):
            if self.primary_uv_i == i:
                self.uv_layers.append((2, uv_primary))
            elif i in uv_numbered:
                layer = uv_numbered[i]
                self.uv_layers.append((VecStorage.component_count(storage), layer))
            else:
                error.recoverable(f"VertexFetcher didn't have a UV for layer {i}, values will be all-0")
                self.uv_layers.append((VecStorage.component_count(storage), None))

        self.error = error

    def extract_vertex(self, vertex_buffer: GMDVertexBuffer, i: int, normal: Optional[Vector], loop: BMLoop):
        if vertex_buffer.layout != self.vertex_layout:
            self.error.fatal(f"VertexFetcher told to fetch vertex for a buffer with a different layout")

        b_vert = self.bm_vertices[i]

        vertex_buffer.pos.append((self.transformation_position @ b_vert.co).resized(4))
        if vertex_buffer.normal is not None:
            vertex_buffer.normal.append(
                (self.transformation_direction @ (normal if normal is not None else b_vert.normal)).resized(4))
        if vertex_buffer.tangent is not None:
            vertex_buffer.tangent.append((self.transformation_direction @ loop.calc_tangent()).resized(4))

        if vertex_buffer.bone_weights is not None:
            if self.deform_layer:
                # Get a list of (vertex group ID, weight) items sorted in descending order of weight
                # Take the top 4 elements, for the top 4 most deforming bones
                # Normalize the weights so they sum to 1
                b_weights = sorted(b_vert[self.deform_layer].items(), key=lambda i: 1 - i[1])
                if len(b_weights) > 4:
                    b_weights = b_weights[:4]
                elif len(b_weights) < 4:
                    # Add zeroed elements to b_weights so it's 4 elements long
                    b_weights += [(0, 0.0)] * (4 - len(b_weights))
                weight_sum = sum(weight for (vtx, weight) in b_weights)
                if weight_sum < 0.0:
                    self.error.fatal(f"Weights {b_weights} summed to negative number!")

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
            else:
                vertex_buffer.bone_weights.append((
                    BoneWeight(bone=0, weight=0),
                    BoneWeight(bone=0, weight=0),
                    BoneWeight(bone=0, weight=0),
                    BoneWeight(bone=0, weight=0),
                ))

        if vertex_buffer.col0 is not None:
            if self.col0_layer:
                vertex_buffer.col0.append(Vector(loop[self.col0_layer]))
            else:
                vertex_buffer.col0.append(Vector((1, 1, 1, 1)))

        if vertex_buffer.col1 is not None:
            if self.col1_layer:
                vertex_buffer.col1.append(Vector(loop[self.col1_layer]))
            else:
                vertex_buffer.col1.append(Vector((1, 1, 1, 1)))

        for i, (component_count, layer) in enumerate(self.uv_layers):
            if layer:
                if self.primary_uv_i == i:
                    blender_uv = loop[layer].uv
                    value = Vector((blender_uv[0], 1 - blender_uv[1]))
                else:
                    value = Vector(loop[layer].resized(component_count))
            else:
                value = Vector([0] * component_count)
            vertex_buffer.uvs[i].append(value)


def split_mesh_by_material(name: str, bm: bmesh.types.BMesh, object_blender_transformation: Matrix, attribute_sets: List[GMDAttributeSet], skinned: bool,
                           vertex_group_mapping: Dict[int, GMDBone], error: ErrorReporter) -> Union[
    List[SubmeshBuilder], List[SkinnedSubmeshBuilder]]:
    col0_layer = bm.loops.layers.color["Color0"] if "Color0" in bm.loops.layers.color else None
    col1_layer = bm.loops.layers.color["Color1"] if "Color1" in bm.loops.layers.color else None

    uv_primary = "UV_Primary"
    uv_numbered_regex = re.compile(r'UV(\d+)')

    primary_uv_layer = bm.loops.layers.uv[uv_primary] if uv_primary in bm.loops.layers.uv else bm.loops.layers.uv.active
    numbered_uv_layers: Dict[int, BMLayerItem] = {}
    if bm.loops.layers.color:
        for name, layer in bm.loops.layers.color.items():
            match = uv_numbered_regex.match(name)
            if match:
                numbered_uv_layers[int(match.group(1))] = layer

    if skinned:
        deform_layer = bm.verts.layers.deform.active

        relevant_gmd_bones = []
        vertex_group_bone_index_map = {}
        for i, (vertex_group_idx, bone) in enumerate(vertex_group_mapping.items()):
            relevant_gmd_bones.append(bone)
            vertex_group_bone_index_map[vertex_group_idx] = i

        submesh_builders = [SkinnedSubmeshBuilder(attribute_set.shader.vertex_buffer_layout, i, relevant_gmd_bones)
                            for i, attribute_set in enumerate(attribute_sets)]
    else:
        deform_layer = None
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
        vertex_fetcher = VertexFetcher(bm.verts, attribute_set.shader.vertex_buffer_layout,
                                       transformation_position=transformation_position,
                                       transformation_direction=transformation_direction,
                                       vertex_group_bone_index_map=vertex_group_bone_index_map,
                                       deform_layer=deform_layer,
                                       col0_layer=col0_layer,
                                       col1_layer=col1_layer,
                                       uv_primary=primary_uv_layer,
                                       uv_numbered=numbered_uv_layers,
                                       error=error)
        vertex_fetchers.append(vertex_fetcher)

    for tri_loops in bm.calc_loop_triangles():
        l0 = tri_loops[0]
        l1 = tri_loops[1]
        l2 = tri_loops[2]

        if not (0 <= l0.face.material_index < len(attribute_sets)):
            error.recoverable(
                f"Mesh {name} has a face with out-of-bounds material index {l0.face.material_index}. It will be skipped!")
            continue

        builder = submesh_builders[l0.face.material_index]
        vertex_fetcher = vertex_fetchers[l0.face.material_index]

        def parse_loop_elem(l):
            if l.face.smooth:
                # Smoothed vertices can be shared between different triangles that use them
                return builder.add_vertex(l.vert.index,
                                          lambda vertex_buffer: vertex_fetcher.extract_vertex(vertex_buffer,
                                                                                              l.vert.index, None, l))
            else:
                # Vertices on hard edges cannot be shared and must be duplicated per-face
                return builder.add_unique_vertex(
                    lambda vertex_buffer: vertex_fetcher.extract_vertex(vertex_buffer, l.vert.index, l.calc_normal(),
                                                                        l))

        triangle = (
            parse_loop_elem(l0),
            parse_loop_elem(l1),
            parse_loop_elem(l2),
        )
        builder.add_triangle(triangle)

    return [builder for builder in submesh_builders if len(builder.vertices)]


def split_submesh_builder_by_bones(skinned_submesh_builder: SkinnedSubmeshBuilder) -> List[SkinnedSubmeshBuilder]:
    pass


# @overload
# def submesh_builder_to_gmd(submesh_builder: SkinnedSubmeshBuilder) -> GMDSkinnedMesh:
#     pass
# def submesh_builder_to_gmd(submesh_builder: SubmeshBuilder) -> GMDMesh:
#     pass


def split_skinned_blender_mesh_object(object: bpy.types.Object, materials: List[GMDAttributeSet], bone_limit: int,
                                      error: ErrorReporter) -> List[GMDSkinnedMesh]:
    pass


def split_unskinned_blender_mesh_object(context: bpy.types.Context, object: bpy.types.Object,
                                        materials: List[GMDAttributeSet], error: ErrorReporter) -> List[GMDMesh]:
    # Apply the dependency graph to the mesh
    # https://blender.stackexchange.com/a/146911
    dg = context.evaluated_depsgraph_get()

    bm = bmesh.new()
    bm.from_object(object, dg)
    bm.verts.ensure_lookup_table()
    bm.verts.index_update()

    submesh_builders = split_mesh_by_material(object.name, bm, Matrix.Identity(4), materials, False, vertex_group_mapping={}, error=error)

    bm.free()

    return [builder.build_to_gmd(materials) for builder in submesh_builders]
