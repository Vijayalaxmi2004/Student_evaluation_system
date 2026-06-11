Here's the current README file for your Student Evaluation System repository:

```markdown name=README.md url=https://github.com/Vijayalaxmi2004/Student_evaluation_system/blob/234f79eecc2d54d4b2d7cb4fe50737e9d4cce4a8/README.md
# 🎓 AI-Powered Student Evaluation System

A comprehensive web-based student evaluation platform built with **Streamlit**, featuring AI-powered analytics, intelligent chatbots, predictive modeling, and real-time feedback with sentiment analysis.

## 🌐 **Live Application**

**🚀 Try the live app here:** https://studentevaluationsystem-kzmaeoedpgx9pbzv7fb5r7.streamlit.app/

---

## 🤖 NEW: AI-Powered Features ⭐

### 🚀 Powered By:
- **Google Gemini API** - Intelligent chatbot and recommendations
- **Machine Learning** - Predictive analytics and risk detection  
- **NLP** - Sentiment analysis and feedback insights

### For Students:
- 🤖 **AI Assistant** - Ask questions, get personalized guidance
- 📊 **AI Insights** - Comprehensive performance analysis
- 🎯 **Study Plans** - AI-generated personalized recommendations
- 📈 **Grade Prediction** - ML-based SGPA forecasting
- 💬 **Sentiment Analysis** - Your feedback is automatically analyzed

### For Faculty:
- 🚨 **At-Risk Detection** - ML-powered student identification
- 📊 **Feedback Analysis** - Automatic sentiment analysis
- 🤖 **Faculty AI Assistant** - Teaching strategies and advice
- 📈 **Performance Analytics** - Comprehensive ML-driven insights

---

## ✨ Complete Features

### 📊 Faculty Dashboard
- 📝 Smart Attendance Management with bulk actions
- ✏️ Mid Marks Entry (CSV upload + manual)
- 📈 Mid Marks Analytics
- 📬 Student Feedback Management
- 📌 Announcements & Notifications
- 💬 Direct Messaging to Students
- 📊 Performance Analytics & Reports
- 🚨 At-Risk Student Detection
- 📊 Feedback Sentiment Analysis
- 🤖 Faculty AI Assistant

### 👨‍🎓 Student Dashboard  
- 📊 View Marks & GPA
- 📅 Attendance Tracking
- 📊 Mid Exam Analysis
- 📈 Academic Progress Charts
- 📝 Submit Feedback with Ratings
- ⚠️ AI Risk Alerts
- 🤖 AI Grade Prediction
- 🤖 AI Assistant Chatbot
- 📊 AI Insights Report
- 🎯 Personalized Study Plans

---

## 🚀 Quick Start

### 1. Get Google API Key
```bash
# Visit: https://aistudio.google.com/app/apikey
# Click "Create API Key" and copy it
```

### 2. Set Environment Variable
```bash
# Windows (Command Prompt):
set GOOGLE_API_KEY=your_api_key_here

# Windows (PowerShell):
$env:GOOGLE_API_KEY="your_api_key_here"

# Mac/Linux:
export GOOGLE_API_KEY="your_api_key_here"
```

### 3. Install & Run
```bash
# Clone repository
git clone https://github.com/Vijayalaxmi2004/Student_evaluation_system.git
cd Student_evaluation_system

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

Open http://localhost:8501

**For detailed setup, see [QUICKSTART.md](QUICKSTART.md) and [AI_SETUP_GUIDE.md](AI_SETUP_GUIDE.md)**

---

## 📁 Project Structure

```
Student_evaluation_system/
├── app.py                  # Main Streamlit app
├── student.py              # Student dashboard with AI
├── faculty.py              # Faculty dashboard with AI
├── ai_service.py           # All AI/ML functions
├── auth.py                 # Authentication
├── attendance.py           # Attendance management
├── mid_marks.py            # Mid marks handling
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── AI_FEATURES.md         # Detailed AI docs
├── AI_SETUP_GUIDE.md      # Setup instructions
├── QUICKSTART.md          # Quick start guide
└── data/                  # CSV databases
    ├── users_db.csv
    ├── student_feedback.csv
    ├── attendance.csv
    ├── grades_db.csv
    ├── announcements.csv
    └── messages.csv
```

