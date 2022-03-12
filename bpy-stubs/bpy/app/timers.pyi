"""


Application Timers (bpy.app.timers)
***********************************


Run a Function in x Seconds
===========================

.. code::

  import bpy


  def in_5_seconds():
      print("Hello World")


  bpy.app.timers.register(in_5_seconds, first_interval=5)


Run a Function every x Seconds
==============================

.. code::

  import bpy


  def every_2_seconds():
      print("Hello World")
      return 2.0


  bpy.app.timers.register(every_2_seconds)


Run a Function n times every x seconds
======================================

.. code::

  import bpy

  counter = 0


  def run_10_times():
      global counter
      counter += 1
      print(counter)
      if counter == 10:
          return None
      return 0.1


  bpy.app.timers.register(run_10_times)


Assign parameters to functions
==============================

.. code::

  import bpy
  import functools


  def print_message(message):
      print("Message:", message)


  bpy.app.timers.register(functools.partial(print_message, "Hello"), first_interval=2.0)
  bpy.app.timers.register(functools.partial(print_message, "World"), first_interval=3.0)


Use a Timer to react to events in another thread
================================================

You should never modify Blender data at arbitrary points in time in separate threads.
However you can use a queue to collect all the actions that should be executed when Blender is in the right state again.
Pythons *queue.Queue* can be used here, because it implements the required locking semantics.

.. code::

  import bpy
  import queue

  execution_queue = queue.Queue()

  # This function can savely be called in another thread.
  # The function will be executed when the timer runs the next time.
  def run_in_main_thread(function):
      execution_queue.put(function)


  def execute_queued_functions():
      while not execution_queue.empty():
          function = execution_queue.get()
          function()
      return 1.0


  bpy.app.timers.register(execute_queued_functions)

:func:`is_registered`

:func:`register`

:func:`unregister`

"""

import typing

def is_registered(function: int) -> bool:

  """

  Check if this function is registered as a timer.

  """

  ...

def register(function: typing.Any, first_interval: float = 0, persistent: bool = False) -> None:

  """

  Add a new function that will be called after the specified amount of seconds.
The function gets no arguments and is expected to return either None or a float.
If ``None`` is returned, the timer will be unregistered.
A returned number specifies the delay until the function is called again.
``functools.partial`` can be used to assign some parameters.

  """

  ...

def unregister(function: typing.Callable) -> None:

  """

  Unregister timer.

  """

  ...
