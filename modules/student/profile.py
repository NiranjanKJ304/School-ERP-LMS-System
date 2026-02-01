import streamlit as st
from utils.data_manager import load_dataframe

def show_student_profile():
    st.header("👤 My Profile")
    
    user_data = st.session_state.user_data
    students_df = load_dataframe('data/students/all_students')
    
    if not students_df.empty:
        student = students_df[
            (students_df['Roll_No'] == user_data['roll_no']) &
            (students_df['Class'] == user_data['class']) &
            (students_df['Section'] == user_data['section'])
        ]
        
        if not student.empty:
            student = student.iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Personal Information")
                st.write(f"**Name:** {student['Name']}")
                st.write(f"**Roll Number:** {student['Roll_No']}")
                st.write(f"**Class:** {student['Class']}{student['Section']}")
                if student.get('Group') and student['Group'] != 'N/A':
                    st.write(f"**Group:** {student['Group']}")
                st.write(f"**Gender:** {student.get('Gender', 'N/A')}")
                st.write(f"**DOB:** {student.get('DOB', 'N/A')}")
            
            with col2:
                st.subheader("Contact Information")
                st.write(f"**Email:** {student.get('Email', 'N/A')}")
                st.write(f"**Phone:** {student.get('Phone', 'N/A')}")
                st.write(f"**Parent/Guardian:** {student.get('Parent_Name', 'N/A')}")
                st.write(f"**Address:** {student.get('Address', 'N/A')}")
        else:
            st.warning("Profile information not found.")
    else:
        st.warning("No student data available.")