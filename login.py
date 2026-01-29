import streamlit as st
import re
import time
from datetime import datetime
import hashlib

# Page configuration
st.set_page_config(
    page_title="User Authentication System",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# Initialize session state
# -------------------------------
if 'users' not in st.session_state:
    st.session_state.users = {}  # stores users as {username: {'email': ..., 'password': hashed}}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# -------------------------------
# Password hashing function
# -------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------------------
# User functions
# -------------------------------
def register_user(username, email, password, confirm_password):
    # Validation
    if not username or not email or not password:
        st.warning("⚠️ Please fill all fields")
        return False
    
    if len(username) < 3:
        st.warning("⚠️ Username must be at least 3 characters long")
        return False
    
    if len(password) < 6:
        st.warning("⚠️ Password must be at least 6 characters long")
        return False
    
    if password != confirm_password:
        st.warning("⚠️ Passwords do not match")
        return False
    
    # Email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        st.warning("⚠️ Please enter a valid email address")
        return False
    
    # Check if username/email exists
    if username in st.session_state.users:
        st.error("❌ Username already exists")
        return False
    for user in st.session_state.users.values():
        if user['email'] == email:
            st.error("❌ Email already registered")
            return False
    
    # Save user
    st.session_state.users[username] = {
        'email': email,
        'password': hash_password(password),
        'created_at': datetime.now()
    }
    st.success("✅ Registration successful! Please login.")
    st.balloons()
    return True

def login_user(username, password):
    if username in st.session_state.users:
        hashed = hash_password(password)
        if st.session_state.users[username]['password'] == hashed:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"✅ Welcome {username}!")
            st.balloons()
            return True
    st.error("❌ Invalid username or password")
    return False

def get_user_count():
    return len(st.session_state.users)

# -------------------------------
# App UI
# -------------------------------
def main():
    st.markdown("<h1 style='text-align: center; color: #667eea;'>🔐 Secure Auth</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Login or Register to Continue</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 Navigation")
        mode = st.radio("Choose an option:", ["🔑 Login", "📝 Register"], key="auth_mode_radio")
        
        # Stats
        st.markdown("---")
        st.markdown("### 📊 Stats")
        user_count = get_user_count()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Users", user_count)
        with col2:
            st.metric("Status", "Online" if st.session_state.logged_in else "Offline")

    # If logged in, show dashboard pages
    if st.session_state.logged_in:
        # Navigation buttons
        col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
        with col1:
            if st.button("🏠 Home", key="nav_home"): st.session_state.page="home"
        with col2:
            if st.button("👤 Profile", key="nav_profile"): st.session_state.page="profile"
        with col3:
            if st.button("📊 Dashboard", key="nav_dashboard"): st.session_state.page="dashboard"
        with col4:
            if st.button("⚙️ Settings", key="nav_settings"): st.session_state.page="settings"
        with col5:
            if st.button("🚪 Logout", key="logout_btn"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.success("✅ Logged out successfully!")
                time.sleep(1)
                st.experimental_rerun()

        # Pages
        if st.session_state.page == "home":
            st.markdown(f"<h2>Welcome Back, {st.session_state.username} 👋</h2>", unsafe_allow_html=True)
            st.balloons()
        elif st.session_state.page == "profile":
            st.subheader("👤 User Profile")
            st.text(f"Username: {st.session_state.username}")
            st.text(f"Email: {st.session_state.users[st.session_state.username]['email']}")
            st.text(f"Member Since: {st.session_state.users[st.session_state.username]['created_at'].strftime('%B %d, %Y')}")
        elif st.session_state.page == "dashboard":
            st.subheader("📊 Dashboard")
            st.metric("Total Users", get_user_count())
            st.metric("Your Username", st.session_state.username)
        elif st.session_state.page == "settings":
            st.subheader("⚙️ Settings")
            theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
            st.info(f"Selected theme: {theme}")

    else:
        # Login/Register forms
        if mode == "🔑 Login":
            st.subheader("🔑 User Login")
            with st.form("login_form", clear_on_submit=True):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_btn = st.form_submit_button("Login")
            if submit_btn:
                login_user(username, password)

        else:  # Register
            st.subheader("📝 Create New Account")
            with st.form("register_form", clear_on_submit=True):
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit_btn = st.form_submit_button("Register")
            if submit_btn:
                register_user(username, email, password, confirm_password)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center; color:gray;'>🔐 Secure Authentication System | Built with Streamlit</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
