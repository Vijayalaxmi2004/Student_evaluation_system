# auth.py
import os
import hashlib
import random
import string
import pandas as pd


# File paths
USERS_FILE = "data/users_db.csv"
FEEDBACK_FILE = "data/student_feedback.csv"
ANNOUNCEMENT_FILE = "data/announcements.csv"
GRADES_FILE = "data/grades_db.csv"

_DB_STRUCTURE = {
    USERS_FILE: ["username","password","role"],
    FEEDBACK_FILE: ["rollno","year","semester","feedback"],
    ANNOUNCEMENT_FILE: ["date","title","message","posted_by"]
}

def _normalize_user(username):
    return username.strip().lower()

def init_db():
    os.makedirs("data", exist_ok=True)
    for filepath, cols in _DB_STRUCTURE.items():
        if not os.path.exists(filepath):
            pd.DataFrame(columns=cols).to_csv(filepath, index=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    df = pd.read_csv(USERS_FILE)
    u_norm = _normalize_user(username)
    user_row = df[df["username"].str.strip().str.lower() == u_norm]
    return user_row.iloc[0]["role"] if not user_row.empty and user_row.iloc[0]["password"] == hash_password(password) else None

def register_user(username, password, role, department=None):
    df = pd.read_csv(USERS_FILE)
    username = _normalize_user(username)
    
    if not username or not password:
        return False, "⚠ Username and Password required"
    if username in df["username"].astype(str).str.strip().str.lower().values:
        return False, "❌ Username already exists"
    if role == "Student" and not department:
        return False, "⚠ Please select a department"
    
    new_user = {"username": username, "password": hash_password(password), "role": role, "department": department if role != "Faculty" else "Not Applicable"}
    pd.concat([df, pd.DataFrame([new_user])], ignore_index=True).to_csv(USERS_FILE, index=False)
    return True, "✅ Registered Successfully"
def reset_password(username, password=None):
    df = pd.read_csv(USERS_FILE)
    u_norm = _normalize_user(username)
    user_mask = df["username"].str.strip().str.lower() == u_norm
    if not user_mask.any():
        return None
    new_password = password if password else ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    df.loc[user_mask, "password"] = hash_password(new_password)
    df.to_csv(USERS_FILE, index=False)
    return new_password
