import json
import os
import re
from pathlib import Path
from typing import Optional, Tuple, cast

import bpy
from bpy.props import FloatVectorProperty, StringProperty, BoolProperty, IntProperty
from bpy.types import NodeSocket, NodeSocketColor, ShaderNodeTexImage, \
    PropertyGroup
from yk_gmd_blender.blender.common import AttribSetLayerNames
from yk_gmd_blender.blender.error_reporter import BlenderErrorReporter
from yk_gmd_blender.gmdlib.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.gmdlib.abstract.gmd_shader import GMDVertexBufferLayout
from yk_gmd_blender.gmdlib.errors.error_reporter import StrictErrorReporter, ErrorReporter


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
    # It can't be stored as an int because blender uses primitive C types and would try to store it in 32 bits.
    shader_vertex_layout_flags: StringProperty(name="Vertex Layout Flags")
    assume_skinned: BoolProperty(name="Assumes Skinned Context",
                                 description="Was imported from a skinned mesh and requires bone-weight pairs")
    cached_expected_uv_layers: StringProperty(name="Uses UV Layers", set=None)
    cached_expected_color_layers: StringProperty(name="Uses Vertex Color Layers", set=None)

    attribute_set_flags: StringProperty(name="Attribute Layout Flags")

    unk12: FloatVectorProperty(name="GMD Unk12 Data", size=32)
    unk14: FloatVectorProperty(name="GMD Unk14 Data", size=32)
    attribute_set_floats: FloatVectorProperty(name="GMD Attribute Set Floats", size=16)
    material_origin_type: IntProperty(name="GMDMaterial origin type")
    material_json: StringProperty(name="GMDMaterial data JSON")


