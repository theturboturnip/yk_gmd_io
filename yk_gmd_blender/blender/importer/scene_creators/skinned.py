import json
from typing import Dict, Optional, Union, cast

import bpy
from mathutils import Matrix, Vector, Quaternion
from ...coordinate_converter import transform_rotation_gmd_to_blender
from .base import BaseGMDSceneCreator, GMDSceneCreatorConfig
from ....gmdlib.abstract.gmd_scene import GMDScene
from ....gmdlib.abstract.nodes.gmd_bone import GMDBone
from ....gmdlib.abstract.nodes.gmd_node import GMDNode
from ....gmdlib.abstract.nodes.gmd_object import GMDSkinnedObject, GMDUnskinnedObject
from ....gmdlib.errors.error_reporter import ErrorReporter


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
        bones_depth_first = [
            node
            for node in self.gmd_scene.overall_hierarchy
            if isinstance(node, GMDBone)
        ]
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
        objects_depth_first = [
            node
            for node in self.gmd_scene.overall_hierarchy
            if not isinstance(node, GMDBone)
        ]

        def check_object(object: GMDNode):
            if object.parent is not None:
                self.error.fatal(f"This import method cannot import object hierarchies, try the [Unskinned] variant")

            for child in object.children:
                if isinstance(child, GMDBone):
                    self.error.fatal(
                        f"Object {object.name} has child {child.name} which is a GMDBone - "
                        f"The importer expects that objects do not have bones as children")

        for object in objects_depth_first:
            check_object(object)

        if any(isinstance(node, GMDUnskinnedObject) for node in self.gmd_scene.overall_hierarchy):
            self.error.recoverable(
                f"This import method cannot import unskinnned objects. Please use the [Unskinned] variant")

    def make_bone_hierarchy(self, context: bpy.types.Context, collection: bpy.types.Collection) -> bpy.types.Object:
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
        armature_obj.yakuza_file_root_data.is_valid_root = True
        armature_obj.yakuza_file_root_data.imported_version = self.config.game.as_blender()
        armature_obj.yakuza_file_root_data.flags_json = json.dumps(self.gmd_scene.flags)
        armature_obj.yakuza_file_root_data.import_mode = "SKINNED"

        collection.objects.link(armature_obj)

        context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT')

        self.bone_world_yakuza_space_matrices: Dict[str, Matrix] = {}

        for _, gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            if not isinstance(gmd_node, GMDBone):
                continue

            self.error.debug("BONES", f"bone {gmd_node.name}")
            self.error.debug("BONES", f"Actual Data\n{gmd_node.pos}\t{gmd_node.rot}\t{gmd_node.scale}")

            # Find the local->world matrix for the parent bone, and use this to find the local->world matrix for the current bone
            if gmd_node.parent:
                parent_matrix_unrotated = self.bone_world_yakuza_space_matrices[gmd_node.parent.name]
            else:
                parent_matrix_unrotated = Matrix.Identity(4)

            this_bone_matrix_unrotated = parent_matrix_unrotated @ Matrix.Translation(gmd_node.pos.xyz)
            head_no_rot = self.gmd_to_blender_world @ this_bone_matrix_unrotated @ Vector((0, 0, 0))
            self.bone_world_yakuza_space_matrices[gmd_node.name] = this_bone_matrix_unrotated

            bone = armature.edit_bones.new(f"{gmd_node.name}")
            bone.use_relative_parent = False
            bone.use_deform = True
            bone.head = self.gmd_to_blender_world @ gmd_node.world_pos.xyz
            bone.tail = self.gmd_to_blender_world @ (gmd_node.world_pos.xyz + gmd_node.anim_axis.xyz)
            if gmd_node.anim_axis.w < 0.00001:
                bone.length = 0.0001
            else:
                bone.length = gmd_node.anim_axis.w

            # If your head is close to your parent's tail, turn on "connected to parent"
            if gmd_node.parent:
                bone.parent = armature.edit_bones[gmd_node.parent.name]
            else:
                bone.parent = None

            # Store bone pos and local rotation as custom properties to be used by the animation importer
            bone["head_no_rot"] = head_no_rot
            bone["local_rot"] = transform_rotation_gmd_to_blender(gmd_node.rot)

        bpy.ops.object.mode_set(mode='POSE')

        # todo - set custom shape for object bones (and bones with no parent?) (and twist bones????)
        # bpy.data.objects['Armature'].pose.bones['Bone1'].custom_shape = bpy.data.objects['wgt_bone1']

        # todo - XNALara sets custom colors for things based on the objects they affect - we could do something like that too?
        # https://github.com/johnzero7/XNALaraMesh/blob/eaccfddf39aef8d3cb60a50c05f2585398fe26ca/import_xnalara_model.py#L748
        # having color differentiation may make it easier to navigate

        bpy.ops.object.mode_set(mode='OBJECT')

        # Set extra GMD data - we have to do this in object mode, because the extra data is on Bone not EditBone
        # (I think this is right, because EditBone only exists in Edit mode?)
        for sibling_order, gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            if not isinstance(gmd_node, GMDBone):
                continue

            # We find the bone we just created by name - we check elsewhere that the GMD doesn't have duplicate bone
            # names in skinned imports
            bone = armature.bones[gmd_node.name]
            bone.yakuza_hierarchy_node_data.inited = True
            bone.yakuza_hierarchy_node_data.anim_axis = gmd_node.anim_axis
            bone.yakuza_hierarchy_node_data.imported_matrix = \
                list(gmd_node.matrix[0]) + list(gmd_node.matrix[1]) + list(gmd_node.matrix[2]) + list(
                    gmd_node.matrix[3])
            bone.yakuza_hierarchy_node_data.flags_json = json.dumps(gmd_node.flags)
            bone.yakuza_hierarchy_node_data.sort_order = (sibling_order + 1) * 10
            bone.yakuza_hierarchy_node_data.bone_local_rot = transform_rotation_gmd_to_blender(gmd_node.rot)

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

        vertex_group_list = [
            node.name
            for node in self.gmd_scene.overall_hierarchy
            if isinstance(node, GMDBone)
        ]
        vertex_group_indices = {
            name: i
            for i, name in enumerate(vertex_group_list)
        }

        gmd_objects = {}

        for _, gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            if not isinstance(gmd_node, GMDSkinnedObject):
                continue
            gmd_node: GMDSkinnedObject = cast(GMDSkinnedObject, gmd_node)

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

            if gmd_node.parent:
                sibling_order = gmd_node.parent.children.index(gmd_node)
            else:
                sibling_order = self.gmd_scene.overall_hierarchy.roots.index(gmd_node)

            mesh_obj.yakuza_hierarchy_node_data.inited = True
            mesh_obj.yakuza_hierarchy_node_data.anim_axis = gmd_node.anim_axis
            # gmd_node is a skinned object, doesn't have a matrix
            mesh_obj.yakuza_hierarchy_node_data.imported_matrix = [0] * 16
            mesh_obj.yakuza_hierarchy_node_data.flags_json = json.dumps(gmd_node.flags)
            # Say the sort_order = the (sibling_order + 1) * 10, so objects are 10, 20, 30, 40...
            # This means you can insert new objects between other ones more easily
            mesh_obj.yakuza_hierarchy_node_data.sort_order = (sibling_order + 1) * 10

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
