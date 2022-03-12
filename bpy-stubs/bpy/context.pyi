"""


Context Access (bpy.context)
****************************

The context members available depend on the area of Blender which is currently being accessed.

Note that all context values are readonly,
but may be modified through the data API or by running operators


Global Context
==============

These properties are available in any contexts.

:data:`area`

:data:`asset_file_handle`

:data:`blend_data`

:data:`collection`

:data:`engine`

:data:`gizmo_group`

:data:`layer_collection`

:data:`mode`

:data:`preferences`

:data:`region`

:data:`region_data`

:data:`scene`

:data:`screen`

:data:`space_data`

:data:`tool_settings`

:data:`view_layer`

:data:`window`

:data:`window_manager`

:data:`workspace`


Screen Context
==============

:data:`scene`

:data:`view_layer`

:data:`visible_objects`

:data:`selectable_objects`

:data:`selected_objects`

:data:`editable_objects`

:data:`selected_editable_objects`

:data:`objects_in_mode`

:data:`objects_in_mode_unique_data`

:data:`visible_bones`

:data:`editable_bones`

:data:`selected_bones`

:data:`selected_editable_bones`

:data:`visible_pose_bones`

:data:`selected_pose_bones`

:data:`selected_pose_bones_from_active_object`

:data:`active_bone`

:data:`active_pose_bone`

:data:`active_object`

:data:`object`

:data:`edit_object`

:data:`sculpt_object`

:data:`vertex_paint_object`

:data:`weight_paint_object`

:data:`image_paint_object`

:data:`particle_edit_object`

:data:`pose_object`

:data:`active_sequence_strip`

:data:`sequences`

:data:`selected_sequences`

:data:`selected_editable_sequences`

:data:`active_nla_track`

:data:`active_nla_strip`

:data:`selected_nla_strips`

:data:`selected_movieclip_tracks`

:data:`gpencil_data`

:data:`gpencil_data_owner`

:data:`annotation_data`

:data:`annotation_data_owner`

:data:`visible_gpencil_layers`

:data:`editable_gpencil_layers`

:data:`editable_gpencil_strokes`

:data:`active_gpencil_layer`

:data:`active_gpencil_frame`

:data:`active_annotation_layer`

:data:`active_operator`

:data:`visible_fcurves`

:data:`editable_fcurves`

:data:`selected_visible_fcurves`

:data:`selected_editable_fcurves`

:data:`active_editable_fcurve`

:data:`selected_editable_keyframes`

:data:`ui_list`

:data:`asset_library_ref`


View3D Context
==============

:data:`active_object`

:data:`selected_ids`


Buttons Context
===============

:data:`texture_slot`

:data:`scene`

:data:`world`

:data:`object`

:data:`mesh`

:data:`armature`

:data:`lattice`

:data:`curve`

:data:`meta_ball`

:data:`light`

:data:`speaker`

:data:`lightprobe`

:data:`camera`

:data:`material`

:data:`material_slot`

:data:`texture`

:data:`texture_user`

:data:`texture_user_property`

:data:`bone`

:data:`edit_bone`

:data:`pose_bone`

:data:`particle_system`

:data:`particle_system_editable`

:data:`particle_settings`

:data:`cloth`

:data:`soft_body`

:data:`fluid`

:data:`collision`

:data:`brush`

:data:`dynamic_paint`

:data:`line_style`

:data:`collection`

:data:`gpencil`

:data:`volume`


Image Context
=============

:data:`edit_image`

:data:`edit_mask`


Node Context
============

:data:`selected_nodes`

:data:`active_node`

:data:`light`

:data:`material`

:data:`world`


Text Context
============

:data:`edit_text`


Clip Context
============

:data:`edit_movieclip`

:data:`edit_mask`


Sequencer Context
=================

:data:`edit_mask`


File Context
============

:data:`active_file`

:data:`selected_files`

:data:`asset_library_ref`

:data:`selected_asset_files`

:data:`id`

"""

import typing

import bpy

area: bpy.types.Area = ...

asset_file_handle: bpy.types.FileSelectEntry = ...

"""

The file of an active asset. Avoid using this, it will be replaced by a proper AssetHandle design

"""

blend_data: bpy.types.BlendData = ...

collection: bpy.types.Collection = ...

engine: str = ...

gizmo_group: bpy.types.GizmoGroup = ...

layer_collection: bpy.types.LayerCollection = ...

mode: str = ...

preferences: bpy.types.Preferences = ...

region: bpy.types.Region = ...

region_data: bpy.types.RegionView3D = ...

scene: bpy.types.Scene = ...

screen: bpy.types.Screen = ...

space_data: bpy.types.Space = ...

tool_settings: bpy.types.ToolSettings = ...

view_layer: bpy.types.ViewLayer = ...

window: bpy.types.Window = ...

window_manager: bpy.types.WindowManager = ...

workspace: bpy.types.WorkSpace = ...

scene: bpy.types.Scene = ...

view_layer: bpy.types.ViewLayer = ...

visible_objects: typing.Sequence[typing.Any] = ...

selectable_objects: typing.Sequence[typing.Any] = ...

selected_objects: typing.Sequence[typing.Any] = ...

editable_objects: typing.Sequence[typing.Any] = ...

selected_editable_objects: typing.Sequence[typing.Any] = ...

objects_in_mode: typing.Sequence[typing.Any] = ...

