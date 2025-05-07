import os
import sqlite3

from crawler.database.database import create_tables
from crawler.parser.java_parser import parse_java_file
from crawler.use_cases.save_data import save_project_data


def run_crawler(project_path: str, db_path: str = "crawler.db") -> None:
    conn = sqlite3.connect(db_path)
    create_tables(conn)

    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                print(f"Analyzing {file_path}...")
                results = parse_java_file(file_path)

                save_project_data(conn, results)

    conn.close()
    print("Crawler done!")
