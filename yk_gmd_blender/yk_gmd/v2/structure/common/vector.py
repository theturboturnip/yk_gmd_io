import mathutils
from yk_gmd_blender.structurelib.base import FixedSizeArrayUnpacker, ValueAdaptor
from yk_gmd_blender.structurelib.primitives import c_float32, List

Vec3Unpacker = ValueAdaptor[mathutils.Vector, List[float]](mathutils.Vector,
                                                           FixedSizeArrayUnpacker(c_float32, 3),
                                                           lambda arr: mathutils.Vector((arr[0], arr[1], arr[2])),
                                                           lambda vec: [vec.x, vec.y, vec.z]
                                                           )

Vec4Unpacker = ValueAdaptor[mathutils.Vector, List[float]](mathutils.Vector,
                                                           FixedSizeArrayUnpacker(c_float32, 4),
                                                           lambda arr: mathutils.Vector((arr[0], arr[1], arr[2], arr[3])),
                                                           lambda vec: [vec.x, vec.y, vec.z, vec.w]
                                                           )

QuatUnpacker = ValueAdaptor[mathutils.Quaternion, List[float]](mathutils.Quaternion,
                                                           FixedSizeArrayUnpacker(c_float32, 4),
                                                           lambda arr: mathutils.Quaternion((arr[3], arr[0], arr[1], arr[2])),
                                                           lambda quat: [quat.x, quat.y, quat.z, quat.w]
                                                           )