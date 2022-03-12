"""


Application Data (bpy.app)
**************************

This module contains application values that remain unchanged during runtime.

:data:`autoexec_fail`

:data:`autoexec_fail_message`

:data:`autoexec_fail_quiet`

:data:`debug`

:data:`debug_depsgraph`

:data:`debug_depsgraph_build`

:data:`debug_depsgraph_eval`

:data:`debug_depsgraph_pretty`

:data:`debug_depsgraph_tag`

:data:`debug_depsgraph_time`

:data:`debug_events`

:data:`debug_ffmpeg`

:data:`debug_freestyle`

:data:`debug_handlers`

:data:`debug_io`

:data:`debug_python`

:data:`debug_simdata`

:data:`debug_value`

:data:`debug_wm`

:data:`driver_namespace`

:data:`render_icon_size`

:data:`render_preview_size`

:data:`tempdir`

:data:`use_event_simulate`

:data:`use_userpref_skip_save_on_exit`

:data:`background`

:data:`factory_startup`

:data:`build_branch`

:data:`build_cflags`

:data:`build_commit_date`

:data:`build_commit_time`

:data:`build_cxxflags`

:data:`build_date`

:data:`build_hash`

:data:`build_linkflags`

:data:`build_platform`

:data:`build_system`

:data:`build_time`

:data:`build_type`

:data:`build_commit_timestamp`

:data:`binary_path`

:data:`version_char`

:data:`version_cycle`

:data:`version_string`

:data:`version`

:data:`version_file`

:data:`alembic`

:data:`build_options`

:data:`ffmpeg`

:data:`ocio`

:data:`oiio`

:data:`opensubdiv`

:data:`openvdb`

:data:`sdl`

:data:`usd`

"""

from . import translations

from . import timers

from . import icons

from . import handlers

import typing

autoexec_fail: typing.Any = ...

"""

Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

"""

autoexec_fail_message: typing.Any = ...

"""

Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

"""

autoexec_fail_quiet: typing.Any = ...

"""

Undocumented, consider `contributing <https://developer.blender.org/T51061>`_.

"""

debug: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_depsgraph: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_depsgraph_build: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_depsgraph_eval: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_depsgraph_pretty: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_depsgraph_tag: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_depsgraph_time: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_events: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_ffmpeg: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_freestyle: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_handlers: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_io: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_python: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_simdata: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

debug_value: typing.Any = ...

"""

Short, number which can be set to non-zero values for testing purposes

"""

debug_wm: typing.Any = ...

"""

Boolean, for debug info (started with --debug / --debug_* matching this attribute name)

"""

driver_namespace: typing.Any = ...

"""

Dictionary for drivers namespace, editable in-place, reset on file load (read-only)

"""

render_icon_size: typing.Any = ...

"""

Reference size for icon/preview renders (read-only)

"""

render_preview_size: typing.Any = ...

"""

Reference size for icon/preview renders (read-only)

"""

tempdir: typing.Any = ...

"""

String, the temp directory used by blender (read-only)

"""

use_event_simulate: typing.Any = ...

"""

Boolean, for application behavior (started with --enable-* matching this attribute name)

"""

use_userpref_skip_save_on_exit: typing.Any = ...

"""

Boolean, for application behavior (started with --enable-* matching this attribute name)

"""

background: typing.Any = ...

"""

Boolean, True when blender is running without a user interface (started with -b)

"""

factory_startup: typing.Any = ...

"""

Boolean, True when blender is running with --factory-startup)

"""

build_branch: typing.Any = ...

"""

The branch this blender instance was built from

"""

build_cflags: typing.Any = ...

"""

C compiler flags

"""

build_commit_date: typing.Any = ...

"""

The date of commit this blender instance was built

"""

build_commit_time: typing.Any = ...

"""

The time of commit this blender instance was built

"""

build_cxxflags: typing.Any = ...

"""

C++ compiler flags

"""

build_date: typing.Any = ...

"""

The date this blender instance was built

"""

build_hash: typing.Any = ...

"""

The commit hash this blender instance was built with

"""

build_linkflags: typing.Any = ...

"""

Binary linking flags

"""

build_platform: typing.Any = ...

"""

The platform this blender instance was built for

"""

build_system: typing.Any = ...

"""

Build system used

"""

build_time: typing.Any = ...

"""

The time this blender instance was built

"""

build_type: typing.Any = ...

"""

The type of build (Release, Debug)

"""

build_commit_timestamp: typing.Any = ...

"""

The unix timestamp of commit this blender instance was built

"""

binary_path: typing.Any = ...

"""

The location of Blender's executable, useful for utilities that open new instances

"""

version_char: typing.Any = ...

"""

Deprecated, always an empty string

"""

version_cycle: typing.Any = ...

"""

The release status of this build alpha/beta/rc/release

"""

version_string: typing.Any = ...

"""

The Blender version formatted as a string

"""

version: typing.Any = ...

"""

The Blender version as a tuple of 3 numbers. eg. (2, 83, 1)

"""

version_file: typing.Any = ...

"""

The Blender version, as a tuple, last used to save a .blend file, compatible with ``bpy.data.version``. This value should be used for handling compatibility changes between Blender versions

"""

alembic: typing.Any = ...

"""

Constant value bpy.app.alembic(supported=True, version=(1, 7, 16), version_string=' 1,  7, 16')

"""

build_options: typing.Any = ...

"""

Constant value bpy.app.build_options(bullet=True, codec_avi=True, codec_ffmpeg=True, codec_sndfile=True, compositor=True, cycles=True, cycles_osl=True, freestyle=True, image_cineon=True, image_dds=True, image_hdr=True, image_openexr=True, image_openjpeg=True, image_tiff=True, input_ndof=True, audaspace=True, international=True, openal=True, opensubdiv=True, sdl=True, sdl_dynload=True, coreaudio=False, jack=True, pulseaudio=True, wasapi=False, libmv=True, mod_oceansim=True, mod_remesh=True, collada=True, opencolorio=True, openmp=False, openvdb=True, alembic=True, usd=True, fluid=True, xr_openxr=True, potrace=True, pugixml=True, haru=True)

"""

ffmpeg: typing.Any = ...

"""

Constant value bpy.app.ffmpeg(supported=True, avcodec_version=(58, 134, 100), avcodec_version_string='58, 134, 100', avdevice_version=(58, 13, 100), avdevice_version_string='58, 13, 100', avformat_version=(58, 76, 100), avformat_version_string='58, 76, 100', avutil_version=(56, 70, 100), avutil_version_string='56, 70, 100', swscale_version=(5, 9, 100), swscale_version_string=' 5,  9, 100')

"""

ocio: typing.Any = ...

"""

Constant value bpy.app.ocio(supported=True, version=(2, 0, 0), version_string=' 2,  0,  0')

"""

oiio: typing.Any = ...

"""

Constant value bpy.app.oiio(supported=True, version=(2, 2, 15), version_string=' 2,  2, 15')

"""

opensubdiv: typing.Any = ...

"""

Constant value bpy.app.opensubdiv(supported=True, version=(0, 0, 0), version_string=' 0,  0,  0')

"""

openvdb: typing.Any = ...

"""

Constant value bpy.app.openvdb(supported=True, version=(8, 0, 0), version_string=' 8,  0,  0')

"""

sdl: typing.Any = ...

"""

Constant value bpy.app.sdl(supported=True, version=(2, 0, 10), version_string='2.0.10', available=True)

"""

usd: typing.Any = ...

"""

Constant value bpy.app.usd(supported=True, version=(0, 21, 2), version_string=' 0, 21,  2')

"""
