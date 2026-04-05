# Setup Instructions for AI-Powered Student Evaluation System

## 📋 Prerequisites

Before running the application, ensure you have the following:

1. **Python 3.8+** installed
2. **pip** (Python package manager)
3. **Google API Key** (for Gemini AI features)

---

## 🔑 Step 1: Get Your Google API Key

### How to Generate a Google API Key:

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google Account (create one if you don't have)
3. Click on **"Create API Key"** button
4. Copy the generated API key
5. Keep it safe and secure (don't share it!)

---

## 🚀 Step 2: Configure the API Key

### Option A: Using Environment Variables (Recommended)

#### On Windows (Command Prompt):
```batch
set GOOGLE_API_KEY=your_api_key_here
```

#### On Windows (PowerShell):
```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

#### On Mac/Linux:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### Option B: Using .env File

1. Create a `.env` file in the project root directory:
```
GOOGLE_API_KEY=your_api_key_here
```

2. Install python-dotenv if not already installed:
```bash
pip install python-dotenv
```

### Option C: Using Streamlit Secrets

1. Create `.streamlit/secrets.toml` file in your project:
```toml
GOOGLE_API_KEY = "your_api_key_here"
```

---

## 📦 Step 3: Install Dependencies

```bash
# Navigate to project directory
cd Student_evaluation_system

# Create virtual environment (optional but recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Step 4: Run the Application

```bash
# Make sure your API key is set in environment variables
# Then run:
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 🤖 AI Features Now Available

### For Students:
- ✅ **AI Chatbot** - Ask questions about academics
- ✅ **AI Insights** - Comprehensive performance analysis
- ✅ **Personalized Study Plans** - AI-generated recommendations
- ✅ **SGPA Prediction** - Machine learning grade forecasting
- ✅ **Risk Detection** - Early warning for low performance
- ✅ **Sentiment Analysis** - Analysis of your feedback

### For Faculty:
- ✅ **At-Risk Student Detection** - Identify struggling students
- ✅ **Feedback Analysis** - Sentiment analysis and insights
- ✅ **Faculty AI Assistant** - Teaching strategies and advice
- ✅ **Performance Analytics** - Comprehensive class analysis

---

## 📋 Feedback Form Enhancements

Students can now provide detailed feedback with:
- Overall Experience Rating (1-5 stars)
- Subject Content Rating (1-5 stars)
- Faculty Teaching Rating (1-5 stars)
- Written feedback
- Automatic sentiment analysis

---

## 🔧 Troubleshooting

### Issue: "API key not configured"
**Solution:** Make sure your GOOGLE_API_KEY environment variable is set before running the app.

### Issue: Gemini features aren't showing up
**Solution:** 
1. Check that your Google API key is valid
2. Ensure `google-generativeai` package is installed: `pip install google-generativeai`
3. Restart the Streamlit app

### Issue: Import errors
**Solution:** Make sure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

---

## 📊 Data Files

The system automatically creates the following CSV files:
- `data/users_db.csv` - User authentication data
- `data/student_feedback.csv` - Student feedback with ratings and sentiment
- `data/attendance.csv` - Attendance records
- `data/grades_db.csv` - Student grades and GPA
- `data/announcements.csv` - Class announcements
- `data/messages.csv` - Faculty-student messages

---

## 🎯 First Time Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Google API Key generated
- [ ] Environment variable GOOGLE_API_KEY set
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Run: `streamlit run app.py`
- [ ] Register as a student or faculty member
- [ ] Start using AI features!

---

## 📚 Documentation

For more information about different modules:

- **student.py** - Student dashboard with AI features
- **faculty.py** - Faculty dashboard with AI analytics
- **ai_service.py** - All AI/ML functions
- **auth.py** - User authentication system
- **utils.py** - Utility functions

---

## 🆘 Need Help?

If you encounter any issues:
1. Check the error message in the terminal
2. Verify your Google API key is valid
3. Make sure all packages are up to date
4. Restart the Streamlit app

---

## 🚀 Start Using AI-Powered Features!

Your Student Evaluation System is now AI-enabled with:
- Natural Language Processing (Sentiment Analysis)
- Machine Learning (Grade Prediction, Risk Detection)
- Generative AI (Google Gemini for personalized recommendations)

Enjoy the enhanced educational experience! 🎓
