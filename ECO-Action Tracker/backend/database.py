import sqlite3
import os
from passlib.context import CryptContext

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "eco_actions.db"))

def initialize_db():
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Users table with password_hash column
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Check if old password column exists and migrate
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'password' in columns:
        # Temporary table for migration
        cursor.execute("""
            CREATE TABLE temp_users AS 
            SELECT id, username, password AS password_hash, is_admin, created_at 
            FROM users
        """)
        cursor.execute("DROP TABLE users")
        cursor.execute("ALTER TABLE temp_users RENAME TO users")
    
    # Rest of your tables (actions, logs, messages)...
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT UNIQUE NOT NULL,
            points INTEGER NOT NULL CHECK(points > 0),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action_id INTEGER NOT NULL,
            points INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(action_id) REFERENCES actions(id) ON DELETE RESTRICT
        )
    """)

    # Create admin user if doesn't exist
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = TRUE")
    if cursor.fetchone()[0] == 0:
        hashed_password = pwd_context.hash("admin123")
        cursor.execute(
            "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
            ("admin", hashed_password, True)
        )
    
    # Add default eco-actions
    cursor.execute("SELECT COUNT(*) FROM actions")
    if cursor.fetchone()[0] == 0:
        default_actions = [
            ("Biking", 10),
            ("Planting a tree", 15),
            ("Recycling", 5),
            ("Using reusable bags", 3),
            ("Composting", 8)
        ]
        cursor.executemany(
            "INSERT INTO actions (action, points) VALUES (?, ?)",
            default_actions
        )

    # Add this table to your initialize_db() function
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        awarded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_delivered BOOLEAN DEFAULT FALSE,
        FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE
    )
""")
    
    conn.commit()
    cursor.close()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Initialize database
if __name__ != "__main__":
    initialize_db()