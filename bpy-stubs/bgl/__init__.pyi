"""


OpenGL Wrapper (bgl)
********************

This module wraps OpenGL constants and functions, making them available from
within Blender Python.

The complete list can be retrieved from the module itself, by listing its
contents: dir(bgl).  A simple search on the web can point to more
than enough material to teach OpenGL programming, from books to many
collections of tutorials.

Here is a comprehensive `list of books <https://www.khronos.org/developers/books/>`_ (non free).
`Learn OpenGL <https://learnopengl.com/>`_ is one of the best resources to learn modern OpenGL and
`opengl-tutorial.org <http://www.opengl-tutorial.org/>`_ offers a set of extensive examples,
including advanced features.

Note: You can use the :class:`bpy.types.Image` type to load and set textures.
See :class:`bpy.types.Image.gl_load` and :class:`bpy.types.Image.gl_free`,
for example.

:func:`glBindTexture`

:func:`glBlendFunc`

:func:`glClear`

:func:`glClearColor`

:func:`glClearDepth`

:func:`glClearStencil`

:func:`glClipPlane`

:func:`glColorMask`

:func:`glCopyTexImage2D`

:func:`glCullFace`

:func:`glDeleteTextures`

:func:`glDepthFunc`

:func:`glDepthMask`

:func:`glDepthRange`

:func:`glDisable`

:func:`glDrawBuffer`

:func:`glEdgeFlag`

:func:`glEdgeFlag`

:func:`glEdgeFlagv`

:func:`glEnable`

:func:`glEvalCoord`

:func:`glEvalCoord1d`

:func:`glEvalCoord1f`

:func:`glEvalCoord2d`

:func:`glEvalCoord2f`

:func:`glEvalCoord1dv`

:func:`glEvalCoord1fv`

:func:`glEvalCoord2dv`

:func:`glEvalCoord2fv`

:func:`glEvalMesh`

:func:`glEvalMesh1`

:func:`glEvalMesh2`

:func:`glEvalPoint`

:func:`glEvalPoint1`

:func:`glEvalPoint2`

:func:`glFeedbackBuffer`

:func:`glFinish`

:func:`glFlush`

:func:`glFog`

:func:`glFogf`

:func:`glFogi`

:func:`glFogfv`

:func:`glFogiv`

:func:`glFrontFace`

:func:`glGenTextures`

:func:`glGet`

:func:`glGetBooleanv`

:func:`glGetfloatv`

:func:`glGetFloatv`

:func:`glGetIntegerv`

:func:`glGetError`

:func:`glGetLight`

:func:`glGetLightfv`

:func:`glGetLightiv`

:func:`glGetMap`

:func:`glGetMapdv`

:func:`glGetMapfv`

:func:`glGetMapiv`

:func:`glGetMaterial`

:func:`glGetMaterialfv`

:func:`glGetMaterialiv`

:func:`glGetPixelMap`

:func:`glGetPixelMapfv`

:func:`glGetPixelMapuiv`

:func:`glGetPixelMapusv`

:func:`glGetString`

:func:`glGetTexEnv`

:func:`glGetTexEnvfv`

:func:`glGetTexEnviv`

:func:`glGetTexGen`

:func:`glGetTexGendv`

:func:`glGetTexGenfv`

:func:`glGetTexGeniv`

:func:`glGetTexImage`

:func:`glGetTexLevelParameter`

:func:`glGetTexLevelParameterfv`

:func:`glGetTexLevelParameteriv`

:func:`glGetTexParameter`

:func:`glGetTexParameterfv`

:func:`glGetTexParameteriv`

:func:`glHint`

:func:`glIsEnabled`

:func:`glIsTexture`

:func:`glLight`

:func:`glLightf`

:func:`glLighti`

:func:`glLightfv`

:func:`glLightiv`

:func:`glLightModel`

:func:`glLightModelf`

:func:`glLightModeli`

:func:`glLightModelfv`

:func:`glLightModeliv`

:func:`glLineWidth`

:func:`glLoadMatrix`

:func:`glLoadMatrixd`

:func:`glLoadMatixf`

:func:`glLogicOp`

:func:`glMap1`

:func:`glMap1d`

:func:`glMap1f`

:func:`glMap2`

:func:`glMap2d`

:func:`glMap2f`

:func:`glMapGrid`

:func:`glMapGrid1d`

:func:`glMapGrid1f`

:func:`glMapGrid2d`

:func:`glMapGrid2f`

:func:`glMaterial`

:func:`glMultMatrix`

:func:`glMultMatrixd`

:func:`glMultMatrixf`

:func:`glNormal3`

:func:`Normal3b`

:func:`Normal3bv`

:func:`Normal3d`

:func:`Normal3dv`

:func:`Normal3f`

:func:`Normal3fv`

:func:`Normal3i`

:func:`Normal3iv`

:func:`Normal3s`

:func:`Normal3sv`

:func:`glPixelMap`

:func:`glPixelMapfv`

:func:`glPixelMapuiv`

:func:`glPixelMapusv`

:func:`glPixelStore`

:func:`glPixelStoref`

:func:`glPixelStorei`

:func:`glPixelTransfer`

:func:`glPixelTransferf`

:func:`glPixelTransferi`

:func:`glPointSize`

:func:`glPolygonMode`

:func:`glPolygonOffset`

:func:`glRasterPos`

:func:`glRasterPos2d`

:func:`glRasterPos2f`

:func:`glRasterPos2i`

:func:`glRasterPos2s`

:func:`glRasterPos3d`

:func:`glRasterPos3f`

:func:`glRasterPos3i`

:func:`glRasterPos3s`

:func:`glRasterPos4d`

:func:`glRasterPos4f`

:func:`glRasterPos4i`

:func:`glRasterPos4s`

:func:`glRasterPos2dv`

:func:`glRasterPos2fv`

:func:`glRasterPos2iv`

:func:`glRasterPos2sv`

:func:`glRasterPos3dv`

:func:`glRasterPos3fv`

:func:`glRasterPos3iv`

:func:`glRasterPos3sv`

:func:`glRasterPos4dv`

:func:`glRasterPos4fv`

:func:`glRasterPos4iv`

:func:`glRasterPos4sv`

:func:`glReadBuffer`

:func:`glReadPixels`

:func:`glRect`

:func:`glRectd`

:func:`glRectf`

:func:`glRecti`

:func:`glRects`

:func:`glRectdv`

:func:`glRectfv`

:func:`glRectiv`

:func:`glRectsv`

:func:`glRotate`

:func:`glRotated`

:func:`glRotatef`

:func:`glScale`

:func:`glScaled`

:func:`glScalef`

:func:`glScissor`

:func:`glStencilFunc`

:func:`glStencilMask`

:func:`glStencilOp`

:func:`glTexCoord`

:func:`glTexCoord1d`

:func:`glTexCoord1f`

:func:`glTexCoord1i`

:func:`glTexCoord1s`

:func:`glTexCoord2d`

:func:`glTexCoord2f`

:func:`glTexCoord2i`

:func:`glTexCoord2s`

:func:`glTexCoord3d`

:func:`glTexCoord3f`

:func:`glTexCoord3i`

:func:`glTexCoord3s`

:func:`glTexCoord4d`

:func:`glTexCoord4f`

:func:`glTexCoord4i`

:func:`glTexCoord4s`

:func:`glTexCoord1dv`

:func:`glTexCoord1fv`

:func:`glTexCoord1iv`

:func:`glTexCoord1sv`

:func:`glTexCoord2dv`

:func:`glTexCoord2fv`

:func:`glTexCoord2iv`

:func:`glTexCoord2sv`

:func:`glTexCoord3dv`

:func:`glTexCoord3fv`

:func:`glTexCoord3iv`

:func:`glTexCoord3sv`

:func:`glTexCoord4dv`

:func:`glTexCoord4fv`

:func:`glTexCoord4iv`

:func:`glTexCoord4sv`

:func:`glTexEnv`

:func:`glTextEnvf`

:func:`glTextEnvi`

:func:`glTextEnvfv`

:func:`glTextEnviv`

:func:`glTexGen`

:func:`glTexGend`

:func:`glTexGenf`

:func:`glTexGeni`

:func:`glTexGendv`

:func:`glTexGenfv`

:func:`glTexGeniv`

:func:`glTexImage1D`

:func:`glTexImage2D`

:func:`glTexParameter`

:func:`glTexParameterf`

:func:`glTexParameteri`

:func:`glTexParameterfv`

:func:`glTexParameteriv`

:func:`glTranslate`

:func:`glTranslatef`

:func:`glTranslated`

:func:`glViewport`

:func:`glUseProgram`

:func:`glValidateProgram`

:func:`glLinkProgram`

:func:`glActiveTexture`

:func:`glAttachShader`

:func:`glCompileShader`

:func:`glCreateProgram`

:func:`glCreateShader`

:func:`glDeleteProgram`

:func:`glDeleteShader`

:func:`glDetachShader`

:func:`glGetAttachedShaders`

:func:`glGetProgramInfoLog`

:func:`glGetShaderInfoLog`

:func:`glGetProgramiv`

:func:`glIsShader`

:func:`glIsProgram`

:func:`glGetShaderSource`

:func:`glShaderSource`

:class:`Buffer`

"""

import typing

def glBindTexture(target: typing.Any, texture: int) -> None:

  """

  Bind a named texture to a texturing target

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glBindTexture.xhtml>`_

  """

  ...

def glBlendFunc(sfactor: typing.Any, dfactor: typing.Any) -> None:

  """

  Specify pixel arithmetic

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glBlendFunc.xhtml>`_

  """

  ...

def glClear(mask: typing.Any) -> None:

  """

  Clear buffers to preset values

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glClear.xhtml>`_

  """

  ...

def glClearColor(red: typing.Any, green: typing.Any, blue: typing.Any, alpha: typing.Any) -> None:

  """

  Specify clear values for the color buffers

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glClearColor.xhtml>`_

  """

  ...

def glClearDepth(depth: int) -> None:

  """

  Specify the clear value for the depth buffer

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glClearDepth.xhtml>`_

  """

  ...

def glClearStencil(s: int) -> None:

  """

  Specify the clear value for the stencil buffer

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glClearStencil.xhtml>`_

  """

  ...

def glClipPlane(plane: typing.Any, equation: Buffer) -> None:

  """

  Specify a plane against which all geometry is clipped

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glClipPlane.xhtml>`_

  """

  ...

def glColorMask(red: typing.Any, green: typing.Any, blue: typing.Any, alpha: typing.Any) -> None:

  """

  Enable and disable writing of frame buffer color components

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glColorMask.xhtml>`_

  """

  ...

def glCopyTexImage2D(target: typing.Any, level: int, internalformat: int, x: typing.Any, y: typing.Any, width: int, height: int, border: int) -> None:

  """

  Copy pixels into a 2D texture image

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glCopyTexImage2D.xhtml>`_

  """

  ...

def glCullFace(mode: typing.Any) -> None:

  """

  Specify whether front- or back-facing facets can be culled

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glCullFace.xhtml>`_

  """

  ...

def glDeleteTextures(n: int, textures: Buffer) -> None:

  """

  Delete named textures

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glDeleteTextures.xhtml>`_

  """

  ...

def glDepthFunc(func: typing.Any) -> None:

  """

  Specify the value used for depth buffer comparisons

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glDepthFunc.xhtml>`_

  """

  ...

def glDepthMask(flag: int) -> None:

  """

  Enable or disable writing into the depth buffer

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glDepthMask.xhtml>`_

  """

  ...

def glDepthRange(zNear: int, zFar: int) -> None:

  """

  Specify mapping of depth values from normalized device coordinates to window coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glDepthRange.xhtml>`_

  """

  ...

def glDisable(cap: typing.Any) -> None:

  """

  Disable server-side GL capabilities

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEnable.xhtml>`_

  """

  ...

def glDrawBuffer(mode: typing.Any) -> None:

  """

  Specify which color buffers are to be drawn into

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glDrawBuffer.xhtml>`_

  """

  ...

def glEdgeFlag(flag: typing.Any) -> None:

  """

  B{glEdgeFlag, glEdgeFlagv}

  Flag edges as either boundary or non-boundary

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEdgeFlag.xhtml>`_

  """

  ...

def glEdgeFlag(flag: typing.Any) -> None:

  """

  B{glEdgeFlag, glEdgeFlagv}

  Flag edges as either boundary or non-boundary

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEdgeFlag.xhtml>`_

  """

  ...

def glEdgeFlagv(flag: typing.Any) -> None:

  """

  B{glEdgeFlag, glEdgeFlagv}

  Flag edges as either boundary or non-boundary

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEdgeFlag.xhtml>`_

  """

  ...

