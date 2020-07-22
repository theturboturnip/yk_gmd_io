import argparse
import glob
from pathlib import Path

from yk_gmd_blender.yk_gmd.file import GMDFile

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("glob_folder", type=Path)

    args = parser.parse_args()

    for gmd_path in glob.iglob(str(args.glob_folder / "**" / "*.gmd"), recursive=True):
        with open(gmd_path, "rb") as f:
            gmd_file = GMDFile(f.read())
        for i, v in enumerate(gmd_file.structs.vertex_buffer_layouts):
            print(f"{gmd_file.structs.name} {i} {v.bytes_per_vertex} {v.flags[0]:02x} {v.flags[1]:02x} {v.flags[2]:02x} {v.flags[3]:02x} {v.flags[4]:02x} {v.flags[5]:02x} {v.flags[6]:02x} {v.flags[7]:02x}")