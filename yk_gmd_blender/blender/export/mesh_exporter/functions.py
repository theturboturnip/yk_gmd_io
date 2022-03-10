import re
from typing import List, Dict, Union

#
import bmesh
import bpy
from mathutils import Vector, Matrix

from yk_gmd_blender.blender.export.mesh_exporter.builders import SubmeshBuilder, SkinnedSubmeshBuilder, \
    SkinnedSubmeshBuilderSubset, VertexFetcher
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDSkinnedMesh, GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter


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
            return builder.add_vertex(tri_loops.vertices[i],
                                      vertex_fetcher,
                                      tri_loops,
                                      i)

        triangle = (
            parse_loop_elem(0),
            parse_loop_elem(1),
            parse_loop_elem(2),
        )
        builder.add_triangle(triangle)

    return [builder for builder in submesh_builders if len(builder.vertices)]


def split_submesh_builder_by_bones(skinned_submesh_builder: SkinnedSubmeshBuilder, bone_limit: int, object_name: str, error: ErrorReporter) -> List[SkinnedSubmeshBuilder]:
    skinned_submesh_builder.reduce_to_used_bones()
    if not skinned_submesh_builder.relevant_gmd_bones:
        error.fatal(f"A submesh of {object_name} does not reference any bones. Make sure all of the vertices of {object_name} have their bone weights correct!")
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


def prepare_mesh(context: bpy.types.Context, object: bpy.types.Object):
    dg = context.evaluated_depsgraph_get()

    mesh = object.evaluated_get(dg).data

    # TODO: Creating a new mesh just to triangulate sucks for perf I'd expect
    tempmesh = bmesh.new()
    tempmesh.from_mesh(mesh)

    bmesh.ops.triangulate(tempmesh, faces=tempmesh.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')

    # Finish up, write the bmesh back to the mesh
    tempmesh.to_mesh(mesh)
    tempmesh.free()

    # Now it's triangulated we can calculate tangents (TODO calc_normals_split may not be necessary anymore)
    mesh.calc_normals_split()
    mesh.calc_tangents()
    mesh.calc_loop_triangles()
    mesh.transform(object.matrix_world)

    return mesh

def split_skinned_blender_mesh_object(context: bpy.types.Context, object: bpy.types.Object, materials: List[GMDAttributeSet], bone_name_map: Dict[str, GMDBone], bone_limit: int,
                                      error: ErrorReporter) -> List[GMDSkinnedMesh]:
    # Apply the dependency graph to the mesh
    # https://blender.stackexchange.com/a/146911
    mesh = prepare_mesh(context, object)

    vertex_group_mapping = {
        i: bone_name_map[group.name]
        for i, group in enumerate(object.vertex_groups)
        if group.name in bone_name_map
    }

    submesh_builders = split_mesh_by_material(object.name, mesh, Matrix.Identity(4), materials, True,
                                              vertex_group_mapping, error=error)


    gmd_skinned_meshes = []
    print(f"Exporting skinned meshes for {object.name}")
    for builder in submesh_builders:
        if not isinstance(builder, SkinnedSubmeshBuilder):
            error.fatal(f"split_mesh_by_material gave a {type(builder).__name__} when a SkinnedSubmeshBuilder was expected")
        for split_builder in split_submesh_builder_by_bones(builder, bone_limit, object.name, error):
            print(f"Adding skinned mesh of vert count {len(split_builder.vertices)}")
            gmd_skinned_meshes.append(split_builder.build_to_gmd(materials))

    return gmd_skinned_meshes


def split_unskinned_blender_mesh_object(context: bpy.types.Context, object: bpy.types.Object,
                                        materials: List[GMDAttributeSet], error: ErrorReporter) -> List[GMDMesh]:
    # Apply the dependency graph to the mesh
    # https://blender.stackexchange.com/a/146911
    mesh = prepare_mesh(context, object)

    submesh_builders = split_mesh_by_material(object.name, mesh, Matrix.Identity(4), materials, False, vertex_group_mapping={}, error=error)

    return [builder.build_to_gmd(materials) for builder in submesh_builders]