---

## 📦 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: Google Gemini, Scikit-learn, TextBlob
- **Data**: Pandas, NumPy
- **Visualization**: Plotly
- **Database**: CSV files (easily migrable to SQL)

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[AI_FEATURES.md](AI_FEATURES.md)** - Comprehensive AI features guide  
- **[AI_SETUP_GUIDE.md](AI_SETUP_GUIDE.md)** - Detailed setup & troubleshooting

---

## 🎯 Key Improvements Over Previous Version

✅ **Complete AI Integration** - Gemini API, ML models, NLP  
✅ **Enhanced Feedback** - Star ratings + sentiment analysis  
✅ **Risk Detection** - Automated at-risk student identification  
✅ **Personalized Plans** - AI-generated study recommendations  
✅ **Grade Prediction** - Advanced SGPA forecasting  
✅ **Faculty Analytics** - Comprehensive feedback analysis  
✅ **Student Guidance** - AI chatbot for personalized advice  

---

## 🆘 Troubleshooting

**API key not found**
```bash
echo %GOOGLE_API_KEY%  # Windows
echo $GOOGLE_API_KEY  # Mac/Linux
```

**Import errors**
```bash
pip install -r requirements.txt --upgrade
```

**See [AI_SETUP_GUIDE.md](AI_SETUP_GUIDE.md) for full troubleshooting**

---

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Select your repository
4. Add `GOOGLE_API_KEY` secret in Settings
5. Deploy!

### Self-Hosted
```bash
streamlit run app.py --server.port 8501
```

---

## 🔐 Security

- ✅ Password hashing with SHA-256
- ✅ API keys via environment variables (never in code)
- ✅ User data isolation per login
- ✅ No external tracking

---

## 📈 System Architecture

```
┌─────────────────┐
│   Streamlit     │ ← Web Interface
├─────────────────┤
│  Student/       │ ← Application Logic
│  Faculty        │
├─────────────────┤
│  AI Service     │ ← ML, NLP, LLM
│  (ai_service)   │
├─────────────────┤
│  CSV Database   │ ← Data Storage
│  (data/*.csv)   │
└─────────────────┘
```

---

## 🎓 Use Cases

**For Students:**
- Track academic performance
- Get personalized study recommendations
- Receive early warnings for failing
- Ask AI for learning help
- Submit detailed feedback

**For Faculty:**
- Monitor class performance
- Identify struggling students early  
- Analyze feedback sentiment
- Generate automated reports
- Get teaching recommendations

---

## 💡 Future Enhancements

- [ ] Mobile app support
- [ ] Database migration to PostgreSQL
- [ ] Advanced visualization dashboards
- [ ] Computer vision for handwriting recognition
- [ ] Real-time performance notifications
- [ ] Career path recommendations
- [ ] Integration with LMS platforms

---

## 📞 Support & Contributing

For issues, suggestions, or contributions:
1. Open an Issue on GitHub
2. Check existing documentation
3. Review [AI_SETUP_GUIDE.md](AI_SETUP_GUIDE.md)

---

## 📝 License

This project is provided for educational purposes.

---

**🚀 Start using AI-powered education today!**

**🌐 Live App:** https://studentevaluationsystem-kzmaeoedpgx9pbzv7fb5r7.streamlit.app/

**📖 Documentation:** [QUICKSTART.md](QUICKSTART.md) | [AI_FEATURES.md](AI_FEATURES.md)
```

This is a well-organized README that covers:
- **Overview** of the AI-powered system
- **Key features** for both students and faculty
- **Quick start guide** with setup instructions
- **Project structure** and tech stack
- **Documentation links** for deeper guidance
- **Deployment instructions** and troubleshooting
- **Security features** and architecture diagram

Would you like me to help you update or improve any section of the README?
