import argparse
import itertools
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List, Callable, TypeVar, Tuple, cast, Iterable, Set, DefaultDict, Optional, Dict

from mathutils import Vector
from yk_gmd.v2.structure.endianness import check_are_vertices_big_endian, check_is_file_big_endian
from yk_gmd_blender.yk_gmd.v2.abstract.gmd_mesh import GMDMesh, GMDSkinnedMesh
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


@dataclass(frozen=True)
class VertApproxData:
    normal: Optional[Tuple]
    tangent: Optional[Tuple]

    @staticmethod
    def new(normal: Optional[Vector], tangent: Optional[Vector]):
        return VertApproxData(
            normal=tuple(round(x, 2) for x in normal.resized(4)) if normal is not None else None,
            tangent=tuple(round(x, 2) for x in tangent.resized(4)) if tangent is not None else None
        )

    def approx_eq(self, other: 'VertApproxData') -> bool:
        t = 0.9  # equality threshold
        if self.normal is None:
            if other.normal is not None:
                return False
        else:
            if other.normal is None or Vector(self.normal).dot(Vector(other.normal)) < t:
                return False

        # if self.tangent is None:
        #     if other.tangent is not None:
        #         return False
        # else:
        #     if other.tangent is None or Vector(self.tangent).dot(Vector(other.tangent)) < t:
        #         return False

        return True

    def __lt__(self, other) -> bool:
        return (self.normal, self.tangent) < (other.normal, other.tangent)

    def __gt__(self, other) -> bool:
        return (self.normal, self.tangent) > (other.normal, other.tangent)


class VertSet:
    """
    Class for storing sets of vertex data, split into "exact" and "approximate" data.
    When computing the difference of two sets, first compares exact parts then
    sees if the approximate parts are close enough.
    """
    verts: DefaultDict[Tuple, Set[VertApproxData]]
    len: int

    def __init__(self):
        self.verts = defaultdict(lambda: set())
        self.len = 0

    def add(self, vert_exact: Tuple, vert_approx: VertApproxData):
        self.verts[vert_exact].add(vert_approx)
        self.len += 1

    def exact_difference(self, other: 'VertSet') -> Set[Tuple]:
        """
        Returns the difference in exact data of two vert-sets as a set
        (i.e. all exact data elements that are in this set but not the others)

        :param other: The other set
        :return: Set of vert_exact tuples not found in the other set
        """
        return set(self.verts.keys()).difference(other.verts.keys())

    def difference(self, other: 'VertSet') -> Dict[Tuple, Tuple[VertApproxData]]:
        """
        Return the difference of two vert-sets as a set.
        (i.e. all elements that are in this set but not the others.)

        Returns a set of tuples: (vert_exact, vert_approx) not found in the other set,
        i.e. for which there does not exist a vert_approx_alt in other.verts[vert_exact]
        where vert_approx.approx_eq(vert_approx_alt)

        :param other: The other set
        :return: Set of (vert_exact, vert_approx) tuples not found in the other set
        """

        verts: Dict[Tuple, Tuple[VertApproxData]] = {}

        key_set = set(self.verts.keys())

        # 1. Find vert_exacts that don't match
        for vert_exact in key_set.difference(other.verts.keys()):
            # foreach vert_exact that doesn't exist in the other verts
            # add all (vert_exact, vert_approx) pairs to the set
            verts[vert_exact] = tuple(v_a for v_a in self.verts[vert_exact])

        # 2. Find vert_approx that don't match within vert_exacts that do match
        for vert_exact in key_set.intersection(other.verts.keys()):
            # foreach vert_exact that is in both sets
            # check the vert_approx lists
            self_approx = self.verts[vert_exact]
            other_approx = other.verts[vert_exact]
            # O(n^2), but there shouldn't be many items in either list
            differing_va = tuple(
                v_a
                for v_a in self_approx
                if not any(v_a.approx_eq(v_a_alt) for v_a_alt in other_approx)
            )
            if len(differing_va) > 0:
                verts[vert_exact] = differing_va

        return verts

    def __len__(self):
        return self.len


def get_unique_verts(ms: List[GMDMesh]) -> VertSet:
    nul_item = (0,)
    all_verts = VertSet()
    for gmd_mesh in ms:
        buf = gmd_mesh.vertices_data
        for i in set(gmd_mesh.triangle_strip_noreset_indices):
            all_verts.add(
                (
                    tuple(round(x, 2) for x in buf.pos[i]),
                    tuple(round(x, 2) for x in buf.col0[i]) if buf.col0 else nul_item,
                    tuple(round(x, 2) for x in buf.col1[i]) if buf.col1 else nul_item,
                    tuple(round(x, 2) for x in buf.unk[i]) if buf.unk else nul_item,
                    tuple(round(x, 2) for uv in buf.uvs for x in uv[i]),
                    "b",
                    tuple(round(x, 1) for x in buf.bone_data[i]) if buf.bone_data else nul_item,
                    "w",
                    tuple(round(x, 2) for x in buf.weight_data[i]) if buf.weight_data else nul_item,
                ),
                VertApproxData.new(
                    normal=buf.normal[i] if buf.normal else None,
                    tangent=buf.tangent[i] if buf.tangent else None
                )
            )
    return all_verts