class YakuzaPropertyPanel(bpy.types.Panel):
    """
    Panel that displays the YakuzaPropertyGroup attached to the selected material.
    """

    bl_label = "Yakuza Properties"

    bl_order = 1  # Make it appear near the top

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
            for i in range(length // 4):
                for j in range(i * 4, (i + 1) * 4):
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
YAKUZA_SHADER_NODE_GROUP = "Neo Yakuza Shader"
YAKUZA_UV_SCALER = "UV scaler"

DEFAULT_DIFFUSE_COLOR = (1, 1, 1, 1)
DEFAULT_UNUSED_COLOR = (0, 0, 0, 1)
DEFAULT_NORMAL_COLOR = (0.5, 0.5, 1, 1)
DEFAULT_MULTI_COLOR = (0, 1, 0, 1)
DEFAULT_Z_COLOR = (0.5, 1, 0.5, 1)

RDRT_SHADERS = ["[rd]", "[rt]", "[rs]", "_m2"]


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

    # set all imported textures to non-color, this makes making shaders easier so you dont have to set every non-di
    # texture to noncolor. _di textures are simply just multiplied by themselves - this is how the ingame shaders do it
    image.colorspace_settings.name = "Non-Color"

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


# Extensions to try when loading textures, in order of preference.
# Dragon Engine level textures are often .png after conversion from DDS.
_SUPPORTED_TEXTURE_EXTENSIONS = (".dds", ".png", ".jpg", ".jpeg", ".tga")


def _find_texture_file(folder: str, tex_name: str) -> Optional[str]:
    """
    Search for a texture file with multiple extension fallbacks.
    Returns the full path if found, None otherwise.
    Tries .dds, .png, .jpg, .jpeg, .tga in order.
    """
    for ext in _SUPPORTED_TEXTURE_EXTENSIONS:
        candidate = os.path.join(folder, f"{tex_name}{ext}")
        if os.path.isfile(candidate):
            return candidate
    return None


def _find_texture_file_in_folders(tex_name: str, folders):
    """
    Search for a texture file with multiple extension fallbacks across several directories.
    Returns the full path if found, None otherwise. Tries each folder in order.
    """
    for folder in folders:
        found = _find_texture_file(folder, tex_name)
        if found:
            return found
    return None


def load_texture_from_name(node_tree: bpy.types.NodeTree, texture_folders, tex_name: str,
                           color_if_not_found=(1, 0, 1, 1)) -> ShaderNodeTexImage:
    """
    Given a GMD texture name, find or create the Blender counterpart and add a texture node to the given material tree
    using that texture.
    It will try to load the image from each folder in texture_folders if possible, but if it's not there then a dummy image
    will be created filled with a specific color.
    Yakuza dummy textures "dummy_{black,white,multi,nmap}" will be created with the correct colors,
    and won't be searched for on disk.
    :param node_tree: The node tree to add the texture node to.
    :param texture_folders: List of directories to search for textures, tried in order.
    :param tex_name: The name of the texture.
    :param color_if_not_found: The color to fill the dummy image with, if an actual texture cannot be found.
    :return: A Texture node containing an image relevant to the name tex_name.
    """

    # Always create the image node
    image_node = node_tree.nodes.new('ShaderNodeTexImage')

    # Check for known dummy textures first — these are created internally and never loaded from disk.
    if tex_name == "dummy_black":
        image_node.image = create_proxy_texture(tex_name, f"{tex_name}.dds", (0, 0, 0, 1))
    elif tex_name == "dummy_white":
        image_node.image = create_proxy_texture(tex_name, f"{tex_name}.dds", (1, 1, 1, 1))
    elif tex_name == "default_z":
        image_node.image = create_proxy_texture(tex_name, f"{tex_name}.dds", DEFAULT_Z_COLOR)
    elif tex_name == "dummy_multi":
        image_node.image = create_proxy_texture(tex_name, f"{tex_name}.dds", DEFAULT_MULTI_COLOR)
    elif tex_name == "dummy_nmap":
        image_node.image = create_proxy_texture(tex_name, f"{tex_name}.dds", DEFAULT_NORMAL_COLOR)
    else:
        # Check if any already-loaded image matches (try all supported extensions).
        found_image = None
        for ext in _SUPPORTED_TEXTURE_EXTENSIONS:
            candidate = f"{tex_name}{ext}"
            if candidate in bpy.data.images:
                found_image = bpy.data.images[candidate]
                break

        if found_image:
            image_node.image = found_image
        else:
            # Try to find on disk with multiple extension fallbacks across all search folders.
            tex_filepath = _find_texture_file_in_folders(tex_name, texture_folders)
            if not tex_filepath:
                # The texture doesn't exist anywhere.
                image_node.image = create_proxy_texture(tex_name, f"{tex_name}.dds", color_if_not_found)
            else:
                image = bpy.data.images.load(tex_filepath, check_existing=True)
                image.colorspace_settings.name = "Non-Color"
                image.yakuza_data.inited = True
                image.yakuza_data.yk_name = tex_name
                image_node.image = image

    return cast(ShaderNodeTexImage, image_node)


def set_yakuza_shader_material_from_attributeset(material: bpy.types.Material, yakuza_inputs: bpy.types.NodeInputs,
                                                 attribute_set: GMDAttributeSet, texture_folders):
    """
    Given a material and an attribute set, attach all of the relevant data from the attribute set to the material.
    :param material: The material to update
    :param yakuza_inputs: The inputs to the Yakuza Shader node in the material
    :param attribute_set: The GMDAttributeSet this Material represents.
    :param texture_folders: List of directories to search for textures, tried in order.
                           Can also be a single string (deprecated) for backward compatibility.
    :return: None
    """
    # Normalize: accept a single str for backward compat, but treat as a list internally.
    if isinstance(texture_folders, str):
        texture_folders = [texture_folders]

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
    material.yakuza_data.unk12 = attribute_set.unk12.float_data if attribute_set.unk12 else [0] * 32
    material.yakuza_data.unk14 = attribute_set.unk14.int_data if attribute_set.unk14 else [0] * 32
    material.yakuza_data.attribute_set_floats = attribute_set.attr_extra_properties
    material.yakuza_data.material_origin_type = attribute_set.material.origin_version.value
    material.yakuza_data.material_json = json.dumps(vars(attribute_set.material.origin_data))

    print('THIS MATERIAL: ' + str(material.yakuza_data.shader_name) + ' EXPECTS: ' + str(material.yakuza_data.cached_expected_uv_layers))

    # TODO detect if yakuza 8 is used, because that apparently uses roughness instead of glossiness (notyoshi)

    # Set the skin shader to 1 if the shader is a skin shader
    yakuza_inputs["Skin shader"].default_value = 1.0 if "[skin]" in attribute_set.shader.name else 0.0

    # variable for checking if de or oe
    engine = 1.0 if material.yakuza_data.material_origin_type == 4 else 0.0

    yakuza_inputs["Engine"].default_value = engine

    # variable for checking if oe clothes shader (MT blue channel is used to blend the pattern textures in this case,
    # instead of multiplying the specular power)
    rdrt_shaders = ["[rd]", "[rt]", "[rs]", "_m2"]

    yakuza_inputs["Is OE cloth shader"].default_value = 1.0 if any([x in attribute_set.shader.name
                                                                    for x in rdrt_shaders]) and engine == 0 else 0.0

    # variable for checking if glossiness should be inverted
    yakuza_inputs["[rough]"].default_value = 1.0 if "[rough]" in attribute_set.shader.name else 0.0

    # Helper: a texture name that contains "none" is a placeholder and should be treated as empty.
    def _is_valid_texture(name):
        return name is not None and "none" not in name.lower()

    # Disable RD/RT when neither the shader name indicates rd/rt usage nor are actual
    # rt/rd textures assigned in the attribute set. Set to 0.0 (enabled) if either is true.
    has_rd_rt_shaders = any(x in attribute_set.shader.name for x in rdrt_shaders)
    has_rd_rt_textures = bool(_is_valid_texture(attribute_set.texture_rt) or _is_valid_texture(attribute_set.texture_rd))
    yakuza_inputs["Disable RD/RT"].default_value = 0.2 if has_rd_rt_shaders or has_rd_rt_textures else 1.0

    # check if asset shader
    yakuza_inputs["Asset shader"].default_value = 1.0 if re.search(r'^r_', attribute_set.shader.name) or \
                                                         re.search(r'^rs_', attribute_set.shader.name) else 0.0
    # check if imperfection
    yakuza_inputs["Imperfection"].default_value = 1.0 if "h2dz" in attribute_set.shader.name else 0.0

    # opacity
    yakuza_inputs["Opacity"].default_value = attribute_set.material.origin_data.opacity / 255

    # oe shader params
    yakuza_inputs["Specular color"].default_value[0] = attribute_set.material.origin_data.specular[0] / 255
    yakuza_inputs["Specular color"].default_value[1] = attribute_set.material.origin_data.specular[1] / 255
    yakuza_inputs["Specular color"].default_value[2] = attribute_set.material.origin_data.specular[2] / 255
    yakuza_inputs["Specular power"].default_value = attribute_set.material.origin_data.power

    # Wire the material's diffuse RGB color multiplier.
    # Dragon Engine building assets use unit-white textures with actual color stored
    # in MaterialStruct_YK1.diffuse (3 uint8 bytes). The shader node group has no native
    # tint socket so we multiply this into the texture path for asset shaders.
    origin_data = attribute_set.material.origin_data
    mat_diffuse_r = origin_data.diffuse[0] / 255
    mat_diffuse_g = origin_data.diffuse[1] / 255
    mat_diffuse_b = origin_data.diffuse[2] / 255
    is_asset_shader = bool(re.search(r'^r_', attribute_set.shader.name) or
                          re.search(r'^rs_', attribute_set.shader.name))
    # Only multiply when the color is not white (1,1,1) — skip if already neutral.
    needs_tint = is_asset_shader and not (mat_diffuse_r == 1.0 and mat_diffuse_g == 1.0 and mat_diffuse_b == 1.0)
    yakuza_inputs["Is Y3 [rs] shader"].default_value = 1.0 if "[rd]" not in attribute_set.shader.name and "[rs]" \
                                                              in attribute_set.shader.name else 0.0

    sp_shaders = ["ds", "st_", "2s"]
    yakuza_inputs["SP shader"].default_value = 1.0 if any([x in attribute_set.shader.name for x in sp_shaders]) \
                                                      and engine == 0 else 0.0

    # Build a mapping from texture slot name to the GMD UV set index it should use.
    tex_slot_to_uv_index = {
        "texture_diffuse": 0,
        "texture_multi": 0,
        "texture_normal": 0,
        "texture_refl": 0,
        "texture_rm": 1,
        "texture_rs": 1,
        "texture_rt": 1,
        "texture_rd": 1,
    }

    # Collect available Blender UV layer names. Each GMD UV set that has 2 components
    blender_uv_names = [spec.name for spec in layer_names.uv_layers if spec.storage.n_comps == 2]

    # Helper: wire a specific UV layer to a destination vector input.
    # ShaderNodeUVMap selects the named UV layer directly (no passthrough needed).
    def wire_uv_for_slot(slot_name: str, dest_input, y_pos: int):
        gmd_uv_i = tex_slot_to_uv_index.get(slot_name, 0)
        if not blender_uv_names or gmd_uv_i >= len(blender_uv_names):
            return
        uvmap = material.node_tree.nodes.new("ShaderNodeUVMap")
        uvmap.name = f"UVSelect_{slot_name}"
        if hasattr(uvmap, "uv_map"):
            uvmap.uv_map = blender_uv_names[gmd_uv_i]
        elif hasattr(uvmap, "map_name"):
            uvmap.map_name = blender_uv_names[gmd_uv_i]
        uvmap.location = (-800, y_pos)
        material.node_tree.links.new(uvmap.outputs["UV"], dest_input)

    # Convenience function for creating a texture node for an Optional texture
    def set_texture(set_into: NodeSocketColor, tex_name: Optional[str],
                    next_image_y: int = 0, color_if_not_found=(1, 0, 1, 1), multiply_color=None) \
            -> Tuple[Optional[ShaderNodeTexImage], int]:
        if not _is_valid_texture(tex_name):
            return None, next_image_y
        image_node = load_texture_from_name(material.node_tree, texture_folders, tex_name, color_if_not_found)
        image_node.location = (-500, next_image_y)
        # image_node.label = tex_name

        # Hide the node unless it has real image data (FILE source). Generated/dummy placeholders stay hidden.
        if image_node.image and image_node.image.source == 'FILE':
            image_node.hide = False
        else:
            image_node.hide = True

        # Wire the correct UV map to this texture node's Vector input using the per-slot selector.
        wire_uv_for_slot(set_into.name, image_node.inputs["Vector"], next_image_y)

        if multiply_color is not None:
            # Insert a MixRGB (Multiply) node to tint the texture with the material's color.
            mix_node = material.node_tree.nodes.new("ShaderNodeMixRGB")
            mix_node.blend_type = "MULTIPLY"
            mix_node.location = (-350, next_image_y)
            mix_node.inputs["Color2"].default_value = (*multiply_color, 1.0)
            material.node_tree.links.new(image_node.outputs["Color"], mix_node.inputs["Color1"])
            material.node_tree.links.new(mix_node.outputs["Color"], set_into)
        else:
            material.node_tree.links.new(image_node.outputs["Color"], set_into)

        next_image_y -= 100
        image_node.label = set_into.name
        return image_node, next_image_y

    # Create the diffuse texture, optionally tinted by the material's intrinsic color.
    diffuse_color_multiplier = (mat_diffuse_r, mat_diffuse_g, mat_diffuse_b) if needs_tint else None
    diffuse_tex, next_y = set_texture(yakuza_inputs["texture_diffuse"], attribute_set.texture_diffuse,
                                      multiply_color=diffuse_color_multiplier)

    # If no diffuse texture was connected (index == -1 or not found), fall back to the material's
    # intrinsic diffuse color instead of leaving the socket at its default white.
    if not diffuse_tex:
        yakuza_inputs["texture_diffuse"].default_value = (mat_diffuse_r, mat_diffuse_g, mat_diffuse_b, 1.0)
        # Also set base_color inputs if they exist on the shader node group,
        # so assets without a diffuse texture still show the correct material color.
        for socket_name in ("base_color", "Base Color"):
            if socket_name in yakuza_inputs:
                yakuza_inputs[socket_name].default_value = (mat_diffuse_r, mat_diffuse_g, mat_diffuse_b, 1.0)

    transparent_shaders = ["_a", "_b", "_c", "_d", "_m", "_p"]

    if diffuse_tex:
        # Link the texture alpha with the Yakuza Shader, and make the material do hashed or blended alpha
        # (depending on shader), and set shadow method to none.
        for i in transparent_shaders:
            regex_test = "^.(" + re.escape(i) + ").+|^..(" + re.escape(i) + ").+"

            if re.search(regex_test, attribute_set.shader.name):
                material.node_tree.links.new(diffuse_tex.outputs["Alpha"], yakuza_inputs["Diffuse Alpha"])
                if "_c" in attribute_set.shader.name:
                    material.blend_method = "HASHED"
                    diffuse_tex.label = diffuse_tex.label + '_clip'
                else:
                    material.blend_method = "BLEND"
                    diffuse_tex.label = diffuse_tex.label + '_blend'
                if hasattr(material, "shadow_method"):
                    material.shadow_method = "NONE"
                else:
                    material.use_transparent_shadow = False

    # Attach the other textures.
    multi_tex, next_y = set_texture(yakuza_inputs["texture_multi"], attribute_set.texture_multi, next_y,
                                    DEFAULT_MULTI_COLOR)
    if multi_tex:
        material.node_tree.links.new(multi_tex.outputs["Alpha"], yakuza_inputs["Multi Alpha"])
    normal_tex, next_y = set_texture(yakuza_inputs["texture_normal"], attribute_set.texture_normal, next_y,
                                     DEFAULT_NORMAL_COLOR)
    if normal_tex:
        material.node_tree.links.new(normal_tex.outputs["Alpha"], yakuza_inputs["Normal Alpha"])
    _, next_y = set_texture(yakuza_inputs["texture_refl"], attribute_set.texture_refl, next_y, DEFAULT_Z_COLOR)
    _, next_y = set_texture(yakuza_inputs["texture_rm"], attribute_set.texture_rm, next_y, DEFAULT_Z_COLOR)
    _, next_y = set_texture(yakuza_inputs["texture_rs"], attribute_set.texture_rs, next_y, DEFAULT_NORMAL_COLOR)
    rt_tex, next_y = set_texture(yakuza_inputs["texture_rt"], attribute_set.texture_rt, next_y, DEFAULT_NORMAL_COLOR)
    if rt_tex:
        material.node_tree.links.new(rt_tex.outputs["Alpha"], yakuza_inputs["RT Alpha"])
    _, next_y = set_texture(yakuza_inputs["texture_rd"], attribute_set.texture_rd, next_y, DEFAULT_DIFFUSE_COLOR)


def append_data_from_yakuza_shader(error: ErrorReporter):
    file_path = Path(__file__).parent / "yakuza_shader.blend"
    with bpy.data.libraries.load(str(file_path)) as (data_from, data_to):
        if YAKUZA_SHADER_NODE_GROUP not in data_from.node_groups:
            error.fatal(
                f"Couldn't find the node group '{YAKUZA_SHADER_NODE_GROUP}' in the built-in shader .blend library")
        if YAKUZA_UV_SCALER not in data_from.node_groups:
            error.fatal(f"Couldn't find the node group '{YAKUZA_UV_SCALER}' in the built-in shader .blend library")
        data_to.node_groups.append(YAKUZA_SHADER_NODE_GROUP)
        data_to.node_groups.append(YAKUZA_UV_SCALER)


def get_yakuza_shader_node_group(error: ErrorReporter):
    """
    Create or retrieve the Yakuza Shader node group, depending on whether it exists.
    :return: The Yakuza Shader node group.
    """

    if YAKUZA_SHADER_NODE_GROUP in bpy.data.node_groups:
        return bpy.data.node_groups[YAKUZA_SHADER_NODE_GROUP]
    else:
        append_data_from_yakuza_shader(error)
        return bpy.data.node_groups[YAKUZA_SHADER_NODE_GROUP]


def get_uv_scaler_node_group(error: ErrorReporter):
    if YAKUZA_UV_SCALER in bpy.data.node_groups:
        return bpy.data.node_groups[YAKUZA_UV_SCALER]
    else:
        append_data_from_yakuza_shader(error)
        return bpy.data.node_groups[YAKUZA_UV_SCALER]
