from dataclasses import dataclass
from enum import IntEnum
from typing import List

from mathutils import Vector, Quaternion
from ....structurelib.base import StructureUnpacker, ValueAdaptor, FixedSizeArrayUnpacker
from ....structurelib.primitives import c_int32, c_uint32
from .vector import Vec4Unpacker, QuatUnpacker


class NodeStackOp(IntEnum):
    PopPush = 0
    Push = 1
    Pop = 2
    NoOp = 3


class NodeType(IntEnum):
    MatrixTransform = 0
    UnskinnedMesh = 1
    SkinnedMesh = 2


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

    world_pos: Vector
    anim_axis: Vector
    flags: List[int]


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

        ("world_pos", Vec4Unpacker),
        ("anim_axis", Vec4Unpacker),
        ("flags", FixedSizeArrayUnpacker(c_uint32, 4)),
    ]
)
