"""


GPU Types (gpu.types)
*********************

:class:`Buffer`

:class:`GPUBatch`

:class:`GPUFrameBuffer`

:class:`GPUIndexBuf`

:class:`GPUOffScreen`

:class:`GPUShader`

:class:`GPUTexture`

:class:`GPUUniformBuf`

:class:`GPUVertBuf`

:class:`GPUVertFormat`

"""

import typing

import mathutils

import bpy

class Buffer:

  """

  For Python access to GPU functions requiring a pointer.

  return the buffer as a list

  """

  def __init__(self, format: typing.Any, dimensions: int, data: typing.Sequence[typing.Any]) -> None:

    """

    :arg format:      
      Format type to interpret the buffer.
Possible values are *FLOAT*, *INT*, *UINT*, *UBYTE*, *UINT_24_8* and *10_11_11_REV*.

    :type type:       
      str

    :arg dimensions:  
      Array describing the dimensions.

    :type dimensions: 
      int

    :arg data:        
      Optional data array.

    :type data:       
      sequence

    """

    ...

  dimensions: typing.Any = ...

  """

  Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

  """

class GPUBatch:

  """

  Reusable container for drawable geometry.

  """

  def __init__(self, type: str, buf: GPUVertBuf, elem: GPUIndexBuf = None) -> None:

    """

    :arg type:        
      The primitive type of geometry to be drawn.
Possible values are *POINTS*, *LINES*, *TRIS*, *LINE_STRIP*, *LINE_LOOP*, *TRI_STRIP*, *TRI_FAN*, *LINES_ADJ*, *TRIS_ADJ* and *LINE_STRIP_ADJ*.

    :type type:       
      str

    :arg buf:         
      Vertex buffer containing all or some of the attributes required for drawing.

    :type buf:        
      :class:`gpu.types.GPUVertBuf`

    :arg elem:        
      An optional index buffer.

    :type elem:       
      :class:`gpu.types.GPUIndexBuf`

    """

    ...

  def draw(self, program: GPUShader = None) -> None:

    """

    Run the drawing program with the parameters assigned to the batch.

    """

    ...

  def program_set(self, program: GPUShader) -> None:

    """

    Assign a shader to this batch that will be used for drawing when not overwritten later.
Note: This method has to be called in the draw context that the batch will be drawn in.
This function does not need to be called when you always
set the shader when calling :meth:`gpu.types.GPUBatch.draw`.

    """

    ...

  def vertbuf_add(self, buf: GPUVertBuf) -> None:

    """

    Add another vertex buffer to the Batch.
It is not possible to add more vertices to the batch using this method.
Instead it can be used to add more attributes to the existing vertices.
A good use case would be when you have a separate
vertex buffer for vertex positions and vertex normals.
Current a batch can have at most 16 vertex buffers.

    """

    ...

class GPUFrameBuffer:

  """

  This object gives access to framebuffer functionallities.
When a 'layer' is specified in a argument, a single layer of a 3D or array texture is attached to the frame-buffer.
For cube map textures, layer is translated into a cube map face.

  """

  def __init__(self, depth_slot: GPUTexture = None, color_slots: typing.Tuple[typing.Any, ...] = None) -> None:

    """

    :arg depth_slot:  
      GPUTexture to attach or a *dict* containing keywords: 'texture', 'layer' and 'mip'.

    :type depth_slot: 
      :class:`gpu.types.GPUTexture`, dict or Nonetype

    :arg color_slots: 
      Tuple where each item can be a GPUTexture or a *dict* containing keywords: 'texture', 'layer' and 'mip'.

    :type color_slots:
      tuple or Nonetype

    """

    ...

  def bind(self) -> None:

    """

    Context manager to ensure balanced bind calls, even in the case of an error.

    """

    ...

  def clear(self, color: typing.Sequence[typing.Any] = None, depth: float = None, stencil: int = None) -> None:

    """

    Fill color, depth and stencil textures with specific value.
Common values: color=(0.0, 0.0, 0.0, 1.0), depth=1.0, stencil=0.

    """

    ...

  def read_color(self, x: typing.Any, y: typing.Any, xsize: typing.Any, ysize: typing.Any, channels: int, slot: int, format: typing.Any, data: Buffer = data) -> Buffer:

    """

    Read a block of pixels from the frame buffer.

    """

    ...

  def read_depth(self, x: typing.Any, y: typing.Any, xsize: typing.Any, ysize: typing.Any, data: Buffer = data) -> Buffer:

    """

    Read a pixel depth block from the frame buffer.

    """

    ...

  def viewport_get(self) -> None:

    """

    Returns position and dimension to current viewport.

    """

    ...

  def viewport_set(self, x: typing.Any, y: typing.Any, xsize: typing.Any, ysize: typing.Any) -> None:

    """

    Set the viewport for this framebuffer object.
Note: The viewport state is not saved upon framebuffer rebind.

    """

    ...

  is_bound: typing.Any = ...

  """

  Checks if this is the active framebuffer in the context.

  """

