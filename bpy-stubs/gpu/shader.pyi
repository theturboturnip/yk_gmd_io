"""


GPU Shader Utilities (gpu.shader)
*********************************

This module provides access to GPUShader internal functions.

-[ Built-in shaders ]-

All built-in shaders have the ``mat4 ModelViewProjectionMatrix`` uniform.

Its value must be modified using the :class:`gpu.matrix` module.

``2D_UNIFORM_COLOR``
  :Attributes:      
    vec3 pos

  :Uniforms:        
    vec4 color

``2D_FLAT_COLOR``
  :Attributes:      
    vec3 pos, vec4 color

  :Uniforms:        
    none

``2D_SMOOTH_COLOR``
  :Attributes:      
    vec3 pos, vec4 color

  :Uniforms:        
    none

``2D_IMAGE``
  :Attributes:      
    vec3 pos, vec2 texCoord

  :Uniforms:        
    sampler2D image

``3D_UNIFORM_COLOR``
  :Attributes:      
    vec3 pos

  :Uniforms:        
    vec4 color

``3D_FLAT_COLOR``
  :Attributes:      
    vec3 pos, vec4 color

  :Uniforms:        
    none

``3D_SMOOTH_COLOR``
  :Attributes:      
    vec3 pos, vec4 color

  :Uniforms:        
    none

:func:`code_from_builtin`

:func:`from_builtin`

:func:`unbind`

"""

import typing

import bpy

def code_from_builtin(pygpu_shader_name: str) -> typing.Dict[str, typing.Any]:

  """

  Exposes the internal shader code for consultation.

  """

  ...

def from_builtin(shader_name: str, config: str = 'DEFAULT') -> bpy.types.GPUShader:

  """

  Shaders that are embedded in the blender internal code.
They all read the uniform ``mat4 ModelViewProjectionMatrix``,
which can be edited by the :mod:`gpu.matrix` module.

  You can also choose a shader configuration that uses clip_planes by setting the ``CLIPPED`` value to the config parameter. Note that in this case you also need to manually set the value of ``mat4 ModelMatrix``.

  For more details, you can check the shader code with the
:func:`gpu.shader.code_from_builtin` function.

  """

  ...

def unbind() -> None:

  """

  Unbind the bound shader object.

  """

  ...
