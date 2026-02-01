import streamlit as st
import plotly.express as px
from utils.data_manager import load_dataframe
from utils.helpers import calculate_grade

def show_performance_analytics():
    st.header("📊 Performance Analytics")
    
    marks_df = load_dataframe('data/marks/all_marks')
    
    if marks_df.empty:
        st.info("No marks data available yet.")
        return
    
    tab1, tab2, tab3 = st.tabs(["Class Performance", "Subject Analysis", "Student Performance"])
    
    with tab1:
        show_class_performance(marks_df)
    
    with tab2:
        show_subject_analysis(marks_df)
    
    with tab3:
        show_student_performance(marks_df)

def show_class_performance(marks_df):
    st.subheader("Class-wise Performance")
    
    col1, col2 = st.columns(2)
    with col1:
        filter_class = st.selectbox("Select Class", marks_df['Class'].unique())
    with col2:
        filter_section = st.selectbox("Select Section", marks_df['Section'].unique())
    
    class_marks = marks_df[
        (marks_df['Class'] == filter_class) & 
        (marks_df['Section'] == filter_section)
    ]
    
    if not class_marks.empty:
        subject_avg = class_marks.groupby('Subject')['Marks'].mean().reset_index()
        
        fig = px.bar(subject_avg, x='Subject', y='Marks',
                    title=f"Average Marks by Subject - Class {filter_class}{filter_section}",
                    color='Marks',
                    color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            grade_dist = class_marks['Grade'].value_counts().reset_index()
            grade_dist.columns = ['Grade', 'Count']
            
            fig2 = px.pie(grade_dist, values='Count', names='Grade',
                         title="Grade Distribution")
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            result_dist = class_marks['Result'].value_counts().reset_index()
            result_dist.columns = ['Result', 'Count']
            
            fig3 = px.pie(result_dist, values='Count', names='Result',
                         title="Pass vs Fail",
                         color='Result',
                         color_discrete_map={'Pass': 'green', 'Fail': 'red'})
            st.plotly_chart(fig3, use_container_width=True)

def show_subject_analysis(marks_df):
    st.subheader("Subject-wise Analysis")
    
    selected_subject = st.selectbox("Select Subject", marks_df['Subject'].unique())
    subject_marks = marks_df[marks_df['Subject'] == selected_subject]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Marks", f"{subject_marks['Marks'].mean():.2f}")
    with col2:
        st.metric("Highest Marks", subject_marks['Marks'].max())
    with col3:
        st.metric("Lowest Marks", subject_marks['Marks'].min())
    
    fig = px.histogram(subject_marks, x='Marks', nbins=20,
                      title=f"Marks Distribution - {selected_subject}")
    st.plotly_chart(fig, use_container_width=True)

def show_student_performance(marks_df):
    st.subheader("Individual Student Performance")
    
    students = marks_df[['Roll_No', 'Name']].drop_duplicates()
    student_list = [f"{row['Roll_No']} - {row['Name']}" for _, row in students.iterrows()]
    
    selected_student = st.selectbox("Select Student", student_list)
    
    if selected_student:
        roll_no = int(selected_student.split(' - ')[0])
        student_marks = marks_df[marks_df['Roll_No'] == roll_no]
        
        if not student_marks.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Subjects", len(student_marks))
            with col2:
                avg_marks = student_marks['Marks'].mean()
                st.metric("Average Marks", f"{avg_marks:.2f}")
            with col3:
                overall_grade = calculate_grade(avg_marks)
                st.metric("Overall Grade", overall_grade)
            
            fig = px.bar(student_marks, x='Subject', y='Marks',
                        title="Subject-wise Performance",
                        color='Marks',
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(student_marks[['Subject', 'Exam_Type', 'Marks', 'Grade', 'Result']], 
                       use_container_width=True)