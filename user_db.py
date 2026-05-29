import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def register_user(name: str, email: str, password: str):
    if not name or not name.strip():
        raise ValueError("Ad Soyad alanı boş bırakılamaz.")
    if not email or not email.strip():
        raise ValueError("E-posta alanı boş bırakılamaz.")
    if not password or not password.strip():
        raise ValueError("Şifre alanı boş bırakılamaz.")
        
    normalized_email = email.strip().lower()
    name = name.strip()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (normalized_email,))
    if cursor.fetchone():
        conn.close()
        raise ValueError("Bu e-posta adresiyle zaten kayıtlı bir hesap bulunmaktadır.")
        
    password_hash = hash_password(password)
    
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, normalized_email, password_hash)
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"id": user_id, "name": name, "email": normalized_email}

def login_user(email: str, password: str):
    if not email or not email.strip() or not password or not password.strip():
        raise ValueError("E-posta ve şifre alanları boş bırakılamaz.")
        
    normalized_email = email.strip().lower()
    password_hash = hash_password(password)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, name, email, password_hash FROM users WHERE email = ?",
        (normalized_email,)
    )
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise ValueError("E-posta adresi veya şifre hatalı.")
        
    user_id, name, email_val, stored_hash = user
    if stored_hash != password_hash:
        raise ValueError("E-posta adresi veya şifre hatalı.")
        
    return {"id": user_id, "name": name, "email": email_val}

def get_user_by_id(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return None
        
    user_id_val, name, email_val = user
    return {"id": user_id_val, "name": name, "email": email_val}
