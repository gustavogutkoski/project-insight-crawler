import sqlite3
from typing import List, Tuple

from crawler.models.class_info import ClassInfo
from crawler.models.method_info import MethodInfo
from crawler.use_cases.save_data import save_project_data


def test_save_project_data(
    db_connection: sqlite3.Connection, sample_class_info: ClassInfo, sample_method_info: MethodInfo
) -> None:
    results = [(sample_class_info, [sample_method_info])]

    save_project_data(db_connection, results)

    cursor = db_connection.cursor()
    cursor.execute("""
                   SELECT c.name, m.method_name, c.file_path, m.line_number
                   FROM classes c
                            JOIN methods m ON c.id = m.class_id
                   """)
    rows = cursor.fetchall()

    assert len(rows) == 1
    assert rows[0] == ("TestClass", "doSomething", "src/TestClass.java", 12)


def test_save_project_data_with_no_methods(
    db_connection: sqlite3.Connection, sample_class_info: ClassInfo
) -> None:
    results: List[Tuple[ClassInfo, List[MethodInfo]]] = [(sample_class_info, [])]

    save_project_data(db_connection, results)

    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM classes")
    rows = cursor.fetchall()

    assert len(rows) == 1
    assert rows[0][0] == "TestClass"

    cursor.execute("SELECT * FROM methods")
    assert cursor.fetchall() == []


def test_save_project_data_with_empty_results(db_connection: sqlite3.Connection) -> None:
    results: List[Tuple[ClassInfo, List[MethodInfo]]] = []

    save_project_data(db_connection, results)

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM classes")
    assert cursor.fetchall() == []

    cursor.execute("SELECT * FROM methods")
    assert cursor.fetchall() == []


def test_save_project_data_multiple_classes_and_methods(db_connection: sqlite3.Connection) -> None:
    class1 = ClassInfo(id=None, name="ClassA", file_path="A.java", line_number=1)
    class2 = ClassInfo(id=None, name="ClassB", file_path="B.java", line_number=2)
    method1 = MethodInfo(class_id=None, method_name="m1", line_number=3)
    method2 = MethodInfo(class_id=None, method_name="m2", line_number=4)

    results = [(class1, [method1]), (class2, [method2])]

    save_project_data(db_connection, results)

    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM classes")
    classes = cursor.fetchall()
    assert len(classes) == 2

    cursor.execute("SELECT method_name FROM methods")
    methods = cursor.fetchall()
    assert len(methods) == 2


def test_method_class_id_is_set_after_save(db_connection: sqlite3.Connection) -> None:
    class_info = ClassInfo(id=None, name="Example", file_path="ex.java", line_number=1)
    method_info = MethodInfo(class_id=class_info.id, method_name="exampleMethod", line_number=2)
    results = [(class_info, [method_info])]

    save_project_data(db_connection, results)

    assert method_info.class_id == class_info.id
