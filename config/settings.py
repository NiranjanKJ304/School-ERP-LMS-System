import streamlit as st

# Application Constants
CLASSES = list(range(1, 13))
SECTIONS = ['A', 'B', 'C', 'D']
GROUPS_11_12 = ['Computer Science', 'Biology', 'Arts', 'Commerce']
SUBJECTS_1_10 = ['Tamil', 'English', 'Maths', 'Science', 'Social', 'Computer']

GROUP_SUBJECTS = {
    'Computer Science': ['Tamil', 'English', 'Maths', 'Physics', 'Chemistry', 'Computer Science'],
    'Biology': ['Tamil', 'English', 'Maths', 'Physics', 'Chemistry', 'Biology'],
    'Arts': ['Tamil', 'English', 'History', 'Geography', 'Economics', 'Political Science'],
    'Commerce': ['Tamil', 'English', 'Accountancy', 'Commerce', 'Economics', 'Business Maths']
}

def configure_page():
    st.set_page_config(
        page_title="School Management System",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown('''
        <style>
        .main {
            padding: 0rem 1rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #4CAF50;
            color: white;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        h1 {
            color: #2C3E50;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498DB;
        }
        h2 {
            color: #34495E;
        }
        h3 {
            color: #7F8C8D;
        }
        .reportview-container {
            background: #F8F9FA;
        }
        div[data-testid="stMetricValue"] {
            font-size: 28px;
        }
        </style>
    ''', unsafe_allow_html=True)