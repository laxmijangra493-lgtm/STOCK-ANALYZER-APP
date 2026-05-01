# this is for database storage and user information:-
import sqlite3
import bcrypt

# ---------------------------
# 📌 DB CONNECTION
# ---------------------------

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# ---------------------------
# 📌 CREATE TABLE
# ---------------------------

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mobile TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# ---------------------------
# 📌 REGISTER USER
# ---------------------------
def register_user(name, mobile, email, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        c.execute(
            "INSERT INTO users (name, mobile, email, password) VALUES (?, ?, ?, ?)",
            (name, mobile, email, hashed)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False


# ---------------------------
# 📌 LOGIN USER
# ---------------------------
def login_user(email, password):
    c.execute("SELECT password FROM users WHERE email = ?", (email,))
    result = c.fetchone()

    if result:
        stored_password = result[0].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_password)

    return False