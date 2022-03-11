import importlib.util
blender_loader = importlib.util.find_spec('bpy')

# Include the bl_info at the top level always
bl_info = {
    "name": "Yakuza GMD File Import/Export",
    "author": "Samuel Stark (TheTurboTurnip)",
    "version": (0, 3, 2),
    "blender": (2, 92, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Yakuza GMD Files",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

if blender_loader:
    from .blender.addon import *