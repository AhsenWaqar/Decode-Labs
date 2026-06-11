import sqlite3
import os
from .config import DB_PATH

def get_db_connection():
    # Ensure db directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        full_name TEXT NOT NULL
            CHECK(length(trim(full_name)) >= 3),
            
        email TEXT NOT NULL UNIQUE,
        
        phone TEXT NOT NULL,
        
        gender TEXT NOT NULL
            CHECK(gender IN ('Male','Female','Other')),
            
        course TEXT NOT NULL,
        
        semester INTEGER NOT NULL
            CHECK(semester BETWEEN 1 AND 12),
            
        cgpa REAL NOT NULL
            CHECK(cgpa >= 0.0 AND cgpa <= 4.0),
            
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()
