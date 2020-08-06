import re
from typing import List, Union, Dict, Optional, cast, Tuple

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       CollectionProperty)
from bpy.types import Operator, ChildOfConstraint
from bpy_extras.io_utils import ExportHelper
from mathutils import Matrix, Vector, Quaternion

from yk_gmd_blender.blender.common import armature_name_for_gmd_file
from yk_gmd_blender.blender.coordinate_converter import transform_matrix_blender_to_gmd, transform_blender_to_gmd
from yk_gmd_blender.blender.error_reporter import BlenderErrorReporter
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene, HierarchyData, depth_first_iterate
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_object import GMDUnskinnedObject, GMDSkinnedObject
from yk_gmd_blender.yk_gmd.v2.errors.error_classes import GMDImportExportError
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import StrictErrorReporter, LenientErrorReporter, ErrorReporter
from yk_gmd_blender.yk_gmd.v2.io import get_file_header, check_version_writeable, write_abstract_scene_out, \
    read_gmd_structures, read_abstract_scene_from_filedata_object
from yk_gmd_blender.yk_gmd.v2.structure.common.header import GMDHeaderStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType

from yk_gmd_blender.yk_gmd.v2.structure.version import combine_versions

class ExportGMD(Operator, ExportHelper):
    """Export scene as glTF 2.0 file"""
    bl_idname = 'export_scene.gmd'
    bl_label = "Export Yakuza GMD (YK1)"

    filename_ext = ''

    filter_glob: StringProperty(default='*.gmd', options={'HIDDEN'})

    strict: BoolProperty(name="Strict File Export",
                         description="If True, will fail the export even on recoverable errors.",
                         default=True)
    copy_bones_from_file: BoolProperty(name="Copy Bones from Original File",
                                     description="If True, will reuse the bone hierarchy in the original file.\n"
                                                 "If False, will export the bones from scratch.\n"
                                                 "WARNING: This is experimental - don't set it to False unless you know what you're doing.",
                                     default=True)
    debug_compare_matrices: BoolProperty(name="[DEBUG] Compare Matrices",
                                         description="If True, will print out a comparison of the scene matrices (for bones and unskinned objects)\n"
                                         "between the original file and the new file.",
                                         default=False)
    # TODO - dry run feature
    #  when set, instead of exporting it will open a window with a report on what would be exported

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = True  # No animation.

        # When properties are added, use "layout.prop" here to display them
        layout.prop(self, 'strict')
        layout.prop(self, 'copy_bones_from_file')
        layout.prop(self, 'debug_compare_matrices')

    def execute(self, context):
        base_error_reporter = StrictErrorReporter() if self.strict else LenientErrorReporter()
        error_reporter = BlenderErrorReporter(self.report, base_error_reporter)

        try:
            version_props, file_data = read_gmd_structures(self.filepath, error_reporter)
            check_version_writeable(version_props, error_reporter)

            original_scene = GMDScene(
                name=file_data.name.text,
                overall_hierarchy=HierarchyData([])
            )
            try_copy_bones = self.copy_bones_from_file
            if self.copy_bones_from_file or self.debug_compare_matrices:
                try:
                    original_scene = read_abstract_scene_from_filedata_object(version_props, file_data, error_reporter)
                except Exception as e:
                    # TODO - error reporter.info
                    print(e)
                    self.report({"ERROR"}, f"Original file failed to import properly, can't check bone hierarchy\nError: {e}")
                    try_copy_bones = False

            scene_gatherer = GMDSceneGatherer(original_scene, try_copy_bones, error_reporter)
            self.report({"INFO"}, "Extracting blender data into abstract scene...")
            # TODO - pull GMDScene out of blender
            scene_gatherer.gather_exported_items(context, self.debug_compare_matrices)
            self.report({"INFO"}, "Finished extracting abstract scene")

            gmd_scene = scene_gatherer.build()

            self.report({"INFO"}, f"Writing scene out...")
            write_abstract_scene_out(version_props,
                                     file_data.file_is_big_endian(), file_data.vertices_are_big_endian(),
                                     gmd_scene,
                                     self.filepath,
                                     error_reporter)

            self.report({"INFO"}, f"Finished exporting {gmd_scene.name}")
            return {'FINISHED'}
        except GMDImportExportError as e:
            print(e)
            self.report({"ERROR"}, str(e))
        return {'CANCELLED'}


