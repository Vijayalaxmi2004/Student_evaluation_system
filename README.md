# 🎓 Student Evaluation System

A comprehensive web-based student evaluation platform built with **Streamlit**, featuring attendance tracking, mid-exam analysis, performance analytics, and real-time feedback.

## ✨ Features

### 📊 **Faculty Dashboard**
- **📝 Smart Attendance Management**: Mark daily/subject-wise attendance with bulk actions
- **✏️ Mid Marks Entry**: Upload marks via CSV/Excel or enter manually
- **📈 Mid Marks Analytics**: Subject-wise, student-wise, and performance distribution analysis
- **📬 Student Feedback**: View and manage student feedback
- **📌 Announcements**: Post and manage class announcements
- **💬 Messages**: Direct messaging to students
- **📊 Performance Analytics**: Risk analysis, department insights, SGPA trends

### 👨‍🎓 **Student Dashboard**
- **📊 View Marks**: Comprehensive grade reports by semester
- **📅 Attendance Tracking**: Personal attendance records and percentage
- **📊 Mid Exam Analysis**: Mid exam marks with analysis
- **📈 Academic Progress**: SGPA trends and charts
- **📝 Submit Feedback**: Course and faculty feedback
- **⚠️ Risk Alerts**: Early warning for low performance
- **🤖 AI Prediction**: ML-based SGPA prediction

---

## 🚀 **Quick Start**

```bash
# Clone repository
git clone https://github.com/<YOUR_USERNAME>/Student_Evaluation_System.git
cd Student_Evaluation_System/Student_evaluation_system

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

Open http://localhost:8501

---

## 📋 **Deployment Steps**

### **1. GitHub Setup**

```powershell
# Initialize git
git init
git add .
git commit -m "Initial commit: Student Evaluation System"

# Add remote
git remote add origin https://github.com/<YOUR_USERNAME>/Student_Evaluation_System.git
git branch -M main
git push -u origin main
```

### **2. Streamlit Cloud Deployment**

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select repository, branch `main`, file `app.py`
5. Click Deploy!

✅ **Live URL**: `https://share.streamlit.io/<USERNAME>/Student_Evaluation_System`

**See [../DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) for detailed steps.**

---

## 🔐 **Default Test Accounts**

Register new accounts or use example data from `data/users_db.csv`

**Faculty**: Create during registration  
**Student**: Roll numbers from grades_db.csv

---

## 📦 **Tech Stack**

- **Frontend**: Streamlit
- **Backend**: Python
- **Data**: Pandas, CSV
- **Visualization**: Plotly
- **ML**: Scikit-learn

---

## 📂 **Project Structure**

```
├── app.py                 # Main entry
├── auth.py               # Login/Registration
├── student.py            # Student dashboard
├── faculty.py            # Faculty dashboard
├── attendance.py         # Attendance system
├── mid_marks.py          # Mid exam marks
├── utils.py              # Utilities
├── requirements.txt      # Dependencies
└── data/                 # CSV database
    ├── users_db.csv
    ├── grades_db.csv
    ├── attendance.csv
    ├── mid_marks.csv
    └── ...
```

---

## 🎯 **Key Features**

✅ Attendance tracking with bulk actions  
✅ Mid marks entry (CSV upload + manual)  
✅ Performance analytics & reports  
✅ Student risk detection  
✅ AI-based SGPA prediction  
✅ Real-time feedback system  

---

## 📊 **Data Files**

- `users_db.csv` - User accounts
- `grades_db.csv` - Student grades
- `attendance.csv` - Attendance records
- `mid_marks.csv` - Mid exam marks
- `messages.csv` - Faculty-student messages
- `announcements.csv` - Class announcements

---

## ⚙️ **Configuration**

Edit `.streamlit/config.toml` for:
- UI theme colors
- Server settings
- Font preferences

---

## 🐛 **Troubleshooting**

**App won't load**: Check `requirements.txt` has all dependencies  
**Data not saving**: CSV files save to `data/` folder  
**ModuleNotFoundError**: Run `pip install -r requirements.txt`

---

## 🚀 **Next Steps - Production Ready**

For production deployment:
1. Migrate from CSV to PostgreSQL/MySQL
2. Use environment variables for secrets
3. Enable HTTPS with reverse proxy
4. Set up automated backups
5. Configure logging and monitoring

---

## 📝 **License**

Open source - Educational use only

---

## 💡 **Need Help?**

- Open an Issue on GitHub
- Check [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md)
- Visit [Streamlit Docs](https://docs.streamlit.io)

---

**Made with ❤️ for educators and students**
