import collections
import functools
import os
from dataclasses import dataclass
from typing import Dict, List, Callable, Tuple, Set, Generator

import bmesh
import bpy

from yk_gmd_blender.blender.common import root_name_for_gmd_file, material_name, blender_to_yk_space, \
    uv_blender_to_yk_space, blender_to_yk_space_vec4, blender_to_yk_color
from yk_gmd_blender.blender.error import GMDError
from yk_gmd_blender.yk_gmd.abstract.bone import GMDBone
from yk_gmd_blender.yk_gmd.abstract.submesh import GMDSubmesh
from yk_gmd_blender.yk_gmd.abstract.vector import Vec4
from yk_gmd_blender.yk_gmd.abstract.vertices import GMDVertex, BoneWeight
from yk_gmd_blender.yk_gmd.v2.structure.common.header import extract_base_header
from yk_gmd_blender.yk_gmd.v2.structure.legacy_io import can_read_from, read_to_legacy, write_from_legacy, \
    can_write_over
from yk_gmd_blender.yk_gmd.v2.structure.yk1.abstractor import convert_YK1_to_legacy_abstraction, \
    package_legacy_abstraction_to_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.file import FilePacker_YK1


@dataclass(frozen=False)
class SubmeshHelper:
    # NOTE - Vertices are stored with bone weights in GMD-FILE SPACE, NOT LOCAL SPACE
    # i.e. the index in the vertex is the bone ID, not some index into a local list
    vertices: List[GMDVertex]
    triangles: List[Tuple[int,int,int]]
    blender_vid_to_this_vid: Dict[int, int]
    # Maps GMD bone ID -> verts which use that ID
    weighted_bone_verts: Dict[int, List[int]]
    # Maps GMD bone ID -> face indexes which use that ID
    weighted_bone_faces: Dict[int, List[int]]

    def __init__(self):
        self.vertices = []
        self.triangles = []
        self.blender_vid_to_this_vid = {}
        self.weighted_bone_verts = collections.defaultdict(list)
        self.weighted_bone_faces = collections.defaultdict(list)

    # Adds the vertex if not already present
    def add_vertex(self, blender_vid, vertex_generator: Callable[[], GMDVertex]) -> int:
        if blender_vid not in self.blender_vid_to_this_vid:
            idx = len(self.vertices)
            self.blender_vid_to_this_vid[blender_vid] = idx
            vertex = vertex_generator()
            self.vertices.append(vertex)
            self.update_bone_vtx_lists(vertex, idx)

        return self.blender_vid_to_this_vid[blender_vid]

    # Adds a unique vertex, which we assume is never duplicated
    # Used for hard edges
    def add_unique_vertex(self, vertex) -> int:
        idx = len(self.vertices)
        self.vertices.append(vertex)
        self.update_bone_vtx_lists(vertex, idx)
        return idx

    def update_bone_vtx_lists(self, new_vtx: GMDVertex, new_vtx_idx):
        for weight in new_vtx.weights:
            if weight.weight != 0:
                self.weighted_bone_verts[weight.bone].append(new_vtx_idx)

    def add_triangle(self, t:Tuple[int,int,int]):
        # TODO: Should triangle_indices be List[Tuple[int,int,int]]?
        triangle_index = len(self.triangles)
        self.triangles.append(t)
        for bone in self.triangle_referenced_bones(triangle_index):
            #print(f"adding to {bone} of self.weighted_bone_faces (a {type(self.weighted_bone_faces).__name__})")
            #print(f"{self.weighted_bone_faces.get(bone, 0)}")
            #print(f"{self.weighted_bone_faces[bone]}")
            self.weighted_bone_faces[bone].append(triangle_index)

    def total_referenced_bones(self):
        return set(bone_id for bone_id, vs in self.weighted_bone_verts.items() if len(vs) > 0)

    def triangle_referenced_bones(self, tri_idx):
        return {weight.bone for vtx_idx in self.triangles[tri_idx] for weight in self.vertices[vtx_idx].weights if weight.weight > 0}