def get_unique_skinned_verts(ms: List[GMDSkinnedMesh]) -> VertSet:
    nul_item = (0,)
    all_verts = VertSet()
    for gmd_mesh in ms:
        buf = gmd_mesh.vertices_data
        for i in set(gmd_mesh.triangle_strip_noreset_indices):
            assert buf.bone_data and buf.weight_data
            all_verts.add(
                (
                    tuple(round(x, 2) for x in buf.pos[i]),
                    tuple(round(x, 2) for x in buf.col0[i]) if buf.col0 else nul_item,
                    tuple(round(x, 2) for x in buf.col1[i]) if buf.col1 else nul_item,
                    tuple(round(x, 2) for x in buf.unk[i]) if buf.unk else nul_item,
                    tuple(round(x, 2) for uv in buf.uvs for x in uv[i]),
                    "bw",
                    tuple(
                        (gmd_mesh.relevant_bones[int(b)].name, round(w, 3))
                        for (b, w) in zip(buf.bone_data[i], buf.weight_data[i])
                        if w > 0
                    ) if buf.bone_data and buf.weight_data else nul_item,
                ),
                VertApproxData.new(
                    normal=buf.normal[i] if buf.normal else None,
                    tangent=buf.tangent[i] if buf.tangent else None
                )
            )
    return all_verts


def compare_same_layout_meshes(skinned: bool, src: List[GMDMesh], dst: List[GMDMesh], error: ErrorReporter,
                               context: str) -> bool:
    if skinned:
        src_vertices = get_unique_skinned_verts(src)
        dst_vertices = get_unique_skinned_verts(dst)
    else:
        src_vertices = get_unique_verts(src)
        dst_vertices = get_unique_verts(dst)

    src_but_not_dst_exact = src_vertices.exact_difference(dst_vertices)
    dst_but_not_src_exact = dst_vertices.exact_difference(src_vertices)

    if src_but_not_dst_exact or dst_but_not_src_exact:
        src_but_not_dst_str = '\n\t'.join(str(x) for x in itertools.islice(sorted(src_but_not_dst_exact), 5))
        dst_but_not_src_str = '\n\t'.join(str(x) for x in itertools.islice(sorted(dst_but_not_src_exact), 5))
        error.fatal(
            f"{context}src ({len(src_vertices)} unique verts) and dst ({len(dst_vertices)} unique verts) exact data differs\n\t"
            f"src meshes have {len(src_but_not_dst_exact)} vertices missing in dst:\n\t"
            f"{src_but_not_dst_str}...\n\t"
            f"dst meshes have {len(dst_but_not_src_exact)} vertices not in src:\n\t"
            f"{dst_but_not_src_str}...")
        return False

    src_but_not_dst = src_vertices.difference(dst_vertices)
    dst_but_not_src = dst_vertices.difference(src_vertices)

    if src_but_not_dst or dst_but_not_src:
        src_but_not_dst_str = '\n\t'.join(
            f"{str(k)}:\n\t\t" + '\n\t\t'.join(str(x) for x in src_but_not_dst[k])
            for k in itertools.islice(sorted(src_but_not_dst.keys()), 5)
        )
        dst_but_not_src_str = '\n\t'.join(
            f"{str(k)}:\n\t\t" + '\n\t\t'.join(str(x) for x in dst_but_not_src[k])
            for k in itertools.islice(sorted(dst_but_not_src.keys()), 5)
        )
        error.recoverable(
            f"{context}src ({len(src_vertices)} unique verts) and dst ({len(dst_vertices)} unique verts) APPROX data differs\n\t"
            f"src meshes have {len(src_but_not_dst)} vertices missing in dst:\n\t"
            f"{src_but_not_dst_str}...\n\t"
            f"dst meshes have {len(dst_but_not_src)} vertices not in src:\n\t"
            f"{dst_but_not_src_str}...")
        return False
    return True


