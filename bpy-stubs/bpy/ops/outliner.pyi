"""


Outliner Operators
******************

:func:`action_set`

:func:`animdata_operation`

:func:`collection_color_tag_set`

:func:`collection_disable`

:func:`collection_disable_render`

:func:`collection_drop`

:func:`collection_duplicate`

:func:`collection_duplicate_linked`

:func:`collection_enable`

:func:`collection_enable_render`

:func:`collection_exclude_clear`

:func:`collection_exclude_set`

:func:`collection_hide`

:func:`collection_hide_inside`

:func:`collection_hierarchy_delete`

:func:`collection_holdout_clear`

:func:`collection_holdout_set`

:func:`collection_indirect_only_clear`

:func:`collection_indirect_only_set`

:func:`collection_instance`

:func:`collection_isolate`

:func:`collection_link`

:func:`collection_new`

:func:`collection_objects_deselect`

:func:`collection_objects_select`

:func:`collection_show`

:func:`collection_show_inside`

:func:`constraint_operation`

:func:`data_operation`

:func:`datastack_drop`

:func:`delete`

:func:`drivers_add_selected`

:func:`drivers_delete_selected`

:func:`expanded_toggle`

:func:`hide`

:func:`highlight_update`

:func:`id_copy`

:func:`id_delete`

:func:`id_operation`

:func:`id_paste`

:func:`id_remap`

:func:`item_activate`

:func:`item_drag_drop`

:func:`item_openclose`

:func:`item_rename`

:func:`keyingset_add_selected`

:func:`keyingset_remove_selected`

:func:`lib_operation`

:func:`lib_relocate`

:func:`material_drop`

:func:`modifier_operation`

:func:`object_operation`

:func:`operation`

:func:`orphans_purge`

:func:`parent_clear`

:func:`parent_drop`

:func:`scene_drop`

:func:`scene_operation`

:func:`scroll_page`

:func:`select_all`

:func:`select_box`

:func:`select_walk`

:func:`show_active`

:func:`show_hierarchy`

:func:`show_one_level`

:func:`unhide_all`

"""

import typing

def action_set(action: str = '') -> None:

  """

  Change the active action used

  """

  ...

def animdata_operation(type: str = 'CLEAR_ANIMDATA') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def collection_color_tag_set(color: str = 'NONE') -> None:

  """

  Set a color tag for the selected collections

  """

  ...

def collection_disable() -> None:

  """

  Disable viewport display in the view layers

  """

  ...

def collection_disable_render() -> None:

  """

  Do not render this collection

  """

  ...

def collection_drop() -> None:

  """

  Drag to move to collection in Outliner

  """

  ...

def collection_duplicate() -> None:

  """

  Recursively duplicate the collection, all its children, objects and object data

  """

  ...

def collection_duplicate_linked() -> None:

  """

  Recursively duplicate the collection, all its children and objects, with linked object data

  """

  ...

def collection_enable() -> None:

  """

  Enable viewport display in the view layers

  """

  ...

def collection_enable_render() -> None:

  """

  Render the collection

  """

  ...

def collection_exclude_clear() -> None:

  """

  Include collection in the active view layer

  """

  ...

def collection_exclude_set() -> None:

  """

  Exclude collection from the active view layer

  """

  ...

def collection_hide() -> None:

  """

  Hide the collection in this view layer

  """

  ...

def collection_hide_inside() -> None:

  """

  Hide all the objects and collections inside the collection

  """

  ...

def collection_hierarchy_delete() -> None:

  """

  Delete selected collection hierarchies

  """

  ...

def collection_holdout_clear() -> None:

  """

  Clear masking of collection in the active view layer

  """

  ...

def collection_holdout_set() -> None:

  """

  Mask collection in the active view layer

  """

  ...

def collection_indirect_only_clear() -> None:

  """

  Clear collection contributing only indirectly in the view layer

  """

  ...

def collection_indirect_only_set() -> None:

  """

  Set collection to only contribute indirectly (through shadows and reflections) in the view layer

  """

  ...

def collection_instance() -> None:

  """

  Instance selected collections to active scene

  """

  ...

def collection_isolate(extend: bool = False) -> None:

  """

  Hide all but this collection and its parents

  """

  ...

def collection_link() -> None:

  """

  Link selected collections to active scene

  """

  ...

