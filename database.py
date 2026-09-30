import sqlite3
from contextlib import contextmanager
from .config import DATABASE_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    input_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as db:
        db.executescript(SCHEMA)

def create_user(name: str, email: str, password_hash: str) -> int:
    with get_db() as db:
        cur = db.execute("INSERT INTO users(name,email,password_hash) VALUES(?,?,?)", (name, email, password_hash))
        return int(cur.lastrowid)

def get_user_by_email(email: str):
    with get_db() as db:
        return db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

def get_user_by_id(user_id: int):
    with get_db() as db:
        return db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()

def save_recommendation(user_id: int, category: str, input_json: str, result_json: str) -> int:
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO recommendations(user_id,category,input_json,result_json) VALUES(?,?,?,?)",
            (user_id, category, input_json, result_json),
        )
        return int(cur.lastrowid)

def get_recommendation(user_id: int, record_id: int):
    with get_db() as db:
        return db.execute(
            "SELECT * FROM recommendations WHERE id=? AND user_id=?",
            (record_id, user_id),
        ).fetchone()

def list_recommendations(user_id: int, limit: int = 50):
    with get_db() as db:
        return db.execute(
            "SELECT * FROM recommendations WHERE user_id=? ORDER BY id DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
