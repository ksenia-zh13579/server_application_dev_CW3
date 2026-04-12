import sqlite3

import config

def get_db_connection():
    conn = sqlite3.connect(config.db_name)
    conn.row_factory = sqlite3.Row  # Это позволяет получать данные в виде словаря
    return conn

def create_register_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()
