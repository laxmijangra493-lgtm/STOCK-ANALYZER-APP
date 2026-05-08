import sqlite3
import bcrypt
import os

DB_NAME = "users.db"

def get_conn():
    """Always return a fresh connection (thread-safe)."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create tables if they don't exist."""
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            mobile   TEXT,
            email    TEXT    UNIQUE NOT NULL,
            password TEXT    NOT NULL
        )
    """)
    # Fixed schema: composite PK so one user can have many symbols
    c.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            user_id INTEGER NOT NULL,
            symbol  TEXT    NOT NULL,
            PRIMARY KEY (user_id, symbol),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

init_db()


def register_user(name, mobile, email, password):
    """Returns True on success, False if email already exists."""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        conn = get_conn()
        conn.execute(
            "INSERT INTO users (name, mobile, email, password) VALUES (?, ?, ?, ?)",
            (name.strip(), mobile.strip(), email.strip().lower(), hashed)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(email, password):
    """Returns (user_id, name) on success, (None, None) on failure."""
    conn = get_conn()
    row = conn.execute(
        "SELECT id, name, password FROM users WHERE email = ?",
        (email.strip().lower(),)
    ).fetchone()
    conn.close()

    if row and bcrypt.checkpw(password.encode(), row["password"].encode()):
        return row["id"], row["name"]
    return None, None



