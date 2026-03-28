import sqlite3
import hashlib
from datetime import datetime

DB_NAME = "shda_local.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password_hash TEXT,
                        role TEXT,
                        sync_status INTEGER DEFAULT 0)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        phone TEXT,
                        join_date TEXT,
                        sync_status INTEGER DEFAULT 0)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS donations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        member_name TEXT,
                        amount REAL,
                        date TEXT,
                        sync_status INTEGER DEFAULT 0)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT,
                        name TEXT,
                        total_amount REAL,
                        comment TEXT,
                        date TEXT,
                        sync_status INTEGER DEFAULT 0)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        action TEXT,
                        timestamp TEXT)''')

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        hashed_pw = hashlib.sha256("admin108".encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                       ("admin", hashed_pw, "Super Admin"))
        log_action("System Initialized.")

    conn.commit()
    conn.close()

def log_action(action):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (action, timestamp) VALUES (?, ?)", 
                   (action, datetime.now().isoformat()))
    conn.commit()
    conn.close()

