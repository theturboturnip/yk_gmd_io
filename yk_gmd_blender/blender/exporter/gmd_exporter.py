import os

from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty, IntProperty)
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from ..common import GMDGame
from ..error_reporter import BlenderErrorReporter
from .scene_gatherers.base import GMDSceneGathererConfig, BoundingBoxCalc
from .scene_gatherers.skinned import SkinnedBoneMatrixOrigin, SkinnedGMDSceneGatherer, \
    GMDSkinnedSceneGathererConfig
from .scene_gatherers.unskinned import UnskinnedGMDSceneGatherer
from ...gmdlib.converters.common.to_abstract import VertexImportMode, FileImportMode
from ...gmdlib.errors.error_classes import GMDImportExportError
from ...gmdlib.errors.error_reporter import StrictErrorReporter, LenientErrorReporter
from ...gmdlib.io import check_version_writeable, write_abstract_scene_out, \
    read_gmd_structures, read_abstract_scene_from_filedata_object
from ...gmdlib.structure.version import GMDVersion, VersionProperties


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

    bounding_box_enum: EnumProperty(name="Bounding Boxes",
                                    description="How bounding boxes are calculated for each item. May affect stage export.",
                                    items=BoundingBoxCalc.blender_props(),
                                    default="OLD_INFINITE")

    logging_categories: StringProperty(name="Debug Log Categories",
                                       description="Space-separated string of debug categories for logging.",
                                       default="ALL")

    debug_compare_matrices: BoolProperty(name="[DEBUG] Compare Matrices",
                                         description="If True, will print out a comparison of the scene matrices "
                                                     "(for bones and unskinned objects)\n"
                                                     "between the original file and the new file.",
                                         default=False)

    def create_logger(self) -> BlenderErrorReporter:
        debug_categories = set(self.logging_categories.split(" "))
        base_error_reporter = StrictErrorReporter(debug_categories) if self.strict else LenientErrorReporter(
            debug_categories)
        return BlenderErrorReporter(self.report, base_error_reporter)

    def create_gmd_config(self, gmd_version: VersionProperties, error: BlenderErrorReporter) -> GMDSceneGathererConfig:
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
                error.fatal(
                    f"Expected a file from {GMDGame(game).name} but file uses engine {GMDGame(engine_enum).name}. "
                    f"Try using Autodetect, or change the engine version to be correct.")

        return GMDSceneGathererConfig(
            game=game,
            bounding_box_calc=BoundingBoxCalc.map_from_blender_props(self.bounding_box_enum),
            debug_compare_matrices=self.debug_compare_matrices
        )


