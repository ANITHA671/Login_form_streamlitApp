import streamlit as st
import pymysql
import hashlib

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
def init_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="password"  # your MySQL password
    )

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="password",
        database="streamlit_db"
    )

# Initialize database & table
conn = init_connection()
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS streamlit_db")
conn.close()

conn = get_connection()
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        username VARCHAR(50) UNIQUE,
        password VARCHAR(256)
    )
""")
conn.commit()
conn.close()

# -------------------------------
# PASSWORD HASHING
# -------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("Menu")

if st.session_state.logged_in:
    choice = st.sidebar.radio("Navigation", ("Status", "Settings", "Users List", "Logout"))
else:
    choice = st.sidebar.radio("Navigation", ("Register", "Login", "Status"))

# -------------------------------
# REGISTER
# -------------------------------
if choice == "Register":
    st.header("User Registration")

    name = st.text_input("Name")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if name and email and username and password:
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (name, email, username, password) VALUES (%s,%s,%s,%s)",
                    (name, email, username, hash_password(password))
                )
                conn.commit()
                st.success("Registration successful! Please login.")
            except pymysql.err.IntegrityError:
                st.error("Username already exists!")
            finally:
                conn.close()
        else:
            st.warning("All fields are required")

# -------------------------------
# LOGIN
# -------------------------------
elif choice == "Login":
    st.header("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, hash_password(password))
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success(f"Welcome {username} 🎉")
            st.balloons()
        else:
            st.error("Invalid username or password")

# -------------------------------
# STATUS
# -------------------------------
elif choice == "Status":
    st.header("Application Status")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    conn.close()

    st.metric("Total Registered Users", total_users)
    st.metric("Database", "Connected ✅")

    if st.session_state.logged_in:
        st.success(f"Logged in as: {st.session_state.current_user}")
    else:
        st.warning("Not logged in")

# -------------------------------
# SETTINGS (UPDATE PROFILE + THEME)
# -------------------------------
elif choice == "Settings":
    if st.session_state.logged_in:
        st.header("Settings / Profile Update")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, email FROM users WHERE username=%s",
            (st.session_state.current_user,)
        )
        user_data = cursor.fetchone()
        conn.close()

        new_name = st.text_input("Name", value=user_data[0])
        new_email = st.text_input("Email", value=user_data[1])
        new_password = st.text_input("New Password (leave blank to keep current)", type="password")

        st.session_state.theme = st.selectbox("Theme", ["Light", "Dark"], index=0 if st.session_state.theme=="Light" else 1)

        if st.button("Update Profile"):
            conn = get_connection()
            cursor = conn.cursor()
            if new_password:
                cursor.execute(
                    "UPDATE users SET name=%s, email=%s, password=%s WHERE username=%s",
                    (new_name, new_email, hash_password(new_password), st.session_state.current_user)
                )
            else:
                cursor.execute(
                    "UPDATE users SET name=%s, email=%s WHERE username=%s",
                    (new_name, new_email, st.session_state.current_user)
                )
            conn.commit()
            conn.close()
            st.success("Profile updated successfully!")

# -------------------------------
# USERS LIST (FOR LOGGED-IN USERS)
# -------------------------------
elif choice == "Users List":
    if st.session_state.logged_in:
        st.header("Registered Users")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, username FROM users")
        users = cursor.fetchall()
        conn.close()

        for u in users:
            st.write(f"ID: {u[0]} | Name: {u[1]} | Email: {u[2]} | Username: {u[3]}")
    else:
        st.error("Please login to view users")

# -------------------------------
# LOGOUT
# -------------------------------
elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.success("You have been logged out successfully 👋")
