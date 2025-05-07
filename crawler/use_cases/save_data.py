import sqlite3
from typing import List, Tuple

from crawler.database.database import insert_class, insert_method
from crawler.models.class_info import ClassInfo
from crawler.models.method_info import MethodInfo


def save_project_data(
    conn: sqlite3.Connection, results: List[Tuple[ClassInfo, List[MethodInfo]]]
) -> None:
    for cls, methods in results:
        class_id = insert_class(conn, cls)
        for mtd in methods:
            mtd.class_id = class_id
            insert_method(conn, mtd)
