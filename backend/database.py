import sqlite3

# Function to initialize tables
def initialize_db():
    conn = sqlite3.connect("eco_actions.db", check_same_thread=False)
    cursor = conn.cursor()
    
    # Create the 'users' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # Create the 'actions' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            points INTEGER NOT NULL
        )
    """)

    # Create the 'logs' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            points INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Commit the changes and close the cursor
    conn.commit()
    cursor.close()
    conn.close()

# Call this function to initialize the database at startup
initialize_db()

# Function to get a new database connection for each request
def get_db_connection():
    conn = sqlite3.connect("eco_actions.db", check_same_thread=False)
    return conn
