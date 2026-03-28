import hashlib
from core.database import get_connection, log_action

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, role, password_hash FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and user[2] == hash_password(password):
        log_action(f"User {username} logged in.")
        return {"id": user[0], "role": user[1], "username": username}
    return None

