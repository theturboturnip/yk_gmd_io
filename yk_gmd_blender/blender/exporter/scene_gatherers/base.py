import abc
import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, cast, Tuple

import bpy
from bpy.types import ShaderNodeGroup, ShaderNodeTexImage
from mathutils import Vector
from ...common import GMDGame, YakuzaFileRootData
from ...materials import YAKUZA_SHADER_NODE_GROUP, RDRT_SHADERS
from ...materials import YakuzaPropertyGroup
from ....gmdlib.abstract.gmd_attributes import GMDAttributeSet, GMDUnk12, GMDUnk14, GMDMaterial
from ....gmdlib.abstract.gmd_scene import GMDScene, HierarchyData
from ....gmdlib.abstract.gmd_shader import GMDShader, GMDVertexBufferLayout
from ....gmdlib.abstract.nodes.gmd_node import GMDNode
from ....gmdlib.abstract.nodes.gmd_object import GMDBoundingBox
from ....gmdlib.errors.error_reporter import ErrorReporter
from ....gmdlib.structure.kenzan.material import MaterialStruct_Kenzan
from ....gmdlib.structure.version import GMDVersion
from ....gmdlib.structure.yk1.material import MaterialStruct_YK1


class BoundingBoxCalc(Enum):
    OLD_INFINITE = 0
    EXPERIMENTAL_FROM_BLENDER = 1
    EXPERIMENTAL_INFINITE_CENTRED = 2

    @staticmethod
    def blender_props():
        return [
            ("OLD_INFINITE", "Huge bounding box around 0,0,0",
             "Old behaviour. Brute-force method, generate a huge bounding box for each item."),
            ("EXPERIMENTAL_FROM_BLENDER", "[EXP] Blender-accurate bounding boxes",
             "Experimental: Use Blender's bounding boxes. Does not work perfectly on skinned"),
            ("EXPERIMENTAL_INFINITE_CENTRED", "[EXP] Huge bounding box around object centres",
             "Experimental: Use huge bounding boxes, properly centred. May be relevant for stage export")
        ]

    @staticmethod
    def map_from_blender_props(blender_enum: str) -> 'BoundingBoxCalc':
        return {
            "OLD_INFINITE": BoundingBoxCalc.OLD_INFINITE,
            "EXPERIMENTAL_FROM_BLENDER": BoundingBoxCalc.EXPERIMENTAL_FROM_BLENDER,
            "EXPERIMENTAL_INFINITE_CENTRED": BoundingBoxCalc.EXPERIMENTAL_INFINITE_CENTRED,
        }[blender_enum]


@dataclass(frozen=True)
class GMDSceneGathererConfig:
    game: GMDGame
    bounding_box_calc: BoundingBoxCalc
    debug_compare_matrices: bool


def name_matches_expected(name, expected):
    # A "correct" name == {expected name}.XXX
    # To check this, split the string on expected name.
    # It will produce ['', ''] if the name is the same, or '', '.XXX' otherwise
    split_name = name.split(expected)
    if split_name == ['', '']:
        return True
    elif len(split_name) != 2 or split_name[0] != '' or not re.match(r'\.\d\d\d', split_name[1]):
        return False
    return True


def remove_blender_duplicate(name: str) -> str:
    return re.sub(r'\.\d\d\d', "", name)


