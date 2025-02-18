import mathutils

from ....structurelib.base import ValueAdaptor, FixedSizeArrayUnpacker
from ....structurelib.primitives import c_float32

MatrixUnpacker = ValueAdaptor(mathutils.Matrix,
                              FixedSizeArrayUnpacker(c_float32, 16),
                              # The array is column-major, but the matrix constructor takes rows
                              # Solution - pass the columns in as rows, and then transpose
                              lambda arr: mathutils.Matrix((arr[0:4], arr[4:8], arr[8:12], arr[12:16])).transposed(),
                              # Column-major = each column concatenated
                              lambda matrix: list(matrix.col[0]) + list(matrix.col[1]) + list(matrix.col[2]) + list(
                                  matrix.col[3])
                              )