def glEnable(cap: typing.Any) -> None:

  """

  Enable server-side GL capabilities

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEnable.xhtml>`_

  """

  ...

def glEvalCoord(u: typing.Any, v: typing.Any) -> None:

  """

  B{glEvalCoord1d, glEvalCoord1f, glEvalCoord2d, glEvalCoord2f, glEvalCoord1dv, glEvalCoord1fv,
glEvalCoord2dv, glEvalCoord2fv}

  Evaluate enabled one- and two-dimensional maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalCoord.xhtml>`_

  """

  ...

def glEvalCoord1d(u: typing.Any, v: typing.Any) -> None:

  """

  B{glEvalCoord1d, glEvalCoord1f, glEvalCoord2d, glEvalCoord2f, glEvalCoord1dv, glEvalCoord1fv,
glEvalCoord2dv, glEvalCoord2fv}

  Evaluate enabled one- and two-dimensional maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalCoord.xhtml>`_

  """

  ...

def glEvalCoord1f(u: typing.Any, v: typing.Any) -> None:

  """

  B{glEvalCoord1d, glEvalCoord1f, glEvalCoord2d, glEvalCoord2f, glEvalCoord1dv, glEvalCoord1fv,
glEvalCoord2dv, glEvalCoord2fv}

  Evaluate enabled one- and two-dimensional maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalCoord.xhtml>`_

  """

  ...

def glEvalCoord2d(u: typing.Any, v: typing.Any) -> None:

  """

  B{glEvalCoord1d, glEvalCoord1f, glEvalCoord2d, glEvalCoord2f, glEvalCoord1dv, glEvalCoord1fv,
glEvalCoord2dv, glEvalCoord2fv}

  Evaluate enabled one- and two-dimensional maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalCoord.xhtml>`_

  """

  ...

def glEvalCoord2f(u: typing.Any, v: typing.Any) -> None:

  """

  B{glEvalCoord1d, glEvalCoord1f, glEvalCoord2d, glEvalCoord2f, glEvalCoord1dv, glEvalCoord1fv,
glEvalCoord2dv, glEvalCoord2fv}

  Evaluate enabled one- and two-dimensional maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalCoord.xhtml>`_

  """

  ...

def glEvalCoord1dv(u: typing.Any, v: typing.Any) -> None:

  """

  B{glEvalCoord1d, glEvalCoord1f, glEvalCoord2d, glEvalCoord2f, glEvalCoord1dv, glEvalCoord1fv,
glEvalCoord2dv, glEvalCoord2fv}

  Evaluate enabled one- and two-dimensional maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalCoord.xhtml>`_

  """

  ...

def glEvalCoord1fv(u: typing.Any, v: typing.Any) -> None:

  """

  B{glEvalCoord1d, glEvalCoord1f, glEvalCoord2d, glEvalCoord2f, glEvalCoord1dv, glEvalCoord1fv,
glEvalCoord2dv, glEvalCoord2fv}

  Evaluate enabled one- and two-dimensional maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalCoord.xhtml>`_

  """

  ...

def glEvalCoord2dv(u: typing.Any, v: typing.Any) -> None:

  """

  B{glEvalCoord1d, glEvalCoord1f, glEvalCoord2d, glEvalCoord2f, glEvalCoord1dv, glEvalCoord1fv,
glEvalCoord2dv, glEvalCoord2fv}

  Evaluate enabled one- and two-dimensional maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalCoord.xhtml>`_

  """

  ...

def glEvalCoord2fv(u: typing.Any, v: typing.Any) -> None:

  """

  B{glEvalCoord1d, glEvalCoord1f, glEvalCoord2d, glEvalCoord2f, glEvalCoord1dv, glEvalCoord1fv,
glEvalCoord2dv, glEvalCoord2fv}

  Evaluate enabled one- and two-dimensional maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalCoord.xhtml>`_

  """

  ...

def glEvalMesh(mode: typing.Any, i1: typing.Any, i2: typing.Any) -> None:

  """

  B{glEvalMesh1 or glEvalMesh2}

  Compute a one- or two-dimensional grid of points or lines

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalMesh.xhtml>`_

  """

  ...

def glEvalMesh1(mode: typing.Any, i1: typing.Any, i2: typing.Any) -> None:

  """

  B{glEvalMesh1 or glEvalMesh2}

  Compute a one- or two-dimensional grid of points or lines

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalMesh.xhtml>`_

  """

  ...

def glEvalMesh2(mode: typing.Any, i1: typing.Any, i2: typing.Any) -> None:

  """

  B{glEvalMesh1 or glEvalMesh2}

  Compute a one- or two-dimensional grid of points or lines

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalMesh.xhtml>`_

  """

  ...

def glEvalPoint(i: int, j: int) -> None:

  """

  B{glEvalPoint1 and glEvalPoint2}

  Generate and evaluate a single point in a mesh

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalPoint.xhtml>`_

  """

  ...

def glEvalPoint1(i: int, j: int) -> None:

  """

  B{glEvalPoint1 and glEvalPoint2}

  Generate and evaluate a single point in a mesh

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalPoint.xhtml>`_

  """

  ...

def glEvalPoint2(i: int, j: int) -> None:

  """

  B{glEvalPoint1 and glEvalPoint2}

  Generate and evaluate a single point in a mesh

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glEvalPoint.xhtml>`_

  """

  ...

def glFeedbackBuffer(size: int, type: typing.Any, buffer: Buffer) -> None:

  """

  Controls feedback mode

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glFeedbackBuffer.xhtml>`_

  """

  ...

def glFinish() -> None:

  """

  Block until all GL execution is complete

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glFinish.xhtml>`_

  """

  ...

def glFlush() -> None:

  """

  Force Execution of GL commands in finite time

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glFlush.xhtml>`_

  """

  ...

def glFog(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glFogf, glFogi, glFogfv, glFogiv}

  Specify fog parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glFog.xhtml>`_

  """

  ...

def glFogf(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glFogf, glFogi, glFogfv, glFogiv}

  Specify fog parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glFog.xhtml>`_

  """

  ...

def glFogi(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glFogf, glFogi, glFogfv, glFogiv}

  Specify fog parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glFog.xhtml>`_

  """

  ...

def glFogfv(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glFogf, glFogi, glFogfv, glFogiv}

  Specify fog parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glFog.xhtml>`_

  """

  ...

def glFogiv(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glFogf, glFogi, glFogfv, glFogiv}

  Specify fog parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glFog.xhtml>`_

  """

  ...

def glFrontFace(mode: typing.Any) -> None:

  """

  Define front- and back-facing polygons

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glFrontFace.xhtml>`_

  """

  ...

def glGenTextures(n: int, textures: Buffer) -> None:

  """

  Generate texture names

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGenTextures.xhtml>`_

  """

  ...

def glGet(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glGetBooleanv, glGetfloatv, glGetFloatv, glGetIntegerv}

  Return the value or values of a selected parameter

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGet.xhtml>`_

  """

  ...

def glGetBooleanv(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glGetBooleanv, glGetfloatv, glGetFloatv, glGetIntegerv}

  Return the value or values of a selected parameter

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGet.xhtml>`_

  """

  ...

def glGetfloatv(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glGetBooleanv, glGetfloatv, glGetFloatv, glGetIntegerv}

  Return the value or values of a selected parameter

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGet.xhtml>`_

  """

  ...

def glGetFloatv(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glGetBooleanv, glGetfloatv, glGetFloatv, glGetIntegerv}

  Return the value or values of a selected parameter

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGet.xhtml>`_

  """

  ...

def glGetIntegerv(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glGetBooleanv, glGetfloatv, glGetFloatv, glGetIntegerv}

  Return the value or values of a selected parameter

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGet.xhtml>`_

  """

  ...

def glGetError() -> None:

  """

  Return error information

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetError.xhtml>`_

  """

  ...

def glGetLight(light: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetLightfv and glGetLightiv}

  Return light source parameter values

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetLight.xhtml>`_

  """

  ...

def glGetLightfv(light: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetLightfv and glGetLightiv}

  Return light source parameter values

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetLight.xhtml>`_

  """

  ...

def glGetLightiv(light: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetLightfv and glGetLightiv}

  Return light source parameter values

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetLight.xhtml>`_

  """

  ...

def glGetMap(target: typing.Any, query: typing.Any, v: Buffer) -> None:

  """

  B{glGetMapdv, glGetMapfv, glGetMapiv}

  Return evaluator parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetMap.xhtml>`_

  """

  ...

def glGetMapdv(target: typing.Any, query: typing.Any, v: Buffer) -> None:

  """

  B{glGetMapdv, glGetMapfv, glGetMapiv}

  Return evaluator parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetMap.xhtml>`_

  """

  ...

def glGetMapfv(target: typing.Any, query: typing.Any, v: Buffer) -> None:

  """

  B{glGetMapdv, glGetMapfv, glGetMapiv}

  Return evaluator parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetMap.xhtml>`_

  """

  ...

def glGetMapiv(target: typing.Any, query: typing.Any, v: Buffer) -> None:

  """

  B{glGetMapdv, glGetMapfv, glGetMapiv}

  Return evaluator parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetMap.xhtml>`_

  """

  ...

def glGetMaterial(face: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetMaterialfv, glGetMaterialiv}

  Return material parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetMaterial.xhtml>`_

  """

  ...

def glGetMaterialfv(face: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetMaterialfv, glGetMaterialiv}

  Return material parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetMaterial.xhtml>`_

  """

  ...

def glGetMaterialiv(face: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetMaterialfv, glGetMaterialiv}

  Return material parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetMaterial.xhtml>`_

  """

  ...

def glGetPixelMap(map: typing.Any, values: Buffer) -> None:

  """

  B{glGetPixelMapfv, glGetPixelMapuiv, glGetPixelMapusv}

  Return the specified pixel map

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetPixelMap.xhtml>`_

  """

  ...

def glGetPixelMapfv(map: typing.Any, values: Buffer) -> None:

  """

  B{glGetPixelMapfv, glGetPixelMapuiv, glGetPixelMapusv}

  Return the specified pixel map

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetPixelMap.xhtml>`_

  """

  ...

def glGetPixelMapuiv(map: typing.Any, values: Buffer) -> None:

  """

  B{glGetPixelMapfv, glGetPixelMapuiv, glGetPixelMapusv}

  Return the specified pixel map

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetPixelMap.xhtml>`_

  """

  ...

def glGetPixelMapusv(map: typing.Any, values: Buffer) -> None:

  """

  B{glGetPixelMapfv, glGetPixelMapuiv, glGetPixelMapusv}

  Return the specified pixel map

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetPixelMap.xhtml>`_

  """

  ...

def glGetString(name: typing.Any) -> None:

  """

  Return a string describing the current GL connection

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetString.xhtml>`_

  """

  ...

def glGetTexEnv(target: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexEnvfv, glGetTexEnviv}

  Return texture environment parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexEnv.xhtml>`_

  """

  ...

def glGetTexEnvfv(target: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexEnvfv, glGetTexEnviv}

  Return texture environment parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexEnv.xhtml>`_

  """

  ...

def glGetTexEnviv(target: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexEnvfv, glGetTexEnviv}

  Return texture environment parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexEnv.xhtml>`_

  """

  ...

def glGetTexGen(coord: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexGendv, glGetTexGenfv, glGetTexGeniv}

  Return texture coordinate generation parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexGen.xhtml>`_

  """

  ...

def glGetTexGendv(coord: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexGendv, glGetTexGenfv, glGetTexGeniv}

  Return texture coordinate generation parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexGen.xhtml>`_

  """

  ...

def glGetTexGenfv(coord: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexGendv, glGetTexGenfv, glGetTexGeniv}

  Return texture coordinate generation parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexGen.xhtml>`_

  """

  ...

def glGetTexGeniv(coord: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexGendv, glGetTexGenfv, glGetTexGeniv}

  Return texture coordinate generation parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexGen.xhtml>`_

  """

  ...

def glGetTexImage(target: typing.Any, level: int, format: typing.Any, type: typing.Any, pixels: Buffer) -> None:

  """

  Return a texture image

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexImage.xhtml>`_

  """

  ...

def glGetTexLevelParameter(target: typing.Any, level: int, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexLevelParameterfv, glGetTexLevelParameteriv}

  return texture parameter values for a specific level of detail

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexLevelParameter.xhtml>`_

  """

  ...

def glGetTexLevelParameterfv(target: typing.Any, level: int, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexLevelParameterfv, glGetTexLevelParameteriv}

  return texture parameter values for a specific level of detail

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexLevelParameter.xhtml>`_

  """

  ...

