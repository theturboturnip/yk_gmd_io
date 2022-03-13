"""


Property Definitions (bpy.props)
********************************

This module defines properties to extend Blender's internal data. The result of these functions is used to assign properties to classes registered with Blender and can't be used directly.

Note: All parameters to these functions must be passed as keywords.


Assigning to Existing Classes
=============================

Custom properties can be added to any subclass of an :class:`ID`,
:class:`Bone` and :class:`PoseBone`.

These properties can be animated, accessed by the user interface and python
like Blender's existing properties.

.. code::

  import bpy

  # Assign a custom property to an existing type.
  bpy.types.Material.custom_float = bpy.props.FloatProperty(name="Test Property")

  # Test the property is there.
  bpy.data.materials[0].custom_float = 5.0


Operator Example
================

A common use of custom properties is for python based :class:`Operator`
classes. Test this code by running it in the text editor, or by clicking the
button in the 3D Viewport's Tools panel. The latter will show the properties
in the Redo panel and allow you to change them.

.. code::

  import bpy


  class OBJECT_OT_property_example(bpy.types.Operator):
      bl_idname = "object.property_example"
      bl_label = "Property Example"
      bl_options = {'REGISTER', 'UNDO'}

      my_float: bpy.props.FloatProperty(name="Some Floating Point")
      my_bool: bpy.props.BoolProperty(name="Toggle Option")
      my_string: bpy.props.StringProperty(name="String Value")

      def execute(self, context):
          self.report(
              {'INFO'}, 'F: %.2f  B: %s  S: %r' %
              (self.my_float, self.my_bool, self.my_string)
          )
          print('My float:', self.my_float)
          print('My bool:', self.my_bool)
          print('My string:', self.my_string)
          return {'FINISHED'}


  class OBJECT_PT_property_example(bpy.types.Panel):
      bl_idname = "object_PT_property_example"
      bl_label = "Property Example"
      bl_space_type = 'VIEW_3D'
      bl_region_type = 'UI'
      bl_category = "Tool"

      def draw(self, context):
          # You can set the property values that should be used when the user
          # presses the button in the UI.
          props = self.layout.operator('object.property_example')
          props.my_bool = True
          props.my_string = "Shouldn't that be 47?"

          # You can set properties dynamically:
          if context.object:
              props.my_float = context.object.location.x
          else:
              props.my_float = 327


  bpy.utils.register_class(OBJECT_OT_property_example)
  bpy.utils.register_class(OBJECT_PT_property_example)

  # Demo call. Be sure to also test in the 3D Viewport.
  bpy.ops.object.property_example(
      my_float=47,
      my_bool=True,
      my_string="Shouldn't that be 327?",
  )


PropertyGroup Example
=====================

PropertyGroups can be used for collecting custom settings into one value
to avoid many individual settings mixed in together.

.. code::

  import bpy


  class MaterialSettings(bpy.types.PropertyGroup):
      my_int: bpy.props.IntProperty()
      my_float: bpy.props.FloatProperty()
      my_string: bpy.props.StringProperty()


  bpy.utils.register_class(MaterialSettings)

  bpy.types.Material.my_settings = bpy.props.PointerProperty(type=MaterialSettings)

  # test the new settings work
  material = bpy.data.materials[0]

  material.my_settings.my_int = 5
  material.my_settings.my_float = 3.0
  material.my_settings.my_string = "Foo"


Collection Example
==================

Custom properties can be added to any subclass of an :class:`ID`,
:class:`Bone` and :class:`PoseBone`.

.. code::

  import bpy


  # Assign a collection.
  class SceneSettingItem(bpy.types.PropertyGroup):
      name: bpy.props.StringProperty(name="Test Property", default="Unknown")
      value: bpy.props.IntProperty(name="Test Property", default=22)


  bpy.utils.register_class(SceneSettingItem)

  bpy.types.Scene.my_settings = bpy.props.CollectionProperty(type=SceneSettingItem)

  # Assume an armature object selected.
  print("Adding 2 values!")

  my_item = bpy.context.scene.my_settings.add()
  my_item.name = "Spam"
  my_item.value = 1000

  my_item = bpy.context.scene.my_settings.add()
  my_item.name = "Eggs"
  my_item.value = 30

  for my_item in bpy.context.scene.my_settings:
      print(my_item.name, my_item.value)


Update Example
==============

It can be useful to perform an action when a property is changed and can be
used to update other properties or synchronize with external data.

All properties define update functions except for CollectionProperty.

.. code::

  import bpy


  def update_func(self, context):
      print("my test function", self)


  bpy.types.Scene.testprop = bpy.props.FloatProperty(update=update_func)

  bpy.context.scene.testprop = 11.0

  # >>> my test function <bpy_struct, Scene("Scene")>


Getter/Setter Example
=====================

Getter/setter functions can be used for boolean, int, float, string and enum properties.
If these callbacks are defined the property will not be stored in the ID properties
automatically. Instead, the *get* and *set* functions will be called when the property
is respectively read or written from the API.

.. code::

  import bpy


  # Simple property reading/writing from ID properties.
  # This is what the RNA would do internally.
  def get_float(self):
      return self["testprop"]


  def set_float(self, value):
      self["testprop"] = value


  bpy.types.Scene.test_float = bpy.props.FloatProperty(get=get_float, set=set_float)


  # Read-only string property, returns the current date
  def get_date(self):
      import datetime
      return str(datetime.datetime.now())


  bpy.types.Scene.test_date = bpy.props.StringProperty(get=get_date)


  # Boolean array. Set function stores a single boolean value, returned as the second component.
  # Array getters must return a list or tuple
  # Array size must match the property vector size exactly
  def get_array(self):
      return (True, self["somebool"])


  def set_array(self, values):
      self["somebool"] = values[0] and values[1]


  bpy.types.Scene.test_array = bpy.props.BoolVectorProperty(size=2, get=get_array, set=set_array)


  # Enum property.
  # Note: the getter/setter callback must use integer identifiers!
  test_items = [
      ("RED", "Red", "", 1),
      ("GREEN", "Green", "", 2),
      ("BLUE", "Blue", "", 3),
      ("YELLOW", "Yellow", "", 4),
  ]


  def get_enum(self):
      import random
      return random.randint(1, 4)


  def set_enum(self, value):
      print("setting value", value)


  bpy.types.Scene.test_enum = bpy.props.EnumProperty(items=test_items, get=get_enum, set=set_enum)


  # Testing the properties:
  scene = bpy.context.scene

  scene.test_float = 12.34
  print('test_float:', scene.test_float)

  scene.test_array = (True, False)
  print('test_array:', tuple(scene.test_array))

  # scene.test_date = "blah"   # this would fail, property is read-only
  print('test_date:', scene.test_date)

  scene.test_enum = 'BLUE'
  print('test_enum:', scene.test_enum)

  # The above outputs:
  # test_float: 12.34000015258789
  # test_array: (True, False)
  # test_date: 2018-03-14 11:36:53.158653
  # setting value 3
  # test_enum: GREEN

:func:`BoolProperty`

:func:`BoolVectorProperty`

:func:`CollectionProperty`

:func:`EnumProperty`

:func:`FloatProperty`

:func:`FloatVectorProperty`

:func:`IntProperty`

:func:`IntVectorProperty`

:func:`PointerProperty`

:func:`RemoveProperty`

Note: Typically this function doesn't need to be accessed directly.
Instead use ``del cls.attr``

:func:`StringProperty`

"""

