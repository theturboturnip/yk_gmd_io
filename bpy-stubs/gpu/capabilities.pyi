"""


GPU Capabilities Utilities (gpu.capabilities)
*********************************************

This module provides access to the GPU capabilities.

:func:`extensions_get`

:func:`max_batch_indices_get`

:func:`max_batch_vertices_get`

:func:`max_texture_layers_get`

:func:`max_texture_size_get`

:func:`max_textures_frag_get`

:func:`max_textures_geom_get`

:func:`max_textures_get`

:func:`max_textures_vert_get`

:func:`max_uniforms_frag_get`

:func:`max_uniforms_vert_get`

:func:`max_varying_floats_get`

:func:`max_vertex_attribs_get`

"""

import typing

def extensions_get() -> typing.Tuple[str, ...]:

  """

  Get supported extensions in the current context.

  """

  ...

def max_batch_indices_get() -> int:

  """

  Get maximum number of vertex array indices.

  """

  ...

def max_batch_vertices_get() -> int:

  """

  Get maximum number of vertex array vertices.

  """

  ...

def max_texture_layers_get() -> int:

  """

  Get maximum number of layers in texture.

  """

  ...

def max_texture_size_get() -> int:

  """

  Get estimated maximum texture size to be able to handle.

  """

  ...

def max_textures_frag_get() -> int:

  """

  Get maximum supported texture image units used for
accessing texture maps from the fragment shader.

  """

  ...

def max_textures_geom_get() -> int:

  """

  Get maximum supported texture image units used for
accessing texture maps from the geometry shader.

  """

  ...

def max_textures_get() -> int:

  """

  Get maximum supported texture image units used for
accessing texture maps from the vertex shader and the
fragment processor.

  """

  ...

def max_textures_vert_get() -> int:

  """

  Get maximum supported texture image units used for
accessing texture maps from the vertex shader.

  """

  ...

def max_uniforms_frag_get() -> int:

  """

  Get maximum number of values held in uniform variable
storage for a fragment shader.

  """

  ...

def max_uniforms_vert_get() -> int:

  """

  Get maximum number of values held in uniform variable
storage for a vertex shader.

  """

  ...

def max_varying_floats_get() -> int:

  """

  Get maximum number of varying variables used by
vertex and fragment shaders.

  """

  ...

def max_vertex_attribs_get() -> int:

  """

  Get maximum number of vertex attributes accessible to
a vertex shader.

  """

  ...