def collection_new(nested: bool = True) -> None:

  """

  Add a new collection inside selected collection

  """

  ...

def collection_objects_deselect() -> None:

  """

  Deselect objects in collection

  """

  ...

def collection_objects_select() -> None:

  """

  Select objects in collection

  """

  ...

def collection_show() -> None:

  """

  Show the collection in this view layer

  """

  ...

def collection_show_inside() -> None:

  """

  Show all the objects and collections inside the collection

  """

  ...

def constraint_operation(type: str = 'ENABLE') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def data_operation(type: str = 'DEFAULT') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def datastack_drop() -> None:

  """

  Copy or reorder modifiers, constraints, and effects

  """

  ...

def delete(hierarchy: bool = False) -> None:

  """

  Delete selected objects and collections

  """

  ...

def drivers_add_selected() -> None:

  """

  Add drivers to selected items

  """

  ...

def drivers_delete_selected() -> None:

  """

  Delete drivers assigned to selected items

  """

  ...

def expanded_toggle() -> None:

  """

  Expand/Collapse all items

  """

  ...

def hide() -> None:

  """

  Hide selected objects and collections

  """

  ...

def highlight_update() -> None:

  """

  Update the item highlight based on the current mouse position

  """

  ...

def id_copy() -> None:

  """

  Selected data-blocks are copied to the clipboard

  """

  ...

def id_delete() -> None:

  """

  Delete the ID under cursor

  """

  ...

def id_operation(type: str = 'UNLINK') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def id_paste() -> None:

  """

  Data-blocks from the clipboard are pasted

  """

  ...

def id_remap(id_type: str = 'OBJECT', old_id: str = '', new_id: str = '') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def item_activate(extend: bool = False, extend_range: bool = False, deselect_all: bool = False) -> None:

  """

  Handle mouse clicks to select and activate items

  """

  ...

def item_drag_drop() -> None:

  """

  Drag and drop element to another place

  """

  ...

def item_openclose(all: bool = False) -> None:

  """

  Toggle whether item under cursor is enabled or closed

  """

  ...

def item_rename(use_active: bool = False) -> None:

  """

  Rename the active element

  """

  ...

def keyingset_add_selected() -> None:

  """

  Add selected items (blue-gray rows) to active Keying Set

  """

  ...

def keyingset_remove_selected() -> None:

  """

  Remove selected items (blue-gray rows) from active Keying Set

  """

  ...

def lib_operation(type: str = 'RENAME') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def lib_relocate() -> None:

  """

  Relocate the library under cursor

  """

  ...

def material_drop() -> None:

  """

  Drag material to object in Outliner

  """

  ...

def modifier_operation(type: str = 'TOGVIS') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def object_operation(type: str = 'SELECT') -> None:

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

  ...

def operation() -> None:

  """

  Context menu for item operations

  """

  ...

def orphans_purge(num_deleted: int = 0, do_local_ids: bool = True, do_linked_ids: bool = True, do_recursive: bool = False) -> None:

  """

  Clear all orphaned data-blocks without any users from the file

  """

  ...

def parent_clear() -> None:

  """

  Drag to clear parent in Outliner

  """

  ...

def parent_drop() -> None:

  """

  Drag to parent in Outliner

  """

  ...

def scene_drop() -> None:

  """

  Drag object to scene in Outliner

  """

  ...

def scene_operation(type: str = 'DELETE') -> None:

  """

  Context menu for scene operations

  """

  ...

def scroll_page(up: bool = False) -> None:

  """

  Scroll page up or down

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Toggle the Outliner selection of items

  """

  ...

def select_box(tweak: bool = False, xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Use box selection to select tree elements

  """

  ...

def select_walk(direction: str = 'UP', extend: bool = False, toggle_all: bool = False) -> None:

  """

  Use walk navigation to select tree elements

  """

  ...

def show_active() -> None:

  """

  Open up the tree and adjust the view so that the active object is shown centered

  """

  ...

def show_hierarchy() -> None:

  """

  Open all object entries and close all others

  """

  ...

def show_one_level(open: bool = True) -> None:

  """

  Expand/collapse all entries by one level

  """

  ...

def unhide_all() -> None:

  """

  Unhide all objects and collections

  """

  ...
