import os

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       CollectionProperty)
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper

from yk_gmd_blender.blender.error_reporter import BlenderErrorReporter
from yk_gmd_blender.yk_gmd.v2.errors.error_classes import GMDImportExportError
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import StrictErrorReporter, LenientErrorReporter
from yk_gmd_blender.yk_gmd.v2.io import read_abstract_scene


class ImportGMD(Operator, ImportHelper):
    """Loads a GMD file into blender"""
    bl_idname = "import_scene.gmd"
    bl_label = "Import Yakuza GMD"

    filter_glob: StringProperty(default="*.gmd", options={"HIDDEN"})

    strict: BoolProperty(name="Strict File Import",
                         description="If True, will fail the import even on recoverable errors.",
                         default=True)

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = True  # No animation.

        # When properties are added, use "layout.prop" here to display them
        # layout.prop(self, 'load_materials')
        # layout.prop(self, 'load_bones')
        # layout.prop(self, 'validate_meshes')
        # layout.prop(self, 'merge_meshes')
        layout.prop(self, 'strict')

    def execute(self, context):
        base_error_reporter = StrictErrorReporter() if self.strict else LenientErrorReporter()
        error_reporter = BlenderErrorReporter(self.report, base_error_reporter)

        try:
            self.report({"INFO"}, "Extracting abstract scene...")
            scene = read_abstract_scene(self.filepath, error_reporter)
            self.report({"INFO"}, "Finished extracting abstract scene")

            return {'FINISHED'}
        except GMDImportExportError as e:
            print(e)
            self.report({"ERROR"}, str(e))
        return {'CANCELLED'}

def menu_func_import(self, context):
    self.layout.operator(ImportGMD.bl_idname, text='Yakuza GMD (.gmd)')