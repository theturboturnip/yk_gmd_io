# This file was based on https://github.com/KhronosGroup/glTF-Blender-IO/blob/master/addons/io_scene_gltf2/__init__.py

import bpy
from bpy.props import PointerProperty

from .importer.image_relink import YakuzaImageRelink, menu_func_yk_image_relink
from .materials import YakuzaPropertyGroup, YakuzaPropertyPanel, YakuzaTexturePropertyGroup, \
    MATERIAL_OT_yakuza_update_expected_layers
from .common import YakuzaHierarchyNodeData, OBJECT_PT_yakuza_hierarchy_node_data_panel, \
    BONE_PT_yakuza_hierarchy_node_data_panel, YakuzaFileRootData, OBJECT_PT_yakuza_file_root_data_panel
from .exporter.gmd_exporter import ExportSkinnedGMD, menu_func_export_skinned, menu_func_export_unskinned, \
    ExportUnskinnedGMD
from .importer.gmd_importers import ImportSkinnedGMD, menu_func_import_skinned, menu_func_import_unskinned, \
    ImportUnskinnedGMD, menu_func_import_animation_unskinned, menu_func_import_animation_skinned, \
    ImportAnimationSkinnedGMD, ImportAnimationUnskinnedGMD

classes = (
    ImportSkinnedGMD,
    ImportUnskinnedGMD,
    ImportAnimationSkinnedGMD,
    ImportAnimationUnskinnedGMD,
    ExportSkinnedGMD,
    ExportUnskinnedGMD,
    YakuzaImageRelink,
    YakuzaPropertyGroup,
    YakuzaPropertyPanel,
    YakuzaTexturePropertyGroup,
    YakuzaHierarchyNodeData,
    OBJECT_PT_yakuza_hierarchy_node_data_panel,
    BONE_PT_yakuza_hierarchy_node_data_panel,
    YakuzaFileRootData,
    OBJECT_PT_yakuza_file_root_data_panel,
    MATERIAL_OT_yakuza_update_expected_layers,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)

    # add to the export / import menu
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_skinned)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_unskinned)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_skinned)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_unskinned)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_animation_skinned)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_animation_unskinned)
    bpy.types.TOPBAR_MT_file_external_data.append(menu_func_yk_image_relink)

    bpy.types.Material.yakuza_data = PointerProperty(type=YakuzaPropertyGroup)
    bpy.types.Image.yakuza_data = PointerProperty(type=YakuzaTexturePropertyGroup)
    bpy.types.Object.yakuza_hierarchy_node_data = PointerProperty(type=YakuzaHierarchyNodeData)
    bpy.types.Object.yakuza_file_root_data = PointerProperty(type=YakuzaFileRootData)
    bpy.types.Bone.yakuza_hierarchy_node_data = PointerProperty(type=YakuzaHierarchyNodeData)


def unregister():
    del bpy.types.Bone.yakuza_hierarchy_node_data
    del bpy.types.Object.yakuza_file_root_data
    del bpy.types.Object.yakuza_hierarchy_node_data
    del bpy.types.Image.yakuza_data
    del bpy.types.Material.yakuza_data

    for c in classes:
        bpy.utils.unregister_class(c)

    # remove from the export / import menu
    bpy.types.TOPBAR_MT_file_external_data.remove(menu_func_yk_image_relink)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_unskinned)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_skinned)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_animation_unskinned)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_animation_skinned)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_unskinned)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_skinned)