def glGetTexLevelParameteriv(target: typing.Any, level: int, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexLevelParameterfv, glGetTexLevelParameteriv}

  return texture parameter values for a specific level of detail

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexLevelParameter.xhtml>`_

  """

  ...

def glGetTexParameter(target: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexParameterfv, glGetTexParameteriv}

  Return texture parameter values

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexParameter.xhtml>`_

  """

  ...

def glGetTexParameterfv(target: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexParameterfv, glGetTexParameteriv}

  Return texture parameter values

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexParameter.xhtml>`_

  """

  ...

def glGetTexParameteriv(target: typing.Any, pname: typing.Any, params: Buffer) -> None:

  """

  B{glGetTexParameterfv, glGetTexParameteriv}

  Return texture parameter values

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetTexParameter.xhtml>`_

  """

  ...

def glHint(target: typing.Any, mode: typing.Any) -> None:

  """

  Specify implementation-specific hints

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glHint.xhtml>`_

  """

  ...

def glIsEnabled(cap: typing.Any) -> None:

  """

  Test whether a capability is enabled

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glIsEnabled.xhtml>`_

  """

  ...

def glIsTexture(texture: int) -> None:

  """

  Determine if a name corresponds to a texture

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glIsTexture.xhtml>`_

  """

  ...

def glLight(light: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glLightf,glLighti, glLightfv, glLightiv}

  Set the light source parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLight.xhtml>`_

  """

  ...

def glLightf(light: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glLightf,glLighti, glLightfv, glLightiv}

  Set the light source parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLight.xhtml>`_

  """

  ...

def glLighti(light: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glLightf,glLighti, glLightfv, glLightiv}

  Set the light source parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLight.xhtml>`_

  """

  ...

def glLightfv(light: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glLightf,glLighti, glLightfv, glLightiv}

  Set the light source parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLight.xhtml>`_

  """

  ...

def glLightiv(light: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glLightf,glLighti, glLightfv, glLightiv}

  Set the light source parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLight.xhtml>`_

  """

  ...

def glLightModel(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glLightModelf, glLightModeli, glLightModelfv, glLightModeliv}

  Set the lighting model parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLightModel.xhtml>`_

  """

  ...

def glLightModelf(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glLightModelf, glLightModeli, glLightModelfv, glLightModeliv}

  Set the lighting model parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLightModel.xhtml>`_

  """

  ...

def glLightModeli(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glLightModelf, glLightModeli, glLightModelfv, glLightModeliv}

  Set the lighting model parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLightModel.xhtml>`_

  """

  ...

def glLightModelfv(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glLightModelf, glLightModeli, glLightModelfv, glLightModeliv}

  Set the lighting model parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLightModel.xhtml>`_

  """

  ...

def glLightModeliv(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glLightModelf, glLightModeli, glLightModelfv, glLightModeliv}

  Set the lighting model parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLightModel.xhtml>`_

  """

  ...

def glLineWidth(width: float) -> None:

  """

  Specify the width of rasterized lines.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLineWidth.xhtml>`_

  """

  ...

def glLoadMatrix(m: Buffer) -> None:

  """

  B{glLoadMatrixd, glLoadMatixf}

  Replace the current matrix with the specified matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLoadMatrix.xhtml>`_

  """

  ...

def glLoadMatrixd(m: Buffer) -> None:

  """

  B{glLoadMatrixd, glLoadMatixf}

  Replace the current matrix with the specified matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLoadMatrix.xhtml>`_

  """

  ...

def glLoadMatixf(m: Buffer) -> None:

  """

  B{glLoadMatrixd, glLoadMatixf}

  Replace the current matrix with the specified matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLoadMatrix.xhtml>`_

  """

  ...

def glLogicOp(opcode: typing.Any) -> None:

  """

  Specify a logical pixel operation for color index rendering

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLogicOp.xhtml>`_

  """

  ...

def glMap1(target: typing.Any, u1: typing.Any, u2: typing.Any, stride: int, order: int, points: Buffer) -> None:

  """

  B{glMap1d, glMap1f}

  Define a one-dimensional evaluator

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMap1.xhtml>`_

  """

  ...

def glMap1d(target: typing.Any, u1: typing.Any, u2: typing.Any, stride: int, order: int, points: Buffer) -> None:

  """

  B{glMap1d, glMap1f}

  Define a one-dimensional evaluator

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMap1.xhtml>`_

  """

  ...

def glMap1f(target: typing.Any, u1: typing.Any, u2: typing.Any, stride: int, order: int, points: Buffer) -> None:

  """

  B{glMap1d, glMap1f}

  Define a one-dimensional evaluator

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMap1.xhtml>`_

  """

  ...

def glMap2(target: typing.Any, u1: typing.Any, u2: typing.Any, ustride: int, uorder: int, v1: typing.Any, v2: typing.Any, vstride: int, vorder: int, points: Buffer) -> None:

  """

  B{glMap2d, glMap2f}

  Define a two-dimensional evaluator

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMap2.xhtml>`_

  """

  ...

def glMap2d(target: typing.Any, u1: typing.Any, u2: typing.Any, ustride: int, uorder: int, v1: typing.Any, v2: typing.Any, vstride: int, vorder: int, points: Buffer) -> None:

  """

  B{glMap2d, glMap2f}

  Define a two-dimensional evaluator

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMap2.xhtml>`_

  """

  ...

def glMap2f(target: typing.Any, u1: typing.Any, u2: typing.Any, ustride: int, uorder: int, v1: typing.Any, v2: typing.Any, vstride: int, vorder: int, points: Buffer) -> None:

  """

  B{glMap2d, glMap2f}

  Define a two-dimensional evaluator

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMap2.xhtml>`_

  """

  ...

def glMapGrid(un: int, u1: typing.Any, u2: typing.Any, vn: int, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glMapGrid1d, glMapGrid1f, glMapGrid2d, glMapGrid2f}

  Define a one- or two-dimensional mesh

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMapGrid.xhtml>`_

  """

  ...

def glMapGrid1d(un: int, u1: typing.Any, u2: typing.Any, vn: int, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glMapGrid1d, glMapGrid1f, glMapGrid2d, glMapGrid2f}

  Define a one- or two-dimensional mesh

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMapGrid.xhtml>`_

  """

  ...

def glMapGrid1f(un: int, u1: typing.Any, u2: typing.Any, vn: int, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glMapGrid1d, glMapGrid1f, glMapGrid2d, glMapGrid2f}

  Define a one- or two-dimensional mesh

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMapGrid.xhtml>`_

  """

  ...

def glMapGrid2d(un: int, u1: typing.Any, u2: typing.Any, vn: int, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glMapGrid1d, glMapGrid1f, glMapGrid2d, glMapGrid2f}

  Define a one- or two-dimensional mesh

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMapGrid.xhtml>`_

  """

  ...

def glMapGrid2f(un: int, u1: typing.Any, u2: typing.Any, vn: int, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glMapGrid1d, glMapGrid1f, glMapGrid2d, glMapGrid2f}

  Define a one- or two-dimensional mesh

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMapGrid.xhtml>`_

  """

  ...

def glMaterial(face: typing.Any, pname: typing.Any, params: int) -> None:

  """

  Specify material parameters for the lighting model.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMaterial.xhtml>`_

  """

  ...

def glMultMatrix(m: Buffer) -> None:

  """

  B{glMultMatrixd, glMultMatrixf}

  Multiply the current matrix with the specified matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMultMatrix.xhtml>`_

  """

  ...

def glMultMatrixd(m: Buffer) -> None:

  """

  B{glMultMatrixd, glMultMatrixf}

  Multiply the current matrix with the specified matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMultMatrix.xhtml>`_

  """

  ...

def glMultMatrixf(m: Buffer) -> None:

  """

  B{glMultMatrixd, glMultMatrixf}

  Multiply the current matrix with the specified matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glMultMatrix.xhtml>`_

  """

  ...

def glNormal3(nx: typing.Any, ny: typing.Any, nz: typing.Any, v: Buffer) -> None:

  """

  B{Normal3b, Normal3bv, Normal3d, Normal3dv, Normal3f, Normal3fv, Normal3i, Normal3iv,
Normal3s, Normal3sv}

  Set the current normal vector

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glNormal.xhtml>`_

  """

  ...

def Normal3b(nx: typing.Any, ny: typing.Any, nz: typing.Any, v: Buffer) -> None:

  """

  B{Normal3b, Normal3bv, Normal3d, Normal3dv, Normal3f, Normal3fv, Normal3i, Normal3iv,
Normal3s, Normal3sv}

  Set the current normal vector

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glNormal.xhtml>`_

  """

  ...

def Normal3bv(nx: typing.Any, ny: typing.Any, nz: typing.Any, v: Buffer) -> None:

  """

  B{Normal3b, Normal3bv, Normal3d, Normal3dv, Normal3f, Normal3fv, Normal3i, Normal3iv,
Normal3s, Normal3sv}

  Set the current normal vector

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glNormal.xhtml>`_

  """

  ...

def Normal3d(nx: typing.Any, ny: typing.Any, nz: typing.Any, v: Buffer) -> None:

  """

  B{Normal3b, Normal3bv, Normal3d, Normal3dv, Normal3f, Normal3fv, Normal3i, Normal3iv,
Normal3s, Normal3sv}

  Set the current normal vector

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glNormal.xhtml>`_

  """

  ...

def Normal3dv(nx: typing.Any, ny: typing.Any, nz: typing.Any, v: Buffer) -> None:

  """

  B{Normal3b, Normal3bv, Normal3d, Normal3dv, Normal3f, Normal3fv, Normal3i, Normal3iv,
Normal3s, Normal3sv}

  Set the current normal vector

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glNormal.xhtml>`_

  """

  ...

def Normal3f(nx: typing.Any, ny: typing.Any, nz: typing.Any, v: Buffer) -> None:

  """

  B{Normal3b, Normal3bv, Normal3d, Normal3dv, Normal3f, Normal3fv, Normal3i, Normal3iv,
Normal3s, Normal3sv}

  Set the current normal vector

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glNormal.xhtml>`_

  """

  ...

def Normal3fv(nx: typing.Any, ny: typing.Any, nz: typing.Any, v: Buffer) -> None:

  """

  B{Normal3b, Normal3bv, Normal3d, Normal3dv, Normal3f, Normal3fv, Normal3i, Normal3iv,
Normal3s, Normal3sv}

  Set the current normal vector

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glNormal.xhtml>`_

  """

  ...

def Normal3i(nx: typing.Any, ny: typing.Any, nz: typing.Any, v: Buffer) -> None:

  """

  B{Normal3b, Normal3bv, Normal3d, Normal3dv, Normal3f, Normal3fv, Normal3i, Normal3iv,
Normal3s, Normal3sv}

  Set the current normal vector

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glNormal.xhtml>`_

  """

  ...

def Normal3iv(nx: typing.Any, ny: typing.Any, nz: typing.Any, v: Buffer) -> None:

  """

  B{Normal3b, Normal3bv, Normal3d, Normal3dv, Normal3f, Normal3fv, Normal3i, Normal3iv,
Normal3s, Normal3sv}

  Set the current normal vector

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glNormal.xhtml>`_

  """

  ...

def Normal3s(nx: typing.Any, ny: typing.Any, nz: typing.Any, v: Buffer) -> None:

  """

  B{Normal3b, Normal3bv, Normal3d, Normal3dv, Normal3f, Normal3fv, Normal3i, Normal3iv,
Normal3s, Normal3sv}

  Set the current normal vector

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glNormal.xhtml>`_

  """

  ...

def Normal3sv(nx: typing.Any, ny: typing.Any, nz: typing.Any, v: Buffer) -> None:

  """

  B{Normal3b, Normal3bv, Normal3d, Normal3dv, Normal3f, Normal3fv, Normal3i, Normal3iv,
Normal3s, Normal3sv}

  Set the current normal vector

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glNormal.xhtml>`_

  """

  ...

def glPixelMap(map: typing.Any, mapsize: int, values: Buffer) -> None:

  """

  B{glPixelMapfv, glPixelMapuiv, glPixelMapusv}

  Set up pixel transfer maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPixelMap.xhtml>`_

  """

  ...

def glPixelMapfv(map: typing.Any, mapsize: int, values: Buffer) -> None:

  """

  B{glPixelMapfv, glPixelMapuiv, glPixelMapusv}

  Set up pixel transfer maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPixelMap.xhtml>`_

  """

  ...

def glPixelMapuiv(map: typing.Any, mapsize: int, values: Buffer) -> None:

  """

  B{glPixelMapfv, glPixelMapuiv, glPixelMapusv}

  Set up pixel transfer maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPixelMap.xhtml>`_

  """

  ...

def glPixelMapusv(map: typing.Any, mapsize: int, values: Buffer) -> None:

  """

  B{glPixelMapfv, glPixelMapuiv, glPixelMapusv}

  Set up pixel transfer maps

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPixelMap.xhtml>`_

  """

  ...

def glPixelStore(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glPixelStoref, glPixelStorei}

  Set pixel storage modes

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPixelStore.xhtml>`_

  """

  ...

