import os

import bpy

YKGMDIO_TEST_ADDON = os.environ["YKGMDIO_TEST_ADDON"].replace("\\", "/")

bpy.ops.preferences.addon_install(filepath=YKGMDIO_TEST_ADDON)
