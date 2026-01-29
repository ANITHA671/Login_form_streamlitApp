import streamlit as st
import hashlib

# -------------------------------
# Initialize session state
# -------------------------------
if "users" not in st.session_state:
    st.session_state.users = {}  # stores users as {username: hashed_password}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# -------------------------------
# Hashing function
# -------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------------------
# Register function
# -------------------------------
def register_user(username, password):
    if username in st.session_state.users:
        st.error("❌ Username already exists")
        return False
    st.session_state.users[username] = hash_password(password)
    st.success("✅ Registration successful! Please login.")
    return True

# -------------------------------
# Login function
# -------------------------------
def login_user(username, password):
    hashed = hash_password(password)
    if username in st.session_state.users and st.session_state.users[username] == hashed:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.success(f"✅ Welcome {username}!")
        return True
    else:
        st.error("❌ Invalid username or password")
        return False

# -------------------------------
# App UI
# -------------------------------
st.title("Student CRUD Application")
st.subheader("Manage student records efficiently")

if not st.session_state.logged_in:
    mode = st.radio("Choose action", ["Login", "Register"])
    
    if mode == "Register":
        st.subheader("📝 Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            if username and password:
                register_user(username, password)
            else:
                st.warning("⚠️ Please fill all fields")
    
    else:
        st.subheader("🔑 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username and password:
                login_user(username, password)
            else:
                st.warning("⚠️ Please fill all fields")

else:
    st.success(f"Logged in as: {st.session_state.current_user}")

    # -------------------------------
    # Your Streamlit Dashboard UI
    # -------------------------------
    st.header("📊 Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Students", 120)
    with col2:
        st.metric("Courses", 6)
    with col3:
        st.metric("Active", 98)
    
    st.divider()
    
    # Add Student Form
    with st.form("add_student"):
        st.subheader("Add Student")
        name = st.text_input("Student Name")
        age = st.number_input("Age", 0, 100)
        course = st.selectbox("Course", ["Python","Java","C++"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success(f"Added {name}, Age: {age}, Course: {course}")
    
    # Example Table
    data = {
        "Name": ["Anurag","Bharath","Chitra"],
        "Age": [23,22,24],
        "Course": ["Python","Java","C++"]
    }
    st.table(data)
    
    # Other UI examples
    st.text_input("Feedback")
    st.slider("Select Age", 0, 100)
    
    # Logout
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.experimental_rerun()
