import sqlite3
from pathlib import Path
from typing import Callable, Generator

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


@pytest.fixture  # type: ignore[misc]
def java_file(tmp_path: Path) -> Callable[[str, str], str]:
    """
    Fixture to create temporary Java files.
    Receives Java code and optionally a file name,
    writes it to disk, and returns the path.
    Args:
        code: Java code
        filename: File name
    Returns:
        File path
    """

    def _create_file(code: str, filename: str = "Test.java") -> str:
        file_path = tmp_path / filename
        file_path.write_text(code)
        return str(file_path)

    return _create_file


@pytest.fixture  # type: ignore[misc]
def java_class_simple() -> str:
    return """
    public class MyClass {
        public void myMethod() {}
    }
    """


@pytest.fixture  # type: ignore[misc]
def java_class_with_return_type() -> str:
    return """
    public class Calculator {
        public int add(int a, int b) { return a + b; }
    }
    """


@pytest.fixture  # type: ignore[misc]
def java_class_with_inheritance() -> str:
    return """
    public class Child extends Parent implements Serializable {
        public String greet() { return "Hello"; }
    }
    """


@pytest.fixture  # type: ignore[misc]
def java_interface() -> str:
    return """
    public interface MyInterface {
        void doSomething();
    }
    """


@pytest.fixture  # type: ignore[misc]
def java_class_with_static_method() -> str:
    return """
    public class Utils {
        public static double pi() { return 3.14; }
    }
    """


@pytest.fixture  # type: ignore[misc]
def java_code_invalid() -> str:
    return "this is not valid java code"
