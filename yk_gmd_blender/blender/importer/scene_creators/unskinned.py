import array
import collections
import os
import re
from typing import Dict, List, Tuple, Union, cast, TypeVar, Optional

from mathutils import Matrix, Vector, Quaternion

import bpy
from yk_gmd_blender.blender.common import armature_name_for_gmd_file, root_name_for_gmd_file
from yk_gmd_blender.blender.coordinate_converter import transform_to_matrix, transform_rotation_gmd_to_blender

from yk_gmd_blender.blender.error_reporter import BlenderErrorReporter
from yk_gmd_blender.blender.importer.mesh_importer import gmd_meshes_to_bmesh
from yk_gmd_blender.blender.importer.scene_creators.base import BaseGMDSceneCreator, GMDSceneCreatorConfig
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

class GMDUnskinnedSceneCreator(BaseGMDSceneCreator):
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

        if len([node for node in self.gmd_scene.overall_hierarchy.depth_first_iterate() if isinstance(node, GMDSkinnedObject)]) != 0:
            self.error.recoverable(f"This import method cannot import skinnned objects. Please use the [Skinned] variant")


    def make_objects(self, collection: bpy.types.Collection):
        """
        Populate the Blender scene with Blender objects for each node in the scene hierarchy representing a GMDUnskinnedObject.
        :param collection: The collection the import process is adding objects and meshes to.
        :return: Nothing
        """

        gmd_objects = {}

        root_name = root_name_for_gmd_file(self.gmd_scene)
        root_obj = bpy.data.objects.new(f"{root_name}", None)
        collection.objects.link(root_obj)

        # Still create the vertex group list, so we create the vertex groups, but don't actually deform anything
        vertex_group_list = [node.name for node in self.gmd_scene.overall_hierarchy.depth_first_iterate() if isinstance(node, GMDBone)]
        vertex_group_indices = {
            name: i
            for i, name in enumerate(vertex_group_list)
        }

        for gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            if isinstance(gmd_node, GMDUnskinnedObject):
                overall_mesh = self.build_object_mesh(collection, gmd_node, vertex_group_indices)
                node_obj = bpy.data.objects.new(f"{gmd_node.name}", overall_mesh)
            else:
                node_obj = bpy.data.objects.new(f"{gmd_node.name}", None)

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

            # Add the object to the gmd_objects map, and link it to the scene. We're done!
            gmd_objects[id(gmd_node)] = node_obj
            collection.objects.link(node_obj)
