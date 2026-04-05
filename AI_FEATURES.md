# 🤖 AI-Powered Student Evaluation System

An intelligent student evaluation platform powered by Google Gemini AI, Machine Learning, and Natural Language Processing.

## ✨ What's New: AI Features

### 🤖 AI Chatbot
- **For Students:** Ask questions about academics, study strategies, and career guidance
- **For Faculty:** Get teaching strategies, student engagement tips, and academic advice
- **Powered by:** Google Gemini

### 📊 AI Insights & Analysis
- **Comprehensive Performance Reports** - AI-generated analysis of student performance
- **Predictive Analytics** - SGPA prediction using random forest models
- **Attendance Trend Analysis** - Predict attendance patterns
- **Sentiment Analysis** - Automatic analysis of student feedback

### 🚨 At-Risk Student Detection
- **Machine Learning Detection** - Uses Isolation Forest to identify struggling students
- **Automated Alerts** - Faculty receives actionable recommendations
- **Early Intervention** - Prevent student failures before they happen

### 🎯 Personalized Study Plans
- **AI-Generated Recommendations** - Customized advice based on academic performance
- **Subject Performance Analysis** - Identify weak areas
- **Improvement Strategies** - Specific, actionable study tips

### 📝 Enhanced Feedback System
- **Star Ratings** - Rate overall experience, subject content, and faculty
- **Sentiment Analysis** - Automatic mood detection from written feedback
- **Faculty Dashboard** - See feedback insights and patterns

### 📈 Advanced Analytics
- **Risk Assessment** - Identify students at risk of failing
- **Attendance Prediction** - Forecast attendance trends
- **Performance Distribution** - Visualize class-wide performance patterns

---

## 🎓 For Students

### Available Features:

1. **📊 Marks & Performance**
   - View semester-wise grades
   - Track academic progress
   - Subject performance analysis

2. **📅 Attendance Tracking**
   - View attendance records
   - Percentage calculation
   - Attendance alerts

3. **📝 Mid-Exam Analysis**
   - View mid-term marks
   - Compare with class average
   - Identify improvement areas

4. **📈 Academic Progress**
   - View historical performance
   - Trend analysis
   - Progress visualizations

5. **📝 Feedback Submission** ⭐ NEW
   - Rate subject content (1-5)
   - Rate faculty teaching (1-5)
   - Rate overall experience (1-5)
   - Submit detailed feedback
   - View sentiment analysis of your feedback

6. **🤖 AI Assistant** ⭐ NEW
   - Ask questions about academics
   - Get personalized guidance
   - Discuss study strategies
   - Powered by Google Gemini

7. **📊 AI Insights** ⭐ NEW
   - Comprehensive performance report
   - Attendance trend analysis
   - Personalized recommendations
   - downloadable PDF report

8. **🎯 Personalized Plan** ⭐ NEW
   - AI-generated study recommendations
   - Subject-specific tips
   - Risk assessment
   - Actionable improvement strategies

9. **🤖 AI Grade Prediction** ⭐ NEW
   - Predict next semester SGPA
   - Top factors influencing grades
   - Subject performance breakdown
   - Model accuracy metrics

---

## 👨‍🏫 For Faculty

### Available Features:

1. **📊 Student Performance Analytics**
   - View class performance statistics
   - Risk analysis for students
   - Department-wise analytics
   - GPA distribution charts

2. **📝 Smart Attendance Management**
   - Quick attendance marking
   - Bulk actions (Mark all Present/Absent)
   - Random check feature
   - Live statistics
   - Sectioned attendance marking
   - Auto-send attendance alerts to students
   - Attendance analytics and reports

3. **📬 Student Feedback Management**
   - View student feedback
   - Search by subject area
   - Rate student submissions

4. **📌 Announcements**
   - Post class announcements
   - Manage important messages
   - Trackable delivery

5. **💬 Direct Messaging**
   - Send messages to students
   - Attendance alerts
   - Performance notifications

6. **✏️ Mid Marks Entry**
   - Upload marks via CSV/Excel
   - Manual mark entry
   - Real-time validation

7. **📊 Mid Marks Analytics**
   - Subject-wise performance
   - Student-wise analysis
   - Performance distribution

8. **🚨 At-Risk Detection** ⭐ NEW
   - Automatic student risk detection
   - ML-based analysis
   - Recommended interventions
   - Export reports

9. **📊 Feedback Analysis** ⭐ NEW
   - Automatic sentiment analysis
   - Rating distributions
   - Positive/negative feedback count
   - Detailed feedback review
   - Export analysis reports

10. **🤖 Faculty AI Assistant** ⭐ NEW
    - Teaching strategy recommendations
    - Student engagement tips
    - Performance improvement strategies
    - Powered by Google Gemini

---

## 🚀 AI Technologies Used

### 1. **Natural Language Processing (NLP)**
- **Sentiment Analysis** - TextBlob for feedback analysis
- **Emotion Detection** - Polarity and subjectivity scoring
- **Text Classification** - Categorizing feedback sentiment

### 2. **Machine Learning**
- **Random Forest Regressor** - SGPA prediction
- **Isolation Forest** - At-risk student detection
- **Feature Importance Analysis** - Identifying key performance factors
- **Standard Scaling** - Data normalization

### 3. **Generative AI**
- **Google Gemini API** - Chat-based recommendations
- **Context-Aware Responses** - Personalized suggestions
- **Educational Focus** - Tailored for academic context