import typing

def BoolProperty(name: str = '', description: str = '', default: typing.Any = False, options: typing.Set[typing.Any] = {'ANIMATABLE'}, override: typing.Set[typing.Any] = set(), tags: typing.Set[typing.Any] = set(), subtype: str = 'NONE', update: typing.Callable = None, get: typing.Callable = None, set: typing.Callable = None) -> None:

  """

  Returns a new boolean property definition.

  """

  ...

def BoolVectorProperty(name: str = '', description: str = '', default: typing.Sequence[typing.Any] = (False, False, False), options: typing.Set[typing.Any] = {'ANIMATABLE'}, override: typing.Set[typing.Any] = set(), tags: typing.Set[typing.Any] = set(), subtype: str = 'NONE', size: int = 3, update: typing.Callable = None, get: typing.Callable = None, set: typing.Callable = None) -> None:

  """

  Returns a new vector boolean property definition.

  """

  ...

def CollectionProperty(type: typing.Type = None, name: str = '', description: str = '', options: typing.Set[typing.Any] = {'ANIMATABLE'}, override: typing.Set[typing.Any] = set(), tags: typing.Set[typing.Any] = set()) -> None:

  """

  Returns a new collection property definition.

  """

  ...

def EnumProperty(items: typing.Sequence[typing.Tuple[str, ...]], name: str = '', description: str = '', default: str = None, options: typing.Set[typing.Any] = {'ANIMATABLE'}, override: typing.Set[typing.Any] = set(), tags: typing.Set[typing.Any] = set(), update: typing.Callable = None, get: typing.Callable = None, set: typing.Callable = None) -> None:

  """

  Returns a new enumerator property definition.

  """

  ...

