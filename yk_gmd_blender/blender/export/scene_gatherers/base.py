import abc
import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, cast, Tuple

from bpy.types import ShaderNodeGroup, ShaderNodeTexImage
from mathutils import Matrix, Vector, Quaternion

import bpy
from yk_gmd_blender.blender.common import GMDGame
from yk_gmd_blender.blender.coordinate_converter import transform_blender_to_gmd, \
    transform_position_gmd_to_blender
from yk_gmd_blender.blender.export.mesh_exporter.functions import split_unskinned_blender_mesh_object, \
    split_skinned_blender_mesh_object
from yk_gmd_blender.blender.materials import YAKUZA_SHADER_NODE_GROUP
from yk_gmd_blender.blender.materials import YakuzaPropertyGroup
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet, GMDUnk12, GMDUnk14, GMDMaterial
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene, HierarchyData, depth_first_iterate
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDShader, GMDVertexBufferLayout
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_object import GMDUnskinnedObject, GMDSkinnedObject
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.material import MaterialStruct_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.version import GMDVersion
from yk_gmd_blender.yk_gmd.v2.structure.yk1.material import MaterialStruct_YK1


@dataclass(frozen=True)
class GMDSceneGathererConfig:
    game: GMDGame
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


def remove_blender_duplicate(name:str) -> str:
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

    node_roots: List[GMDNode]
    material_map: Dict[str, GMDAttributeSet]

    def __init__(self, filepath: str, original_scene: GMDScene, config: GMDSceneGathererConfig, error: ErrorReporter):
        self.config = config
        self.filepath = filepath
        self.name = original_scene.name
        self.original_scene = original_scene
        self.error = error

        self.node_roots = []
        self.material_map = {}

        if self.config.debug_compare_matrices:
            assert original_scene is not None

    def build(self) -> GMDScene:
        return GMDScene(
            name=self.name,
            overall_hierarchy=HierarchyData(self.node_roots)
        )

    def detect_export_collection(self, context: bpy.types.Context) -> bpy.types.Collection:
        # Decide on an export root
        # Require a collection to be selected I guess?
        # Issue a warning if the name is different?

        selected_object = context.view_layer.objects.active

        # This is the list of all collections an object could be in, including nested ones.
        # i.e. the full chain Collection > scene_name_collection > object
        possible_collections: Tuple[bpy.types.Collection, ...] = context.view_layer.objects.active.users_collection
        # The selected collection is the one that has the armature as a root object
        selected_collection = None
        for collection in possible_collections:
            if selected_object in list(collection.objects):
                selected_collection = collection
                break
        if not selected_collection:
            self.error.fatal(f"Can't figure out which collection the selected object is a part of! This should never happen")

        if not name_matches_expected(selected_collection.name, self.name):
            self.error.recoverable(f"Collection name {selected_collection.name} does not map to expected {self.name}!\n"
                                   f"Expected '{self.name}' or '{self.name}.XYZ'.")

        if selected_collection.children:
            self.error.recoverable(
                f"Collection {selected_collection.name} has children collections, which will be ignored.")

        return selected_collection

    def blender_material_to_gmd_attribute_set(self, material: bpy.types.Material, referencing_object: bpy.types.Object) -> GMDAttributeSet:
        if material.name in self.material_map:
            return self.material_map[material.name]

        if (not material.yakuza_data.inited):
            self.error.fatal(f"Material {material.name} on object {referencing_object.name} does not have any Yakuza Properties, and cannot be exported.\n"
                             f"A Yakuza Material must have valid Yakuza Properties, and must have exactly one Yakuza Shader node.")
        if not material.use_nodes:
            self.error.fatal(
                f"Material {material.name} on object {referencing_object.name} does not use nodes, and cannot be exported.\n"
                f"A Yakuza Material must have valid Yakuza Properties, and must have exactly one Yakuza Shader node.")

        yakuza_shader_nodes = [node for node in material.node_tree.nodes if node.bl_idname == "ShaderNodeGroup" and node.node_tree.name == YAKUZA_SHADER_NODE_GROUP]
        self.error.debug("MATERIAL", str([node.name for node in material.node_tree.nodes]))
        self.error.debug("MATERIAL", str([node.bl_idname for node in material.node_tree.nodes]))
        self.error.debug("MATERIAL", str([node.bl_label for node in material.node_tree.nodes]))
        if not yakuza_shader_nodes:
            self.error.fatal(
                f"Material {material.name} on object {referencing_object.name} does not have a Yakuza Shader node, and cannot be exported.\n"
                f"A Yakuza Material must have valid Yakuza Properties, and must have exactly one Yakuza Shader node.")
        elif len(yakuza_shader_nodes) > 1:
            self.error.fatal(
                f"Material {material.name} on object {referencing_object.name} has multiple Yakuza Shader nodes, and cannot be exported.\n"
                f"A Yakuza Material must have valid Yakuza Properties, and must have exactly one Yakuza Shader node.")
        yakuza_shader_node = cast(ShaderNodeGroup, yakuza_shader_nodes[0])

        yakuza_data: YakuzaPropertyGroup = material.yakuza_data
        vertex_layout_flags = int(yakuza_data.shader_vertex_layout_flags, base=16)
        vertex_layout = GMDVertexBufferLayout.build_vertex_buffer_layout_from_flags(vertex_layout_flags, True, self.error)

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
                self.error.fatal(f"Material {material.name} on object {referencing_object.name} has an input {texture_name} which is linked to a {type(input.links[0])} node.\n"
                                 f"All the texture inputs on a Yakuza Shader node should either be linked to an Image Texture node or not linked at all.")
            teximage_node: ShaderNodeTexImage = input.links[0].from_node
            import os
            image_name, ext = os.path.splitext(teximage_node.image.name)
            if ext not in ['', '.dds']:
                self.error.fatal(f"Input {texture_name} in material {material.name} on object {referencing_object.name} is '{teximage_node.image.name}', which is not a DDS file.\n"
                                 f"Yakuza cannot handle these. Please change it to be a .dds file.")

            if not image_name:
                self.error.fatal(f"Material {material.name}.{texture_name} filepath {teximage_node.image.filepath} couldn't be parsed correctly.")

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

        # TODO - Add a check for "missing expected texture". Put "expected textures" in Material Yakuza Data, and compare against provided in the node.
        # TODO - image nodes will null textures exist - those currently break the export

        attribute_set = GMDAttributeSet(
            shader=shader,

            texture_diffuse=get_texture("texture_diffuse"),
            texture_refl=get_texture("texture_refl"),
            texture_multi=get_texture("texture_multi"),
            texture_unk1=get_texture("texture_unk1"),
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


class SkinnedBoneMatrixOrigin(Enum):
    # Calculate bone matrices directly
    Calculate = 0
    # Take the bone matrices from the file we're exporting over
    FromTargetFile = 1
    # Take the bone matrices from the per-bone Yakuza Hierarchy Node Data
    # (the entire skeleton must have been imported from another GMD!)
    FromCurrentSkeleton = 2
    

class SkinnedGMDSceneGatherer(BaseGMDSceneGatherer):
    bone_matrix_origin: SkinnedBoneMatrixOrigin
    bone_name_map: Dict[str, GMDBone]

    def __init__(self, filepath: str, original_scene: GMDScene, config: GMDSceneGathererConfig, bone_matrix_origin: SkinnedBoneMatrixOrigin, error: ErrorReporter):
        super().__init__(filepath, original_scene, config, error)

        self.bone_matrix_origin = bone_matrix_origin
        self.bone_name_map = {}

    def detect_export_armature_collection(self, context: bpy.types.Context) -> Tuple[bpy.types.Armature, bpy.types.Collection]:
        # Check we're selecting a correct armature
        # Find armature - should only be one, and should be named {name}_armature (see common for expected name)
        selected_armature = context.view_layer.objects.active

        if not selected_armature or selected_armature.type != "ARMATURE":
            self.error.fatal(f"Please select the armature for the skinned file you want to export!")

        if selected_armature.parent:
            self.error.fatal(f"The file armature should not have a parent.")

        if selected_armature.matrix_world != Matrix.Identity(4):
            self.error.fatal(
                f"Selected armature {selected_armature.name} should be at the origin (0, 0, 0), and must not be rotated or scaled!")

        self.error.info(f"Selected armature {selected_armature.name}")

        return selected_armature, super().detect_export_collection(context)

    def gather_exported_items(self, context: bpy.types.Context):
        selected_armature, selected_collection = self.detect_export_armature_collection(context)

        armature_data = cast(bpy.types.Armature, selected_armature.data)
        old_pose_position = armature_data.pose_position
        if old_pose_position != "REST":
            armature_data.pose_position = "REST"

        if self.bone_matrix_origin == SkinnedBoneMatrixOrigin.FromTargetFile:
            self.copy_bones_from_target(armature_data)
        elif self.bone_matrix_origin == SkinnedBoneMatrixOrigin.FromCurrentSkeleton:
            self.load_bones_from_blender(armature_data, True)
        else:
            self.load_bones_from_blender(armature_data, False)

        # Once an armature has been chosen, find the un/skinned objects
        root_skinned_objects: List[bpy.types.Object] = []

        # Go through all objects at the top level of the collection
        for object in selected_collection.objects:
            if object.type != "MESH":
                continue

            if object.parent:
                self.error.debug("GATHER", f"Skipping object {object.name} because parent")
                continue

            # Unparented objects
            # with vertex groups or an Armature modifier => warning. TODO - a "lenient mode" could try and work this into the hierarchy
            # with no object child-of modifier => unskinned root
            # with a child-of modifier
            # for the expected skeleton => unskinned child
            # for a different skeleton => error

            armature_modifiers = [m for m in object.modifiers if m.type == "ARMATURE"]
            if armature_modifiers:
                self.error.fatal(f"Mesh {object.name} has an armature modifier, but it isn't parented to the armature.")

            if object.vertex_groups:
                # This is recoverable, because sometimes if you're converting a skinned -> unskinned (i.e. majima as a baseball bat) then you don't want to go through deleting vertex groups.
                self.error.info(
                    f"Mesh {object.name} has vertex groups, but it isn't parented to the armature. Exporting as an unskinned mesh.")

            self.error.recoverable(
                f"Mesh {object.name} is not parented, so isn't skinned. This exporter doesn't support unskinned meshes. It may support it in v0.4.")

        for object in selected_armature.children:
            if object.type != "MESH":
                continue

            if object.parent != selected_armature:
                self.error.debug("GATHER",
                                 f"Skipping object {object.name} because parent not equal to {selected_armature.name}")
                continue

            # Objects parented to the armature
            # with both vertex groups and an Armature modifier => skinned root
            # with either vertex groups or an Armature modifier => warning
            # skinned root only if vertex groups present
            # with neither => unskinned object?
            # do same child-of check? not for now

            armature_modifiers = [m for m in object.modifiers if m.type == "ARMATURE"]
            if armature_modifiers and object.vertex_groups:
                root_skinned_objects.append(object)
            elif armature_modifiers and not object.vertex_groups:
                self.error.fatal(
                    f"Mesh {object.name} is a child of the skeleton, but it doesn't have any vertex groups.")
            elif object.vertex_groups and not armature_modifiers:
                self.error.info(
                    f"Mesh {object.name} is a child of the skeleton, but it doesn't have an armature modifier!\nIt will still be exported")
                # TODO - only do this if .lenient?
                root_skinned_objects.append(object)

        for skinned_object in root_skinned_objects:
            if skinned_object.children:
                self.error.recoverable(
                    f"Mesh {skinned_object.name} is skinned, but it has children. These children will not be exported.")

        # Then go through the rest of the scene, and check?
        # Not for now
        # if object has child-of for our armature => warning??

        for skinned_object in root_skinned_objects:
            self.export_skinned_object(context, skinned_object)

        self.error.debug("GATHER", f"NODE REPORT")
        for node in depth_first_iterate(self.node_roots):
            self.error.debug("GATHER", f"{node.name} - {node.node_type}")

        if self.config.debug_compare_matrices:
            self.error.debug("GATHER", f"MATRIX COMPARISONS")
            for node in depth_first_iterate(self.node_roots):
                if node.name in self.original_scene.overall_hierarchy.elem_from_name:
                    self.error.debug("GATHER", f"{node.name} vs original scene")
                    self.error.debug("GATHER",
                                     f"Old Matrix\n{self.original_scene.overall_hierarchy.elem_from_name[node.name].matrix}")
                    self.error.debug("GATHER", f"New Matrix\n{node.matrix}")
                    self.error.debug("GATHER", "")

        armature_data.pose_position = old_pose_position

        pass

    def load_bones_from_blender(self, armature_data: bpy.types.Armature, use_previously_imported_matrix: bool):
        def add_bone(blender_bone: bpy.types.Bone, parent_gmd_bone: Optional[GMDBone] = None):
            # Generating bone matrices is more difficult, because when we set the head/tail in the import process
            # the blender matrix changes from the GMD version
            # matrix_local is relative to the armature, not the parent

            if use_previously_imported_matrix:
                if not blender_bone.yakuza_hierarchy_node_data.inited:
                    self.error.fatal(f"Blender bone {blender_bone.name} was not imported from a GMD, so I can't reuse an imported matrix."
                                     f"Try rerunning with Bone Matrices = Calculated")
                bone_matrix = blender_bone.yakuza_hierarchy_node_data.imported_matrix
                self.error.info(str(bone_matrix))
            else:
                # Calculate from scratch
                # TODO - calculate this better
                bone_matrix = Matrix.Translation(transform_position_gmd_to_blender(blender_bone.head_local))
                bone_matrix.resize_4x4()
            
            gmd_bone_pos, gmd_bone_axis, gmd_bone_scale = transform_blender_to_gmd(*blender_bone.matrix_local.decompose())
            # TODO - try to extract this mathematically instead of copying the one from the last import
            anim_axis = blender_bone.yakuza_hierarchy_node_data.anim_axis
            flags = json.loads(blender_bone.yakuza_hierarchy_node_data.flags_json)
            if len(flags) != 4 or any(not isinstance(x, int) for x in flags):
                self.error.fatal(f"bone {blender_bone.name} has invalid flags - must be a list of 4 integers")
            bone = GMDBone(
                name=remove_blender_duplicate(blender_bone.name),
                node_type=NodeType.MatrixTransform,
                parent=parent_gmd_bone,

                pos=gmd_bone_pos,
                rot=Quaternion(), # TODO - Is there a better way to handle this? Does the game react to this at all?
                scale=Vector((1,1,1)),

                world_pos=Vector((gmd_bone_pos.x, gmd_bone_pos.y, gmd_bone_pos.z, 1)),
                anim_axis=anim_axis,
                flags=flags,
                matrix=bone_matrix.inverted()
            )

            if not parent_gmd_bone:
                self.node_roots.append(bone)
            self.bone_name_map[bone.name] = bone

            for child in blender_bone.children:
                add_bone(child, bone)

        # Build a GMDNode structure for the armature only (objects will be added to this later)
        for root_bone in armature_data.bones:
            if root_bone.parent:
                continue
            add_bone(root_bone, None)

    def copy_bones_from_target(self, armature_data: bpy.types.Armature):
        original_root_bones = [b for b in self.original_scene.overall_hierarchy.roots if isinstance(b, GMDBone)]

        def check_bone_sets_match(parent_name: str, blender_bones: List[bpy.types.Bone], gmd_bones: List[GMDBone]):
            blender_bone_dict = {x.name:x for x in blender_bones}
            gmd_bone_dict = {x.name:x for x in gmd_bones}
            if blender_bone_dict.keys() != gmd_bone_dict.keys():
                blender_bone_names = set(blender_bone_dict.keys())
                gmd_bone_names = set(gmd_bone_dict.keys())
                missing_names = gmd_bone_names - blender_bone_names
                unexpected_names = blender_bone_names - gmd_bone_names
                self.error.fatal(f"Bones under {parent_name} didn't match between the file and the Blender object. Missing {missing_names}, and found unexpected names {unexpected_names}")
            for (name, gmd_bone) in gmd_bone_dict.items():
                blender_bone = blender_bone_dict[name]
                check_bone_sets_match(name, blender_bone.children, [b for b in gmd_bone.children if isinstance(b, GMDBone)])

        check_bone_sets_match("root",
                              [b for b in armature_data.bones if not b.parent],
                              original_root_bones)

        def copy_bone(original_file_gmd_bone: GMDBone, new_gmd_parent: Optional[GMDBone] = None):
            bone = GMDBone(
                name=remove_blender_duplicate(original_file_gmd_bone.name),
                node_type=NodeType.MatrixTransform,
                parent=new_gmd_parent,

                pos=original_file_gmd_bone.pos,
                rot=original_file_gmd_bone.rot,
                scale=original_file_gmd_bone.scale,

                world_pos=original_file_gmd_bone.world_pos,
                anim_axis=original_file_gmd_bone.anim_axis,
                flags=original_file_gmd_bone.flags,

                matrix=original_file_gmd_bone.matrix
            )
            if not new_gmd_parent:
                self.node_roots.append(bone)
            self.bone_name_map[bone.name] = bone

            for child in original_file_gmd_bone.children:
                if not isinstance(child, GMDBone):
                    continue
                copy_bone(child, bone)

        for root_bone in original_root_bones:
            copy_bone(root_bone, None)

    def export_skinned_object(self, context: bpy.types.Context, object: bpy.types.Object):
        """
        Export a Blender object into a GMDSkinnedObject
        :param object: TODO
        :return: TODO
        """

        flags = json.loads(object.yakuza_hierarchy_node_data.flags_json)
        if len(flags) != 4 or any(not isinstance(x, int) for x in flags):
            self.error.fatal(f"bone {object.name} has invalid flags - must be a list of 4 integers")
        gmd_object = GMDSkinnedObject(
            name=remove_blender_duplicate(object.name),
            node_type=NodeType.SkinnedMesh,

            pos=Vector((0,0,0)),
            rot=Quaternion(),
            scale=Vector((1,1,1)),
            parent=None,

            world_pos=Vector((0,0,0,1)),
            anim_axis=object.yakuza_hierarchy_node_data.anim_axis,
            flags=flags
        )
        self.node_roots.append(gmd_object)

        # Add meshes to object
        if not object.data.vertices:
            self.error.debug("MESH", f"Object {object.name} has no mesh")
        else:
            if not object.material_slots:
                self.error.fatal(f"Object {object.name} has no materials")
            attribute_sets = [self.blender_material_to_gmd_attribute_set(material_slot.material, object) for material_slot in object.material_slots]
            assumed_unskinned_attr_sets = [
                attr.shader.name
                for attr in attribute_sets
                if not attr.shader.assume_skinned
            ]
            # If the material doesn't use weight/bone storage, it's definitely impossible

            impossible_unskinned_attr_sets = [
                attr.shader.name
                for attr in attribute_sets
                if (not attr.shader.vertex_buffer_layout.weights_storage) or
                   (not attr.shader.vertex_buffer_layout.bones_storage)
            ]
            if len(impossible_unskinned_attr_sets) > 0:
                self.error.fatal(
                    f"Object {object.name} uses shaders {impossible_unskinned_attr_sets} which require it to be not-skinned.\n"
                    f"Try unparenting it from the skeleton, or changing to a different material."
                )
            if len(assumed_unskinned_attr_sets) > 0:
                self.error.fatal(
                    f"Object {object.name} uses shaders {assumed_unskinned_attr_sets} which *may* require it to be not-skinned.\n"
                    f"Try unparenting it from the skeleton, or changing to a different material.\n"
                    f"If you're absolutely sure that this material works for skinned meshes,"
                    f"check the 'Assume Skinned' box in the Yakuza Material Properties."
                )
            #bone_limit = -1 if (self.export_version == GMDVersion.Dragon) else 32
            gmd_meshes = split_skinned_blender_mesh_object(context, object, attribute_sets, self.bone_name_map, 32, self.error)
            for gmd_mesh in gmd_meshes:
                gmd_object.add_mesh(gmd_mesh)


class UnskinnedGMDSceneGatherer(BaseGMDSceneGatherer):
    try_copy_hierarchy: bool

    def __init__(self, filepath: str, original_scene: GMDScene, config: GMDSceneGathererConfig, error: ErrorReporter,
                 try_copy_hierarchy: bool):
        super().__init__(filepath, original_scene, config, error)

        self.try_copy_hierarchy = try_copy_hierarchy

    def gather_exported_items(self, context: bpy.types.Context):
        selected_object, selected_collection = self.detect_export_collection(context)

        # Stores a list of (parent node, blender object).

        roots: List[bpy.types.Object] = []

        # Go through all objects at the top level of the collection
        for object in selected_collection.objects:
            if object.type == "ARMATURE":
                self.error.recoverable(f"Found armature ({object}), it and all objects beneath it will be ignored.")

            if object.type not in ["MESH", "EMPTY"]:
                continue

            if object.parent:
                self.error.debug("GATHER", f"Skipping object {object.name} because parent")
                continue

            armature_modifiers = [m for m in object.modifiers if m.type == "ARMATURE"]
            if armature_modifiers:
                self.error.recoverable(f"Mesh {object.name} has an armature modifier, but it isn't parented to an armature. It may be exported incorrectly.")

            if object.type == "MESH" and object.vertex_groups:
                # This is recoverable, because sometimes if you're converting a skinned -> unskinned (i.e. majima as a baseball bat) then you don't want to go through deleting vertex groups.
                self.error.info(
                    f"Mesh {object.name} has vertex groups, but it isn't parented to the armature. Exporting as an unskinned mesh.")

            roots.append(object)

        for parent, unskinned_object in roots:
            self.export_unskinned_object(context, selected_collection, unskinned_object, parent)

        self.error.debug("GATHER", f"NODE REPORT")
        for node in depth_first_iterate(self.node_roots):
            self.error.debug("GATHER", f"{node.name} - {node.node_type}")

        if self.config.debug_compare_matrices:
            self.error.debug("GATHER", f"MATRIX COMPARISONS")
            for node in depth_first_iterate(self.node_roots):
                if node.name in self.original_scene.overall_hierarchy.elem_from_name:
                    self.error.debug("GATHER", f"{node.name} vs original scene")
                    self.error.debug("GATHER",
                                     f"Old Matrix\n{self.original_scene.overall_hierarchy.elem_from_name[node.name].matrix}")
                    self.error.debug("GATHER", f"New Matrix\n{node.matrix}")
                    self.error.debug("GATHER", "")
        pass

    def export_unskinned_object(self, context: bpy.types.Context, collection: bpy.types.Collection, object: bpy.types.Object, parent: Optional[GMDNode]):
        """
        Export a Blender object into a GMDUnskinnedObject
        :param object: TODO
        :return: TODO
        """

        # pos, rot, scale are local
        adjusted_pos, adjusted_rot, adjusted_scale = transform_blender_to_gmd(object.location, object.rotation_quaternion, object.scale)
        inv_t = Matrix.Translation(-adjusted_pos)
        inv_r = adjusted_rot.inverted().to_matrix().to_4x4()
        inv_s = Matrix.Diagonal(Vector((1 / adjusted_scale.x, 1 / adjusted_scale.y, 1 / adjusted_scale.z))).to_4x4()
        parent_mat = parent.matrix if parent is not None else Matrix.Identity(4)
        adjusted_matrix = (inv_s @ inv_r @ inv_t @ parent_mat)

        world_pos = parent_mat.inverted_safe() @ adjusted_pos.to_3d()
        anim_axis = object.yakuza_hierarchy_node_data.anim_axis
        flags = json.loads(object.yakuza_hierarchy_node_data.flags_json)
        if len(flags) != 4 or any(not isinstance(x, int) for x in flags):
            self.error.fatal(f"bone {object.name} has invalid flags - must be a list of 4 integers")

        # if object.type == "EMPTY":

        gmd_object = GMDUnskinnedObject(
            name=remove_blender_duplicate(object.name),
            node_type=NodeType.UnskinnedMesh,

            pos=adjusted_pos,
            rot=adjusted_rot,
            scale=adjusted_scale,
            parent=parent,

            world_pos=world_pos,
            anim_axis=anim_axis,
            flags=flags,

            matrix=adjusted_matrix
        )
        if not parent:
            self.node_roots.append(gmd_object)

        # Add meshes to gmd_object
        if not object.data.vertices:
            self.error.debug("MESH", f"Object {object.name} has no mesh")
        else:
            if not object.material_slots:
                self.error.fatal(f"Object {object.name} has no materials")
            attribute_sets = [self.blender_material_to_gmd_attribute_set(material_slot.material, object) for material_slot in object.material_slots]
            if any(attr.shader.assume_skinned for attr in attribute_sets):
                self.error.fatal(f"Object {object.name} uses a material which *may* require it to be skinned.\n"
                                 f"Try parenting it to the skeleton using Ctrl P > Empty Weights, or changing to a different material.\n"
                                 f"If you're absolutely sure that this material works for unskinned meshes,"
                                 f"uncheck the 'Assume Skinned' box in the Yakuza Material Properties.")
            gmd_meshes = split_unskinned_blender_mesh_object(context, object, attribute_sets, self.error)
            for gmd_mesh in gmd_meshes:
                gmd_object.add_mesh(gmd_mesh)

        # Object.children returns all children, not just direct descendants.
        direct_children = [o for o in collection.objects if o.parent == object]
        for child_object in direct_children:
            self.export_unskinned_object(context, collection, child_object, gmd_object)
