import streamlit as st
from utils.auth import logout
from modules.teacher.marks_entry import enter_student_marks
from modules.teacher.analytics import show_performance_analytics
from modules.teacher.materials import manage_study_materials
from modules.teacher.assignments import manage_assignments
from utils.data_manager import load_dataframe
from pathlib import Path

def show_teacher_dashboard():
    st.title("👨‍🏫 Teacher Dashboard")
    st.markdown(f"**Welcome, {st.session_state.user_data['name']}**")
    
    with st.sidebar:
        st.markdown("### 📋 Teacher Menu")
        menu = st.radio(
            "Navigate to:",
            ["Dashboard", "Enter Marks", "Performance Analytics", 
             "Study Materials", "Assignments", "View Students"]
        )
        
        st.markdown("---")
        if st.button("🚪 Logout"):
            logout()
    
    if menu == "Dashboard":
        show_teacher_overview()
    elif menu == "Enter Marks":
        enter_student_marks()
    elif menu == "Performance Analytics":
        show_performance_analytics()
    elif menu == "Study Materials":
        manage_study_materials()
    elif menu == "Assignments":
        manage_assignments()
    elif menu == "View Students":
        view_students_teacher()

def show_teacher_overview():
    st.header("📊 Dashboard Overview")
    
    students_df = load_dataframe('data/students/all_students')
    marks_df = load_dataframe('data/marks/all_marks')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👨‍🎓 Total Students", len(students_df) if not students_df.empty else 0)
    with col2:
        st.metric("📝 Marks Entered", len(marks_df) if not marks_df.empty else 0)
    with col3:
        assignments_path = Path('data/assignments')
        assignment_count = len(list(assignments_path.glob('*.csv'))) if assignments_path.exists() else 0
        st.metric("📚 Assignments", assignment_count)
    
    st.markdown("---")
    st.info("👈 Use the sidebar menu to navigate through different sections")

def view_students_teacher():
    st.header("👨‍🎓 View Students")
    
    from config.settings import CLASSES, SECTIONS
    
    students_df = load_dataframe('data/students/all_students')
    
    if not students_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            filter_class = st.selectbox("Filter by Class", ["All"] + CLASSES)
        with col2:
            filter_section = st.selectbox("Filter by Section", ["All"] + SECTIONS)
        
        filtered_df = students_df.copy()
        if filter_class != "All":
            filtered_df = filtered_df[filtered_df['Class'] == filter_class]
        if filter_section != "All":
            filtered_df = filtered_df[filtered_df['Section'] == filter_section]
        
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("No students found.")