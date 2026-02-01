import streamlit as st
from utils.auth import logout
from modules.student.profile import show_student_profile
from modules.student.performance import show_student_performance
from modules.student.materials import view_study_materials
from modules.student.assignments import student_assignments

def show_student_dashboard():
    st.title("👨‍🎓 Student Dashboard")
    st.markdown(f"**Welcome, {st.session_state.user_data['name']}**")
    
    with st.sidebar:
        st.markdown("### 📋 Student Menu")
        menu = st.radio(
            "Navigate to:",
            ["Profile", "My Performance", "Study Materials", "Assignments"]
        )
        
        st.markdown("---")
        if st.button("🚪 Logout"):
            logout()
    
    if menu == "Profile":
        show_student_profile()
    elif menu == "My Performance":
        show_student_performance()
    elif menu == "Study Materials":
        view_study_materials()
    elif menu == "Assignments":
        student_assignments()