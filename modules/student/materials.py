import streamlit as st
import os
from utils.data_manager import load_dataframe

def view_study_materials():
    st.header("📚 Study Materials")
    
    user_data = st.session_state.user_data
    materials_df = load_dataframe('data/materials/all_materials')
    
    if materials_df.empty:
        st.info("No study materials available yet.")
        return
    
    student_materials = materials_df[
        (materials_df['Class'] == user_data['class']) &
        (materials_df['Visible'] == True)
    ]
    
    student_materials = student_materials[
        student_materials['Sections'].str.contains(user_data['section'])
    ]
    
    if student_materials.empty:
        st.info("No materials available for your class.")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        subjects = ["All"] + list(student_materials['Subject'].unique())
        filter_subject = st.selectbox("Filter by Subject", subjects)
    with col2:
        chapters = ["All"] + list(student_materials['Chapter'].dropna().unique())
        filter_chapter = st.selectbox("Filter by Chapter", chapters)
    
    filtered_materials = student_materials.copy()
    if filter_subject != "All":
        filtered_materials = filtered_materials[filtered_materials['Subject'] == filter_subject]
    if filter_chapter != "All":
        filtered_materials = filtered_materials[filtered_materials['Chapter'] == filter_chapter]
    
    st.markdown("---")
    
    # Display materials
    for idx, material in filtered_materials.iterrows():
        with st.expander(f"📄 {material['Title']} - {material['Subject']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Subject:** {material['Subject']}")
                st.write(f"**Chapter:** {material.get('Chapter', 'N/A')}")
                st.write(f"**Type:** {material['Type']}")
                st.write(f"**Description:** {material.get('Description', 'N/A')}")
                st.write(f"**Uploaded:** {material['Upload_Date']}")
            
            with col2:
                if material['File_Path'] != "N/A" and os.path.exists(material['File_Path']):
                    with open(material['File_Path'], "rb") as file:
                        st.download_button(
                            label="📥 Download",
                            data=file,
                            file_name=os.path.basename(material['File_Path']),
                            mime="application/octet-stream",
                            key=f"download_{idx}"
                        )