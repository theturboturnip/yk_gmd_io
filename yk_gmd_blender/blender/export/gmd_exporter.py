from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty)
from bpy.types import Operator, ShaderNodeGroup
from bpy_extras.io_utils import ExportHelper

from yk_gmd_blender.blender.common import armature_name_for_gmd_file, GMDGame
from yk_gmd_blender.blender.error_reporter import BlenderErrorReporter
from yk_gmd_blender.blender.materials import YAKUZA_SHADER_NODE_GROUP
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene, HierarchyData
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.converters.common.to_abstract import VertexImportMode, FileImportMode
from yk_gmd_blender.yk_gmd.v2.errors.error_classes import GMDImportExportError
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import StrictErrorReporter, LenientErrorReporter
from yk_gmd_blender.yk_gmd.v2.io import check_version_writeable, write_abstract_scene_out, \
    read_gmd_structures, read_abstract_scene_from_filedata_object
from yk_gmd_blender.yk_gmd.v2.structure.version import GMDVersion, VersionProperties

import os

class BaseExportGMD(Operator, ExportHelper):
    filename_ext = '.gmd'

    filter_glob: StringProperty(default='*.gmd', options={'HIDDEN'})

    strict: BoolProperty(name="Strict File Export",
                         description="If True, will fail the export even on recoverable errors.",
                         default=True)

    game_enum: EnumProperty(name="Game/Engine Version",
                            description="The Game or Engine version you're importing from."
                                        "If the specific game isn't available, you can select the engine type.",
                            items=GMDGame.blender_props() + [
                                ("AUTODETECT", "Autodetect", "Autodetect version from GMD file")],
                            default="AUTODETECT")

    logging_categories: StringProperty(name="Debug Log Categories",
                                       description="Space-separated string of debug categories for logging.",
                                       default="ALL")

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

class ExportSkinnedGMD(BaseExportGMD):
    """Export scene as glTF 2.0 file"""
    bl_idname = 'export_scene.gmd_skinned'
    bl_label = "Export Yakuza GMD [Skinned]"

    copy_bones_from_file: BoolProperty(name="Copy Bones from Original File",
                                       description="If True, will reuse the bone hierarchy in the original file.\n"
                                                   "If False, will export the bones from scratch.\n"
                                                   "WARNING: This is experimental - don't set it to False unless you know what you're doing.",
                                       default=True)
    debug_compare_matrices: BoolProperty(name="[DEBUG] Compare Matrices",
                                         description="If True, will print out a comparison of the scene matrices (for bones and unskinned objects)\n"
                                                     "between the original file and the new file.",
                                         default=False)
    # TODO - dry run feature
    #  when set, instead of exporting it will open a window with a report on what would be exported

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = True  # No animation.

        # When properties are added, use "layout.prop" here to display them
        layout.prop(self, 'strict')
        layout.prop(self, 'logging_categories')
        layout.prop(self, "game_enum")

        layout.prop(self, 'copy_bones_from_file')
        layout.prop(self, 'debug_compare_matrices')

    def execute(self, context):
        error = self.create_logger()

        try:
            filepath = self.filepath
            _, ext = os.path.splitext(filepath)
            if not ext == ".gmd":
                error.info(f"[Blender 2.93+ bug?] Filepath had no .gmd extension, adding one manually")
                filepath = f"{filepath}.gmd"

            error.info(f"Reading original file properties {filepath}")
            gmd_version, gmd_header, gmd_contents = read_gmd_structures(filepath, error)
            check_version_writeable(gmd_version, error)

            original_scene = GMDScene(
                name=gmd_contents.name.text,
                overall_hierarchy=HierarchyData([])
            )
            try_copy_bones = self.copy_bones_from_file
            if self.copy_bones_from_file or self.debug_compare_matrices:
                try:
                    original_scene = read_abstract_scene_from_filedata_object(gmd_version, FileImportMode.SKINNED, VertexImportMode.NO_VERTICES, gmd_contents, error)
                except Exception as e:
                    if self.copy_bones_from_file:
                        error.fatal(f"Original file failed to import properly, can't check bone hierarchy\nError: {e}")
                    else:
                        error.info(f"Original file failed to import properly, can't check bone hierarchy\nError: {e}")
                    try_copy_bones = False

            scene_gatherer = GMDSceneGatherer(original_scene, try_copy_bones, gmd_version.major_version, error)

            self.report({"INFO"}, "Extracting blender data into abstract scene...")
            scene_gatherer.validate_scene()

            scene_gatherer.gather_exported_items(context, self.debug_compare_matrices)
            self.report({"INFO"}, "Finished extracting abstract scene")

            gmd_scene = scene_gatherer.build()

            self.report({"INFO"}, f"Writing scene out...")
            write_abstract_scene_out(gmd_version,
                                     gmd_contents.file_is_big_endian(), gmd_contents.vertices_are_big_endian(),
                                     gmd_scene,
                                     filepath,
                                     error)

            self.report({"INFO"}, f"Finished exporting {gmd_scene.name}")
            return {'FINISHED'}
        except GMDImportExportError as e:
            print(e)
            self.report({"ERROR"}, str(e))
        return {'CANCELLED'}


def menu_func_export(self, context):
    self.layout.operator(ExportSkinnedGMD.bl_idname, text='Yakuza GMD [Skinned] (.gmd)')
