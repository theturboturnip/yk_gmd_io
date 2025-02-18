import json
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, cast, Tuple

import bpy
from bpy.types import ShaderNodeGroup
from mathutils import Matrix, Vector, Quaternion
from ...common import yakuza_hierarchy_node_data_sort_key
from ...coordinate_converter import transform_position_blender_to_gmd, \
    transform_rotation_blender_to_gmd
from ..mesh.functions import split_skinned_blender_mesh_object
from .base import BaseGMDSceneGatherer, remove_blender_duplicate, \
    GMDSceneGathererConfig
from ....gmdlib.abstract.gmd_scene import GMDScene, depth_first_iterate
from ....gmdlib.abstract.nodes.gmd_bone import GMDBone
from ....gmdlib.abstract.nodes.gmd_object import GMDSkinnedObject
from ....gmdlib.errors.error_classes import GMDImportExportError
from ....gmdlib.errors.error_reporter import ErrorReporter
from ....gmdlib.structure.common.node import NodeType


@dataclass(frozen=True)
class GMDSkinnedSceneGathererConfig(GMDSceneGathererConfig):
    # The maximum number of bones allowed per export.
    # Must be a positive integer.
    bone_limit: int

    def __post_init__(self):
        assert self.bone_limit > 0


class SkinnedBoneMatrixOrigin(Enum):
    # Calculate bone matrices directly
    Calculate = 0
    # Take the bone matrices from the file we're exporting over
    FromTargetFile = 1
    # Take the bone matrices from the per-bone Yakuza Hierarchy Node Data
    # (the entire skeleton must have been imported from another GMD!)
    FromOriginalGMDImport = 2


