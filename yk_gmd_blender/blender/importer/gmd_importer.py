import array
import collections
import os
import re
from typing import Dict, List, Tuple, Union, cast, TypeVar, Optional

from mathutils import Matrix, Vector, Quaternion

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       CollectionProperty)
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
import bmesh
from yk_gmd_blender.blender.common import armature_name_for_gmd_file, root_name_for_gmd_file
from yk_gmd_blender.blender.coordinate_converter import transform_to_matrix, transform_rotation_gmd_to_blender

from yk_gmd_blender.blender.error_reporter import BlenderErrorReporter
from yk_gmd_blender.blender.importer.mesh_importer import gmd_meshes_to_bmesh
from yk_gmd_blender.blender.materials import get_yakuza_shader_node_group, \
    set_yakuza_shader_material_from_attributeset
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import BoneWeight, VecStorage
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

    fuse_vertices: BoolProperty(name="Fuse Vertices",
                                     description="If True, meshes that are attached to the same object will have duplicate vertices removed.",
                                     default=True)

    anim_skeleton: BoolProperty(name="Load Animation Skeleton",
                                     description="If True, will modify skeleton before importing to allow for proper animation imports",
                                     default=False)

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = True  # No animation.

        # When properties are added, use "layout.prop" here to display them
        layout.prop(self, 'strict')
        layout.prop(self, 'import_hierarchy')
        layout.prop(self, 'import_objects')
        layout.prop(self, 'import_materials')
        layout.prop(self, 'fuse_vertices')
        layout.prop(self, 'anim_skeleton')

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

            scene_creator = GMDSceneCreator(self.filepath, gmd_scene, error_reporter)
            gmd_collection = scene_creator.make_collection(context)

            if self.import_hierarchy:
                self.report({"INFO"}, "Importing bone hierarchy...")
                gmd_armature = scene_creator.make_bone_hierarchy(context, gmd_collection, anim_skeleton=self.anim_skeleton)

            if self.import_objects:
                self.report({"INFO"}, "Importing objects...")
                scene_creator.make_objects(context, gmd_collection, gmd_armature if self.import_hierarchy else None,
                                           use_materials=self.import_materials, fuse_vertices=self.fuse_vertices)#self.import_materials)

            self.report({"INFO"}, f"Finished importing {gmd_scene.name}")
            return {'FINISHED'}
        except GMDImportExportError as e:
            print(e)
            self.report({"ERROR"}, str(e))
        return {'CANCELLED'}

TMesh = TypeVar('TMesh', bound=GMDMesh)

