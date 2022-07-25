import json
import os
import re
from typing import Optional, Tuple, cast

import bpy
from yk_gmd_blender.blender.common import AttribSetLayerNames
from yk_gmd_blender.blender.error_reporter import BlenderErrorReporter
from bpy.props import FloatVectorProperty, StringProperty, BoolProperty, IntProperty
from bpy.types import NodeSocket, NodeSocketColor, ShaderNodeTexImage, \
    PropertyGroup
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBufferLayout, VecStorage
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import StrictErrorReporter

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet


class YakuzaPropertyGroup(PropertyGroup):
    """
    PropertyGroup holding all of the Yakuza data for an attribute set that can't be easily changed by the user
    or stored in the Yakuza Shader node.

    This includes a lot of data arrays, like unk12 or unk14, and also includes various flags that we can't work out
    ourselves right now.
    """

    # Has this PropertyGroup been initialized from a GMD file?
    # Used to hide data for normal Blender materials
    inited: BoolProperty(name="Initialized", default=False)

    shader_name: StringProperty(name="Shader Name")
    # These flags are stored as a hex-string encoding a 64-bit unsigned number.
    # It can't be stored as an int because blender uses primitive C types for that, and would try to store it in 32 bits.
    shader_vertex_layout_flags: StringProperty(name="Vertex Layout Flags")
    assume_skinned: BoolProperty(name="Assumes Skinned Context",
                                 description="Was imported from a skinned mesh and requires bone-weight pairs")
    cached_expected_uv_layers: StringProperty(name="Uses UV Layers", set=None)
    cached_expected_color_layers: StringProperty(name="Uses Vertex Color Layers", set=None)

    attribute_set_flags: StringProperty(name="Attribute Layout Flags")

    unk12: FloatVectorProperty(name="GMD Unk12 Data", size=32)
    unk14: FloatVectorProperty(name="GMD Unk14 Data", size=32)
    attribute_set_floats: FloatVectorProperty(name="GMD Attribute Set Floats", size=16)
    #material_floats: FloatVectorProperty(name="GMD Material Floats", size=16)
    material_origin_type: IntProperty(name="GMDMaterial origin type")
    material_json: StringProperty(name="GMDMaterial data JSON")


