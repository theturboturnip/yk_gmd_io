import os

import bpy

YKGMDIO_TEST_SRC = os.environ["YKGMDIO_TEST_SRC"].replace("\\", "/")
YKGMDIO_TEST_DST = os.environ["YKGMDIO_TEST_DST"].replace("\\", "/")
YKGMDIO_SKINNED = (os.environ["YKGMDIO_SKINNED"] == "True")

bpy.ops.preferences.addon_enable(module='yk_gmd_blender')

if YKGMDIO_TEST_SRC == YKGMDIO_TEST_DST:
    raise RuntimeError(f"Tried to import and export to the same location {YKGMDIO_TEST_SRC}")

try:
    import yk_gmd_blender

    window = bpy.context.window_manager.windows[0]
    with bpy.context.temp_override(window=window):
        # Clean up the default scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        # Import the file
        print(f"Loading from {YKGMDIO_TEST_SRC}")
        if YKGMDIO_SKINNED:
            bpy.ops.import_scene.gmd_skinned(filepath=YKGMDIO_TEST_SRC, logging_categories="")
        else:
            bpy.ops.import_scene.gmd_unskinned(filepath=YKGMDIO_TEST_SRC, logging_categories="")

        # Select the top-level object in the first collection
        toplevel_collection = next(k for k in bpy.data.collections.keys() if k != "Collection")
        toplevel_object = next(o for o in bpy.data.collections[toplevel_collection].objects if o.parent is None)
        bpy.context.view_layer.objects.active = toplevel_object

        # Export to the destination
        if YKGMDIO_SKINNED:
            bpy.ops.export_scene.gmd_skinned(filepath=YKGMDIO_TEST_DST, logging_categories="")
        else:
            bpy.ops.export_scene.gmd_unskinned(filepath=YKGMDIO_TEST_DST, logging_categories="")
finally:
    # Disable the addon
    # USe a context temp_override to set context.area
    with bpy.context.temp_override(area=bpy.data.screens["Layout"].areas[0]):
        bpy.ops.preferences.addon_disable(module='yk_gmd_blender')
