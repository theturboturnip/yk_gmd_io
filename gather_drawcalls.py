from typing import Callable, Optional
import yk_gmd_blender
import argparse
import glob
import sqlite3
from dataclasses import dataclass

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
    attrib_set_id: int


DRAWCALL_TABLE_SPEC_V1 = """CREATE TABLE DrawCalls (
    id INT PRIMARY KEY,
    GmdFile TEXT NOT NULL,
    NodeName TEXT NOT NULL,
    DrawOrder INT NOT NULL,
    VertLayoutFlags INT NOT NULL,
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
    # Never filled
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
    Flags INT NOT NULL,
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
        print(f"Version: {self.version}")
        if self.version > DRAWCALL_DB_VERSION:
            raise RuntimeError(f"DB user_version {self.version} greater than current max version {DRAWCALL_DB_VERSION}. Please update this tool")
        self.migrate()

    def bump_version(self, migration: Callable, new_version: int):
        self.cur.execute("begin")
        try:
            migration()
            self.cur.execute(f"PRAGMA user_version = {new_version:d}")
            self.cur.execute("commit")
            self.conn.commit()
        except sqlite3.Error as e:
            self.cur.execute("rollback")
            raise e
        finally:
            self.version = new_version

    def migrate(self):
        if self.version == 0:
            def v1():
                self.cur.execute(ATTRIBSET_TABLE_SPEC_V1)
                self.cur.execute(DRAWCALL_TABLE_SPEC_V1)
            self.bump_version(v1, 1)
        assert self.version == DRAWCALL_DB_VERSION

    def close(self):
        self.cur.close()
        self.conn.close()
        self.cur = None
        self.conn = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("db")

    args = parser.parse_args()

    db = DrawCallDb(args.db)

    db.close()