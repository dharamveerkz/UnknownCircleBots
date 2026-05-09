import sqlite3
import os

DB_PATH = "data/bot.db"

os.makedirs("data", exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # =====================================================
    # WARNINGS TABLE
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warnings (
        user_id INTEGER PRIMARY KEY,
        count INTEGER DEFAULT 0
    )
    """)

    # =====================================================
    # AI HISTORY (optional future use)
    # =====================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        question TEXT,
        response TEXT
    )
    """)

    conn.commit()
    conn.close()