class YakuzaPropertyPanel(bpy.types.Panel):
    """
    Panel that displays the YakuzaPropertyGroup attached to the selected material.
    """

    bl_label = "Yakuza Properties"

    bl_order = 1 # Make it appear near the top

    bl_space_type = "PROPERTIES"
    bl_context = "material"
    bl_region_type = "WINDOW"

    def draw(self, context):
        ob = context.object
        if not ob:
            return
        ma = ob.active_material
        if not ma:
            return

        def matrix_prop(prop_name, length: int, text=""):
            self.layout.label(text=text)
            box = self.layout.box().grid_flow(row_major=True, columns=4, even_rows=True, even_columns=True)
            for i in range(length//4):
                for j in range(i*4, (i+1)*4):
                    box.prop(ma.yakuza_data, prop_name, index=j, text="")

        if ma.yakuza_data.inited:
            self.layout.prop(ma.yakuza_data, "shader_name")

            vertex_layout_box = self.layout.box()
            vertex_layout_box.prop(ma.yakuza_data, "shader_vertex_layout_flags")
            vertex_layout_box.prop(ma.yakuza_data, "assume_skinned")
            vertex_layout_box.prop(ma.yakuza_data, "cached_expected_uv_layers")
            vertex_layout_box.prop(ma.yakuza_data, "cached_expected_color_layers")
            vertex_layout_box.operator("material.yakuza_update_expected_layers")

            self.layout.prop(ma.yakuza_data, "attribute_set_flags")

            self.layout.prop(ma.yakuza_data, "material_origin_type")
            self.layout.prop(ma.yakuza_data, "material_json")
            matrix_prop("attribute_set_floats", 16, text="Attribute Set Floats")
            #matrix_prop("material_floats", 16, text="Material Floats")
            matrix_prop("unk12", 32, text="Unk 12")
            matrix_prop("unk14", 32, text="Unk 14 (Should be ints)")
        else:
            self.layout.label(text=f"No Yakuza Data present for this material")


class MATERIAL_OT_yakuza_update_expected_layers(bpy.types.Operator):
    """Re-check the expected color and UV layers based on the vertex layout flags"""
    bl_idname = "material.yakuza_update_expected_layers"
    bl_label = "Re-check expected layers for Yakuza material"

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob is not None and ob.active_material is not None and ob.active_material.yakuza_data.inited

    def execute(self, context):
        ob = context.object
        if not ob:
            return
        ma = ob.active_material
        if not ma or not ma.yakuza_data.inited:
            return

        error = BlenderErrorReporter(self.report, StrictErrorReporter({"ALL"}))

        try:
            vertex_layout_flags = int(ma.yakuza_data.shader_vertex_layout_flags, base=16)
        except ValueError as ex:
            error.fatal_exception(ex)

        vertex_layout = GMDVertexBufferLayout.build_vertex_buffer_layout_from_flags(vertex_layout_flags,
                                                                                    ma.yakuza_data.assume_skinned,
                                                                                    error)

        layer_names = AttribSetLayerNames.build_from(vertex_layout, ma.yakuza_data.assume_skinned)

        expected_uv_layers = ", ".join(layer_names.get_blender_uv_layers())
        expected_color_layers = ", ".join(layer_names.get_blender_color_layers())

        ma.yakuza_data.cached_expected_uv_layers = expected_uv_layers
        ma.yakuza_data.cached_expected_color_layers = expected_color_layers

        return {'FINISHED'}

# Custom property group for textures imported from GMD files.
# Allows for "Yakuza relinking": updating the file associated with an image based on the texture name,
# potentially using a different file format.
class YakuzaTexturePropertyGroup(PropertyGroup):
    # Has this PropertyGroup been initialized from a GMD file?
    inited: BoolProperty(name="Initialized", default=False)

    # Name of the texture from the GMD file
    yk_name: StringProperty(name="Texture Name (from GMD)")


# Inspired by XNALara importer code - https://github.com/johnzero7/XNALaraMesh/blob/eaccfddf39aef8d3cb60a50c05f2585398fe26ca/material_creator.py#L527

YAKUZA_SHADER_NODE_GROUP = "Yakuza Shader"

DEFAULT_DIFFUSE_COLOR = (0.9, 0.9, 0.9, 1)
DEFAULT_UNUSED_COLOR = (0, 0, 0, 1)
# TODO: Some normal maps use the G/A channels for normals instead of the R/B. Figure out how to handle that
DEFAULT_NORMAL_COLOR = (0.5, 0.5, 1, 1)
DEFAULT_MULTI_COLOR = (0, 0, 1, 1)


def create_proxy_texture(name: str, filename: str, color: Tuple[float, float, float, float]) -> bpy.types.Image:
    """
    Create an Image with a given name and filename, which is of a given color.
    Returns an 128x128 image.
    :param name: The name of the new image.
    :param filename: The filepath to be associated with the new image.
    :param color: The color to fill the image with.
    :return: A 128x128 Image of the given color, with the given filepath and name.
    """

    # Create an image where the Blender name = the file name i.e. the name + extension.
    image = bpy.data.images.new(filename, 128, 128, alpha=True)

    # Set up the Yakuza Data for this texture to contain the GMD name i.e. the name without an extension.
    image.yakuza_data.inited = True
    image.yakuza_data.yk_name = name

    # Using a GENERATED image means Blender won't try to save it out to a file when you exit
    image.source = 'GENERATED'
    image.generated_type = 'BLANK'
    image.generated_color = color
    image.generated_width = 128
    image.generated_height = 128

    return image


def load_texture_from_name(node_tree: bpy.types.NodeTree, gmd_folder: str, tex_name: str, color_if_not_found=(1, 0, 1, 1)) -> ShaderNodeTexImage:
    """
    Given a GMD texture name, find or create the Blender counterpart and add a texture node to the given material tree
    using that texture.
    It will try to load the image from the gmd_folder if possible, but if it's not there then a dummy image
    will be created filled with a specific color.
    Yakuza dummy textures "dummy_{black,white,multi,nmap}" will be created with the correct colors,
    and won't be searched for in the gmd_folder.
    :param node_tree: The node tree to add the texture node to.
    :param gmd_folder: The folder to search for as-yet-not-found textures.
    :param tex_name: The name of the texture.
    :param color_if_not_found: The color to fill the dummy image with, if an actual texture cannot be found.
    :return: A Texture node containing an image relevant to the name tex_name.
    """

    # Always create the image node
    image_node = node_tree.nodes.new('ShaderNodeTexImage')

    # use the texture basename i.e. "c_am_kiryu_suit_di.dds" with the dds extension always.
    # bpy.data.images.load() uses this convension, so when we look up images in bpy.data.images we have to match.
    tex_filepath_basename = f"{tex_name}.dds"
    if tex_filepath_basename in bpy.data.images:
        # The texture already exists, just use that one
        image_node.image = bpy.data.images[tex_filepath_basename]
    elif tex_name == "dummy_black":
        image_node.image = create_proxy_texture(tex_name, tex_filepath_basename, (0, 0, 0, 1))
    elif tex_name == "dummy_white":
        image_node.image = create_proxy_texture(tex_name, tex_filepath_basename, (1, 1, 1, 1))
    elif tex_name == "dummy_multi":
        image_node.image = create_proxy_texture(tex_name, tex_filepath_basename, DEFAULT_MULTI_COLOR)
    elif tex_name == "dummy_nmap":
        image_node.image = create_proxy_texture(tex_name, tex_filepath_basename, DEFAULT_NORMAL_COLOR)
    else:
        # The texture doesn't already exist, and isn't a dummy texture we can create ourselves.
        # Try to find it in the gmd_folder.
        tex_filepath = os.path.join(gmd_folder, tex_filepath_basename)
        if not os.path.isfile(tex_filepath):
            # The texture doesn't exist.
            image_node.image = create_proxy_texture(tex_name, tex_filepath_basename, color_if_not_found)
        else:
            # The texture does exist, load it!
            image = bpy.data.images.load(tex_filepath, check_existing=True)
            image.yakuza_data.inited = True
            image.yakuza_data.yk_name = tex_name
            image_node.image = image

    return cast(ShaderNodeTexImage, image_node)


def set_yakuza_shader_material_from_attributeset(material: bpy.types.Material, yakuza_inputs: bpy.types.NodeInputs,
                                                 attribute_set: GMDAttributeSet, gmd_folder: str):
    """
    Given a material and an attribute set, attach all of the relevant data from the attribute set to the material.
    :param material: The material to update
    :param yakuza_inputs: The inputs to the Yakuza Shader node in the material
    :param attribute_set: The GMDAttributeSet this Material represents.
    :param gmd_folder: The folder to examine for new textures.
    :return: None
    """

    layer_names = AttribSetLayerNames.build_from(attribute_set.shader.vertex_buffer_layout,
                                                 attribute_set.shader.assume_skinned)

    # Setup the yakuza_data inside the material
    material.yakuza_data.inited = True
    material.yakuza_data.shader_name = attribute_set.shader.name
    material.yakuza_data.shader_vertex_layout_flags = f"{attribute_set.shader.vertex_buffer_layout.packing_flags:016x}"
    material.yakuza_data.assume_skinned = attribute_set.shader.assume_skinned
    material.yakuza_data.attribute_set_flags = f"{attribute_set.attr_flags:016x}"
    material.yakuza_data.cached_expected_uv_layers = ", ".join(layer_names.get_blender_uv_layers())
    material.yakuza_data.cached_expected_color_layers = ", ".join(layer_names.get_blender_color_layers())
    material.yakuza_data.unk12 = attribute_set.unk12.float_data if attribute_set.unk12 else [0]*32
    material.yakuza_data.unk14 = attribute_set.unk14.int_data if attribute_set.unk14 else [0]*32
    material.yakuza_data.attribute_set_floats = attribute_set.attr_extra_properties
    material.yakuza_data.material_origin_type = attribute_set.material.origin_version.value
    material.yakuza_data.material_json = json.dumps(vars(attribute_set.material.origin_data))

    # Set the skin shader to 1 if the shader is a skin shader
    yakuza_inputs["Skin Shader"].default_value = 1.0 if "[skin]" in attribute_set.shader.name else 0.0

    # Convenience function for creating a texture node for an Optional texture
    def set_texture(set_into: NodeSocketColor, tex_name: Optional[str],
                    next_image_y: int = 0, color_if_not_found=(1, 0, 1, 1)) -> Tuple[Optional[ShaderNodeTexImage], int]:
        if not tex_name:
            return None, next_image_y
        image_node = load_texture_from_name(material.node_tree, gmd_folder, tex_name, color_if_not_found)
        image_node.location = (-500, next_image_y)
        #image_node.label = tex_name
        image_node.hide = True
        material.node_tree.links.new(image_node.outputs["Color"], set_into)
        next_image_y -= 100
        return image_node, next_image_y

    # Create the diffuse texture
    diffuse_tex, next_y = set_texture(yakuza_inputs["texture_diffuse"], attribute_set.texture_diffuse)
    if diffuse_tex and re.search(r'^s_b', attribute_set.shader.name):
        # The shader name starts with s_b so we know it's transparent
        # Link the texture alpha with the Yakuza Shader, and make the material do alpha blending.
        material.node_tree.links.new(diffuse_tex.outputs["Alpha"], yakuza_inputs["Diffuse Alpha"])
        material.blend_method = "BLEND"
    # Attach the other textures.
    _, next_y = set_texture(yakuza_inputs["texture_multi"], attribute_set.texture_multi, next_y, DEFAULT_MULTI_COLOR)
    _, next_y = set_texture(yakuza_inputs["texture_normal"], attribute_set.texture_normal, next_y, DEFAULT_NORMAL_COLOR)
    _, next_y = set_texture(yakuza_inputs["texture_refl"], attribute_set.texture_refl, next_y)
    _, next_y = set_texture(yakuza_inputs["texture_unk1"], attribute_set.texture_unk1, next_y)
    _, next_y = set_texture(yakuza_inputs["texture_rs"], attribute_set.texture_rs, next_y)
    _, next_y = set_texture(yakuza_inputs["texture_rt"], attribute_set.texture_rt, next_y)
    _, next_y = set_texture(yakuza_inputs["texture_rd"], attribute_set.texture_rd, next_y)


def get_yakuza_shader_node_group():
    """
    Create or retrieve the Yakuza Shader node group, depending on whether it exists.
    :return: The Yakuza Shader node group.
    """

    # If it already exists, return it.
    if YAKUZA_SHADER_NODE_GROUP in bpy.data.node_groups:
        return bpy.data.node_groups[YAKUZA_SHADER_NODE_GROUP]

    # Create the node group
    shader = bpy.data.node_groups.new(name=YAKUZA_SHADER_NODE_GROUP, type="ShaderNodeTree")
    shader.nodes.clear()

    # Convenience function to avoid typing out shader.links.new all the time
    link = shader.links.new

    # Use FloatFactor for a [0, 1] range float
    # can't use boolean here because it doesn't work with the "subsurface scattering" float input on the shader.
    shader_is_skin = shader.inputs.new("NodeSocketFloatFactor", "Skin Shader")
    shader_is_skin.min_value = 0
    shader_is_skin.max_value = 1.0
    shader_is_skin.default_value = 0

    # Define the texture inputs that are actually used
    shader_diffuse = shader.inputs.new("NodeSocketColor", "texture_diffuse")
    shader_diffuse.default_value = DEFAULT_DIFFUSE_COLOR
    shader_alpha = shader.inputs.new("NodeSocketFloat", "Diffuse Alpha")
    shader_alpha.default_value = 1.0
    shader_multi = shader.inputs.new("NodeSocketColor", "texture_multi")
    shader_multi.default_value = DEFAULT_MULTI_COLOR
    # Define the texture inputs that aren't used
    shader_normal = shader.inputs.new("NodeSocketColor", "texture_normal")
    shader_normal.default_value = DEFAULT_NORMAL_COLOR
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

    # Create outputs
    shader.outputs.new("NodeSocketShader", 'Shader')

    # The "Group Output" nodes is how we link values from shader.outputs into the other nodes in the shader
    group_output = shader.nodes.new("NodeGroupOutput")

    # Create the shader node and link it to the output.
    principled_shader = shader.nodes.new("ShaderNodeBsdfPrincipled")
    principled_shader.location = (100, 0)
    group_output.location = (principled_shader.location[0] + principled_shader.width + 100, 0)
    group_input_x = -800
    link(principled_shader.outputs['BSDF'], group_output.inputs["Shader"])

    # Create multiple "Group Input" nodes containing only the bits we want
    group_input_diffuse = shader.nodes.new("NodeGroupInput")
    for output in group_input_diffuse.outputs:
        output.hide = (output.name != "texture_diffuse")
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
        output.hide = (output.name != "texture_multi")
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

    # Helper function for creating a MixRGB node between the given colors by the given factor.
    def mix_between(fac: NodeSocket, color1, color2):
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

    # Apply the multi texture
    # Split the color into R, G, B
    split_multi = shader.nodes.new("ShaderNodeSeparateRGB")
    split_multi.location = (-600, group_input_multi.location[1])
    link(group_input_multi.outputs["texture_multi"], split_multi.inputs[0])
    # The R is shininess
    link(split_multi.outputs['R'], principled_shader.inputs['Specular'])
    # The B is Ambient Occlusion, so it darkens the diffuse color to create a "main color"
    # TODO - this isn't consistent for Y3/4/5 models
    # main_color = mix_between(split_multi.outputs['B'], group_input_diffuse.outputs['texture_diffuse'], (0, 0, 0, 1))
    # main_color.label = "Main Color"
    # main_color.hide = True
    # main_color.location = (-400, 0)
    # The G is emission, so use it to mix between diffuse and emission
    main_color_diffuse_portion = mix_between(split_multi.outputs['G'], group_input_diffuse.outputs['texture_diffuse'], (0, 0, 0, 1))
    main_color_diffuse_portion.label = "Diffuse Portion"
    main_color_diffuse_portion.hide = True
    main_color_diffuse_portion.location = (-200, 0)
    main_color_emissive_portion = mix_between(split_multi.outputs['G'], (0, 0, 0, 1), group_input_diffuse.outputs['texture_diffuse'])
    main_color_emissive_portion.label = "Emissive Portion"
    main_color_emissive_portion.hide = True
    main_color_emissive_portion.location = (-200, -50)
    # Link the diffuse/emissive portions correctly
    link(main_color_diffuse_portion.outputs[0], principled_shader.inputs['Base Color'])
    link(main_color_emissive_portion.outputs[0], principled_shader.inputs['Emission'])

    # TODO: normal maps? They are very complicated so probably not right now

    # If the material supports transparency, Diffuse Alpha will be set to a non-zero value
    link(group_input_alpha.outputs["Diffuse Alpha"], principled_shader.inputs["Alpha"])

    # Skin
    # Skin Shader = 1 if the shader is skin else 0. Attach this to the Subsurface control.
    link(group_input_is_skin.outputs['Skin Shader'], principled_shader.inputs['Subsurface'])
    # Use the base diffuse texture without any AO for the subsurface color. This may be wrong, but it looks OK.
    link(group_input_diffuse.outputs['texture_diffuse'], principled_shader.inputs['Subsurface Color'])

    return shader