class GPUIndexBuf:

  """

  Contains an index buffer.

  """

  def __init__(self, type: str, seq: typing.Any) -> None:

    """

    :arg type:        
      The primitive type this index buffer is composed of.
Possible values are *POINTS*, *LINES*, *TRIS* and *LINE_STRIP_ADJ*.

    :type type:       
      str

    :param seq:       
      Indices this index buffer will contain.
Whether a 1D or 2D sequence is required depends on the type.
Optionally the sequence can support the buffer protocol.

    :type seq:        
      1D or 2D sequence

    """

    ...

class GPUOffScreen:

  """

  This object gives access to off screen buffers.

  """

  def __init__(self, width: int, height: int) -> None:

    """

    :arg width:       
      Horizontal dimension of the buffer.

    :type width:      
      int

    :arg height:      
      Vertical dimension of the buffer.

    :type height:     
      int

    """

    ...

  def bind(self) -> None:

    """

    Context manager to ensure balanced bind calls, even in the case of an error.

    """

    ...

  def draw_view3d(self, scene: bpy.types.Scene, view_layer: bpy.types.ViewLayer, view3d: bpy.types.SpaceView3D, region: bpy.types.Region, view_matrix: mathutils.Matrix, projection_matrix: mathutils.Matrix, do_color_management: bool = False) -> None:

    """

    Draw the 3d viewport in the offscreen object.

    """

    ...

  def free(self) -> None:

    """

    Free the offscreen object.
The framebuffer, texture and render objects will no longer be accessible.

    """

    ...

  def unbind(self, restore: bool = True) -> None:

    """

    Unbind the offscreen object.

    """

    ...

  color_texture: int = ...

  """

  OpenGL bindcode for the color texture.

  """

  height: int = ...

  """

  Height of the texture.

  """

  texture_color: GPUTexture = ...

  """

  The color texture attached.

  """

  width: int = ...

  """

  Width of the texture.

  """

class GPUShader:

  """

  GPUShader combines multiple GLSL shaders into a program used for drawing.
It must contain at least a vertex and fragment shaders.

  The GLSL ``#version`` directive is automatically included at the top of shaders,
and set to 330. Some preprocessor directives are automatically added according to
the Operating System or availability: ``GPU_ATI``, ``GPU_NVIDIA`` and ``GPU_INTEL``.

  The following extensions are enabled by default if supported by the GPU:
``GL_ARB_texture_gather``, ``GL_ARB_texture_cube_map_array``
and ``GL_ARB_shader_draw_parameters``.

  For drawing user interface elements and gizmos, use
``fragOutput = blender_srgb_to_framebuffer_space(fragOutput)``
to transform the output sRGB colors to the frame-buffer color-space.

  """

  def __init__(self, vertexcode: str, fragcode: typing.Any, geocode: typing.Any = None, libcode: typing.Any = None, defines: typing.Any = None, name: typing.Any = 'pyGPUShader') -> None:

    """

    :param vertexcode:
      Vertex shader code.

    :type vertexcode: 
      str

    :param fragcode:  
      Fragment shader code.

    :type value:      
      str

    :param geocode:   
      Geometry shader code.

    :type value:      
      str

    :param libcode:   
      Code with functions and presets to be shared between shaders.

    :type value:      
      str

    :param defines:   
      Preprocessor directives.

    :type value:      
      str

    :param name:      
      Name of shader code, for debugging purposes.

    :type value:      
      str

    """

    ...

  def attr_from_name(self, name: str) -> int:

    """

    Get attribute location by name.

    """

    ...

  def bind(self) -> None:

    """

    Bind the shader object. Required to be able to change uniforms of this shader.

    """

    ...

  def calc_format(self) -> GPUVertFormat:

    """

    Build a new format based on the attributes of the shader.

    """

    ...

  def uniform_block(self, name: str, ubo: typing.Any) -> None:

    """

    Specify the value of an uniform buffer object variable for the current GPUShader.

    """

    ...

  def uniform_block_from_name(self, name: str) -> int:

    """

    Get uniform block location by name.

    """

    ...

  def uniform_bool(self, name: str, seq: typing.Sequence[bool]) -> None:

    """

    Specify the value of a uniform variable for the current program object.

    """

    ...

  def uniform_float(self, name: str, value: typing.Any) -> None:

    """

    Specify the value of a uniform variable for the current program object.

    """

    ...

  def uniform_from_name(self, name: str) -> int:

    """

    Get uniform location by name.

    """

    ...

  def uniform_int(self, name: str, seq: typing.Sequence[typing.Any]) -> None:

    """

    Specify the value of a uniform variable for the current program object.

    """

    ...

  def uniform_sampler(self, name: str, texture: GPUTexture) -> None:

    """

    Specify the value of a texture uniform variable for the current GPUShader.

    """

    ...

  def uniform_vector_float(self, location: int, buffer: typing.Sequence[float], length: int, count: int) -> None:

    """

    Set the buffer to fill the uniform.

    """

    ...

  def uniform_vector_int(self, location: typing.Any, buffer: typing.Any, length: typing.Any, count: typing.Any) -> None:

    """

    See GPUShader.uniform_vector_float(...) description.

    """

    ...

  name: str = ...

  """

  The name of the shader object for debugging purposes (read-only).

  """

  program: int = ...

  """

  The name of the program object for use by the OpenGL API (read-only).

  """