def glPixelStoref(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glPixelStoref, glPixelStorei}

  Set pixel storage modes

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPixelStore.xhtml>`_

  """

  ...

def glPixelStorei(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glPixelStoref, glPixelStorei}

  Set pixel storage modes

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPixelStore.xhtml>`_

  """

  ...

def glPixelTransfer(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glPixelTransferf, glPixelTransferi}

  Set pixel transfer modes

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPixelTransfer.xhtml>`_

  """

  ...

def glPixelTransferf(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glPixelTransferf, glPixelTransferi}

  Set pixel transfer modes

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPixelTransfer.xhtml>`_

  """

  ...

def glPixelTransferi(pname: typing.Any, param: typing.Any) -> None:

  """

  B{glPixelTransferf, glPixelTransferi}

  Set pixel transfer modes

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPixelTransfer.xhtml>`_

  """

  ...

def glPointSize(size: float) -> None:

  """

  Specify the diameter of rasterized points

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPointSize.xhtml>`_

  """

  ...

def glPolygonMode(face: typing.Any, mode: typing.Any) -> None:

  """

  Select a polygon rasterization mode

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPolygonMode.xhtml>`_

  """

  ...

def glPolygonOffset(factor: float, units: float) -> None:

  """

  Set the scale and units used to calculate depth values

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glPolygonOffset.xhtml>`_

  """

  ...

def glRasterPos(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos2d(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos2f(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos2i(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos2s(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos3d(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos3f(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos3i(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos3s(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos4d(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos4f(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos4i(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos4s(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos2dv(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos2fv(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos2iv(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos2sv(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos3dv(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos3fv(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos3iv(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos3sv(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos4dv(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos4fv(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos4iv(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glRasterPos4sv(x: typing.Any, y: typing.Any, z: typing.Any, w: typing.Any) -> None:

  """

  B{glRasterPos2d, glRasterPos2f, glRasterPos2i, glRasterPos2s, glRasterPos3d,
glRasterPos3f, glRasterPos3i, glRasterPos3s, glRasterPos4d, glRasterPos4f,
glRasterPos4i, glRasterPos4s, glRasterPos2dv, glRasterPos2fv, glRasterPos2iv,
glRasterPos2sv, glRasterPos3dv, glRasterPos3fv, glRasterPos3iv, glRasterPos3sv,
glRasterPos4dv, glRasterPos4fv, glRasterPos4iv, glRasterPos4sv}

  Specify the raster position for pixel operations

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRasterPos.xhtml>`_

  Note: If you are drawing to the 3d view with a Scriptlink of a space handler
the zoom level of the panels will scale the glRasterPos by the view matrix.
so a X of 10 will not always offset 10 pixels as you would expect.To work around this get the scale value of the view matrix and use it to scale your pixel values.

    .. code:: python

      import bgl
      xval, yval= 100, 40
      # Get the scale of the view matrix
      view_matrix = bgl.Buffer(bgl.GL_FLOAT, 16)
      bgl.glGetFloatv(bgl.GL_MODELVIEW_MATRIX, view_matrix)
      f = 1.0 / view_matrix[0]

      # Instead of the usual glRasterPos2i(xval, yval)
      bgl.glRasterPos2f(xval * f, yval * f)

  """

  ...

def glReadBuffer(mode: typing.Any) -> None:

  """

  Select a color buffer source for pixels.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glReadBuffer.xhtml>`_

  """

  ...

def glReadPixels(x: typing.Any, y: typing.Any, width: typing.Any, height: typing.Any, format: typing.Any, type: typing.Any, pixels: Buffer) -> None:

  """

  Read a block of pixels from the frame buffer

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glReadPixels.xhtml>`_

  """

  ...

def glRect(x1: typing.Any, y1: typing.Any, x2: typing.Any, y2: typing.Any, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glRectd, glRectf, glRecti, glRects, glRectdv, glRectfv, glRectiv, glRectsv}

  Draw a rectangle

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRect.xhtml>`_

  """

  ...

def glRectd(x1: typing.Any, y1: typing.Any, x2: typing.Any, y2: typing.Any, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glRectd, glRectf, glRecti, glRects, glRectdv, glRectfv, glRectiv, glRectsv}

  Draw a rectangle

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRect.xhtml>`_

  """

  ...

def glRectf(x1: typing.Any, y1: typing.Any, x2: typing.Any, y2: typing.Any, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glRectd, glRectf, glRecti, glRects, glRectdv, glRectfv, glRectiv, glRectsv}

  Draw a rectangle

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRect.xhtml>`_

  """

  ...

def glRecti(x1: typing.Any, y1: typing.Any, x2: typing.Any, y2: typing.Any, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glRectd, glRectf, glRecti, glRects, glRectdv, glRectfv, glRectiv, glRectsv}

  Draw a rectangle

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRect.xhtml>`_

  """

  ...

def glRects(x1: typing.Any, y1: typing.Any, x2: typing.Any, y2: typing.Any, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glRectd, glRectf, glRecti, glRects, glRectdv, glRectfv, glRectiv, glRectsv}

  Draw a rectangle

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRect.xhtml>`_

  """

  ...

def glRectdv(x1: typing.Any, y1: typing.Any, x2: typing.Any, y2: typing.Any, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glRectd, glRectf, glRecti, glRects, glRectdv, glRectfv, glRectiv, glRectsv}

  Draw a rectangle

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRect.xhtml>`_

  """

  ...

def glRectfv(x1: typing.Any, y1: typing.Any, x2: typing.Any, y2: typing.Any, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glRectd, glRectf, glRecti, glRects, glRectdv, glRectfv, glRectiv, glRectsv}

  Draw a rectangle

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRect.xhtml>`_

  """

  ...

def glRectiv(x1: typing.Any, y1: typing.Any, x2: typing.Any, y2: typing.Any, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glRectd, glRectf, glRecti, glRects, glRectdv, glRectfv, glRectiv, glRectsv}

  Draw a rectangle

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRect.xhtml>`_

  """

  ...

def glRectsv(x1: typing.Any, y1: typing.Any, x2: typing.Any, y2: typing.Any, v1: typing.Any, v2: typing.Any) -> None:

  """

  B{glRectd, glRectf, glRecti, glRects, glRectdv, glRectfv, glRectiv, glRectsv}

  Draw a rectangle

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRect.xhtml>`_

  """

  ...

def glRotate(angle: typing.Any, x: typing.Any, y: typing.Any, z: typing.Any) -> None:

  """

  B{glRotated, glRotatef}

  Multiply the current matrix by a rotation matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRotate.xhtml>`_

  """

  ...

def glRotated(angle: typing.Any, x: typing.Any, y: typing.Any, z: typing.Any) -> None:

  """

  B{glRotated, glRotatef}

  Multiply the current matrix by a rotation matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRotate.xhtml>`_

  """

  ...

def glRotatef(angle: typing.Any, x: typing.Any, y: typing.Any, z: typing.Any) -> None:

  """

  B{glRotated, glRotatef}

  Multiply the current matrix by a rotation matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glRotate.xhtml>`_

  """

  ...

def glScale(x: typing.Any, y: typing.Any, z: typing.Any) -> None:

  """

  B{glScaled, glScalef}

  Multiply the current matrix by a general scaling matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glScale.xhtml>`_

  """

  ...

def glScaled(x: typing.Any, y: typing.Any, z: typing.Any) -> None:

  """

  B{glScaled, glScalef}

  Multiply the current matrix by a general scaling matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glScale.xhtml>`_

  """

  ...

def glScalef(x: typing.Any, y: typing.Any, z: typing.Any) -> None:

  """

  B{glScaled, glScalef}

  Multiply the current matrix by a general scaling matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glScale.xhtml>`_

  """

  ...

def glScissor(x: typing.Any, y: typing.Any, width: typing.Any, height: typing.Any) -> None:

  """

  Define the scissor box

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glScissor.xhtml>`_

  """

  ...

def glStencilFunc(func: typing.Any, ref: int, mask: int) -> None:

  """

  Set function and reference value for stencil testing

  `OpenGL Docs <https://www.opengl.org/sdk/docs/man/docbook4/xhtml/glStencilFunc.xhtml>`_

  """

  ...

def glStencilMask(mask: int) -> None:

  """

  Control the writing of individual bits in the stencil planes

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glStencilMask.xhtml>`_

  """

  ...

def glStencilOp(fail: typing.Any, zfail: typing.Any, zpass: typing.Any) -> None:

  """

  Set stencil test actions

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glStencilOp.xhtml>`_

  """

  ...

def glTexCoord(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord1d(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord1f(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord1i(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord1s(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord2d(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord2f(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord2i(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord2s(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord3d(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord3f(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord3i(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord3s(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord4d(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord4f(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord4i(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord4s(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord1dv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord1fv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord1iv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord1sv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord2dv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord2fv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord2iv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord2sv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord3dv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord3fv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord3iv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord3sv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord4dv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord4fv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord4iv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexCoord4sv(s: typing.Any, t: typing.Any, r: typing.Any, q: typing.Any, v: Buffer) -> None:

  """

  B{glTexCoord1d, glTexCoord1f, glTexCoord1i, glTexCoord1s, glTexCoord2d, glTexCoord2f,
glTexCoord2i, glTexCoord2s, glTexCoord3d, glTexCoord3f, glTexCoord3i, glTexCoord3s,
glTexCoord4d, glTexCoord4f, glTexCoord4i, glTexCoord4s, glTexCoord1dv, glTexCoord1fv,
glTexCoord1iv, glTexCoord1sv, glTexCoord2dv, glTexCoord2fv, glTexCoord2iv,
glTexCoord2sv, glTexCoord3dv, glTexCoord3fv, glTexCoord3iv, glTexCoord3sv,
glTexCoord4dv, glTexCoord4fv, glTexCoord4iv, glTexCoord4sv}

  Set the current texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexCoord.xhtml>`_

  """

  ...

def glTexEnv(target: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTextEnvf, glTextEnvi, glTextEnvfv, glTextEnviv}

  Set texture environment parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexEnv.xhtml>`_

  """

  ...

def glTextEnvf(target: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTextEnvf, glTextEnvi, glTextEnvfv, glTextEnviv}

  Set texture environment parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexEnv.xhtml>`_

  """

  ...

def glTextEnvi(target: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTextEnvf, glTextEnvi, glTextEnvfv, glTextEnviv}

  Set texture environment parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexEnv.xhtml>`_

  """

  ...

def glTextEnvfv(target: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTextEnvf, glTextEnvi, glTextEnvfv, glTextEnviv}

  Set texture environment parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexEnv.xhtml>`_

  """

  ...

def glTextEnviv(target: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTextEnvf, glTextEnvi, glTextEnvfv, glTextEnviv}

  Set texture environment parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexEnv.xhtml>`_

  """

  ...

def glTexGen(coord: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTexGend, glTexGenf, glTexGeni, glTexGendv, glTexGenfv, glTexGeniv}

  Control the generation of texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexGen.xhtml>`_

  """

  ...

def glTexGend(coord: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTexGend, glTexGenf, glTexGeni, glTexGendv, glTexGenfv, glTexGeniv}

  Control the generation of texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexGen.xhtml>`_

  """

  ...

def glTexGenf(coord: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTexGend, glTexGenf, glTexGeni, glTexGendv, glTexGenfv, glTexGeniv}

  Control the generation of texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexGen.xhtml>`_

  """

  ...

def glTexGeni(coord: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTexGend, glTexGenf, glTexGeni, glTexGendv, glTexGenfv, glTexGeniv}

  Control the generation of texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexGen.xhtml>`_

  """

  ...

def glTexGendv(coord: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTexGend, glTexGenf, glTexGeni, glTexGendv, glTexGenfv, glTexGeniv}

  Control the generation of texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexGen.xhtml>`_

  """

  ...

def glTexGenfv(coord: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTexGend, glTexGenf, glTexGeni, glTexGendv, glTexGenfv, glTexGeniv}

  Control the generation of texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexGen.xhtml>`_

  """

  ...

