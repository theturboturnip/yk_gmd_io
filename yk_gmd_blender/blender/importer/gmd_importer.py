import array
import collections
import os
import re
from typing import Dict, Iterable, List, Tuple, Union, cast, TypeVar, Optional

from mathutils import Matrix, Vector, Quaternion

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       CollectionProperty)
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper
import bmesh
from yk_gmd_blender.blender.common import armature_name_for_gmd_file, root_name_for_gmd_file

from yk_gmd_blender.blender.error_reporter import BlenderErrorReporter
from yk_gmd_blender.blender.materials import YAKUZA_SHADER_NODE_GROUP, get_yakuza_shader_node_group
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDMaterial, GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import BoneWeight4, GMDVertexBuffer, BoneWeight
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_object import GMDSkinnedObject, GMDUnskinnedObject
from yk_gmd_blender.yk_gmd.v2.errors.error_classes import GMDImportExportError
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import StrictErrorReporter, LenientErrorReporter, ErrorReporter
from yk_gmd_blender.yk_gmd.v2.io import read_abstract_scene
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType


class ImportGMD(Operator, ImportHelper):
    """Loads a GMD file into blender"""
    bl_idname = "import_scene.gmd"
    bl_label = "Import Yakuza GMD"

    filter_glob: StringProperty(default="*.gmd", options={"HIDDEN"})

    strict: BoolProperty(name="Strict File Import",
                         description="If True, will fail the import even on recoverable errors.",
                         default=True)

    import_hierarchy: BoolProperty(name="Import Hierarchy",
                                   description="If True, will import the full node hierarchy including skeleton bones. "
                                               "This is required if you want to export the scene later. "
                                               "Skinned meshes will be imported with bone weights.",
                                   default=True)
    import_objects: BoolProperty(name="Import Objects",
                                 description="If True, will import the full object hierarchy. "
                                             "This is required if you want to export the scene later.",
                                 default=True)
    import_materials: BoolProperty(name="Import Materials",
                                   description="If True, will import materials. If False, all objects will not have any materials. "
                                               "This is required if you want to export the scene later.",
                                   default=True)

    fuse_object_meshes: BoolProperty(name="Fuse Object Meshes",
                                     description="If True, meshes that are attached to the same object will have duplicate vertices removed.",
                                     default=True)

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = True  # No animation.

        # When properties are added, use "layout.prop" here to display them
        # layout.prop(self, 'load_materials')
        # layout.prop(self, 'load_bones')
        # layout.prop(self, 'validate_meshes')
        # layout.prop(self, 'merge_meshes')
        layout.prop(self, 'strict')
        layout.prop(self, 'import_hierarchy')
        layout.prop(self, 'import_objects')
        layout.prop(self, 'import_materials')
        layout.prop(self, 'fuse_object_meshes')

    def execute(self, context):
        base_error_reporter = StrictErrorReporter() if self.strict else LenientErrorReporter()
        error_reporter = BlenderErrorReporter(self.report, base_error_reporter)

        try:
            self.report({"INFO"}, "Extracting abstract scene...")
            gmd_scene = read_abstract_scene(self.filepath, error_reporter)
            self.report({"INFO"}, "Finished extracting abstract scene")

            # Check for bone name overlap
            # Only bones are added to the overall armature, not objects
            # But the bones are referenced by name, so we need to check if there are multiple bones with the same name
            bones_depth_first = [node for node in gmd_scene.overall_hierarchy.depth_first_iterate() if isinstance(node, GMDBone)]
            bone_names = {bone.name for bone in bones_depth_first}
            if len(bone_names) != len(bones_depth_first):
                # Find the duplicate names by listing them all, and removing one occurence of each name
                # The only names left will be duplicates
                bone_name_list = [bone.name for bone in bones_depth_first]
                for name in bone_names:
                    bone_name_list.remove(name)
                duplicate_names = set(bone_name_list)
                error_reporter.fatal(f"Some bones don't have unique names - found duplicates {duplicate_names}")

            # Check that objects do not have bones underneath them
            objects_depth_first = [node for node in gmd_scene.overall_hierarchy.depth_first_iterate() if not isinstance(node, GMDBone)]
            def check_objects_children(object: GMDNode):
                for child in object.children:
                    if isinstance(child, GMDBone):
                        error_reporter.fatal(f"Object {object.name} has child {child.name} which is a GMDBone - The importer expects that objects do not have bones as children")
                    check_objects_children(child)
            for object in objects_depth_first:
                check_objects_children(object)

            scene_creator = GMDSceneCreator(gmd_scene, error_reporter)
            gmd_collection = scene_creator.make_collection(context)

            if self.import_hierarchy:
                gmd_armature = scene_creator.make_bone_hierarchy(context, gmd_collection)

            if self.import_objects:
                scene_creator.make_objects(context, gmd_collection, gmd_armature if self.import_hierarchy else None,
                                           use_materials=self.import_materials, fuse_vertices=self.fuse_object_meshes)#self.import_materials)

            return {'FINISHED'}
        except GMDImportExportError as e:
            print(e)
            self.report({"ERROR"}, str(e))
        return {'CANCELLED'}

