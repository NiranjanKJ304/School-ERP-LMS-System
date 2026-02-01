import streamlit as st
import pandas as pd
import os
from datetime import date
from utils.data_manager import load_dataframe, save_dataframe

def student_assignments():
    st.header("📝 My Assignments")
    
    user_data = st.session_state.user_data
    
    tab1, tab2 = st.tabs(["📋 View Assignments", "📤 My Submissions"])
    
    with tab1:
        view_assignments(user_data)
    
    with tab2:
        view_submissions(user_data)

def view_assignments(user_data):
    assignments_df = load_dataframe('data/assignments/all_assignments')
    
    if assignments_df.empty:
        st.info("No assignments available.")
        return
    
    student_assignments = assignments_df[
        (assignments_df['Class'] == user_data['class']) &
        (assignments_df['Section'] == user_data['section'])
    ]
    
    if student_assignments.empty:
        st.info("No assignments for your class.")
        return
    
    for idx, assignment in student_assignments.iterrows():
        with st.expander(f"📝 {assignment['Title']} - {assignment['Subject']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Subject:** {assignment['Subject']}")
                st.write(f"**Description:** {assignment['Description']}")
                st.write(f"**Maximum Marks:** {assignment['Max_Marks']}")
                st.write(f"**Due Date:** {assignment['Due_Date']}")
                st.write(f"**Created:** {assignment['Created_Date']}")
            
            with col2:
                submissions_df = load_dataframe('data/submissions/all_submissions')
                
                already_submitted = False
                if not submissions_df.empty:
                    already_submitted = not submissions_df[
                        (submissions_df['Assignment_ID'] == assignment['Assignment_ID']) &
                        (submissions_df['Roll_No'] == user_data['roll_no'])
                    ].empty
                
                if already_submitted:
                    st.success("✅ Submitted")
                else:
                    st.warning("⏳ Pending")
            
            if not already_submitted:
                st.markdown("#### Submit Assignment")
                upload_file = st.file_uploader(
                    "Upload your work",
                    type=['pdf', 'doc', 'docx', 'txt', 'zip'],
                    key=f"upload_{assignment['Assignment_ID']}"
                )
                
                if st.button(f"📤 Submit", key=f"submit_{assignment['Assignment_ID']}"):
                    if upload_file:
                        submissions_df = load_dataframe('data/submissions/all_submissions')
                        
                        file_path = f"data/submissions/{user_data['roll_no']}_{assignment['Assignment_ID']}_{upload_file.name}"
                        with open(file_path, "wb") as f:
                            f.write(upload_file.getbuffer())
                        
                        new_submission = {
                            'Assignment_ID': assignment['Assignment_ID'],
                            'Roll_No': user_data['roll_no'],
                            'Student_Name': user_data['name'],
                            'Class': user_data['class'],
                            'Section': user_data['section'],
                            'File_Path': file_path,
                            'Submission_Date': str(date.today()),
                            'Max_Marks': assignment['Max_Marks'],
                            'Marks_Obtained': 0,
                            'Graded': False,
                            'Remarks': ''
                        }
                        
                        if submissions_df.empty:
                            submissions_df = pd.DataFrame([new_submission])
                        else:
                            submissions_df = pd.concat([submissions_df, pd.DataFrame([new_submission])], 
                                                     ignore_index=True)
                        
                        save_dataframe(submissions_df, 'data/submissions/all_submissions')
                        st.success("✅ Assignment submitted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please upload a file")

def view_submissions(user_data):
    st.subheader("My Submissions")
    
    submissions_df = load_dataframe('data/submissions/all_submissions')
    
    if submissions_df.empty:
        st.info("No submissions yet.")
        return
    
    student_submissions = submissions_df[submissions_df['Roll_No'] == user_data['roll_no']]
    
    if student_submissions.empty:
        st.info("You haven't submitted any assignments yet.")
        return
    
    for idx, submission in student_submissions.iterrows():
        with st.expander(f"📄 {submission['Assignment_ID']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Submitted:** {submission['Submission_Date']}")
                st.write(f"**File:** {os.path.basename(submission['File_Path'])}")
            
            with col2:
                st.write(f"**Max Marks:** {submission['Max_Marks']}")
                if submission['Graded']:
                    st.write(f"**Marks Obtained:** {submission['Marks_Obtained']}")
                else:
                    st.write("**Status:** Not graded yet")
            
            with col3:
                if submission['Graded']:
                    from utils.helpers import calculate_grade
                    percentage = (submission['Marks_Obtained'] / submission['Max_Marks']) * 100
                    grade = calculate_grade(percentage)
                    st.metric("Grade", grade)
            
            if submission.get('Remarks'):
                st.info(f"**Teacher's Remarks:** {submission['Remarks']}")