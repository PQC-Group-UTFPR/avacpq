import sqlite3
import os

DATABASE_PATH = 'database.db'

def get_db():
    """Connect to the SQLite database and return the connection"""
    db = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize the database with the necessary tables"""
    db = get_db()
    
    try:
        # Create users table
        db.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                profile_pic TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        db.commit()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        db.close()

def init_db_command():
    """CLI command to initialize the database"""
    init_db()
