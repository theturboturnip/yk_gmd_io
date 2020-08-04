import os
import re
from typing import List, Optional, Tuple, cast

import bpy
from bpy.props import FloatVectorProperty, StringProperty, BoolProperty
from bpy.types import NodeSocketStandard, NodeSocket, Context, UILayout, Node, NodeSocketColor, ShaderNodeTexImage, \
    PropertyGroup
from mathutils import Matrix, Vector

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet


# def get_row(self: 'Matrix4x4NodeSocket', idx):
#     return list(self.default_value.row[idx])
# def set_row(self: 'Matrix4x4NodeSocket', idx, value):
#     self.default_value.row[idx] = Vector(value)

# class MatrixPropertyGroup(PropertyGroup):
#     prop_row0: FloatVectorProperty(name="row0", size=4)#, get=lambda self: get_row(self, 0), set=lambda self, value: set_row(self, 0, value))
#     prop_row1: FloatVectorProperty(name="row1", size=4)#, get=lambda self: get_row(self, 1), set=lambda self, value: set_row(self, 1, value))
#     prop_row2: FloatVectorProperty(name="row2", size=4)#, get=lambda self: get_row(self, 2), set=lambda self, value: set_row(self, 2, value))
#     prop_row3: FloatVectorProperty(name="row3", size=4)#, get=lambda self: get_row(self, 3), set=lambda self, value: set_row(self, 3, value))
#
#     def __init__(self, data: Optional[List[float]] = None):
#         if not data:
#             data = [0] * 16
#         self.set_from_data(data)
#
#     def set_from_data(self, data: List[float]):
#         self.prop_row0 = data[0:4]
#         self.prop_row1 = data[4:8]
#         self.prop_row2 = data[8:12]
#         self.prop_row3 = data[12:16]

# class Matrix4x4NodeSocket(NodeSocket):
#     bl_idname = "Matrix4x4NodeSocket"
#     bl_label = "Socket for holding 4x4 matrix values"
#
#     default_value = bpy.props.PointerProperty(type=MatrixPropertyGroup) #: Matrix = Matrix.Diagonal(Vector((0, 0, 0, 0)))
#
#
#     # Derived from https://github.com/zeffii/SoundPetal/blob/9fde0c64d5a4d3b30f0d4a75e73d29c0757463f8/node_tree.py#L94
#     # I'm pretty sure this is boilerplate though?
#     def draw(self, context: 'Context', layout: 'UILayout', node: 'Node',
#              text: str):
#         if self.is_output and text:
#             row = layout.row()
#             row.prop(node, text)
#         else:
#             if self.is_linked:
#                 layout.label(text)
#                 return
#
#             # We are not linked, so just display the vector rows
#             # layout.row().grid_flow creates a new line, and creates a grid_flow that will organize the rest of the rows nicely
#             box = layout.grid_flow(row_major=True, columns=1, even_columns=True, even_rows=True)
#             box.row().label(text=text)
#             # Each row in the grid_flow is then a row in the matrix
#             box.row().prop(self, 'default_value', text="")#, text="Row0")
#             # box.row().prop(self, 'default_value.prop_row1', text="")#, text="Row1")
#             # box.row().prop(self, 'default_value.prop_row2', text="")#, text="Row2")
#             # box.row().prop(self, 'default_value.prop_row3', text="")#, text="Row3")
#
#             # Unsure what this is?
#             #layout.prop(node, text)
#
#     def draw_color(self, context: 'Context', node: 'Node') -> List[float]:
#         return [1, 1, 1, 1]

class YakuzaPropertyGroup(PropertyGroup):
    inited: BoolProperty(name="Initialized", default=False)

    shader_name: StringProperty(name="Shader Name")
    # These flags are stored as a hex-string encoding a 64-bit unsigned number.
    # It can't be stored as an IntUnsigned because blender uses primitive C types for that, and would try to store it in 32 bits.
    shader_vertex_layout_flags: StringProperty(name="Vertex Layout Flags")
    attribute_set_flags: StringProperty(name="Attribute Layout Flags")

    unk12: FloatVectorProperty(name="GMD Unk12 Data", size=32)
    unk14: FloatVectorProperty(name="GMD Unk14 Data", size=32)
    attribute_set_floats: FloatVectorProperty(name="GMD Attribute Set Floats", size=16)
    material_floats: FloatVectorProperty(name="GMD Material Floats", size=16)

