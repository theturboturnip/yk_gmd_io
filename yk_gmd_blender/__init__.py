import importlib.util
blender_loader = importlib.util.find_spec('bpy')

# Include the bl_info at the top level always
bl_info = {
    "name": "Yakuza GMD File Import/Export",
    "author": "Samuel Stark (TheTurboTurnip)",
    "version": (0, 1, 3),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Yakuza GMD Files (tested with Kenzan, Y3, Y4, Y5, Y0, YK1)",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

if blender_loader:
    from .blender.addon import *
