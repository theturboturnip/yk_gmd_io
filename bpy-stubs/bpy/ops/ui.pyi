"""


Ui Operators
************

:func:`assign_default_button`

:func:`button_execute`

:func:`button_string_clear`

:func:`copy_as_driver_button`

:func:`copy_data_path_button`

:func:`copy_python_command_button`

:func:`copy_to_selected_button`

:func:`drop_color`

:func:`drop_name`

:func:`editsource`

:func:`edittranslation_init`

:func:`eyedropper_color`

:func:`eyedropper_colorramp`

:func:`eyedropper_colorramp_point`

:func:`eyedropper_depth`

:func:`eyedropper_driver`

:func:`eyedropper_gpencil_color`

:func:`eyedropper_id`

:func:`jump_to_target_button`

:func:`list_start_filter`

:func:`override_remove_button`

:func:`override_type_set_button`

:func:`reloadtranslation`

:func:`reset_default_button`

:func:`tree_view_drop`

:func:`tree_view_item_rename`

:func:`unset_property_button`

"""

import typing

def assign_default_button() -> None:

  """

  Set this property's current value as the new default

  """

  ...

def button_execute(skip_depressed: bool = False) -> None:

  """

  Presses active button

  """

  ...

def button_string_clear() -> None:

  """

  Unsets the text of the active button

  """

  ...

def copy_as_driver_button() -> None:

  """

  Create a new driver with this property as input, and copy it to the clipboard. Use Paste Driver to add it to the target property, or Paste Driver Variables to extend an existing driver

  """

  ...

def copy_data_path_button(full_path: bool = False) -> None:

  """

  Copy the RNA data path for this property to the clipboard

  """

  ...

def copy_python_command_button() -> None:

  """

  Copy the Python command matching this button

  """

  ...

def copy_to_selected_button(all: bool = True) -> None:

  """

  Copy property from this object to selected objects or bones

  """

  ...

def drop_color(color: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), gamma: bool = False) -> None:

  """

  Drop colors to buttons

  """

  ...

def drop_name(string: str = '') -> None:

  """

  Drop name to button

  """

  ...

def editsource() -> None:

  """

  Edit UI source code of the active button

  """

  ...

def edittranslation_init() -> None:

  """

  Edit i18n in current language for the active button

  """

  ...

def eyedropper_color() -> None:

  """

  Sample a color from the Blender window to store in a property

  """

  ...

def eyedropper_colorramp() -> None:

  """

  Sample a color band

  """

  ...

def eyedropper_colorramp_point() -> None:

  """

  Point-sample a color band

  """

  ...

def eyedropper_depth() -> None:

  """

  Sample depth from the 3D view

  """

  ...

def eyedropper_driver(mapping_type: str = 'SINGLE_MANY') -> None:

  """

  Pick a property to use as a driver target

  """

  ...

def eyedropper_gpencil_color(mode: str = 'MATERIAL') -> None:

  """

  Sample a color from the Blender Window and create Grease Pencil material

  """

  ...

def eyedropper_id() -> None:

  """

  Sample a data-block from the 3D View to store in a property

  """

  ...

def jump_to_target_button() -> None:

  """

  Switch to the target object or bone

  """

  ...

def list_start_filter() -> None:

  """

  Start entering filter text for the list in focus

  """

  ...

def override_remove_button(all: bool = True) -> None:

  """

  Remove an override operation

  """

  ...

def override_type_set_button(all: bool = True, type: str = 'REPLACE') -> None:

  """

  Create an override operation, or set the type of an existing one

  """

  ...

def reloadtranslation() -> None:

  """

  Force a full reload of UI translation

  """

  ...

def reset_default_button(all: bool = True) -> None:

  """

  Reset this property's value to its default value

  """

  ...

def tree_view_drop() -> None:

  """

  Drag and drop items onto a tree item

  """

  ...

def tree_view_item_rename() -> None:

  """

  Rename the active item in the tree

  """

  ...

def unset_property_button() -> None:

  """

  Clear the property and use default or generated value in operators

  """

  ...