def glTexGeniv(coord: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTexGend, glTexGenf, glTexGeni, glTexGendv, glTexGenfv, glTexGeniv}

  Control the generation of texture coordinates

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexGen.xhtml>`_

  """

  ...

def glTexImage1D(target: typing.Any, level: int, internalformat: int, width: int, border: int, format: typing.Any, type: typing.Any, pixels: Buffer) -> None:

  """

  Specify a one-dimensional texture image

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexImage1D.xhtml>`_

  """

  ...

def glTexImage2D(target: typing.Any, level: int, internalformat: int, width: int, height: int, border: int, format: typing.Any, type: typing.Any, pixels: Buffer) -> None:

  """

  Specify a two-dimensional texture image

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexImage2D.xhtml>`_

  """

  ...

def glTexParameter(target: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTexParameterf, glTexParameteri, glTexParameterfv, glTexParameteriv}

  Set texture parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexParameter.xhtml>`_

  """

  ...

def glTexParameterf(target: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTexParameterf, glTexParameteri, glTexParameterfv, glTexParameteriv}

  Set texture parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexParameter.xhtml>`_

  """

  ...

def glTexParameteri(target: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTexParameterf, glTexParameteri, glTexParameterfv, glTexParameteriv}

  Set texture parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexParameter.xhtml>`_

  """

  ...

def glTexParameterfv(target: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTexParameterf, glTexParameteri, glTexParameterfv, glTexParameteriv}

  Set texture parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexParameter.xhtml>`_

  """

  ...

def glTexParameteriv(target: typing.Any, pname: typing.Any, param: typing.Any) -> None:

  """

  B{glTexParameterf, glTexParameteri, glTexParameterfv, glTexParameteriv}

  Set texture parameters

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTexParameter.xhtml>`_

  """

  ...

def glTranslate(x: typing.Any, y: typing.Any, z: typing.Any) -> None:

  """

  B{glTranslatef, glTranslated}

  Multiply the current matrix by a translation matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTranslate.xhtml>`_

  """

  ...

def glTranslatef(x: typing.Any, y: typing.Any, z: typing.Any) -> None:

  """

  B{glTranslatef, glTranslated}

  Multiply the current matrix by a translation matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTranslate.xhtml>`_

  """

  ...

def glTranslated(x: typing.Any, y: typing.Any, z: typing.Any) -> None:

  """

  B{glTranslatef, glTranslated}

  Multiply the current matrix by a translation matrix

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glTranslate.xhtml>`_

  """

  ...

def glViewport(x: typing.Any, y: typing.Any, width: typing.Any, height: typing.Any) -> None:

  """

  Set the viewport

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glViewport.xhtml>`_

  """

  ...

def glUseProgram(program: int) -> None:

  """

  Installs a program object as part of current rendering state

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glUseProgram.xhtml>`_

  """

  ...

def glValidateProgram(program: int) -> None:

  """

  Validates a program object

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glValidateProgram.xhtml>`_

  """

  ...

def glLinkProgram(program: int) -> None:

  """

  Links a program object.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glLinkProgram.xhtml>`_

  """

  ...

def glActiveTexture(texture: int) -> None:

  """

  Select active texture unit.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glActiveTexture.xhtml>`_

  """

  ...

def glAttachShader(program: int, shader: int) -> None:

  """

  Attaches a shader object to a program object.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glAttachShader.xhtml>`_

  """

  ...

def glCompileShader(shader: int) -> None:

  """

  Compiles a shader object.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glCompileShader.xhtml>`_

  """

  ...

def glCreateProgram() -> int:

  """

  Creates a program object

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glCreateProgram.xhtml>`_

  """

  ...

def glCreateShader(shaderType: typing.Any) -> int:

  """

  Creates a shader object.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glCreateShader.xhtml>`_

  """

  ...

def glDeleteProgram(program: int) -> None:

  """

  Deletes a program object.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glDeleteProgram.xhtml>`_

  """

  ...

def glDeleteShader(shader: int) -> None:

  """

  Deletes a shader object.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glDeleteShader.xhtml>`_

  """

  ...

def glDetachShader(program: int, shader: int) -> None:

  """

  Detaches a shader object from a program object to which it is attached.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glDetachShader.xhtml>`_

  """

  ...

def glGetAttachedShaders(program: int, maxCount: int, count: Buffer, shaders: Buffer) -> None:

  """

  Returns the handles of the shader objects attached to a program object.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetAttachedShaders.xhtml>`_

  """

  ...

def glGetProgramInfoLog(program: int, maxLength: int, length: Buffer, infoLog: Buffer) -> None:

  """

  Returns the information log for a program object.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetProgramInfoLog.xhtml>`_

  """

  ...

def glGetShaderInfoLog(program: typing.Any, maxLength: int, length: Buffer, infoLog: Buffer) -> None:

  """

  Returns the information log for a shader object.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetShaderInfoLog.xhtml>`_

  """

  ...

def glGetProgramiv(program: int, pname: int, params: Buffer) -> None:

  """

  Returns a parameter from a program object.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetProgram.xhtml>`_

  """

  ...

def glIsShader(shader: int) -> None:

  """

  Determines if a name corresponds to a shader object.

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glIsShader.xhtml>`_

  """

  ...

def glIsProgram(program: int) -> None:

  """

  Determines if a name corresponds to a program object

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glIsProgram.xhtml>`_

  """

  ...

def glGetShaderSource(shader: int, bufSize: int, length: Buffer, source: Buffer) -> None:

  """

  Returns the source code string from a shader object

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glGetShaderSource.xhtml>`_

  """

  ...

def glShaderSource(shader: int, shader_string: str) -> None:

  """

  Replaces the source code in a shader object.

  `OpenGL Docs <https://www.opengl.org/sdk/docs/man/html/glShaderSource.xhtml>`_

  """

  ...

class Buffer:

  """

  The Buffer object is simply a block of memory that is delineated and initialized by the
user. Many OpenGL functions return data to a C-style pointer, however, because this
is not possible in python the Buffer object can be used to this end. Wherever pointer
notation is used in the OpenGL functions the Buffer object can be used in it's bgl
wrapper. In some instances the Buffer object will need to be initialized with the template
parameter, while in other instances the user will want to create just a blank buffer
which will be zeroed by default.

  .. code:: python

    import bgl

    myByteBuffer = bgl.Buffer(bgl.GL_BYTE, [32, 32])
    bgl.glGetPolygonStipple(myByteBuffer)

    print(myByteBuffer.dimensions)
    print(myByteBuffer.to_list())

    sliceBuffer = myByteBuffer[0:16]
    print(sliceBuffer)

  """

  dimensions: typing.Any = ...

  """

  The number of dimensions of the Buffer.

  """

  def to_list(self) -> None:

    """

    The contents of the Buffer as a python list.

    """

    ...

  def __init__(self, type: int, dimensions: typing.Any, template: typing.Any = None) -> typing.Any:

    """

    This will create a new Buffer object for use with other bgl OpenGL commands.
