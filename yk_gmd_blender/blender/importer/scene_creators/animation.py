import json
from typing import Dict, Tuple, Set

import bpy
from mathutils import Quaternion, Matrix, Vector
from ...coordinate_converter import transform_rotation_gmd_to_blender
from .base import BaseGMDSceneCreator, GMDSceneCreatorConfig
from .skinned import armature_name_for_gmd_file
from ....gmdlib.abstract.gmd_scene import GMDScene
from ....gmdlib.abstract.nodes.gmd_bone import GMDBone
from ....gmdlib.abstract.nodes.gmd_object import GMDUnskinnedObject, GMDSkinnedObject
from ....gmdlib.errors.error_reporter import ErrorReporter


class GMDAnimationSceneCreator(BaseGMDSceneCreator):
    """
    Implementation of a GMDSceneCreator that imports skinned and unskinned meshes under a single armature
    for the sake of animation.
    """

    def __init__(self, filepath: str, gmd_scene: GMDScene, config: GMDSceneCreatorConfig, error: ErrorReporter):
        super().__init__(filepath, gmd_scene, config, error)

    def validate_scene(self):
        pass

    def make_bone_hierarchy(
            self,
            context: bpy.types.Context,
            collection: bpy.types.Collection,
    ) -> Tuple[bpy.types.Object, Dict[int, str]]:
        """
        Make an Armature representing all of the GMD *NODES* in the imported scene hierarchy.
        :param context: The context used by the import process.
        :param collection: The collection the import process is adding objects and meshes to.
        :return: An object with an armature with a bone for every GMDNode in the imported scene hierarchy,
        and a mapping of id(gmd_node) to the name of the relevant bone in the blender armature.
        """
        armature_name = armature_name_for_gmd_file(self.gmd_scene)
        armature = bpy.data.armatures.new(f"{armature_name}")
        armature.display_type = 'STICK'
        armature_obj = bpy.data.objects.new(f"{armature_name}", armature)
        armature_obj.show_in_front = True
        armature_obj.yakuza_file_root_data.is_valid_root = True
        armature_obj.yakuza_file_root_data.imported_version = self.config.game.as_blender()
        armature_obj.yakuza_file_root_data.flags_json = json.dumps(self.gmd_scene.flags)
        armature_obj.yakuza_file_root_data.import_mode = "ANIMATION"

        collection.objects.link(armature_obj)

        context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT')

        node_yakuza_world_space_matrices: Dict[int, Matrix] = {}
        node_id_to_blender_bone_name: Dict[int, str] = {}

        for _, gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            self.error.debug("BONES", f"node {gmd_node.name}")
            self.error.debug("BONES", f"Actual Data\n{gmd_node.pos}\t{gmd_node.rot}\t{gmd_node.scale}")

            # Find the local->world matrix for the parent bone, and use this to find the local->world matrix for the current bone
            if gmd_node.parent:
                parent_matrix_unrotated = node_yakuza_world_space_matrices[id(gmd_node.parent)]
            else:
                parent_matrix_unrotated = Matrix.Identity(4)

            this_bone_matrix_unrotated = parent_matrix_unrotated @ Matrix.Translation(gmd_node.pos.xyz)
            node_yakuza_world_space_matrices[id(gmd_node)] = this_bone_matrix_unrotated

            head_no_rot = self.gmd_to_blender_world @ this_bone_matrix_unrotated @ Vector((0, 0, 0))

            bone = armature.edit_bones.new(f"{gmd_node.name}")
            bone.use_relative_parent = False
            bone.use_deform = True
            if isinstance(gmd_node, GMDBone):
                # Compatibility with the anim_skeleton property removed in
                # https://github.com/theturboturnip/yk_gmd_io/commit/24577b5190ec4031683b7a0b025e8ca61925af88
                # This was removed because "Newer versions of the animation importer don't need it",
                # but people have asked for it back.
                bone.head = self.gmd_to_blender_world @ gmd_node.matrix.inverted() @ Vector((0, 0, 0))
                bone.tail = self.gmd_to_blender_world @ gmd_node.matrix.inverted() @ Vector((0, 0, 1))
                bone.length = 0.0001
                # Do not under any circumstances connect to the parent
                bone.use_connect = False
            else:
                bone.head = self.gmd_to_blender_world @ gmd_node.world_pos.xyz
                bone.tail = self.gmd_to_blender_world @ (gmd_node.world_pos.xyz + gmd_node.anim_axis.xyz)
                if gmd_node.anim_axis.w < 0.00001:
                    bone.length = 0.0001
                else:
                    bone.length = gmd_node.anim_axis.w

            # Register the name so we can set up export data later.
            # I don't plan to export from this setup, but it doesn't hurt to set up the info
            node_id_to_blender_bone_name[id(gmd_node)] = bone.name

            # Make sure GMDBones have the same names in the armature, so vertex groups work correctly.
            if isinstance(gmd_node, GMDBone):
                if bone.name != gmd_node.name:
                    self.error.recoverable(
                        f"The GMDBone '{gmd_node.name}' has the same name as other GMD nodes in this scene.\n"
                        f"Skinned objects may not have the right rigging.\n"
                        f"Disable Strict Import to continue."
                    )

            # If the original node was parented, give it a parent
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
            # We find the bone we just created by name - we check elsewhere that the GMD doesn't have duplicate bone
            # names in skinned imports
            bone = armature.bones[node_id_to_blender_bone_name[id(gmd_node)]]
            bone.yakuza_hierarchy_node_data.inited = True
            bone.yakuza_hierarchy_node_data.anim_axis = gmd_node.anim_axis
            if isinstance(gmd_node, (GMDBone, GMDUnskinnedObject)):
                bone.yakuza_hierarchy_node_data.imported_matrix = \
                    list(gmd_node.matrix[0]) + list(gmd_node.matrix[1]) + list(gmd_node.matrix[2]) + list(
                        gmd_node.matrix[3])
            else:
                bone.yakuza_hierarchy_node_data.imported_matrix = [0] * 16
            bone.yakuza_hierarchy_node_data.flags_json = json.dumps(gmd_node.flags)
            bone.yakuza_hierarchy_node_data.sort_order = (sibling_order + 1) * 10
            bone.yakuza_hierarchy_node_data.bone_local_rot = transform_rotation_gmd_to_blender(gmd_node.rot)

        return armature_obj, node_id_to_blender_bone_name

    def make_objects(self, context: bpy.types.Context, collection: bpy.types.Collection,
                     armature_object: bpy.types.Object, node_id_to_blender_bone_name: Dict[int, str]):
        """
        Populate the Blender scene with Blender objects for each node in the scene hierarchy representing a GMDSkinnedObject
        or GMDUnskinnedObject.
        :param context: The Blender context the import process was given.
        :param collection: The collection the import process is adding objects and meshes to.
        :param armature_object: The object used for the armature.
        :return: Nothing
        """

        skinned_vertex_group_list = [
            node.name
            for node in self.gmd_scene.overall_hierarchy
            if isinstance(node, GMDBone)
        ]
        skinned_vertex_group_indices = {
            name: i
            for i, name in enumerate(skinned_vertex_group_list)
        }

        gmd_objects: Dict[int, bpy.types.Object] = {}

        bones_parenting_meshes: Set[int] = set()
        for _, gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            if isinstance(gmd_node, GMDBone):
                continue

            # This is a mesh
            # Check all parents and put them in the bones_parenting_meshes column
            parent = gmd_node.parent
            while parent is not None:
                if isinstance(parent, GMDBone):
                    bones_parenting_meshes.add(id(parent))
                parent = parent.parent

        for sibling_order, gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            if isinstance(gmd_node, (GMDSkinnedObject, GMDUnskinnedObject)):
                # Build the mesh, providing the vertex group indices in case it's a skinned object
                overall_mesh = self.build_object_mesh(collection, gmd_node,
                                                      skinned_vertex_group_indices)
                node_obj = bpy.data.objects.new(f"{gmd_node.name}", overall_mesh)

                # Objects use an Armature modifier to deform them.
                modifier = node_obj.modifiers.new(type='ARMATURE', name="Armature")
                modifier.object = armature_object

                # Skinned objects are deformed by the GMDBones
                if isinstance(gmd_node, GMDSkinnedObject):
                    for name in skinned_vertex_group_list:
                        node_obj.vertex_groups.new(name=name)
                else:
                    # Unskinned objects are mapped to a single bone just for them
                    vertex_group = node_obj.vertex_groups.new(name=node_id_to_blender_bone_name[id(gmd_node)])
                    # Set the vertex weights to max for all vertices
                    all_vertex_indices = tuple(range(len(node_obj.data.vertices)))
                    vertex_group.add(all_vertex_indices, 1, "REPLACE")
            else:
                if id(gmd_node) in bones_parenting_meshes:
                    # Create an empty if it has non-bones as children
                    node_obj = bpy.data.objects.new(f"{gmd_node.name}", None)
                    node_obj.empty_display_size = 0.05
                else:
                    continue

            # Set the GMDNode position, rotation, scale
            node_obj.location = self.gmd_to_blender_world @ gmd_node.pos.xyz
            # TODO: Use a proper function for this - I hate that the matrix multiply doesn't work
            node_obj.rotation_quaternion = Quaternion((gmd_node.rot.w, -gmd_node.rot.x, gmd_node.rot.z, gmd_node.rot.y))
            # TODO - When applying gmd_to_blender_world to (1,1,1) you get (-1,1,1) out. This undoes the previous scaling applied to the vertices.
            #  .xzy is used to swap the components for now, but there's probably a better way?
            node_obj.scale = gmd_node.scale.xzy

            node_obj.yakuza_hierarchy_node_data.inited = True
            node_obj.yakuza_hierarchy_node_data.anim_axis = gmd_node.anim_axis
            if isinstance(gmd_node, (GMDBone, GMDUnskinnedObject)):
                node_obj.yakuza_hierarchy_node_data.imported_matrix = \
                    list(gmd_node.matrix[0]) + list(gmd_node.matrix[1]) + list(gmd_node.matrix[2]) + list(
                        gmd_node.matrix[3])
            else:
                node_obj.yakuza_hierarchy_node_data.imported_matrix = [0] * 16
            node_obj.yakuza_hierarchy_node_data.flags_json = json.dumps(gmd_node.flags)
            # Say the sort_order = the (sibling_order + 1) * 10, so objects are 10, 20, 30, 40...
            # This means you can insert new objects between other ones more easily
            node_obj.yakuza_hierarchy_node_data.sort_order = (sibling_order + 1) * 10

            if gmd_node.parent:
                # Parenting an object to another object is easy
                node_obj.parent = gmd_objects[id(gmd_node.parent)]
            else:
                node_obj.parent = armature_object

            # Add the object to the gmd_objects map, and link it to the scene. We're done!
            print(id(gmd_node), node_obj)
            gmd_objects[id(gmd_node)] = node_obj
            collection.objects.link(node_obj)
