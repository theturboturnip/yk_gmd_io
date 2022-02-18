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

from yk_gmd_blender.blender.common import GMDGame
from yk_gmd_blender.blender.error_reporter import BlenderErrorReporter
from yk_gmd_blender.blender.importer.scene_creators.base import GMDSceneCreatorConfig, MaterialNamingType
from yk_gmd_blender.blender.importer.scene_creators.skinned import GMDSkinnedSceneCreator
from yk_gmd_blender.blender.importer.scene_creators.unskinned import GMDUnskinnedSceneCreator
from yk_gmd_blender.yk_gmd.v2.converters.common.to_abstract import FileImportMode, VertexImportMode
from yk_gmd_blender.yk_gmd.v2.errors.error_classes import GMDImportExportError
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import StrictErrorReporter, LenientErrorReporter
from yk_gmd_blender.yk_gmd.v2.io import read_abstract_scene_from_filedata_object, \
    read_gmd_structures
from yk_gmd_blender.yk_gmd.v2.structure.version import VersionProperties, GMDVersion


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
                                   description="If True, will import materials. If False, all objects will not have any materials. "
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
                                description="If True, meshes that are attached to the same object will have duplicate vertices removed.",
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


class ImportSkinnedGMD(BaseImportGMD, Operator, ImportHelper):
    """Loads a GMD file into blender"""
    bl_idname = "import_scene.gmd_skinned"
    bl_label = "Import Yakuza GMD [Characters/Skinned]"

    import_hierarchy: BoolProperty(name="Import Hierarchy",
                                   description="If True, will import the full node hierarchy including skeleton bones. "
                                               "This is required if you want to export the scene later. "
                                               "Skinned meshes will be imported with bone weights.",
                                   default=True)
    import_objects: BoolProperty(name="Import Objects",
                                 description="If True, will import the full object hierarchy. "
                                             "This is required if you want to export the scene later.",
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
        layout.prop(self, 'stop_on_fail')
        layout.prop(self, 'logging_categories')
        layout.prop(self, "game_enum")
        layout.prop(self, 'import_materials')
        layout.prop(self, 'material_naming')
        layout.prop(self, 'fuse_vertices')

        layout.prop(self, 'import_hierarchy')
        layout.prop(self, 'import_objects')
        layout.prop(self, 'anim_skeleton')

    def execute(self, context):
        error = self.create_logger()

        successes = 0
        base_folder = self.directory
        for f in self.files:
            gmd_filepath = os.path.join(base_folder, f.name)

            try:
                if (not os.path.isfile(gmd_filepath)) or (not gmd_filepath.lower().endswith("gmd")):
                    error.fatal(f"{gmd_filepath} is not a gmd file.")

                self.report({"INFO"}, f"Importing {f.name}...")

                self.report({"INFO"}, "Extracting abstract scene...")
                gmd_version, gmd_header, gmd_contents = read_gmd_structures(gmd_filepath, error)
                gmd_config = self.create_gmd_config(gmd_version, error)
                gmd_scene = read_abstract_scene_from_filedata_object(gmd_version, FileImportMode.SKINNED, VertexImportMode.IMPORT_VERTICES, gmd_contents, error)
                self.report({"INFO"}, "Finished extracting abstract scene")

                scene_creator = GMDSkinnedSceneCreator(gmd_filepath, gmd_scene, gmd_config, error)

                scene_creator.validate_scene()

                gmd_collection = scene_creator.make_collection(context)

                if self.import_hierarchy:
                    self.report({"INFO"}, "Importing bone hierarchy...")
                    gmd_armature = scene_creator.make_bone_hierarchy(context, gmd_collection, anim_skeleton=self.anim_skeleton)

                if self.import_objects:
                    self.report({"INFO"}, "Importing objects...")
                    scene_creator.make_objects(context, gmd_collection, gmd_armature if self.import_hierarchy else None)

                self.report({"INFO"}, f"Finished importing {gmd_scene.name}")

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

        return {'FINISHED'}


def menu_func_import_skinned(self, context):
    self.layout.operator(ImportSkinnedGMD.bl_idname, text="Yakuza GMD [Characters/Skinned] (.gmd)")


class ImportUnskinnedGMD(BaseImportGMD, Operator, ImportHelper):
    """Loads a GMD file into blender"""
    bl_idname = "import_scene.gmd_unskinned"
    bl_label = "Import Yakuza GMD [Stages/Weapons/Unskinned]"

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

        successes = 0
        base_folder = self.directory
        for f in self.files:
            gmd_filepath = os.path.join(base_folder, f.name)

            try:
                if (not os.path.isfile(gmd_filepath)) or (not gmd_filepath.lower().endswith("gmd")):
                    error.fatal(f"{gmd_filepath} is not a gmd file.")

                self.report({"INFO"}, f"Importing {f.name}...")

                self.report({"INFO"}, "Extracting abstract scene...")
                gmd_version, gmd_header, gmd_contents = read_gmd_structures(gmd_filepath, error)
                gmd_config = self.create_gmd_config(gmd_version, error)
                gmd_scene = read_abstract_scene_from_filedata_object(gmd_version, FileImportMode.UNSKINNED, VertexImportMode.IMPORT_VERTICES, gmd_contents, error)
                self.report({"INFO"}, "Finished extracting abstract scene")

                scene_creator = GMDUnskinnedSceneCreator(gmd_filepath, gmd_scene, gmd_config, error)

                scene_creator.validate_scene()

                gmd_collection = scene_creator.make_collection(context)

                self.report({"INFO"}, "Importing objects...")
                scene_creator.make_objects(gmd_collection)

                self.report({"INFO"}, f"Finished importing {gmd_scene.name}")
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

        return {'FINISHED'}


def menu_func_import_unskinned(self, context):
    self.layout.operator(ImportUnskinnedGMD.bl_idname, text="Yakuza GMD [Stages/Weapons/Unskinned] (.gmd)")