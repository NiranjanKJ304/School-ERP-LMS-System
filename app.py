import streamlit as st
from config.settings import configure_page
from utils.data_manager import init_directories
from utils.auth import init_users, init_session_state, show_login_page
from modules.admin.dashboard import show_admin_dashboard
from modules.teacher.dashboard import show_teacher_dashboard
from modules.student.dashboard import show_student_dashboard

def main():
    # Configure page
    configure_page()
    
    # Initialize directories and session state
    init_directories()
    init_users()
    init_session_state()
    
    # Route based on login status
    if not st.session_state.logged_in:
        show_login_page()
    else:
        # Route based on role
        if st.session_state.role == "Admin":
            show_admin_dashboard()
        elif st.session_state.role == "Teacher":
            show_teacher_dashboard()
        elif st.session_state.role == "Student":
            show_student_dashboard()

if __name__ == "__main__":
    main()