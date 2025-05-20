import sqlite3
from typing import Generator

import pytest

from crawler.database.database import create_tables, insert_class
from crawler.models.class_info import ClassInfo
from crawler.models.method_info import MethodInfo


@pytest.fixture  # type: ignore[misc]
def db_connection() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(":memory:")
    create_tables(conn)
    yield conn
    conn.close()


@pytest.fixture  # type: ignore[misc]
def sample_class_info() -> ClassInfo:
    return ClassInfo(
        id=None,
        name="TestClass",
        file_path="src/TestClass.java",
        line_number=10,
    )


@pytest.fixture  # type: ignore[misc]
def persisted_class_info(
        db_connection: sqlite3.Connection, sample_class_info: ClassInfo
) -> ClassInfo:
    class_id = insert_class(db_connection, sample_class_info)
    sample_class_info.id = class_id
    return sample_class_info


@pytest.fixture  # type: ignore[misc]
def sample_method_info(persisted_class_info: ClassInfo) -> MethodInfo:
    return MethodInfo(
        class_id=persisted_class_info.id,
        method_name="doSomething",
        line_number=12,
    )
