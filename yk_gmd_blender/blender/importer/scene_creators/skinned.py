import re
from typing import Dict, Optional, Union

from mathutils import Matrix, Vector, Quaternion

import bpy
from yk_gmd_blender.blender.coordinate_converter import transform_rotation_gmd_to_blender
from yk_gmd_blender.blender.importer.scene_creators.base import BaseGMDSceneCreator, GMDSceneCreatorConfig
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_object import GMDSkinnedObject, GMDUnskinnedObject
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter


def armature_name_for_gmd_file(gmd_file: Union[GMDScene, str]):
    if isinstance(gmd_file, GMDScene):
        return f"{gmd_file.name}_armature"
    else:
        return f"{gmd_file}_armature"


class GMDSkinnedSceneCreator(BaseGMDSceneCreator):
    """
    Implementation of a GMDSceneCreator that focuses on skinned meshes.
    """

    def __init__(self, filepath: str, gmd_scene: GMDScene, config: GMDSceneCreatorConfig, error: ErrorReporter):
        super().__init__(filepath, gmd_scene, config, error)

    def validate_scene(self):
        # Check for bone name overlap
        # Only bones are added to the overall armature, not objects
        # But the bones are referenced by name, so we need to check if there are multiple bones with the same name
        bones_depth_first = [node for node in self.gmd_scene.overall_hierarchy.depth_first_iterate() if
                             isinstance(node, GMDBone)]
        bone_names = {bone.name for bone in bones_depth_first}
        if len(bone_names) != len(bones_depth_first):
            # Find the duplicate names by listing them all, and removing one occurence of each name
            # The only names left will be duplicates
            bone_name_list = [bone.name for bone in bones_depth_first]
            for name in bone_names:
                bone_name_list.remove(name)
            duplicate_names = set(bone_name_list)
            self.error.fatal(f"Some bones don't have unique names - found duplicates {duplicate_names}")

        # Check that objects do not have bones underneath them
        objects_depth_first = [node for node in self.gmd_scene.overall_hierarchy.depth_first_iterate() if
                               not isinstance(node, GMDBone)]

        def check_object(object: GMDNode):
            if object.parent is not None:
                self.error.fatal(f"This import method cannot import object hierarchies, try the [Unskinned] variant")

            for child in object.children:
                if isinstance(child, GMDBone):
                    self.error.fatal(
                        f"Object {object.name} has child {child.name} which is a GMDBone - The importer expects that objects do not have bones as children")

        for object in objects_depth_first:
            check_object(object)

        if len([node for node in self.gmd_scene.overall_hierarchy.depth_first_iterate() if isinstance(node, GMDUnskinnedObject)]) != 0:
            self.error.recoverable(f"This import method cannot import unskinnned objects. Please use the [Unskinned] variant")

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
                     armature_object: Optional[bpy.types.Object]):
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

        vertex_group_list = [node.name for node in self.gmd_scene.overall_hierarchy.depth_first_iterate() if isinstance(node, GMDBone)]
        vertex_group_indices = {
            name: i
            for i, name in enumerate(vertex_group_list)
        }

        gmd_objects = {}

        for gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            if not isinstance(gmd_node, GMDSkinnedObject):
                continue

            is_skinned = isinstance(gmd_node, GMDSkinnedObject)

            overall_mesh = self.build_object_mesh(collection, gmd_node, vertex_group_indices)

            # Create the final object representing this GMDNode
            mesh_obj: bpy.types.Object = bpy.data.objects.new(gmd_node.name, overall_mesh)

            # Set the GMDNode position, rotation, scale
            mesh_obj.location = self.gmd_to_blender_world @ gmd_node.pos.xyz
            # TODO: Use a proper function for this - I hate that the matrix multiply doesn't work
            mesh_obj.rotation_quaternion = Quaternion((gmd_node.rot.w, -gmd_node.rot.x, gmd_node.rot.z, gmd_node.rot.y))
            # TODO - When applying gmd_to_blender_world to (1,1,1) you get (-1,1,1) out. This undoes the previous scaling applied to the vertices.
            #  .xzy is used to swap the components for now, but there's probably a better way?
            mesh_obj.scale = gmd_node.scale.xzy

            if is_skinned:
                # Skinned Objects are parented to the armature, with an Armature modifier to deform them.
                if armature_object:
                    mesh_obj.parent = armature_object
                    for name in vertex_group_list:
                        mesh_obj.vertex_groups.new(name=name)
                    modifier = mesh_obj.modifiers.new(type='ARMATURE', name="Armature")
                    modifier.object = armature_object


            # Add the object to the gmd_objects map, and link it to the scene. We're done!
            gmd_objects[id(gmd_node)] = mesh_obj
            collection.objects.link(mesh_obj)