### 4. **Data Analysis**
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Plotly** - Interactive visualizations

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Student_Evaluation_System.git
cd Student_Evaluation_System/Student_evaluation_system
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Google API Key
```bash
# Windows (Command Prompt):
set GOOGLE_API_KEY=your_api_key_here

# Windows (PowerShell):
$env:GOOGLE_API_KEY="your_api_key_here"

# Mac/Linux:
export GOOGLE_API_KEY="your_api_key_here"
```

Get your Google API key from: https://aistudio.google.com/app/apikey

### 5. Run the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📊 Data Structure

The system uses CSV files for data storage:

```
data/
├── users_db.csv              # User credentials and roles
├── student_feedback.csv      # Student feedback with ratings & sentiment
├── attendance.csv            # Attendance records
├── grades_db.csv            # Student grades and GPA
├── announcements.csv        # Class announcements
└── messages.csv             # Faculty-student messages
```

### Enhanced Feedback CSV Structure:
```
rollno,year,semester,feedback,rating,subject_rating,faculty_rating,date
,,,,,,,
```

---

## 🎯 Key AI Features in Detail

### At-Risk Student Detection
```python
# Detects students likely to fail using ML
risk_data = detect_at_risk_students(grades_file)
# Returns: at-risk students, risk timeline, recommendations
```

### Personalized Recommendations
```python
# AI-generated study plans based on student data
plan = generate_personalized_recommendations(student_context)
# Includes: study tips, targeted areas, success strategies
```

### Sentiment Analysis
```python
# Analyzes feedback sentiment automatically
polarity, sentiment, subjectivity = analyze_feedback_sentiment(feedback_text)
# Returns: Positive/Negative/Neutral with confidence score
```

### SGPA Prediction
```python
# ML-based prediction of next semester performance
pred, r2_score, feature_importance = advanced_grade_prediction(student_id)
# Returns: Predicted SGPA, model accuracy, key factors
```

---

## 🔐 Security & Privacy

- **API Keys:** Never stored in code, use environment variables
- **Password Security:** SHA-256 hashing for user passwords
- **Data Privacy:** Student data isolated per user
- **No Tracking:** No external tracking or analytics

---

## 🐛 Troubleshooting

### Issue: "API key not configured"
```bash
# Verify your environment variable is set:
echo $GOOGLE_API_KEY  # Mac/Linux
echo %GOOGLE_API_KEY%  # Windows
```

### Issue: Cannot import Google Gemini
```bash
pip install google-generativeai --upgrade
```

### Issue: Feedback columns missing
```python
# Auto-creates new columns on first run
# If issues persist, delete data/student_feedback.csv and restart
```

---

## 📚 File Structure

```
Student_evaluation_system/
├── app.py                    # Main Streamlit application
├── student.py                # Student dashboard with AI features
├── faculty.py                # Faculty dashboard with AI analytics
├── ai_service.py             # All AI/ML functions
├── auth.py                   # Authentication system
├── utils.py                  # Utility functions
├── attendance.py             # Attendance management
├── mid_marks.py              # Mid-term marks handling
├── requirements.txt          # Python dependencies
├── AI_SETUP_GUIDE.md        # Detailed setup instructions
├── .env.example              # Environment variables template
├── data/                     # Data storage folder
│   ├── users_db.csv
│   ├── student_feedback.csv
│   ├── attendance.csv
│   ├── grades_db.csv
│   ├── announcements.csv
│   └── messages.csv
└── deploy.bat                # Deployment script
```

---

## 🚀 Deployment

### Deploy to Streamlit Cloud:
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Add `GOOGLE_API_KEY` secret to deployment settings
5. Deploy!

### Deploy to Your Server:
```bash
# Install Streamlit Server
pip install streamlit
# Configure systemd service or use gunicorn
gunicorn --workers 1 --threads 8 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8501 app:app
```

---

## 📈 Performance Metrics

The AI system provides:
- **R² Score:** Accuracy of grade predictions (0-1 scale)
- **Sentiment Score:** -1 to 1 (negative to positive)
- **Risk Confidence:** Percentage confidence of risk detection
- **Feature Importance:** Which factors most influence performance

---

## 🎓 Educational Benefits

✅ **Early Risk Detection** - Identify struggling students before failure  
✅ **Personalized Learning** - Tailored recommendations for each student  
✅ **Data-Driven Insights** - Make decisions based on ML analysis  
✅ **Student Engagement** - AI chatbot encourages academic questions  
✅ **Faculty Efficiency** - Automate feedback analysis and reporting  
✅ **Predictive Analytics** - Forecast student performance  

---

## 📞 Support

For issues or questions:
1. Check `AI_SETUP_GUIDE.md`
2. Review error messages in terminal
3. Verify all dependencies are installed
4. Ensure Google API key is valid

---

## 📝 License

This project is provided as-is for educational purposes.

---

## 🎯 Future Enhancements

- [ ] Advanced NLP for essay grading
- [ ] Computer Vision for handwriting recognition
- [ ] Real-time performance dashboards
- [ ] Mobile app support
- [ ] Integration with external LMS
- [ ] Advanced student recommendation engine
- [ ] Predictive career path suggestions

---

## 🌟 Credits

Built with:
- **Streamlit** - Web framework
- **Google Gemini** - Generative AI
- **Scikit-learn** - Machine Learning
- **Pandas** - Data analysis
- **Plotly** - Visualizations

---

**Made with ❤️ for better education through AI**
