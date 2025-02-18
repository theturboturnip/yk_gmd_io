import os

from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       CollectionProperty)
from bpy.types import (
    Operator,
    OperatorFileListElement,
)
from bpy_extras.io_utils import ImportHelper
from ..common import GMDGame
from ..error_reporter import BlenderErrorReporter
from .scene_creators.animation import GMDAnimationSceneCreator
from .scene_creators.base import GMDSceneCreatorConfig, MaterialNamingType
from .scene_creators.skinned import GMDSkinnedSceneCreator
from .scene_creators.unskinned import GMDUnskinnedSceneCreator
from ...gmdlib.converters.common.to_abstract import FileImportMode, VertexImportMode
from ...gmdlib.errors.error_classes import GMDImportExportError
from ...gmdlib.errors.error_reporter import StrictErrorReporter, LenientErrorReporter
from ...gmdlib.io import read_abstract_scene_from_filedata_object, \
    read_gmd_structures
from ...gmdlib.structure.version import VersionProperties, GMDVersion


class BaseImportGMD:
    filter_glob: StringProperty(default="*.gmd", options={"HIDDEN"})

    # Selected files (allows for multi-import)
    files: CollectionProperty(name="File Path",
                              type=OperatorFileListElement)
    directory: StringProperty(
        subtype='DIR_PATH',
    )

    strict: BoolProperty(name="Strict File Import",
                         description="If True, will fail the import even on recoverable errors.",
                         default=True)
    stop_on_fail: BoolProperty(name="Stop on Failure",
                               description="If True, when importing multiple GMDs, an import failure in one file will "
                                           "stop all subsequent files from importing.",
                               default=True)

    import_materials: BoolProperty(name="Import Materials",
                                   description="If True, will import materials. "
                                               "If False, all objects will not have any materials. "
                                               "This is required if you want to export the scene later.",
                                   default=True)
    material_naming: EnumProperty(name="Material Naming",
                                  description="How materials are named",
                                  items=[
                                      ("COLLECTION_SHADER", "[Collection]_[Shader]", "Collection name and Shader name"),
                                      ("COLLECTION_TEXTURE", "[Collection]_[Texture]",
                                       "Collection name and Diffuse Texture name"),
                                      ("TEXTURE", "[Texture]", "Diffuse Texture name"),
                                  ],
                                  default="COLLECTION_TEXTURE")

    fuse_vertices: BoolProperty(name="Fuse Vertices",
                                description="If True, meshes that are attached to the same object "
                                            "will have duplicate vertices removed.",
                                default=True)

    custom_split_normals: BoolProperty(name="Custom Split Normals",
                                       description="If True, will use the custom split normals feature "
                                                   "to exactly preserve normals.",
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
        base_error_reporter = StrictErrorReporter(debug_categories) if self.strict else LenientErrorReporter(
            debug_categories)
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
                error.fatal(
                    f"Expected a file from {GMDGame(game).name} but file uses engine {GMDGame(engine_enum).name}. "
                    f"Try using Autodetect, or change the engine version to be correct.")

        material_naming_from_enum = {
            "COLLECTION_SHADER": MaterialNamingType.Collection_Shader,
            "COLLECTION_TEXTURE": MaterialNamingType.Collection_DiffuseTexture,
            "TEXTURE": MaterialNamingType.DiffuseTexture,
        }

        return GMDSceneCreatorConfig(
            game=game,

            import_materials=self.import_materials,
            material_naming_convention=material_naming_from_enum[self.material_naming],

            fuse_vertices=self.fuse_vertices,
            custom_split_normals=self.custom_split_normals,
        )


class ImportSkinnedGMD(BaseImportGMD, Operator, ImportHelper):
    """Loads a GMD file into blender"""
    bl_idname = "import_scene.gmd_skinned"
    bl_label = "Import Yakuza Skinned GMD for Modelling"

    import_hierarchy: BoolProperty(name="Import Hierarchy",
                                   description="If True, will import the full node hierarchy including skeleton bones. "
                                               "This is required if you want to export the scene later. "
                                               "Skinned meshes will be imported with bone weights.",
                                   default=True)
    import_objects: BoolProperty(name="Import Objects",
                                 description="If True, will import the full object hierarchy. "
                                             "This is required if you want to export the scene later.",
                                 default=True)

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = True  # No animation.

        # When properties are added, use "layout.prop" here to display them
        layout.prop(self, 'strict')
        layout.prop(self, 'stop_on_fail')
        layout.prop(self, 'logging_categories')
        layout.prop(self, "game_enum")
        layout.prop(self, 'import_materials')
        layout.prop(self, 'material_naming')
        layout.prop(self, 'fuse_vertices')
        layout.prop(self, 'custom_split_normals')

        layout.prop(self, 'import_hierarchy')
        layout.prop(self, 'import_objects')

    def execute(self, context):
        error = self.create_logger()

        if self.files:
            successes = 0
            base_folder = self.directory
            for f in self.files:
                gmd_filepath = os.path.join(base_folder, f.name)

                try:
                    self.import_single(context, gmd_filepath, error)
                    successes += 1
                except GMDImportExportError as e:
                    print(e)
                    self.report({"ERROR"}, str(e))
                    # If one failure should stop subsequent files from importing, return here.
                    # Otherwise, the loop will continue.
                    if self.stop_on_fail:
                        if len(self.files) > 1:
                            self.report({"ERROR"}, f"Stopped importing because of error in file {f.name}")
                        return {'CANCELLED'}

            if len(self.files) > 1:
                self.report({"INFO"}, f"Successfully imported {successes} of {len(self.files)} files")
        else:
            self.import_single(context, self.filepath, error)

        return {'FINISHED'}

    def import_single(self, context, gmd_filepath, error):
        if (not os.path.isfile(gmd_filepath)) or (not gmd_filepath.lower().endswith("gmd")):
            error.fatal(f"{gmd_filepath} is not a gmd file.")

        self.report({"INFO"}, f"Importing {gmd_filepath}...")

        self.report({"INFO"}, "Extracting abstract scene...")
        gmd_version, gmd_header, gmd_contents = read_gmd_structures(gmd_filepath, error)
        gmd_config = self.create_gmd_config(gmd_version, error)
        gmd_scene = read_abstract_scene_from_filedata_object(gmd_version, FileImportMode.SKINNED,
                                                             VertexImportMode.IMPORT_VERTICES, gmd_contents,
                                                             error)
        self.report({"INFO"}, "Finished extracting abstract scene")

        scene_creator = GMDSkinnedSceneCreator(gmd_filepath, gmd_scene, gmd_config, error)

        scene_creator.validate_scene()

        gmd_collection = scene_creator.make_collection(context)

        if self.import_hierarchy:
            self.report({"INFO"}, "Importing bone hierarchy...")
            gmd_armature = scene_creator.make_bone_hierarchy(context, gmd_collection)

        if self.import_objects:
            self.report({"INFO"}, "Importing objects...")
            scene_creator.make_objects(context, gmd_collection, gmd_armature if self.import_hierarchy else None)

        self.report({"INFO"}, f"Finished importing {gmd_scene.name}")


def menu_func_import_skinned(self, context):
    self.layout.operator(ImportSkinnedGMD.bl_idname, text="Yakuza Skinned GMD for Modelling [Characters] (.gmd)")


class ImportUnskinnedGMD(BaseImportGMD, Operator, ImportHelper):
    """Loads a GMD file into blender"""
    bl_idname = "import_scene.gmd_unskinned"
    bl_label = "Import Yakuza Unskinned GMD for Modelling"

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = True  # No animation.

        # When properties are added, use "layout.prop" here to display them
        layout.prop(self, 'strict')
        layout.prop(self, 'stop_on_fail')
        layout.prop(self, 'logging_categories')
        layout.prop(self, "game_enum")
        layout.prop(self, 'import_materials')
        layout.prop(self, 'material_naming')
        layout.prop(self, 'fuse_vertices')
        layout.prop(self, 'custom_split_normals')

    def execute(self, context):
        error = self.create_logger()

        if self.files:
            successes = 0
            base_folder = self.directory
            for f in self.files:
                gmd_filepath = os.path.join(base_folder, f.name)
                try:
                    self.import_single(context, gmd_filepath, error)
                    successes += 1
                except GMDImportExportError as e:
                    print(e)
                    self.report({"ERROR"}, str(e))
                    # If one failure should stop subsequent files from importing, return here.
                    # Otherwise, the loop will continue.
                    if self.stop_on_fail:
                        if len(self.files) > 1:
                            self.report({"ERROR"}, f"Stopped importing because of error in file {f.name}")
                        return {'CANCELLED'}

            if len(self.files) > 1:
                self.report({"INFO"}, f"Successfully imported {successes} of {len(self.files)} files")
        else:
            self.import_single(context, self.filepath, error)

        return {'FINISHED'}

    def import_single(self, context, gmd_filepath, error):
        if (not os.path.isfile(gmd_filepath)) or (not gmd_filepath.lower().endswith("gmd")):
            error.fatal(f"{gmd_filepath} is not a gmd file.")

        self.report({"INFO"}, f"Importing {gmd_filepath}...")

        self.report({"INFO"}, "Extracting abstract scene...")
        gmd_version, gmd_header, gmd_contents = read_gmd_structures(gmd_filepath, error)
        gmd_config = self.create_gmd_config(gmd_version, error)
        gmd_scene = read_abstract_scene_from_filedata_object(gmd_version, FileImportMode.UNSKINNED,
                                                             VertexImportMode.IMPORT_VERTICES, gmd_contents,
                                                             error)
        self.report({"INFO"}, "Finished extracting abstract scene")

        scene_creator = GMDUnskinnedSceneCreator(gmd_filepath, gmd_scene, gmd_config, error)

        scene_creator.validate_scene()

        gmd_collection = scene_creator.make_collection(context)

        self.report({"INFO"}, "Importing objects...")
        scene_creator.make_objects(gmd_collection)

        self.report({"INFO"}, f"Finished importing {gmd_scene.name}")


def menu_func_import_unskinned(self, context):
    self.layout.operator(ImportUnskinnedGMD.bl_idname, text="Yakuza Unskinned GMD for Modelling [Props/Stages] (.gmd)")


# Abstract base class for importers that use GMDAnimationSceneCreator.
# Only abstract function is the one that specifies file import mode.
class BaseImportAnimationGMD(BaseImportGMD, Operator, ImportHelper):
    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = True  # No animation.

        # When properties are added, use "layout.prop" here to display them
        layout.prop(self, 'strict')
        layout.prop(self, 'stop_on_fail')
        layout.prop(self, 'logging_categories')
        layout.prop(self, "game_enum")
        layout.prop(self, 'import_materials')
        layout.prop(self, 'material_naming')
        layout.prop(self, 'fuse_vertices')

    def execute(self, context):
        error = self.create_logger()

        if self.files:
            successes = 0
            base_folder = self.directory
            for f in self.files:
                gmd_filepath = os.path.join(base_folder, f.name)
                try:
                    self.import_single(context, gmd_filepath, error)
                    successes += 1
                except GMDImportExportError as e:
                    print(e)
                    self.report({"ERROR"}, str(e))
                    # If one failure should stop subsequent files from importing, return here.
                    # Otherwise, the loop will continue.
                    if self.stop_on_fail:
                        if len(self.files) > 1:
                            self.report({"ERROR"}, f"Stopped importing because of error in file {f.name}")
                        return {'CANCELLED'}

            if len(self.files) > 1:
                self.report({"INFO"}, f"Successfully imported {successes} of {len(self.files)} files")
        else:
            self.import_single(context, self.filepath, error)

        return {'FINISHED'}

    def file_import_mode(self) -> FileImportMode:
        raise NotImplementedError()

    def import_single(self, context, gmd_filepath, error):
        if (not os.path.isfile(gmd_filepath)) or (not gmd_filepath.lower().endswith("gmd")):
            error.fatal(f"{gmd_filepath} is not a gmd file.")

        self.report({"INFO"}, f"Importing {gmd_filepath}...")

        self.report({"INFO"}, "Extracting abstract scene...")
        gmd_version, gmd_header, gmd_contents = read_gmd_structures(gmd_filepath, error)
        gmd_config = self.create_gmd_config(gmd_version, error)
        gmd_scene = read_abstract_scene_from_filedata_object(gmd_version, self.file_import_mode(),
                                                             VertexImportMode.IMPORT_VERTICES, gmd_contents,
                                                             error)
        self.report({"INFO"}, "Finished extracting abstract scene")

        scene_creator = GMDAnimationSceneCreator(gmd_filepath, gmd_scene, gmd_config, error)

        scene_creator.validate_scene()

        gmd_collection = scene_creator.make_collection(context)

        self.report({"INFO"}, "Importing bone hierarchy...")
        gmd_armature, node_id_to_blender_bone_name = scene_creator.make_bone_hierarchy(context, gmd_collection)
        self.report({"INFO"}, "Importing objects...")
        scene_creator.make_objects(context, gmd_collection, gmd_armature, node_id_to_blender_bone_name)

        self.report({"INFO"}, f"Finished importing {gmd_scene.name}")


class ImportAnimationUnskinnedGMD(BaseImportAnimationGMD):
    """Loads a GMD file into blender"""
    bl_idname = "import_scene.gmd_animation_unskinned"
    bl_label = "Import Yakuza Unskinned GMD for Animation"

    def file_import_mode(self) -> FileImportMode:
        return FileImportMode.UNSKINNED


class ImportAnimationSkinnedGMD(BaseImportAnimationGMD):
    """Loads a GMD file into blender"""
    bl_idname = "import_scene.gmd_animation_skinned"
    bl_label = "Import Yakuza Skinned GMD for Animation"

    def file_import_mode(self) -> FileImportMode:
        return FileImportMode.SKINNED


def menu_func_import_animation_unskinned(self, context):
    self.layout.operator(ImportAnimationUnskinnedGMD.bl_idname,
                         text="Yakuza Unskinned GMD for Animation [Props/Stages] (.gmd)")


# This allows you to use the legacy animation option where bones are not connected to their parents.
def menu_func_import_animation_skinned(self, context):
    self.layout.operator(ImportAnimationSkinnedGMD.bl_idname,
                         text="Yakuza Skinned GMD for Animation [Characters] (.gmd)")
