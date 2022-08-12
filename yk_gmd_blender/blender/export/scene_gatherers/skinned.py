import json
from enum import Enum
from typing import List, Dict, Optional, cast, Tuple

import bpy
from bpy.types import ShaderNodeGroup
from mathutils import Matrix, Vector, Quaternion
from yk_gmd_blender.blender.common import yakuza_hierarchy_node_data_sort_key, GMDGame, is_gmd_node_a_phys_bone, \
    generate_padding_bone_name
from yk_gmd_blender.blender.coordinate_converter import transform_position_blender_to_gmd, \
    transform_rotation_blender_to_gmd
from yk_gmd_blender.blender.export.mesh_exporter.functions import split_skinned_blender_mesh_object
from yk_gmd_blender.blender.export.scene_gatherers.base import BaseGMDSceneGatherer, remove_blender_duplicate, \
    GMDSceneGathererConfig
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene, depth_first_iterate, HierarchyData
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_object import GMDSkinnedObject
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType


class SkinnedBoneMatrixOrigin(Enum):
    # Calculate bone matrices directly
    Calculate = 0
    # Take the bone matrices from the file we're exporting over
    FromTargetFile = 1
    # Take the bone matrices from the per-bone Yakuza Hierarchy Node Data
    # (the entire skeleton must have been imported from another GMD!)
    FromOriginalGMDImport = 2


