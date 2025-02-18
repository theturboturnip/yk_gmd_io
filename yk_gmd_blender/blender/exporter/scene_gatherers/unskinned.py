import json
from typing import Optional, Union, Tuple

import bpy
from bpy.types import ShaderNodeGroup
from mathutils import Matrix, Vector
from ...common import yakuza_hierarchy_node_data_sort_key
from ...coordinate_converter import transform_blender_to_gmd
from ..mesh.functions import split_unskinned_blender_mesh_object
from .base import BaseGMDSceneGatherer, remove_blender_duplicate, \
    GMDSceneGathererConfig
from ....gmdlib.abstract.gmd_scene import GMDScene, depth_first_iterate
from ....gmdlib.abstract.nodes.gmd_bone import GMDBone
from ....gmdlib.abstract.nodes.gmd_object import GMDUnskinnedObject
from ....gmdlib.errors.error_classes import GMDImportExportError
from ....gmdlib.errors.error_reporter import ErrorReporter
from ....gmdlib.structure.common.node import NodeType


class UnskinnedGMDSceneGatherer(BaseGMDSceneGatherer):
    try_copy_hierarchy: bool

    def __init__(self, filepath: str, original_scene: GMDScene, config: GMDSceneGathererConfig, error: ErrorReporter,
                 try_copy_hierarchy: bool):
        super().__init__(filepath, original_scene, config, error)

        self.try_copy_hierarchy = try_copy_hierarchy

    def detect_export_collection(self, context: bpy.types.Context) -> Tuple[bpy.types.Object, bpy.types.Collection]:
        scene_root, collection = super().detect_export_collection(context)

        if scene_root.yakuza_file_root_data.is_valid_root \
                and scene_root.yakuza_file_root_data.import_mode != "UNSKINNED":
            if scene_root.yakuza_file_root_data.import_mode == "SKINNED":
                self.error.recoverable("File was imported in skinned mode, can't export as unskinned.\n"
                                       "Try exporting in skinned mode.")
            elif scene_root.yakuza_file_root_data.import_mode == "ANIMATION":
                self.error.recoverable("File was imported in animation mode, export will likely go wrong.\n"
                                       "Disable Strict Export if you really know what you're doing.")
            else:
                self.error.info("File root data wasn't marked as unskinned, export may go wrong.")

        return scene_root, collection

    def gather_exported_items(self, context: bpy.types.Context):
        scene_root, selected_collection = self.detect_export_collection(context)
        self.guess_or_take_flags(scene_root.yakuza_file_root_data)

        if remove_blender_duplicate(scene_root.name) != remove_blender_duplicate(selected_collection.name):
            self.error.fatal(f"Please select the root object of the collection, "
                             f"which should have the same name as the collection. "
                             f"Right now, the selected object '{scene_root.name}' doesn't have the same name "
                             f"as the collection '{selected_collection.name}'")
        if scene_root.parent is not None:
            self.error.fatal(f"Please select the root object of the collection, "
                             f"which should have the same name as the collection. "
                             f"Right now, the selected object has a parent and is not at the root of the collection")

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
                self.error.recoverable(
                    f"Mesh {object.name} has an armature modifier, but it isn't parented to an armature. "
                    f"It may be exported incorrectly.")

            if object.type == "MESH" and object.vertex_groups:
                # This is recoverable, because sometimes if you're converting a skinned -> unskinned
                # (i.e. majima as a baseball bat) then you don't want to go through deleting vertex groups.
                self.error.info(
                    f"Mesh {object.name} has vertex groups, but it isn't parented to the armature. "
                    f"Exporting as an unskinned mesh.")

        # Export each child of the scene root
        # Export unskinned object roots in order
        for unskinned_object in sorted(scene_root.children, key=yakuza_hierarchy_node_data_sort_key):
            self.export_unskinned_object(context, selected_collection, unskinned_object, None)

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
        pass

    def export_unskinned_object(self, context: bpy.types.Context, collection: bpy.types.Collection,
                                object: bpy.types.Object, parent: Optional[Union[GMDBone, GMDUnskinnedObject]]):
        """
        Export a Blender object into a GMDUnskinnedObject, adding it to the node_roots list or appending
        it to its parent's `children` list.

        :param context: Blender context
        :param collection: Blender collection containing the scene to export
        :param object: Blender object to export
        :param parent: The GMD node for the object's parent, if it has one
        """

        # pos, rot, scale are local
        adjusted_pos, adjusted_rot, adjusted_scale = transform_blender_to_gmd(object.location,
                                                                              object.rotation_quaternion, object.scale)
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

        gmd_object: Union[GMDUnskinnedObject, GMDBone]
        if object.type == "MESH":  # and object.data.vertices:
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

                matrix=adjusted_matrix,

                bbox=self.gmd_bounding_box(object)
            )
            if object.data.vertices:
                if not object.material_slots:
                    self.error.fatal(f"Object {object.name} has no materials")
                attribute_sets = [self.blender_material_to_gmd_attribute_set(material_slot.material, object) for
                                  material_slot in object.material_slots]
                if any(attr.shader.assume_skinned for attr in attribute_sets):
                    self.error.fatal(f"Object {object.name} uses a material which *may* require it to be skinned.\n"
                                     f"Try parenting it to the skeleton using Ctrl P > Empty Weights, "
                                     f"or changing to a different material.\n"
                                     f"If you're absolutely sure that this material works for unskinned meshes,"
                                     f"uncheck the 'Assume Skinned' box in the Yakuza Material Properties.")
                try:
                    gmd_meshes = split_unskinned_blender_mesh_object(context, object, attribute_sets, self.error)
                    for gmd_mesh in gmd_meshes:
                        gmd_object.add_mesh(gmd_mesh)
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
            else:
                self.error.info(f"Object {object.name} is a mesh with no vertices - exporting as GMDUnskinnedObject")
        else:
            self.error.debug("MESH", f"Object {object.name} of type {object.type} has no mesh, exporting as empty")
            gmd_object = GMDBone(
                name=remove_blender_duplicate(object.name),
                node_type=NodeType.MatrixTransform,

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

        # Object.children returns all children, not just direct descendants.
        direct_children = [o for o in collection.objects if o.parent == object]
        # In-place sort by key - export unskinned object children in order
        direct_children.sort(key=yakuza_hierarchy_node_data_sort_key)
        for child_object in direct_children:
            self.export_unskinned_object(context, collection, child_object, gmd_object)
