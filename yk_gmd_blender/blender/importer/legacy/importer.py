import bpy
import math
from typing import Dict, List

from yk_gmd_blender.blender.error import GMDError
from yk_gmd_blender.blender.common import material_name, uv_yk_to_blender_space, yk_to_blender_space
from yk_gmd_blender.yk_gmd.legacy.abstract.material import GMDMaterialTextureIndex
from yk_gmd_blender.yk_gmd.v2.structure.common.header import extract_base_header
from yk_gmd_blender.yk_gmd.v2.legacy_io import can_read_from, read_to_legacy
from yk_gmd_blender.yk_gmd.v2.structure.yk1.legacy_abstractor import convert_YK1_to_legacy_abstraction
from yk_gmd_blender.yk_gmd.v2.structure.yk1.file import FilePacker_YK1


class GMDImporter:
    def __init__(self, filepath, import_settings: Dict):
        self.filepath = filepath
        self.load_materials = import_settings.get("load_materials")
        self.load_bones = import_settings.get("load_bones")
        self.validate_meshes = import_settings.get("validate_meshes")
        self.merge_meshes = import_settings.get("merge_meshes")

    def read(self):
        with open(self.filepath, "rb") as in_file:
            data = in_file.read()

        can_read, base_header = can_read_from(data)
        if not can_read:
            raise GMDError(f"Can't read files with version {base_header.version_str()}")
        self.initial_data, self.scene = read_to_legacy(data)

    def check(self) -> bool:
        pass # TODO: Do checks here?

    def make_armature_object(self) -> bpy.types.Object:
        from yk_gmd_blender.yk_gmd.legacy.abstract.vector import Mat4, Vec3
        from yk_gmd_blender.yk_gmd.legacy.abstract.bone import GMDBone

        pos_to_blender = lambda p: (p.x, p.z, p.y)

        armature = bpy.data.armatures.new(f"{self.scene.name}")
        armature_object = bpy.data.objects.new(f"{self.scene.name}", armature)
        bpy.context.scene.collection.objects.link(armature_object)

        bpy.context.view_layer.objects.active = armature_object
        # Enter edit mode to create bones
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

        def recursive_bone_create(parent_blender_bone: bpy.types.EditBone, parent_matrix, bone_gmd: GMDBone):
            if bone_gmd.matrix_world_to_local and False:
                from mathutils import Matrix
                bone_gmd_transform_mathutil = Matrix(bone_gmd.matrix_world_to_local.as_tuple()).inverted()
                bone_gmd_transform = Mat4.from_tuple(
                    bone_gmd_transform_mathutil.row[0],
                    bone_gmd_transform_mathutil.row[1],
                    bone_gmd_transform_mathutil.row[2],
                    bone_gmd_transform_mathutil.row[3],
                )
            else:
                bone_gmd_transform = Mat4.translation(bone_gmd.pos) * Mat4.rotation(bone_gmd.rot) * Mat4.scale(
                    bone_gmd.scl)
                if parent_matrix:
                    bone_gmd_transform = parent_matrix * bone_gmd_transform

            bone = armature.edit_bones.new(f"{bone_gmd.name}")
            bone.use_relative_parent = False
            # TODO: This ignores bone_gmd rotation?
            head = pos_to_blender(bone_gmd_transform * Vec3(0, 0, 0))
            if parent_blender_bone:
                from mathutils import Vector
                bone.use_connect = (Vector(head) - parent_blender_bone.tail).length < 0.01
            else:
                bone.use_connect = False

            separate_child_heads = []
            for b in bone_gmd.children:
                if b.pos.magnitude() > 0.01:
                    separate_child_heads.append(b.pos)

            if len(separate_child_heads) > 0:
                sum_child_heads = sum(separate_child_heads, Vec3(0, 0, 0))
                tail = pos_to_blender(bone_gmd_transform * Vec3(
                    sum_child_heads.x / len(separate_child_heads),
                    sum_child_heads.y / len(separate_child_heads),
                    sum_child_heads.z / len(separate_child_heads),
                ))
            else:
                if bone_gmd.parent:
                    # TODO: Set 0.05 as a parameter for minimum bone length?
                    length = min(0.05, (bone_gmd.parent.pos - bone_gmd.pos).magnitude())
                else:
                    length = 0.05
                tail = pos_to_blender(bone_gmd_transform * Vec3(math.copysign(length, head[0]), 0, 0))

            # if not should_attach_to_parent:
            bone.head = head
            bone.tail = tail
            bone.parent = parent_blender_bone

            for child_bone_gmd in bone_gmd.children:
                recursive_bone_create(bone, bone_gmd_transform, child_bone_gmd)

        for root in self.scene.bone_roots:
            recursive_bone_create(None, None, root)

        # Exit edit mode
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        return armature_object

    # end self.load_bones

    def make_blender_materials(self) -> List[bpy.types.Material]:
        from bpy_extras.node_shader_utils import PrincipledBSDFWrapper
        from bpy_extras.image_utils import load_image
        import os.path

        blender_material_list = []
        for material in self.scene.materials:
            blender_name = material_name(material)

            if blender_name in bpy.data.materials:
                bpy.data.materials.remove(bpy.data.materials[blender_name])

            blender_mat: bpy.types.Material = bpy.data.materials.new(name=blender_name)
            blender_mat.use_nodes = True
            principled = PrincipledBSDFWrapper(blender_mat, is_readonly=False)

            diffuse_name = material.texture_names[GMDMaterialTextureIndex.Diffuse]
            if diffuse_name == "dummy_black":
                principled.base_color = (0, 0, 0)
            elif diffuse_name == "dummy_white":
                principled.base_color = (1, 1, 1)
            else:
                principled.base_color_texture.image = load_image(f"{diffuse_name}.dds", os.path.dirname(self.filepath),
                                                                 place_holder=True, check_existing=True)

            normal_name = material.texture_names[GMDMaterialTextureIndex.Normal]
            if normal_name != "dummy_nmap":
                principled.normalmap_texture.image = load_image(f"{normal_name}.dds", os.path.dirname(self.filepath),
                                                                place_holder=True, check_existing=True)

            # TODO: If multi texture present:
            # Map red = shininess
            # Make green lerp between setting diffuse and emission color i.e. green=0 -> diffuse, 1->emission
            # Make blue darken base color (blue=0->base, 1->black or base = base * (1 - blue)
            # See blender screenshot
            # Note - if the actual file doesn't exist, changing this to be a placeholder will mess with stuff because the placeholder is purple. Disable placeholder?
            # TODO: If shader contains [skin], enable subsurf? would require connecting the base color texture to the subsurf texture and setting "subsurface" to 1
            # Enable backface culling
            blender_mat.use_backface_culling = True

            blender_material_list.append(blender_mat)
        return blender_material_list

    def add_items(self, context: bpy.types.Context):

        self.root_obj = bpy.data.objects.new(self.scene.name, None )
        bpy.context.scene.collection.objects.link( self.root_obj )

        if self.load_bones:
            self.armature_object = self.make_armature_object()
            self.armature_object.parent = self.root_obj

        if self.load_materials:
            self.blender_materials = self.make_blender_materials()

        # Import submeshes
        # Import all meshes into a single mesh blob
        import bmesh
        bmeshes = []
        for sm_index, submesh in enumerate(self.scene.submeshes):
            print(f"Loading submesh {sm_index} with {len(submesh.vertices)} verts")
            vertex_layout = submesh.material.vertex_buffer_layout

            # (bmesh_idx, submesh_idx) pairs
            idxs = []
            bm = bmesh.new()
            bmesh_idx = 0

            # Add vertex positions
            # Assumes normals+bone weights are also present
            # Create layers for each affected bone
            deform = bm.verts.layers.deform.new("Vertex Weights")
            for i,v in enumerate(submesh.vertices):
                idxs.append((bmesh_idx, i))
                vert = bm.verts.new(yk_to_blender_space(v.pos))
                if vertex_layout.normal_type:
                    vert.normal = yk_to_blender_space(v.normal)
                #if vertex_layout.tangent_en:
                #    vert.tangent = pos_to_blender(v.tangent)
                if self.load_bones:
                    if vertex_layout.weights_type:
                        for bone_weight in v.weights:
                            if bone_weight.weight > 0:
                                vert[deform][submesh.relevant_bones[bone_weight.bone]] = bone_weight.weight
                #bmesh_idx += 1
            # Set up the indexing table inside the bmesh so lookups work
            bm.verts.ensure_lookup_table()
            bm.verts.index_update()
            #sm_idx_to_bm = {s:b for (b,s) in idxs}
            #bm_idx_to_sm = {b:s for (b,s) in idxs}

            # Connect faces
            for i in range(0, len(submesh.triangle_indices), 3):
                tri_idxs = submesh.triangle_indices[i:i+3]
                if len(set(tri_idxs)) != 3:
                    continue
                if 0xFFFF in tri_idxs:
                    continue
                self.add_face_to_bmesh(bm, submesh, tri_idxs)

            # These faces are repeats of the previous faces, so don't import then
            if False:
                for i in range(len(submesh.triangle_strip_noreset_indices)-3):
                    tri_idxs = submesh.triangle_strip_noreset_indices[i:i + 3]
                    if len(set(tri_idxs)) != 3:
                        continue
                    if 0xFFFF in tri_idxs:
                        continue
                    self.add_face_to_bmesh(bm, submesh, tri_idxs)

                for i in range(len(submesh.triangle_strip_reset_indices)-3):
                    tri_idxs = submesh.triangle_strip_reset_indices[i:i + 3]
                    if len(set(tri_idxs)) != 3:
                        continue
                    if 0xFFFF in tri_idxs:
                        continue
                    self.add_face_to_bmesh(bm, submesh, tri_idxs)

            # TODO Ignoring tangents

            # TODO Color0
            if vertex_layout.col0_type:
                col0_layer = bm.loops.layers.color.new("color0")
                for face in bm.faces:
                    for loop in face.loops:
                        color = submesh.vertices[loop.vert.index].col0
                        loop[col0_layer] = (color.x, color.y, color.z, color.w)

            # TODO Color1
            if vertex_layout.col1_type:
                col1_layer = bm.loops.layers.color.new("color1")
                for face in bm.faces:
                    for loop in face.loops:
                        color = submesh.vertices[loop.vert.index].col1
                        loop[col1_layer] = (color.x, color.y, color.z, color.w)

            # If UVs are present, add them
            # TODO add the second set of UVs
            if vertex_layout.uv0_type:
                uv_layer = bm.loops.layers.uv.new("TexCoords0")
                for face in bm.faces:
                    for loop in face.loops:
                        original_uv = submesh.vertices[loop.vert.index].uv0
                        loop[uv_layer].uv = uv_yk_to_blender_space(original_uv)

            if vertex_layout.uv1_type:
                uv_layer = bm.loops.layers.uv.new("TexCoords1")
                for face in bm.faces:
                    for loop in face.loops:
                        original_uv = submesh.vertices[loop.vert.index].uv1
                        loop[uv_layer].uv = uv_yk_to_blender_space(original_uv)

            bmeshes.append(bm)
            pass

        if self.merge_meshes:
            overall_bm = bmesh.new()
            temp_mesh = bpy.data.meshes.new(".temp")
            for bm in bmeshes:
                bm.to_mesh(temp_mesh)
                bm.free()
                overall_bm.from_mesh(temp_mesh)
                pass
            bpy.data.meshes.remove(temp_mesh)
            self.create_object_from_bmesh(overall_bm, f"{self.scene.name}_merged_mesh")
        else:
            for sm_index,bm in enumerate(bmeshes):
                self.create_object_from_bmesh(bm, f"{self.scene.name}_mesh_{sm_index}")
                pass

    def create_object_from_bmesh(self, bm, name):
        # Create a mesh object for it
        mesh = bpy.data.meshes.new(name)
        bm.to_mesh(mesh)
        bm.free()
        if self.validate_meshes:
            mesh.validate()
        if self.load_materials:
            for mat in self.blender_materials:
                mesh.materials.append(mat)
        mesh_obj = bpy.data.objects.new(name, mesh)
        if self.load_bones:
            mesh_obj.parent = self.armature_object
            for bone in self.scene.bones_in_order():
                mesh_obj.vertex_groups.new(name=bone.name)
            modifier = mesh_obj.modifiers.new(type='ARMATURE', name="Armature")
            modifier.object = self.armature_object
        else:
            mesh_obj.parent = self.root_obj
        bpy.context.collection.objects.link(mesh_obj)

    def add_face_to_bmesh(self, bm, submesh, face):
        try:
            # TODO: For some reason when using the normal winding order blender complains
            face = bm.faces.new((bm.verts[face[0]], bm.verts[face[2]], bm.verts[face[1]]))
            #face = bm.faces.new((bm.verts[face[0]], bm.verts[face[1]], bm.verts[face[2]]))
        except ValueError:
            pass
        else:
            face.smooth = True
            if self.load_materials:
                face.material_index = submesh.material.id
