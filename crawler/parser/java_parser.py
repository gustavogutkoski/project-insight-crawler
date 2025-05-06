import os
import re
import sqlite3
import sys
from typing import List, Tuple

from crawler.database.database import create_tables, insert_class, insert_method
from crawler.models.class_info import ClassInfo
from crawler.models.method_info import MethodInfo

class_pattern = re.compile(
    r"^(?:public\s+|protected\s+|private\s+|abstract\s+|final\s+|static\s+)*"
    r"(class|interface|enum)\s+(\w+)"
    r"(?:\s+extends\s+(\w+))?"
    r"(?:\s+implements\s+([\w\s,]+))?"
)

method_pattern = re.compile(
    r"(public|private|protected)?\s*"
    r"(static\s+)?"
    r"([\w<>\[\]]+\s+)"
    r"(\w+)\s*"
    r"\("
)


def parse_java_file(file_path: str) -> Tuple[List[ClassInfo], List[MethodInfo]]:
    classes: List[ClassInfo] = []
    methods: List[MethodInfo] = []

    current_class = None

    with open(file_path, "r", encoding="utf-8") as file:
        for idx, line in enumerate(file):
            # Search for classes
            class_match = class_pattern.search(line)
            if class_match:
                current_class = process_class(class_match, file_path, idx)
                classes.append(current_class)

            # Search for methods if class found
            method_match = method_pattern.search(line)
            if method_match and current_class:
                process_method(line, current_class, idx, methods)

    return classes, methods


def process_class(class_match: re.Match[str], file_path: str, line_number: int) -> ClassInfo:
    class_type = class_match.group(1)
    class_name = class_match.group(2)
    superclass = class_match.group(3)
    interfaces = class_match.group(4)

    return ClassInfo(
        id=None,
        name=class_name,
        file_path=file_path,
        line_number=line_number + 1,
        superclass=superclass,
        interfaces=interfaces,
        class_type=class_type,
    )


def process_method(
    line: str, current_class: ClassInfo, line_number: int, methods: List[MethodInfo]
) -> None:
    method_match = method_pattern.search(line)
    if method_match:
        modifier = method_match.group(1)
        is_static = method_match.group(2) is not None
        return_type = method_match.group(3).strip()
        method_name = method_match.group(4)

        if current_class.id is None:
            raise ValueError(f"ID not set for class {current_class.name}")

        method_info = MethodInfo(
            class_id=current_class.id,
            method_name=method_name,
            line_number=line_number + 1,
            return_type=return_type,
            modifier=modifier,
            is_static=is_static,
        )
        methods.append(method_info)


def crawl_project(base_path: str, db_path: str = "crawler.db") -> None:
    conn = sqlite3.connect(db_path)
    create_tables(conn)

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                print(f"Analyzing {file_path}...")
                classes, methods = parse_java_file(file_path)

                # Insert class and link its ID to methods
                for cls in classes:
                    class_id = insert_class(conn, cls)
                    for mtd in methods:
                        mtd.class_id = class_id
                        insert_method(conn, mtd)

    conn.close()
    print("Crawler done!")


if __name__ == "__main__":
    project_path = input("Enter the Java project path: ").strip()

    if not os.path.exists(project_path):
        print(f"Error: The path '{project_path}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(project_path):
        print(f"Error: The path '{project_path}' is not a directory.")
        sys.exit(1)

    crawl_project(project_path)
