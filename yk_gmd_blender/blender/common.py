from dataclasses import dataclass
from enum import IntEnum
from typing import Tuple, List, Dict, Optional, Union

import bpy
from bmesh.types import BMesh, BMLayerCollection
from bpy.props import BoolProperty, FloatVectorProperty, StringProperty, IntProperty, EnumProperty
from bpy.types import PropertyGroup, Panel
from ..gmdlib.abstract.gmd_shader import GMDVertexBufferLayout, VecStorage
from ..gmdlib.errors.error_reporter import ErrorReporter


class GMDGame(IntEnum):
    """
    List of games using each engine in release order.
    Can be used to handle engine or game-specific quirks.
    (theoretically) bitmask-capable, so you can test a game against an engine and see if it matches.
    """
    Engine_MagicalV = 0x10
    Kenzan = 0x11
    Yakuza3 = 0x12
    Yakuza4 = 0x13
    DeadSouls = 0x14
    BinaryDomain = 0x15

    Engine_Kiwami = 0x20
    Yakuza5 = 0x21
    Yakuza0 = 0x22
    YakuzaKiwami1 = 0x23
    FOTNS = 0x24

    Engine_Dragon = 0x40
    Yakuza6 = 0x41
    YakuzaKiwami2 = 0x42
    Judgment = 0x43
    Yakuza7 = 0x44

    @staticmethod
    def blender_props() -> List[Tuple[str, str, str]]:
        return [
            ("ENGINE_MAGICALV", "Old Engine", "Magical-V Engine (Kenzan - Binary Domain)"),
            ("KENZAN", "Yakuza Kenzan", "Yakuza Kenzan"),
            ("YAKUZA3", "Yakuza 3", "Yakuza 3"),
            ("YAKUZA4", "Yakuza 4", "Yakuza 4"),
            ("DEADSOULS", "Yakuza Dead Souls", "Yakuza Dead Souls"),
            ("BINARYDOMAIN", "Binary Domain", "Binary Domain"),

            ("ENGINE_KIWAMI", "Kiwami Engine", "Kiwami Engine (Yakuza 5 - Yakuza Kiwami 1)"),
            ("YAKUZA5", "Yakuza 5", "Yakuza 5"),
            ("YAKUZA0", "Yakuza 0", "Yakuza 0"),
            ("YAKUZAK1", "Yakuza K1", "Yakuza Kiwami 1"),
            ("FOTNS", "FOTNS: LP", "Fist of the North Star: Lost Paradise"),

            ("ENGINE_DRAGON", "Dragon Engine", "Dragon Engine (Yakuza 6 onwards)"),
            ("YAKUZA6", "Yakuza 6", "Yakuza 6"),
            ("YAKUZAK2", "Yakuza K2", "Yakuza K2"),
            ("JUDGMENT", "Judgment", "Judgment"),
            ("YAKUZA7", "Yakuza 7", "Yakuza 7"),
        ]

    @staticmethod
    def mapping_from_blender_props() -> Dict[str, 'GMDGame']:
        return {
            "ENGINE_MAGICALV": GMDGame.Engine_MagicalV,
            "KENZAN": GMDGame.Kenzan,
            "YAKUZA3": GMDGame.Yakuza3,
            "YAKUZA4": GMDGame.Yakuza4,
            "DEADSOULS": GMDGame.DeadSouls,
            "BINARYDOMAIN": GMDGame.BinaryDomain,

            "ENGINE_KIWAMI": GMDGame.Engine_Kiwami,
            "YAKUZA5": GMDGame.Yakuza5,
            "YAKUZA0": GMDGame.Yakuza0,
            "YAKUZAK1": GMDGame.YakuzaKiwami1,
            "FOTNS": GMDGame.FOTNS,

            "ENGINE_DRAGON": GMDGame.Engine_Dragon,
            "YAKUZA6": GMDGame.Yakuza6,
            "YAKUZAK2": GMDGame.YakuzaKiwami2,
            "JUDGMENT": GMDGame.Judgment,
            "YAKUZA7": GMDGame.Yakuza7,
        }

    @staticmethod
    def mapping_to_blender_props() -> Dict['GMDGame', str]:
        return {v: k for k, v in GMDGame.mapping_from_blender_props().items()}

    def as_blender(self) -> str:
        return GMDGame.mapping_to_blender_props()[self]


