import streamlit as st
import pandas as pd
from datetime import date
from config.settings import CLASSES, SECTIONS, GROUPS_11_12
from utils.data_manager import load_dataframe, save_dataframe
from utils.auth import load_users, save_users, hash_password

def manage_students():
    st.header("👨‍🎓 Student Management")
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Student", "📋 View Students", "✏️ Edit Student"])
    
    with tab1:
        add_student()
    
    with tab2:
        view_students()
    
    with tab3:
        edit_student()

def add_student():
    st.subheader("Add New Student")
    
    col1, col2 = st.columns(2)
    
    with col1:
        student_name = st.text_input("Student Name*")
        roll_no = st.number_input("Roll Number*", min_value=1, step=1)
        class_num = st.selectbox("Class*", CLASSES)
        section = st.selectbox("Section*", SECTIONS)
    
    with col2:
        dob = st.date_input("Date of Birth")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
    
    group = None
    if class_num in [11, 12]:
        group = st.selectbox("Select Group*", GROUPS_11_12)
    
    parent_name = st.text_input("Parent/Guardian Name")
    address = st.text_area("Address")
    
    if st.button("➕ Add Student"):
        if student_name and roll_no and class_num and section:
            students_df = load_dataframe('data/students/all_students')
            
            new_student = {
                'Roll_No': roll_no,
                'Name': student_name,
                'Class': class_num,
                'Section': section,
                'Group': group if class_num in [11, 12] else 'N/A',
                'DOB': str(dob),
                'Gender': gender,
                'Phone': phone,
                'Email': email,
                'Parent_Name': parent_name,
                'Address': address,
                'Admission_Date': str(date.today())
            }
            
            if students_df.empty:
                students_df = pd.DataFrame([new_student])
            else:
                students_df = pd.concat([students_df, pd.DataFrame([new_student])], ignore_index=True)
            
            save_dataframe(students_df, 'data/students/all_students')
            
            # Create user account
            users = load_users()
            username = f"student_{roll_no}_{class_num}{section}".lower()
            users[username] = {
                'password': hash_password('student123'),
                'role': 'Student',
                'name': student_name,
                'class': class_num,
                'section': section,
                'roll_no': roll_no
            }
            save_users(users)
            
            st.success(f"✅ Student added successfully! Username: {username}, Password: student123")
        else:
            st.error("❌ Please fill all required fields marked with *")

def view_students():
    st.subheader("All Students")
    
    students_df = load_dataframe('data/students/all_students')
    
    if not students_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            filter_class = st.selectbox("Filter by Class", ["All"] + CLASSES, key="view_class")
        with col2:
            filter_section = st.selectbox("Filter by Section", ["All"] + SECTIONS, key="view_section")
        
        filtered_df = students_df.copy()
        if filter_class != "All":
            filtered_df = filtered_df[filtered_df['Class'] == filter_class]
        if filter_section != "All":
            filtered_df = filtered_df[filtered_df['Section'] == filter_section]
        
        st.dataframe(filtered_df, use_container_width=True)
        st.info(f"📊 Showing {len(filtered_df)} students")
    else:
        st.info("No students found. Add students to see them here.")

def edit_student():
    st.subheader("Edit Student Information")
    
    students_df = load_dataframe('data/students/all_students')
    
    if not students_df.empty:
        student_list = [f"{row['Roll_No']} - {row['Name']} (Class {row['Class']}{row['Section']})" 
                       for _, row in students_df.iterrows()]
        selected = st.selectbox("Select Student", student_list)
        
        if selected:
            idx = student_list.index(selected)
            student = students_df.iloc[idx]
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Student Name", value=student['Name'])
                new_phone = st.text_input("Phone Number", value=student.get('Phone', ''))
            
            with col2:
                new_email = st.text_input("Email", value=student.get('Email', ''))
                new_parent = st.text_input("Parent Name", value=student.get('Parent_Name', ''))
            
            new_address = st.text_area("Address", value=student.get('Address', ''))
            
            if st.button("💾 Update Student"):
                students_df.at[idx, 'Name'] = new_name
                students_df.at[idx, 'Phone'] = new_phone
                students_df.at[idx, 'Email'] = new_email
                students_df.at[idx, 'Parent_Name'] = new_parent
                students_df.at[idx, 'Address'] = new_address
                
                save_dataframe(students_df, 'data/students/all_students')
                st.success("✅ Student information updated successfully!")
    else:
        st.info("No students found.")