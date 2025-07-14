import sqlite3
import os

def get_db_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "eco_actions.db"))

# Initialize database tables if not already present
def initialize_db():
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            points INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            points INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

# Always get a fresh connection with the correct path
def get_db_connection():
    path = get_db_path()
    print("🔍 Using DB path:", path)  # TEMPORARY DEBUG PRINT
    return sqlite3.connect(path, check_same_thread=False)

# Call this once on app start
initialize_db()
