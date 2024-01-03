import json
from pathlib import Path
import subprocess
from typing import Any, Generator, List, Callable, Optional, Set
import yk_gmd_blender
import argparse
import glob
import sqlite3
from dataclasses import dataclass

from yk_gmd_blender.gmdlib.errors.error_reporter import LenientErrorReporter
from yk_gmd_blender.gmdlib.io import read_gmd_structures

# two databases: one of gmd files and their n_meshes, n_nodes, flags, etc.
# one of the mappings (file_name, node_name, draw_order, x vertices, x indices, vertex buffer layout flags, shader, textures, attribute sets, material)

@dataclass
class DrawCall:
    gmd_file: str
    node_name: str
    draw_order: int
    vertex_layout_flags: int
    bytes_per_vertex: int
    vert_count: int
    index_count_tri: int
    index_count_tri_strip: int
    index_count_tri_strip_reset: int
    matrix_count: int
    attrib_set_index: int # This is different to the column in the table! This is relative to the list of attribsets in the associated file. The database 


DRAWCALL_TABLE_SPEC_V1 = """CREATE TABLE DrawCalls (
    id INT PRIMARY KEY,
    GmdFile TEXT NOT NULL,
    NodeName TEXT NOT NULL,
    DrawOrder INT NOT NULL,
    VertLayoutFlags BLOB(8) NOT NULL,
    BytesPerVert INT NOT NULL,
    VertCount INT NOT NULL,
    IndexCountTri INT NOT NULL,
    IndexCountTriStrip INT NOT NULL,
    IndexCountTriStripReset INT NOT NULL,
    MatrixCount INT NOT NULL,
    AttribSetId INT NOT NULL,
    FOREIGN KEY(AttribSetId) REFERENCES AttribSet(id)
)"""


@dataclass
class AttribSet:
    gmd_file: str
    shader: str
    flags: int
    material: str # JSON-encoded from MaterialStruct_YK1
    texture_diffuse: Optional[str]  # Usually has textures with _di postfix
    texture_refl: Optional[str]  # Observed to have a cubemap texture for one eye-related material
    texture_multi: Optional[str]
    texture_rm: Optional[str]
    texture_ts: Optional[str]  # Only present in "rs" shaders
    texture_normal: Optional[str]  # Usually has textures with _tn postfix
    texture_rt: Optional[str]  # Usually has textures with _rt postfix
    texture_rd: Optional[str]  # Usually has textures with _rd postfix
    extra_properties: str  # JSON-encoded set of 16 floats. Could be scale (x,y) pairs for the textures, although 0 is present a lot.


ATTRIBSET_TABLE_SPEC_V1 = """CREATE TABLE AttribSet (
    id INT PRIMARY KEY,
    GmdFile TEXT NOT NULL,
    Shader TEXT NOT NULL,
    Flags BLOB(8) NOT NULL,
    Material JSON NOT NULL,
    TexDiffuse TEXT,
    TexRefl TEXT,
    TexMulti TEXT,
    TexRm TEXT,
    TexTs TEXT,
    TexNormal TEXT,
    TexRt TEXT,
    TexRd TEXT,
    ExtraProperties JSON NOT NULL
)"""

DRAWCALL_DB_VERSION = 1


