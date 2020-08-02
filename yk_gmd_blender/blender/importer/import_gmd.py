import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       CollectionProperty)
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper

from yk_gmd_blender.blender.error import GMDError

class ImportGMD(Operator, ImportHelper):
    """Loads a GMD file into blender"""
    bl_idname = "import_scene.gmd"
    bl_label = "Import Yakuza GMD (YK1)"

    filter_glob: StringProperty(default="*.gmd", options={"HIDDEN"})
    #files: CollectionProperty(
    #    name="File Path",
    #    type=bpy.types.OperatorFileListElement,
    #)
    # Only allow importing one file at a time
    #file: StringProperty(name="File Path", subtype="FILE_PATH")

    load_materials: BoolProperty(name="Load Materials", default=True)
    load_bones: BoolProperty(name="Load Bones", default=True)
    # TODO option for setting armature to "display in front" in the viewport"
    validate_meshes: BoolProperty(name="Validate Meshes", description="Run the Blender mesh validation on each loaded mesh. Debug only", default=False)
    merge_meshes: BoolProperty(name="Merge Meshes", description="Merge all meshes into a single mesh", default=False)

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = True  # No animation.

        layout.prop(self, 'load_materials')
        layout.prop(self, 'load_bones')
        layout.prop(self, 'validate_meshes')
        layout.prop(self, 'merge_meshes')

    def execute(self, context):
        return self.import_gmd(context)

    def import_gmd(self, context):
        return self.unit_import(context, self.filepath, self.as_keywords(ignore=("filter_glob",)))

    def unit_import(self, context, filepath, import_settings):
        from yk_gmd_blender.blender.importer.importer import GMDImporter
        import time

        try:
            start_time = time.time()

            importer = GMDImporter(filepath, import_settings)
            importer.read()
            importer.check()
            importer.add_items(context)

            elapsed_s = "{:.2f}s".format(time.time() - start_time)
            print("GMD import finished in " + elapsed_s)

            return {'FINISHED'}
        except GMDError as error:
            print("Catching Error")
            self.report({"ERROR"}, str(error))
        return {'CANCELLED'}

def menu_func_import(self, context):
    self.layout.operator(ImportGMD.bl_idname, text='Yakuza GMD (.gmd)')