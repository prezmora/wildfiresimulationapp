import json
import os
import hashlib

# File path for the JSON file
user_file_path = 'user.json'

def load_users():
    if os.path.exists(user_file_path):
        with open(user_file_path, 'r') as file:
            users_db = json.load(file)
    else:
        users_db = {}

    # Ensure the correct structure
    if "emails" not in users_db:
        users_db["emails"] = []
    if "users" not in users_db:
        users_db["users"] = []

    return users_db

def save_users(users_db):
    with open(user_file_path, 'w') as file:
        json.dump(users_db, file, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(users_db, email, password):
    if email in users_db["emails"]:
        return False, "Email already registered."
    
    hashed_password = hash_password(password)
    users_db["emails"].append(email)
    users_db["users"].append({"email": email, "password": hashed_password})
    save_users(users_db)
    return True, "Registration successful!"

def authenticate_user(users_db, email, password):
    hashed_password = hash_password(password)
    if email in users_db["emails"]:
        user_index = users_db["emails"].index(email)
        user = users_db["users"][user_index]
        if user["password"] == hashed_password:
            return True
    return False
