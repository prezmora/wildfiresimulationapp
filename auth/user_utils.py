import json
import os
import hashlib
from cryptography.fernet import Fernet
import streamlit as st

# Path to the users file
USERS_FILE = "users.json"

# Generate or load encryption key
def get_key():
    key = os.environ.get("ENCRYPTION_KEY")
    if not key:
        key = Fernet.generate_key()
        os.environ["ENCRYPTION_KEY"] = key.decode()
    return key

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(data, key):
    f = Fernet(key)
    return f.decrypt(data.encode()).decode()

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as file:
        encrypted_data = file.read()
    key = get_key()
    try:
        decrypted_data = decrypt_data(encrypted_data, key)
        return json.loads(decrypted_data)
    except:
        return {}

def save_users(users):
    data = json.dumps(users, indent=4)
    key = get_key()
    encrypted_data = encrypt_data(data, key)
    with open(USERS_FILE, "w") as file:
        file.write(encrypted_data)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(email, password, locations, send_verification_code):
    users = load_users()
    if email in users:
        st.warning("Email already exists. Please choose another one.")
        return False

    verification_code = send_verification_code(email)
    if not verification_code:
        return False

    st.session_state['verification_code'] = verification_code
    st.session_state['pending_user'] = {
        'email': email,
        'password': hash_password(password),
        'locations': locations
    }
    st.session_state['registration_pending'] = True
    return True

def complete_registration(verification_input):
    if verification_input != st.session_state['verification_code']:
        st.warning("Verification code is incorrect.")
        return False

    users = load_users()
    pending_user = st.session_state['pending_user']
    users[pending_user['email']] = pending_user
    save_users(users)
    st.success("Registration successful. You can now log in.")
    st.session_state.clear()
    return True

def login(email, password):
    users = load_users()
    if email not in users:
        st.warning("Email does not exist.")
        return False
    if users[email]['password'] != hash_password(password):
        st.warning("Incorrect password.")
        return False
    st.success("Login successful.")
    st.session_state['logged_in_user'] = email
    return True
