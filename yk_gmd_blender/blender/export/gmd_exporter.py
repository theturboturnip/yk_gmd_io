from typing import List, Union

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty,
                       CollectionProperty)
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from mathutils import Matrix

from yk_gmd_blender.blender.error_reporter import BlenderErrorReporter
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene, HierarchyData
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_shader import GMDVertexBuffer
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_object import GMDUnskinnedObject, GMDSkinnedObject
from yk_gmd_blender.yk_gmd.v2.errors.error_classes import GMDImportExportError
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import StrictErrorReporter, LenientErrorReporter
from yk_gmd_blender.yk_gmd.v2.io import get_file_header, check_version_writeable, write_abstract_scene_out
from yk_gmd_blender.yk_gmd.v2.structure.common.header import GMDHeaderStruct

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
    # TODO - dry run feature
    #  when set, instead of exporting it will open a window with a report on what would be exported

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = True  # No animation.

        # When properties are added, use "layout.prop" here to display them
        layout.prop(self, 'strict')

    def execute(self, context):
        base_error_reporter = StrictErrorReporter() if self.strict else LenientErrorReporter()
        error_reporter = BlenderErrorReporter(self.report, base_error_reporter)

        try:
            base_header = get_file_header(self.filename, error_reporter)
            version_props = base_header.get_version_properties()

            check_version_writeable(version_props, error_reporter)

            scene_gatherer = GMDSceneGatherer(base_header)
            self.report({"INFO"}, "Extracting abstract scene...")
            # TODO - pull GMDScene out of blender
            self.report({"INFO"}, "Finished extracting abstract scene")

            gmd_scene = scene_gatherer.build()

            self.report({"INFO"}, f"Writing scene out...")
            write_abstract_scene_out(version_props,
                                     base_header.file_is_big_endian(), base_header.vertices_are_big_endian(),
                                     gmd_scene,
                                     self.filename,
                                     error_reporter)

            self.report({"INFO"}, f"Finished exporting {gmd_scene.name}")
            return {'FINISHED'}
        except GMDImportExportError as e:
            print(e)
            self.report({"ERROR"}, str(e))
        return {'CANCELLED'}


class GMDSceneGatherer:
    name: str
    node_roots: List[GMDNode]

    def __init__(self, base_header: GMDHeaderStruct):
        self.name = base_header.name.text
        self.node_roots = []

    def build(self) -> GMDScene:
        return GMDScene(
            name=self.name,
            overall_hierarchy=HierarchyData(self.node_roots)
        )

    def gather_exported_items(self):
        # Decide on an export root
            # Require a collection to be selected I guess?
            # Issue a warning if the name is different?
            # Find armature - should only be one, and should be named {name}_armature (see common for expected name)
            # Optional check against original setup
                # Just like before - go through each bone, see if the children names are the same
                # Do a recoverable_error? or a fail? maybe fail only if it's enabled
            # Once an armature has been chosen, find the un/skinned objects
                # Go through all objects in collection
                    # Unparented objects
                        # with no object child-of modifier => unskinned root
                        # with a child-of modifier
                            # for the expected skeleton => unskinned child
                            # for a different skeleton => error
                    # Objects parented to the armature
                        # with both vertex groups and an Armature modifier => skinned root
                        # with either vertex groups or an Armature modifier => warning, and skinned root
                        # with neither => unskinned object
                            # do same child-of check
                # Then go through the rest of the scene, and check?
                    # if object has child-of for our armature => warning

        pass

    def export_object(self, object: bpy.types.Object) -> Union[GMDSkinnedObject, GMDUnskinnedObject]:
        """
        Export a Blender object and it's children recursively into a GMDSkinnedObject or a GMDUnskinnedObject
        :param object: TODO
        :return: TODO
        """
        pass

    # TODO: Check in original exporter how this was done. Probably create a new file with some of those old bits.
    def export_skinned_mesh(self, object_matrix: Matrix, mesh: bpy.types.Mesh) -> List[GMDSkinnedMesh]:
        pass
    def export_unskinned_mesh(self, mesh: bpy.types.Mesh) -> List[GMDMesh]:
        pass

def menu_func_export(self, context):
    self.layout.operator(ExportGMD.bl_idname, text='Yakuza GMD (.gmd)')
