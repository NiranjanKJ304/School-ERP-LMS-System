import streamlit as st
import pandas as pd
from datetime import date
from config.settings import CLASSES, SECTIONS, SUBJECTS_1_10
from utils.data_manager import load_dataframe, save_dataframe
from utils.auth import load_users, save_users, hash_password

def manage_teachers():
    st.header("👨‍🏫 Teacher Management")
    
    tab1, tab2 = st.tabs(["➕ Add Teacher", "📋 View Teachers"])
    
    with tab1:
        add_teacher()
    
    with tab2:
        view_teachers()

def add_teacher():
    st.subheader("Add New Teacher")
    
    col1, col2 = st.columns(2)
    
    with col1:
        teacher_name = st.text_input("Teacher Name*")
        employee_id = st.text_input("Employee ID*")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
    
    with col2:
        qualification = st.text_input("Qualification")
        experience = st.number_input("Years of Experience", min_value=0, step=1)
        subject_specialization = st.text_input("Subject Specialization")
    
    st.markdown("#### Assign Classes & Subjects")
    assigned_classes = st.multiselect("Assign Classes", CLASSES)
    assigned_sections = st.multiselect("Assign Sections", SECTIONS)
    
    all_subjects = SUBJECTS_1_10 + ['Physics', 'Chemistry', 'Biology', 
                                     'Computer Science', 'Accountancy', 'Commerce',
                                     'Economics', 'Business Maths', 'History', 
                                     'Geography', 'Political Science']
    assigned_subjects = st.multiselect("Assign Subjects", all_subjects)
    
    if st.button("➕ Add Teacher"):
        if teacher_name and employee_id:
            teachers_df = load_dataframe('data/teachers/all_teachers')
            
            new_teacher = {
                'Employee_ID': employee_id,
                'Name': teacher_name,
                'Phone': phone,
                'Email': email,
                'Qualification': qualification,
                'Experience': experience,
                'Specialization': subject_specialization,
                'Assigned_Classes': ', '.join(map(str, assigned_classes)),
                'Assigned_Sections': ', '.join(assigned_sections),
                'Assigned_Subjects': ', '.join(assigned_subjects),
                'Join_Date': str(date.today())
            }
            
            if teachers_df.empty:
                teachers_df = pd.DataFrame([new_teacher])
            else:
                teachers_df = pd.concat([teachers_df, pd.DataFrame([new_teacher])], ignore_index=True)
            
            save_dataframe(teachers_df, 'data/teachers/all_teachers')
            
            # Create user account
            users = load_users()
            username = f"teacher_{employee_id}".lower()
            users[username] = {
                'password': hash_password('teacher123'),
                'role': 'Teacher',
                'name': teacher_name,
                'employee_id': employee_id
            }
            save_users(users)
            
            st.success(f"✅ Teacher added successfully! Username: {username}, Password: teacher123")
        else:
            st.error("❌ Please fill all required fields")

def view_teachers():
    st.subheader("All Teachers")
    teachers_df = load_dataframe('data/teachers/all_teachers')
    
    if not teachers_df.empty:
        st.dataframe(teachers_df, use_container_width=True)
        st.info(f"📊 Total Teachers: {len(teachers_df)}")
    else:
        st.info("No teachers found.")