import argparse
import math
from pathlib import Path

from yk_gmd_blender.yk_gmd.v2.io import read_gmd_structures, read_abstract_scene_from_contents
from yk_gmd_blender.yk_gmd.v2.structure.common.attribute import AttributeStruct
from yk_gmd_blender.yk_gmd.v2.structure.common.header import GMDHeaderStruct_Unpack
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.legacy_abstractor import convert_Kenzan_to_legacy_abstraction
from yk_gmd_blender.yk_gmd.v2.structure.kenzan.file import FilePacker_Kenzan
from yk_gmd_blender.yk_gmd.v2.structure.version import GMDVersion, get_version_properties
from yk_gmd_blender.yk_gmd.v2.structure.yk1.abstractor import pack_abstract_contents_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.legacy_abstractor import convert_YK1_to_legacy_abstraction, \
    package_legacy_abstraction_to_YK1
from yk_gmd_blender.yk_gmd.v2.structure.yk1.file import FilePacker_YK1
from yk_gmd_blender.yk_gmd.legacy.abstract.vector import Quat
from yk_gmd_blender.yk_gmd.legacy.file import GMDFile, GMDFileIOAbstraction


from yk_gmd_blender.yk_gmd.v2.legacy_io import *

def quaternion_to_euler_angle(q: Quat):
    ysqr = q.y * q.y

    t0 = +2.0 * (q.w * q.x + q.y * q.z)
    t1 = +1.0 - 2.0 * (q.x * q.x + ysqr)
    X = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (q.w * q.y - q.z * q.x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))

    t3 = +2.0 * (q.w * q.z + q.x * q.y)
    t4 = +1.0 - 2.0 * (ysqr + q.z * q.z)
    Z = math.degrees(math.atan2(t3, t4))

    return X, Y, Z

def csv_str(iter):
    return ", ".join(str(x) for x in iter)

def print_each(iter):
    for x in iter:
        print(x)


def old_main(args):

    #if os.path.isdir(args.output_dir):
    #    shutil.rmtree(args.output_dir)
    #shutil.copytree(args.input_dir, args.output_dir)

    with open(args.input_dir / args.file_to_poke, "rb") as in_file:
        data = in_file.read()
    original_gmd_file = GMDFile(data)

    gmd_file = GMDFileIOAbstraction(GMDFile(data).structs)

    #mat_floats_val = 10000.0
    #for material in gmd_file.structs.materials:
    #    material.texture_diffuse = PaddedTextureIndexStruct(16)
    #    material.floats[0:16] = [mat_floats_val] * 16
    #    pass

    #for unk in gmd_file.structs.unk12:
    #    unk.data_hidden[0:32] = [mat_floats_val] * 32

    # for submesh in gmd_file.submeshes:
    #     #submesh.linked_l0_number_maybe = 0
    #     #submesh.linked_l0_bone_maybe = 0
    #     #submesh.unk1 = 0
    #     #submesh.unk2 = 216
    #     #print(f"submesh unk2 = {submesh.unk2}, points to byte {gmd_file.structs.unk11[submesh.unk2].data}")
    #     #gmd_file.structs.unk11[submesh.unk2].data = 0
    #     #submesh.unk1 = 0
    #
    #     #submesh.unk1 = 121
    #     #submesh.unk2 = 0
    #     if len(submesh.vertices) == 26:
    #         mid = Vec3(0, 1.755, 0.065)
    #         print(Mat4.rotation(Quat(0, 0, 1, 0)))
    #         # s = sin(2*angle)
    #         # c = cos(2*angle)
    #         # q = (axis.x*s, axis.y*s, axis.z*s, c) for axis,angle
    #         mat = Mat4.translation(mid) * Mat4.rotation(Quat(0, 0, 1, 0)) * Mat4.translation(-mid)
    #         for v in submesh.vertices:
    #             #print(v.pos)
    #             print(v.pos)
    #             v.pos = (mat * v.pos).xyz
    #             print(f"{v.pos}\n")
    #             #v.pos.z += 0.1
    #
    #             #v.pos.z += 0.1
    #             #v.pos.y += 0.1
    #             #v.pos.x = -v.pos.x
    #             #v.normal.x = 1-v.normal.x
    #             #v.normal.y = -v.normal.y
    #             #v.normal.z = -v.normal.z
    #     pass

    new_submeshes = gmd_file.submeshes

    # Swap submeshes around
    #temp = new_submeshes[5]
    #new_submeshes[5] = new_submeshes[24]
    #new_submeshes[24] = temp
    #random.shuffle(new_submeshes)

    # for i in range(len(new_submeshes)):
    #     submesh = new_submeshes[i]
    #     new_submeshes[i] = Submesh(
    #         material=submesh.material,
    #         relevant_bones=submesh.relevant_bones,
    #         vertices=submesh.vertices,
    #         triangle_indices=submesh.triangle_indices,
    #         triangle_strip_indices1=submesh.triangle_strip_indices1,
    #         triangle_strip_indices2=submesh.triangle_strip_indices2,
    #     )

    # [:22] works, [:1] doesn't, [:15] works, [:5] doesn't, [:10] does but looks weird
    # NEW: [:5] works if different order of meshes is used?
    gmd_file.submeshes = new_submeshes[:1]
    #gmd_file.structs.parts = GMDArray(gmd_file.structs.parts.items[:10])

    #gmd_file.structs.unk11[0] = bytes(list(range(121)))

    #original_reexported_data = original_gmd_file.structs.make_bytes()
    #original_reexported_file = GMDFile(original_reexported_data)

    #l0_count = 0
    #for name in gmd_file.structs.bone_names.items:
    #    if "[l0]" in name.text:
    #        name.text_internal = f"[l0]{l0_count}".encode("ascii")
    #        l0_count += 1

    new_data = gmd_file.repack_into_bytes()
    new_gmd_file = GMDFile(new_data)

    # find diff between original_reexported and new_data
    #equal_bytes = [new_data[i] == original_reexported_data[i] for i in range(len(new_data))]
    #unequal_ranges = false_ranges_in(equal_bytes)
    #for (ra, rb) in unequal_ranges:
    #    print(f"[0x{ra:06x}...0x{rb:06x})")

    #uncovered = set()
    #for (covered, val) in zip(equal_bytes, new_data, original_reexported_data):
    #    if not covered:
    #        uncovered.add(val)
    #print(f"Values in uncovered areas: {uncovered}")

    if args.output_dir:
        with open(args.output_dir / args.file_to_poke, "wb") as out_file:
            out_file.write(new_data)

