import os
import re
from typing import Dict

from mathutils import Matrix, Vector

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       CollectionProperty)
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper
from yk_gmd_blender.blender.common import armature_name_for_gmd_file, root_name_for_gmd_file

from yk_gmd_blender.blender.error_reporter import BlenderErrorReporter
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDMaterial
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.errors.error_classes import GMDImportExportError
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import StrictErrorReporter, LenientErrorReporter, ErrorReporter
from yk_gmd_blender.yk_gmd.v2.io import read_abstract_scene


class ImportGMD(Operator, ImportHelper):
    """Loads a GMD file into blender"""
    bl_idname = "import_scene.gmd"
    bl_label = "Import Yakuza GMD"

    filter_glob: StringProperty(default="*.gmd", options={"HIDDEN"})

    strict: BoolProperty(name="Strict File Import",
                         description="If True, will fail the import even on recoverable errors.",
                         default=True)

    import_hierarchy: BoolProperty(name="Import Hierarchy",
                                   description="If True, will import the full node hierarchy including skeleton bones. "
                                               "This is required if you want to export the scene later. "
                                               "Skinned meshes will be imported with bone weights.",
                                   default=True)
    import_objects: BoolProperty(name="Import Objects",
                                 description="If True, will import the full object hierarchy. "
                                             "This is required if you want to export the scene later.",
                                 default=True)
    import_materials: BoolProperty(name="Import Materials",
                                   description="If True, will import materials. If False, all objects will not have any materials. "
                                               "This is required if you want to export the scene later.",
                                   default=True)

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = True  # No animation.

        # When properties are added, use "layout.prop" here to display them
        # layout.prop(self, 'load_materials')
        # layout.prop(self, 'load_bones')
        # layout.prop(self, 'validate_meshes')
        # layout.prop(self, 'merge_meshes')
        layout.prop(self, 'strict')
        layout.prop(self, 'import_hierarchy')
        layout.prop(self, 'import_objects')
        layout.prop(self, 'import_materials')

    def execute(self, context):
        base_error_reporter = StrictErrorReporter() if self.strict else LenientErrorReporter()
        error_reporter = BlenderErrorReporter(self.report, base_error_reporter)

        try:
            self.report({"INFO"}, "Extracting abstract scene...")
            gmd_scene = read_abstract_scene(self.filepath, error_reporter)
            self.report({"INFO"}, "Finished extracting abstract scene")

            nodes_depth_first = [node for node in gmd_scene.overall_hierarchy.depth_first_iterate()]
            node_names = {node.name for node in nodes_depth_first}
            if len(node_names) != len(nodes_depth_first):
                # Find the duplicate names by listing them all, and removing one occurence of each name
                # The only names left will be duplicates
                node_name_list = [node.name for node in nodes_depth_first]
                for name in node_names:
                    node_name_list.remove(name)
                duplicate_names = set(node_name_list)
                error_reporter.fatal(f"Some nodes don't have unique names - found duplicates {duplicate_names}")

            scene_creator = GMDSceneCreator(gmd_scene)
            gmd_collection = scene_creator.make_collection(context)

            if self.import_hierarchy:
                gmd_armature = scene_creator.make_bone_hierarchy(context, gmd_collection)

            if self.import_materials:
                pass

            if self.import_objects:
                pass

            return {'FINISHED'}
        except GMDImportExportError as e:
            print(e)
            self.report({"ERROR"}, str(e))
        return {'CANCELLED'}


