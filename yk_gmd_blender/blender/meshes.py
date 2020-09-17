import bpy
from bpy.props import FloatVectorProperty, StringProperty, BoolProperty, IntProperty
from bpy.types import NodeSocket, NodeSocketColor, ShaderNodeTexImage, \
    PropertyGroup

class YakuzaMeshPropertyGroup(PropertyGroup):
    """
    PropertyGroup holding all of the Yakuza data for an attribute set that can't be easily changed by the user
    or stored in the Yakuza Shader node.

    This includes a lot of data arrays, like unk12 or unk14, and also includes various flags that we can't work out
    ourselves right now.
    """

    # Has this PropertyGroup been initialized from a GMD file?
    # Used to hide data for normal Blender materials
    inited: BoolProperty(name="Initialized", default=False)

    origin_version: IntProperty(name="Imported from version")
    flag_str: StringProperty(name="Mesh flags", default="")


class YakuzaMeshPropertyPanel(bpy.types.Panel):
    """
    Panel that displays the YakuzaMeshPropertyGroup attached to the selected mesh.
    """

    bl_label = "Yakuza Properties"

    bl_order = 1 # Make it appear near the top

    bl_space_type = "PROPERTIES"
    bl_context = "data"
    bl_region_type = "WINDOW"

    def draw(self, context):
        ob = context.object
        mesh = ob.data

        if not mesh or not isinstance(mesh, bpy.types.Mesh):
            return

        if mesh.yakuza_data.inited:
            self.layout.prop(mesh.yakuza_data, "origin_version")
            self.layout.prop(mesh.yakuza_data, "flag_str")
        else:
            self.layout.label(text=f"No Yakuza Data present for this mesh")