class DrawCallDb:
    conn: sqlite3.Connection
    cur: sqlite3.Cursor
    version: int

    def __init__(self, path: str):
        self.conn = sqlite3.Connection(path)
        self.conn.isolation_level = None
        # self.conn.set_trace_callback(print)
        self.cur = self.conn.cursor()
        self.version = self.cur.execute("SELECT user_version FROM pragma_user_version").fetchone()[0]
        print(f"DB Version: {self.version}")
        if self.version > DRAWCALL_DB_VERSION:
            raise RuntimeError(f"DB user_version {self.version} greater than current max version {DRAWCALL_DB_VERSION}. Please update this tool")
        self.migrate()

    def bump_version(self, migration: Callable, new_version: int):
        self.cur.execute("begin")
        try:
            migration()
            # Can't use a placeholder here - SQLite complains
            self.cur.execute(f"PRAGMA user_version = {new_version:d}")
            self.cur.execute("commit")
        except sqlite3.Error as e:
            self.cur.execute("rollback")
            raise e
        finally:
            self.version = new_version

    def transact(self, t: Callable):
        self.cur.execute("begin")
        try:
            t()
            self.cur.execute("commit")
        except Exception as e:
            self.cur.execute("rollback")
            raise e

    def migrate(self):
        if self.version == 0:
            def v1():
                self.cur.execute(ATTRIBSET_TABLE_SPEC_V1)
                self.cur.execute(DRAWCALL_TABLE_SPEC_V1)
            self.bump_version(v1, 1)
        assert self.version == DRAWCALL_DB_VERSION

    def insert_attrsets_and_drawcalls(self, attr_sets: List[AttribSet], drawcalls: List[DrawCall]):
        def inner():
            attr_set_primary_keys = []
            for a in attr_sets:
                self.cur.execute(
                    "INSERT INTO AttribSet (GmdFile, Shader, Flags, Material, TexDiffuse, TexRefl, TexMulti, TexRm, TexTs, TexNormal, TexRt, TexRd, ExtraProperties) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (a.gmd_file, a.shader, a.flags.to_bytes(8), a.material, a.texture_diffuse, a.texture_refl, a.texture_multi, a.texture_rm, a.texture_ts, a.texture_normal, a.texture_rt, a.texture_rd, a.extra_properties)
                )
                attr_set_primary_keys.append(self.cur.lastrowid)
            for d in drawcalls:
                self.cur.execute(
                    "INSERT INTO DrawCalls (GmdFile, NodeName, DrawOrder, VertLayoutFlags, BytesPerVert, VertCount, IndexCountTri, IndexCountTriStrip, IndexCountTriStripReset, MatrixCount, AttribSetId)"
                    " VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        d.gmd_file, d.node_name, d.draw_order,
                        d.vertex_layout_flags.to_bytes(8), d.bytes_per_vertex, d.vert_count,
                        d.index_count_tri, d.index_count_tri_strip, d.index_count_tri_strip_reset,
                        d.matrix_count, attr_set_primary_keys[d.attrib_set_index]
                    )
                )
        self.transact(inner)

    def close(self):
        self.cur.close()
        self.conn.close()
        self.cur = None
        self.conn = None

class ParTool:
    exe_path: Path

    def __init__(self, exe_path: Path, skip_check: bool=False) -> None:
        if not exe_path.is_file():
            raise ValueError(f"Path {exe_path} doesn't point to a file, so couldn't possibly point to ParTool.")
        self.exe_path = exe_path
        if not skip_check:
            test_run = self.run_partool([], check_retcode=False)
            if not test_run.stdout.startswith("ParTool"):
                raise ValueError(f"{exe_path} doesn't print 'ParTool' when run, so is probably not ParTool. Use --skip_partool_check to use it anyway.")

    def run_partool(self, args: List[Any], check_retcode: bool=True) -> subprocess.CompletedProcess:
        return subprocess.run([self.exe_path] + args, check=check_retcode, capture_output=True, text=True)

    def get_listing(self, file: Path) -> Generator[str, None, None]:
        if not file.is_file():
            raise ValueError(f"can't get listing for archive {file} that doesn't exist")
        # Do a recursive listing
        output: str = self.run_partool(["list", "-r", "--filter", r".*\.gmd$", str(file)]).stdout
        # output is line-by-line and tab-separated
        for line in output.splitlines():
            if line.startswith("/"): # the first few lines are e.g. partool version, but files seem to always start with /
                internal_path = line.split("\t")[0]
                # Remove following * if present - that denotes compression
                if internal_path.endswith("*"):
                    internal_path = internal_path[:-1]
                yield internal_path
    
    def extract_par(self, par_path: Path):
        extract_to = extracted_par_name(par_path)
        if extract_to.is_dir():
            raise ValueError("I won't try to extract to a directory that already exists!")
        self.run_partool(["extract", "-r", "--filter", r".*\.gmd$", str(par_path), str(extract_to)])

# Generate the directory name partool should extract a par into.
# This matches ParToolShell's behaviour.
def extracted_par_name(par_path: Path) -> Path:
    # assert par_path.is_file()
    # assert str(par_path).endswith(".par")
    return par_path.with_name(par_path.name + ".unpack")

import os

