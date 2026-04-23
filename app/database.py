
import sqlite3

DB_NAME = "database.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # ---------- PLAYERS ----------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                team TEXT NOT NULL
            )
        """)

        # ---------- PERFORMANCES ----------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                goals INTEGER,
                assists INTEGER,
                matches_played INTEGER,
                FOREIGN KEY(player_id) REFERENCES players(id)
            )
        """)

        # ---------- USERS (AUTH) ----------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)

        conn.commit()
        conn.close()

    except Exception:
        raise Exception("Database initialization failed")
    
    