class GMDSceneCreator:
    """
    Class used to create all meshes and materials in Blender, from a GMDScene.
    Uses ErrorReporter for all error handling.
    """
    filepath: str
    gmd_scene: GMDScene
    material_id_to_blender: Dict[int, bpy.types.Material]
    gmd_to_blender_world: Matrix

    def __init__(self, filepath: str, gmd_scene: GMDScene, error: ErrorReporter):
        self.filepath = filepath
        self.gmd_scene = gmd_scene
        self.material_id_to_blender = {}
        # TODO - Would it be simpler to just have a scene root object, which we rotate to get the axes correct?
        #  need to think about how it would affect export - if export can handle it easily, then it would be easier
        # The Yakuza games treat +Y as up, +Z as forward.
        # Blender treats +Z as up, +Y as forward, but if we just leave it at that then X is inverted.
        self.gmd_to_blender_world = Matrix((
            Vector((-1, 0, 0, 0)),
            Vector((0, 0, 1, 0)),
            Vector((0, 1, 0, 0)),
            Vector((0, 0, 0, 1)),
        ))
        self.error = error

    def make_collection(self, context: bpy.types.Context) -> bpy.types.Collection:
        """
        Build a collection to hold all of the objects and meshes from the GMDScene.
        :param context: The context used by the import process.
        :return: A collection which the importer can add objects and meshes to.
        """
        collection_name = root_name_for_gmd_file(self.gmd_scene)
        collection = bpy.data.collections.new(collection_name)
        # Link the new collection to the currently active collection.
        context.collection.children.link(collection)
        return collection

    def make_bone_hierarchy(self, context: bpy.types.Context, collection: bpy.types.Collection, anim_skeleton: bool) -> bpy.types.Object:
        """
        Make an Armature representing all of the GMDBones in the imported scene hierarchy.
        :param context: The context used by the import process.
        :param collection: The collection the import process is adding objects and meshes to.
        :return: An object with an armature representing all of the GMDBones in the imported scene hierarchy.
        """
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

        self.bone_world_yakuza_space_matrices: Dict[str, Matrix] = {}

        def generate_perpendicular_bone_direction(this_bone_matrix: Matrix, parent_dir: Vector):
            # Pick a vector that's sort of in the same direction we want the bone to point in
            # (i.e. we don't want the bone to go in/out, so don't pick (0, 0, 1))
            target_dir = Vector((0, 1, 0))
            if abs(parent_dir.dot(target_dir)) > 0.99:
                # Parent and proposed perpendicular direction are basically the same axis, cross product won't work
                # Choose a different one
                target_dir = Vector((1, 0, 0))

            # parent_dir cross target_dir creates a vector that's guaranteed to be perpendicular to both of them.
            perp_dir = parent_dir.cross(target_dir).normalized()
            print(f"{parent_dir} X {target_dir} = {perp_dir}")

            # Then, parent_dir cross perp_dir will create a vector that is both
            #   1) perpendicular to parent_dir
            #   2) in the same sort of direction as target_dir
            # use this vector as our tail_delta
            tail_delta_dir = parent_dir.cross(perp_dir).normalized()
            print(f"{parent_dir} X {perp_dir} = {tail_delta_dir}")

            # Cross product can have bad symmetry - bones on opposite sides of the skeleton can get deltas that look weird
            # Fix this by picking the delta which moves the tail the farthest possible distance from the origin
            # This will choose consistent directions regardless of which side of the vertical axis you are on
            distance_from_origin_with_positive = (this_bone_matrix @ (tail_delta_dir * 0.1)).length
            distance_from_origin_with_negative = (this_bone_matrix @ (-tail_delta_dir * 0.1)).length
            if distance_from_origin_with_negative > distance_from_origin_with_positive:
                tail_delta_dir = -tail_delta_dir

            return tail_delta_dir

        for gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            if not isinstance(gmd_node, GMDBone):
                continue

            # Find the local->world matrix for the parent bone, and use this to find the local->world matrix for the current bone
            if gmd_node.parent:
                parent_matrix_unrotated = self.bone_world_yakuza_space_matrices[gmd_node.parent.name]
            else:
                parent_matrix_unrotated = Matrix.Identity(4)

            print(f"bone {gmd_node.name}")
            gmd_bone_pos, gmd_bone_axis_maybe, gmd_bone_scale = gmd_node.matrix.inverted().decompose()
            print(f"Decomposed Data\n{gmd_bone_pos},\t{gmd_bone_axis_maybe},\t{gmd_bone_scale}")
            print(f"Actual Data\n{gmd_node.pos},\t{gmd_node.rot},\t{gmd_node.scale}")
            print()

            # TODO - this produces an uninvertible matrix - why?
            #   this_bone_matrix = parent_matrix @ transform_to_matrix(gmd_node.pos, gmd_node.rot, gmd_node.scale)
            this_bone_matrix_unrotated = parent_matrix_unrotated @ Matrix.Translation(gmd_node.pos.xyz)# @ Matrix.Diagonal(gmd_node.scale.xyz).resize_4x4())
            head_no_rot = self.gmd_to_blender_world @ this_bone_matrix_unrotated @ Vector((0,0,0))
            self.bone_world_yakuza_space_matrices[gmd_node.name] = this_bone_matrix_unrotated

            tail_delta = gmd_node.bone_pos.xyz + gmd_node.bone_axis.xyz
            # This is unused now because we can just use the gmd bone axis
            """
            # Take a page out of XNA Importer's book for bone tails - make roots just stick towards the camera
            # and make nodes with (non-twist) children try to go to the average of those children's positions
            if not gmd_node.parent:
                tail_delta = Vector((0, 0, 0.5))
            elif twist_regex.search(gmd_node.name) and not gmd_node.children:
                print(f"Twisting {gmd_node.name}")
                # We have a parent, and we're a twist bone
                # "Twist Bones" allow things like shoulders to be twisted when the arm is bent.
                # They are separate from the main arm bone, and shouldn't really extend in the same direction
                # as the arm bone, as otherwise it would be difficult to tell them apart.

                # First, check if we have siblings in a similar position to ours - these are the bones we want to be different from
                adjacent_siblings = [child for child in gmd_node.parent.children if child is not gmd_node and (child.pos - gmd_node.pos).length < 0.01]
                if adjacent_siblings:
                    if gmd_node.pos.xyz.length < 0.00001:
                        tail_delta = Vector((0, 0, 0.05))
                    else:
                        # If we're trying to be different from our sibling, we pick a direction that is perpendicular to the direction we would normally pick
                        # i.e. a vector perpendicular to the "parent direction"
                        parent_dir = gmd_node.pos.xyz.normalized() # gmd_node.pos is relative to the parent already
                        tail_delta_dir = generate_perpendicular_bone_direction(this_bone_matrix, parent_dir)
                        # Extend the tail in the direction of the delta
                        print(f"Extending in the direction {tail_delta_dir}")
                        tail_delta = (tail_delta_dir.xyz * 0.1)
                else:
                    # There aren't any bones we have to differentiate ourselves from -> just follow the parent delta, like the default for having no children
                    if gmd_node.pos.xyz.length < 0.00001:
                        tail_delta = Vector((0, 0, 0.05))
                    else:
                        tail_delta = gmd_node.pos.xyz.normalized() * 0.05
            else:
                # This either isn't a twist bone or it has children - most likely this just isn't a twist bone, as twist bones generally don't have children anyway
                # If there are non-twist children, set the tail to the average of their positions
                countable_children_gmd_positions = [child.pos.xyz for child in gmd_node.children if not twist_regex.search(child.name)]

                if countable_children_gmd_positions:
                    # TODO - if children all start at the same place we do, tail_delta = (0,0,0) and bone disappears
                    #  Do the perpendicular thing for this case too? Requires refactor
                    tail_delta = sum(countable_children_gmd_positions, Vector((0,0,0))) / len(countable_children_gmd_positions)

                    if tail_delta.length < 0.001:
                        if gmd_node.pos.xyz.length < 0.00001:
                            tail_delta = Vector((0, 0, 0.05))
                        else:
                            parent_dir = gmd_node.pos.xyz.normalized()  # gmd_node.pos is relative to the parent already
                            tail_delta_dir = generate_perpendicular_bone_direction(this_bone_matrix, parent_dir)
                            tail_delta = (tail_delta_dir.xyz * 0.1)
                else:
                    # Extend the tail in the direction of the parent
                    # gmd_node.pos.xyz is relative to the parent already
                    if gmd_node.pos.xyz.length < 0.00001:
                        tail_delta = Vector((0, 0, 0.05))
                    else:
                        tail_delta = gmd_node.pos.xyz.normalized() * 0.05
            """

            bone = armature.edit_bones.new(f"{gmd_node.name}")
            bone.use_relative_parent = False
            bone.use_deform = True
            if tail_delta.xyz == (0, 0, 0) or gmd_node.bone_axis.w < 0.00001:
               tail_delta = Vector((0, 0, 0.5))
            if not anim_skeleton:
                bone.head = self.gmd_to_blender_world @ gmd_node.bone_pos.xyz
                bone.tail = self.gmd_to_blender_world @ tail_delta
                if gmd_node.bone_axis.w < 0.00001:
                    bone.length = 0.0001
                else:
                    bone.length = gmd_node.bone_axis.w
            else:
                bone.head = self.gmd_to_blender_world @ gmd_node.matrix.inverted() @ Vector((0,0,0))
                bone.tail = self.gmd_to_blender_world @ gmd_node.matrix.inverted() @ Vector((0,0,1))
                bone.length = 0.0001
            if tail_delta.length < 0.00001:
                self.error.recoverable(f"Bone {bone.name} generated a tail_delta of 0 and will be deleted by Blender.")
            # If your head is close to your parent's tail, turn on "connected to parent"
            if gmd_node.parent:
                bone.parent = armature.edit_bones[gmd_node.parent.name]
                if (bone.head - bone.parent.tail).length < 0.00001 and not anim_skeleton:
                    bone.use_connect = True
                else:
                    bone.use_connect = False
            else:
                bone.parent = None

            # Store bone pos and local rotation as custom properties to be used by the animation importer
            bone["head_no_rot"] = head_no_rot
            bone["local_rot"] = transform_rotation_gmd_to_blender(gmd_node.rot)

        bpy.ops.object.mode_set(mode='POSE')

        # todo - set custom shape for object bones (and bones with no parent?) (and twist bones????)
        #bpy.data.objects['Armature'].pose.bones['Bone1'].custom_shape = bpy.data.objects['wgt_bone1']

        # todo - XNALara sets custom colors for things based on the objects they affect - we could do something like that too?
        # https://github.com/johnzero7/XNALaraMesh/blob/eaccfddf39aef8d3cb60a50c05f2585398fe26ca/import_xnalara_model.py#L748
        # having color differentiation may make it easier to navigate

        bpy.ops.object.mode_set(mode='OBJECT')

        return armature_obj

    def make_objects(self, context: bpy.types.Context, collection: bpy.types.Collection,
                     armature_object: Optional[bpy.types.Object], use_materials: bool, fuse_vertices: bool):
        """
        Populate the Blender scene with Blender objects for each node in the scene hierarchy representing a GMDSkinnedObject
        or GMDUnskinnedObject.
        :param context: The Blender context the import process was given.
        :param collection: The collection the import process is adding objects and meshes to.
        :param armature_object: The object used for the armature, if a scene skeleton was imported.
        :param use_materials: Should the objects have correct materials set or not.
        :param fuse_vertices: Should vertices in meshes using the same attribute sets in the same object be fused?
        :return: Nothing
        """

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

            custom_normals = []

            # 1. Make a single BMesh containing all meshes referenced by this object.
            # We want to do vertex deduplication any meshes that use the same attribute sets, as it is likely that they were
            # originally split up for the sake of bone limits, and not merging them would make blender bug up.
            # To do this, we list all of the unique attribute sets:
            gmd_attr_set_ids = list({id(mesh.attribute_set) for mesh in gmd_node.mesh_list})
            # TODO: This method probably wastes a lot of time creating new BMeshes.
            #  It could be better to just append to the overall_bm instead of making a new one, sending it to a Mesh, then adding it back.
            overall_bm = bmesh.new()
            blender_material_list = []

            self.error.info(f"Creating node {gmd_node.name} from {len(gmd_node.mesh_list)} meshes and {len(gmd_attr_set_ids)} attribute sets")

            # then we make a merged GMDMesh object for each attribute set, containing the meshes that use that attribute set.
            for i, attr_set_id in enumerate(gmd_attr_set_ids):
                meshes_for_attr_set = [gmd_mesh for gmd_mesh in gmd_node.mesh_list if id(gmd_mesh.attribute_set) == attr_set_id]
                attr_set = meshes_for_attr_set[0].attribute_set
                self.error.info(f"\tattr_set #{attr_set_id} has {len(meshes_for_attr_set)} meshes with {[len(gmd_mesh.vertices_data) for gmd_mesh in meshes_for_attr_set]} verts each.")
                # merged_gmd_mesh = self.make_merged_gmd_mesh(
                #     [gmd_mesh for gmd_mesh in gmd_node.mesh_list if id(gmd_mesh.attribute_set) == attr_set_id], remove_dupes=fuse_vertices)

                # Convert this merged GMDMesh to a BMesh, then merge it into the overall BMesh.
                if use_materials:
                    blender_material_list.append(self.make_material(collection, attr_set))
                    new_bmesh = gmd_meshes_to_bmesh(
                        meshes_for_attr_set,
                        vertex_group_indices,
                        attr_idx=i,
                        gmd_to_blender_world=self.gmd_to_blender_world,
                        fuse_vertices=fuse_vertices,
                        error=self.error
                    )
                else:
                    new_bmesh = gmd_meshes_to_bmesh(
                        meshes_for_attr_set,
                        vertex_group_indices,
                        attr_idx=0,
                        gmd_to_blender_world=self.gmd_to_blender_world,
                        fuse_vertices=fuse_vertices,
                        error=self.error
                    )

                self.error.info(f"\t\tAdding {len(new_bmesh.verts)} verts and {len(new_bmesh.faces)} faces for accumulated, (fused={fuse_vertices}) mesh of attr_set #{attr_set_id}")

                # Merge it in to the overall bmesh.
                new_bmesh.to_mesh(temp_mesh)
                new_bmesh.free()
                overall_bm.from_mesh(temp_mesh)
            self.error.info(f"\tOverall mesh vert count: {len(overall_bm.verts)}")

            # Turn the overall BMesh into a Blender Mesh (there's a difference) so that it can be attached to an Object.
            overall_mesh = bpy.data.meshes.new(gmd_node.name)
            overall_bm.to_mesh(overall_mesh)
            overall_bm.free()
            if use_materials:
                for mat in blender_material_list:
                    overall_mesh.materials.append(mat)
            # print(f"total custom normals: {len(custom_normals)}")
            # print(f"total verts: {len(overall_mesh.vertices)}")
            # For the normals to work right, you have 1. create and set the "split normals" for each vertex
            # 2. enable "use_auto_smooth", which tells blender to actually use the custom split normals data.
            # overall_mesh.create_normals_split()
            # overall_mesh.normals_split_custom_set_from_vertices(custom_normals)
            # overall_mesh.auto_smooth_angle = 0
            # overall_mesh.use_auto_smooth = True

            # Create the final object representing this GMDNode
            mesh_obj: bpy.types.Object = bpy.data.objects.new(gmd_node.name, overall_mesh)

            # Set the GMDNode position, rotation, scale
            mesh_obj.location = self.gmd_to_blender_world @ gmd_node.pos.xyz
            # TODO: Use a proper function for this - I hate that the matrix multiply doesn't work
            mesh_obj.rotation_quaternion = Quaternion((gmd_node.rot.w, -gmd_node.rot.x, gmd_node.rot.z, gmd_node.rot.y))#self.gmd_to_blender_world @ gmd_node.rot
            # TODO - When applying gmd_to_blender_world to (1,1,1) you get (-1,1,1) out. This undoes the previous scaling applied to the vertices.
            #  .xzy is used to swap the components for now, but there's probably a better way?
            #mesh_obj.scale = self.gmd_to_blender_world @ gmd_node.scale.xyz
            mesh_obj.scale = gmd_node.scale.xzy

            if is_skinned:
                # Skinned Objects are parented to the armature, with an Armature modifier to deform them.
                if armature_object:
                    mesh_obj.parent = armature_object
                    for name in vertex_group_list:
                        mesh_obj.vertex_groups.new(name=name)
                    modifier = mesh_obj.modifiers.new(type='ARMATURE', name="Armature")
                    modifier.object = armature_object
            else:
                # Unskinned objects are either parented to a bone, or to another unskinned object.
                if gmd_node.parent:
                    if gmd_node.parent.node_type == NodeType.MatrixTransform:
                        # To parent an object to a specific bone in the armature, use the Child-Of constraint.
                        child_constraint = mesh_obj.constraints.new("CHILD_OF")

                        # TODO - This may be unnecessary now that the forward vectors are sign-consistent
                        # Line up the object with the bone it's parented to
                        parent_yakuza_space = self.bone_world_yakuza_space_matrices[gmd_node.parent.name]
                        mesh_unparented_yakuza_space = (self.gmd_to_blender_world.inverted() @ mesh_obj.matrix_world)
                        expected_mesh_obj_matrix = self.gmd_to_blender_world @ parent_yakuza_space @ mesh_unparented_yakuza_space

                        # Set the inverse matrix based on this orientation - otherwise things get weird
                        # Make sure to set the inverse matrix BEFORE changing other stuff, apparently changing it last doesn't work
                        # https://blender.stackexchange.com/questions/19602/child-of-constraint-set-inverse-with-python
                        child_constraint.inverse_matrix = (expected_mesh_obj_matrix).inverted()
                        child_constraint.target = armature_object
                        child_constraint.subtarget = gmd_node.parent.name
                    else:
                        # Parenting an object to another object is easy
                        mesh_obj.parent = gmd_objects[id(gmd_node.parent)]

            # Add the object to the gmd_objects map, and link it to the scene. We're done!
            gmd_objects[id(gmd_node)] = mesh_obj
            collection.objects.link(mesh_obj)

        bpy.data.meshes.remove(temp_mesh)

    def make_material(self, collection: bpy.types.Collection, gmd_attribute_set: GMDAttributeSet) -> bpy.types.Material:
        """
        Given a gmd_attribute_set, make a Blender material.
        The material name is based on the collection name NOT the gmd_scene name, in case duplicate scenes exist.
        i.e. if c_am_kiryu is imported twice, the second collection will be named c_am_kiryu.001. For consistency,
        the materials take this c_am_kiryu.001 as a prefix.
        :param collection: The collection the scene is associated with.
        :param gmd_attribute_set: The attribute set to create a material for.
        :return: A Blender material with all of the data from the gmd_attribute_set represented in an exportable way.
        """
        # If the attribute set has a material already, reuse it.
        if id(gmd_attribute_set) in self.material_id_to_blender:
            return self.material_id_to_blender[id(gmd_attribute_set)]

        def make_yakuza_node_group(node_tree: bpy.types.NodeTree):
            node = node_tree.nodes.new("ShaderNodeGroup")
            node.node_tree = get_yakuza_shader_node_group()
            return node

        material_name = f"{collection.name_full}_{gmd_attribute_set.shader.name}"

        material = bpy.data.materials.new(material_name)
        # Yakuza shaders all use backface culling (even the transparent ones!)
        material.use_backface_culling = True
        # They all have to use nodes, of course
        material.use_nodes = True
        # Don't use the default node setup
        material.node_tree.nodes.clear()
        # Make a Yakuza Shader group, and position it
        yakuza_shader_node_group = make_yakuza_node_group(material.node_tree)
        yakuza_shader_node_group.location = (0, 0)
        yakuza_shader_node_group.width = 400
        yakuza_shader_node_group.height = 800
        # Hook up the Yakuza Shader to the output
        output_node = material.node_tree.nodes.new("ShaderNodeOutputMaterial")
        output_node.location = (500, 0)
        material.node_tree.links.new(yakuza_shader_node_group.outputs["Shader"], output_node.inputs["Surface"])

        # Set up the group inputs and material data based on the attribute set.
        set_yakuza_shader_material_from_attributeset(
            material,
            yakuza_shader_node_group.inputs,
            gmd_attribute_set,
            os.path.dirname(self.filepath)
        )

        self.material_id_to_blender[id(gmd_attribute_set)] = material
        return material


def menu_func_import(self, context):
    self.layout.operator(ImportGMD.bl_idname, text='Yakuza GMD (.gmd)')
