import streamlit as st
from config.settings import CLASSES, SECTIONS
from utils.data_manager import load_dataframe

def export_data():
    st.header("📤 Data Export")
    
    st.subheader("Export Student Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        export_class = st.selectbox("Select Class", ["All"] + CLASSES)
    with col2:
        export_section = st.selectbox("Select Section", ["All"] + SECTIONS)
    
    students_df = load_dataframe('data/students/all_students')
    
    if not students_df.empty:
        filtered_df = students_df.copy()
        if export_class != "All":
            filtered_df = filtered_df[filtered_df['Class'] == export_class]
        if export_section != "All":
            filtered_df = filtered_df[filtered_df['Section'] == export_section]
        
        st.dataframe(filtered_df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"students_class_{export_class}_section_{export_section}.csv",
                mime="text/csv"
            )
        
        with col2:
            st.info("💡 Excel files are automatically saved in data/students/ folder")
    else:
        st.warning("No student data available for export.")