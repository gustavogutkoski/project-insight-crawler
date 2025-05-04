import os
import re
import sqlite3
import sys
from models import ClassInfo, MethodInfo
from database import create_tables, insert_class, insert_method

def parse_java_file(file_path):
    classes = []
    methods = []

    class_pattern = re.compile(
        r'^(?:public\s+|protected\s+|private\s+|abstract\s+|final\s+|static\s+)*'  # Optional modifiers
        r'class\s+(\w+)'                                                           # Class name
        r'(?:\s+extends\s+(\w+))?'                                                 # Optional superclass
        r'(?:\s+implements\s+([\w\s,]+))?'                                         # Optional interfaces
    )

    method_pattern = re.compile(
        r'(public|private|protected)?\s*'  # Access modifier (optional)
        r'(static\s+)?'                    # static keyword (optional)
        r'([\w<>\[\]]+\s+)'                # Return type (e.g., int, String, List<String>, int[])
        r'(\w+)\s*'                        # Method name
        r'\('                              # Opening parenthesis of method parameters
    )

    enum_pattern = re.compile(
        r'^(?:public\s+|protected\s+|private\s+|static\s+)*'  # Optional modifiers
        r'enum\s+(\w+)'  # Enum name
    )

    interface_pattern = re.compile(
        r'^(?:public\s+|protected\s+|private\s+|abstract\s+|static\s+)*'  # Optional modifiers
        r'interface\s+(\w+)'  # Interface name
    )

    current_class = None

    with open(file_path, 'r', encoding='utf-8') as file:
        for idx, line in enumerate(file):
            # Search for classes
            class_match = class_pattern.search(line)
            if class_match:
                current_class = class_match.group(1)
                classes.append(ClassInfo(name=current_class, file_path=file_path))

            # Search for methods if class found
            method_match = method_pattern.search(line)
            if method_match and current_class:
                method_name = method_match.group(4)
                methods.append(MethodInfo(class_name=current_class, method_name=method_name, line_number=idx + 1))

    return classes, methods


def crawl_project(base_path, db_path="crawler.db"):
    conn = sqlite3.connect(db_path)
    create_tables(conn)

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                print(f"Analyzing {file_path}...")
                classes, methods = parse_java_file(file_path)

                for cls in classes:
                    insert_class(conn, cls)
                for mtd in methods:
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
