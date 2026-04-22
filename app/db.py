import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

def create_user(u, p):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (NULL, ?, ?)",
              (u, generate_password_hash(p)))
    conn.commit()
    conn.close()

def verify_user(u, p):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    user = c.execute("SELECT * FROM users WHERE username=?", (u,)).fetchone()
    conn.close()

    return user and check_password_hash(user[2], p)