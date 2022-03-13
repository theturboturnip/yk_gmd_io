# Include the bl_info at the top level always
bl_info = {
    "name": "Yakuza GMD File Import/Export",
    "author": "Samuel Stark (TheTurboTurnip)",
    "version": (0, 3, 2, 1),
    "blender": (2, 92, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Yakuza GMD Files",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

# Check if we're in Blender by seeing if bpy.app.version exists.
# We can't just check for the presence of bpy, because the type library
import bpy.app
if getattr(bpy.app, "version", None) is not None:
    # If we're in Blender, add the rest of the addon
    from .blender.addon import *