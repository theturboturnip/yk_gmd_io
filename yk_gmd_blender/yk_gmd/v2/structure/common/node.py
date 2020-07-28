import collections
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Dict, Deque

from mathutils import Vector, Quaternion, Matrix
from yk_gmd_blender.structurelib.base import StructureUnpacker, ValueAdaptor
from yk_gmd_blender.structurelib.primitives import c_int32
from yk_gmd_blender.yk_gmd.legacy.abstract.bone import GMDBone
from yk_gmd_blender.yk_gmd.legacy.abstract.vector import Vec3, Quat
from yk_gmd_blender.yk_gmd.v2.structure.common.checksum_str import ChecksumStrStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.vector import Vec4Unpacker, QuatUnpacker


class NodeStackOp(IntEnum):
    PopPush = 0
    Push = 1
    Pop = 2
    NoOp = 3


class NodeType(IntEnum):
    NoType = 0,
    Skin = 2


@dataclass(frozen=True)
class NodeStruct:
    index: int
    parent_of: int
    sibling_of: int
    object_index: int  # -1 if not an object
    matrix_index: int  # Still unclear, but this is probably a matrix index. Usually == index.
    stack_op: NodeStackOp
    name_index: int
    node_type: NodeType

    pos: Vector
    rot: Quaternion
    scale: Vector

    bone_pos: Vector
    bone_axis: Quaternion
    padding: Vector


NodeStruct_Unpack = StructureUnpacker(
    NodeStruct,
    fields=[
        ("index", c_int32),
        ("parent_of", c_int32),
        ("sibling_of", c_int32),
        ("object_index", c_int32),
        ("matrix_index", c_int32),
        ("stack_op", ValueAdaptor[NodeStackOp, int](NodeStackOp,
                                                    c_int32,
                                                    NodeStackOp,
                                                    lambda stack_op: stack_op.value
                                                    )),
        ("name_index", c_int32),
        ("node_type", ValueAdaptor[NodeType, int](NodeType,
                                                  c_int32,
                                                  NodeType,
                                                  lambda node_type: node_type.value
                                                  )),

        ("pos", Vec4Unpacker),
        ("rot", QuatUnpacker),
        ("scale", Vec4Unpacker),

        ("bone_pos", Vec4Unpacker),
        ("bone_axis", QuatUnpacker),
        ("padding", Vec4Unpacker),
    ]
)