class YakuzaHierarchyNodeData(PropertyGroup):
    # Has this PropertyGroup been initialized from a GMD file?
    # Used to hide data for normal Blender objects
    inited: BoolProperty(name="Initialized", default=False)
    # The original imported node matrix
    imported_matrix: FloatVectorProperty(name="Imported Node Matrix", default=[0.0] * 16, size=16, subtype="MATRIX")

    # The animation axis for the node imported from the GMD
    anim_axis: FloatVectorProperty(name="Animation Axis (Quaternion)", default=[0.0] * 4, size=4, subtype="QUATERNION")
    # The local rotation of the bone imported from the GMD
    bone_local_rot: FloatVectorProperty(name="Bone Local Rot (Quaternion)", default=[0.0] * 4, size=4,
                                        subtype="QUATERNION")
    # Node flags - currently unknown. Stored as JSON because IntVectorProperty doesn't support unsigned 32-bit integers
    flags_json: StringProperty(name="Imported Node Flags (JSON)", default="[0,0,0,0]")

    # The order of this node with respect to siblings
    sort_order: IntProperty(name="Sort Order", default=0,
                            description="Order of this node with respect to siblings. Applied on export.")


def yakuza_hierarchy_node_data_sort_key(x) -> int:
    return x.yakuza_hierarchy_node_data.sort_order


