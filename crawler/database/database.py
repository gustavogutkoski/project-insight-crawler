import sqlite3
from typing import cast

from crawler.models.class_info import ClassInfo
from crawler.models.method_info import MethodInfo


def create_tables(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            file_path TEXT,
            line_number INTEGER,
            superclass TEXT,
            interfaces TEXT,
            class_type TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER,
            method_name TEXT,
            line_number INTEGER,
            return_type TEXT,
            modifier TEXT,
            is_static BOOLEAN,
            FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
        )
    """)
    conn.commit()


def insert_class(conn: sqlite3.Connection, class_info: ClassInfo) -> int:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO classes (name,
                             file_path,
                             line_number,
                             superclass,
                             interfaces,
                             class_type)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            class_info.name,
            class_info.file_path,
            class_info.line_number,
            class_info.superclass,
            class_info.interfaces,
            class_info.class_type,
        ),
    )
    conn.commit()
    class_id = cursor.lastrowid
    assert class_id is not None
    class_info.id = class_id
    return class_id


def insert_method(conn: sqlite3.Connection, method_info: MethodInfo) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO methods (class_id,
                             method_name,
                             line_number,
                             return_type,
                             modifier,
                             is_static)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            method_info.class_id,
            method_info.method_name,
            method_info.line_number,
            method_info.return_type,
            method_info.modifier,
            method_info.is_static,
        ),
    )
    conn.commit()