class YakuzaPropertyPanel(bpy.types.Panel):
    bl_label = "Yakuza Properties"

    bl_order = 1 # Make it appear near the top

    bl_space_type = "PROPERTIES"
    bl_context = "material"
    bl_region_type = "WINDOW"

    def draw(self, context):
        ob = context.object
        ma = ob.active_material

        def matrix_box(prop_name, length: int):
            # TODO: Better label
            self.layout.label(text=prop_name)
            box = self.layout.box().grid_flow(row_major=True, columns=4, even_rows=True, even_columns=True)
            for i in range(length//4):
                for j in range(i*4, (i+1)*4):
                    box.prop(ma.yakuza_data, prop_name, index=j, text="")

        if ma.yakuza_data.inited:
            self.layout.prop(ma.yakuza_data, "shader_name")
            self.layout.prop(ma.yakuza_data, "shader_vertex_layout_flags")
            self.layout.prop(ma.yakuza_data, "attribute_set_flags")


            matrix_box("unk12", 32)
            matrix_box("unk14", 32)
            matrix_box("attribute_set_floats", 16)
            matrix_box("material_floats", 16)
        else:
            self.layout.label(text=f"No Yakuza Data present for this material")


# Inspired by XNALara importer code - https://github.com/johnzero7/XNALaraMesh/blob/eaccfddf39aef8d3cb60a50c05f2585398fe26ca/material_creator.py#L527

YAKUZA_SHADER_NODE_GROUP = "Yakuza Shader"


DEFAULT_DIFFUSE_COLOR = (0.9, 0.9, 0.9, 1)
DEFAULT_UNUSED_COLOR = (0, 0, 0, 1)
# TODO: Some normal maps use the G/A channels for normals instead of the R/B. Figure out how to handle that
DEFAULT_NORMAL_COLOR = (0.5, 0.5, 0, 1)
DEFAULT_MULTI_COLOR = (0, 0, 0, 1)


def create_single_color_texture(name: str, filepath: str, color: Tuple[float, float, float, float]) -> bpy.types.Image:
    image = bpy.data.images.new(name, 128, 128, alpha=True)
    image.filepath = filepath
    image.pixels[:] = color * 128 * 128
    return image


def load_texture_from_name(node_tree: bpy.types.NodeTree, gmd_folder: str, tex_name: str, color_if_not_found=(1, 0, 1, 1)) -> ShaderNodeTexImage:
    from bpy_extras.image_utils import load_image

    image_node = node_tree.nodes.new('ShaderNodeTexImage')

    if tex_name in bpy.data.images:
        image_node.image = bpy.data.images[tex_name]
    elif tex_name in ["dummy_black", "dummy_multi"]:
        image_node.image = create_single_color_texture(tex_name, tex_name, (0, 0, 0, 1))
    elif tex_name == "dummy_white":
        image_node.image = create_single_color_texture(tex_name, tex_name, (1, 1, 1, 1))
    else:
        tex_filepath = os.path.join(gmd_folder, f"{tex_name}.dds")
        if not os.path.isfile(tex_filepath):
            # Make a purple texture to signify "not found"
            image_node.image = create_single_color_texture(tex_name, tex_filepath, color_if_not_found)
        else:
            image = bpy.data.images.load(tex_filepath, check_existing=True)
            image.name = tex_name
            image_node.image = image

    return cast(ShaderNodeTexImage, image_node)
    # load_image(f"{diffuse_name}.dds", os.path.dirname(self.filepath),
    #                                                  place_holder=True, check_existing=True)

def set_yakuza_shader_material_from_attributeset(material: bpy.types.Material, yakuza_inputs: bpy.types.NodeInputs, attribute_set: GMDAttributeSet, gmd_folder: str):
    material.yakuza_data.inited = True
    material.yakuza_data.shader_name = attribute_set.shader.name
    material.yakuza_data.shader_vertex_layout_flags = f"{attribute_set.shader.vertex_buffer_layout.packing_flags:016x}"
    material.yakuza_data.attribute_set_flags = f"{attribute_set.attr_flags:016x}"
    material.yakuza_data.unk12 = attribute_set.unk12.float_data if attribute_set.unk12 else [0]*32
    material.yakuza_data.unk14 = attribute_set.unk14.int_data if attribute_set.unk14 else [0]*32
    material.yakuza_data.attribute_set_floats = attribute_set.attr_extra_properties

    yakuza_inputs["Skin Shader"].default_value = 1.0 if "[skin]" in attribute_set.shader.name else 0.0

    # def set_matrix(set_into: Matrix4x4NodeSocket, data: List[float]):
    #     # set_into.prop_row0 = data[0:4]
    #     # set_into.prop_row1 = data[4:8]
    #     # set_into.prop_row2 = data[8:12]
    #     # set_into.prop_row3 = data[12:16]
    #     # print("Setting data ", data)
    #
    #     set_into.default_value.set_from_data(data)
    #
    # yakuza_inputs["Attribute Set Flags"].default_value = attribute_set.attr_flags
    # set_matrix(yakuza_inputs["Attribute Set Floats"], attribute_set.attr_extra_properties)
    # # TODO - Material
    # #  set_matrix(yakuza_inputs["Material Floats"], attribute_set.material.)
    # set_matrix(yakuza_inputs["Unk12 Floats"], attribute_set.unk12.float_data)
    # set_matrix(yakuza_inputs["Unk14 Ints"], attribute_set.unk14.int_data)

    def set_texture(set_into: NodeSocketColor, tex_name: Optional[str], next_image_y: int = 0, color_if_not_found=(1, 0, 1, 1)) -> Tuple[Optional[ShaderNodeTexImage], int]:
        if not tex_name:
            return None, next_image_y
        image_node = load_texture_from_name(material.node_tree, gmd_folder, tex_name, color_if_not_found)
        image_node.location = (-500, next_image_y)
        image_node.label = tex_name
        image_node.hide = True
        material.node_tree.links.new(image_node.outputs["Color"], set_into)
        next_image_y -= 100
        return image_node, next_image_y

    diffuse_tex, next_y = set_texture(yakuza_inputs["Diffuse Texture"], attribute_set.texture_diffuse)
    if diffuse_tex and re.search(r'^s_b', attribute_set.shader.name):
        # The shader name starts with s_b so we know it's transparent
        material.node_tree.links.new(diffuse_tex.outputs["Alpha"], yakuza_inputs["Diffuse Alpha"])
        material.blend_method = "BLEND"
    _, next_y = set_texture(yakuza_inputs["Normal Texture"], attribute_set.texture_normal, next_y, DEFAULT_NORMAL_COLOR)
    _, next_y = set_texture(yakuza_inputs["Multi Texture"], attribute_set.texture_multi, next_y, DEFAULT_MULTI_COLOR)
    _, next_y = set_texture(yakuza_inputs["texture_refl"], attribute_set.texture_refl, next_y)
    _, next_y = set_texture(yakuza_inputs["texture_unk1"], attribute_set.texture_unk1, next_y)
    _, next_y = set_texture(yakuza_inputs["texture_rs"], attribute_set.texture_rs, next_y)
    _, next_y = set_texture(yakuza_inputs["texture_rt"], attribute_set.texture_rt, next_y)
    _, next_y = set_texture(yakuza_inputs["texture_rd"], attribute_set.texture_rd, next_y)


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

    # Create Inputs
    # shader_name = shader.inputs.new("NodeSocketString", "Shader Name")
    # shader_name.default_value = "Invalid Shader"

    # shader_vertex_packing_flags = shader.inputs.new("NodeSocketString", "Shader Vertex Packing Flags")
    # shader_vertex_packing_flags.default_value = "0"

    # Use FloatFactor for a [0, 1] range float
    # can't use boolean here because it doesn't work with the "subsurface scattering" float
    shader_is_skin = shader.inputs.new("NodeSocketFloatFactor", "Skin Shader")
    shader_is_skin.min_value = 0
    shader_is_skin.max_value = 1.0
    shader_is_skin.default_value = 0
    # shader_is_transparent = shader.inputs.new("NodeSocketBool", "Transparent")
    # shader_is_transparent.default_value = False
    # shader_old_style_normal = shader.inputs.new("NodeSocketBool", "Old-Style Normal Maps")
    # shader_old_style_normal.default_value = False

    shader_diffuse = shader.inputs.new("NodeSocketColor", "Diffuse Texture")
    shader_diffuse.default_value = DEFAULT_DIFFUSE_COLOR
    shader_alpha = shader.inputs.new("NodeSocketFloat", "Diffuse Alpha")
    shader_alpha.default_value = 1.0
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

    # shader_flags = shader.inputs.new("NodeSocketIntUnsigned", "Attribute Set Flags")
    # shader_flags.default_value = 0
    # shader_extra_properties = shader.inputs.new(Matrix4x4NodeSocket.bl_idname, "Attribute Set Floats")
    # shader_material_floats = shader.inputs.new(Matrix4x4NodeSocket.bl_idname, "Material Floats")
    # shader_unk12 = shader.inputs.new(Matrix4x4NodeSocket.bl_idname, "Unk12 Floats")
    # shader_unk14 = shader.inputs.new(Matrix4x4NodeSocket.bl_idname, "Unk14 Ints")

    # Create outputs
    shader.outputs.new("NodeSocketShader", 'Shader')

    # The "Group Output" nodes is how we link values from shader.outputs into the other nodes in the shader
    group_output = shader.nodes.new("NodeGroupOutput")

    principled_shader = shader.nodes.new("ShaderNodeBsdfPrincipled")
    link(principled_shader.outputs['BSDF'], group_output.inputs["Shader"])

    principled_shader.location = (100, 0)
    group_output.location = (principled_shader.location[0] + principled_shader.width + 100, 0)
    group_input_x = -800

    # Create multiple "Group Input" nodes containing only the bits we want
    group_input_diffuse = shader.nodes.new("NodeGroupInput")
    for output in group_input_diffuse.outputs:
        output.hide = (output.name != "Diffuse Texture")
    group_input_diffuse.label = "Diffuse Input"
    group_input_diffuse.hide = True
    group_input_diffuse.location = (group_input_x, 0)

    group_input_is_skin = shader.nodes.new("NodeGroupInput")
    for output in group_input_is_skin.outputs:
        output.hide = (output.name != "Skin Shader")
    group_input_is_skin.label = "Is-Skin Input"
    group_input_is_skin.hide = True
    group_input_is_skin.location = (group_input_x, -100)

    group_input_multi = shader.nodes.new("NodeGroupInput")
    for output in group_input_multi.outputs:
        output.hide = (output.name != "Multi Texture")
    group_input_multi.label = "Multi Input"
    group_input_multi.hide = True
    group_input_multi.location = (group_input_x, -400)

    group_input_alpha = shader.nodes.new("NodeGroupInput")
    for output in group_input_alpha.outputs:
        output.hide = (output.name != "Diffuse Alpha")
    group_input_alpha.label = "Alpha Input"
    group_input_alpha.hide = True
    group_input_alpha.location = (group_input_x, -600)

    # group_input_normal = shader.nodes.new("NodeGroupInput")
    # for output in group_input_normal.outputs:
    #     output.hide = ("Normal" not in output.name)
    # group_input_normal.label = "Normal Input"
    # group_input_normal.hide = True
    # group_input_normal.location = (group_input_x, -800)


    def mix_between(fac, color1, color2):
        mix_node = shader.nodes.new("ShaderNodeMixRGB")

        link(fac, mix_node.inputs['Fac'])

        if isinstance(color1, NodeSocket):
            link(color1, mix_node.inputs['Color1'])
        else:
            mix_node.inputs['Color1'].default_value = color1

        if isinstance(color2, NodeSocket):
            link(color2, mix_node.inputs['Color2'])
        else:
            mix_node.inputs['Color2'].default_value = color2

        return mix_node

    # Multi texture
    # 1. Split the color into R, G, B
    split_multi = shader.nodes.new("ShaderNodeSeparateRGB")
    split_multi.location = (-600, group_input_multi.location[1])
    link(group_input_multi.outputs["Multi Texture"], split_multi.inputs[0])
    # The R is specular
    link(split_multi.outputs['R'], principled_shader.inputs['Specular'])
    # The B is Ambient Occlusion, so it darkens the diffuse color
    main_color = mix_between(split_multi.outputs['B'], group_input_diffuse.outputs['Diffuse Texture'], (0, 0, 0, 1))
    main_color.label = "Main Color"
    main_color.hide = True
    main_color.location = (-400, 0)
    # The G is emission, so use it to mix between diffuse and emission
    main_color_diffuse_portion = mix_between(split_multi.outputs['G'], main_color.outputs[0], (0, 0, 0, 1))
    main_color_diffuse_portion.label = "Diffuse Portion"
    main_color_diffuse_portion.hide = True
    main_color_diffuse_portion.location = (-200, 0)
    main_color_emissive_portion = mix_between(split_multi.outputs['G'], (0, 0, 0, 1), main_color.outputs[0])
    main_color_emissive_portion.label = "Emissive Portion"
    main_color_emissive_portion.hide = True
    main_color_emissive_portion.location = (-200, -50)
    # Link the diffuse/emissive portions correctly
    link(main_color_diffuse_portion.outputs[0], principled_shader.inputs['Base Color'])
    link(main_color_emissive_portion.outputs[0], principled_shader.inputs['Emission'])

    # TODO: normal maps? They are very complicated so probably not right now

    # is_transparent
    link(group_input_alpha.outputs["Diffuse Alpha"], principled_shader.inputs["Alpha"])

    # is_skin
    link(group_input_is_skin.outputs['Skin Shader'], principled_shader.inputs['Subsurface'])
    link(group_input_diffuse.outputs['Diffuse Texture'], principled_shader.inputs['Subsurface Color'])

    return shader