class OBJECT_PT_yakuza_hierarchy_node_data_panel(Panel):
    bl_label = "Yakuza Hierarchy-Node Data"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        ob = context.object

        if not ob:
            return

        layout.prop(ob.yakuza_hierarchy_node_data, "anim_axis")
        layout.prop(ob.yakuza_hierarchy_node_data, "flags_json")
        layout.prop(ob.yakuza_hierarchy_node_data, "sort_order")

        if ob.yakuza_file_root_data.is_valid_root:
            layout.label(text="This is a Yakuza File Root, it shouldn't have hierarchy-node data")
        elif ob.yakuza_hierarchy_node_data.inited:
            def matrix_prop(dat, prop_name, length: int, text=""):
                layout.label(text=text)
                box = layout.box().grid_flow(row_major=True, columns=4, even_rows=True, even_columns=True)
                for i in range(length // 4):
                    for j in range(i * 4, (i + 1) * 4):
                        box.prop(dat, prop_name, index=j, text="")

            matrix_prop(ob.yakuza_hierarchy_node_data, "imported_matrix", 16)
        else:
            if any(m.type == "ARMATURE" for m in ob.modifiers):
                layout.label(text="Skinned objects don't have the imported_matrix property")
            else:
                layout.label(text=f"This object wasn't imported from a GMD, doesn't have a imported_matrix property")


class BONE_PT_yakuza_hierarchy_node_data_panel(Panel):
    bl_label = "Yakuza Hierarchy-Node Data (Bone)"

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'bone'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        bone = context.bone
        if not bone:
            bone = context.edit_bone

        if not bone:
            return

        layout.prop(bone.yakuza_hierarchy_node_data, "anim_axis")
        layout.prop(bone.yakuza_hierarchy_node_data, "bone_local_rot")
        layout.prop(bone.yakuza_hierarchy_node_data, "flags_json")
        layout.prop(bone.yakuza_hierarchy_node_data, "sort_order")

        if bone.yakuza_hierarchy_node_data.inited:
            def matrix_prop(dat, prop_name, length: int, text=""):
                layout.label(text=text)
                box = layout.box().grid_flow(row_major=True, columns=4, even_rows=True, even_columns=True)
                for i in range(length // 4):
                    for j in range(i * 4, (i + 1) * 4):
                        box.prop(dat, prop_name, index=j, text="")

            matrix_prop(bone.yakuza_hierarchy_node_data, "imported_matrix", 16)
        else:
            layout.label(text=f"No original matrix, this bone wasn't imported from a GMD")


class YakuzaFileRootData(PropertyGroup):
    is_valid_root: BoolProperty(name="Is Valid Root", default=False)
    # GMD version this file was imported from
    imported_version: EnumProperty(items=GMDGame.blender_props(), name="Imported File Version", default=None)
    # scene flags
    flags_json: StringProperty(name="Imported Scene Flags (JSON)", default="[0,0,0,0,0,0]")
    # how this file was imported
    import_mode: EnumProperty(items=[
        ("SKINNED", "Skinned",
         "Imported as a top-level armature with direct children objects, manipulated via skinning. Exportable."),
        ("UNSKINNED", "Unskinned", "Imported as a hierarchy of unskinned objects. Exportable."),
        ("ANIMATION", "Animation-friendly",
         "Imported with every mesh attached to a bone, for animation purposes. NOT exportable.")
    ], name="Import Mode", default=None)


class OBJECT_PT_yakuza_file_root_data_panel(Panel):
    bl_label = "Yakuza File Root"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    bl_category = "Tool"
    bl_order = 1  # Make it appear near the top

    def draw_header(self, context):
        ob = context.object
        if not ob:
            return

        self.layout.prop(ob.yakuza_file_root_data, "is_valid_root", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        ob = context.object
        if not ob:
            return

        layout.active = ob.yakuza_file_root_data.is_valid_root

        layout.prop(ob.yakuza_file_root_data, "imported_version")
        layout.prop(ob.yakuza_file_root_data, "flags_json")


@dataclass
class LayerSpec:
    """
    Specification for a Blender layer - the name of the layer, and the data it's intended to store
    """
    name: str
    storage: VecStorage


@dataclass
class AttribSetLayerNames:
    """
    Set of Blender layers required for a GMD attribute set/vertex buffer layout
    """
    col0_layer: Optional[LayerSpec]
    col1_layer: Optional[LayerSpec]
    # Used in unskinned, where the normal W component may store information. Skinned meshes don't do that
    normal_w_layer: Optional[LayerSpec]
    # Used in skinned, where only the tangent W component may store information. Skinned meshes calculate tangent XYZ from data
    tangent_w_layer: Optional[LayerSpec]
    # Used for unskinned, where the whole tangent may not be calculated
    tangent_layer: Optional[LayerSpec]
    weight_data_layer: Optional[LayerSpec]
    bone_data_layer: Optional[LayerSpec]
    uv_layers: List[LayerSpec]
    # Index into uv_layers
    primary_uv_i: Optional[int]

    @staticmethod
    def build_from(layout: GMDVertexBufferLayout, is_skinned: bool) -> 'AttribSetLayerNames':
        """
        Look at a GMD vertex buffer layout and determine the required/expected Blender layers.
        For skinned layouts, will assume the weight/bone data are stored in vertex groups instead of custom data layers.

        :param layout: The GMD vertex buffer layout
        :param is_skinned: True if this is intended for a skinned mesh
        :return: The generated AttribSetLayerNames
        """

        # For Col0, Col1, TangentW, UVs
        #   Create layer
        # Color0
        col0_layer = None
        if layout.col0_storage:
            col0_layer = LayerSpec("Color0", layout.col0_storage)

        # Color1
        col1_layer = None
        if layout.col1_storage:
            col1_layer = LayerSpec("Color1", layout.col1_storage)

        # Weight Data
        weight_data_layer = None
        if layout.weights_storage and not is_skinned:
            weight_data_layer = LayerSpec("Weight_Data", layout.weights_storage)

        # Bone Data
        bone_data_layer = None
        if layout.bones_storage and not is_skinned:
            bone_data_layer = LayerSpec("Bone_Data", layout.bones_storage)

        # Normal W data
        normal_w_layer = None
        if layout.normal_storage and layout.normal_storage.n_comps == 4:
            normal_w_layer = LayerSpec("NormalW", layout.normal_storage)

        # Tangent data
        tangent_layer = None
        tangent_w_layer = None
        if is_skinned:
            # For skinned, we may need to store tangent-W
            if layout.tangent_storage and layout.tangent_storage.n_comps == 4:
                tangent_w_layer = LayerSpec("TangentW", layout.tangent_storage)
        else:
            # For unskinned, we may need to store the whole thing
            if layout.tangent_storage:
                tangent_layer = LayerSpec("Tangent", layout.tangent_storage)

        # UVs
        # Yakuza has 3D/4D UV coordinates. Blender doesn't support this in the UV channel.
        # The solution is to have a deterministic "primary UV" designation that can only be 2D
        # This is the only UV loaded into the actual UV layer, the rest are all loaded into vertex colors.

        def get_primary_uv_index() -> Optional[int]:
            for i, uv_storage in enumerate(layout.uv_storages):
                if uv_storage.n_comps == 2:
                    return i
            return None

        primary_uv_i = get_primary_uv_index()

        uv_layers = []
        for i, uv_storage in enumerate(layout.uv_storages):
            if i == primary_uv_i:
                uv_spec = LayerSpec(f"UV_Primary", uv_storage)
            else:
                uv_spec = LayerSpec(f"UV{i}_{uv_storage.n_comps}_components", uv_storage)

            uv_layers.append(uv_spec)

        return AttribSetLayerNames(
            col0_layer=col0_layer,
            col1_layer=col1_layer,
            weight_data_layer=weight_data_layer,
            bone_data_layer=bone_data_layer,
            normal_w_layer=normal_w_layer,
            tangent_layer=tangent_layer,
            tangent_w_layer=tangent_w_layer,
            uv_layers=uv_layers,
            primary_uv_i=primary_uv_i
        )

    def create_on(self, bm: BMesh, error: ErrorReporter) -> 'AttribSetLayers_bmesh':
        """
        Given a BMesh, create the necessary data layers, reusing pre-existing ones if present.

        :param bm: The mesh to add the layers to
        :param error: The error reporter used to report debug messages
        :return: A structure containing the layers
        """

        def create_color_layer(spec: Optional[LayerSpec], purpose: str) -> Optional[BMLayerCollection]:
            if spec is None:
                return None
            if spec.name in bm.loops.layers.float_color:
                return bm.loops.layers.float_color[spec.name]
            error.debug("MESH",
                        f"Creating color layer {spec.name} for {purpose}: storage {spec.storage}")
            return bm.loops.layers.float_color.new(spec.name)

        def create_uv_layer(spec: Optional[LayerSpec], purpose: str) -> Optional[BMLayerCollection]:
            if spec is None:
                return None
            if spec.name in bm.loops.layers.uv:
                return bm.loops.layers.uv[spec.name]
            error.debug("MESH",
                        f"Creating UV layer {spec.name} for {purpose}: storage {spec.storage}")
            return bm.loops.layers.uv.new(spec.name)

        col0_layer = create_color_layer(self.col0_layer, "Color0")
        col1_layer = create_color_layer(self.col1_layer, "Color1")
        weight_data_layer = create_color_layer(self.weight_data_layer, "WeightData")
        bone_data_layer = create_color_layer(self.bone_data_layer, "BoneData")
        normal_w_layer = create_color_layer(self.normal_w_layer, "NormalW")
        tangent_layer = create_color_layer(self.tangent_layer, "Tangent")
        tangent_w_layer = create_color_layer(self.tangent_w_layer, "TangentW")

        if self.primary_uv_i is not None:
            error.debug("MESH", f"Using UV{self.primary_uv_i} as primary UV layer")
            assert self.uv_layers[self.primary_uv_i].storage.n_comps == 2

        uv_layers = []
        for i, uv_spec in enumerate(self.uv_layers):
            if uv_spec.storage.n_comps == 2:
                uv_layer = create_uv_layer(uv_spec, f"UV{i}")
            else:
                uv_layer = create_color_layer(uv_spec, f"UV{i}")
            assert uv_layer is not None

            uv_layers.append((uv_spec.storage.n_comps, uv_layer))

        return AttribSetLayers_bmesh(
            col0_layer=col0_layer,
            col1_layer=col1_layer,
            weight_data_layer=weight_data_layer,
            bone_data_layer=bone_data_layer,
            normal_w_layer=normal_w_layer,
            tangent_layer=tangent_layer,
            tangent_w_layer=tangent_w_layer,
            uv_layers=uv_layers,
            primary_uv_i=self.primary_uv_i,
        )

    def try_retrieve_from(self, mesh: bpy.types.Mesh, error: ErrorReporter) -> 'AttribSetLayers_bpy':
        """
        Given a bpy mesh, retrieve the layers that are present.
        May not return all expected layers - the mesh may not have some, e.g. a mesh with a material that requires Color0 may not have it.
        In that case, a warning will be reported.

        :param mesh: The mesh to retrieve layers from
        :param error: The error reporter used to report debug messages and warnings
        :return: A structure containing the existing layers
        """

        def retrieve_color_layer(spec: Optional[LayerSpec], purpose: str) -> Optional[bpy.types.MeshLoopColorLayer]:
            if spec is None:
                return None
            attr = mesh.color_attributes[spec.name] if spec.name in mesh.color_attributes else None
            if attr:
                if attr.domain != 'CORNER':
                    error.fatal(f"Found color layer {spec.name} for {purpose}: storage {spec.storage}, "
                                f"but has wrong domain {attr.domain} - expected CORNER.")
                error.debug("MESH",
                            f"Retrieved color layer {spec.name} for {purpose}: storage {spec.storage}")
                return attr
            else:
                error.info(f"Expected {mesh.name} to have a color layer {spec.name} for {purpose}: "
                           f"storage {spec.storage} "
                           f"but found None")
                return None

        def retrieve_uv_layer(spec: Optional[LayerSpec], purpose: str) -> Optional[bpy.types.MeshUVLoopLayer]:
            if spec is None:
                return None
            layer = mesh.uv_layers[spec.name] if spec.name in mesh.uv_layers else None
            if layer:
                error.debug("MESH",
                            f"Retrieved UV layer {spec.name} for {purpose}: storage {spec.storage}")
            else:
                error.info(f"Expected {mesh.name} to have a UV layer {spec.name} for {purpose}: "
                           f"storage {spec.storage}, "
                           f"but found None")
            return layer

        col0_layer = retrieve_color_layer(self.col0_layer, "Color0")
        col1_layer = retrieve_color_layer(self.col1_layer, "Color1")
        weight_data_layer = retrieve_color_layer(self.weight_data_layer, "WeightData")
        bone_data_layer = retrieve_color_layer(self.bone_data_layer, "BoneData")
        normal_w_layer = retrieve_color_layer(self.normal_w_layer, "NormalW")
        tangent_layer = retrieve_color_layer(self.tangent_layer, "Tangent")
        tangent_w_layer = retrieve_color_layer(self.tangent_w_layer, "TangentW")

        if self.primary_uv_i is not None:
            error.debug("MESH", f"Using UV{self.primary_uv_i} as primary UV layer")
            assert self.uv_layers[self.primary_uv_i].storage.n_comps == 2

        uv_layers = []
        for i, uv_spec in enumerate(self.uv_layers):
            uv_layer: Optional[Union[bpy.types.MeshLoopColorLayer, bpy.types.MeshUVLoopLayer]]
            if uv_spec.storage.n_comps == 2:
                uv_layer = retrieve_uv_layer(uv_spec, f"UV{i}")
            else:
                uv_layer = retrieve_color_layer(uv_spec, f"UV{i}")

            uv_layers.append((uv_spec.storage.n_comps, uv_layer))

        if self.primary_uv_i is not None and uv_layers[self.primary_uv_i][1] is None:
            # Fallback for finding the primary map
            # If the "primary map" is not already used for a layer, use it
            if not ((2, mesh.uv_layers.active) in uv_layers):
                uv_layers[self.primary_uv_i] = (2, mesh.uv_layers.active)
                error.debug("MESH",
                            f"Using UVlayer {mesh.uv_layers.active.name} as the primary UV map - it is otherwise unused")
            else:
                error.recoverable(f"Tried to find the primary UV map for {mesh.name}, but couldn't. "
                                  f"The currently in-use UV map {mesh.uv_layers.active.name} is already used for a "
                                  f"different UV layer.")

        return AttribSetLayers_bpy(
            col0_layer=col0_layer,
            col1_layer=col1_layer,
            weight_data_layer=weight_data_layer,
            bone_data_layer=bone_data_layer,
            normal_w_layer=normal_w_layer,
            tangent_layer=tangent_layer,
            tangent_w_layer=tangent_w_layer,
            uv_layers=uv_layers,
            primary_uv_i=self.primary_uv_i,
        )

    def get_blender_uv_layers(self) -> List[str]:
        """
        Return a list of the layer names this expects to be present as UV layers
        """
        return [
            spec.name
            for spec in self.uv_layers
            if spec.storage.n_comps == 2
        ]

    def get_blender_color_layers(self) -> List[str]:
        """
        Return a list of the layer names this expects to be present as vertex color layers
        """
        color_layers = []
        if self.col0_layer:
            color_layers.append(self.col0_layer.name)
        if self.col1_layer:
            color_layers.append(self.col1_layer.name)
        if self.weight_data_layer:
            color_layers.append(self.weight_data_layer.name)
        if self.bone_data_layer:
            color_layers.append(self.bone_data_layer.name)
        if self.normal_w_layer:
            color_layers.append(self.normal_w_layer.name)
        if self.tangent_layer:
            color_layers.append(self.tangent_layer.name)
        if self.tangent_w_layer:
            color_layers.append(self.tangent_w_layer.name)
        return color_layers + [
            spec.name
            for spec in self.uv_layers
            if spec.storage.n_comps != 2
        ]


@dataclass
class AttribSetLayers_bpy:
    """
    Set of Blender layers used by the exporter to retrieve relevant vertex data
    """
    col0_layer: Optional[bpy.types.FloatColorAttribute]
    col1_layer: Optional[bpy.types.FloatColorAttribute]
    weight_data_layer: Optional[bpy.types.FloatColorAttribute]
    bone_data_layer: Optional[bpy.types.FloatColorAttribute]
    normal_w_layer: Optional[bpy.types.FloatColorAttribute]
    tangent_layer: Optional[bpy.types.FloatColorAttribute]
    tangent_w_layer: Optional[bpy.types.FloatColorAttribute]
    # Stores (component length, layer)
    uv_layers: List[Tuple[int, Optional[Union[bpy.types.FloatColorAttribute, bpy.types.MeshUVLoopLayer]]]]
    primary_uv_i: Optional[int]


@dataclass
class AttribSetLayers_bmesh:
    """
    Set of Blender layers used by the importer to create relevant vertex data
    """
    col0_layer: Optional[BMLayerCollection]
    col1_layer: Optional[BMLayerCollection]
    weight_data_layer: Optional[BMLayerCollection]
    bone_data_layer: Optional[BMLayerCollection]
    normal_w_layer: Optional[BMLayerCollection]
    tangent_layer: Optional[BMLayerCollection]
    tangent_w_layer: Optional[BMLayerCollection]
    # Stores (component length, layer)
    uv_layers: List[Tuple[int, BMLayerCollection]]
    primary_uv_i: Optional[int]
