import argparse
from pathlib import Path
from typing import List, Callable, TypeVar, Tuple, cast, Iterable

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_bone import GMDBone
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_node import GMDNode
from yk_gmd_blender.yk_gmd.v2.abstract.nodes.gmd_object import GMDSkinnedObject, GMDUnskinnedObject
from yk_gmd_blender.yk_gmd.v2.converters.common.to_abstract import FileImportMode, VertexImportMode
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import LenientErrorReporter, ErrorReporter
from yk_gmd_blender.yk_gmd.v2.io import read_gmd_structures, read_abstract_scene_from_filedata_object
from yk_gmd_blender.yk_gmd.v2.structure.common.node import NodeType

T = TypeVar('T')


def sort_src_dest_lists(src: Iterable[T], dst: Iterable[T], key: Callable[[T], str]) -> Tuple[List[T], List[T]]:
    sorted_src: List[T] = [n for n in src]
    sorted_src.sort(key=key)
    sorted_dst: List[T] = [n for n in dst]
    sorted_dst.sort(key=key)

    return sorted_src, sorted_dst


def compare_single_node_pair(src: GMDNode, dst: GMDNode, error: ErrorReporter, context: str):
    def compare_field(f: str):
        if getattr(src, f) != getattr(dst, f):
            error.recoverable(f"{context}: field {f} differs:\nsrc:\n\t{getattr(src, f)}\ndst:\n\t{getattr(dst, f)}")

    # Compare subclass-agnostic, hierarchy-agnostic values
    compare_field("node_type")
    compare_field("pos")
    compare_field("rot")
    compare_field("scale")
    compare_field("world_pos")
    compare_field("anim_axis")
    compare_field("flags")
    compare_field("matrix")

    if src.node_type == dst.node_type:
        if src.node_type == NodeType.MatrixTransform:
            assert isinstance(src, GMDBone)
            pass  # Nothing more to check
        else:
            # Compare meshes
            assert isinstance(src, (GMDSkinnedObject, GMDUnskinnedObject))
            assert isinstance(dst, (GMDSkinnedObject, GMDUnskinnedObject))

            src_attrs = set(str(m.attribute_set) for m in cast(List[GMDMesh], src.mesh_list))
            dst_attrs = set(str(m.attribute_set) for m in cast(List[GMDMesh], dst.mesh_list))

            # Generate sorted attribute set lists
            # We can't compare meshes directly, because a re-exported mesh may have been split differently
            sorted_attrs_src, sorted_attrs_dst = sort_src_dest_lists(
                src_attrs,
                dst_attrs,
                key=str
            )

            if sorted_attrs_src != sorted_attrs_dst:
                error.recoverable(
                    f"{context} has different sets of attribute sets:\nsrc:\n\t{sorted_attrs_src}\ndst:{sorted_attrs_dst}\n\t")


def recursive_compare_node_lists(src: List[GMDNode], dst: List[GMDNode], error: ErrorReporter, context: str):
    sorted_src, sorted_dst = sort_src_dest_lists(src, dst, key=lambda n: n.name)

    src_names = [n.name for n in sorted_src]
    dst_names = [n.name for n in sorted_dst]

    if src_names != dst_names:
        error.fatal(f"{context} has different sets of children:\nsrc:\n\t{src_names}\ndst:{dst_names}\n\t")

    for child_src, child_dst in zip(sorted_src, sorted_dst):
        child_context = f"{context}{child_src.name} > "
        compare_single_node_pair(child_src, child_dst, error, child_context)
        recursive_compare_node_lists(child_src.children, child_dst.children, error, child_context)


def compare_files(file_src: Path, file_dst: Path, skinned: bool):
    error = LenientErrorReporter(allowed_categories=set())

    # Load and compare basic information - GMD version, headers
    version_props_src, header_src, file_data_src = read_gmd_structures(file_src, error)
    version_props_dst, header_dst, file_data_dst = read_gmd_structures(file_dst, error)

    if version_props_src != version_props_dst:
        error.fatal(f"Version props mismatch\nsrc:\n\t{version_props_src}\ndst:\n\t{version_props_dst}")

    def compare_header_field(f: str):
        if getattr(header_src, f) != getattr(header_dst, f):
            error.recoverable(f"header: field {f} differs:\nsrc:\n\t{getattr(header_src, f)}\ndst:\n\t{getattr(header_dst, f)}")

    compare_header_field("magic")
    compare_header_field("vertex_endian_check")
    compare_header_field("file_endian_check")
    compare_header_field("version_combined")
    compare_header_field("name")
    compare_header_field("padding")

    # Technically YK1-specific?
    compare_header_field("overall_bounds")
    compare_header_field("flags")

    # Load and compare scene hierarchies
    scene_src = read_abstract_scene_from_filedata_object(version_props_src,
                                                         FileImportMode.SKINNED if skinned else FileImportMode.UNSKINNED,
                                                         VertexImportMode.NO_VERTICES,
                                                         file_data_src, error)
    scene_dst = read_abstract_scene_from_filedata_object(version_props_dst,
                                                         FileImportMode.SKINNED if skinned else FileImportMode.UNSKINNED,
                                                         VertexImportMode.NO_VERTICES,
                                                         file_data_dst, error)

    recursive_compare_node_lists(scene_src.overall_hierarchy.roots, scene_dst.overall_hierarchy.roots, error, "")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("GMD Comparer")

    parser.add_argument("file_src", type=Path)
    parser.add_argument("file_dst", type=Path)
    parser.add_argument("--skinned", action="store_true")

    args = parser.parse_args()

    compare_files(args.file_src, args.file_dst, args.skinned)
