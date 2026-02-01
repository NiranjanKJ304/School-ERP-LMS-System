import streamlit as st
import plotly.express as px
from utils.data_manager import load_dataframe
from utils.helpers import calculate_grade

def show_student_performance():
    st.header("📊 My Performance")
    
    user_data = st.session_state.user_data
    marks_df = load_dataframe('data/marks/all_marks')
    
    if marks_df.empty:
        st.info("No performance data available yet.")
        return
    
    student_marks = marks_df[marks_df['Roll_No'] == user_data['roll_no']]
    
    if student_marks.empty:
        st.info("No marks recorded yet.")
        return
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Subjects", len(student_marks['Subject'].unique()))
    with col2:
        avg_marks = student_marks['Marks'].mean()
        st.metric("Average Marks", f"{avg_marks:.2f}")
    with col3:
        overall_grade = calculate_grade(avg_marks)
        st.metric("Overall Grade", overall_grade)
    with col4:
        pass_count = len(student_marks[student_marks['Result'] == 'Pass'])
        st.metric("Passed Subjects", f"{pass_count}/{len(student_marks)}")
    
    st.markdown("---")
    
    # Subject-wise performance chart
    st.subheader("📈 Subject-wise Performance")
    
    subject_avg = student_marks.groupby('Subject')['Marks'].mean().reset_index()
    
    fig = px.bar(subject_avg, x='Subject', y='Marks',
                title="My Marks by Subject",
                color='Marks',
                color_continuous_scale='Greens',
                text='Marks')
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed marks table
    st.subheader("📋 Detailed Marks")
    display_marks = student_marks[['Subject', 'Exam_Type', 'Marks', 'Grade', 'Result', 'Date']]
    st.dataframe(display_marks, use_container_width=True)
    
    # Grade distribution
    col1, col2 = st.columns(2)
    
    with col1:
        grade_counts = student_marks['Grade'].value_counts().reset_index()
        grade_counts.columns = ['Grade', 'Count']
        
        fig2 = px.pie(grade_counts, values='Count', names='Grade',
                     title="My Grade Distribution")
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        if len(student_marks['Exam_Type'].unique()) > 1:
            exam_avg = student_marks.groupby('Exam_Type')['Marks'].mean().reset_index()
            
            fig3 = px.line(exam_avg, x='Exam_Type', y='Marks',
                          title="Performance Trend",
                          markers=True)
            st.plotly_chart(fig3, use_container_width=True)