class GMDSceneGatherer:
    name: str
    original_scene: GMDScene
    node_roots: List[GMDNode]
    bone_name_map: Dict[str, GMDNode]
    error: ErrorReporter
    try_copy_bones: bool

    blender_to_gmd_space_matrix: Matrix

    def __init__(self, original_scene: GMDScene, try_copy_bones: bool, error: ErrorReporter):
        self.name = original_scene.name
        self.original_scene = original_scene
        self.node_roots = []
        self.bone_name_map = {}
        self.error = error
        self.try_copy_bones = try_copy_bones
        self.blender_to_gmd_space_matrix = Matrix((
            Vector((-1, 0, 0, 0)),
            Vector((0, 0, 1, 0)),
            Vector((0, 1, 0, 0)),
            Vector((0, 0, 0, 1)),
        ))

    def build(self) -> GMDScene:
        return GMDScene(
            name=self.name,
            overall_hierarchy=HierarchyData(self.node_roots)
        )

    def name_matches_expected(self, name, expected):
        # A "correct" name == {expected name}.XXX
        # To check this, split the string on expected name.
        # It will produce ['', ''] if the name is the same, or '', '.XXX' otherwise
        split_name = name.split(expected)
        if split_name == ['', '']:
            return True
        elif len(split_name) != 2 or split_name[0] != '' or not re.match(r'\.\d\d\d', split_name[1]):
            return False
        return True

    def remove_blender_duplicate(self, name:str) -> str:
        return re.sub(r'\.\d\d\d', "", name)

    def gather_exported_items(self, context: bpy.types.Context, debug_compare_matrices: bool):
        # Decide on an export root
            # Require a collection to be selected I guess?
            # Issue a warning if the name is different?

        # Find armature - should only be one, and should be named {name}_armature (see common for expected name)
        selected_armature = context.view_layer.objects.active
        # armature_objs = [object for object in collection.objects if object.type == "ARMATURE"]
        # if not armature_objs:
        #     self.error.fatal(f"No armature objects found in the collection - one must be present")
        # elif len(armature_objs) == 1:
        #     selected_armature = armature_objs[0]
        # else:
        #     # Mutliple armatures present, if only one of them fits the scene name then select that one
        #     expected_name = armature_name_for_gmd_file(self.name)
        #     matching_name_armature_objs = [object for object in armature_objs if self.name_matches_expected(object.name, expected_name)]
        #     if not matching_name_armature_objs:
        #         self.error.fatal(f"Multiple armature objects found ({[a.name for a in armature_objs]}), couldn't decide which to use.\n"
        #                          f"None of their names matched the scene name {self.name}.")
        #     elif len(matching_name_armature_objs) == 1:
        #         selected_armature = matching_name_armature_objs[0]
        #     else:
        #         self.error.fatal(
        #             f"Multiple armature objects found ({[a.name for a in armature_objs]}), couldn't decide which to use.\n"
        #             f"Many of their names ({[a.name for a in matching_name_armature_objs]}) matched the scene name {self.name}.")

        if not selected_armature or selected_armature.type != "ARMATURE":
            self.error.fatal(f"Please select the armature for the file you want to export!")

        if selected_armature.parent:
            self.error.fatal(f"The file armature should not have a parent.")

        # TODO - decide how to handle armatures that are not at the identity
        if selected_armature.matrix_world != Matrix.Identity(4):
            self.error.fatal(f"Selected armature {selected_armature.name} should be at the origin (0, 0, 0), and must not be rotated or scaled!")

        # TODO - add error.info?
        print(f"Selected armature {selected_armature.name}")

        # This is the list of all collections an object could be in, including nested ones.
        # i.e. the full chain Collection > scene_name_collection > object
        possible_collections: Tuple[bpy.types.Collection, ...] = context.view_layer.objects.active.users_collection
        # The selected collection is the one that has the armature as a root object
        selected_collection = None
        for collection in possible_collections:
            if selected_armature in list(collection.objects):
                selected_collection = collection
                break
        if not selected_collection:
            self.error.fatal(f"Can't figure out which collection the armature is a part of! This should never happen")

        if not self.name_matches_expected(selected_collection.name, self.name):
            # TODO - shouldn't be an error
            self.error.recoverable(f"Collection name {selected_collection.name} does not map to expected {self.name}!\n"
                                   f"Expected '{self.name}' or '{self.name}.XYZ'.")

        if selected_collection.children:
            self.error.recoverable(f"Collection {selected_collection.name} has children collections, which will be ignored.")

        armature_data = cast(bpy.types.Armature, selected_armature.data)
        old_pose_position = armature_data.pose_position
        if old_pose_position != "REST":
            armature_data.pose_position = "REST"

        if self.try_copy_bones:
            self.copy_bones_from_original(armature_data)
        else:
            self.load_bones_from_blender(armature_data)

        # Once an armature has been chosen, find the un/skinned objects
        root_skinned_objects: List[bpy.types.Object] = []
        # Stores a list of (parent node, blender object).
        # This is a list of unskinned roots, not a list of all of the unskinned objects.
        # i.e. if you have a hierarchy
        # unskinned object A
        # |--- unskinned object B
        # where B is a child of A, only A will be in this list, not B.
        unskinned_object_roots: List[Tuple[Optional[GMDNode], bpy.types.Object]] = []


        # Go through all objects at the top level of the collection
        for object in selected_collection.objects:
            if object.type != "MESH":
                continue

            if object.parent:
                print(f"Skipping object {object.name} because parent")
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
                # TODO - in that case, this would be better off as a .info
                self.error.recoverable(f"Mesh {object.name} has vertex groups, but it isn't parented to the armature. Exporting as an unskinned mesh.")

            child_of_constraints = [c for c in object.constraints if c.type == "CHILD_OF"]
            if not child_of_constraints:
                # Object is not parented to the armature, so it's an unskinned root
                unskinned_object_roots.append((None, object))
                continue
            elif len(child_of_constraints) > 1:
                self.error.fatal(f"Mesh {object.name} has multiple child of constraints!")
            else:
                child_of_constraint = cast(ChildOfConstraint, child_of_constraints[0])
                if child_of_constraint.target != selected_armature:
                    self.error.fatal(f"Mesh {object.name} is a Child Of a different skeleton! Change this in the Object Constraints tab.")
                if child_of_constraint.subtarget not in self.bone_name_map:
                    self.error.fatal(f"Mesh {object.name} is a Child Of the bone '{child_of_constraint.subtarget}' that doesn't exist in the skeleton!")

                # Object is a Child-Of an existing bone
                unskinned_object_roots.append((self.bone_name_map[child_of_constraint.subtarget], object))

        for object in selected_armature.children:
            if object.type != "MESH":
                continue

            if object.parent != selected_armature:
                print(f"Skipping object {object.name} because parent not equal to {selected_armature.name}")
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
                self.error.fatal(f"Mesh {object.name} is a child of the skeleton, but it doesn't have any vertex groups.")
            elif object.vertex_groups and not armature_modifiers:
                # TODO - .info
                self.error.recoverable(f"Mesh {object.name} is a child of the skeleton, but it doesn't have an armature modifier!")
                # TODO - only do this if .lenient?
                root_skinned_objects.append(object)
            else:
                # TODO - .info
                self.error.recoverable(f"Mesh {object.name} is a child of the skeleton, but it doesn't have an armature modifier or a vertex group! Exporting as an unskinned mesh")
                unskinned_object_roots.append((None, object))

        for skinned_object in root_skinned_objects:
            if skinned_object.children:
                self.error.recoverable(f"Mesh {skinned_object.name} is skinned, but it has children. These children will not be exported.")

        # Then go through the rest of the scene, and check?
        # Not for now
            # if object has child-of for our armature => warning??

        for skinned_object in root_skinned_objects:
            self.export_skinned_object(skinned_object)

        for parent, unskinned_object in unskinned_object_roots:
            self.export_unskinned_object(selected_collection, unskinned_object, parent)

        print(f"NODE REPORT")
        for node in depth_first_iterate(self.node_roots):
            print(f"{node.name} - {node.node_type}")

        if debug_compare_matrices:
            print(f"MATRIX COMPARISONS")
            for node in depth_first_iterate(self.node_roots):
                if node.name in self.original_scene.overall_hierarchy.elem_from_name:
                    print(f"{node.name} vs original scene")
                    print(f"Old Matrix\n{self.original_scene.overall_hierarchy.elem_from_name[node.name].matrix}")
                    print(f"New Matrix\n{node.matrix}")
                    print("")

        armature_data.pose_position = old_pose_position

        pass

    def load_bones_from_blender(self, armature_data: bpy.types.Armature):
        def add_bone(blender_bone: bpy.types.Bone, parent_gmd_bone: Optional[GMDBone] = None):
            # Generating bone matrices is more difficult, because when we set the head/tail in the import process the blender matrix changes from the GMD version
            # matrix_local is relative to the armature, not the parent
            bone_matrix = transform_matrix_blender_to_gmd(blender_bone.matrix_local)
            gmd_bone_pos, gmd_bone_axis, gmd_bone_scale = transform_blender_to_gmd(*blender_bone.matrix.decompose())
            bone = GMDBone(
                name=self.remove_blender_duplicate(blender_bone.name),
                node_type=NodeType.MatrixTransform,
                parent=parent_gmd_bone,

                pos=gmd_bone_pos,
                rot=Quaternion(), # TODO - Is there a better way to handle this? Does the game react to this at all?
                scale=Vector((1,1,1)),

                bone_pos=Vector((gmd_bone_pos.x, gmd_bone_pos.y, gmd_bone_pos.z, 1)),
                bone_axis=gmd_bone_axis, # TODO - Kiwmai1 format might be using this for flags? in which case including it could crash
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

    def copy_bones_from_original(self, armature_data: bpy.types.Armature):
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
                name=self.remove_blender_duplicate(original_file_gmd_bone.name),
                node_type=NodeType.MatrixTransform,
                parent=new_gmd_parent,

                pos=original_file_gmd_bone.pos,
                rot=original_file_gmd_bone.rot,
                scale=original_file_gmd_bone.scale,

                bone_pos=original_file_gmd_bone.bone_pos,
                bone_axis=original_file_gmd_bone.bone_axis,

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

    def export_skinned_object(self, object: bpy.types.Object):
        """
        Export a Blender object into a GMDSkinnedObject
        :param object: TODO
        :return: TODO
        """

        object = GMDSkinnedObject(
            name=self.remove_blender_duplicate(object.name),
            node_type=NodeType.SkinnedMesh,

            pos=Vector((0,0,0)),
            rot=Quaternion(),
            scale=Vector((1,1,1)),
            parent=None,
        )
        self.node_roots.append(object)

        # TODO - add meshes to object
        # TODO - make sure to apply the object matrix to the mesh vertices - Yakuza expects skinned meshes to be at the identity


    def export_unskinned_object(self, collection: bpy.types.Collection, object: bpy.types.Object, parent: Optional[GMDNode]):
        """
        Export a Blender object into a GMDUnskinnedObject
        :param object: TODO
        :return: TODO
        """

        # adjusted_pos = self.blender_to_gmd_space_matrix @ object.location.xyz
        #
        # b_rot = object.rotation_quaternion
        # adjusted_rot = Quaternion((b_rot.w, -b_rot.x, b_rot.z, b_rot.y))#object.rotation_quaternion.rotate(self.blender_to_gmd_space_matrix)

        # matrix is inverse world space
        gmd_world_matrix = transform_matrix_blender_to_gmd(object.matrix_world)
        # pos, rot, scale are local
        adjusted_pos, adjusted_rot, adjusted_scale = transform_blender_to_gmd(object.location, object.rotation_quaternion, object.scale)

        gmd_object = GMDUnskinnedObject(
            name=self.remove_blender_duplicate(object.name),
            node_type=NodeType.UnskinnedMesh,

            pos=adjusted_pos,
            rot=adjusted_rot,
            scale=adjusted_scale,
            parent=parent,

            matrix=gmd_world_matrix.inverted()
        )
        if not parent:
            self.node_roots.append(gmd_object)

        # TODO - add meshes to gmd_object

        # Object.children returns all children, not just direct descendants.
        direct_children = [o for o in collection.objects if o.parent == object]
        for child_object in direct_children:
            self.export_unskinned_object(collection, child_object, gmd_object)


def menu_func_export(self, context):
    self.layout.operator(ExportGMD.bl_idname, text='Yakuza GMD (.gmd)')