class GMDSceneCreator:
    gmd_scene: GMDScene
    material_id_to_blender: Dict[int, bpy.types.Material]
    gmd_to_blender_world: Matrix

    def __init__(self, gmd_scene: GMDScene, error: ErrorReporter):
        self.gmd_scene = gmd_scene
        self.material_id_to_blender = {}
        self.gmd_to_blender_world = Matrix((
            Vector((1, 0, 0, 0)),
            Vector((0, 0, -1, 0)),
            Vector((0, 1, 0, 0)),
            Vector((0, 0, 0, 1)),
        ))
        self.error = error

    def make_collection(self, context: bpy.types.Context) -> bpy.types.Collection:
        collection_name = root_name_for_gmd_file(self.gmd_scene)
        collection = bpy.data.collections.new(collection_name)
        # TODO: This was just sort of copied from XNALara - it's probably better to just take the scene collections?
        view_layer = bpy.context.view_layer
        active_collection = view_layer.active_layer_collection.collection
        active_collection.children.link(collection)
        return collection

    def make_bone_hierarchy(self, context: bpy.types.Context, collection: bpy.types.Collection) -> bpy.types.Object:
        armature_name = armature_name_for_gmd_file(self.gmd_scene)
        armature = bpy.data.armatures.new(f"{armature_name}")
        armature.display_type = 'STICK'
        armature_obj = bpy.data.objects.new(f"{armature_name}", armature)
        armature_obj.show_in_front = True

        collection.objects.link(armature_obj)

        context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT')

        # Idea for regex taken from https://github.com/johnzero7/XNALaraMesh/blob/eaccfddf39aef8d3cb60a50c05f2585398fe26ca/import_xnalara_model.py#L356
        # The actual regex has been changed tho
        twist_regex = re.compile(r'[-_](twist|adj|sup)\d*([-_\s]|$)')

        parent_world_yakuza_space_matrices: Dict[str, Matrix] = {}

        for gmd_node in self.gmd_scene.overall_hierarchy.depth_first_iterate():
            if not isinstance(gmd_node, GMDBone):
                if gmd_node.children:
                    # The importer assumes that SkinnedObjects and UnskinnedObjects cannot have children
                    self.error.fatal(f"Node {gmd_node.name} is a {gmd_node.node_type} node with children! The importer expects only MatrixTransform nodes to have children.")
                continue

            bone = armature.edit_bones.new(f"{gmd_node.name}")
            bone.use_relative_parent = False

            # Find the local->world matrix for this bone, and it's parent
            # if gmd_node.matrix:
            #     this_bone_matrix = self.gmd_to_blender_world @ gmd_node.matrix.inverted()
            # elif gmd_node.parent:
            #     this_bone_matrix = armature.edit_bones[gmd_node.parent.name].matrix @ (Matrix.Translation(gmd_node.pos.xyz) @ gmd_node.rot.to_matrix().resize_4x4() @ Matrix.Diagonal(gmd_node.scale.xyz).resize_4x4())
            # else:
            #     this_bone_matrix = self.gmd_to_blender_world @ Matrix.Identity(4)

            if gmd_node.parent:
                parent_matrix = parent_world_yakuza_space_matrices[gmd_node.parent.name]
            else:
                parent_matrix = Matrix.Identity(4)

            rot_matrix = gmd_node.rot.to_matrix()
            rot_matrix.resize_4x4()
            this_bone_matrix = parent_matrix @ (Matrix.Translation(gmd_node.pos.xyz) @ rot_matrix)# @ Matrix.Diagonal(gmd_node.scale.xyz).resize_4x4())
            parent_world_yakuza_space_matrices[gmd_node.name] = this_bone_matrix

            #print(f"{gmd_node.name}")
            #if isinstance(gmd_node, GMDBone):
            bone.use_deform = True

            # Take a page out of XNA Importer's book for bone tails - make roots just stick towards the camera
            # and make nodes with (non-twist) children try to go to the average of those children's positions
            if not gmd_node.parent:
                #print("Using basic Z-delta for tail")
                tail_delta = Vector((0, 0, 0.5))
            elif twist_regex.search(gmd_node.name) and not gmd_node.children:
                # We have a parent, and we're a twist bone
                # "Twist Bones" allow things like shoulders to be twisted when the arm is bent.
                # They are separate from the main arm bone, and shouldn't really extend in the same direction
                # as the arm bone, as otherwise it would be difficult to tell them apart.

                # First, check if we have siblings in a similar position to ours - these are the bones we want to be different from
                adjacent_siblings = [child for child in gmd_node.parent.children if child is not gmd_node and (child.pos - gmd_node.pos).length < 0.01]
                if adjacent_siblings:
                    # If we're trying to be different from our sibling, we pick a direction that is perpendicular to the direction we would normally pick

                    # Pick a vector perpendicular to the parent direction
                    parent_dir = (gmd_node.pos.xyz) # gmd_node.pos is relative to the parent already
                    original_parent_dir_length = parent_dir.length
                    parent_dir.normalize()
                    perp_dir = Vector((0, 0, 1))
                    if parent_dir.dot(perp_dir) > 0.99:
                        # Parent and proposed perpendicular direction are basically the same, cross product won't work
                        # Choose a different one
                        perp_dir = Vector((0, 1, 0))

                    tail_delta_dir = parent_dir.cross(perp_dir)
                    tail_delta_dir.normalize()

                    #tail_delta_dir = perp_dir.cross(guaranteed_perp)

                    # Cross product can have bad symmetry - bones on opposite sides
                    # Fix this by picking the delta which moves the tail the farthest possible distance from the origin
                    # This will choose consistent directions regardless of which side of the Y axis you are on
                    distance_from_origin_with_positive = (this_bone_matrix @ (tail_delta_dir * 0.1)).length
                    distance_from_origin_with_negative = (this_bone_matrix @ (-tail_delta_dir * 0.1)).length
                    if distance_from_origin_with_negative > distance_from_origin_with_positive:
                        tail_delta_dir = -tail_delta_dir

                    # Extend the tail in the direction of the delta, for the same length between this bone and our parent
                    #print(f"Using twist formula - parent_dir {parent_dir} perp_dir {perp_dir} tail_delta_dir {tail_delta_dir}")
                    tail_delta = (tail_delta_dir.xyz * 0.1)
                else:
                    # There aren't any bones we have to differentiate ourselves from -> just follow the parent delta, like the default for having no children
                    tail_delta = gmd_node.pos.xyz.normalized() * 0.05
            else:
                # This either isn't a twist bone or it has children - most likely this just isn't a twist bone, as twist bones generally don't have children anyway
                # If there are non-twist children, set the tail to the average of their positions
                countable_children_gmd_positions = [child.pos.xyz for child in gmd_node.children if not twist_regex.search(child.name)]

                if countable_children_gmd_positions:
                    #print(f"Has usable children - using delta from average of {countable_children_gmd_positions}")
                    tail_delta = sum(countable_children_gmd_positions, Vector((0,0,0))) / len(countable_children_gmd_positions)
                else:
                    #print(f"No usable children - just extending in direction of pos, which is {gmd_node.pos.xyz}")
                    # Extend the tail in the direction of the parent
                    # gmd_node.pos.xyz is relative to the parent already
                    if gmd_node.pos.xyz.length < 0.00001:
                        tail_delta = Vector((0, 0, 0.05))
                    else:
                        tail_delta = gmd_node.pos.xyz.normalized() * 0.05 # + (gmd_node.pos.xyz - gmd_node.parent.pos.xyz)
            # else:
            #     bone.use_deform = False
            #     print(f"Not deforming - using straight offset")
            #     tail_delta = Vector((0, 0, 0.5))

            #bone.matrix = self.gmd_to_blender_world @ this_bone_matrix
            bone.head = self.gmd_to_blender_world @ this_bone_matrix @ Vector((0,0,0))
            bone.tail = self.gmd_to_blender_world @ this_bone_matrix @ tail_delta
            # TODO: If your head is close to your parent's tail, turn on "connected to parent"
            bone.parent = armature.edit_bones[gmd_node.parent.name] if gmd_node.parent else None

        bpy.ops.object.mode_set(mode='POSE')
        # todo - set custom shape for object bones (and bones with no parent?) (and twist bones????)
        #bpy.data.objects['Armature'].pose.bones['Bone1'].custom_shape = bpy.data.objects['wgt_bone1']

        # todo - XNALara sets custom colors for things based on the objects they affect - we could do something like that too?
        # https://github.com/johnzero7/XNALaraMesh/blob/eaccfddf39aef8d3cb60a50c05f2585398fe26ca/import_xnalara_model.py#L748
        # having color differentiation may make it easier to navigate

        bpy.ops.object.mode_set(mode='OBJECT')

        return armature_obj

    def make_material(self, gmd_material: GMDMaterial) -> bpy.types.Material:
        if id(gmd_material) in self.material_id_to_blender:
            return self.material_id_to_blender[id(gmd_material)]
        raise NotImplementedError()


def menu_func_import(self, context):
    self.layout.operator(ImportGMD.bl_idname, text='Yakuza GMD (.gmd)')
