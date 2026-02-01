import streamlit as st
import hashlib
import json
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_users():
    users_file = 'data/users/users.json'
    if not os.path.exists(users_file):
        default_users = {
            'admin': {
                'password': hash_password('admin123'),
                'role': 'Admin',
                'name': 'System Administrator'
            },
            'teacher1': {
                'password': hash_password('teacher123'),
                'role': 'Teacher',
                'name': 'Demo Teacher'
            },
            'student1': {
                'password': hash_password('student123'),
                'role': 'Student',
                'name': 'Demo Student',
                'class': 10,
                'section': 'A',
                'roll_no': 1
            }
        }
        with open(users_file, 'w') as f:
            json.dump(default_users, f, indent=4)

def load_users():
    users_file = 'data/users/users.json'
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    users_file = 'data/users/users.json'
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

def authenticate_user(username, password, role):
    users = load_users()
    if username in users:
        user = users[username]
        if user['password'] == hash_password(password) and user['role'] == role:
            return True, user
    return False, None

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None

def show_login_page():
    st.markdown("<h1 style='text-align: center;'>🎓 School Management System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Complete ERP + LMS Solution</h3>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login to Continue")
        
        role = st.selectbox(
            "Select Your Role",
            ["Admin", "Teacher", "Student"],
            help="Choose your role to access the system"
        )
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.write("")
        
        if st.button("🚀 Login", use_container_width=True):
            if username and password:
                success, user_data = authenticate_user(username, password, role)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = role
                    st.session_state.user_data = user_data
                    st.success(f"✅ Welcome {user_data['name']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials or role mismatch!")
            else:
                st.warning("⚠️ Please enter both username and password")
        
        st.write("")
        st.markdown("---")
        st.info('''
        **Default Credentials:**
        - Admin: admin / admin123
        - Teacher: teacher1 / teacher123
        - Student: student1 / student123
        ''')

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.user_data = None
    st.rerun()