objects_in_mode_unique_data: typing.Sequence[typing.Any] = ...

visible_bones: typing.Sequence[typing.Any] = ...

editable_bones: typing.Sequence[typing.Any] = ...

selected_bones: typing.Sequence[typing.Any] = ...

selected_editable_bones: typing.Sequence[typing.Any] = ...

visible_pose_bones: typing.Sequence[typing.Any] = ...

selected_pose_bones: typing.Sequence[typing.Any] = ...

selected_pose_bones_from_active_object: typing.Sequence[typing.Any] = ...

active_bone: bpy.types.EditBone = ...

active_pose_bone: bpy.types.PoseBone = ...

active_object: bpy.types.Object = ...

object: bpy.types.Object = ...

edit_object: bpy.types.Object = ...

sculpt_object: bpy.types.Object = ...

vertex_paint_object: bpy.types.Object = ...

weight_paint_object: bpy.types.Object = ...

image_paint_object: bpy.types.Object = ...

particle_edit_object: bpy.types.Object = ...

pose_object: bpy.types.Object = ...

active_sequence_strip: bpy.types.Sequence = ...

sequences: typing.Sequence[typing.Any] = ...

selected_sequences: typing.Sequence[typing.Any] = ...

selected_editable_sequences: typing.Sequence[typing.Any] = ...

active_nla_track: bpy.types.NlaTrack = ...

active_nla_strip: bpy.types.NlaStrip = ...

selected_nla_strips: typing.Sequence[typing.Any] = ...

selected_movieclip_tracks: typing.Sequence[typing.Any] = ...

gpencil_data: bpy.types.GreasePencil = ...

gpencil_data_owner: bpy.types.ID = ...

annotation_data: bpy.types.GreasePencil = ...

annotation_data_owner: bpy.types.ID = ...

visible_gpencil_layers: typing.Sequence[typing.Any] = ...

editable_gpencil_layers: typing.Sequence[typing.Any] = ...

editable_gpencil_strokes: typing.Sequence[typing.Any] = ...

active_gpencil_layer: typing.Sequence[typing.Any] = ...

active_gpencil_frame: typing.Sequence[typing.Any] = ...

active_annotation_layer: bpy.types.GPencilLayer = ...

active_operator: bpy.types.Operator = ...

visible_fcurves: typing.Sequence[typing.Any] = ...

editable_fcurves: typing.Sequence[typing.Any] = ...

selected_visible_fcurves: typing.Sequence[typing.Any] = ...

selected_editable_fcurves: typing.Sequence[typing.Any] = ...

active_editable_fcurve: bpy.types.FCurve = ...

selected_editable_keyframes: typing.Sequence[typing.Any] = ...

ui_list: bpy.types.UIList = ...

asset_library_ref: bpy.types.AssetLibraryReference = ...

active_object: bpy.types.Object = ...

selected_ids: typing.Sequence[typing.Any] = ...

texture_slot: bpy.types.MaterialTextureSlot = ...

scene: bpy.types.Scene = ...

world: bpy.types.World = ...

object: bpy.types.Object = ...

mesh: bpy.types.Mesh = ...

armature: bpy.types.Armature = ...

lattice: bpy.types.Lattice = ...

curve: bpy.types.Curve = ...

meta_ball: bpy.types.MetaBall = ...

light: bpy.types.Light = ...

speaker: bpy.types.Speaker = ...

lightprobe: bpy.types.LightProbe = ...

camera: bpy.types.Camera = ...

material: bpy.types.Material = ...

material_slot: bpy.types.MaterialSlot = ...

texture: bpy.types.Texture = ...

texture_user: bpy.types.ID = ...

texture_user_property: bpy.types.Property = ...

bone: bpy.types.Bone = ...

edit_bone: bpy.types.EditBone = ...

pose_bone: bpy.types.PoseBone = ...

particle_system: bpy.types.ParticleSystem = ...

particle_system_editable: bpy.types.ParticleSystem = ...

particle_settings: bpy.types.ParticleSettings = ...

cloth: bpy.types.ClothModifier = ...

soft_body: bpy.types.SoftBodyModifier = ...

fluid: bpy.types.FluidSimulationModifier = ...

collision: bpy.types.CollisionModifier = ...

brush: bpy.types.Brush = ...

dynamic_paint: bpy.types.DynamicPaintModifier = ...

line_style: bpy.types.FreestyleLineStyle = ...

collection: bpy.types.LayerCollection = ...

gpencil: bpy.types.GreasePencil = ...

volume: bpy.types.Volume = ...

edit_image: bpy.types.Image = ...

edit_mask: bpy.types.Mask = ...

selected_nodes: typing.Sequence[typing.Any] = ...

active_node: bpy.types.Node = ...

light: bpy.types.Light = ...

material: bpy.types.Material = ...

world: bpy.types.World = ...

edit_text: bpy.types.Text = ...

edit_movieclip: bpy.types.MovieClip = ...

edit_mask: bpy.types.Mask = ...

edit_mask: bpy.types.Mask = ...

active_file: bpy.types.FileSelectEntry = ...

selected_files: typing.Sequence[typing.Any] = ...

asset_library_ref: bpy.types.AssetLibraryReference = ...

selected_asset_files: typing.Sequence[typing.Any] = ...

id: bpy.types.ID = ...
