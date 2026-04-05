# 🚀 Quick Start Guide: AI-Powered Student Evaluation System

## ⚡ 5-Minute Quick Setup

### 1️⃣ Get Your Google API Key (2 minutes)
```
1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
```

### 2️⃣ Set Environment Variable (1 minute)

**Windows Command Prompt:**
```cmd
set GOOGLE_API_KEY=paste_your_key_here
```

**Windows PowerShell:**
```powershell
$env:GOOGLE_API_KEY="paste_your_key_here"
```

**Mac/Linux:**
```bash
export GOOGLE_API_KEY="paste_your_key_here"
```

### 3️⃣ Install & Run (2 minutes)
```bash
# Navigate to project
cd Student_evaluation_system

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Done! 🎉 App opens at http://localhost:8501

---

## 📊 First Time Using the System?

### As a Student:
1. **Register** → Choose "Student" role
2. **Explore** → Go to "AI Assistant" tab
3. **View Results** → Check "AI Insights" for analysis
4. **Get Help** → Use "AI Plan" for study recommendations

### As Faculty:
1. **Register** → Choose "Faculty" role
2. **Check Alerts** → See "At-Risk Detection" for struggling students
3. **Analyze Feedback** → Use "Feedback Analysis" tab
4. **Get Advice** → Use "Faculty AI Assistant" for teaching tips

---

## 🎯 Key AI Features At A Glance

| Feature | Who | What It Does |
|---------|-----|-------------|
| 🤖 **AI Chatbot** | Both | Ask AI questions about academics |
| 📊 **AI Insights** | Student | Get comprehensive performance analysis |
| 🎯 **Study Plan** | Student | AI-generated personalized study plan |
| 🚨 **Risk Detection** | Faculty | Identify students at risk |
| 📊 **Feedback Analysis** | Faculty | Automatic sentiment analysis of feedback |
| 📈 **Grade Prediction** | Student | Predict next semester SGPA |

---

## 🔧 Troubleshooting One-Liners

```bash
# Issue: API key not found
echo %GOOGLE_API_KEY%  # Verify it's set

# Issue: Import errors
pip install -r requirements.txt --upgrade

# Issue: Streamlit not found
pip install streamlit

# Issue: Port already in use
streamlit run app.py --server.port 8502
```

---

## 📋 File Locations

- **App Main File:** `app.py`
- **Student Features:** `student.py`
- **Faculty Features:** `faculty.py`
- **All AI Functions:** `ai_service.py`
- **Setup Instructions:** `AI_SETUP_GUIDE.md`
- **Feature Documentation:** `AI_FEATURES.md`

---

## 🆘 Still Stuck?

1. **Check Setup Guide:** `AI_SETUP_GUIDE.md`
2. **Read Features:** `AI_FEATURES.md`
3. **Verify Installation:** `pip list | grep -E "streamlit|google|scikit|pandas"`

---

## 🎓 Example: Student Using AI Features

```
1. Student logs in with roll number
2. Goes to "🤖 AI Assistant" tab
3. Asks: "How can I improve my GPA?"
4. AI responds with personalized advice
5. Checks "📊 AI Insights" for detailed analysis
6. Views "🎯 AI Plan" for step-by-step recommendations
7. Submits feedback with ratings
8. System analyzes sentiment automatically
```

---

## 📈 Example: Faculty Using AI Features

```
1. Faculty logs in
2. Clicks "🚨 At-Risk Detection"
3. Sees list of struggling students
4. Gets AI recommendations for interventions
5. Checks "📊 Feedback Analysis"
6. Reviews student sentiment and suggestions
7. Uses "🤖 Faculty AI Assistant" for teaching ideas
8. Exports reports for documentation
```

---

## ✅ Checklist

- [ ] Google API key obtained
- [ ] GOOGLE_API_KEY environment variable set
- [ ] `pip install -r requirements.txt` completed
- [ ] No Python syntax errors (ran py_compile)
- [ ] Ready to run `streamlit run app.py`

---

## 🎉 You're All Set!

Run the app and explore the AI-powered features. The system will create all necessary data files automatically on first run.

**Need the full documentation?** →  See `AI_FEATURES.md` and `AI_SETUP_GUIDE.md`

Happy learning! 🚀
