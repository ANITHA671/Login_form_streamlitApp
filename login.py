import streamlit as st
import json
import hashlib
from datetime import datetime
import os

st.set_page_config(page_title="Login App", page_icon="🔐")

DATA_FILE = "users.json"

# -------------------------
# Helpers
# -------------------------
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------------
# Session init
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

users = load_users()

# -------------------------
# UI
# -------------------------
st.title("🔐 Login & Register App")

menu = st.radio("Select Option", ["Login", "Register"])

# -------------------------
# REGISTER
# -------------------------
if menu == "Register":
    st.subheader("📝 Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if username == "" or password == "":
            st.error("All fields required")
        elif password != confirm:
            st.error("Passwords do not match")
        elif username in users:
            st.error("User already exists")
        else:
            users[username] = {
                "password": hash_password(password),
                "created": str(datetime.now())
            }
            save_users(users)
            st.success("Registration successful 🎉")

# -------------------------
# LOGIN
# -------------------------
if menu == "Login":
    st.subheader("🔑 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == hash_password(password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome {username} 🎉")
        else:
            st.error("Invalid credentials")

# -------------------------
# DASHBOARD
# -------------------------
if st.session_state.logged_in:
    st.divider()
    st.subheader("📊 Dashboard")
    st.write("Logged in as:", st.session_state.username)

    col1, col2, col3 = st.columns(3)
    col1.metric("Users", len(users))
    col2.metric("Status", "Active")
    col3.metric("Version", "1.0")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out")
