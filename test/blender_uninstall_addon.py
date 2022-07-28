import bpy

with bpy.context.temp_override(area=bpy.data.screens["Layout"].areas[0]):
    bpy.ops.preferences.addon_remove(module='yk_gmd_blender')