class SkinnedGMDSceneGatherer(BaseGMDSceneGatherer):
    bone_matrix_origin: SkinnedBoneMatrixOrigin
    bone_name_map: Dict[str, GMDBone]

    def __init__(self, filepath: str, original_scene: GMDScene, config: GMDSceneGathererConfig,
                 bone_matrix_origin: SkinnedBoneMatrixOrigin, error: ErrorReporter):
        super().__init__(filepath, original_scene, config, error)

        self.bone_matrix_origin = bone_matrix_origin
        self.bone_name_map = {}

    def detect_export_armature_collection(self, context: bpy.types.Context) \
            -> Tuple[bpy.types.Object, bpy.types.Collection]:
        # Check we're selecting a correct armature
        # Find armature - should only be one, and should be named {name}_armature (see common for expected name)
        selected_armature, selected_collection = super().detect_export_collection(context)

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
            self.check_bones_match_target(armature_data)
        self.generate_bones(armature_data)

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
        for node in depth_first_iterate(self.node_roots):
            self.error.debug("GATHER", f"{node.name} - {node.node_type}")

        if self.config.debug_compare_matrices:
            self.error.debug("GATHER", f"MATRIX COMPARISONS")
            for node in depth_first_iterate(self.node_roots):
                if node.name in self.original_scene.overall_hierarchy.elem_from_name:
                    self.error.debug("GATHER", f"{node.name} vs original scene")
                    self.error.debug("GATHER",
                                     f"Old Matrix\n"
                                     f"{self.original_scene.overall_hierarchy.elem_from_name[node.name].matrix}")
                    self.error.debug("GATHER", f"New Matrix\n{node.matrix}")
                    self.error.debug("GATHER", "")

        armature_data.pose_position = old_pose_position

        pass

    def generate_gmd_bone_for_blender(self, blender_bone: bpy.types.Bone,
                                      target_file_gmd_bone: Optional[GMDBone],
                                      parent_gmd_bone: Optional[GMDBone]) -> GMDBone:
        """
        Given a Blender bone, generate a GMD Bone (including the matrix if necessary).
        
        
        :param blender_bone: 
        :param target_file_gmd_bone: If the target file had a bone with the same name and parentage, that bone is passed as a paramter.
        :param parent_gmd_bone: 
        :return: 
        """

        if self.bone_matrix_origin == SkinnedBoneMatrixOrigin.FromTargetFile:
            assert target_file_gmd_bone
            return GMDBone(
                name=target_file_gmd_bone.name,
                node_type=NodeType.MatrixTransform,
                parent=parent_gmd_bone,

                pos=target_file_gmd_bone.pos,
                rot=target_file_gmd_bone.rot,
                scale=target_file_gmd_bone.scale,

                world_pos=target_file_gmd_bone.world_pos,
                anim_axis=target_file_gmd_bone.anim_axis,
                flags=target_file_gmd_bone.flags,

                matrix=target_file_gmd_bone.matrix
            )
        else:
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

            if self.bone_matrix_origin == SkinnedBoneMatrixOrigin.FromOriginalGMDImport:
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
                assert self.bone_matrix_origin == SkinnedBoneMatrixOrigin.Calculate
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
            return GMDBone(
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

    def generate_bones(self, armature_data: bpy.types.Armature):
        """
        Generates the GMDBones from a Blender armature.
        Overwrites self.node_roots and self.bone_name_map instead of returning.

        :param armature_data:
        :return:
        """

        bone_roots = []
        internal_bone_name_map: Dict[str, GMDBone] = {}

        def lookup_target_bone(name: str, target_file_possible_parents: List[GMDNode]) -> Optional[GMDBone]:
            for bone in target_file_possible_parents:
                if bone.name == name and isinstance(bone, GMDBone):
                    return bone
            return None

        def add_bone(blender_bone: bpy.types.Bone, target_file_gmd_bone: Optional[GMDBone],
                     parent_gmd_bone: Optional[GMDBone]):
            gmd_bone = self.generate_gmd_bone_for_blender(blender_bone, target_file_gmd_bone, parent_gmd_bone)

            if not parent_gmd_bone:
                bone_roots.append(gmd_bone)
            internal_bone_name_map[gmd_bone.name] = gmd_bone

            # Export bone children in order
            for child in sorted(blender_bone.children, key=yakuza_hierarchy_node_data_sort_key):
                add_bone(
                    child,
                    lookup_target_bone(child.name, target_file_gmd_bone.children if target_file_gmd_bone else []),
                    gmd_bone
                )

        # Build a GMDNode structure for the armature only (objects will be added to this later)

        # Grab the original bones in case we need them
        original_root_bones = [b for b in self.original_scene.overall_hierarchy.roots if isinstance(b, GMDBone)]

        # Export root bones in order
        for root_bone in sorted(armature_data.bones, key=yakuza_hierarchy_node_data_sort_key):
            if root_bone.parent:
                continue
            add_bone(root_bone, lookup_target_bone(root_bone.name, original_root_bones), None)

        # TODO: If dragon engine, check if phys bones are exported in the correct indices.
        #  if they aren't:
        #     1. sort phys bones by expected index
        #     2. assert the phys bones are in chains with a common parent
        #        i.e. either phys_bone[i].parent is a phys bone, or phys_bone[i].parent = X where X is the same for all i.
        #     3. reexport parent bones for X
        #     4. once you've exported X, export padding bones until you reach the expected phys_bones[0] index
        #     5. export all padding bones
        #     6. export all other bones (children of X, then children of X.parent, then children of X.parent.parent and so on)

        print(
            f"DEBUG special - {self.config.game} matches_engine {GMDGame.Engine_Dragon}? {self.config.game.matches_engine(GMDGame.Engine_Dragon)} ")
        if self.config.game.matches_engine(GMDGame.Engine_Dragon):
            old_phys_bone_indices: Dict[str, int] = {
                gmd_bone_old.name: i
                for i, gmd_bone_old in enumerate(self.original_scene.overall_hierarchy.depth_first_iterate())
                if is_gmd_node_a_phys_bone(gmd_bone_old)
            }
            new_phys_bone_indices: Dict[str, int] = {
                gmd_bone_new.name: i
                for i, gmd_bone_new in enumerate(HierarchyData(bone_roots).depth_first_iterate())
                if is_gmd_node_a_phys_bone(gmd_bone_new)
            }

            print(old_phys_bone_indices)
            print(new_phys_bone_indices)

            if set(old_phys_bone_indices.keys()) != set(new_phys_bone_indices.keys()):
                self.error.recoverable(f"Adding or removing phys bones - ")  # TODO better error message

            if old_phys_bone_indices != new_phys_bone_indices:
                print("DEBUG special - phys bones in different indices")
                # The same bones are present in different places
                old_phys_bone_indices_set = set(old_phys_bone_indices.values())
                contiguous_old_phys_bone_indices_set = set(
                    range(min(old_phys_bone_indices.values()), max(old_phys_bone_indices.values()) + 1))

                print(old_phys_bone_indices_set)
                print(contiguous_old_phys_bone_indices_set)

                # TODO - YK2 kiryu has phys bones on his feet, arms?, *and* jacket
                #   Assumption that all are contiguous is faulty
                phys_are_contiguous = old_phys_bone_indices_set == contiguous_old_phys_bone_indices_set

                if phys_are_contiguous:
                    # TODO ensure that the parentage for the new bones is the same as the old ones
                    print("DEBUG special phys_are_contiguous")

                    phys_chain_starts = []
                    for phys_bone_name in new_phys_bone_indices.keys():
                        gmd_bone_new = internal_bone_name_map[phys_bone_name]
                        # If the bone doesn't have a parent, or its parent is not a phys bone, it's the start of a chain
                        if not gmd_bone_new.parent or (gmd_bone_new.parent.name not in new_phys_bone_indices):
                            phys_chain_starts.append(gmd_bone_new)
                    assert len(phys_chain_starts) > 0

                    # Assume they all have the same parent
                    if all((p.parent == phys_chain_starts[0].parent) for p in phys_chain_starts):
                        # Find the chain of bones that leads to the common parent
                        parent_chain = []
                        parent_chain_bone = phys_chain_starts[0].parent
                        while parent_chain_bone is not None:
                            parent_chain.append(parent_chain_bone)
                            parent_chain_bone = parent_chain_bone.parent
                        # Reverse the parent chain so the top of the chain is first
                        parent_chain = list(reversed(parent_chain))

                        # Create a new bone hierarchy from the existing bones
                        recreated_bone_roots = []
                        recreated_internal_bone_name_map = {}

                        extra_bone_i = 0

                        def gen_pad_bone(parent: Optional[GMDBone]) -> GMDBone:
                            nonlocal extra_bone_i, recreated_internal_bone_name_map
                            extra_bone_i += 1
                            bone = GMDBone(
                                name=generate_padding_bone_name(extra_bone_i),
                                node_type=NodeType.MatrixTransform,
                                parent=parent,

                                pos=Vector((0, 0, 0)),
                                rot=Quaternion(),
                                scale=Vector((1, 1, 1)),

                                world_pos=parent.world_pos if parent else Vector((0, 0, 0)),
                                anim_axis=Vector((0, 0, 0, 0)),
                                flags=[0, 0, 0, 0],
                                matrix=parent.matrix if parent else Matrix.Identity(4)
                            )
                            assert bone.name not in recreated_internal_bone_name_map
                            recreated_internal_bone_name_map[bone.name] = bone
                            return bone

                        def gen_copy_of_bone(to_copy: GMDBone, new_parent: Optional[GMDBone]) -> GMDBone:
                            nonlocal recreated_internal_bone_name_map
                            bone = GMDBone(
                                name=to_copy.name,
                                node_type=NodeType.MatrixTransform,
                                parent=new_parent,

                                pos=to_copy.pos,
                                rot=to_copy.rot,
                                scale=to_copy.scale,

                                world_pos=to_copy.world_pos,
                                anim_axis=to_copy.anim_axis,
                                flags=to_copy.flags,
                                matrix=to_copy.matrix
                            )
                            assert bone.name not in recreated_internal_bone_name_map
                            recreated_internal_bone_name_map[bone.name] = bone
                            return bone

                        def recursive_gen_copy_of_bone(to_copy: GMDBone, new_parent: Optional[GMDBone]) -> GMDBone:
                            bone = gen_copy_of_bone(to_copy, new_parent)
                            for child_to_copy in to_copy.children:
                                assert isinstance(child_to_copy, GMDBone)
                                recursive_gen_copy_of_bone(child_to_copy, bone)
                            return bone

                        def recreate_phys_bone_chain_parent(base: GMDBone, new_parent: Optional[GMDBone]) -> GMDBone:
                            # First copy the base bone
                            bone = gen_copy_of_bone(base, new_parent)
                            # If we have a child in parent_chain, copy it first
                            had_child_in_parent_chain = False
                            for c in base.children:
                                assert isinstance(c, GMDBone)
                                if c in parent_chain:
                                    recreate_phys_bone_chain_parent(c, bone)
                                    had_child_in_parent_chain = True
                                    break

                            # If we didn't have a child in parent chain, we must have the phys_chain_starts
                            if not had_child_in_parent_chain:
                                assert all(phys_chain_start in base.children for phys_chain_start in phys_chain_starts)
                                # TODO: Find the current index of the current child
                                # We should have only created the elements of the parent chain by this point
                                assert len(recreated_internal_bone_name_map) == len(parent_chain)
                                current_dfs_index = len(parent_chain)
                                index_to_pad_to = min(old_phys_bone_indices.values())
                                assert index_to_pad_to > current_dfs_index
                                # Create a bunch of padding
                                for i in range(current_dfs_index, index_to_pad_to):
                                    gen_pad_bone(bone)
                                # Create those (TODO: Are they sorted correctly??)
                                for phys_chain_start in phys_chain_starts:
                                    recursive_gen_copy_of_bone(phys_chain_start, bone)
                            # Copy the rest
                            for c in base.children:
                                assert isinstance(c, GMDBone)
                                if c in parent_chain or c in phys_chain_starts:
                                    continue
                                recursive_gen_copy_of_bone(c, bone)
                            return bone

                        if parent_chain:
                            recreate_phys_bone_chain_parent(parent_chain[0], None)
                        # Create other bone roots
                        for base_root in bone_roots:
                            if base_root not in parent_chain:
                                recreated_bone_roots.append(recursive_gen_copy_of_bone(base_root, None))

                        self.node_roots = recreated_bone_roots
                        self.bone_name_map = recreated_internal_bone_name_map
                        return
                    else:
                        self.error.recoverable(f"Can't rearrange when phys chains don't share common parent")
                else:
                    self.error.fatal(f"Phys bones are being exported in the wrong place ")
        # All phys bones are in the right place
        self.node_roots = bone_roots
        self.bone_name_map = internal_bone_name_map

    def check_bones_match_target(self, armature_data: bpy.types.Armature):
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
            flags=flags
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
            # bone_limit = -1 if (self.export_version == GMDVersion.Dragon) else 32
            gmd_meshes = split_skinned_blender_mesh_object(context, object, attribute_sets, self.bone_name_map, 32,
                                                           self.error)
            for gmd_mesh in gmd_meshes:
                gmd_object.add_mesh(gmd_mesh)