def legacy_abstract_v2_struct_main(args):
    with open(args.input_dir / args.file_to_poke, "rb") as in_file:
        data = in_file.read()

    big_endian = True
    base_header, _ = GMDHeaderStruct_Unpack.unpack(big_endian, data=data, offset=0)
    if base_header.file_endian_check == 0:
        big_endian = False
    elif base_header.file_endian_check == 1:
        big_endian = True
    else:
        raise Exception(f"Unknown base_header file endian check {base_header.file_endian_check}")

    base_header, _ = GMDHeaderStruct_Unpack.unpack(big_endian, data=data, offset=0)

    # Version check
    # version_properties = base_header.get_version_properties()
    # if version_properties.major_version == GMDVersion.Kiwami1:
    #     contents, _ = FilePacker_YK1.unpack(big_endian, data=data, offset=0)
    #
    #     #print("Trying identity transformation")
    #     scene = convert_YK1_to_legacy_abstraction(contents, version_properties)
    #     new_contents = package_legacy_abstraction_to_YK1(big_endian, contents, scene)
    #     new_data = bytearray()
    #     FilePacker_YK1.pack(big_endian, new_contents, new_data)
    #
    #     unpacked_new_data, _ = FilePacker_YK1.unpack(big_endian, data=new_data, offset=0)
    #
    #     if args.output_dir:
    #         with open(args.output_dir / args.file_to_poke, "wb") as out_file:
    #             out_file.write(new_data)
    # elif version_properties.major_version == GMDVersion.Kenzan:
    #     contents, _ = FilePacker_Kenzan.unpack(big_endian, data=data, offset=0)
    #
    #     scene = convert_Kenzan_to_legacy_abstraction(contents, version_properties)
    # else:
    #     raise Exception(f"Unknown base_header version {base_header.version_str()}")

    can_read, header = can_read_from(data)
    if can_read_from:
        contents, scene = read_to_legacy(data)

        can_write, _ = can_write_over(data)
        if can_write:
            new_attrs = []
            # for attr in cast(FileData_YK1, contents).attribute_arr:
            #     new_attrs.append(AttributeStruct(
            #         index=attr.index,
            #         material_index=attr.material_index,
            #         shader_index=attr.shader_index,
            #
            #         # Which meshes use this material - offsets in the Mesh_YK1 array
            #         meshset_start=attr.meshset_start,
            #         meshset_count=attr.meshset_count,
            #
            #         # Always one of {6,7,8} for kiwami bob
            #         # i.e. 0b0110, 0b0111, 0b1000
            #         # probably not a bitmask?
            #         unk1=0,
            #         # Always 0x00_01_00_00
            #         unk2=attr.unk2,
            #         # Observed to be 0x0000, 0x0001, 0x2001, 0x8001
            #         flags=attr.flags,
            #
            #         texture_diffuse=attr.texture_diffuse,
            #         texture_refl=attr.texture_refl,
            #         texture_multi=attr.texture_multi,
            #         # Never filled
            #         texture_unk1=attr.texture_unk1,
            #         texture_ts=attr.texture_ts,
            #         texture_normal=attr.texture_normal,
            #         texture_rt=attr.texture_rt,
            #         texture_rd=attr.texture_rd,
            #
            #         extra_properties=attr.extra_properties
            #
            #     ))
            # contents.attribute_arr = new_attrs
            new_bytes = bytearray()
            FilePacker_YK1.pack(contents.file_is_big_endian(), contents, new_bytes)
            new_bytes = bytes(new_bytes)
            #new_bytes = write_from_legacy(contents, scene)
            new_contents, new_scene = read_to_legacy(new_bytes)
            print(new_contents.attribute_arr)

            if args.output_dir:
                with open(args.output_dir / args.file_to_poke, "wb") as out_file:
                    out_file.write(new_bytes)
        else:
            print(f"Can't write to version {header.version_str()}")
    else:
        print(f"Can't read from version {header.version_str()}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("GMD Poker")

    parser.add_argument("input_dir", type=Path)
    parser.add_argument("--output_dir", type=Path)
    parser.add_argument("file_to_poke", type=Path)

    args = parser.parse_args()

    version_props, file_data = read_gmd_structures(args.input_dir / args.file_to_poke)
    scene = read_abstract_scene_from_contents(version_props, file_data)

    new_file_data = pack_abstract_contents_YK1(version_props, file_data.file_is_big_endian(), file_data.vertices_are_big_endian(), scene)
    new_file_bytearray = bytearray()
    FilePacker_YK1.pack(file_data.file_is_big_endian(), new_file_data, new_file_bytearray)

    #legacy_abstract_v2_struct_main(args)