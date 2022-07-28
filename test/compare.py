import argparse
import itertools
from pathlib import Path
from typing import List, Callable, TypeVar, Tuple, cast, Iterable, Any

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


def compare_same_layout_meshes(src: List[GMDMesh], dst: List[GMDMesh], error: ErrorReporter, context: str) -> bool:
    src_vertices = set()
    dst_vertices = set()

    nul_item = (0,)

    for gmd_mesh in src:
        buf = gmd_mesh.vertices_data
        verts: List[Tuple[Any,...]] = [nul_item] * len(buf)
        for i in range(len(buf)):
            verts[i] = (
                tuple(round(x, 1) for x in buf.pos[i]),
                tuple(round(x, 1) for x in buf.normal[i]) if buf.normal else nul_item,
                tuple(round(x, 1) for x in buf.tangent[i]) if buf.tangent else nul_item,
                tuple(round(x, 1) for x in buf.col0[i]) if buf.col0 else nul_item,
                tuple(round(x, 1) for x in buf.col1[i]) if buf.col1 else nul_item,
                tuple(round(x, 1) for x in buf.bone_data[i]) if buf.bone_data else nul_item,
                tuple(round(x, 1) for x in buf.weight_data[i]) if buf.weight_data else nul_item,
                tuple(round(x, 1) for x in buf.unk[i]) if buf.unk else nul_item,
                tuple(round(x, 2) for uv in buf.uvs for x in uv[i]),
            )
        src_vertices.update(verts)

    for gmd_mesh in dst:
        buf = gmd_mesh.vertices_data
        verts = [nul_item] * len(buf)
        for i in range(len(buf)):
            verts[i] = (
                tuple(round(x, 1) for x in buf.pos[i]),
                tuple(round(x, 1) for x in buf.normal[i]) if buf.normal else nul_item,
                tuple(round(x, 1) for x in buf.tangent[i]) if buf.tangent else nul_item,
                tuple(round(x, 1) for x in buf.col0[i]) if buf.col0 else nul_item,
                tuple(round(x, 1) for x in buf.col1[i]) if buf.col1 else nul_item,
                tuple(round(x, 1) for x in buf.bone_data[i]) if buf.bone_data else nul_item,
                tuple(round(x, 1) for x in buf.weight_data[i]) if buf.weight_data else nul_item,
                tuple(round(x, 1) for x in buf.unk[i]) if buf.unk else nul_item,
                tuple(round(x, 2) for uv in buf.uvs for x in uv[i]),
            )
        dst_vertices.update(verts)

    src_but_not_dst = src_vertices.difference(dst_vertices)
    dst_but_not_src = dst_vertices.difference(src_vertices)

    if src_but_not_dst or dst_but_not_src:
        src_but_not_dst_str = '\n\t'.join(str(x) for x in itertools.islice(sorted(src_but_not_dst), 5))
        dst_but_not_src_str = '\n\t'.join(str(x) for x in itertools.islice(sorted(dst_but_not_src), 5))
        error.recoverable(f"src ({len(src_vertices)} unique verts) and dst ({len(dst_vertices)} unique verts) differ\nt"
                          f"{context} src meshes have {len(src_but_not_dst)} vertices missing in dst:\n\t"
                          f"{src_but_not_dst_str}...\n\t"
                          f"{context} dst meshes have {len(dst_but_not_src)} vertices not in src:\n\t"
                          f"{dst_but_not_src_str}...")
        return False
    return True


def compare_single_node_pair(vertices: bool, src: GMDNode, dst: GMDNode, error: ErrorReporter, context: str):
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

            # Generate sorted attribute set lists to compare them
            # If there are different materials, there's a problem
            sorted_attrs_src, sorted_attrs_dst = sort_src_dest_lists(
                src_attrs,
                dst_attrs,
                key=lambda x: x
            )

            if sorted_attrs_src != sorted_attrs_dst:
                error.recoverable(
                    f"{context} has different sets of attribute sets:\nsrc:\n\t{sorted_attrs_src}\ndst:{sorted_attrs_dst}\n\t")

            if vertices:
                # For each unique attribute set
                # compare the vertices in the sets of meshes that use it
                unique_attr_sets = []
                for m in src.mesh_list:
                    if m.attribute_set not in unique_attr_sets:
                        unique_attr_sets.append(m.attribute_set)
                if all(
                    compare_same_layout_meshes(
                        [m for m in src.mesh_list if m.attribute_set == attr],
                        [m for m in dst.mesh_list if m.attribute_set == attr],
                        error, f"{context}attr set {attr.texture_diffuse}"
                    )
                    for attr in unique_attr_sets
                ):
                    error.info(f"{context} meshes are functionally identical")


def recursive_compare_node_lists(vertices: bool, src: List[GMDNode], dst: List[GMDNode], error: ErrorReporter, context: str):
    src_names_unordered = set(n.name for n in src)
    dst_names_unordered = set(n.name for n in dst)
    if src_names_unordered != dst_names_unordered:
        error.fatal(f"{context} has different sets of children:\nsrc:\n\t{src_names_unordered}\ndst:{dst_names_unordered}\n\t")

    src_names = [n.name for n in src]
    dst_names = [n.name for n in dst]
    if src_names != dst_names:
        error.fatal(f"{context} children in different order:\nsrc:\n\t{src_names}\ndst:{dst_names}\n\t")

    for child_src, child_dst in zip(src, dst):
        child_context = f"{context}{child_src.name} > "
        compare_single_node_pair(vertices, child_src, child_dst, error, child_context)
        recursive_compare_node_lists(vertices, child_src.children, child_dst.children, error, child_context)


def compare_files(file_src: Path, file_dst: Path, skinned: bool, vertices: bool):
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
    import_mode = VertexImportMode.IMPORT_VERTICES if vertices else VertexImportMode.NO_VERTICES

    scene_src = read_abstract_scene_from_filedata_object(version_props_src,
                                                         FileImportMode.SKINNED if skinned else FileImportMode.UNSKINNED,
                                                         import_mode,
                                                         file_data_src, error)
    scene_dst = read_abstract_scene_from_filedata_object(version_props_dst,
                                                         FileImportMode.SKINNED if skinned else FileImportMode.UNSKINNED,
                                                         import_mode,
                                                         file_data_dst, error)

    recursive_compare_node_lists(vertices, scene_src.overall_hierarchy.roots, scene_dst.overall_hierarchy.roots, error, "")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("GMD Comparer")

    parser.add_argument("file_src", type=Path)
    parser.add_argument("file_dst", type=Path)
    parser.add_argument("--skinned", action="store_true")
    parser.add_argument("--vertices", action="store_true")

    args = parser.parse_args()

    compare_files(args.file_src, args.file_dst, args.skinned, args.vertices)
