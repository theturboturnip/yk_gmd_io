from dataclasses import dataclass
from typing import Dict, List, Generator, Tuple, TypeVar, Iterable, Iterator

from .nodes.gmd_node import GMDNode

T = TypeVar('T')


def typed_enumerate(iterable: Iterable[T], start=0) -> Generator[Tuple[int, T], None, None]:
    """
    enumerate() with proper type hints
    """
    n = start
    for elem in iterable:
        yield n, elem
        n += 1


def depth_first_iterate(roots: List[GMDNode]) -> Generator[Tuple[int, GMDNode], None, None]:
    """
    Iterate through all (sibling index, node) pairs in `roots` depth-first,
    such that when `node` is encountered `node.parent` has also been encountered.
    """
    # Build a stack of people to visit
    # Put the first root at the top of the stack i.e. reverse the list, so we do it first
    stack = list(typed_enumerate(roots))[::-1]
    # While there are elements on the stack...
    while stack:
        # Pop the top off and yield it
        next = stack.pop()
        yield next

        # Add that node's children to the top of the stack
        # Again, use reverse order
        _, next_node = next
        stack += list(typed_enumerate(next_node.children))[::-1]


class HierarchyData:
    roots: List[GMDNode]
    # TODO: This doesn't work! Do one just for bones, those are guaranteed(?) to not have duplicates
    elem_from_name: Dict[str, GMDNode]

    def __init__(self, roots: List[GMDNode]):
        self.roots = roots[:]
        self.elem_from_name = {
            node.name: node
            for _, node in depth_first_iterate(self.roots)
        }

    def depth_first_iterate(self) -> Generator[Tuple[int, GMDNode], None, None]:
        return depth_first_iterate(self.roots)

    def __iter__(self) -> Iterator[GMDNode]:
        return (node for _, node in self.depth_first_iterate())

    @property
    def total_elems(self):
        return len(self.elem_from_name.values())


@dataclass(repr=False)
class GMDScene:
    name: str
    flags: Tuple[int, int, int, int, int, int]
    overall_hierarchy: HierarchyData