class SubmeshHelperSubset:
    base: SubmeshHelper
    referenced_triangles: Set[int]
    referenced_verts: Set[int]

    def __init__(self, base, referenced_triangles, referenced_verts):
        self.base = base
        self.referenced_triangles = referenced_triangles
        self.referenced_verts = referenced_verts

    def add_triangle(self, tri_idx:int):
        self.referenced_triangles.add(tri_idx)
        for vert_idx in self.base.triangles[tri_idx]:
            self.referenced_verts.add(vert_idx)

    @staticmethod
    def empty(base: SubmeshHelper):
        return SubmeshHelperSubset(base, set([]), set([]))
    @staticmethod
    def complete(base: SubmeshHelper):
        return SubmeshHelperSubset(base, set(range(len(base.triangles))), set(range(len(base.vertices))))

    def convert_to_submeshhelper(self) -> SubmeshHelper:
        sm = SubmeshHelper()
        vertex_remap = {}
        for vert_idx in self.referenced_verts:
            new_idx = sm.add_unique_vertex(self.base.vertices[vert_idx])
            vertex_remap[vert_idx] = new_idx
        for tri_idx in self.referenced_triangles:
            sm.add_triangle((
                vertex_remap[self.base.triangles[tri_idx][0]],
                vertex_remap[self.base.triangles[tri_idx][1]],
                vertex_remap[self.base.triangles[tri_idx][2]],
            ))
        return sm


# Export process
    # Check selected object - should be armature with same name as file
    # Export all meshes which are parented to that armature
        # for all mesh children of the armature
            # split on material
                # Export each split as submesh
        # alt algo - for pair in [(mat,mesh) | mat <- materials, mesh <- children] export (faces with mat in mesh if not [])

