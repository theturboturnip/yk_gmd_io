import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       CollectionProperty)
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper

from yk_gmd_blender.blender.error import GMDError
from yk_gmd_blender.blender.export.exporter import GMDExporter


class ExportGMD(bpy.types.Operator, ExportHelper):
    """Export scene as glTF 2.0 file"""
    bl_idname = 'export_scene.gmd'
    bl_label = "Export Yakuza GMD (YK1)"

    filename_ext = ''

    filter_glob: StringProperty(default='*.gmd', options={'HIDDEN'})

    def execute(self, context):
        exporter = GMDExporter(self.filepath, self.as_keywords(ignore=("filter_glob",)))
        try:
            exporter.read_base_file()
            exporter.check()
            exporter.update_gmd_submeshes()
            exporter.overwrite_file_with_abstraction()
            self.report({'INFO'}, f"Finished export to {self.filepath}")
            return {"FINISHED"}
        except GMDError as error:
            print("Catching Error")
            self.report({"ERROR"}, str(error))
        return {"CANCELLED"}

def menu_func_export(self, context):
    self.layout.operator(ExportGMD.bl_idname, text='Yakuza GMD (.gmd)')