def compare_single_node_pair(skinned: bool, vertices: bool, src: GMDNode, dst: GMDNode, error: ErrorReporter,
                             context: str):
    from math import fabs

    def compare_field(f: str):
        if getattr(src, f) != getattr(dst, f):
            error.fatal(f"{context}: field '{f}' differs:\nsrc:\n\t{getattr(src, f)}\ndst:\n\t{getattr(dst, f)}")

    def compare_vec_field(f: str):
        src_f = tuple(round(x, 3) for x in getattr(src, f))
        dst_f = tuple(round(x, 3) for x in getattr(dst, f))
        if src_f != dst_f:
            if sum(fabs(s - r) for (s, r) in zip(src_f, dst_f)) > 0.05:
                error.fatal(f"{context}: vector '{f}'' differs:\nsrc:\n\t{src_f}\ndst:\n\t{dst_f}")
            else:
                error.recoverable(f"{context}: vector '{f}' differs slightly:\nsrc:\n\t{src_f}\ndst:\n\t{dst_f}")

    def compare_mat_field(f: str):
        src_f = tuple(tuple(round(x, 3) for x in v) for v in getattr(src, f))
        dst_f = tuple(tuple(round(x, 3) for x in v) for v in getattr(dst, f))
        if src_f != dst_f:
            src_floats = tuple(x for v in src_f for x in v)
            dst_floats = tuple(x for v in dst_f for x in v)
            if sum(fabs(s - r) for (s, r) in zip(src_floats, dst_floats)) > 0.05:
                error.fatal(f"{context}: matrix '{f}' differs:\nsrc:\n\t{src_f}\ndst:\n\t{dst_f}")
            else:
                error.recoverable(f"{context}: matrix '{f}' differs slightly:\nsrc:\n\t{src_f}\ndst:\n\t{dst_f}")

    # Compare subclass-agnostic, hierarchy-agnostic values
    compare_field("node_type")
    compare_vec_field("pos")
    compare_vec_field("rot")
    compare_vec_field("scale")
    compare_vec_field("world_pos")
    compare_vec_field("anim_axis")
    compare_field("flags")

    if not isinstance(src, GMDSkinnedObject):
        compare_mat_field("matrix")

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
                error.fatal(
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
                            skinned,
                            [m for m in src.mesh_list if m.attribute_set == attr],
                            [m for m in dst.mesh_list if m.attribute_set == attr],
                            error, f"{context}attr set {attr.texture_diffuse} "
                        )
                        for attr in unique_attr_sets
                ):
                    error.info(f"{context} meshes are functionally identical")


def recursive_compare_node_lists(skinned: bool, vertices: bool, src: List[GMDNode], dst: List[GMDNode],
                                 error: ErrorReporter, context: str):
    src_names_unordered = set(n.name for n in src)
    dst_names_unordered = set(n.name for n in dst)
    if src_names_unordered != dst_names_unordered:
        error.fatal(
            f"{context} has different sets of children:\nsrc:\n\t{src_names_unordered}\ndst:{dst_names_unordered}\n\t")

    src_names = [n.name for n in src]
    dst_names = [n.name for n in dst]
    if src_names != dst_names:
        error.fatal(f"{context} children in different order:\nsrc:\n\t{src_names}\ndst:{dst_names}\n\t")

    for child_src, child_dst in zip(src, dst):
        child_context = f"{context}{child_src.name} > "
        compare_single_node_pair(skinned, vertices, child_src, child_dst, error, child_context)
        recursive_compare_node_lists(skinned, vertices, child_src.children, child_dst.children, error, child_context)


def compare_files(file_src: Path, file_dst: Path, skinned: bool, vertices: bool, error: ErrorReporter):
    # Load and compare basic information - GMD version, headers
    version_props_src, header_src, file_data_src = read_gmd_structures(file_src, error)
    version_props_dst, header_dst, file_data_dst = read_gmd_structures(file_dst, error)

    if version_props_src != version_props_dst:
        error.fatal(f"Version props mismatch\nsrc:\n\t{version_props_src}\ndst:\n\t{version_props_dst}")

    def compare_header_field(f: str):
        if getattr(header_src, f) != getattr(header_dst, f):
            error.recoverable(
                f"header: field {f} differs:\nsrc:\n\t{getattr(header_src, f)}\ndst:\n\t{getattr(header_dst, f)}")

    compare_header_field("magic")
    # Compare endianness
    if check_are_vertices_big_endian(header_src.vertex_endian_check) != \
            check_are_vertices_big_endian(header_dst.vertex_endian_check):
        error.recoverable(
            f"header: vertex endian differs:\nsrc:\n\t"
            f"{header_src.vertex_endian_check} {check_are_vertices_big_endian(header_src.vertex_endian_check)}\n"
            f"dst:\n\t{header_dst.vertex_endian_check} {check_are_vertices_big_endian(header_dst.vertex_endian_check)}")
    if check_is_file_big_endian(header_src.file_endian_check) != \
            check_is_file_big_endian(header_dst.file_endian_check):
        error.recoverable(
            f"header: file endian differs:\nsrc:\n\t"
            f"{header_src.file_endian_check} {check_is_file_big_endian(header_src.file_endian_check)}\n"
            f"dst:\n\t{header_dst.file_endian_check} {check_is_file_big_endian(header_dst.file_endian_check)}")
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

    recursive_compare_node_lists(skinned, vertices, scene_src.overall_hierarchy.roots,
                                 scene_dst.overall_hierarchy.roots, error, "")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("GMD Comparer")

    parser.add_argument("file_src", type=Path)
    parser.add_argument("file_dst", type=Path)
    parser.add_argument("--skinned", action="store_true")
    parser.add_argument("--vertices", action="store_true")

    args = parser.parse_args()

    error = LenientErrorReporter(allowed_categories=set())

    compare_files(args.file_src, args.file_dst, args.skinned, args.vertices, error)
