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
from yk_gmd_blender.blender.importer.scene_creators.base import GMDSceneCreatorConfig, GMDGame, MaterialNamingType
from yk_gmd_blender.blender.importer.scene_creators.skinned import GMDSkinnedSceneCreator
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
from yk_gmd_blender.yk_gmd.v2.io import read_abstract_scene, read_abstract_scene_from_filedata_object, \
    read_gmd_structures
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType
from yk_gmd_blender.yk_gmd.v2.structure.version import VersionProperties, GMDVersion


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
    material_naming: EnumProperty(name="Material Naming",
                                  description="How materials are named",
                                  items=[
                                      ("COLLECTION_SHADER", "[Collection]_[Shader]", "Collection name and Shader name"),
                                      ("COLLECTION_TEXTURE", "[Collection]_[Texture]", "Collection name and Diffuse Texture name"),
                                      ("TEXTURE", "[Texture]", "Diffuse Texture name"),
                                  ],
                                  default="COLLECTION_TEXTURE")

    fuse_vertices: BoolProperty(name="Fuse Vertices",
                                     description="If True, meshes that are attached to the same object will have duplicate vertices removed.",
                                     default=True)

    anim_skeleton: BoolProperty(name="Load Animation Skeleton",
                                     description="If True, will modify skeleton before importing to allow for proper animation imports",
                                     default=False)

    game_enum: EnumProperty(name="Game/Engine Version",
                            description="The Game or Engine version you're importing from."
                                        "If the specific game isn't available, you can select the engine type.",
                            items=GMDGame.blender_props() + [("AUTODETECT", "Autodetect", "Autodetect version from GMD file")],
                            default="AUTODETECT")

    logging_categories: StringProperty(name="Debug Log Categories",
                                       description="Space-separated string of debug categories for logging.",
                                       default="ALL")

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = True  # No animation.

        # When properties are added, use "layout.prop" here to display them
        layout.prop(self, 'strict')
        layout.prop(self, 'import_hierarchy')
        layout.prop(self, 'import_objects')
        layout.prop(self, 'import_materials')
        layout.prop(self, 'material_naming')
        layout.prop(self, 'fuse_vertices')
        layout.prop(self, 'anim_skeleton')
        layout.prop(self, "game_enum")
        layout.prop(self, 'logging_categories')

    def create_logger(self) -> BlenderErrorReporter:
        debug_categories = set(self.logging_categories.split(" "))
        base_error_reporter = StrictErrorReporter(debug_categories) if self.strict else LenientErrorReporter(debug_categories)
        return BlenderErrorReporter(self.report, base_error_reporter)

    def create_gmd_config(self, gmd_version: VersionProperties, error: BlenderErrorReporter) -> GMDSceneCreatorConfig:
        engine_from_version = {
            GMDVersion.Kenzan: GMDGame.Engine_MagicalV,
            GMDVersion.Kiwami1: GMDGame.Engine_Kiwami,
            GMDVersion.Dragon: GMDGame.Engine_Dragon
        }
        engine_enum = engine_from_version[gmd_version.major_version]
        if self.game_enum == "AUTODETECT":
            game = engine_enum
        else:
            game = GMDGame.mapping_from_blender_props()[self.game_enum]
            if game & engine_enum == 0:
                # the specified game doesn't use the same engine as expected
                error.fatal(f"Expected a file from {GMDGame(game).name} but file uses engine {GMDGame(engine_enum).name}. Try using Autodetect, or change the engine version to be correct.")

        material_naming_from_enum ={
            "COLLECTION_SHADER": MaterialNamingType.Collection_Shader,
            "COLLECTION_TEXTURE": MaterialNamingType.Collection_DiffuseTexture,
            "TEXTURE": MaterialNamingType.DiffuseTexture,
        }

        return GMDSceneCreatorConfig(
            game=game,

            import_materials=self.import_materials,
            material_naming_convention=material_naming_from_enum[self.material_naming],

            fuse_vertices=self.fuse_vertices
        )

    def execute(self, context):
        error = self.create_logger()

        try:
            self.report({"INFO"}, "Extracting abstract scene...")
            gmd_version, gmd_header, gmd_contents = read_gmd_structures(self.filepath, error)
            gmd_config = self.create_gmd_config(gmd_version, error)
            gmd_scene = read_abstract_scene_from_filedata_object(gmd_version, gmd_contents, error)
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
                error.fatal(f"Some bones don't have unique names - found duplicates {duplicate_names}")

            # Check that objects do not have bones underneath them
            objects_depth_first = [node for node in gmd_scene.overall_hierarchy.depth_first_iterate() if not isinstance(node, GMDBone)]
            def check_objects_children(object: GMDNode):
                for child in object.children:
                    if isinstance(child, GMDBone):
                        error.fatal(f"Object {object.name} has child {child.name} which is a GMDBone - The importer expects that objects do not have bones as children")
                    check_objects_children(child)
            for object in objects_depth_first:
                check_objects_children(object)

            scene_creator = GMDSkinnedSceneCreator(self.filepath, gmd_scene, gmd_config, error)
            gmd_collection = scene_creator.make_collection(context)

            if self.import_hierarchy:
                self.report({"INFO"}, "Importing bone hierarchy...")
                gmd_armature = scene_creator.make_bone_hierarchy(context, gmd_collection, anim_skeleton=self.anim_skeleton)

            if self.import_objects:
                self.report({"INFO"}, "Importing objects...")
                scene_creator.make_objects(context, gmd_collection, gmd_armature if self.import_hierarchy else None)#self.import_materials)

            self.report({"INFO"}, f"Finished importing {gmd_scene.name}")
            return {'FINISHED'}
        except GMDImportExportError as e:
            print(e)
            self.report({"ERROR"}, str(e))
        return {'CANCELLED'}


def menu_func_import(self, context):
    self.layout.operator(ImportGMD.bl_idname, text='Yakuza GMD (.gmd)')