class GPUTexture:

  """

  This object gives access to off GPU textures.

  """

  def __init__(self, size: typing.Union[typing.Tuple[typing.Any, ...], int], layers: int = 0, is_cubemap: int = False, format: str = 'RGBA8', data: Buffer = None) -> None:

    """

    :arg size:        
      Dimensions of the texture 1D, 2D, 3D or cubemap.

    :type size:       
      tuple or int

    :arg layers:      
      Number of layers in texture array or number of cubemaps in cubemap array

    :type layers:     
      int

    :arg is_cubemap:  
      Indicates the creation of a cubemap texture.

    :type is_cubemap: 
      int

    :arg format:      
      Internal data format inside GPU memory. Possible values are:
*RGBA8UI*,
*RGBA8I*,
*RGBA8*,
*RGBA32UI*,
*RGBA32I*,
*RGBA32F*,
*RGBA16UI*,
*RGBA16I*,
*RGBA16F*,
*RGBA16*,
*RG8UI*,
*RG8I*,
*RG8*,
*RG32UI*,
*RG32I*,
*RG32F*,
*RG16UI*,
*RG16I*,
*RG16F*,
*RG16*,
*R8UI*,
*R8I*,
*R8*,
*R32UI*,
*R32I*,
*R32F*,
*R16UI*,
*R16I*,
*R16F*,
*R16*,
*R11F_G11F_B10F*,
*DEPTH32F_STENCIL8*,
*DEPTH24_STENCIL8*,
*SRGB8_A8*,
*RGB16F*,
*SRGB8_A8_DXT1*,
*SRGB8_A8_DXT3*,
*SRGB8_A8_DXT5*,
*RGBA8_DXT1*,
*RGBA8_DXT3*,
*RGBA8_DXT5*,
*DEPTH_COMPONENT32F*,
*DEPTH_COMPONENT24*,
*DEPTH_COMPONENT16*,

    :type format:     
      str

    :arg data:        
      Buffer object to fill the texture.

    :type data:       
      :class:`gpu.types.Buffer`

    """

    ...

  def clear(self, format: typing.Any = 'FLOAT', value: typing.Sequence[typing.Any] = (0.0, 0.0, 0.0, 1.0)) -> None:

    """

    Fill texture with specific value.

    """

    ...

  def read(self) -> None:

    """

    Creates a buffer with the value of all pixels.

    """

    ...

  format: str = ...

  """

  Format of the texture.

  """

  height: int = ...

  """

  Height of the texture.

  """

  width: int = ...

  """

  Width of the texture.

  """

class GPUUniformBuf:

  """

  This object gives access to off uniform buffers.

  """

  def __init__(self, data: Buffer) -> None:

    """

    :arg data:        
      Buffer object.

    :type data:       
      :class:`gpu.types.Buffer`

    """

    ...

  def update(self, data: typing.Any) -> None:

    """

    Update the data of the uniform buffer object.

    """

    ...

class GPUVertBuf:

  """

  Contains a VBO.

  """

  def __init__(self, len: typing.Any, format: typing.Any) -> None:

    """

    :param len:       
      Amount of vertices that will fit into this buffer.

    :type type:       
      *int*

    :param format:    
      Vertex format.

    :type buf:        
      :class:`gpu.types.GPUVertFormat`

    """

    ...

  def attr_fill(self, id: typing.Union[int, str], data: typing.Sequence[float]) -> None:

    """

    Insert data into the buffer for a single attribute.

    """

    ...

class GPUVertFormat:

  """

  This object contains information about the structure of a vertex buffer.

  """

  def attr_add(self, id: str, comp_type: str, len: int, fetch_mode: str) -> None:

    """

    Add a new attribute to the format.

    """

    ...
