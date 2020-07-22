import os

from yk_gmd_blender.blender.error import GMDError
from yk_gmd_blender.blender.exporter import GMDExporter

bl_info = {
    "name": "Yakuza GMD File Import/Export",
    "author": "Samuel Stark (TheTurboTurnip)",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Yakuza GMD Files (only tested with YK1)",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

# This file is based on https://github.com/KhronosGroup/glTF-Blender-IO/blob/master/addons/io_scene_gltf2/__init__.py

#
# Script reloading (if the user calls 'Reload Scripts' from Blender)
#

def reload_package(module_dict_main):
    import importlib
    from pathlib import Path

    def reload_package_recursive(current_dir, module_dict):
        for path in current_dir.iterdir():
            if "__init__" in str(path) or path.stem not in module_dict:
                continue

            if path.is_file() and path.suffix == ".py":
                importlib.reload(module_dict[path.stem])
            elif path.is_dir():
                reload_package_recursive(path, module_dict[path.stem].__dict__)

    reload_package_recursive(Path(__file__).parent, module_dict_main)


if "bpy" in locals():
    reload_package(locals())

#
# Import Class
#
import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       CollectionProperty)
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper

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
        from yk_gmd_blender.blender.importer import GMDImporter
        import time

        start_time = time.time()
        importer = GMDImporter(filepath, import_settings)
        importer.read()
        importer.check()
        importer.add_items(context)
        elapsed_s = "{:.2f}s".format(time.time() - start_time)
        print("GMD import finished in " + elapsed_s)

        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(ImportGMD.bl_idname, text='Yakuza GMD (.gmd)')


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

classes = (ImportGMD, ExportGMD)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    # bpy.utils.register_module(__name__)

    # add to the export / import menu
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    #for f in extension_panel_unregister_functors:
    #    f()
    #extension_panel_unregister_functors.clear()

    # bpy.utils.unregister_module(__name__)

    # remove from the export / import menu
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)