class GMDExporter:
    def __init__(self, filepath, import_settings: Dict):
        self.filepath = filepath
        # TODO - connect to settings
        self.strict = True

    def read_base_file(self):
        if not os.path.exists(self.filepath):
            raise GMDError("Must export into an existing file")

        with open(self.filepath, "rb") as in_file:
            data = in_file.read()

        can_write, base_header = can_write_over(data)
        if not can_write:
            raise GMDError(f"Can't write over files with version {base_header.version_str()}")
        self.initial_data, self.scene = read_to_legacy(data)

    def check(self):
        #if bpy.context.object.mode != "OBJECT":
        #    raise GMDError("Can only export in object mode")

        # Check that only one object is selected
        if len(bpy.context.selected_objects) != 1:
            raise GMDError("Exactly one object should be selected to export into the file")
        root = bpy.context.active_object
        if root.type != "EMPTY":
            raise GMDError("The selected object must not be a mesh or armature.")
        if len(root.children) != 1:
            raise GMDError("The selected object should have exactly one child, which should be an armature")
        armature_obj = root.children[0]
        if armature_obj.type != "ARMATURE":
            raise GMDError("The selected object should have exactly one child, which should be an armature")
        if self.strict:
            # Check that the name of the file == the name of the selected object
            expected_name = root_name_for_gmd_file(self.scene)
            if root.name != expected_name:
                raise GMDError(f"Strict Check: The name of the selected object should match the file name: {expected_name}")

        # Check that the bones in the file == the connected bones in the armature?
        def check_bone_sets_match(parent_name: str, blender_bones: List[bpy.types.Bone], gmd_bones: List[GMDBone]):
            blender_bone_dict = {x.name:x for x in blender_bones}
            gmd_bone_dict = {x.name:x for x in gmd_bones}
            if blender_bone_dict.keys() != gmd_bone_dict.keys():
                blender_bone_names = set(blender_bone_dict.keys())
                gmd_bone_names = set(gmd_bone_dict.keys())
                missing_names = gmd_bone_names - blender_bone_names
                unexpected_names = blender_bone_names - gmd_bone_names
                raise GMDError(f"Bones under {parent_name} didn't match between the file and the Blender object. Missing {missing_names}, and found unexpected names {unexpected_names}")
            for (name, gmd_bone) in gmd_bone_dict.items():
                blender_bone = blender_bone_dict[name]
                check_bone_sets_match(name, blender_bone.children, gmd_bone.children)

        self.armature = armature_obj.data
        check_bone_sets_match("root", [b for b in self.armature.bones if not b.parent], self.scene.bone_roots)

        # Gather a list of all of the meshes connected to the selected armature
        # Must be MESH type objects that have an ARMATURE modifier
        self.mesh_objs = [obj for obj in armature_obj.children if (obj.type == "MESH") and (m for m in obj.modifiers if m.types == "ARMATURE")]
        if len(self.mesh_objs) != len(armature_obj.children):
            #raise GMDError(f"Found {len(self.mesh_objs)} valid exportable meshes, but {len(armature_obj.children)} total objects were present.")
            raise GMDError(f"All armature children must be meshes and actually deformed by the armature.")

        # Collect all of the blender materials for the GMDFile material
        self.blender_mat_name_map: Dict[str, int] = {material_name(material):material.id for material in self.scene.materials}

        pass

    def update_gmd_submeshes(self):
        # Convert to REST pose
        old_pose_position = self.armature.pose_position
        if old_pose_position != "REST":
            self.armature.pose_position = "REST"
            #bpy.context.scene.update()

        depsgraph = bpy.context.evaluated_depsgraph_get()

        gmd_submeshes = []
        # Extract mesh data while in the rest pose
        for mesh_obj in self.mesh_objs:
            # Check the mesh uses at least one approved materials
            if len(mesh_obj.material_slots) == 0:
                raise GMDError(f"Mesh {mesh_obj.name} doesn't use any materials! Each mesh must use at least one material")
            unexpected_material_names = {m.name for m in mesh_obj.material_slots if m.name not in self.blender_mat_name_map}
            if unexpected_material_names:
                raise GMDError(f"Mesh {mesh_obj.name} uses materials {unexpected_material_names} which are not already present in the file")
            # Mapping of material slot -> material ID in the GMD file
            obj_mat_slot_to_gmd_id: List[int] = [self.blender_mat_name_map[m.name] for i,m in enumerate(mesh_obj.material_slots)]
            # Mapping of vertex group ID -> bone ID in the GMD file
            # Bones have already been checked, this mesh is a child of a correct armature so the bones in blender == the bones in the file
            # TODO - However, the object itself may still contain other vertex groups
            obj_vertex_group_to_gmd_id = {i:self.scene.bone_name_map[group.name].id for i,group in enumerate(mesh_obj.vertex_groups) if group.name in self.scene.bone_name_map}
            if len(obj_vertex_group_to_gmd_id) != len(mesh_obj.vertex_groups):
                # TODO: Report!
                blender_vgroups = set(g.name for g in mesh_obj.vertex_groups)
                mesh_vgroups = set(self.scene.bone_name_map.keys())
                expected_groups = mesh_vgroups.difference(blender_vgroups)
                new_groups = blender_vgroups.difference(mesh_vgroups)
                print(f"Mesh {mesh_obj.name} is missing vertex groups for {expected_groups}, and has extra groups {new_groups}")

            # Generate a mesh with modifiers applied, and put it into a bmesh
            mesh = mesh_obj.evaluated_get(depsgraph).data
            #mesh_obj.to_mesh(apply_modifiers=True, calc_undeformed=True)
            bm = bmesh.new()
            bm.from_mesh(mesh)
            bm.verts.ensure_lookup_table()
            bm.verts.index_update()

            material_submeshes = [SubmeshHelper() for m in self.scene.materials]

            deform_layer = bm.verts.layers.deform.active

            # TODO: In situations where >2 layers are present, do we want to prompt the user to remove one?
            # TODO: Make sure, if we're doing this, to remember that the else: blocks also cover len(layers) == 0

            if len(bm.loops.layers.color) == 1:
                col0_layer = bm.loops.layers.color[0]
                col1_layer = None
            elif len(bm.loops.layers.color) == 2:
                col0_layer = bm.loops.layers.color[0]
                col1_layer = bm.loops.layers.color[1]
            else:
                col0_layer = bm.loops.layers.color["color0"] if "color0" in bm.loops.layers.color else None
                col1_layer = bm.loops.layers.color["color1"] if "color1" in bm.loops.layers.color else None

            if len(bm.loops.layers.uv) == 1:
                uv0_layer = bm.loops.layers.uv[0]
                uv1_layer = None
            elif len(bm.loops.layers.uv) == 2:
                uv0_layer = bm.loops.layers.uv[0]
                uv1_layer = bm.loops.layers.uv[1]
            else:
                uv0_layer = bm.loops.layers.uv["TexCoords0"] if "TexCoords0" in bm.loops.layers.uv else None
                uv1_layer = bm.loops.layers.uv["TexCoords1"] if "TexCoords1" in bm.loops.layers.uv else None

            # TODO: Check vertex layout against expected layers?
            print(f"Exporting {mesh_obj.name}:")
            print(f"\tmaterial slot mapping: {obj_mat_slot_to_gmd_id}")
            print(f"\tvertex group mapping: {obj_vertex_group_to_gmd_id}")
            print(f"\tdeform_layer: {deform_layer.name}")
            print(f"\tuv_layers: {uv0_layer.name if uv0_layer else None} {uv1_layer.name if uv1_layer else None}")
            print(f"\tcolor_layers: {col0_layer.name if col0_layer else None} {col1_layer.name if col1_layer else None}")

            for tri_loops in bm.calc_loop_triangles():
                l0 = tri_loops[0]
                l1 = tri_loops[1]
                l2 = tri_loops[2]

                if not (0 <= l0.face.material_index < len(obj_mat_slot_to_gmd_id)):
                    # TODO: Report
                    print(f"Mesh {mesh_obj.name} has a face with out-of-bounds material index {l0.face.material_index}. It will be skipped!")
                    continue
                material_id = obj_mat_slot_to_gmd_id[l0.face.material_index]
                sm = material_submeshes[material_id]

                def vertex_of(l, normal, tangent):
                    b_vert = bm.verts[l.vert.index]
                    v = GMDVertex()
                    v.pos = blender_to_yk_space(b_vert.co)
                    v.normal = blender_to_yk_space_vec4(normal if normal else b_vert.normal, 1)
                    v.tangent = blender_to_yk_space_vec4(tangent, 1)

                    # TODO: Color0, Color1
                    if col0_layer:
                        v.col0 = blender_to_yk_color(l[col0_layer])
                    else:
                        v.col0 = Vec4(1, 1, 1, 1)

                    if col1_layer:
                        v.col1 = blender_to_yk_color(l[col1_layer])
                    else:
                        v.col1 = Vec4(1, 1, 1, 1)

                    # Get a list of (vertex group ID, weight) items sorted in descending order of weight
                    # Take the top 4 elements, for the top 4 most deforming bones
                    # Normalize the weights so they sum to 1
                    b_weights = sorted(b_vert[deform_layer].items(), key=lambda i: 1-i[1])
                    if len(b_weights) > 4:
                        b_weights = b_weights[:4]
                    elif len(b_weights) < 4:
                        # Add zeroed elements to b_weights so it's 4 elements long
                        b_weights += [(0, 0.0)] * (4 - len(b_weights))
                    weight_sum = sum(weight for (vtx,weight) in b_weights)
                    if weight_sum <= 0.0:
                        # TODO: Report this with self.report()
                        pass
                    else:
                        b_weights = [(vtx,weight/weight_sum) for (vtx,weight) in b_weights]

                    # Convert the weights to the yk_gmd abstract BoneWeight format
                    weights_list = [BoneWeight(bone=obj_vertex_group_to_gmd_id[vtx], weight=weight) for vtx, weight in b_weights]
                    v.weights = (
                        weights_list[0],
                        weights_list[1],
                        weights_list[2],
                        weights_list[3],
                    )

                    if uv0_layer:
                        v.uv0 = uv_blender_to_yk_space(l[uv0_layer].uv)
                    else:
                        v.uv0 = (0, 0)

                    if uv1_layer:
                        v.uv1 = uv_blender_to_yk_space(l[uv1_layer].uv)
                    else:
                        v.uv1 = (0, 0)

                    return v

                def parse_loop_elem(l):
                    if l.face.smooth:
                        # Smoothed vertices can be shared between different triangles that use them
                        return sm.add_vertex(l.vert.index, lambda: vertex_of(l, None, l.calc_tangent()))
                    else:
                        # Vertices on hard edges cannot be shared and must be duplicated per-face
                        return sm.add_unique_vertex(vertex_of(l, l.calc_normal(), l.calc_tangent()))

                # if face.smooth:
                #     # Vertices can be reused from the base vertex buffer.
                #     # If they're being created from this face, the face tangent for this vert is taken.
                #     # Otherwise, the vertex is taken from
                #     triangle = (
                #         sm.add_vertex(l0.vert.index, ),
                #         sm.add_vertex(l1.vert.index, lambda: vertex_of(l1.vert.index, None, l1.calc_tangent())),
                #         sm.add_vertex(l2.vert.index, lambda: vertex_of(l2.vert.index, None, l2.calc_tangent())),
                #     )
                # else:
                #     # Make copies of the vertices and add them
                #     triangle = (
                #         sm.add_unique_vertex(vertex_of(l0.vert.index, l0.calc_normal(), l0.calc_tangent())),
                #         sm.add_unique_vertex(vertex_of(l1.vert.index, l1.calc_normal(), l1.calc_tangent())),
                #         sm.add_unique_vertex(vertex_of(l2.vert.index, l2.calc_normal(), l2.calc_tangent())),
                #     )
                triangle = (
                    parse_loop_elem(l0),
                    parse_loop_elem(l1),
                    parse_loop_elem(l2),
                )
                sm.add_triangle(triangle)
                pass

            # Free the memory associated with the meshes we created
            bm.free()
            # The mesh isn't in the main database, so don't remove it
            # bpy.data.meshes.remove(mesh)

            # Filter the generated submeshes and put them in the overall submesh list
            for material_id, sm in enumerate(material_submeshes):
                if len(sm.vertices) == 0:
                    continue
                bones = [b for b,vs in sm.weighted_bone_verts.items() if len(vs) > 0]

                split_submeshes = []
                if len(bones) <= 32:
                    split_submeshes.append(sm)
                else:
                    # Split SubmeshHelpers so that you never get >32 unique bones weighting a single submesh
                    # This will always be possible, as any triangle can reference at most 12 bones (3 verts * 4 bones/vert)
                    # so a naive solution of 2 triangles per SubmeshHelper will always reference at most 24 bones which is <32.

                    x_too_many_bones = SubmeshHelperSubset.complete(sm)

                    def bonesplit(x: SubmeshHelperSubset):
                        bones = set()
                        print(x.referenced_triangles)
                        for tri in x.referenced_triangles:
                            tri_bones = x.base.triangle_referenced_bones(tri)
                            if len(tri_bones) + len(bones) < 32:
                                bones = bones.union(tri_bones)

                        x_withbones = SubmeshHelperSubset.empty(x.base)
                        x_withoutbones = SubmeshHelperSubset.empty(x.base)
                        for tri in x.referenced_triangles:
                            tri_bones = x.base.triangle_referenced_bones(tri)
                            if bones.issuperset(tri_bones):
                                x_withbones.add_triangle(tri)
                            else:
                                x_withoutbones.add_triangle(tri)

                        if len(x_withoutbones.referenced_triangles) == len(x.referenced_triangles):
                            raise GMDError("bonesplit() did not reduce triangle count!")

                        return x_withbones, x_withoutbones


                    # Start by selecting 32 bones.
                        # bones = {}
                        # for tri in submesh:
                            # tri_bones = tri.referenced_bones() (at max 24)
                            # if len(tri_bones) + len(bones) > 32
                                # break
                            # bones += tri_bones
                        # This algorithm guarantees that at least one triangle uses ONLY those bones.
                    # Then put all of the triangles that reference ONLY those bones in a new mesh.
                    # Put the other triangles in a separate mesh. If they reference > 32 bones, apply the process again.
                    # This splitting transformation bonesplit(x, bones) -> x_thosebones, x_otherbones will always produce x_otherbones with fewer triangles than x
                        # We know that at least one triangle uses only the selected bones
                            # => len(x_thosebones) >= 1
                            # len(x_otherbones) = len(x) - len(x_thosebones)
                            # => len(x_otherbones) <= len(x) - 1
                            # => len(x_otherbones) < len(x)
                    # => applying bonesplit to x_otherbones recursively will definitely reduce the amount of triangles to 0
                    # it will produce at maximum len(x) new meshes
                    split_meshes = []
                    while len(x_too_many_bones.referenced_triangles) > 0:
                        new_submesh,x_too_many_bones = bonesplit(x_too_many_bones)
                        split_meshes.append(new_submesh)

                    # these can then be merged back together!!!!
                    # TODO: Check if it's even worth it
                    print(f"Mesh {mesh_obj.name} had >32 bone references ({len(bones)}) and was split into {len(split_meshes)} chunks")

                    for split_mesh in split_meshes:
                        split_submeshes.append(split_mesh.convert_to_submeshhelper())

                    pass
                # Convert the SubmeshHelpers to Submeshes
                for sm in split_submeshes:
                    relevant_bone_list = list(sm.total_referenced_bones())
                    bone_id_map = {bone_id:idx for idx,bone_id in enumerate(relevant_bone_list)}

                    def remap_weight(w: BoneWeight):
                        if w.weight == 0:
                            return w
                        else:
                            return BoneWeight(bone=bone_id_map[w.bone], weight=w.weight)

                    def remap_vertex(v: GMDVertex):
                        new_v = GMDVertex()
                        new_v.pos = v.pos
                        new_v.normal = v.normal
                        new_v.tangent = v.tangent
                        new_v.uv0 = v.uv0
                        new_v.uv1 = v.uv1
                        new_v.col0 = v.col0
                        new_v.col1 = v.col1
                        new_v.weights = ((
                            remap_weight(v.weights[0]),
                            remap_weight(v.weights[1]),
                            remap_weight(v.weights[2]),
                            remap_weight(v.weights[3]),
                        ))
                        return new_v

                    vertices = [remap_vertex(v) for v in sm.vertices]

                    # TODO: Better strip handling?
                    # The newer games only render triangle_strip_reset_indices, but the file should contain all variants
                    # TODO: Enable configurable import for each triangle strip type - import only one type, or all?
                    triangle_indices = []
                    triangle_strip_noreset_indices = []
                    triangle_strip_reset_indices = []
                    for t in sm.triangles:
                        # Blender uses reversed winding order
                        triangle_indices.append(t[0])
                        triangle_indices.append(t[2])
                        triangle_indices.append(t[1])

                        # If we can continue the strip, do so
                        if not triangle_strip_noreset_indices:
                            # Add the triangle as normal
                            triangle_strip_noreset_indices.append(t[0])
                            triangle_strip_noreset_indices.append(t[2])
                            triangle_strip_noreset_indices.append(t[1])
                        elif (triangle_strip_noreset_indices[-2] == t[0] and
                                triangle_strip_noreset_indices[-1] == t[2]):
                            triangle_strip_noreset_indices.append(t[1])
                        else:
                            # Two extra verts to create a degenerate triangle, signalling the end of the strip
                            triangle_strip_noreset_indices.append(triangle_strip_noreset_indices[-1])
                            triangle_strip_noreset_indices.append(t[0])
                            # Add the triangle as normal
                            triangle_strip_noreset_indices.append(t[0])
                            triangle_strip_noreset_indices.append(t[2])
                            triangle_strip_noreset_indices.append(t[1])

                        # If we can continue the strip, do so
                        if not triangle_strip_reset_indices:
                            # Add the triangle as normal
                            triangle_strip_reset_indices.append(t[0])
                            triangle_strip_reset_indices.append(t[2])
                            triangle_strip_reset_indices.append(t[1])
                        elif (triangle_strip_reset_indices[-2] == t[0] and
                                triangle_strip_reset_indices[-1] == t[2]):
                            triangle_strip_reset_indices.append(t[1])
                        else:
                            # Reset index signalling the end of the strip
                            triangle_strip_reset_indices.append(0xFFFF)
                            # Add the triangle as normal
                            triangle_strip_reset_indices.append(t[0])
                            triangle_strip_reset_indices.append(t[2])
                            triangle_strip_reset_indices.append(t[1])

                    # triangle_indices = [sm.triangles[0][0], sm.triangles[0][2], sm.triangles[0][1]]
                    # triangle_strip_noreset_indices = [sm.triangles[1][0], sm.triangles[1][2], sm.triangles[1][1]]
                    # triangle_strip_reset_indices = functools.reduce(lambda a,b: a + [0xFFFF] + b, [[t[0], t[2], t[1]] for t in sm.triangles])

                    gmd_submeshes.append(GMDSubmesh(
                        material=self.scene.materials[material_id],

                        relevant_bones=relevant_bone_list,

                        vertices=vertices,

                        triangle_indices=triangle_indices,
                        triangle_strip_noreset_indices=triangle_strip_noreset_indices,
                        triangle_strip_reset_indices=triangle_strip_reset_indices,
                    ))
                    # Remove the submesh data, avoid massive memory usage
                    del sm
            pass

        # Put the submesh list into self.gmd_file
        self.scene.submeshes = gmd_submeshes

        print(f"Built list of submeshes: {len(self.scene.submeshes)}")

        # Convert back to normal pose
        if old_pose_position != "REST":
            self.armature.pose_position = old_pose_position
            #bpy.context.scene.update()
        pass

    def overwrite_file_with_abstraction(self):
        new_data = write_from_legacy(self.initial_data, self.scene)
        with open(self.filepath, "wb") as out_file:
            out_file.write(new_data)
