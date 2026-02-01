import streamlit as st
import pandas as pd
from datetime import date
from config.settings import CLASSES, SECTIONS
from utils.data_manager import load_dataframe, save_dataframe
from utils.helpers import get_subjects_for_class, calculate_grade, calculate_result

def enter_student_marks():
    st.header("📝 Enter Student Marks")
    
    students_df = load_dataframe('data/students/all_students')
    
    if students_df.empty:
        st.warning("No students found in the system.")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_class = st.selectbox("Select Class", CLASSES, key="marks_class")
    with col2:
        selected_section = st.selectbox("Select Section", SECTIONS, key="marks_section")
    with col3:
        exam_type = st.selectbox("Exam Type", ["Term 1", "Term 2", "Half Yearly", "Annual"])
    
    class_students = students_df[
        (students_df['Class'] == selected_class) & 
        (students_df['Section'] == selected_section)
    ]
    
    if class_students.empty:
        st.info(f"No students found in Class {selected_class}{selected_section}")
        return
    
    if selected_class in [11, 12]:
        groups = class_students['Group'].unique()
        selected_group = st.selectbox("Select Group", groups)
        subjects = get_subjects_for_class(selected_class, selected_group)
    else:
        subjects = get_subjects_for_class(selected_class)
    
    selected_subject = st.selectbox("Select Subject", subjects)
    
    st.markdown("---")
    st.subheader(f"Enter Marks - {selected_subject}")
    
    marks_df = load_dataframe('data/marks/all_marks')
    marks_data = []
    
    for _, student in class_students.iterrows():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{student['Name']}** (Roll: {student['Roll_No']})")
        
        with col2:
            marks = st.number_input(
                f"Marks",
                min_value=0,
                max_value=100,
                value=0,
                key=f"marks_{student['Roll_No']}",
                label_visibility="collapsed"
            )
        
        with col3:
            grade = calculate_grade(marks)
            st.write(f"Grade: **{grade}**")
        
        marks_data.append({
            'Roll_No': student['Roll_No'],
            'Name': student['Name'],
            'Class': selected_class,
            'Section': selected_section,
            'Subject': selected_subject,
            'Exam_Type': exam_type,
            'Marks': marks,
            'Grade': grade,
            'Result': calculate_result(marks),
            'Date': str(date.today())
        })
    
    if st.button("💾 Save All Marks", use_container_width=True):
        new_marks_df = pd.DataFrame(marks_data)
        
        if marks_df.empty:
            marks_df = new_marks_df
        else:
            marks_df = marks_df[
                ~((marks_df['Class'] == selected_class) & 
                  (marks_df['Section'] == selected_section) & 
                  (marks_df['Subject'] == selected_subject) & 
                  (marks_df['Exam_Type'] == exam_type))
            ]
            marks_df = pd.concat([marks_df, new_marks_df], ignore_index=True)
        
        save_dataframe(marks_df, 'data/marks/all_marks')
        st.success("✅ Marks saved successfully!")