TMesh = TypeVar('TMesh', bound=GMDMesh)

class GMDSceneCreator:
    gmd_scene: GMDScene
    material_id_to_blender: Dict[int, bpy.types.Material]
    gmd_to_blender_world: Matrix

    def __init__(self, gmd_scene: GMDScene, error: ErrorReporter):
        self.gmd_scene = gmd_scene
        self.material_id_to_blender = {}
        self.gmd_to_blender_world = Matrix((
            Vector((1, 0, 0, 0)),
            Vector((0, 0, -1, 0)),
            Vector((0, 1, 0, 0)),
            Vector((0, 0, 0, 1)),
        ))
        self.error = error

    def make_collection(self, context: bpy.types.Context) -> bpy.types.Collection:
        collection_name = root_name_for_gmd_file(self.gmd_scene)
        collection = bpy.data.collections.new(collection_name)
        # TODO: This was just sort of copied from XNALara - it's probably better to just take the scene collections?
        # view_layer = bpy.context.view_layer
        # active_collection = view_layer.active_layer_collection.collection
        # active_collection.children.link(collection)
        context.collection.children.link(collection)
        return collection

    def make_bone_hierarchy(self, context: bpy.types.Context, collection: bpy.types.Collection) -> bpy.types.Object:
        armature_name = armature_name_for_gmd_file(self.gmd_scene)
        armature = bpy.data.armatures.new(f"{armature_name}")
        armature.display_type = 'STICK'
        armature_obj = bpy.data.objects.new(f"{armature_name}", armature)
        armature_obj.show_in_front = True

        collection.objects.link(armature_obj)

        context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT')

        # Idea for regex taken from https://github.com/johnzero7/XNALaraMesh/blob/eaccfddf39aef8d3cb60a50c05f2585398fe26ca/import_xnalara_model.py#L356
        # The actual regex has been changed tho
        twist_regex = re.compile(r'[-_](twist|adj|sup)\d*([-_\s]|$)')

        parent_world_yakuza_space_matrices: Dict[str, Matrix] = {}

        for gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            if not isinstance(gmd_node, GMDBone):
                continue

            bone = armature.edit_bones.new(f"{gmd_node.name}")
            bone.use_relative_parent = False

            # Find the local->world matrix for this bone, and it's parent
            # if gmd_node.matrix:
            #     this_bone_matrix = self.gmd_to_blender_world @ gmd_node.matrix.inverted()
            # elif gmd_node.parent:
            #     this_bone_matrix = armature.edit_bones[gmd_node.parent.name].matrix @ (Matrix.Translation(gmd_node.pos.xyz) @ gmd_node.rot.to_matrix().resize_4x4() @ Matrix.Diagonal(gmd_node.scale.xyz).resize_4x4())
            # else:
            #     this_bone_matrix = self.gmd_to_blender_world @ Matrix.Identity(4)

            if gmd_node.parent:
                parent_matrix = parent_world_yakuza_space_matrices[gmd_node.parent.name]
            else:
                parent_matrix = Matrix.Identity(4)

            rot_matrix = gmd_node.rot.to_matrix()
            rot_matrix.resize_4x4()
            this_bone_matrix = parent_matrix @ (Matrix.Translation(gmd_node.pos.xyz) @ rot_matrix)# @ Matrix.Diagonal(gmd_node.scale.xyz).resize_4x4())
            parent_world_yakuza_space_matrices[gmd_node.name] = this_bone_matrix

            #print(f"{gmd_node.name}")
            #if isinstance(gmd_node, GMDBone):
            bone.use_deform = True

            # Take a page out of XNA Importer's book for bone tails - make roots just stick towards the camera
            # and make nodes with (non-twist) children try to go to the average of those children's positions
            if not gmd_node.parent:
                #print("Using basic Z-delta for tail")
                tail_delta = Vector((0, 0, 0.5))
            elif twist_regex.search(gmd_node.name) and not gmd_node.children:
                # We have a parent, and we're a twist bone
                # "Twist Bones" allow things like shoulders to be twisted when the arm is bent.
                # They are separate from the main arm bone, and shouldn't really extend in the same direction
                # as the arm bone, as otherwise it would be difficult to tell them apart.

                # First, check if we have siblings in a similar position to ours - these are the bones we want to be different from
                adjacent_siblings = [child for child in gmd_node.parent.children if child is not gmd_node and (child.pos - gmd_node.pos).length < 0.01]
                if adjacent_siblings:
                    # If we're trying to be different from our sibling, we pick a direction that is perpendicular to the direction we would normally pick

                    # Pick a vector perpendicular to the parent direction
                    parent_dir = (gmd_node.pos.xyz) # gmd_node.pos is relative to the parent already
                    original_parent_dir_length = parent_dir.length
                    parent_dir.normalize()
                    perp_dir = Vector((0, 0, 1))
                    if parent_dir.dot(perp_dir) > 0.99:
                        # Parent and proposed perpendicular direction are basically the same, cross product won't work
                        # Choose a different one
                        perp_dir = Vector((0, 1, 0))

                    tail_delta_dir = parent_dir.cross(perp_dir)
                    tail_delta_dir.normalize()

                    #tail_delta_dir = perp_dir.cross(guaranteed_perp)

                    # Cross product can have bad symmetry - bones on opposite sides
                    # Fix this by picking the delta which moves the tail the farthest possible distance from the origin
                    # This will choose consistent directions regardless of which side of the Y axis you are on
                    distance_from_origin_with_positive = (this_bone_matrix @ (tail_delta_dir * 0.1)).length
                    distance_from_origin_with_negative = (this_bone_matrix @ (-tail_delta_dir * 0.1)).length
                    if distance_from_origin_with_negative > distance_from_origin_with_positive:
                        tail_delta_dir = -tail_delta_dir

                    # Extend the tail in the direction of the delta, for the same length between this bone and our parent
                    #print(f"Using twist formula - parent_dir {parent_dir} perp_dir {perp_dir} tail_delta_dir {tail_delta_dir}")
                    tail_delta = (tail_delta_dir.xyz * 0.1)
                else:
                    # There aren't any bones we have to differentiate ourselves from -> just follow the parent delta, like the default for having no children
                    tail_delta = gmd_node.pos.xyz.normalized() * 0.05
            else:
                # This either isn't a twist bone or it has children - most likely this just isn't a twist bone, as twist bones generally don't have children anyway
                # If there are non-twist children, set the tail to the average of their positions
                countable_children_gmd_positions = [child.pos.xyz for child in gmd_node.children if not twist_regex.search(child.name)]

                if countable_children_gmd_positions:
                    #print(f"Has usable children - using delta from average of {countable_children_gmd_positions}")
                    tail_delta = sum(countable_children_gmd_positions, Vector((0,0,0))) / len(countable_children_gmd_positions)
                else:
                    #print(f"No usable children - just extending in direction of pos, which is {gmd_node.pos.xyz}")
                    # Extend the tail in the direction of the parent
                    # gmd_node.pos.xyz is relative to the parent already
                    if gmd_node.pos.xyz.length < 0.00001:
                        tail_delta = Vector((0, 0, 0.05))
                    else:
                        tail_delta = gmd_node.pos.xyz.normalized() * 0.05 # + (gmd_node.pos.xyz - gmd_node.parent.pos.xyz)
            # else:
            #     bone.use_deform = False
            #     print(f"Not deforming - using straight offset")
            #     tail_delta = Vector((0, 0, 0.5))

            #bone.matrix = self.gmd_to_blender_world @ this_bone_matrix
            bone.head = self.gmd_to_blender_world @ this_bone_matrix @ Vector((0,0,0))
            bone.tail = self.gmd_to_blender_world @ this_bone_matrix @ tail_delta
            # TODO: If your head is close to your parent's tail, turn on "connected to parent"
            bone.parent = armature.edit_bones[gmd_node.parent.name] if gmd_node.parent else None

        bpy.ops.object.mode_set(mode='POSE')
        # todo - set custom shape for object bones (and bones with no parent?) (and twist bones????)
        #bpy.data.objects['Armature'].pose.bones['Bone1'].custom_shape = bpy.data.objects['wgt_bone1']

        # todo - XNALara sets custom colors for things based on the objects they affect - we could do something like that too?
        # https://github.com/johnzero7/XNALaraMesh/blob/eaccfddf39aef8d3cb60a50c05f2585398fe26ca/import_xnalara_model.py#L748
        # having color differentiation may make it easier to navigate

        bpy.ops.object.mode_set(mode='OBJECT')

        return armature_obj

    def make_objects(self, context: bpy.types.Context, collection: bpy.types.Collection, armature_object: Optional[bpy.types.Object], use_materials: bool, fuse_vertices: bool):
        temp_mesh = bpy.data.meshes.new(".temp")

        vertex_group_list = [node.name for node in self.gmd_scene.overall_hierarchy.depth_first_iterate() if isinstance(node, GMDBone)]
        vertex_group_indices = {
            name: i
            for i, name in enumerate(vertex_group_list)
        }

        gmd_objects = {}

        for gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            if not isinstance(gmd_node, (GMDSkinnedObject, GMDUnskinnedObject)):
                continue

            is_skinned = isinstance(gmd_node, GMDSkinnedObject)
            print(f"making object {gmd_node.name}, is_skinned {is_skinned} from meshes {gmd_node.mesh_list}")

            # List of all attribute set IDs referenced by an object
            # Make a list from a set to avoid duplicates
            gmd_attr_set_ids = list({id(mesh.attribute_set) for mesh in gmd_node.mesh_list})
            # TODO: This method probably wastes a lot of time creating new BMeshes. It could be better to just append to the overall_bm instead of making a new one, sending it to a Mesh, then adding it back.
            overall_bm = bmesh.new()
            blender_material_list = []
            for i, attr_set_id in enumerate(gmd_attr_set_ids):
                merged_gmd_mesh = self.make_merged_gmd_mesh(
                    [gmd_mesh for gmd_mesh in gmd_node.mesh_list if id(gmd_mesh.attribute_set) == attr_set_id], remove_dupes=fuse_vertices)
                if use_materials:
                    blender_material_list.append(self.make_material(collection, merged_gmd_mesh.attribute_set))
                    new_bmesh = self.gmd_to_bmesh(merged_gmd_mesh, vertex_group_indices, material_index=i)
                else:
                    new_bmesh = self.gmd_to_bmesh(merged_gmd_mesh, vertex_group_indices, material_index=0)
                new_bmesh.to_mesh(temp_mesh)
                new_bmesh.free()
                overall_bm.from_mesh(temp_mesh)

            # Create a mesh object for it
            overall_mesh = bpy.data.meshes.new(gmd_node.name)
            overall_bm.to_mesh(overall_mesh)
            overall_bm.free()
            # if self.validate_meshes:
            #     mesh.validate()
            if use_materials:
                for mat in blender_material_list:
                    overall_mesh.materials.append(mat)
            mesh_obj: bpy.types.Object = bpy.data.objects.new(gmd_node.name, overall_mesh)

            if is_skinned:
                if armature_object:
                    mesh_obj.parent = armature_object
                    for name in vertex_group_list:
                        mesh_obj.vertex_groups.new(name=name)
                    modifier = mesh_obj.modifiers.new(type='ARMATURE', name="Armature")
                    modifier.object = armature_object
            else:
                if gmd_node.parent:
                    if gmd_node.parent.node_type == NodeType.MatrixTransform:
                        child_constraint = mesh_obj.constraints.new("CHILD_OF")
                        child_constraint.target = armature_object
                        child_constraint.subtarget = gmd_node.parent.name
                    else:
                        mesh_obj.parent = gmd_objects[id(gmd_node.parent)]

            # Objects have positions
            mesh_obj.location = self.gmd_to_blender_world @ gmd_node.pos.xyz
            # TODO: Use a proper function for this - I hate that the matrix multiply doesn't work
            mesh_obj.rotation_quaternion = Quaternion((gmd_node.rot.w, gmd_node.rot.x, -gmd_node.rot.z, gmd_node.rot.y))#self.gmd_to_blender_world @ gmd_node.rot
            # TODO - When applying gmd_to_blender_world to (1,1,1) you get (1,-1,1) out. This undoes the previous scaling applied to the vertices.
            # .xzy is used to swap the components for now, but there's probably a better way?
            #mesh_obj.scale = self.gmd_to_blender_world @ gmd_node.scale.xyz
            mesh_obj.scale = gmd_node.scale.xzy

            gmd_objects[id(gmd_node)] = mesh_obj
            collection.objects.link(mesh_obj)

        bpy.data.meshes.remove(temp_mesh)

    def gmd_to_bmesh(self, gmd_mesh: Union[GMDMesh, GMDSkinnedMesh], vertex_group_indices: Dict[str, int], material_index: int) -> bmesh.types.BMesh:
        apply_bone_weights = isinstance(gmd_mesh, GMDSkinnedMesh)

        bm = bmesh.new()

        # Create initial vertices (position, normal, bone weights if present)
        if apply_bone_weights:
            deform = bm.verts.layers.deform.new("Vertex Weights")

        vtx_buffer = gmd_mesh.vertices_data
        for i in range(len(vtx_buffer)):
            vert = bm.verts.new(self.gmd_to_blender_world @ vtx_buffer.pos[i].xyz)
            if vtx_buffer.normal:
                # apply the matrix to normal.xyz.resized(4) to set the w component to 0 - normals cannot be translated!
                # Just using .xyz would make blender apply a translation (TODO - check this?)
                vert.normal = (self.gmd_to_blender_world @ (vtx_buffer.normal[i].xyz.resized(4))).xyz
            # Tangents cannot be applied
            if apply_bone_weights and vtx_buffer.bone_weights:
                for bone_weight in vtx_buffer.bone_weights[i]:
                    if bone_weight.weight > 0:
                        if bone_weight.bone >= len(gmd_mesh.relevant_bones):
                            print(f"bone out of bounds - bone {bone_weight.bone} in {[b.name for b in gmd_mesh.relevant_bones]}")
                            print(f"mesh len = {len(vtx_buffer)}")
                        vertex_group_index = vertex_group_indices[gmd_mesh.relevant_bones[bone_weight.bone].name]
                        vert[deform][vertex_group_index] = bone_weight.weight
        # Set up the indexing table inside the bmesh so lookups work
        bm.verts.ensure_lookup_table()
        bm.verts.index_update()

        # Connect triangles
        def add_face_to_bmesh(face: Tuple[int, int, int]):
            try:
                # blender has a reversed winding order
                face = bm.faces.new((bm.verts[face[0]], bm.verts[face[2]], bm.verts[face[1]]))
            except ValueError:
                pass
            else:
                face.smooth = True
                face.material_index = material_index

        for i in range(0, len(gmd_mesh.triangle_indices), 3):
            tri_idxs = gmd_mesh.triangle_indices[i:i + 3]
            if len(set(tri_idxs)) != 3:
                continue
            if 0xFFFF in tri_idxs:
                self.error.recoverable(f"Found an 0xFFFF index inside a triangle_indices list! That shouldn't happen.")
                continue
            add_face_to_bmesh(tri_idxs)

        # Color0
        if vtx_buffer.col0:
            col0_layer = bm.loops.layers.color.new("color0")
            for face in bm.faces:
                for loop in face.loops:
                    color = vtx_buffer.col0[loop.vert.index]
                    loop[col0_layer] = (color.x, color.y, color.z, color.w)

        # Color1
        if vtx_buffer.col1:
            col1_layer = bm.loops.layers.color.new("color1")
            for face in bm.faces:
                for loop in face.loops:
                    color = vtx_buffer.col1[loop.vert.index]
                    loop[col1_layer] = (color.x, color.y, color.z, color.w)

        # If UVs are present, add them
        for i, uv in enumerate(vtx_buffer.uvs):
            uv_layer = bm.loops.layers.uv.new(f"TexCoords{i}")
            for face in bm.faces:
                for loop in face.loops:
                    original_uv = uv[loop.vert.index]
                    # TODO - check if we actually need to rearrange 2D UVs
                    # TODO - fuuuuck. blender doesn't accept 3D/4D UVs. How the hell are we supposed to handle them?
                    loop[uv_layer].uv = original_uv.xy

        # Removed unused verts
        # Typically the mesh passed into this function comes from make_merged_gmd_mesh, which "fuses" vertices by changing the index buffer
        # However, the unused verts themselves are still in the buffer, and should be removed.
        # THIS MUST ONLY HAPPEN AFTER ALL OTHER LOADING - otherwise different data channels will be messed up
        unused_verts = [v for v in bm.verts if not v.link_faces]
        print(f"Bmesh removing {len(unused_verts)} verts")
        # equiv of bmesh.ops.delete(bm, geom=verts, context='VERTS')
        for v in unused_verts:
            bm.verts.remove(v)
        bm.verts.ensure_lookup_table()
        bm.verts.index_update()
        print(f"total vert count = {len(bm.verts)}")

        return bm

    def make_merged_gmd_mesh(self, gmd_meshes: List[TMesh], remove_dupes: bool = True) -> TMesh:
        from mathutils import kdtree
        """
        Given multiple GMD Meshes that use the same material, merge them into a single GMDMesh that uses a single vertex buffer and index set.
        :param gmd_meshes:
        :return: A merged GMD Mesh. Only has triangle indices, not strips.
        """
        if len(gmd_meshes) == 1:
            return gmd_meshes[0]

        if not all(gmd_mesh.attribute_set is gmd_meshes[0].attribute_set for gmd_mesh in gmd_meshes):
            self.error.fatal("Trying to merge GMDMeshes that do not share an attribute set!")

        making_skinned_mesh = isinstance(gmd_meshes[0], GMDSkinnedMesh)
        print(f"Merging {gmd_meshes}")
        print(f"Is skinned {making_skinned_mesh}")

        if making_skinned_mesh:
            # Skinned meshes are more complicated because vertices reference bones using a *per-mesh* index into that "relevant_bones" list
            # These indices have to be changed for the merged mesh, because each mesh will usually have a different "relevant_bones" list
            gmd_meshes = cast(List[GMDSkinnedMesh], gmd_meshes)
            # Handling skinned meshes
            relevant_bones = gmd_meshes[0].relevant_bones[:]
            merged_vertex_buffer = gmd_meshes[0].vertices_data[:]
            for gmd_mesh in gmd_meshes[1:]:
                bone_index_mapping = {}
                for i, bone in enumerate(gmd_mesh.relevant_bones):
                    if bone not in relevant_bones:
                        relevant_bones.append(bone)
                    bone_index_mapping[i] = relevant_bones.index(bone)

                print(bone_index_mapping)

                def remap_weight(bone_weight: BoneWeight):
                    # If the weight is 0 the bone is unused, so don't remap it.
                    # It's usually 0, which is a valid remappable value, but if we remap it then BoneWeight(bone=0, weight=0) != BoneWeight(bone=remapped 0, weight=0)
                    if bone_weight.weight == 0:
                        return bone_weight
                    else:
                        return BoneWeight(bone_index_mapping[bone_weight.bone], bone_weight.weight)

                index_start_to_adjust_bones = len(merged_vertex_buffer)
                merged_vertex_buffer += gmd_mesh.vertices_data
                for i in range(index_start_to_adjust_bones, len(merged_vertex_buffer)):
                    old_weights = merged_vertex_buffer.bone_weights[i]
                    merged_vertex_buffer.bone_weights[i] = (
                        remap_weight(old_weights[0]),
                        remap_weight(old_weights[1]),
                        remap_weight(old_weights[2]),
                        remap_weight(old_weights[3]),
                    )
            print(len(relevant_bones))
        else:
            merged_vertex_buffer = gmd_meshes[0].vertices_data[:]
            for gmd_mesh in gmd_meshes[1:]:
                merged_vertex_buffer += gmd_mesh.vertices_data

        # Mapping of vertex index pre-merge -> merged vertex index
        # i.e. if the merger decides vertex 5 and vertex 7 are merged, mapping[5] = 5 and mapping[7] = 5
        merged_indices_map = {}
        dupes_of_map = collections.defaultdict(list)
        unused_indices = set()
        if remove_dupes:
            # Build a 3D tree of positions, so we can efficiently find the closest vertices
            equality_check_distance = 0.000001
            actual_equality_epsilon = 0.0

            size = len(merged_vertex_buffer)
            kd = kdtree.KDTree(size)
            for i, pos in enumerate(merged_vertex_buffer.pos):
                kd.insert(pos.xyz, i)
            kd.balance()

            merged_indices_map = {
                i:i
                for i in range(len(merged_vertex_buffer))
            }

            rejects = set()

            for i, pos in enumerate(merged_vertex_buffer.pos):
                if i in unused_indices:
                    continue

                for (co, index, dist) in kd.find_range(pos.xyz, equality_check_distance):
                    if index == i:
                        continue

                    if index in unused_indices:
                        continue

                    if dist <= actual_equality_epsilon and merged_vertex_buffer.verts_equalish(i, index):
                        unused_indices.add(index)
                        merged_indices_map[index] = i
                        dupes_of_map[i].append(index)
                    else:
                        # print(f"Rejected index {index}, which was of distance {dist} vs {actual_equality_epsilon}")
                        rejects.add(index)

            total_verts = len(merged_vertex_buffer) - len(unused_indices)
            print(
                f"After merging {len(gmd_meshes)} meshes, {len(unused_indices)} vertex indices were determined to be redundant. Expected total verts = {total_verts}")
            print(f"total rejects (will include doubles?) {len(rejects)}")

        index_maps = []
        overall_i = 0
        for gmd_mesh in gmd_meshes:
            index_map = {}
            if merged_indices_map:
                for i in range(len(gmd_mesh.vertices_data)):
                    index_map[i] = merged_indices_map[overall_i]
                    overall_i += 1
            else:
                for i in range(len(gmd_mesh.vertices_data)):
                    index_map[i] = overall_i
                    overall_i += 1

            index_maps.append(index_map)

        #import array
        triangle_indices = array.array('i')
        for gmd_mesh, index_map in zip(gmd_meshes, index_maps):
            for index in gmd_mesh.triangle_indices:
                triangle_indices.append(index_map[index])

        if making_skinned_mesh:
            print(len(relevant_bones))
            print({x.bone for bone_weights in merged_vertex_buffer.bone_weights for x in bone_weights})
            return GMDSkinnedMesh(
                attribute_set=gmd_meshes[0].attribute_set,

                vertices_data=merged_vertex_buffer,
                triangle_indices=triangle_indices,
                triangle_strip_noreset_indices=array.array('i'),
                triangle_strip_reset_indices=array.array('i'),

                relevant_bones=relevant_bones
            )
        else:
            return GMDMesh(
                attribute_set=gmd_meshes[0].attribute_set,

                vertices_data=merged_vertex_buffer,
                triangle_indices=triangle_indices,
                triangle_strip_noreset_indices=array.array('i'),
                triangle_strip_reset_indices=array.array('i'),
            )

    def make_material(self, collection: bpy.types.Collection, gmd_attribute_set: GMDAttributeSet) -> bpy.types.Material:
        if id(gmd_attribute_set) in self.material_id_to_blender:
            return self.material_id_to_blender[id(gmd_attribute_set)]

        def make_yakuza_node_group(node_tree: bpy.types.NodeTree):
            node = node_tree.nodes.new("ShaderNodeGroup")
            node.node_tree = get_yakuza_shader_node_group()
            return node

        material_name = f"{collection.name_full}_{gmd_attribute_set.shader.name}"

        material = bpy.data.materials.new(material_name)
        material.use_backface_culling = True
        material.use_nodes = True
        material.node_tree.nodes.clear()
        yakuza_shader_node_group = make_yakuza_node_group(material.node_tree)
        yakuza_shader_node_group.location = (0, 0)
        yakuza_shader_node_group.width = 400
        yakuza_shader_node_group.height = 800
        output_node = material.node_tree.nodes.new("ShaderNodeOutputMaterial")
        output_node.location = (500, 0)
        material.node_tree.links.new(yakuza_shader_node_group.outputs["Shader"], output_node.inputs["Surface"])

        self.material_id_to_blender[id(gmd_attribute_set)] = material
        return material

def menu_func_import(self, context):
    self.layout.operator(ImportGMD.bl_idname, text='Yakuza GMD (.gmd)')
