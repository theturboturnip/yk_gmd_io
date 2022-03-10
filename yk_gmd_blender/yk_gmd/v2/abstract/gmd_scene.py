from dataclasses import dataclass
from typing import Dict, List, Generic, TypeVar, Generator

from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode

TNode = TypeVar('TNode', bound=GMDNode)

def depth_first_iterate(roots: List[TNode]) -> Generator[TNode, None, None]:
    queue = []
    # Insert roots in reverse order, so we yield the first root first
    for root in roots[::-1]:
        queue.append(root)

    while queue:
        next = queue.pop()
        yield next
        for child in next.children[::-1]:
            queue.append(child)


class HierarchyData(Generic[TNode]):
    roots: List[TNode]
    # TODO: This doesn't work! Do one just for bones, those are guaranteed(?) to not have duplicates
    elem_from_name: Dict[str, TNode]

    def __init__(self, roots: List[TNode]):
        self.roots = roots[:]
        self.elem_from_name = {
            node.name:node
            for node in depth_first_iterate(self.roots)
        }

    def depth_first_iterate(self) -> Generator[TNode, None, None]:
        return depth_first_iterate(self.roots)

    @property
    def total_elems(self):
        return len(self.elem_from_name.values())


@dataclass(repr=False)
class GMDScene:
    name: str

    # Node Hierarchy stuff
    overall_hierarchy: HierarchyData[GMDNode]

    # bones: Optional[HierarchyData[GMDBone]]
    # skinned_objects: Optional[HierarchyData[GMDSkinnedObject]]
    # unskinned_objects: Optional[HierarchyData[GMDUnskinnedObject]]

    # def __post_init__(self):
    #     if self.skinned_objects and self.skinned_objects.total_elems != len(self.skinned_objects.roots):
    #         raise Exception("Skinned objects are expected to all be at the root of the heirarchy")