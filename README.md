# 🎓 School Management ERP + LMS System

A complete School Management System built with Streamlit, featuring role-based access for Admin, Teachers, and Students.

## 📁 Project Structure
```
LMS/
├── config/          # Configuration & settings
├── data/            # Auto-generated data storage (CSV/Excel)
├── modules/         # Admin, Teacher, Student modules
│   ├── admin/       # Student/Teacher management
│   ├── teacher/     # Marks, Materials, Assignments
│   └── student/     # Profile, Performance, Submissions
├── utils/           # Authentication & data handlers
├── app.py           # Main application
└── requirements.txt # Dependencies
```

## ✨ Features

### 👨‍💼 Admin Dashboard
- ✅ Add/Edit/View Students & Teachers
- ✅ Manage Class Structure (1-12, Groups for 11-12)
- ✅ Export Data (CSV/Excel)
- ✅ User Account Management

### 👨‍🏫 Teacher Dashboard
- ✅ Enter Student Marks with Auto-calculation
- ✅ Performance Analytics with Charts
- ✅ Upload Study Materials (PDF, PPT, DOC)
- ✅ Create & Grade Assignments
- ✅ Subject-wise Analysis

### 👨‍🎓 Student Dashboard
- ✅ View Profile & Marks
- ✅ Performance Visualization
- ✅ Download Study Materials
- ✅ Submit Assignments
- ✅ Track Grades & Feedback

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/School-ERP-LMS-System.git
cd School-ERP-LMS-System
```

2. **Create virtual environment (optional but recommended)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the app**
```
Open browser: http://localhost:8501
```

## 🔑 Default Login Credentials

| Role    | Username  | Password    |
|---------|-----------|-------------|
| Admin   | admin     | admin123    |
| Teacher | teacher1  | teacher123  |
| Student | student1  | student123  |

⚠️ **Important:** Change default passwords in production!

## 🛠️ Technology Stack

- **Frontend & UI:** Streamlit
- **Data Processing:** Pandas
- **Visualizations:** Plotly
- **Storage:** CSV + Excel (File-based)
- **Authentication:** Session-based with SHA-256 hashing

## 📊 Modules Overview

### Admin Module
- Student Management (CRUD)
- Teacher Management (CRUD)
- Class & Section Setup
- Data Export Tools

### Teacher Module
- Marks Entry System
- Performance Analytics
- Study Materials Manager
- Assignment Creator & Grader

### Student Module
- Personal Profile
- Performance Dashboard
- Materials Downloader
- Assignment Submitter

## 📸 Screenshots

(Add screenshots here after deployment)

## 🔄 Workflow

1. **Admin** creates students and teachers
2. **Teacher** enters marks and uploads materials
3. **Student** views performance and downloads content
4. System auto-calculates grades and generates analytics

## 🌟 Future Enhancements

- [ ] Attendance Management
- [ ] Fee Management
- [ ] Time Table Generator
- [ ] Parent Portal
- [ ] Mobile App
- [ ] SMS/Email Notifications

## 📄 License

MIT License - Free to use for educational purposes

## 👨‍💻 Developer

Developed as a complete School ERP solution

## 🤝 Contributing

Contributions welcome! Please fork and submit pull requests.

## 📞 Support

For issues or questions, please create an issue in the repository.

---

**⭐ If you find this helpful, please star the repository!**