class ExportSkinnedGMD(BaseExportGMD):
    """Export scene as glTF 2.0 file"""
    bl_idname = 'export_scene.gmd_skinned'
    bl_label = "Export Yakuza GMD [Skinned]"

    bone_matrix_origin: EnumProperty(name="Bone Matrices",
                                     description="How the addon should calculate a bone's animation matrices.",
                                     items=[
                                         ("CALCULATE", "Arbitrary Skeleton [ADVANCED]",
                                          "Export the skeleton with any changes made in Blender.\n"
                                          "May break in-game animations or crash the game.\n"
                                          "Only use this if you know what you are doing."),
                                         ("FROM_TARGET_FILE", "Keep Target Skeleton",
                                          "Keep the skeleton in the target file.\n"
                                          "The current skeleton must match the skeleton you're exporting over."),
                                         ("FROM_ORIGINAL_GMD_IMPORT", "Keep Original Imported Skeleton",
                                          "Keep the values originally imported for this skeleton.\n"
                                          "The current skeleton must have been imported from a GMD file.")
                                     ],
                                     default="FROM_TARGET_FILE")

    autodetect_bone_limit: BoolProperty(name="Autodetect Bone Limit",
                                        description="Automatically find the maximum amount of bones per mesh.\n"
                                                    "Pre-DE games have at most 32 bones per mesh, the addon splits\n"
                                                    "meshes up to stay within this. DE doesn't have a known limit,\n"
                                                    "but we use 256 to be on the safe side.",
                                        default=True)
    manual_bone_limit: IntProperty(name="Manual Bone Limit",
                                   description="Set the maximum bone count manually.\nUse at your own risk!",
                                   default=32,
                                   min=1)

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
        layout.prop(self, "bounding_box_enum")

        layout.prop(self, 'bone_matrix_origin')
        layout.prop(self, 'debug_compare_matrices')
        layout.prop(self, 'autodetect_bone_limit')
        if not self.autodetect_bone_limit:
            layout.prop(self, 'manual_bone_limit')

    def create_skinned_gmd_config(
            self, gmd_version: VersionProperties, error: BlenderErrorReporter
    ) -> GMDSkinnedSceneGathererConfig:
        base_config = self.create_gmd_config(gmd_version, error)
        if self.autodetect_bone_limit:
            bone_limit = 256 if (base_config.game & GMDGame.Engine_Dragon) else 32
        else:
            bone_limit = 32 if self.manual_bone_limit <= 0 else self.manual_bone_limit
        return GMDSkinnedSceneGathererConfig(game=base_config.game,
                                             bounding_box_calc=base_config.bounding_box_calc,
                                             debug_compare_matrices=base_config.debug_compare_matrices,
                                             bone_limit=bone_limit)

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
            gmd_config = self.create_skinned_gmd_config(gmd_version, error)
            check_version_writeable(gmd_version, error)

            bone_matrix_origin = {
                "CALCULATE": SkinnedBoneMatrixOrigin.Calculate,
                "FROM_TARGET_FILE": SkinnedBoneMatrixOrigin.FromTargetFile,
                "FROM_ORIGINAL_GMD_IMPORT": SkinnedBoneMatrixOrigin.FromOriginalGMDImport,
            }[self.bone_matrix_origin]

            try:
                original_scene = read_abstract_scene_from_filedata_object(gmd_version, FileImportMode.SKINNED,
                                                                          VertexImportMode.NO_VERTICES, gmd_contents,
                                                                          error)
            except Exception as e:
                error.fatal(f"Original file failed to import properly, can't check flags or bone hierarchy\nError: {e}")

            scene_gatherer = SkinnedGMDSceneGatherer(filepath, original_scene, gmd_config, bone_matrix_origin, error)

            self.report({"INFO"}, "Extracting blender data into abstract scene...")

            scene_gatherer.gather_exported_items(context)
            self.report({"INFO"}, "Finished extracting abstract scene")

            gmd_scene = scene_gatherer.build()

            self.report({"INFO"}, f"Writing scene out...")
            write_abstract_scene_out(gmd_version,
                                     gmd_contents.file_is_big_endian(), gmd_contents.vertices_are_big_endian(),
                                     gmd_scene,
                                     gmd_contents,
                                     filepath,
                                     error)

            self.report({"INFO"}, f"Finished exporting {gmd_scene.name}")
            return {'FINISHED'}
        except GMDImportExportError as e:
            print(e)
            self.report({"ERROR"}, str(e))
        return {'CANCELLED'}


def menu_func_export_skinned(self, context):
    self.layout.operator(ExportSkinnedGMD.bl_idname, text='Yakuza GMD [Skinned] (.gmd)')


class ExportUnskinnedGMD(BaseExportGMD):
    """Export scene as glTF 2.0 file"""
    bl_idname = 'export_scene.gmd_unskinned'
    bl_label = "Export Yakuza GMD [Unskinned]"

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
        layout.prop(self, "bounding_box_enum")

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
            gmd_config = self.create_gmd_config(gmd_version, error)
            check_version_writeable(gmd_version, error)

            try:
                original_scene = read_abstract_scene_from_filedata_object(gmd_version, FileImportMode.SKINNED,
                                                                          VertexImportMode.NO_VERTICES, gmd_contents,
                                                                          error)
            except Exception as e:
                error.info(f"Original file failed to import properly, can't check bone hierarchy\nError: {e}")

            scene_gatherer = UnskinnedGMDSceneGatherer(filepath, original_scene, gmd_config, error, False)

            self.report({"INFO"}, "Extracting blender data into abstract scene...")

            scene_gatherer.gather_exported_items(context)
            self.report({"INFO"}, "Finished extracting abstract scene")

            gmd_scene = scene_gatherer.build()

            self.report({"INFO"}, f"Writing scene out...")
            write_abstract_scene_out(gmd_version,
                                     gmd_contents.file_is_big_endian(), gmd_contents.vertices_are_big_endian(),
                                     gmd_scene,
                                     gmd_contents,
                                     filepath,
                                     error)

            self.report({"INFO"}, f"Finished exporting {gmd_scene.name}")
            return {'FINISHED'}
        except GMDImportExportError as e:
            print(e)
            self.report({"ERROR"}, str(e))
        return {'CANCELLED'}


def menu_func_export_unskinned(self, context):
    self.layout.operator(ExportUnskinnedGMD.bl_idname, text='Yakuza GMD [Unskinned] (.gmd)')
