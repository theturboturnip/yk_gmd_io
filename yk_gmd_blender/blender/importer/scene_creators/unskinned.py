import json

import bpy
from mathutils import Quaternion
from .base import BaseGMDSceneCreator, GMDSceneCreatorConfig, \
    root_name_for_gmd_file
from ....gmdlib.abstract.gmd_scene import GMDScene
from ....gmdlib.abstract.nodes.gmd_bone import GMDBone
from ....gmdlib.abstract.nodes.gmd_object import GMDSkinnedObject, GMDUnskinnedObject
from ....gmdlib.errors.error_reporter import ErrorReporter


class GMDUnskinnedSceneCreator(BaseGMDSceneCreator):
    """
    Implementation of a GMDSceneCreator that focuses on skinned meshes.
    """

    def __init__(self, filepath: str, gmd_scene: GMDScene, config: GMDSceneCreatorConfig, error: ErrorReporter):
        super().__init__(filepath, gmd_scene, config, error)

    def validate_scene(self):
        # Skinned Importer checks for duplicate "bone" names (technically node names).
        # Skeletons can't have duplicate bones, but objects can.
        # We remove the Blender-enforced duplicate suffix e.g. "object.001" on export,
        # so nothing will break if we import duplicates
        if any(isinstance(node, GMDSkinnedObject) for node in self.gmd_scene.overall_hierarchy):
            self.error.recoverable(
                f"This import method cannot import skinnned objects. Please use the [Skinned] variant")

    def make_objects(self, collection: bpy.types.Collection):
        """
        Populate the Blender scene with Blender objects for each node in the scene hierarchy
        representing a GMDUnskinnedObject.
        :param collection: The collection the import process is adding objects and meshes to.
        :return: Nothing
        """

        gmd_objects = {}

        root_name = root_name_for_gmd_file(self.gmd_scene)
        root_obj = bpy.data.objects.new(f"{root_name}", None)
        root_obj.yakuza_file_root_data.is_valid_root = True
        root_obj.yakuza_file_root_data.imported_version = self.config.game.as_blender()
        root_obj.yakuza_file_root_data.flags_json = json.dumps(self.gmd_scene.flags)
        root_obj.yakuza_file_root_data.import_mode = "UNSKINNED"
        collection.objects.link(root_obj)

        # Still create the vertex group list, so we create the vertex groups, but don't actually deform anything
        vertex_group_list = [
            node.name
            for node in self.gmd_scene.overall_hierarchy
            if isinstance(node, GMDBone)
        ]
        vertex_group_indices = {
            name: i
            for i, name in enumerate(vertex_group_list)
        }

        for sibling_order, gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            if isinstance(gmd_node, GMDUnskinnedObject):
                overall_mesh = self.build_object_mesh(collection, gmd_node, vertex_group_indices)
                node_obj = bpy.data.objects.new(f"{gmd_node.name}", overall_mesh)
            else:
                node_obj = bpy.data.objects.new(f"{gmd_node.name}", None)
                node_obj.empty_display_size = 0.1

            if gmd_node.parent:
                # Parenting an object to another object is easy
                node_obj.parent = gmd_objects[id(gmd_node.parent)]
            else:
                node_obj.parent = root_obj

            # Set the GMDNode position, rotation, scale
            node_obj.location = self.gmd_to_blender_world @ gmd_node.pos.xyz
            # TODO: Use a proper function for this - I hate that the matrix multiply doesn't work
            node_obj.rotation_quaternion = Quaternion(
                (gmd_node.rot.w, -gmd_node.rot.x, gmd_node.rot.z, gmd_node.rot.y))
            # TODO - When applying gmd_to_blender_world to (1,1,1) you get (-1,1,1) out. This undoes the previous scaling applied to the vertices.
            #  .xzy is used to swap the components for now, but there's probably a better way?
            node_obj.scale = gmd_node.scale.xzy

            # Set custom GMD data
            node_obj.yakuza_hierarchy_node_data.inited = True
            node_obj.yakuza_hierarchy_node_data.anim_axis = gmd_node.anim_axis
            # gmd_node is an unskinned object, guaranteed to have a matrix
            node_obj.yakuza_hierarchy_node_data.imported_matrix = \
                list(gmd_node.matrix[0]) + list(gmd_node.matrix[1]) + list(gmd_node.matrix[2]) + list(
                    gmd_node.matrix[3])
            node_obj.yakuza_hierarchy_node_data.flags_json = json.dumps(gmd_node.flags)
            # Say the sort_order = the (sibling_order + 1) * 10, so objects are 10, 20, 30, 40...
            # This means you can insert new objects between other ones more easily
            node_obj.yakuza_hierarchy_node_data.sort_order = (sibling_order + 1) * 10

            # Add the object to the gmd_objects map, and link it to the scene. We're done!
            gmd_objects[id(gmd_node)] = node_obj
            collection.objects.link(node_obj)
