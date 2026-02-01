import streamlit as st
import pandas as pd
from datetime import date
from config.settings import CLASSES, SECTIONS
from utils.data_manager import load_dataframe, save_dataframe

def manage_assignments():
    st.header("📝 Assignment Management")
    
    tab1, tab2, tab3 = st.tabs(["➕ Create Assignment", "📋 View Assignments", "✅ Grade Submissions"])
    
    with tab1:
        create_assignment()
    
    with tab2:
        view_assignments()
    
    with tab3:
        grade_submissions()

def create_assignment():
    st.subheader("Create New Assignment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        assign_title = st.text_input("Assignment Title*")
        assign_class = st.selectbox("Class*", CLASSES, key="assign_class")
        assign_section = st.selectbox("Section*", SECTIONS, key="assign_section")
    
    with col2:
        assign_subject = st.text_input("Subject*")
        assign_max_marks = st.number_input("Maximum Marks*", min_value=1, value=100)
        assign_due_date = st.date_input("Due Date*")
    
    assign_description = st.text_area("Assignment Description*")
    
    attach_file = st.file_uploader("Attach File (Optional)", 
                                   type=['pdf', 'doc', 'docx', 'txt'])
    
    if st.button("➕ Create Assignment"):
        if assign_title and assign_class and assign_section and assign_subject and assign_description:
            assignments_df = load_dataframe('data/assignments/all_assignments')
            
            file_path = "N/A"
            if attach_file:
                save_path = f"data/assignments/{attach_file.name}"
                with open(save_path, "wb") as f:
                    f.write(attach_file.getbuffer())
                file_path = save_path
            
            assignment_id = f"ASSIGN_{len(assignments_df) + 1}_{date.today().strftime('%Y%m%d')}"
            
            new_assignment = {
                'Assignment_ID': assignment_id,
                'Title': assign_title,
                'Class': assign_class,
                'Section': assign_section,
                'Subject': assign_subject,
                'Description': assign_description,
                'Max_Marks': assign_max_marks,
                'Due_Date': str(assign_due_date),
                'File_Path': file_path,
                'Created_Date': str(date.today()),
                'Created_By': st.session_state.user_data['name']
            }
            
            if assignments_df.empty:
                assignments_df = pd.DataFrame([new_assignment])
            else:
                assignments_df = pd.concat([assignments_df, pd.DataFrame([new_assignment])], 
                                         ignore_index=True)
            
            save_dataframe(assignments_df, 'data/assignments/all_assignments')
            st.success(f"✅ Assignment created! ID: {assignment_id}")
        else:
            st.error("❌ Please fill all required fields")

def view_assignments():
    st.subheader("All Assignments")
    
    assignments_df = load_dataframe('data/assignments/all_assignments')
    
    if not assignments_df.empty:
        st.dataframe(assignments_df, use_container_width=True)
    else:
        st.info("No assignments created yet.")

def grade_submissions():
    st.subheader("Grade Submissions")
    
    submissions_df = load_dataframe('data/submissions/all_submissions')
    
    if not submissions_df.empty:
        assignments_df = load_dataframe('data/assignments/all_assignments')
        if not assignments_df.empty:
            assign_list = assignments_df['Assignment_ID'].tolist()
            selected_assign = st.selectbox("Select Assignment", assign_list)
            
            assign_submissions = submissions_df[submissions_df['Assignment_ID'] == selected_assign]
            
            if not assign_submissions.empty:
                for idx, submission in assign_submissions.iterrows():
                    with st.expander(f"📄 {submission['Student_Name']} - Roll: {submission['Roll_No']}"):
                        st.write(f"**Submitted:** {submission['Submission_Date']}")
                        st.write(f"**File:** {submission['File_Path']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            marks = st.number_input(
                                "Marks",
                                min_value=0,
                                max_value=int(submission['Max_Marks']),
                                value=int(submission.get('Marks_Obtained', 0)),
                                key=f"marks_{idx}"
                            )
                        with col2:
                            remarks = st.text_input(
                                "Remarks",
                                value=submission.get('Remarks', ''),
                                key=f"remarks_{idx}"
                            )
                        
                        if st.button(f"💾 Save Grade", key=f"save_{idx}"):
                            submissions_df.at[idx, 'Marks_Obtained'] = marks
                            submissions_df.at[idx, 'Remarks'] = remarks
                            submissions_df.at[idx, 'Graded'] = True
                            submissions_df.at[idx, 'Graded_Date'] = str(date.today())
                            
                            save_dataframe(submissions_df, 'data/submissions/all_submissions')
                            st.success("✅ Grade saved!")
            else:
                st.info("No submissions for this assignment yet.")
    else:
        st.info("No submissions yet.")