class BaseGMDSceneGatherer(abc.ABC):
    """
    Class used to gather meshes and materials from Blender, to export a GMDScene.
    Uses ErrorReporter for all error handling.
    """
    config: GMDSceneGathererConfig
    name: str
    original_scene: GMDScene
    error: ErrorReporter
    flags: Optional[Tuple[int, int, int, int, int, int]]

    node_roots: List[GMDNode]
    material_map: Dict[str, GMDAttributeSet]

    def __init__(self, filepath: str, original_scene: GMDScene, config: GMDSceneGathererConfig, error: ErrorReporter):
        self.config = config
        self.filepath = filepath
        self.name = original_scene.name
        self.original_scene = original_scene
        self.error = error
        self.flags = None

        self.node_roots = []
        self.material_map = {}

        if self.config.debug_compare_matrices:
            assert original_scene is not None

    def build(self) -> GMDScene:
        assert self.flags is not None
        return GMDScene(
            name=self.name,
            flags=self.flags,
            overall_hierarchy=HierarchyData(self.node_roots)
        )

    def detect_export_collection(self, context: bpy.types.Context) -> Tuple[bpy.types.Object, bpy.types.Collection]:
        # Decide on an export root
        # Require a collection to be selected I guess?
        # Issue a warning if the name is different?

        selected_object = context.view_layer.objects.active

        if not selected_object:
            self.error.fatal("No object selected - please select the root object to export")

        # This is the list of all collections an object could be in, including nested ones.
        # i.e. the full chain Collection > scene_name_collection > object
        possible_collections: Tuple[bpy.types.Collection, ...] = selected_object.users_collection
        # The selected collection is the one that has the armature as a root object
        selected_collection = None
        for collection in possible_collections:
            if selected_object in list(collection.objects):
                selected_collection = collection
                break
        if not selected_collection:
            self.error.fatal(
                f"Can't figure out which collection the selected object is a part of! This should never happen")

        if not name_matches_expected(selected_collection.name, self.name):
            self.error.recoverable(f"Collection name {selected_collection.name} does not map to expected {self.name}!\n"
                                   f"Expected '{self.name}' or '{self.name}.XYZ'.")

        if selected_collection.children:
            self.error.recoverable(
                f"Collection {selected_collection.name} has children collections, which will be ignored.")

        if not selected_object.yakuza_file_root_data.is_valid_root:
            self.error.info(
                f"Yakuza File Root Data not checked for {selected_object.name} - assuming this is a legacy file. "
                f"In the future this might become an error.")

        return selected_object, selected_collection

    def guess_or_take_flags(self, yakuza_file_root_data: YakuzaFileRootData):
        imported_ver = GMDGame.mapping_from_blender_props()[yakuza_file_root_data.imported_version]
        # If the scene we're exporting came from the same engine as the file we're exporting over, keep those flags
        if yakuza_file_root_data.is_valid_root and (imported_ver & self.config.game != 0):
            self.flags = json.loads(yakuza_file_root_data.flags_json)
            if len(self.flags) != 6 or any(not isinstance(x, int) for x in self.flags):
                self.error.fatal(f"File root has invalid flags {self.flags} - must be a list of 6 integers")
            self.error.info(f"Taking flags from previously imported file root")
        else:
            # Take the flags from the target file
            self.flags = self.original_scene.flags
            self.error.info(f"Taking flags from target file")

    def gmd_bounding_box(self, object: bpy.types.Object) -> GMDBoundingBox:
        if self.config.bounding_box_calc == BoundingBoxCalc.OLD_INFINITE:
            return GMDBoundingBox.from_points((
                Vector((-1000, -1000, -1000)),
                Vector((+1000, +1000, +1000))
            ))
        elif self.config.bounding_box_calc == BoundingBoxCalc.EXPERIMENTAL_FROM_BLENDER:
            return GMDBoundingBox.from_points(
                Vector((-x, z, y))
                for x, y, z in object.bound_box
            )
        elif self.config.bounding_box_calc == BoundingBoxCalc.EXPERIMENTAL_INFINITE_CENTRED:
            blender_centre = object.location
            centre = Vector((-blender_centre[0], blender_centre[2], blender_centre[1]))
            return GMDBoundingBox.from_points((
                Vector((-1000, -1000, -1000)) + centre,
                Vector((+1000, +1000, +1000)) + centre
            ))
        else:
            self.error.fatal(f"bounding_box_calc config is invalid value {self.config.bounding_box_calc}")

    def blender_material_to_gmd_attribute_set(self, material: bpy.types.Material,
                                              referencing_object: bpy.types.Object) -> GMDAttributeSet:
        if material.name in self.material_map:
            return self.material_map[material.name]

        if not material.yakuza_data.inited:
            self.error.fatal(
                f"Material {material.name} on object {referencing_object.name} does not have any Yakuza Properties, "
                f"and cannot be exported.\n"
                f"A Yakuza Material must have valid Yakuza Properties, and must have exactly one Yakuza Shader node.")
        if not material.use_nodes:
            self.error.fatal(
                f"Material {material.name} on object {referencing_object.name} does not use nodes, "
                f"and cannot be exported.\n"
                f"A Yakuza Material must have valid Yakuza Properties, and must have exactly one Yakuza Shader node.")

        yakuza_shader_nodes = [node for node in material.node_tree.nodes if
                               node.bl_idname == "ShaderNodeGroup" and node.node_tree.name == YAKUZA_SHADER_NODE_GROUP]
        self.error.debug("MATERIAL", str([node.name for node in material.node_tree.nodes]))
        self.error.debug("MATERIAL", str([node.bl_idname for node in material.node_tree.nodes]))
        self.error.debug("MATERIAL", str([node.bl_label for node in material.node_tree.nodes]))
        if not yakuza_shader_nodes:
            self.error.fatal(
                f"Material {material.name} on object {referencing_object.name} does not have a Yakuza Shader node, "
                f"and cannot be exported.\n"
                f"A Yakuza Material must have valid Yakuza Properties, and must have exactly one Yakuza Shader node.")
        elif len(yakuza_shader_nodes) > 1:
            self.error.fatal(
                f"Material {material.name} on object {referencing_object.name} has multiple Yakuza Shader nodes, "
                f"and cannot be exported.\n"
                f"A Yakuza Material must have valid Yakuza Properties, and must have exactly one Yakuza Shader node.")
        yakuza_shader_node = cast(ShaderNodeGroup, yakuza_shader_nodes[0])

        yakuza_data: YakuzaPropertyGroup = material.yakuza_data
        vertex_layout_flags = int(yakuza_data.shader_vertex_layout_flags, base=16)
        vertex_layout = GMDVertexBufferLayout.build_vertex_buffer_layout_from_flags(vertex_layout_flags, True,
                                                                                    self.error)

        shader = GMDShader(
            name=yakuza_data.shader_name,
            vertex_buffer_layout=vertex_layout,
            assume_skinned=yakuza_data.assume_skinned
        )

        def get_texture(texture_name: str) -> Optional[str]:
            input = yakuza_shader_node.inputs[texture_name]
            if not input.links:
                return None
            if not isinstance(input.links[0].from_node, ShaderNodeTexImage):
                self.error.fatal(
                    f"Material {material.name} on object {referencing_object.name} has an input {texture_name} "
                    f"which is linked to a {type(input.links[0])} node.\n"
                    f"All the texture inputs on a Yakuza Shader node should either be linked to an Image Texture node or not linked at all.")
            teximage_node: ShaderNodeTexImage = input.links[0].from_node
            import os
            image_name, ext = os.path.splitext(teximage_node.image.name)
            if ext not in ['', '.dds']:
                self.error.fatal(
                    f"Input {texture_name} in material {material.name} on object {referencing_object.name} "
                    f"is '{teximage_node.image.name}', which is not a DDS file.\n"
                    f"Yakuza cannot handle these. Please change it to be a .dds file.")

            if not image_name:
                self.error.fatal(
                    f"Material {material.name}.{texture_name} filepath {teximage_node.image.filepath} "
                    f"couldn't be parsed correctly.")

            return image_name

        gmd_material_origin_version = GMDVersion(yakuza_data.material_origin_type)
        if gmd_material_origin_version == GMDVersion.Kiwami1 or gmd_material_origin_version == GMDVersion.Dragon:
            gmd_material = GMDMaterial(
                origin_version=gmd_material_origin_version,
                origin_data=MaterialStruct_YK1(**json.loads(yakuza_data.material_json))
            )
        elif gmd_material_origin_version == GMDVersion.Kenzan:
            gmd_material = GMDMaterial(
                origin_version=gmd_material_origin_version,
                origin_data=MaterialStruct_Kenzan(**json.loads(yakuza_data.material_json))
            )
        else:
            self.error.fatal(f"Unknown GMDVersion {gmd_material_origin_version}")

        # TODO - Add a check for "missing expected texture". Put "expected textures" in Material Yakuza Data,
        #  and compare against provided in the node.
        # TODO - image nodes will null textures exist - those currently break the export

        # gmd material override... dunno how else to do this!

        gmd_material.origin_data.specular[0] = round(yakuza_shader_node.inputs["Specular color"].default_value[0] * 255)
        gmd_material.origin_data.specular[1] = round(yakuza_shader_node.inputs["Specular color"].default_value[1] * 255)
        gmd_material.origin_data.specular[2] = round(yakuza_shader_node.inputs["Specular color"].default_value[2] * 255)
        gmd_material.origin_data.power = yakuza_shader_node.inputs["Specular power"].default_value
        gmd_material.origin_data.opacity = round(yakuza_shader_node.inputs["Opacity"].default_value * 255)

        uv_node = [node for node in material.node_tree.nodes if node.bl_idname == "ShaderNodeGroup" and
                   node.node_tree.name == "UV scaler"]

        if len(uv_node) == 1:
            if not any([x in yakuza_data.shader_name for x in RDRT_SHADERS]):
                self.error.recoverable(
                    f"Blender material '{material.name}' contains a UV scaler node, "
                    f"but the shader may not support UV scaling. "
                    f"This may produce unexpected results. Disable Strict Export to continue."
                )

            rtpos = uv_node[0].inputs[0].default_value  # RT X
            rtpos2 = uv_node[0].inputs[1].default_value  # RT Y
            rdpos = uv_node[0].inputs[2].default_value  # R(D/S/M) X
            rdpos2 = uv_node[0].inputs[3].default_value  # ^ Y

            if gmd_material_origin_version == GMDVersion.Dragon:
                imperfection = uv_node[0].inputs[4].default_value  # imperfection

                yakuza_data.unk12[6] = rtpos
                yakuza_data.unk12[7] = rtpos2
                yakuza_data.unk12[4] = rdpos
                yakuza_data.unk12[5] = rdpos2
                yakuza_data.unk12[12] = imperfection
            else:
                if "[rd]" not in shader.name and "[rt]" not in shader.name:
                    yakuza_data.unk12[2] = rtpos
                    yakuza_data.unk12[3] = rtpos2
                    yakuza_data.attribute_set_floats[8] = rdpos
                    yakuza_data.attribute_set_floats[9] = rdpos2
                else:
                    yakuza_data.attribute_set_floats[8] = rtpos
                    yakuza_data.attribute_set_floats[9] = rtpos2
                    yakuza_data.unk12[8] = rdpos
                    yakuza_data.unk12[9] = rdpos2

        elif len(uv_node) > 1:
            self.error.fatal(f"Too many UV scaler nodes in " + material.name + "!")

        attribute_set = GMDAttributeSet(
            shader=shader,

            texture_diffuse=get_texture("texture_diffuse"),
            texture_refl=get_texture("texture_refl"),
            texture_multi=get_texture("texture_multi"),
            texture_rm=get_texture("texture_rm"),
            texture_rs=get_texture("texture_rs"),
            texture_normal=get_texture("texture_normal"),
            texture_rt=get_texture("texture_rt"),
            texture_rd=get_texture("texture_rd"),

            material=gmd_material,
            unk12=GMDUnk12(list(yakuza_data.unk12)),
            unk14=GMDUnk14(list([int(x) for x in yakuza_data.unk14])),
            attr_flags=int(yakuza_data.attribute_set_flags, base=16),
            attr_extra_properties=yakuza_data.attribute_set_floats,
        )
        self.material_map[material.name] = attribute_set
        self.error.debug("MATERIAL", f"mat {material.name} -> {attribute_set}")
        return attribute_set

    def gather_exported_items(self, context: bpy.types.Context):
        raise NotImplementedError()
