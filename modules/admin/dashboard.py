import streamlit as st
from utils.auth import logout
from modules.admin.student_management import manage_students
from modules.admin.teacher_management import manage_teachers
from modules.admin.data_export import export_data
from utils.data_manager import load_dataframe
import plotly.express as px

def show_admin_dashboard():
    st.title("👨‍💼 Admin Dashboard")
    st.markdown(f"**Welcome, {st.session_state.user_data['name']}**")
    
    with st.sidebar:
        st.markdown("### 📋 Admin Menu")
        menu = st.radio(
            "Navigate to:",
            ["Dashboard Overview", "Manage Students", "Manage Teachers", 
             "Class Structure", "Data Export", "User Management"]
        )
        
        st.markdown("---")
        if st.button("🚪 Logout"):
            logout()
    
    if menu == "Dashboard Overview":
        show_admin_overview()
    elif menu == "Manage Students":
        manage_students()
    elif menu == "Manage Teachers":
        manage_teachers()
    elif menu == "Class Structure":
        show_class_structure()
    elif menu == "Data Export":
        export_data()
    elif menu == "User Management":
        show_user_management()

def show_admin_overview():
    st.header("📊 System Overview")
    
    students_df = load_dataframe('data/students/all_students')
    teachers_df = load_dataframe('data/teachers/all_teachers')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👨‍🎓 Total Students", len(students_df) if not students_df.empty else 0)
    with col2:
        st.metric("👨‍🏫 Total Teachers", len(teachers_df) if not teachers_df.empty else 0)
    with col3:
        st.metric("📚 Classes", 12)
    with col4:
        from config.settings import SECTIONS
        st.metric("📂 Sections", len(SECTIONS))
    
    st.markdown("---")
    
    if not students_df.empty:
        st.subheader("📈 Class-wise Student Distribution")
        class_dist = students_df.groupby('Class').size().reset_index(name='Count')
        fig = px.bar(class_dist, x='Class', y='Count', 
                     title="Students per Class",
                     color='Count',
                     color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

def show_class_structure():
    st.header("📚 Class Structure Management")
    
    from config.settings import SUBJECTS_1_10, GROUP_SUBJECTS
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Classes 1-10")
        st.write("**Fixed Subjects:**")
        for subject in SUBJECTS_1_10:
            st.write(f"• {subject}")
    
    with col2:
        st.markdown("#### Classes 11-12")
        st.write("**Group-based Subjects:**")
        for group, subjects in GROUP_SUBJECTS.items():
            with st.expander(f"📖 {group}"):
                for subject in subjects:
                    st.write(f"• {subject}")

def show_user_management():
    st.header("👥 User Management")
    
    from utils.auth import load_users
    import pandas as pd
    
    users = load_users()
    
    users_data = []
    for username, user_info in users.items():
        users_data.append({
            'Username': username,
            'Name': user_info.get('name', 'N/A'),
            'Role': user_info['role']
        })
    
    if users_data:
        users_df = pd.DataFrame(users_data)
        st.dataframe(users_df, use_container_width=True)
    
    st.markdown("---")
    st.info("💡 User accounts are automatically created when adding students/teachers")