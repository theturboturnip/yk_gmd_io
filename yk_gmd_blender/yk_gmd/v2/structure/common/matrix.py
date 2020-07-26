from typing import List

import mathutils

from yk_gmd_blender.structurelib.base import ValueAdaptor, FixedSizeArrayUnpacker
from yk_gmd_blender.structurelib.primitives import c_float32

MatrixUnpacker = ValueAdaptor(mathutils.Matrix,
                              FixedSizeArrayUnpacker(c_float32, 16),
                              # The array is column-major, but the matrix constructor takes rows
                              # Solution - pass the columns in as rows, and then transpose
                              lambda arr: mathutils.Matrix((arr[0:3], arr[4:7], arr[8:11], arr[12:15])).transposed(),
                              # Column-major = each column concatenated
                              lambda matrix: matrix.col[0] + matrix.col[1] + matrix.col[2] + matrix.col[3]
                              )