Only the type of argument to store in the buffer and the dimensions of the buffer
are necessary. Buffers are zeroed by default unless a template is supplied, in
which case the buffer is initialized to the template.

    """

    ...

GL_ACTIVE_ATTRIBUTES: int = ...

GL_ACTIVE_ATTRIBUTE_MAX_LENGTH: int = ...

GL_ACTIVE_TEXTURE: int = ...

GL_ACTIVE_UNIFORMS: int = ...

GL_ACTIVE_UNIFORM_BLOCKS: int = ...

GL_ACTIVE_UNIFORM_BLOCK_MAX_NAME_LENGTH: int = ...

GL_ACTIVE_UNIFORM_MAX_LENGTH: int = ...

GL_ALIASED_LINE_WIDTH_RANGE: int = ...

GL_ALPHA: int = ...

GL_ALREADY_SIGNALED: int = ...

GL_ALWAYS: int = ...

GL_AND: int = ...

GL_AND_INVERTED: int = ...

GL_AND_REVERSE: int = ...

GL_ANY_SAMPLES_PASSED: int = ...

GL_ARRAY_BUFFER: int = ...

GL_ARRAY_BUFFER_BINDING: int = ...

GL_ATTACHED_SHADERS: int = ...

GL_BACK: int = ...

GL_BACK_LEFT: int = ...

GL_BACK_RIGHT: int = ...

GL_BGR: int = ...

GL_BGRA: int = ...

GL_BGRA_INTEGER: int = ...

GL_BGR_INTEGER: int = ...

GL_BLEND: int = ...

GL_BLEND_DST: int = ...

GL_BLEND_DST_ALPHA: int = ...

GL_BLEND_DST_RGB: int = ...

GL_BLEND_EQUATION_ALPHA: int = ...

GL_BLEND_EQUATION_RGB: int = ...

GL_BLEND_SRC: int = ...

GL_BLEND_SRC_ALPHA: int = ...

GL_BLEND_SRC_RGB: int = ...

GL_BLUE: int = ...

GL_BLUE_INTEGER: int = ...

GL_BOOL: int = ...

GL_BOOL_VEC2: int = ...

GL_BOOL_VEC3: int = ...

GL_BOOL_VEC4: int = ...

GL_BUFFER_ACCESS: int = ...

GL_BUFFER_ACCESS_FLAGS: int = ...

GL_BUFFER_MAPPED: int = ...

GL_BUFFER_MAP_LENGTH: int = ...

GL_BUFFER_MAP_OFFSET: int = ...

GL_BUFFER_MAP_POINTER: int = ...

GL_BUFFER_SIZE: int = ...

GL_BUFFER_USAGE: int = ...

GL_BYTE: int = ...

GL_CCW: int = ...

GL_CLAMP_READ_COLOR: int = ...

GL_CLAMP_TO_BORDER: int = ...

GL_CLAMP_TO_EDGE: int = ...

GL_CLEAR: int = ...

GL_CLIP_DISTANCE0: int = ...

GL_CLIP_DISTANCE1: int = ...

GL_CLIP_DISTANCE2: int = ...

GL_CLIP_DISTANCE3: int = ...

GL_CLIP_DISTANCE4: int = ...

GL_CLIP_DISTANCE5: int = ...

GL_COLOR: int = ...

GL_COLOR_ATTACHMENT0: int = ...

GL_COLOR_ATTACHMENT1: int = ...

GL_COLOR_ATTACHMENT10: int = ...

GL_COLOR_ATTACHMENT11: int = ...

GL_COLOR_ATTACHMENT12: int = ...

GL_COLOR_ATTACHMENT13: int = ...

GL_COLOR_ATTACHMENT14: int = ...

GL_COLOR_ATTACHMENT15: int = ...

GL_COLOR_ATTACHMENT2: int = ...

GL_COLOR_ATTACHMENT3: int = ...

GL_COLOR_ATTACHMENT4: int = ...

GL_COLOR_ATTACHMENT5: int = ...

GL_COLOR_ATTACHMENT6: int = ...

GL_COLOR_ATTACHMENT7: int = ...

GL_COLOR_ATTACHMENT8: int = ...

GL_COLOR_ATTACHMENT9: int = ...

GL_COLOR_BUFFER_BIT: int = ...

GL_COLOR_CLEAR_VALUE: int = ...

GL_COLOR_LOGIC_OP: int = ...

GL_COLOR_WRITEMASK: int = ...

GL_COMPARE_REF_TO_TEXTURE: int = ...

GL_COMPILE_STATUS: int = ...

GL_COMPRESSED_RED: int = ...

GL_COMPRESSED_RED_RGTC1: int = ...

GL_COMPRESSED_RG: int = ...

GL_COMPRESSED_RGB: int = ...

GL_COMPRESSED_RGBA: int = ...

GL_COMPRESSED_RG_RGTC2: int = ...

GL_COMPRESSED_SIGNED_RED_RGTC1: int = ...

GL_COMPRESSED_SIGNED_RG_RGTC2: int = ...

GL_COMPRESSED_SRGB: int = ...

GL_COMPRESSED_SRGB_ALPHA: int = ...

GL_COMPRESSED_TEXTURE_FORMATS: int = ...

GL_CONDITION_SATISFIED: int = ...

GL_CONSTANT_ALPHA: int = ...

GL_CONSTANT_COLOR: int = ...

GL_CONTEXT_COMPATIBILITY_PROFILE_BIT: int = ...

GL_CONTEXT_CORE_PROFILE_BIT: int = ...

GL_CONTEXT_FLAGS: int = ...

GL_CONTEXT_FLAG_FORWARD_COMPATIBLE_BIT: int = ...

GL_CONTEXT_PROFILE_MASK: int = ...

GL_COPY: int = ...

GL_COPY_INVERTED: int = ...

GL_COPY_READ_BUFFER: int = ...

GL_COPY_WRITE_BUFFER: int = ...

GL_CULL_FACE: int = ...

GL_CULL_FACE_MODE: int = ...

GL_CURRENT_PROGRAM: int = ...

GL_CURRENT_QUERY: int = ...

GL_CURRENT_VERTEX_ATTRIB: int = ...

GL_CW: int = ...

GL_DECR: int = ...

GL_DECR_WRAP: int = ...

GL_DELETE_STATUS: int = ...

GL_DEPTH: int = ...

GL_DEPTH24_STENCIL8: int = ...

GL_DEPTH32F_STENCIL8: int = ...

GL_DEPTH_ATTACHMENT: int = ...

GL_DEPTH_BUFFER_BIT: int = ...

GL_DEPTH_CLAMP: int = ...

GL_DEPTH_CLEAR_VALUE: int = ...

GL_DEPTH_COMPONENT: int = ...

GL_DEPTH_COMPONENT16: int = ...

GL_DEPTH_COMPONENT24: int = ...

GL_DEPTH_COMPONENT32: int = ...

GL_DEPTH_COMPONENT32F: int = ...

GL_DEPTH_FUNC: int = ...

GL_DEPTH_RANGE: int = ...

GL_DEPTH_STENCIL: int = ...

GL_DEPTH_STENCIL_ATTACHMENT: int = ...

GL_DEPTH_TEST: int = ...

GL_DEPTH_WRITEMASK: int = ...

GL_DITHER: int = ...

GL_DONT_CARE: int = ...

GL_DOUBLE: int = ...

GL_DOUBLEBUFFER: int = ...

GL_DRAW_BUFFER: int = ...

GL_DRAW_BUFFER0: int = ...

GL_DRAW_BUFFER1: int = ...

GL_DRAW_BUFFER10: int = ...

GL_DRAW_BUFFER11: int = ...

GL_DRAW_BUFFER12: int = ...

GL_DRAW_BUFFER13: int = ...

GL_DRAW_BUFFER14: int = ...

GL_DRAW_BUFFER15: int = ...

GL_DRAW_BUFFER2: int = ...

GL_DRAW_BUFFER3: int = ...

GL_DRAW_BUFFER4: int = ...

GL_DRAW_BUFFER5: int = ...

GL_DRAW_BUFFER6: int = ...

GL_DRAW_BUFFER7: int = ...

GL_DRAW_BUFFER8: int = ...

GL_DRAW_BUFFER9: int = ...

GL_DRAW_FRAMEBUFFER: int = ...

GL_DRAW_FRAMEBUFFER_BINDING: int = ...

GL_DST_ALPHA: int = ...

GL_DST_COLOR: int = ...

GL_DYNAMIC_COPY: int = ...

GL_DYNAMIC_DRAW: int = ...

GL_DYNAMIC_READ: int = ...

GL_ELEMENT_ARRAY_BUFFER: int = ...

GL_ELEMENT_ARRAY_BUFFER_BINDING: int = ...

GL_EQUAL: int = ...

GL_EQUIV: int = ...

GL_EXTENSIONS: int = ...

GL_FALSE: int = ...

GL_FASTEST: int = ...

GL_FILL: int = ...

GL_FIRST_VERTEX_CONVENTION: int = ...

GL_FIXED_ONLY: int = ...

GL_FLOAT: int = ...

GL_FLOAT_32_UNSIGNED_INT_24_8_REV: int = ...

GL_FLOAT_MAT2: int = ...

GL_FLOAT_MAT2x3: int = ...

GL_FLOAT_MAT2x4: int = ...

GL_FLOAT_MAT3: int = ...

GL_FLOAT_MAT3x2: int = ...

GL_FLOAT_MAT3x4: int = ...

GL_FLOAT_MAT4: int = ...

GL_FLOAT_MAT4x2: int = ...

GL_FLOAT_MAT4x3: int = ...

GL_FLOAT_VEC2: int = ...

GL_FLOAT_VEC3: int = ...

GL_FLOAT_VEC4: int = ...

GL_FRAGMENT_SHADER: int = ...

GL_FRAGMENT_SHADER_DERIVATIVE_HINT: int = ...

GL_FRAMEBUFFER: int = ...

GL_FRAMEBUFFER_ATTACHMENT_ALPHA_SIZE: int = ...

GL_FRAMEBUFFER_ATTACHMENT_BLUE_SIZE: int = ...

GL_FRAMEBUFFER_ATTACHMENT_COLOR_ENCODING: int = ...

GL_FRAMEBUFFER_ATTACHMENT_COMPONENT_TYPE: int = ...

GL_FRAMEBUFFER_ATTACHMENT_DEPTH_SIZE: int = ...

GL_FRAMEBUFFER_ATTACHMENT_GREEN_SIZE: int = ...

GL_FRAMEBUFFER_ATTACHMENT_LAYERED: int = ...

GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME: int = ...

GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE: int = ...

GL_FRAMEBUFFER_ATTACHMENT_RED_SIZE: int = ...

GL_FRAMEBUFFER_ATTACHMENT_STENCIL_SIZE: int = ...

GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_CUBE_MAP_FACE: int = ...

GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LAYER: int = ...

GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL: int = ...

GL_FRAMEBUFFER_BINDING: int = ...

GL_FRAMEBUFFER_COMPLETE: int = ...

GL_FRAMEBUFFER_DEFAULT: int = ...

GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT: int = ...

GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER: int = ...

GL_FRAMEBUFFER_INCOMPLETE_LAYER_TARGETS: int = ...

GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT: int = ...

GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE: int = ...

GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER: int = ...

GL_FRAMEBUFFER_SRGB: int = ...

GL_FRAMEBUFFER_UNDEFINED: int = ...

GL_FRAMEBUFFER_UNSUPPORTED: int = ...

GL_FRONT: int = ...

GL_FRONT_AND_BACK: int = ...

GL_FRONT_FACE: int = ...

GL_FRONT_LEFT: int = ...

GL_FRONT_RIGHT: int = ...

GL_FUNC_ADD: int = ...

GL_FUNC_REVERSE_SUBTRACT: int = ...

GL_FUNC_SUBTRACT: int = ...

GL_GEOMETRY_INPUT_TYPE: int = ...

GL_GEOMETRY_OUTPUT_TYPE: int = ...

GL_GEOMETRY_SHADER: int = ...

GL_GEOMETRY_VERTICES_OUT: int = ...

GL_GEQUAL: int = ...

GL_GREATER: int = ...

GL_GREEN: int = ...

GL_GREEN_INTEGER: int = ...

GL_HALF_FLOAT: int = ...

GL_INCR: int = ...

GL_INCR_WRAP: int = ...

GL_INDEX: int = ...

GL_INFO_LOG_LENGTH: int = ...

GL_INT: int = ...

GL_INTERLEAVED_ATTRIBS: int = ...

GL_INT_2_10_10_10_REV: int = ...

GL_INT_SAMPLER_1D: int = ...

GL_INT_SAMPLER_1D_ARRAY: int = ...

GL_INT_SAMPLER_2D: int = ...

GL_INT_SAMPLER_2D_ARRAY: int = ...

GL_INT_SAMPLER_2D_MULTISAMPLE: int = ...

GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY: int = ...

GL_INT_SAMPLER_2D_RECT: int = ...

GL_INT_SAMPLER_3D: int = ...

GL_INT_SAMPLER_BUFFER: int = ...

GL_INT_SAMPLER_CUBE: int = ...

GL_INT_VEC2: int = ...

GL_INT_VEC3: int = ...

GL_INT_VEC4: int = ...

GL_INVALID_ENUM: int = ...

GL_INVALID_FRAMEBUFFER_OPERATION: int = ...

GL_INVALID_INDEX: int = ...

GL_INVALID_OPERATION: int = ...

GL_INVALID_VALUE: int = ...

GL_INVERT: int = ...

GL_KEEP: int = ...

GL_LAST_VERTEX_CONVENTION: int = ...

GL_LEFT: int = ...

GL_LEQUAL: int = ...

GL_LESS: int = ...

GL_LINE: int = ...

GL_LINEAR: int = ...

GL_LINEAR_MIPMAP_LINEAR: int = ...

GL_LINEAR_MIPMAP_NEAREST: int = ...

GL_LINES: int = ...

GL_LINES_ADJACENCY: int = ...

GL_LINE_LOOP: int = ...

GL_LINE_SMOOTH: int = ...

GL_LINE_SMOOTH_HINT: int = ...

GL_LINE_STRIP: int = ...

GL_LINE_STRIP_ADJACENCY: int = ...

GL_LINE_WIDTH: int = ...

GL_LINE_WIDTH_GRANULARITY: int = ...

GL_LINE_WIDTH_RANGE: int = ...

GL_LINK_STATUS: int = ...

GL_LOGIC_OP_MODE: int = ...

GL_LOWER_LEFT: int = ...

GL_MAJOR_VERSION: int = ...

GL_MAP_FLUSH_EXPLICIT_BIT: int = ...

GL_MAP_INVALIDATE_BUFFER_BIT: int = ...

GL_MAP_INVALIDATE_RANGE_BIT: int = ...

GL_MAP_READ_BIT: int = ...

GL_MAP_UNSYNCHRONIZED_BIT: int = ...

GL_MAP_WRITE_BIT: int = ...

GL_MAX: int = ...

GL_MAX_3D_TEXTURE_SIZE: int = ...

GL_MAX_ARRAY_TEXTURE_LAYERS: int = ...

GL_MAX_CLIP_DISTANCES: int = ...

GL_MAX_COLOR_ATTACHMENTS: int = ...

GL_MAX_COLOR_TEXTURE_SAMPLES: int = ...

GL_MAX_COMBINED_FRAGMENT_UNIFORM_COMPONENTS: int = ...

GL_MAX_COMBINED_GEOMETRY_UNIFORM_COMPONENTS: int = ...

GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS: int = ...

GL_MAX_COMBINED_UNIFORM_BLOCKS: int = ...

GL_MAX_COMBINED_VERTEX_UNIFORM_COMPONENTS: int = ...

GL_MAX_CUBE_MAP_TEXTURE_SIZE: int = ...

GL_MAX_DEPTH_TEXTURE_SAMPLES: int = ...

GL_MAX_DRAW_BUFFERS: int = ...

GL_MAX_DUAL_SOURCE_DRAW_BUFFERS: int = ...

GL_MAX_ELEMENTS_INDICES: int = ...

GL_MAX_ELEMENTS_VERTICES: int = ...

GL_MAX_FRAGMENT_INPUT_COMPONENTS: int = ...

GL_MAX_FRAGMENT_UNIFORM_BLOCKS: int = ...

GL_MAX_FRAGMENT_UNIFORM_COMPONENTS: int = ...

GL_MAX_GEOMETRY_INPUT_COMPONENTS: int = ...

GL_MAX_GEOMETRY_OUTPUT_COMPONENTS: int = ...

GL_MAX_GEOMETRY_OUTPUT_VERTICES: int = ...

GL_MAX_GEOMETRY_TEXTURE_IMAGE_UNITS: int = ...

GL_MAX_GEOMETRY_TOTAL_OUTPUT_COMPONENTS: int = ...

GL_MAX_GEOMETRY_UNIFORM_BLOCKS: int = ...

GL_MAX_GEOMETRY_UNIFORM_COMPONENTS: int = ...

GL_MAX_INTEGER_SAMPLES: int = ...

GL_MAX_PROGRAM_TEXEL_OFFSET: int = ...

GL_MAX_RECTANGLE_TEXTURE_SIZE: int = ...

GL_MAX_RENDERBUFFER_SIZE: int = ...

GL_MAX_SAMPLES: int = ...

GL_MAX_SAMPLE_MASK_WORDS: int = ...

GL_MAX_SERVER_WAIT_TIMEOUT: int = ...

GL_MAX_TEXTURE_BUFFER_SIZE: int = ...

GL_MAX_TEXTURE_IMAGE_UNITS: int = ...

GL_MAX_TEXTURE_LOD_BIAS: int = ...

GL_MAX_TEXTURE_SIZE: int = ...

GL_MAX_TRANSFORM_FEEDBACK_INTERLEAVED_COMPONENTS: int = ...

GL_MAX_TRANSFORM_FEEDBACK_SEPARATE_ATTRIBS: int = ...

GL_MAX_TRANSFORM_FEEDBACK_SEPARATE_COMPONENTS: int = ...

GL_MAX_UNIFORM_BLOCK_SIZE: int = ...

GL_MAX_UNIFORM_BUFFER_BINDINGS: int = ...

GL_MAX_VARYING_COMPONENTS: int = ...

GL_MAX_VARYING_FLOATS: int = ...

GL_MAX_VERTEX_ATTRIBS: int = ...

GL_MAX_VERTEX_OUTPUT_COMPONENTS: int = ...

GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS: int = ...

GL_MAX_VERTEX_UNIFORM_BLOCKS: int = ...

GL_MAX_VERTEX_UNIFORM_COMPONENTS: int = ...

GL_MAX_VIEWPORT_DIMS: int = ...

GL_MIN: int = ...

GL_MINOR_VERSION: int = ...

GL_MIN_PROGRAM_TEXEL_OFFSET: int = ...

GL_MIRRORED_REPEAT: int = ...

GL_MULTISAMPLE: int = ...

GL_NAND: int = ...

GL_NEAREST: int = ...

GL_NEAREST_MIPMAP_LINEAR: int = ...

GL_NEAREST_MIPMAP_NEAREST: int = ...

GL_NEVER: int = ...

GL_NICEST: int = ...

GL_NONE: int = ...

GL_NOOP: int = ...

GL_NOR: int = ...

GL_NOTEQUAL: int = ...

GL_NO_ERROR: int = ...

GL_NUM_COMPRESSED_TEXTURE_FORMATS: int = ...

GL_NUM_EXTENSIONS: int = ...

GL_OBJECT_TYPE: int = ...

GL_ONE: int = ...

GL_ONE_MINUS_CONSTANT_ALPHA: int = ...

GL_ONE_MINUS_CONSTANT_COLOR: int = ...

GL_ONE_MINUS_DST_ALPHA: int = ...

GL_ONE_MINUS_DST_COLOR: int = ...

GL_ONE_MINUS_SRC1_ALPHA: int = ...

GL_ONE_MINUS_SRC1_COLOR: int = ...

GL_ONE_MINUS_SRC_ALPHA: int = ...

GL_ONE_MINUS_SRC_COLOR: int = ...

GL_OR: int = ...

GL_OR_INVERTED: int = ...

GL_OR_REVERSE: int = ...

GL_OUT_OF_MEMORY: int = ...

GL_PACK_ALIGNMENT: int = ...

GL_PACK_IMAGE_HEIGHT: int = ...

GL_PACK_LSB_FIRST: int = ...

GL_PACK_ROW_LENGTH: int = ...

GL_PACK_SKIP_IMAGES: int = ...

GL_PACK_SKIP_PIXELS: int = ...

GL_PACK_SKIP_ROWS: int = ...

GL_PACK_SWAP_BYTES: int = ...

GL_PIXEL_PACK_BUFFER: int = ...

GL_PIXEL_PACK_BUFFER_BINDING: int = ...

GL_PIXEL_UNPACK_BUFFER: int = ...

GL_PIXEL_UNPACK_BUFFER_BINDING: int = ...

GL_POINT: int = ...

GL_POINTS: int = ...

GL_POINT_FADE_THRESHOLD_SIZE: int = ...

GL_POINT_SIZE: int = ...

GL_POINT_SPRITE_COORD_ORIGIN: int = ...

GL_POLYGON_MODE: int = ...

GL_POLYGON_OFFSET_FACTOR: int = ...

GL_POLYGON_OFFSET_FILL: int = ...

GL_POLYGON_OFFSET_LINE: int = ...

GL_POLYGON_OFFSET_POINT: int = ...

GL_POLYGON_OFFSET_UNITS: int = ...

GL_POLYGON_SMOOTH: int = ...

GL_POLYGON_SMOOTH_HINT: int = ...

GL_PRIMITIVES_GENERATED: int = ...

GL_PRIMITIVE_RESTART: int = ...

GL_PRIMITIVE_RESTART_INDEX: int = ...

GL_PROGRAM_POINT_SIZE: int = ...

GL_PROVOKING_VERTEX: int = ...

GL_PROXY_TEXTURE_1D: int = ...

GL_PROXY_TEXTURE_1D_ARRAY: int = ...

GL_PROXY_TEXTURE_2D: int = ...

GL_PROXY_TEXTURE_2D_ARRAY: int = ...

GL_PROXY_TEXTURE_2D_MULTISAMPLE: int = ...

GL_PROXY_TEXTURE_2D_MULTISAMPLE_ARRAY: int = ...

GL_PROXY_TEXTURE_3D: int = ...

GL_PROXY_TEXTURE_CUBE_MAP: int = ...

GL_PROXY_TEXTURE_RECTANGLE: int = ...

GL_QUADS_FOLLOW_PROVOKING_VERTEX_CONVENTION: int = ...

GL_QUERY_BY_REGION_NO_WAIT: int = ...

GL_QUERY_BY_REGION_WAIT: int = ...

GL_QUERY_COUNTER_BITS: int = ...

GL_QUERY_NO_WAIT: int = ...

GL_QUERY_RESULT: int = ...

GL_QUERY_RESULT_AVAILABLE: int = ...

GL_QUERY_WAIT: int = ...

GL_R11F_G11F_B10F: int = ...

GL_R16: int = ...

GL_R16F: int = ...

GL_R16I: int = ...

GL_R16UI: int = ...

GL_R16_SNORM: int = ...

GL_R32F: int = ...

GL_R32I: int = ...

GL_R32UI: int = ...

GL_R3_G3_B2: int = ...

GL_R8: int = ...

GL_R8I: int = ...

GL_R8UI: int = ...

GL_R8_SNORM: int = ...

GL_RASTERIZER_DISCARD: int = ...

GL_READ_BUFFER: int = ...

GL_READ_FRAMEBUFFER: int = ...

GL_READ_FRAMEBUFFER_BINDING: int = ...

GL_READ_ONLY: int = ...

GL_READ_WRITE: int = ...

GL_RED: int = ...

GL_RED_INTEGER: int = ...

GL_RENDERBUFFER: int = ...

GL_RENDERBUFFER_ALPHA_SIZE: int = ...

GL_RENDERBUFFER_BINDING: int = ...

GL_RENDERBUFFER_BLUE_SIZE: int = ...

GL_RENDERBUFFER_DEPTH_SIZE: int = ...

GL_RENDERBUFFER_GREEN_SIZE: int = ...

GL_RENDERBUFFER_HEIGHT: int = ...

GL_RENDERBUFFER_INTERNAL_FORMAT: int = ...

GL_RENDERBUFFER_RED_SIZE: int = ...

GL_RENDERBUFFER_SAMPLES: int = ...

GL_RENDERBUFFER_STENCIL_SIZE: int = ...

GL_RENDERBUFFER_WIDTH: int = ...

GL_RENDERER: int = ...

GL_REPEAT: int = ...

GL_REPLACE: int = ...

GL_RG: int = ...

GL_RG16: int = ...

GL_RG16F: int = ...

GL_RG16I: int = ...

GL_RG16UI: int = ...

GL_RG16_SNORM: int = ...

GL_RG32F: int = ...

GL_RG32I: int = ...

GL_RG32UI: int = ...

GL_RG8: int = ...

GL_RG8I: int = ...

GL_RG8UI: int = ...

GL_RG8_SNORM: int = ...

GL_RGB: int = ...

GL_RGB10: int = ...

GL_RGB10_A2: int = ...

GL_RGB10_A2UI: int = ...

GL_RGB12: int = ...

GL_RGB16: int = ...

GL_RGB16F: int = ...

GL_RGB16I: int = ...

GL_RGB16UI: int = ...

GL_RGB16_SNORM: int = ...

GL_RGB32F: int = ...

GL_RGB32I: int = ...

GL_RGB32UI: int = ...

GL_RGB4: int = ...

GL_RGB5: int = ...

GL_RGB5_A1: int = ...

GL_RGB8: int = ...

GL_RGB8I: int = ...

GL_RGB8UI: int = ...

GL_RGB8_SNORM: int = ...

GL_RGB9_E5: int = ...

GL_RGBA: int = ...

GL_RGBA12: int = ...

GL_RGBA16: int = ...

GL_RGBA16F: int = ...

GL_RGBA16I: int = ...

GL_RGBA16UI: int = ...

GL_RGBA16_SNORM: int = ...

GL_RGBA2: int = ...

GL_RGBA32F: int = ...

GL_RGBA32I: int = ...

GL_RGBA32UI: int = ...

GL_RGBA4: int = ...

GL_RGBA8: int = ...

GL_RGBA8I: int = ...

GL_RGBA8UI: int = ...

GL_RGBA8_SNORM: int = ...

GL_RGBA_INTEGER: int = ...

GL_RGB_INTEGER: int = ...

GL_RG_INTEGER: int = ...

GL_RIGHT: int = ...

GL_SAMPLER_1D: int = ...

GL_SAMPLER_1D_ARRAY: int = ...

GL_SAMPLER_1D_ARRAY_SHADOW: int = ...

GL_SAMPLER_1D_SHADOW: int = ...

GL_SAMPLER_2D: int = ...

GL_SAMPLER_2D_ARRAY: int = ...

GL_SAMPLER_2D_ARRAY_SHADOW: int = ...

GL_SAMPLER_2D_MULTISAMPLE: int = ...

GL_SAMPLER_2D_MULTISAMPLE_ARRAY: int = ...

GL_SAMPLER_2D_RECT: int = ...

GL_SAMPLER_2D_RECT_SHADOW: int = ...

GL_SAMPLER_2D_SHADOW: int = ...

GL_SAMPLER_3D: int = ...

GL_SAMPLER_BINDING: int = ...

GL_SAMPLER_BUFFER: int = ...

GL_SAMPLER_CUBE: int = ...

GL_SAMPLER_CUBE_SHADOW: int = ...

GL_SAMPLES: int = ...

GL_SAMPLES_PASSED: int = ...

GL_SAMPLE_ALPHA_TO_COVERAGE: int = ...

GL_SAMPLE_ALPHA_TO_ONE: int = ...

GL_SAMPLE_BUFFERS: int = ...

GL_SAMPLE_COVERAGE: int = ...

GL_SAMPLE_COVERAGE_INVERT: int = ...

GL_SAMPLE_COVERAGE_VALUE: int = ...

GL_SAMPLE_MASK: int = ...

GL_SAMPLE_MASK_VALUE: int = ...

GL_SAMPLE_POSITION: int = ...

GL_SCISSOR_BOX: int = ...

GL_SCISSOR_TEST: int = ...

GL_SEPARATE_ATTRIBS: int = ...

GL_SET: int = ...

GL_SHADER_SOURCE_LENGTH: int = ...

GL_SHADER_TYPE: int = ...

GL_SHADING_LANGUAGE_VERSION: int = ...

GL_SHORT: int = ...

GL_SIGNALED: int = ...

GL_SIGNED_NORMALIZED: int = ...

GL_SMOOTH_LINE_WIDTH_GRANULARITY: int = ...

GL_SMOOTH_LINE_WIDTH_RANGE: int = ...

GL_SMOOTH_POINT_SIZE_GRANULARITY: int = ...

GL_SMOOTH_POINT_SIZE_RANGE: int = ...

GL_SRC1_COLOR: int = ...

GL_SRC_ALPHA: int = ...

GL_SRC_ALPHA_SATURATE: int = ...

GL_SRC_COLOR: int = ...

GL_SRGB: int = ...

GL_SRGB8: int = ...

GL_SRGB8_ALPHA8: int = ...

GL_SRGB_ALPHA: int = ...

GL_STATIC_COPY: int = ...

GL_STATIC_DRAW: int = ...

GL_STATIC_READ: int = ...

GL_STENCIL: int = ...

GL_STENCIL_ATTACHMENT: int = ...

GL_STENCIL_BACK_FAIL: int = ...

GL_STENCIL_BACK_FUNC: int = ...

GL_STENCIL_BACK_PASS_DEPTH_FAIL: int = ...

GL_STENCIL_BACK_PASS_DEPTH_PASS: int = ...

GL_STENCIL_BACK_REF: int = ...

GL_STENCIL_BACK_VALUE_MASK: int = ...

GL_STENCIL_BACK_WRITEMASK: int = ...

GL_STENCIL_BUFFER_BIT: int = ...

GL_STENCIL_CLEAR_VALUE: int = ...

GL_STENCIL_FAIL: int = ...

GL_STENCIL_FUNC: int = ...

GL_STENCIL_INDEX: int = ...

GL_STENCIL_INDEX1: int = ...

GL_STENCIL_INDEX16: int = ...

GL_STENCIL_INDEX4: int = ...

GL_STENCIL_INDEX8: int = ...

GL_STENCIL_PASS_DEPTH_FAIL: int = ...

GL_STENCIL_PASS_DEPTH_PASS: int = ...

GL_STENCIL_REF: int = ...

GL_STENCIL_TEST: int = ...

GL_STENCIL_VALUE_MASK: int = ...

GL_STENCIL_WRITEMASK: int = ...

GL_STEREO: int = ...

GL_STREAM_COPY: int = ...

GL_STREAM_DRAW: int = ...

GL_STREAM_READ: int = ...

GL_SUBPIXEL_BITS: int = ...

GL_SYNC_CONDITION: int = ...

GL_SYNC_FENCE: int = ...

GL_SYNC_FLAGS: int = ...

GL_SYNC_FLUSH_COMMANDS_BIT: int = ...

GL_SYNC_GPU_COMMANDS_COMPLETE: int = ...

GL_SYNC_STATUS: int = ...

GL_TEXTURE: int = ...

GL_TEXTURE0: int = ...

GL_TEXTURE1: int = ...

GL_TEXTURE10: int = ...

GL_TEXTURE11: int = ...

GL_TEXTURE12: int = ...

GL_TEXTURE13: int = ...

GL_TEXTURE14: int = ...

GL_TEXTURE15: int = ...

GL_TEXTURE16: int = ...

GL_TEXTURE17: int = ...

GL_TEXTURE18: int = ...

GL_TEXTURE19: int = ...

GL_TEXTURE2: int = ...

GL_TEXTURE20: int = ...

GL_TEXTURE21: int = ...

GL_TEXTURE22: int = ...

GL_TEXTURE23: int = ...

GL_TEXTURE24: int = ...

GL_TEXTURE25: int = ...

GL_TEXTURE26: int = ...

GL_TEXTURE27: int = ...

GL_TEXTURE28: int = ...

GL_TEXTURE29: int = ...

GL_TEXTURE3: int = ...

GL_TEXTURE30: int = ...

GL_TEXTURE31: int = ...

GL_TEXTURE4: int = ...

GL_TEXTURE5: int = ...

GL_TEXTURE6: int = ...

GL_TEXTURE7: int = ...

GL_TEXTURE8: int = ...

GL_TEXTURE9: int = ...

GL_TEXTURE_1D: int = ...

GL_TEXTURE_1D_ARRAY: int = ...

GL_TEXTURE_2D: int = ...

GL_TEXTURE_2D_ARRAY: int = ...

GL_TEXTURE_2D_MULTISAMPLE: int = ...

GL_TEXTURE_2D_MULTISAMPLE_ARRAY: int = ...

GL_TEXTURE_3D: int = ...

GL_TEXTURE_ALPHA_SIZE: int = ...

GL_TEXTURE_ALPHA_TYPE: int = ...

GL_TEXTURE_BASE_LEVEL: int = ...

GL_TEXTURE_BINDING_1D: int = ...

GL_TEXTURE_BINDING_1D_ARRAY: int = ...

GL_TEXTURE_BINDING_2D: int = ...

GL_TEXTURE_BINDING_2D_ARRAY: int = ...

GL_TEXTURE_BINDING_2D_MULTISAMPLE: int = ...

GL_TEXTURE_BINDING_2D_MULTISAMPLE_ARRAY: int = ...

GL_TEXTURE_BINDING_3D: int = ...

GL_TEXTURE_BINDING_BUFFER: int = ...

GL_TEXTURE_BINDING_CUBE_MAP: int = ...

GL_TEXTURE_BINDING_RECTANGLE: int = ...

GL_TEXTURE_BLUE_SIZE: int = ...

GL_TEXTURE_BLUE_TYPE: int = ...

GL_TEXTURE_BORDER_COLOR: int = ...

GL_TEXTURE_BUFFER: int = ...

GL_TEXTURE_BUFFER_DATA_STORE_BINDING: int = ...

GL_TEXTURE_COMPARE_FUNC: int = ...

GL_TEXTURE_COMPARE_MODE: int = ...

GL_TEXTURE_COMPRESSED: int = ...

GL_TEXTURE_COMPRESSED_IMAGE_SIZE: int = ...

GL_TEXTURE_COMPRESSION_HINT: int = ...

GL_TEXTURE_CUBE_MAP: int = ...

GL_TEXTURE_CUBE_MAP_NEGATIVE_X: int = ...

GL_TEXTURE_CUBE_MAP_NEGATIVE_Y: int = ...

GL_TEXTURE_CUBE_MAP_NEGATIVE_Z: int = ...

GL_TEXTURE_CUBE_MAP_POSITIVE_X: int = ...

GL_TEXTURE_CUBE_MAP_POSITIVE_Y: int = ...

GL_TEXTURE_CUBE_MAP_POSITIVE_Z: int = ...

GL_TEXTURE_CUBE_MAP_SEAMLESS: int = ...

GL_TEXTURE_DEPTH: int = ...

GL_TEXTURE_DEPTH_SIZE: int = ...

GL_TEXTURE_DEPTH_TYPE: int = ...

GL_TEXTURE_FIXED_SAMPLE_LOCATIONS: int = ...

GL_TEXTURE_GREEN_SIZE: int = ...

GL_TEXTURE_GREEN_TYPE: int = ...

GL_TEXTURE_HEIGHT: int = ...

GL_TEXTURE_INTERNAL_FORMAT: int = ...

GL_TEXTURE_LOD_BIAS: int = ...

GL_TEXTURE_MAG_FILTER: int = ...

GL_TEXTURE_MAX_LEVEL: int = ...

GL_TEXTURE_MAX_LOD: int = ...

GL_TEXTURE_MIN_FILTER: int = ...

GL_TEXTURE_MIN_LOD: int = ...

GL_TEXTURE_RECTANGLE: int = ...

GL_TEXTURE_RED_SIZE: int = ...

GL_TEXTURE_RED_TYPE: int = ...

GL_TEXTURE_SAMPLES: int = ...

GL_TEXTURE_SHARED_SIZE: int = ...

GL_TEXTURE_STENCIL_SIZE: int = ...

GL_TEXTURE_SWIZZLE_A: int = ...

GL_TEXTURE_SWIZZLE_B: int = ...

GL_TEXTURE_SWIZZLE_G: int = ...

GL_TEXTURE_SWIZZLE_R: int = ...

GL_TEXTURE_SWIZZLE_RGBA: int = ...

GL_TEXTURE_WIDTH: int = ...

GL_TEXTURE_WRAP_R: int = ...

GL_TEXTURE_WRAP_S: int = ...

GL_TEXTURE_WRAP_T: int = ...

GL_TIMEOUT_EXPIRED: int = ...

GL_TIMEOUT_IGNORED: int = ...

GL_TIMESTAMP: int = ...

GL_TIME_ELAPSED: int = ...

GL_TRANSFORM_FEEDBACK_BUFFER: int = ...

GL_TRANSFORM_FEEDBACK_BUFFER_BINDING: int = ...

GL_TRANSFORM_FEEDBACK_BUFFER_MODE: int = ...

GL_TRANSFORM_FEEDBACK_BUFFER_SIZE: int = ...

GL_TRANSFORM_FEEDBACK_BUFFER_START: int = ...

GL_TRANSFORM_FEEDBACK_PRIMITIVES_WRITTEN: int = ...

GL_TRANSFORM_FEEDBACK_VARYINGS: int = ...

GL_TRANSFORM_FEEDBACK_VARYING_MAX_LENGTH: int = ...

GL_TRIANGLES: int = ...

GL_TRIANGLES_ADJACENCY: int = ...

GL_TRIANGLE_FAN: int = ...

GL_TRIANGLE_STRIP: int = ...

GL_TRIANGLE_STRIP_ADJACENCY: int = ...

GL_TRUE: int = ...

GL_UNIFORM_ARRAY_STRIDE: int = ...

GL_UNIFORM_BLOCK_ACTIVE_UNIFORMS: int = ...

GL_UNIFORM_BLOCK_ACTIVE_UNIFORM_INDICES: int = ...

GL_UNIFORM_BLOCK_BINDING: int = ...

GL_UNIFORM_BLOCK_DATA_SIZE: int = ...

GL_UNIFORM_BLOCK_INDEX: int = ...

GL_UNIFORM_BLOCK_NAME_LENGTH: int = ...

GL_UNIFORM_BLOCK_REFERENCED_BY_FRAGMENT_SHADER: int = ...

GL_UNIFORM_BLOCK_REFERENCED_BY_GEOMETRY_SHADER: int = ...

GL_UNIFORM_BLOCK_REFERENCED_BY_VERTEX_SHADER: int = ...

GL_UNIFORM_BUFFER: int = ...

GL_UNIFORM_BUFFER_BINDING: int = ...

GL_UNIFORM_BUFFER_OFFSET_ALIGNMENT: int = ...

GL_UNIFORM_BUFFER_SIZE: int = ...

GL_UNIFORM_BUFFER_START: int = ...

GL_UNIFORM_IS_ROW_MAJOR: int = ...

GL_UNIFORM_MATRIX_STRIDE: int = ...

GL_UNIFORM_NAME_LENGTH: int = ...

GL_UNIFORM_OFFSET: int = ...

GL_UNIFORM_SIZE: int = ...

GL_UNIFORM_TYPE: int = ...

GL_UNPACK_ALIGNMENT: int = ...

GL_UNPACK_IMAGE_HEIGHT: int = ...

GL_UNPACK_LSB_FIRST: int = ...

GL_UNPACK_ROW_LENGTH: int = ...

GL_UNPACK_SKIP_IMAGES: int = ...

GL_UNPACK_SKIP_PIXELS: int = ...

GL_UNPACK_SKIP_ROWS: int = ...

GL_UNPACK_SWAP_BYTES: int = ...

GL_UNSIGNALED: int = ...

GL_UNSIGNED_BYTE: int = ...

GL_UNSIGNED_BYTE_2_3_3_REV: int = ...

GL_UNSIGNED_BYTE_3_3_2: int = ...

GL_UNSIGNED_INT: int = ...

GL_UNSIGNED_INT_10F_11F_11F_REV: int = ...

GL_UNSIGNED_INT_10_10_10_2: int = ...

GL_UNSIGNED_INT_24_8: int = ...

GL_UNSIGNED_INT_2_10_10_10_REV: int = ...

GL_UNSIGNED_INT_5_9_9_9_REV: int = ...

GL_UNSIGNED_INT_8_8_8_8: int = ...

GL_UNSIGNED_INT_8_8_8_8_REV: int = ...

GL_UNSIGNED_INT_SAMPLER_1D: int = ...

GL_UNSIGNED_INT_SAMPLER_1D_ARRAY: int = ...

GL_UNSIGNED_INT_SAMPLER_2D: int = ...

GL_UNSIGNED_INT_SAMPLER_2D_ARRAY: int = ...

GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE: int = ...

GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY: int = ...

GL_UNSIGNED_INT_SAMPLER_2D_RECT: int = ...

GL_UNSIGNED_INT_SAMPLER_3D: int = ...

GL_UNSIGNED_INT_SAMPLER_BUFFER: int = ...

GL_UNSIGNED_INT_SAMPLER_CUBE: int = ...

GL_UNSIGNED_INT_VEC2: int = ...

GL_UNSIGNED_INT_VEC3: int = ...

GL_UNSIGNED_INT_VEC4: int = ...

GL_UNSIGNED_NORMALIZED: int = ...

GL_UNSIGNED_SHORT: int = ...

GL_UNSIGNED_SHORT_1_5_5_5_REV: int = ...

GL_UNSIGNED_SHORT_4_4_4_4: int = ...

GL_UNSIGNED_SHORT_4_4_4_4_REV: int = ...

GL_UNSIGNED_SHORT_5_5_5_1: int = ...

GL_UNSIGNED_SHORT_5_6_5: int = ...

GL_UNSIGNED_SHORT_5_6_5_REV: int = ...

GL_UPPER_LEFT: int = ...

GL_VALIDATE_STATUS: int = ...

GL_VENDOR: int = ...

GL_VERSION: int = ...

GL_VERTEX_ARRAY_BINDING: int = ...

GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING: int = ...

GL_VERTEX_ATTRIB_ARRAY_DIVISOR: int = ...

GL_VERTEX_ATTRIB_ARRAY_ENABLED: int = ...

GL_VERTEX_ATTRIB_ARRAY_INTEGER: int = ...

GL_VERTEX_ATTRIB_ARRAY_NORMALIZED: int = ...

GL_VERTEX_ATTRIB_ARRAY_POINTER: int = ...

GL_VERTEX_ATTRIB_ARRAY_SIZE: int = ...

GL_VERTEX_ATTRIB_ARRAY_STRIDE: int = ...

GL_VERTEX_ATTRIB_ARRAY_TYPE: int = ...

GL_VERTEX_PROGRAM_POINT_SIZE: int = ...

GL_VERTEX_SHADER: int = ...

GL_VIEWPORT: int = ...

GL_WAIT_FAILED: int = ...

GL_WRITE_ONLY: int = ...

GL_XOR: int = ...

GL_ZERO: int = ...

def glDeleteBuffers(n: int, buffers: typing.Any) -> None:

  """

    Delete named buffer objects

  `OpenGL Docs <https://khronos.org/registry/OpenGL-Refpages/gl4/html/glDeleteBuffers.xhtml>`_

  """

  ...
