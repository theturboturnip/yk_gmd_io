import array
import collections
import re
from dataclasses import dataclass
from typing import List, Tuple, Dict, Callable, Set, overload, Union, cast, Optional
#
import bmesh
import bpy
from bmesh.types import BMLayerItem, BMVert, BMLoop

from yk_gmd_blender.blender.export.mesh_exporter.builders import SubmeshBuilder, SkinnedSubmeshBuilder, SkinnedSubmeshBuilderSubset
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDSkinnedMesh, GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer, GMDVertexBufferLayout, BoneWeight4, BoneWeight, VecStorage
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter

from mathutils import Vector, Matrix


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
    tangent_w_layer: Optional[bpy.types.MeshLoopColorLayer]
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

    def normal_for(self, loop: bpy.types.MeshLoopTriangle, tri_index: int, normal: Optional[Vector]):
        normal = (self.transformation_direction @ (normal if normal is not None else Vector(loop.split_normals[tri_index]))).resized(4)
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
                    self.error.recoverable(f"UV{uv_idx} has values outside of the storable range. Expected between 0 and 1, got {vec}")
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

    def extract_vertex(self, vertex_buffer: GMDVertexBuffer, i: int, normal: Optional[Vector], loop: bpy.types.MeshLoopTriangle, tri_index: int):
        if vertex_buffer.layout != self.vertex_layout:
            self.error.fatal(f"VertexFetcher told to fetch vertex for a buffer with a different layout")

        vertex_buffer.pos.append((self.transformation_position @ self.mesh.vertices[i].co).resized(4))
        if vertex_buffer.bone_weights is not None:
            vertex_buffer.bone_weights.append(self.boneweights_for(i))
        if vertex_buffer.normal is not None:
            vertex_buffer.normal.append(self.normal_for(loop, tri_index, normal))
        if vertex_buffer.tangent is not None:
            vertex_buffer.tangent.append(self.tangent_for(loop, tri_index))
        if vertex_buffer.col0 is not None:
            vertex_buffer.col0.append(self.col0_for(loop, tri_index))
        if vertex_buffer.col1 is not None:
            vertex_buffer.col1.append(self.col1_for(loop, tri_index))
        for uv_idx in range(len(self.uv_layers)):
            vertex_buffer.uvs[uv_idx].append(self.uv_for(uv_idx, loop, tri_index))


def split_mesh_by_material(mesh_name: str, mesh: bpy.types.Mesh, object_blender_transformation: Matrix, attribute_sets: List[GMDAttributeSet], skinned: bool,
                           vertex_group_mapping: Dict[int, GMDBone], error: ErrorReporter) -> Union[
    List[SubmeshBuilder], List[SkinnedSubmeshBuilder]]:
    col0_layer = mesh.vertex_colors["Color0"] if "Color0" in mesh.vertex_colors else None
    col1_layer = mesh.vertex_colors["Color1"] if "Color1" in mesh.vertex_colors else None
    tangent_w_layer = mesh.vertex_colors["TangentW"] if "TangentW" in mesh.vertex_colors else None

    uv_primary = "UV_Primary"
    uv_numbered_regex = re.compile(r'UV(\d+)')

    primary_uv_layer = mesh.uv_layers[uv_primary] if uv_primary in mesh.uv_layers else mesh.uv_layers.active
    numbered_uv_layers = {}
    if mesh.uv_layers:
        for name, layer in mesh.uv_layers.items():
            match = uv_numbered_regex.match(name)
            if match:
                uv_i = int(match.group(1))
                if uv_i in numbered_uv_layers:
                    error.recoverable(f"Found multiple possible layers for UV{uv_i}, will take latest one")
                numbered_uv_layers[uv_i] = layer
    if mesh.vertex_colors:
        for name, layer in mesh.vertex_colors.items():
            match = uv_numbered_regex.match(name)
            if match:
                uv_i = int(match.group(1))
                if uv_i in numbered_uv_layers:
                    error.recoverable(f"Found multiple possible layers for UV{uv_i}, will take latest one")
                numbered_uv_layers[uv_i] = layer

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
                                       tangent_w_layer=tangent_w_layer,
                                       uv_primary=primary_uv_layer,
                                       uv_numbered=numbered_uv_layers,
                                       error=error)
        vertex_fetchers.append(vertex_fetcher)

    for tri_loops in mesh.loop_triangles:
        if not (0 <= tri_loops.material_index < len(attribute_sets)):
            error.recoverable(
                f"Mesh {mesh_name} has a face with out-of-bounds material index {tri_loops.vertices[i].face.material_index}. It will be skipped!")
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
