"""


gpu_extras submodule (gpu_extras.batch)
***************************************

:func:`batch_for_shader`

"""

import typing

import gpu

def batch_for_shader(shader: gpu.types.GPUShader, type: str, content: typing.Dict[str, typing.Any], *args, indices: typing.Any = None) -> gpu.types.Batch:

  """

  Return a batch already configured and compatible with the shader.

  """

  ...
