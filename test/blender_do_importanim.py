import os

import bpy

YKGMDIO_TEST_SRC = os.environ["YKGMDIO_TEST_SRC"].replace("\\", "/")
YKGMDIO_SKINNED_METHOD = os.environ["YKGMDIO_SKINNED"]
YKGMDIO_LOGGING = os.environ["YKGMDIO_LOGGING"]

bpy.ops.preferences.addon_enable(module='yk_gmd_blender')

try:
    import yk_gmd_blender

    window = bpy.context.window_manager.windows[0]
    with bpy.context.temp_override(window=window):
        # Clean up the default scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        # Import the file
        print(f"Loading from {YKGMDIO_TEST_SRC}")
        if YKGMDIO_SKINNED_METHOD:
            bpy.ops.import_scene.gmd_animation_skinned(filepath=YKGMDIO_TEST_SRC, logging_categories=YKGMDIO_LOGGING)
        else:
            bpy.ops.import_scene.gmd_animation_unskinned(filepath=YKGMDIO_TEST_SRC, logging_categories=YKGMDIO_LOGGING)

finally:
    # Disable the addon
    # USe a context temp_override to set context.area
    with bpy.context.temp_override(area=bpy.data.screens["Layout"].areas[0]):
        bpy.ops.preferences.addon_disable(module='yk_gmd_blender')
