from enum import IntEnum
from typing import Tuple, List, Dict

import bpy
from bpy.props import BoolProperty, FloatVectorProperty, StringProperty
from bpy.types import PropertyGroup, Panel


class GMDGame(IntEnum):
    """
    List of games using each engine in release order.
    Can be used to handle engine or game-specific quirks.
    (theoretically) bitmask-capable, so you can test a game against an engine and see if it matches.
    """
    Engine_MagicalV = 0x10
    Kenzan = 0x11
    Yakuza3 = 0x12
    Yakuza4 = 0x13
    DeadSouls = 0x14
    BinaryDomain = 0x15

    Engine_Kiwami = 0x20
    Yakuza5 = 0x21
    Yakuza0 = 0x22
    YakuzaKiwami1 = 0x23
    FOTNS = 0x24

    Engine_Dragon = 0x40
    Yakuza6 = 0x41
    YakuzaKiwami2 = 0x42
    Judgment = 0x43
    Yakuza7 = 0x44

    @staticmethod
    def blender_props() -> List[Tuple[str, str, str]]:
        return [
            ("ENGINE_MAGICALV", "Old Engine", "Magical-V Engine (Kenzan - Binary Domain)"),
            ("KENZAN", "Yakuza Kenzan", "Yakuza Kenzan"),
            ("YAKUZA3", "Yakuza 3", "Yakuza 3"),
            ("YAKUZA4", "Yakuza 4", "Yakuza 4"),
            ("DEADSOULS", "Yakuza Dead Souls", "Yakuza Dead Souls"),
            ("BINARYDOMAIN", "Binary Domain", "Binary Domain"),

            ("ENGINE_KIWAMI", "Kiwami Engine", "Kiwami Engine (Yakuza 5 - Yakuza Kiwami 1)"),
            ("YAKUZA5", "Yakuza 5", "Yakuza 5"),
            ("YAKUZA0", "Yakuza 0", "Yakuza 0"),
            ("YAKUZAK1", "Yakuza K1", "Yakuza Kiwami 1"),
            ("FOTNS", "FOTNS: LP", "Fist of the North Star: Lost Paradise"),

            ("ENGINE_DRAGON", "Dragon Engine", "Dragon Engine (Yakuza 6 onwards)"),
            ("YAKUZA6", "Yakuza 6", "Yakuza 6"),
            ("YAKUZAK2", "Yakuza K2", "Yakuza K2"),
            ("JUDGMENT", "Judgment", "Judgment"),
            ("YAKUZA7", "Yakuza 7", "Yakuza 7"),
        ]

    @staticmethod
    def mapping_from_blender_props() -> Dict[str, 'GMDGame']:
        return {
            "ENGINE_MAGICALV": GMDGame.Engine_MagicalV,
            "KENZAN": GMDGame.Kenzan,
            "YAKUZA3": GMDGame.Yakuza3,
            "YAKUZA4": GMDGame.Yakuza4,
            "DEADSOULS": GMDGame.DeadSouls,
            "BINARYDOMAIN": GMDGame.BinaryDomain,

            "ENGINE_KIWAMI": GMDGame.Engine_Kiwami,
            "YAKUZA5": GMDGame.Yakuza5,
            "YAKUZA0": GMDGame.Yakuza0,
            "YAKUZAK1": GMDGame.YakuzaKiwami1,
            "FOTNS": GMDGame.FOTNS,

            "ENGINE_DRAGON": GMDGame.Engine_Dragon,
            "YAKUZA6": GMDGame.Yakuza6,
            "YAKUZAK2": GMDGame.YakuzaKiwami2,
            "JUDGMENT": GMDGame.Judgment,
            "YAKUZA7": GMDGame.Yakuza7,
        }


class YakuzaHierarchyNodeData(PropertyGroup):
    # Has this PropertyGroup been initialized from a GMD file?
    # Used to hide data for normal Blender materials
    inited: BoolProperty(name="Initialized", default=False)
    # The original imported node matrix
    imported_matrix: FloatVectorProperty(name="Imported Node Matrix", default=[0.0]*16,size=16, subtype="MATRIX")

    # The animation axis for the node imported from the GMD
    anim_axis: FloatVectorProperty(name="Animation Axis (Quaternion)", default=[0.0]*4, size=4, subtype="QUATERNION")
    # Node flags - currently unknown. Stored as JSON because IntVectorProperty doesn't support unsigned 32-bit integers
    flags_json: StringProperty(name="Imported Node Flags (JSON)",default="[0,0,0,0]")


class OBJECT_PT_yakuza_hierarchy_node_data_panel(Panel):
    bl_label = "Yakuza Hierarchy-Node Data"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        ob = context.object

        if not ob:
            return

        layout.prop(ob.yakuza_hierarchy_node_data, "anim_axis")
        layout.prop(ob.yakuza_hierarchy_node_data, "flags_json")

        if ob.yakuza_hierarchy_node_data.inited:
            def matrix_prop(dat, prop_name, length: int, text=""):
                layout.label(text=text)
                box = layout.box().grid_flow(row_major=True, columns=4, even_rows=True, even_columns=True)
                for i in range(length//4):
                    for j in range(i*4, (i+1)*4):
                        box.prop(dat, prop_name, index=j, text="")

            matrix_prop(ob.yakuza_hierarchy_node_data, "imported_matrix", 16)
        else:
            layout.label(text=f"No original matrix, this object wasn't imported from a GMD")


class BONE_PT_yakuza_hierarchy_node_data_panel(Panel):
    bl_label = "Yakuza Hierarchy-Node Data (Bone)"

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'bone'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        bone = context.bone
        if not bone:
            bone = context.edit_bone

        if not bone:
            return

        layout.prop(bone.yakuza_hierarchy_node_data, "anim_axis")
        layout.prop(bone.yakuza_hierarchy_node_data, "flags_json")

        if bone.yakuza_hierarchy_node_data.inited:
            def matrix_prop(dat, prop_name, length: int, text=""):
                layout.label(text=text)
                box = layout.box().grid_flow(row_major=True, columns=4, even_rows=True, even_columns=True)
                for i in range(length//4):
                    for j in range(i*4, (i+1)*4):
                        box.prop(dat, prop_name, index=j, text="")

            matrix_prop(bone.yakuza_hierarchy_node_data, "imported_matrix", 16)
        else:
            layout.label(text=f"No original matrix, this bone wasn't imported from a GMD")
