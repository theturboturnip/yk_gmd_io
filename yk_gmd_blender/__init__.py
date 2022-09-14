# Include the bl_info at the top level always
bl_info = {
    "name": "Yakuza GMD File Import/Export",
    "author": "Samuel Stark (TheTurboTurnip)",
    "version": (0, 4, 0),
    "blender": (3, 2, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Yakuza GMD Files",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

# Check if we're in Blender by seeing if bpy.app.version exists.
# We can't just check for the presence of bpy, because the type library sets that.

try:
    import bpy.app

    bpy_app_present = True
except ImportError:
    bpy_app_present = False
    pass

if bpy_app_present:
    if getattr(bpy.app, "version", None) is not None:
        # We must be in Blender => bpy types will exist => we can import .blender.addon safely.
        # noinspection PyUnresolvedReferences
        from .blender.addon import *
