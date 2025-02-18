import mathutils

from ....structurelib.base import FixedSizeArrayUnpacker, ValueAdaptor, BaseUnpacker
from ....structurelib.primitives import c_float32, List


def Vec3Unpacker_of(float_type: BaseUnpacker[float]):
    return ValueAdaptor[mathutils.Vector, List[float]](mathutils.Vector,
                                                       FixedSizeArrayUnpacker(float_type, 3),
                                                       lambda arr: mathutils.Vector((arr[0], arr[1], arr[2])),
                                                       lambda vec: [vec[0], vec[1], vec[2]]
                                                       )


Vec3Unpacker = Vec3Unpacker_of(c_float32)


def Vec4Unpacker_of(float_type: BaseUnpacker[float]):
    return ValueAdaptor[mathutils.Vector, List[float]](mathutils.Vector,
                                                       FixedSizeArrayUnpacker(float_type, 4),
                                                       lambda arr: mathutils.Vector(
                                                           (arr[0], arr[1], arr[2], arr[3])),
                                                       lambda vec: [vec[0], vec[1], vec[2], vec[3]]
                                                       )


Vec4Unpacker = Vec4Unpacker_of(c_float32)

QuatUnpacker = ValueAdaptor[mathutils.Quaternion, List[float]](mathutils.Quaternion,
                                                               FixedSizeArrayUnpacker(c_float32, 4),
                                                               lambda arr: mathutils.Quaternion(
                                                                   (arr[3], arr[0], arr[1], arr[2])),
                                                               lambda quat: [quat.x, quat.y, quat.z, quat.w]
                                                               )
