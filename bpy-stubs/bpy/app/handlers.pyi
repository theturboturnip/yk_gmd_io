"""


Application Handlers (bpy.app.handlers)
***************************************

This module contains callback lists


Basic Handler Example
=====================

This script shows the most simple example of adding a handler.

.. code::

  import bpy


  def my_handler(scene):
      print("Frame Change", scene.frame_current)


  bpy.app.handlers.frame_change_pre.append(my_handler)


Persistent Handler Example
==========================

By default handlers are freed when loading new files, in some cases you may
want the handler stay running across multiple files (when the handler is
part of an add-on for example).

For this the :data:`bpy.app.handlers.persistent` decorator needs to be used.

.. code::

  import bpy
  from bpy.app.handlers import persistent


  @persistent
  def load_handler(dummy):
      print("Load Handler:", bpy.data.filepath)


  bpy.app.handlers.load_post.append(load_handler)


Note on Altering Data
=====================

Altering data from handlers should be done carefully. While rendering the
``frame_change_pre`` and ``frame_change_post`` handlers are called from one
thread and the viewport updates from a different thread. If the handler changes
data that is accessed by the viewport, this can cause a crash of Blender. In
such cases, lock the interface (Render â†’ Lock Interface or
:data:`bpy.types.RenderSettings.use_lock_interface`) before starting a render.

Below is an example of a mesh that is altered from a handler:

.. code::

  def frame_change_pre(scene):
      # A triangle that shifts in the z direction
      zshift = scene.frame_current * 0.1
      vertices = [(-1, -1, zshift), (1, -1, zshift), (0, 1, zshift)]
      triangles = [(0, 1, 2)]

      object = bpy.data.objects["The Object"]
      object.data.clear_geometry()
      object.data.from_pydata(vertices, [], triangles)

:data:`depsgraph_update_post`

:data:`depsgraph_update_pre`

:data:`frame_change_post`

:data:`frame_change_pre`

:data:`load_factory_preferences_post`

:data:`load_factory_startup_post`

:data:`load_post`

:data:`load_pre`

:data:`redo_post`

:data:`redo_pre`

:data:`render_cancel`

:data:`render_complete`

:data:`render_init`

:data:`render_post`

:data:`render_pre`

:data:`render_stats`

:data:`render_write`

:data:`save_post`

:data:`save_pre`

:data:`undo_post`

:data:`undo_pre`

:data:`version_update`

:data:`xr_session_start_pre`

:data:`persistent`

"""

import typing

depsgraph_update_post: typing.Any = ...

"""

on depsgraph update (post)

"""

depsgraph_update_pre: typing.Any = ...

"""

on depsgraph update (pre)

"""

frame_change_post: typing.Any = ...

"""

Called after frame change for playback and rendering, after the data has been evaluated for the new frame.

"""

frame_change_pre: typing.Any = ...

"""

Called after frame change for playback and rendering, before any data is evaluated for the new frame. This makes it possible to change data and relations (for example swap an object to another mesh) for the new frame. Note that this handler is **not** to be used as 'before the frame changes' event. The dependency graph is not available in this handler, as data and relations may have been altered and the dependency graph has not yet been updated for that.

"""

load_factory_preferences_post: typing.Any = ...

"""

on loading factory preferences (after)

"""

load_factory_startup_post: typing.Any = ...

"""

on loading factory startup (after)

"""

load_post: typing.Any = ...

"""

on loading a new blend file (after)

"""

load_pre: typing.Any = ...

"""

on loading a new blend file (before)

"""

redo_post: typing.Any = ...

"""

on loading a redo step (after)

"""

redo_pre: typing.Any = ...

"""

on loading a redo step (before)

"""

render_cancel: typing.Any = ...

"""

on canceling a render job

"""

render_complete: typing.Any = ...

"""

on completion of render job

"""

render_init: typing.Any = ...

"""

on initialization of a render job

"""

render_post: typing.Any = ...

"""

on render (after)

"""

render_pre: typing.Any = ...

"""

on render (before)

"""

render_stats: typing.Any = ...

"""

on printing render statistics

"""

render_write: typing.Any = ...

"""

on writing a render frame (directly after the frame is written)

"""

save_post: typing.Any = ...

"""

on saving a blend file (after)

"""

save_pre: typing.Any = ...

"""

on saving a blend file (before)

"""

undo_post: typing.Any = ...

"""

on loading an undo step (after)

"""

undo_pre: typing.Any = ...

"""

on loading an undo step (before)

"""

version_update: typing.Any = ...

"""

on ending the versioning code

"""

xr_session_start_pre: typing.Any = ...

"""

on starting an xr session (before)

"""

persistent: typing.Any = ...

"""

Function decorator for callback functions not to be removed when loading new files

"""