def fastglob(path: str, ext: str) -> Generator[Path, None, None]:
    for (dirpath, dirnames, filenames) in os.walk(path):
        for i in reversed(range(len(dirnames))):
            if dirnames[i].endswith(".unpack"):
                del dirnames[i]
        for f in filenames:
            if f.endswith(ext):
                yield Path(dirpath) / f

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("db", type=Path)
    parser.add_argument("game_folder", type=Path)
    parser.add_argument("--extract_pars_with", type=Path)
    parser.add_argument("--skip_partool_check", action="store_true", default=False)
    parser.add_argument("--dry_run", action="store_true", default=False)

    args = parser.parse_args()

    db = DrawCallDb(args.db)

    game_folder: Path = args.game_folder    

    if args.extract_pars_with:
        partool = ParTool(args.extract_pars_with, args.skip_partool_check)

        # Glob the .pars in the game_folder, extract GMDs from them
        for par_file in game_folder.glob("**/*.par"):
        # for par_file in fastglob(str(game_folder), ".par"):
            # If the par_file isn't a file, skip
            if not par_file.is_file():
                print(f"{par_file} apparently is not a file, skipping...")
                continue
            # Check if the par has already been extracted, assume it has extracted all the GMDs
            if not extracted_par_name(par_file).is_dir():
                # If the par contains a GMD, we want to extract it
                # if any(x.endswith(".gmd") for x in partool.get_listing(par_file)):
                if not args.dry_run:
                    print(f"Extracting GMDs from {par_file}... ", end="")
                    partool.extract_par(par_file)
                    print("done")
                else:
                    print(f"DRY RUN extracting {par_file}")
            else:
                print(f"{par_file} was already extracted - skipping")
    else:
        print(f"Will scan {game_folder} for GMDs, but won't find any in unextracted PARs!!")

    # Glob the .gmds in the game_folder, process them
    error_reporter = LenientErrorReporter(set())
    
    db.cur.execute("SELECT DISTINCT GmdFile FROM AttribSet")
    meshs_already_handled = set(db.cur.fetchall())

    for gmd_file in game_folder.glob("**/*.gmd"):
        gmd_file_name = gmd_file.name
        if "bone.gmd" in gmd_file_name:
            continue # Hack, bone files are weird and sometimes break things? and I don't want to deal wit that
        if (gmd_file_name,) in meshs_already_handled:
            continue

        print(gmd_file)
        version_props, header, file_data = read_gmd_structures(gmd_file, error_reporter)

        def lookup_tex(tex):
            if tex.tex_index < 0:
                return None
            else:
                return file_data.texture_arr[tex.tex_index].text

        attr_sets = []
        for attr_set in file_data.attribute_arr:
            attr_sets.append(AttribSet(
                gmd_file=gmd_file_name,
                shader=file_data.shader_arr[attr_set.shader_index].text,
                flags=attr_set.flags, # TODO this may miss out some parts of the flags in non-dragon engine games
                material=json.dumps(file_data.material_arr[attr_set.material_index].__dict__),
                extra_properties=json.dumps(attr_set.extra_properties),
                texture_diffuse=lookup_tex(attr_set.texture_diffuse),
                texture_refl=lookup_tex(attr_set.texture_refl),
                texture_multi=lookup_tex(attr_set.texture_multi),
                texture_rm=lookup_tex(attr_set.texture_rm),
                texture_ts=lookup_tex(attr_set.texture_ts),
                texture_normal=lookup_tex(attr_set.texture_normal),
                texture_rt=lookup_tex(attr_set.texture_rt),
                texture_rd=lookup_tex(attr_set.texture_rd),
            ))
        drawcalls = []
        for i, drawcall in enumerate(file_data.mesh_arr):
            drawcalls.append(DrawCall(
                gmd_file=gmd_file_name,
                node_name=file_data.node_name_arr[file_data.node_arr[drawcall.node_index].name_index].text,
                draw_order=i,
                vertex_layout_flags=file_data.vertex_buffer_arr[drawcall.vertex_buffer_index].vertex_packing_flags,
                bytes_per_vertex=file_data.vertex_buffer_arr[drawcall.vertex_buffer_index].bytes_per_vertex,
                vert_count=drawcall.vertex_count,
                index_count_tri=drawcall.triangle_list_indices.index_count,
                index_count_tri_strip=drawcall.noreset_strip_indices.index_count,
                index_count_tri_strip_reset=drawcall.reset_strip_indices.index_count,
                matrix_count=drawcall.matrixlist_length,
                attrib_set_index=drawcall.attribute_index,
            ))
        db.insert_attrsets_and_drawcalls(attr_sets, drawcalls)

    db.close()