def FloatProperty(name: str = '', description: str = '', default: typing.Any = 0.0, min: float = -3.402823e+38, max: float = 3.402823e+38, soft_min: float = -3.402823e+38, soft_max: float = 3.402823e+38, step: int = 3, precision: int = 2, options: typing.Set[typing.Any] = {'ANIMATABLE'}, override: typing.Set[typing.Any] = set(), tags: typing.Set[typing.Any] = set(), subtype: str = 'NONE', unit: str = 'NONE', update: typing.Callable = None, get: typing.Callable = None, set: typing.Callable = None) -> None:

  """

  Returns a new float (single precision) property definition.

  """

  ...

def FloatVectorProperty(name: str = '', description: str = '', default: typing.Sequence[typing.Any] = (0.0, 0.0, 0.0), min: float = sys.float_info.min, max: float = sys.float_info.max, soft_min: float = sys.float_info.min, soft_max: float = sys.float_info.max, step: int = 3, precision: int = 2, options: typing.Set[typing.Any] = {'ANIMATABLE'}, override: typing.Set[typing.Any] = set(), tags: typing.Set[typing.Any] = set(), subtype: str = 'NONE', unit: str = 'NONE', size: int = 3, update: typing.Callable = None, get: typing.Callable = None, set: typing.Callable = None) -> None:

  """

  Returns a new vector float property definition.

  """

  ...

def IntProperty(name: str = '', description: str = '', default: typing.Any = 0, min: int = -2 ** args31, max: int = 2 ** args31 - 1, soft_min: int = -2 ** args31, soft_max: int = 2 ** args31 - 1, step: int = 1, options: typing.Set[typing.Any] = {'ANIMATABLE'}, override: typing.Set[typing.Any] = set(), tags: typing.Set[typing.Any] = set(), subtype: str = 'NONE', update: typing.Callable = None, get: typing.Callable = None, set: typing.Callable = None) -> None:

  """

  Returns a new int property definition.

  """

  ...

def IntVectorProperty(name: str = '', description: str = '', default: typing.Sequence[typing.Any] = (0, 0, 0), min: int = -2 ** args31, max: int = 2 ** args31 - 1, soft_min: int = -2 ** args31, soft_max: int = 2 ** args31 - 1, step: int = 1, options: typing.Set[typing.Any] = {'ANIMATABLE'}, override: typing.Set[typing.Any] = set(), tags: typing.Set[typing.Any] = set(), subtype: str = 'NONE', size: int = 3, update: typing.Callable = None, get: typing.Callable = None, set: typing.Callable = None) -> None:

  """

  Returns a new vector int property definition.

  """

  ...

def PointerProperty(type: typing.Type = None, name: str = '', description: str = '', options: typing.Set[typing.Any] = {'ANIMATABLE'}, override: typing.Set[typing.Any] = set(), tags: typing.Set[typing.Any] = set(), poll: typing.Callable = None, update: typing.Callable = None) -> None:

  """

  Returns a new pointer property definition.

  """

  ...

def RemoveProperty(cls: typing.Type, attr: str) -> None:

  """

  Removes a dynamically defined property.

  """

  ...

def StringProperty(name: str = '', description: str = '', default: str = '', maxlen: int = 0, options: typing.Set[typing.Any] = {'ANIMATABLE'}, override: typing.Set[typing.Any] = set(), tags: typing.Set[typing.Any] = set(), subtype: str = 'NONE', update: typing.Callable = None, get: typing.Callable = None, set: typing.Callable = None) -> None:

  """

  Returns a new string property definition.

  """

  ...
