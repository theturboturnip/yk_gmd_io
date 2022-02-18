import abc
import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Union

import bmesh
from mathutils import Vector, Matrix

import bpy
from yk_gmd_blender.blender.common import root_name_for_gmd_file, GMDGame
from yk_gmd_blender.blender.importer.mesh_importer import gmd_meshes_to_bmesh
from yk_gmd_blender.blender.materials import get_yakuza_shader_node_group, set_yakuza_shader_material_from_attributeset
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_attributes import GMDAttributeSet
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_scene import GMDScene
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_object import GMDSkinnedObject, GMDUnskinnedObject
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter


class MaterialNamingType(Enum):
    # Collection Name then Shader Name (old default)
    Collection_Shader = 0
    # Collection Name then DiffuseTexture Name
    # (fall back to Shader Name if no diffusetexture?)
    # Theoretically the best method for differentiating models with common shaders
    Collection_DiffuseTexture = 1
    # Just DiffuseTexture name, for @Haruka-Chan
    DiffuseTexture = 2


@dataclass(frozen=True)
class GMDSceneCreatorConfig:
    game: GMDGame

    import_materials: bool
    material_naming_convention: MaterialNamingType

    fuse_vertices: bool


class BaseGMDSceneCreator(abc.ABC):
    """
    Class used to create all meshes and materials in Blender, from a GMDScene.
    Uses ErrorReporter for all error handling.
    """
    config: GMDSceneCreatorConfig
    filepath: str
    gmd_scene: GMDScene
    error: ErrorReporter

    material_id_to_blender: Dict[int, bpy.types.Material]
    gmd_to_blender_world: Matrix

    def __init__(self, filepath: str, gmd_scene: GMDScene, config: GMDSceneCreatorConfig, error: ErrorReporter):
        self.config = config
        self.filepath = filepath
        self.gmd_scene = gmd_scene
        self.error = error

        self.material_id_to_blender = {}
        # The Yakuza games treat +Y as up, +Z as forward.
        # Blender treats +Z as up, +Y as forward, but if we just leave it at that then X is inverted.
        self.gmd_to_blender_world = Matrix((
            Vector((-1, 0, 0, 0)),
            Vector((0, 0, 1, 0)),
            Vector((0, 1, 0, 0)),
            Vector((0, 0, 0, 1)),
        ))

    def validate_scene(self):
        raise NotImplementedError()

    def make_collection(self, context: bpy.types.Context) -> bpy.types.Collection:
        """
        Build a collection to hold all of the objects and meshes from the GMDScene.
        :param context: The context used by the import process.
        :return: A collection which the importer can add objects and meshes to.
        """
        collection_name = root_name_for_gmd_file(self.gmd_scene)
        collection = bpy.data.collections.new(collection_name)
        # Link the new collection to the currently active collection.
        context.collection.children.link(collection)
        return collection

    def build_object_mesh(self, collection: bpy.types.Collection,
                          gmd_node: Union[GMDSkinnedObject, GMDUnskinnedObject],
                          vertex_group_indices: Dict[str, int]) -> bpy.types.Mesh:
        temp_mesh = bpy.data.meshes.new(gmd_node.name)

        if isinstance(gmd_node, GMDSkinnedObject) and not vertex_group_indices:
            self.error.fatal(f"Trying to make a skinned object without any vertex groups")

        # 1. Make a single BMesh containing all meshes referenced by this object.
        # We want to do vertex deduplication any meshes that use the same attribute sets, as it is likely that they were
        # originally split up for the sake of bone limits, and not merging them would make blender bug up.
        # To do this, we list all of the unique attribute sets:
        gmd_attr_set_ids = list({id(mesh.attribute_set) for mesh in gmd_node.mesh_list})
        # TODO: This method probably wastes a lot of time creating new BMeshes.
        #  It could be better to just append to the overall_bm instead of making a new one, sending it to a Mesh, then adding it back.
        overall_bm = bmesh.new()
        blender_material_list = []

        self.error.info(
            f"Creating node {gmd_node.name} from {len(gmd_node.mesh_list)} meshes and {len(gmd_attr_set_ids)} attribute sets")

        # then we make a merged GMDMesh object for each attribute set, containing the meshes that use that attribute set.
        for i, attr_set_id in enumerate(gmd_attr_set_ids):
            meshes_for_attr_set = [gmd_mesh for gmd_mesh in gmd_node.mesh_list if
                                   id(gmd_mesh.attribute_set) == attr_set_id]
            attr_set = meshes_for_attr_set[0].attribute_set
            self.error.info(
                f"\tattr_set #{attr_set_id} has {len(meshes_for_attr_set)} meshes with {[len(gmd_mesh.vertices_data) for gmd_mesh in meshes_for_attr_set]} verts each.")

            # Convert this merged GMDMesh to a BMesh, then merge it into the overall BMesh.
            if self.config.import_materials:
                blender_material_list.append(self.make_material(collection, attr_set))
                new_bmesh = gmd_meshes_to_bmesh(
                    meshes_for_attr_set,
                    vertex_group_indices,
                    attr_idx=i,
                    gmd_to_blender_world=self.gmd_to_blender_world,
                    fuse_vertices=self.config.fuse_vertices,
                    error=self.error
                )
            else:
                new_bmesh = gmd_meshes_to_bmesh(
                    meshes_for_attr_set,
                    vertex_group_indices,
                    attr_idx=0,
                    gmd_to_blender_world=self.gmd_to_blender_world,
                    fuse_vertices=self.config.fuse_vertices,
                    error=self.error
                )

            self.error.info(
                f"\t\tAdding {len(new_bmesh.verts)} verts and {len(new_bmesh.faces)} faces for accumulated, (fused={self.config.fuse_vertices}) mesh of attr_set #{attr_set_id}")

            # Merge it in to the overall bmesh.
            new_bmesh.to_mesh(temp_mesh)
            new_bmesh.free()
            overall_bm.from_mesh(temp_mesh)
        self.error.info(f"\tOverall mesh vert count: {len(overall_bm.verts)}")

        # Turn the overall BMesh into a Blender Mesh (there's a difference) so that it can be attached to an Object.
        # Reuse the temp mesh from before
        overall_mesh = temp_mesh
        overall_bm.to_mesh(overall_mesh)
        overall_bm.free()
        if self.config.import_materials:
            for mat in blender_material_list:
                overall_mesh.materials.append(mat)

        return overall_mesh

    def make_material(self, collection: bpy.types.Collection, gmd_attribute_set: GMDAttributeSet) -> bpy.types.Material:
        """
        Given a gmd_attribute_set, make a Blender material.
        The material name is based on the collection name NOT the gmd_scene name, in case duplicate scenes exist.
        i.e. if c_am_kiryu is imported twice, the second collection will be named c_am_kiryu.001.
        For consistency, the materials can take this c_am_kiryu.001 as a prefix.
        :param collection: The collection the scene is associated with.
        :param gmd_attribute_set: The attribute set to create a material for.
        :return: A Blender material with all of the data from the gmd_attribute_set represented in an exportable way.
        """
        # If the attribute set has a material already, reuse it.
        if id(gmd_attribute_set) in self.material_id_to_blender:
            return self.material_id_to_blender[id(gmd_attribute_set)]

        def make_yakuza_node_group(node_tree: bpy.types.NodeTree):
            node = node_tree.nodes.new("ShaderNodeGroup")
            node.node_tree = get_yakuza_shader_node_group()
            return node

        if self.config.material_naming_convention == MaterialNamingType.Collection_Shader:
            material_name = f"{collection.name_full}_{gmd_attribute_set.shader.name}"
        elif self.config.material_naming_convention == MaterialNamingType.Collection_DiffuseTexture:
            material_name = f"{collection.name_full}_{gmd_attribute_set.texture_diffuse or 'no_tex'}"
        elif self.config.material_naming_convention == MaterialNamingType.DiffuseTexture:
            material_name = f"{gmd_attribute_set.texture_diffuse or 'no_tex'}"
        else:
            self.error.fatal(f"config.material_naming_convention not valid - expected a MaterialNamingType, got {self.config.material_naming_convention}")

        material = bpy.data.materials.new(material_name)
        # Yakuza shaders all use backface culling (even the transparent ones!)
        material.use_backface_culling = True
        # They all have to use nodes, of course
        material.use_nodes = True
        # Don't use the default node setup
        material.node_tree.nodes.clear()
        # Make a Yakuza Shader group, and position it
        yakuza_shader_node_group = make_yakuza_node_group(material.node_tree)
        yakuza_shader_node_group.location = (0, 0)
        yakuza_shader_node_group.width = 400
        yakuza_shader_node_group.height = 800
        # Hook up the Yakuza Shader to the output
        output_node = material.node_tree.nodes.new("ShaderNodeOutputMaterial")
        output_node.location = (500, 0)
        material.node_tree.links.new(yakuza_shader_node_group.outputs["Shader"], output_node.inputs["Surface"])

        # Set up the group inputs and material data based on the attribute set.
        set_yakuza_shader_material_from_attributeset(
            material,
            yakuza_shader_node_group.inputs,
            gmd_attribute_set,
            os.path.dirname(self.filepath)
        )

        self.material_id_to_blender[id(gmd_attribute_set)] = material
        return material
