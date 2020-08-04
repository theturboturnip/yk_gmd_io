from typing import List

import bpy
from bpy.props import FloatVectorProperty, StringProperty
from bpy.types import NodeSocketStandard, NodeSocket, Context, UILayout, Node


class Matrix4x4NodeSocket(NodeSocket):
    bl_idname = "Matrix4x4NodeSocket"
    bl_label = "Socket for holding 4x4 matrix values"

    socket_col = FloatVectorProperty(size=4, default=[1, 1, 1, 1])

    prop_row0 = FloatVectorProperty(size=4, default=[0, 0, 0, 0])
    prop_row1 = FloatVectorProperty(size=4, default=[0, 0, 0, 0])
    prop_row2 = FloatVectorProperty(size=4, default=[0, 0, 0, 0])
    prop_row3 = FloatVectorProperty(size=4, default=[0, 0, 0, 0])

    # Derived from https://github.com/zeffii/SoundPetal/blob/9fde0c64d5a4d3b30f0d4a75e73d29c0757463f8/node_tree.py#L94
    # I'm pretty sure this is boilerplate though?
    def draw(self, context: 'Context', layout: 'UILayout', node: 'Node',
             text: str):
        if self.is_output and text:
            row = layout.row()
            row.prop(node, text)
        else:
            if self.is_linked:
                layout.label(text)
                return

            # We are not linked, so just display the vector rows
            # layout.row().grid_flow creates a new line, and creates a grid_flow that will organize the rest of the rows nicely
            box = layout.grid_flow(row_major=True, columns=1, even_columns=True, even_rows=True)
            box.row().label(text=text)
            # Each row in the grid_flow is then a row in the matrix
            box.row().prop(self, 'prop_row0', text="")#, text="Row0")
            box.row().prop(self, 'prop_row1', text="")#, text="Row1")
            box.row().prop(self, 'prop_row2', text="")#, text="Row2")
            box.row().prop(self, 'prop_row3', text="")#, text="Row3")

            # Unsure what this is?
            #layout.prop(node, text)

    def draw_color(self, context: 'Context', node: 'Node') -> List[float]:
        return self.socket_col

# Inspired by XNALara importer code - https://github.com/johnzero7/XNALaraMesh/blob/eaccfddf39aef8d3cb60a50c05f2585398fe26ca/material_creator.py#L527

YAKUZA_SHADER_NODE_GROUP = "Yakuza Shader"


DEFAULT_DIFFUSE_COLOR = (0.9, 0.9, 0.9, 1)
DEFAULT_UNUSED_COLOR = (0, 0, 0, 1)
# TODO: Some normal maps use the G/A channels for normals instead of the R/B. Figure out how to handle that
DEFAULT_NORMAL_COLOR = (0.5, 0.5, 0, 1)
DEFAULT_MULTI_COLOR = (0, 0, 0, 1)

def get_yakuza_shader_node_group():
    if YAKUZA_SHADER_NODE_GROUP in bpy.data.node_groups:
        return bpy.data.node_groups[YAKUZA_SHADER_NODE_GROUP]
    shader = bpy.data.node_groups.new(name=YAKUZA_SHADER_NODE_GROUP, type="ShaderNodeTree")
    shader.nodes.clear()

    link = shader.links.new

    # shader: GMDShader
    #
    # texture_diffuse: Optional[str]
    # texture_refl: Optional[str]
    # texture_multi: Optional[str]
    # texture_unk1: Optional[str]
    # texture_rs: Optional[str]
    # texture_normal: Optional[str]
    # texture_rt: Optional[str]
    # texture_rd: Optional[str]
    #
    # material: GMDMaterial
    # unk12: Optional[GMDUnk12]
    # unk14: Optional[GMDUnk14]
    # attr_extra_properties: List[float]
    # attr_flags: int

    # The "Group Input" and "Group Output" nodes are how we link values from shader.inputs, shader.outputs into the other nodes in the shader?
    group_input = shader.nodes.new("NodeGroupInput")
    group_output = shader.nodes.new("NodeGroupOutput")

    # Create Inputs
    shader_name = shader.inputs.new("NodeSocketString", "Shader Name")
    shader_name.default_value = "Invalid Shader"

    shader_is_skin = shader.inputs.new("NodeSocketBool", "Skin Shader")
    shader_is_skin.default_value = False
    shader_is_transparent = shader.inputs.new("NodeSocketBool", "Transparent")
    shader_is_transparent.default_value = False

    shader_diffuse = shader.inputs.new("NodeSocketColor", "Diffuse Texture")
    shader_diffuse.default_value = DEFAULT_DIFFUSE_COLOR
    shader_normal = shader.inputs.new("NodeSocketColor", "Normal Texture")
    shader_normal.default_value = DEFAULT_NORMAL_COLOR
    shader_multi = shader.inputs.new("NodeSocketColor", "Multi Texture")
    shader_multi.default_value = DEFAULT_MULTI_COLOR

    shader_refl = shader.inputs.new("NodeSocketColor", "texture_refl")
    shader_refl.default_value = DEFAULT_UNUSED_COLOR
    shader_unk1 = shader.inputs.new("NodeSocketColor", "texture_unk1")
    shader_unk1.default_value = DEFAULT_UNUSED_COLOR
    shader_rs = shader.inputs.new("NodeSocketColor", "texture_rs")
    shader_rs.default_value = DEFAULT_UNUSED_COLOR
    shader_rt = shader.inputs.new("NodeSocketColor", "texture_rt")
    shader_rt.default_value = DEFAULT_UNUSED_COLOR
    shader_rd = shader.inputs.new("NodeSocketColor", "texture_rd")
    shader_rd.default_value = DEFAULT_UNUSED_COLOR

    shader_flags = shader.inputs.new("NodeSocketIntUnsigned", "Attribute Set Flags")
    shader_flags.default_value = 0
    shader_extra_properties = shader.inputs.new(Matrix4x4NodeSocket.bl_idname, "Attribute Set Floats")
    shader_material_floats = shader.inputs.new(Matrix4x4NodeSocket.bl_idname, "Material Floats")
    shader_unk12 = shader.inputs.new(Matrix4x4NodeSocket.bl_idname, "Unk12 Ints")
    shader_unk14 = shader.inputs.new(Matrix4x4NodeSocket.bl_idname, "Unk14 Floats")

    # Create outputs
    shader.outputs.new("NodeSocketShader", 'Shader')

    principled_shader = shader.nodes.new("ShaderNodeBsdfPrincipled")
    # TODO - why does group_output.inputs[0] work but not .inputs["Shader"]?
    link(principled_shader.outputs['BSDF'], group_output.inputs["Shader"])

    # TODO: Multi textures, normals, is_transparent, is_skin
    link(group_input.outputs['Diffuse Texture'], principled_shader.inputs['Base Color'])

    return shader