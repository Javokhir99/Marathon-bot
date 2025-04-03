import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect("marathon.db")

def create_tables():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section TEXT,
                day INTEGER,
                type TEXT,
                content TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_progress (
                user_id INTEGER,
                section TEXT,
                day INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        db.commit()

# Materiallar bilan ishlash
def add_material(section, day, material_type, content):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO materials (section, day, type, content)
            VALUES (?, ?, ?, ?)
        """, (section, day, material_type, content))
        db.commit()

def get_material(section, day, material_type):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT content FROM materials
            WHERE section=? AND day=? AND type=?
        """, (section, day, material_type))
        result = cursor.fetchone()
        return result[0] if result else None

def delete_material(section, day, material_type):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            DELETE FROM materials WHERE section=? AND day=? AND type=?
        """, (section, day, material_type))
        db.commit()

# Progress
def save_progress(user_id, section, day):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT 1 FROM user_progress WHERE user_id=? AND section=? AND day=?
        """, (user_id, section, day))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO user_progress (user_id, section, day) VALUES (?, ?, ?)
            """, (user_id, section, day))
            db.commit()

def get_user_progress(user_id, section):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            SELECT day FROM user_progress WHERE user_id=? AND section=? ORDER BY day
        """, (user_id, section))
        return [row[0] for row in cursor.fetchall()]

# Bugungi kun sanasi bilan ishlash
def set_start_date(date_str):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO settings (key, value) VALUES ('start_date', ?)
        """, (date_str,))
        db.commit()

def get_start_date():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT value FROM settings WHERE key='start_date'")
        row = cursor.fetchone()
        return row[0] if row else None
