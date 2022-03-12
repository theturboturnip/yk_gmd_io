"""


Operators (bpy.ops)
*******************


Calling Operators
=================

Provides python access to calling operators, this includes operators written in
C, Python or macros.

Only keyword arguments can be used to pass operator properties.

Operators don't have return values as you might expect,
instead they return a set() which is made up of:
``{'RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH'}``.
Common return values are ``{'FINISHED'}`` and ``{'CANCELLED'}``.

Calling an operator in the wrong context will raise a ``RuntimeError``,
there is a poll() method to avoid this problem.

Note that the operator ID (bl_idname) in this example is ``mesh.subdivide``,
``bpy.ops`` is just the access path for python.


Keywords and Positional Arguments
---------------------------------

For calling operators keywords are used for operator properties and
positional arguments are used to define how the operator is called.

There are 3 optional positional arguments (documented in detail below).

.. code:: python

  bpy.ops.test.operator(override_context, execution_context, undo)

* override_context - ``dict`` type.

* execution_context - ``str`` (enum).

* undo - ``bool`` type.

Each of these arguments is optional, but must be given in the order above.

.. code::

  import bpy

  # calling an operator
  bpy.ops.mesh.subdivide(number_cuts=3, smoothness=0.5)


  # check poll() to avoid exception.
  if bpy.ops.object.mode_set.poll():
      bpy.ops.object.mode_set(mode='EDIT')


Overriding Context
==================

It is possible to override context members that the operator sees, so that they
act on specified rather than the selected or active data, or to execute an
operator in the different part of the user interface.

The context overrides are passed as a dictionary, with keys matching the context
member names in bpy.context.
For example to override ``bpy.context.active_object``,
you would pass ``{'active_object': object}``.

Note: You will nearly always want to use a copy of the actual current context as basis
(otherwise, you'll have to find and gather all needed data yourself).

.. code::

  # remove all objects in scene rather than the selected ones
  import bpy
  override = bpy.context.copy()
  override['selected_objects'] = list(bpy.context.scene.objects)
  bpy.ops.object.delete(override)

.. _operator-execution-context:


Execution Context
=================

When calling an operator you may want to pass the execution context.

This determines the context that is given for the operator to run in, and whether
invoke() is called or only execute().

``EXEC_DEFAULT`` is used by default, running only the ``execute()`` method, but you may
want the operator to take user interaction with ``INVOKE_DEFAULT`` which will also
call invoke() if existing.

The execution context is one of:

* ``INVOKE_DEFAULT``

* ``INVOKE_REGION_WIN``

* ``INVOKE_REGION_CHANNELS``

* ``INVOKE_REGION_PREVIEW``

* ``INVOKE_AREA``

* ``INVOKE_SCREEN``

* ``EXEC_DEFAULT``

* ``EXEC_REGION_WIN``

* ``EXEC_REGION_CHANNELS``

* ``EXEC_REGION_PREVIEW``

* ``EXEC_AREA``

* ``EXEC_SCREEN``

.. code::

  # collection add popup
  import bpy
  bpy.ops.object.collection_instance_add('INVOKE_DEFAULT')

It is also possible to run an operator in a particular part of the user
interface. For this we need to pass the window, screen, area and sometimes
a region.

.. code::

  # maximize 3d view in all windows
  import bpy

  for window in bpy.context.window_manager.windows:
      screen = window.screen

      for area in screen.areas:
          if area.type == 'VIEW_3D':
              override = {'window': window, 'screen': screen, 'area': area}
              bpy.ops.screen.screen_full_area(override)
              break

"""

from . import world

from . import workspace

from . import wm

from . import view3d

from . import view2d

from . import uv

from . import ui

from . import transform

from . import texture

from . import text

from . import surface

from . import spreadsheet

from . import sound

from . import sequencer

from . import sculpt

from . import script

from . import screen

from . import scene

from . import safe_areas

from . import rigidbody

from . import render

from . import ptcache

from . import preferences

from . import poselib

from . import pose

from . import particle

from . import palette

from . import paintcurve

from . import paint

from . import outliner

from . import object

from . import node

from . import nla

from . import mesh

from . import mball

from . import material

from . import mask

from . import marker

from . import lattice

from . import info

from . import import_scene

from . import import_mesh

from . import import_curve

from . import import_anim

from . import image

from . import graph

from . import gpencil

from . import gizmogroup

from . import geometry

from . import font

from . import fluid

from . import file

from . import export_scene

from . import export_mesh

from . import export_anim

from . import ed

from . import dpaint

from . import cycles

from . import curve

from . import constraint

from . import console

from . import collection

from . import cloth

from . import clip

from . import camera

from . import cachefile

from . import buttons

from . import brush

from . import boid

from . import asset

from . import armature

from . import anim

from . import action

import typing
