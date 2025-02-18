import abc
import os
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Union

import bpy
from mathutils import Vector, Matrix
from ...common import GMDGame
from ..mesh.mesh_importer import gmd_meshes_to_bmesh
from ...materials import get_yakuza_shader_node_group, get_uv_scaler_node_group, \
    set_yakuza_shader_material_from_attributeset, YakuzaPropertyGroup, RDRT_SHADERS
from ....gmdlib.abstract.gmd_attributes import GMDAttributeSet
from ....gmdlib.abstract.gmd_scene import GMDScene
from ....gmdlib.abstract.nodes.gmd_object import GMDSkinnedObject, GMDUnskinnedObject
from ....gmdlib.errors.error_reporter import ErrorReporter
from ....gmdlib.structure.version import GMDVersion


def root_name_for_gmd_file(gmd_file: GMDScene):
    return f"{gmd_file.name}"


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
    custom_split_normals: bool


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
        if isinstance(gmd_node, GMDSkinnedObject) and not vertex_group_indices:
            self.error.fatal(f"Trying to make a skinned object without any vertex groups")

        gmd_attr_set_ids = set(id(mesh.attribute_set) for mesh in gmd_node.mesh_list)
        self.error.debug("OBJ",
                         f"Creating node {gmd_node.name} from {len(gmd_node.mesh_list)} meshes and {len(gmd_attr_set_ids)} attribute sets")

        # Create materials, and make a mapping from (id(attr_set)) -> (blender material index)
        if self.config.import_materials:
            attr_set_material_idx_mapping: Dict[int, int] = {}
            blender_material_list = []

            for i, attr_set_id in enumerate(gmd_attr_set_ids):
                meshes_for_attr_set = (gmd_mesh for gmd_mesh in gmd_node.mesh_list if
                                       id(gmd_mesh.attribute_set) == attr_set_id)
                attr_set = next(meshes_for_attr_set).attribute_set

                # Create the material
                blender_material_list.append(self.make_material(collection, attr_set))
                attr_set_material_idx_mapping[attr_set_id] = i
        else:
            # Otherwise all attribute sets are mapped to blender material index 0
            attr_set_material_idx_mapping = defaultdict(lambda: 0)

        # If we have any meshes, merge them into an overall BMesh
        if gmd_node.mesh_list:
            overall_mesh = gmd_meshes_to_bmesh(
                gmd_node.name,
                gmd_node.mesh_list,
                vertex_group_indices,
                attr_set_material_idx_mapping,
                gmd_to_blender_world=self.gmd_to_blender_world,
                fuse_vertices=self.config.fuse_vertices,
                custom_split_normals=self.config.custom_split_normals,
                error=self.error
            )
            if self.config.import_materials:
                for mat in blender_material_list:
                    overall_mesh.materials.append(mat)
        else:
            # Else use an empty mesh
            overall_mesh = bpy.data.meshes.new(gmd_node.name)
            self.error.debug("OBJ", f"Empty mesh")

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
            node.node_tree = get_yakuza_shader_node_group(self.error)
            return node

        if self.config.material_naming_convention == MaterialNamingType.Collection_Shader:
            material_name = f"{collection.name_full}_{gmd_attribute_set.shader.name}"
        elif self.config.material_naming_convention == MaterialNamingType.Collection_DiffuseTexture:
            material_name = f"{collection.name_full}_{gmd_attribute_set.texture_diffuse or 'no_tex'}"
        elif self.config.material_naming_convention == MaterialNamingType.DiffuseTexture:
            material_name = f"{gmd_attribute_set.texture_diffuse or 'no_tex'}"
        else:
            self.error.fatal(
                f"config.material_naming_convention not valid - "
                f"expected a MaterialNamingType, got {self.config.material_naming_convention}")

        material = bpy.data.materials.new(material_name)
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

        # check engine
        mat_yk_data: YakuzaPropertyGroup = material.yakuza_data  # type: ignore
        enginever = GMDVersion(mat_yk_data.material_origin_type)

        # Yakuza shaders all use backface culling (except for hair in DE.)
        material.use_backface_culling = True
        if "[hair]" in mat_yk_data.shader_name and enginever == GMDVersion.Dragon:
            material.use_backface_culling = False

        if mat_yk_data.inited == True and any([x in mat_yk_data.shader_name for x in RDRT_SHADERS]):
            uv_scaler_node = material.node_tree.nodes.new('ShaderNodeGroup')
            uv_scaler_node.node_tree = get_uv_scaler_node_group(self.error)

            if enginever == GMDVersion.Dragon:
                rtpos = mat_yk_data.unk12[6]
                rtpos2 = mat_yk_data.unk12[7]
                rdpos = mat_yk_data.unk12[4]
                rdpos2 = mat_yk_data.unk12[5]
            else:
                if "[rd]" not in mat_yk_data.shader_name and "[rt]" not in mat_yk_data.shader_name:
                    rtpos = mat_yk_data.unk12[2]
                    rtpos2 = mat_yk_data.unk12[3]
                    rdpos = mat_yk_data.attribute_set_floats[8]
                    rdpos2 = mat_yk_data.attribute_set_floats[9]
                else:
                    rtpos = mat_yk_data.attribute_set_floats[8]
                    rtpos2 = mat_yk_data.attribute_set_floats[9]
                    rdpos = mat_yk_data.unk12[8]
                    rdpos2 = mat_yk_data.unk12[9]

            uv_scaler_node.inputs[0].default_value = rtpos  # RT X
            uv_scaler_node.inputs[1].default_value = rtpos2  # RT Y
            uv_scaler_node.inputs[2].default_value = rdpos  # R(D/S/M) X
            uv_scaler_node.inputs[3].default_value = rdpos2  # ^ Y
            uv_scaler_node.inputs[4].default_value = mat_yk_data.unk12[12]  # imperfection (UV1 * (2 ^ x))
            uv_scaler_node.inputs[5].default_value = 1.0 if enginever == GMDVersion.Dragon else 0.0

            uv_scaler_node.location = (-750, -300)
            for x in material.node_tree.links:
                rdrm_textures = ["texture_rd", "texture_rm", "texture_rs"]
                if "skin" not in mat_yk_data.shader_name and any([y in x.to_socket.name
                                                                  for y in rdrm_textures]):
                    material.node_tree.links.new(uv_scaler_node.outputs[1], x.from_node.inputs[0])
                if x.to_socket.name == "texture_rt":
                    material.node_tree.links.new(uv_scaler_node.outputs[2], x.from_node.inputs[0])
                if x.to_socket.name == "texture_refl" and "h2dz" in mat_yk_data.shader_name:
                    material.node_tree.links.new(uv_scaler_node.outputs[0], x.from_node.inputs[0])

        self.material_id_to_blender[id(gmd_attribute_set)] = material
        return material