class SkinnedGMDSceneGatherer(BaseGMDSceneGatherer):
    config: GMDSkinnedSceneGathererConfig
    bone_matrix_origin: SkinnedBoneMatrixOrigin
    bone_name_map: Dict[str, GMDBone]

    def __init__(self, filepath: str, original_scene: GMDScene, config: GMDSkinnedSceneGathererConfig,
                 bone_matrix_origin: SkinnedBoneMatrixOrigin, error: ErrorReporter):
        super().__init__(filepath, original_scene, config, error)

        self.bone_matrix_origin = bone_matrix_origin
        self.bone_name_map = {}

    def detect_export_armature_collection(self, context: bpy.types.Context) \
            -> Tuple[bpy.types.Object, bpy.types.Collection]:
        # Check we're selecting a correct armature
        # Find armature - should only be one, and should be named {name}_armature (see common for expected name)
        selected_armature, selected_collection = super().detect_export_collection(context)

        if selected_armature.yakuza_file_root_data.is_valid_root \
                and selected_armature.yakuza_file_root_data.import_mode != "SKINNED":
            if selected_armature.yakuza_file_root_data.import_mode == "UNSKINNED":
                self.error.recoverable("File was imported in unskinned mode, can't export as skinned.\n"
                                       "Try exporting in unskinned mode.")
            elif selected_armature.yakuza_file_root_data.import_mode == "ANIMATION":
                self.error.recoverable("File was imported in animation mode, export will likely go wrong.\n"
                                       "Disable Strict Export if you really know what you're doing.")
            else:
                self.error.info("File root data wasn't marked as skinned, export may go wrong.")

        if not selected_armature or selected_armature.type != "ARMATURE":
            self.error.fatal(f"Please select the armature for the skinned file you want to export!")

        if selected_armature.parent:
            self.error.fatal(f"The file armature should not have a parent.")

        if selected_armature.matrix_world != Matrix.Identity(4):
            self.error.fatal(
                f"Selected armature {selected_armature.name} should be at the origin (0, 0, 0), "
                f"and must not be rotated or scaled!")

        self.error.info(f"Selected armature {selected_armature.name}")

        return selected_armature, selected_collection

    def gather_exported_items(self, context: bpy.types.Context):
        selected_armature, selected_collection = self.detect_export_armature_collection(context)
        self.guess_or_take_flags(selected_armature.yakuza_file_root_data)

        armature_data = cast(bpy.types.Armature, selected_armature.data)
        old_pose_position = armature_data.pose_position
        if old_pose_position != "REST":
            armature_data.pose_position = "REST"

        if self.bone_matrix_origin == SkinnedBoneMatrixOrigin.FromTargetFile:
            self.copy_bones_from_target(armature_data)
        elif self.bone_matrix_origin == SkinnedBoneMatrixOrigin.FromOriginalGMDImport:
            self.load_bones_from_blender(armature_data, use_previously_imported_matrix=True)
        elif self.bone_matrix_origin == SkinnedBoneMatrixOrigin.Calculate:
            self.load_bones_from_blender(armature_data, use_previously_imported_matrix=False)

        # Once an armature has been chosen, find the un/skinned objects
        root_skinned_objects: List[bpy.types.Object] = []

        # Go through all objects at the top level of the collection and check them for errors
        # Don't need to sort them here
        for object in selected_collection.objects:
            if object.type != "MESH":
                continue

            if object.parent:
                self.error.debug("GATHER", f"Skipping object {object.name} because parent")
                continue

            # Unparented objects
            # with vertex groups or an Armature modifier => warning.
            # with no object child-of modifier => unskinned root
            # with a child-of modifier
            # for the expected skeleton => unskinned child
            # for a different skeleton => error

            armature_modifiers = [m for m in object.modifiers if m.type == "ARMATURE"]
            if armature_modifiers:
                self.error.fatal(f"Mesh {object.name} has an armature modifier, but it isn't parented to the armature.")

            if object.vertex_groups:
                # This is recoverable, because sometimes if you're converting a skinned -> unskinned
                # (i.e. majima as a baseball bat) then you don't want to go through deleting vertex groups.
                self.error.info(
                    f"Mesh {object.name} has vertex groups, but it isn't parented to the armature. "
                    f"Exporting as an unskinned mesh.")

            self.error.recoverable(
                f"Mesh {object.name} is not parented, so isn't skinned. "
                f"This exporter doesn't support unskinned meshes.")

        # Go through the objects we're actually going to export
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
                    f"Mesh {object.name} is a child of the skeleton, but it doesn't have an armature modifier!\n"
                    f"It will still be exported")
                # TODO - only do this if .lenient?
                root_skinned_objects.append(object)

        # Export skinned objects in order
        for skinned_object in sorted(root_skinned_objects, key=yakuza_hierarchy_node_data_sort_key):
            if skinned_object.children:
                self.error.recoverable(
                    f"Mesh {skinned_object.name} is skinned, but it has children. These children will not be exported.")
            self.export_skinned_object(context, skinned_object)

        self.error.debug("GATHER", f"NODE REPORT")
        for _, node in depth_first_iterate(self.node_roots):
            self.error.debug("GATHER", f"{node.name} - {node.node_type}")

        if self.config.debug_compare_matrices:
            self.error.debug("GATHER", f"MATRIX COMPARISONS")
            for _, node in depth_first_iterate(self.node_roots):
                if node.name in self.original_scene.overall_hierarchy.elem_from_name:
                    self.error.debug("GATHER", f"{node.name} vs original scene")
                    self.error.debug("GATHER",
                                     f"Old Matrix\n"
                                     f"{self.original_scene.overall_hierarchy.elem_from_name[node.name].matrix}")
                    self.error.debug("GATHER", f"New Matrix\n{node.matrix}")
                    self.error.debug("GATHER", "")

        armature_data.pose_position = old_pose_position

        pass

    def load_bones_from_blender(self, armature_data: bpy.types.Armature, use_previously_imported_matrix: bool):
        def add_bone(blender_bone: bpy.types.Bone, parent_gmd_bone: Optional[GMDBone] = None):
            # Generating bone matrices is more difficult, because when we set the head/tail in the import process
            # the blender matrix changes from the GMD version
            # matrix_local is relative to the armature, not the parent

            # Blender is bad at naming things
            # blender_bone.head_local = local to *armature*, not parent bone
            # blender_bone.head = local to parent, but doesn't seem to work correctly
            # Work out the local position from the parent bone's matrix instead
            armature_rel_head = transform_position_blender_to_gmd(Vector(blender_bone.head_local))
            if parent_gmd_bone:
                parent_local_head = parent_gmd_bone.matrix @ armature_rel_head
            else:
                parent_local_head = armature_rel_head

            if blender_bone.yakuza_hierarchy_node_data.inited:
                gmd_local_rot = transform_rotation_blender_to_gmd(
                    blender_bone.yakuza_hierarchy_node_data.bone_local_rot
                )
            else:
                gmd_local_rot = Quaternion()

            if use_previously_imported_matrix:
                if not blender_bone.yakuza_hierarchy_node_data.inited:
                    self.error.fatal(
                        f"Blender bone {blender_bone.name} was not imported from a GMD, "
                        f"so I can't reuse an imported matrix."
                        f"Try rerunning with Bone Matrices = Calculated")
                matrix_columns = list(blender_bone.yakuza_hierarchy_node_data.imported_matrix)
                rows = (
                    (matrix_columns[0].x, matrix_columns[1].x, matrix_columns[2].x, matrix_columns[3].x),
                    (matrix_columns[0].y, matrix_columns[1].y, matrix_columns[2].y, matrix_columns[3].y),
                    (matrix_columns[0].z, matrix_columns[1].z, matrix_columns[2].z, matrix_columns[3].z),
                    (matrix_columns[0].w, matrix_columns[1].w, matrix_columns[2].w, matrix_columns[3].w),
                )
                bone_matrix = Matrix(rows)
            else:
                # Calculate from scratch
                inv_t = Matrix.Translation(-parent_local_head)
                inv_r = gmd_local_rot.inverted().to_matrix().to_4x4()
                # Bones cannot be scaled
                parent_mat = parent_gmd_bone.matrix if parent_gmd_bone else Matrix.Identity(4)
                bone_matrix = (inv_r @ inv_t @ parent_mat)

            # Can't extract this mathematically - have to take it from the last import
            # (defaults to (0,0,0,0) if not imported from a GMD)
            anim_axis = blender_bone.yakuza_hierarchy_node_data.anim_axis
            flags = json.loads(blender_bone.yakuza_hierarchy_node_data.flags_json)
            if len(flags) != 4 or any(not isinstance(x, int) for x in flags):
                self.error.fatal(f"bone {blender_bone.name} has invalid flags - must be a list of 4 integers")
            bone = GMDBone(
                # Don't remove duplicates here - they're namespaced within the armature, blender guarantees unique names
                # within the armature
                name=blender_bone.name,
                node_type=NodeType.MatrixTransform,
                parent=parent_gmd_bone,

                pos=parent_local_head,
                rot=gmd_local_rot,
                scale=Vector((1, 1, 1)),

                world_pos=Vector((armature_rel_head.x, armature_rel_head.y, armature_rel_head.z, 1)),
                anim_axis=anim_axis,
                flags=flags,
                matrix=bone_matrix
            )

            if not parent_gmd_bone:
                self.node_roots.append(bone)
            self.bone_name_map[bone.name] = bone

            # Export bone children in order
            for child in sorted(blender_bone.children, key=yakuza_hierarchy_node_data_sort_key):
                add_bone(child, bone)

        # Build a GMDNode structure for the armature only (objects will be added to this later)
        # Export root bones in order
        for root_bone in sorted(armature_data.bones, key=yakuza_hierarchy_node_data_sort_key):
            if root_bone.parent:
                continue
            add_bone(root_bone, None)

    def copy_bones_from_target(self, armature_data: bpy.types.Armature):
        original_root_bones = [b for b in self.original_scene.overall_hierarchy.roots if isinstance(b, GMDBone)]

        def check_bone_sets_match(parent_name: str, blender_bones: List[bpy.types.Bone], gmd_bones: List[GMDBone]):
            blender_bone_dict = {x.name: x for x in blender_bones}
            gmd_bone_dict = {x.name: x for x in gmd_bones}
            if blender_bone_dict.keys() != gmd_bone_dict.keys():
                blender_bone_names = set(blender_bone_dict.keys())
                gmd_bone_names = set(gmd_bone_dict.keys())
                missing_names = gmd_bone_names - blender_bone_names
                unexpected_names = blender_bone_names - gmd_bone_names
                self.error.fatal(
                    f"Bones under {parent_name} didn't match between the file and the Blender object. "
                    f"Missing {missing_names}, and found unexpected names {unexpected_names}")
            for (name, gmd_bone) in gmd_bone_dict.items():
                blender_bone = blender_bone_dict[name]
                check_bone_sets_match(name, blender_bone.children,
                                      [b for b in gmd_bone.children if isinstance(b, GMDBone)])

        check_bone_sets_match("root",
                              [b for b in armature_data.bones if not b.parent],
                              original_root_bones)

        def copy_bone(original_file_gmd_bone: GMDBone, new_gmd_parent: Optional[GMDBone] = None):
            bone = GMDBone(
                name=original_file_gmd_bone.name,
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
        Export a Blender object into a GMDSkinnedObject, adding it to the node_roots list.

        :param context: Blender context
        :param object: Blender object to export
        """

        flags = json.loads(object.yakuza_hierarchy_node_data.flags_json)
        if len(flags) != 4 or any(not isinstance(x, int) for x in flags):
            self.error.fatal(f"bone {object.name} has invalid flags - must be a list of 4 integers")
        gmd_object = GMDSkinnedObject(
            name=remove_blender_duplicate(object.name),
            node_type=NodeType.SkinnedMesh,

            pos=Vector((0, 0, 0)),
            rot=Quaternion(),
            scale=Vector((1, 1, 1)),
            parent=None,

            world_pos=Vector((0, 0, 0, 1)),
            anim_axis=object.yakuza_hierarchy_node_data.anim_axis,
            flags=flags,

            bbox=self.gmd_bounding_box(object)
        )
        self.node_roots.append(gmd_object)

        # Add meshes to object
        if not object.data.vertices:
            self.error.debug("MESH", f"Object {object.name} has no mesh")
        else:
            if not object.material_slots:
                self.error.fatal(f"Object {object.name} has no materials")
            attribute_sets = [self.blender_material_to_gmd_attribute_set(material_slot.material, object) for
                              material_slot in object.material_slots]
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
                    f"Object {object.name} uses shaders {impossible_unskinned_attr_sets} "
                    f"which require it to be not-skinned.\n"
                    f"Try unparenting it from the skeleton, or changing to a different material."
                )
            if len(assumed_unskinned_attr_sets) > 0:
                self.error.fatal(
                    f"Object {object.name} uses shaders {assumed_unskinned_attr_sets} "
                    f"which *may* require it to be not-skinned.\n"
                    f"Try unparenting it from the skeleton, or changing to a different material.\n"
                    f"If you're absolutely sure that this material works for skinned meshes,"
                    f"check the 'Assume Skinned' box in the Yakuza Material Properties."
                )
            try:
                gmd_meshes = split_skinned_blender_mesh_object(context, object, attribute_sets, self.bone_name_map,
                                                               self.config.bone_limit,
                                                               self.error)
            except GMDImportExportError:
                # Assume GMDImportExportErrors have enough context
                raise
            except Exception as err:
                # Raising a new RuntimeError (NOT a new GMDImportExportError) here makes blender show both
                # the old error and this new error. Combined, they should give enough context for people to
                # figure out where the problem in their meshes is
                # TODO `raise X from err` doesn't show `err` in Blender python console. If it ever does, use it here instead?
                raise RuntimeError(
                    f"Error handling meshes in {object.name_full}: {err}"
                )  # from err

            for gmd_mesh in gmd_meshes:
                gmd_object.add_mesh(gmd_mesh)
