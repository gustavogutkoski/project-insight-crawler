import sqlite3

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            file_path TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT,
            method_name TEXT,
            line_number INTEGER
        )
    ''')
    conn.commit()

def insert_class(conn, class_info):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO classes (name, file_path)
        VALUES (?, ?)
    ''', (class_info.name, class_info.file_path))
    conn.commit()

def insert_method(conn, method_info):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO methods (class_name, method_name, line_number)
        VALUES (?, ?, ?)
    ''', (method_info.class_name, method_info.method_name, method_info.line_number))
    conn.commit()
