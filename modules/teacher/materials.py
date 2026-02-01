import streamlit as st
import pandas as pd
from datetime import date
from config.settings import CLASSES, SECTIONS
from utils.data_manager import load_dataframe, save_dataframe

def manage_study_materials():
    st.header("📚 Study Materials Management")
    
    tab1, tab2 = st.tabs(["📤 Upload Material", "📋 View Materials"])
    
    with tab1:
        upload_material()
    
    with tab2:
        view_materials()

def upload_material():
    st.subheader("Upload New Study Material")
    
    col1, col2 = st.columns(2)
    
    with col1:
        material_title = st.text_input("Material Title*")
        material_class = st.selectbox("Class*", CLASSES, key="mat_class")
        material_section = st.multiselect("Section(s)*", SECTIONS)
    
    with col2:
        material_subject = st.text_input("Subject*")
        material_chapter = st.text_input("Chapter/Topic")
        material_type = st.selectbox("Material Type", 
                                    ["PDF", "PPT", "DOC", "Video Link", "Image", "Other"])
    
    material_description = st.text_area("Description")
    
    uploaded_file = st.file_uploader("Upload File", 
                                    type=['pdf', 'ppt', 'pptx', 'doc', 'docx', 
                                          'jpg', 'jpeg', 'png', 'txt'])
    
    visibility = st.checkbox("Make visible to students", value=True)
    
    if st.button("📤 Upload Material"):
        if material_title and material_class and material_section and material_subject:
            materials_df = load_dataframe('data/materials/all_materials')
            
            file_path = "N/A"
            if uploaded_file:
                save_path = f"data/materials/{uploaded_file.name}"
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_path = save_path
            
            new_material = {
                'Title': material_title,
                'Class': material_class,
                'Sections': ', '.join(material_section),
                'Subject': material_subject,
                'Chapter': material_chapter,
                'Type': material_type,
                'Description': material_description,
                'File_Path': file_path,
                'Visible': visibility,
                'Upload_Date': str(date.today()),
                'Uploaded_By': st.session_state.user_data['name']
            }
            
            if materials_df.empty:
                materials_df = pd.DataFrame([new_material])
            else:
                materials_df = pd.concat([materials_df, pd.DataFrame([new_material])], 
                                       ignore_index=True)
            
            save_dataframe(materials_df, 'data/materials/all_materials')
            st.success("✅ Material uploaded successfully!")
        else:
            st.error("❌ Please fill all required fields")

def view_materials():
    st.subheader("All Study Materials")
    
    materials_df = load_dataframe('data/materials/all_materials')
    
    if not materials_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            filter_class = st.selectbox("Filter by Class", 
                                       ["All"] + list(materials_df['Class'].unique()))
        with col2:
            filter_subject = st.selectbox("Filter by Subject", 
                                         ["All"] + list(materials_df['Subject'].unique()))
        
        filtered_materials = materials_df.copy()
        if filter_class != "All":
            filtered_materials = filtered_materials[filtered_materials['Class'] == filter_class]
        if filter_subject != "All":
            filtered_materials = filtered_materials[filtered_materials['Subject'] == filter_subject]
        
        st.dataframe(filtered_materials, use_container_width=True)
    else:
        st.info("No study materials uploaded yet.")