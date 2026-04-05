# ai_service.py - Comprehensive AI Integration
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score
import streamlit as st
from datetime import datetime, timedelta
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from textblob import TextBlob

# ========== CONFIGURATION ==========
def get_gemini_api_key():
    """Get API key from environment or Streamlit secrets"""
    # First check environment variable
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        return api_key
    
    # Then try Streamlit secrets (with error handling)
    try:
        if hasattr(st, "secrets"):
            api_key = st.secrets.get("GOOGLE_API_KEY", "")
            if api_key:
                return api_key
    except Exception:
        pass
    
    return ""

def init_gemini():
    """Initialize Gemini API"""
    if not GEMINI_AVAILABLE:
        return False
    api_key = get_gemini_api_key()
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# ========== OFFLINE CHATBOT (No API Required) ==========
def generate_offline_response(user_message, context="general", student_data=None):
    """
    Generate intelligent responses offline using rule-based templates
    No API key required - works instantly
    
    Args:
        user_message: User's question
        context: "student", "faculty", or "general"
        student_data: Optional student info dict
    """
    message_lower = user_message.lower()
    
    # Student-specific responses
    if context == "student":
        student_responses = {
            # GPA & Grades
            "gpa|grade|score|mark|result": f"""📚 **Grade Improvement Tips:**
• Attend classes regularly (aim for 90%+ attendance)
• Form study groups with classmates
• Visit faculty office hours for clarification
• Start assignments early, don't procrastinate
• Review previous exam papers
{f"Your Current GPA: {student_data.get('gpa', 'N/A')}" if student_data else ""}""",
            
            # Attendance
            "attendance|absent|class|present": """✅ **Attendance Matters:**
• Maintain at least 75% attendance (check your policy)
• Communicate with faculty if you'll miss class
• Catch up with notes from classmates
• Review recorded lectures if available
• Remember: Attendance affects academic standing""",
            
            # Study strategies
            "study|learn|prepare|exam|test": """🎯 **Effective Study Strategies:**
• Use Pomodoro Technique (25 min focus + 5 min break)
• Create concept maps and mind maps
• Teach topics to others (explains gaps in knowledge)
• Use active recall: test yourself frequently
• Mix subjects to improve retention
• Get 7-9 hours of sleep before exams""",
            
            # Time management
            "time|busy|schedule|manage|stress": """⏰ **Time Management & Stress:**
• Break tasks into smaller chunks
• Prioritize using Eisenhower Matrix (urgent/important)
• Use calendar or app to track deadlines
• Take regular breaks (prevents burnout)
• Practice deep breathing for stress relief
• Connect with college counselor if overwhelmed""",
            
            # Engagement
            "engagement|participate|discussion|question": """🤝 **Classroom Engagement:**
• Ask questions - they help you learn better!
• Participate in class discussions
• Join clubs or study groups related to your major
• Visit professor during office hours
• Join online forums or study communities
• Volunteer for group projects""",
            
            # Career advice
            "career|job|internship|placement|future": """💼 **Career Development:**
• Build a strong resume highlighting projects
• Seek internships in your field
• Network with professionals on LinkedIn
• Develop relevant skills (coding, languages, etc)
• Attend career fairs and workshops
• Work on portfolio projects""",
            
            # Subject difficulty
            "difficult|hard|struggle|problem|help": """💪 **Overcoming Subject Difficulties:**
• Identify specific topics that are challenging
• Break them into smaller concepts
• Use multiple learning resources (textbooks, YouTube, etc)
• Work through practice problems
• Form study groups to discuss difficult topics
• Ask for tutoring or extra help from faculty""",
        }
        
        for keywords, response in student_responses.items():
            if any(keyword in message_lower for keyword in keywords.split("|")):
                return response
    
    # Faculty-specific responses
    elif context == "faculty":
        # Self-improvement questions may arise in faculty chat too
        if any(phrase in message_lower for phrase in ["improve myself", "improve my self", "how can i improve my self", "how can i improve myself", "self improvement", "improve myself"]):
            return """🌱 **Personal Improvement Tips:**
• Set one or two clear daily goals and track progress
• Build a consistent study or planning routine
• Reflect each week on what worked and what didn’t
• Use small habits to make progress sustainable
• Stay balanced with sleep, exercise, and breaks
• Ask for mentorship and feedback when needed"""
        
        faculty_responses = [
            ("student engagement|engagement|interactive|participation|motivate|discussion|classroom", """🎓 **Improving Student Engagement:**
• Use active learning techniques (discussions, debates)
• Incorporate real-world examples and case studies
• Gamify learning with quizzes and challenges
• Use multimedia (videos, animations, images)
• Create collaborative projects
• Provide timely and constructive feedback
• Recognize and praise good participation"""),
            ("assessment|feedback|evaluation|grade|rubric", """✏️ **Assessment Best Practices:**
• Use clear rubrics communicated upfront
• Provide specific, actionable feedback
• Balance formative and summative assessments
• Give feedback quickly (within 1-2 weeks)
• Include both strengths and improvement areas
• Offer revision opportunities when possible
• Use varied assessment methods"""),
            ("attendance|absent|skip", """📋 **Handling Attendance Issues:**
• Track attendance patterns to identify problems
• Contact students missing multiple classes
• Understand root causes (illness, transport, work)
• Work with academic support services
• Communicate policy clearly from day 1
• Be flexible while maintaining standards"""),
            ("difficult|behavior|disrupt|conflict|challenging", """👥 **Managing Difficult Situations:**
• Approach with empathy - understand their perspective
• Set clear expectations and boundaries
• Document incidents professionally
• Consult with department head if needed
• Refer to counseling services when appropriate
• Focus on behavior, not personality
• Follow institutional policies"""),
            ("teach|method|technique|strategy|subject", """🏫 **Effective Teaching Strategies:**
• Start lessons with engaging hooks/questions
• Use varied instructional methods
• Incorporate visual, auditory, kinesthetic learning
• Check for understanding frequently
• Use think-pair-share activities
• Review and reinforce previous concepts
• Connect content to student interests"""),
            ("class|manage|control|discipline|order", """🎯 **Classroom Management:**
• Establish clear rules and expectations
• Be consistent with policies
• Build positive relationships with students
• Use proximity and positive reinforcement
• Minimize distractions and transitions
• Manage time effectively
• Address issues promptly"""),
            ("performance|struggling|low|concern|at-risk", """📊 **Student Performance Management:**
• Review attendance and grade trends regularly
• Identify at-risk students early
• Schedule one-on-one meetings for support
• Provide clear feedback on assessments
• Offer extra office hours or tutoring
• Consider differentiated learning strategies"""),
        ]
        
        for keywords, response in faculty_responses:
            if any(keyword in message_lower for keyword in keywords.split("|")):
                return response
    
    # General responses (no context or default)
    general_responses = {
        "hello|hi|hey|greet": "👋 **Hello!** I'm your AI Education Assistant. How can I help you today? Ask me about grades, study tips, careers, or teaching strategies!",
        "thank|thanks|appreciate": "😊 You're welcome! Feel free to ask me anything about education, learning, or academic success!",
        "help|assist|support": """📖 **I can help with:**
• Study tips and learning strategies
• Time management and stress relief
• Career and academic advice
• Performance analysis
• Engagement strategies
• And much more!
Ask me anything!""",
        "what|who|how": """❓ **About Me:**
I'm an AI Education Assistant that helps both students and faculty:
• For **students**: Improve grades, attendance, study skills, career planning
• For **faculty**: Analyze student performance, engagement strategies, assessment tips
Ask me any education-related question!""",
    }
    
    for keywords, response in general_responses.items():
        if any(keyword in message_lower for keyword in keywords.split("|")):
            return response
    
    # Default intelligent response
    return """🤔 That's a great question! While I don't have a specific response for that, here are some general tips:

• **If it's academic**: Visit your faculty during office hours or check your course materials
• **If it's career-related**: Connect with your career services center or mentor
• **If it's personal**: Reach out to your academic advisor or counseling services
• **For technical help**: Contact your IT support

Remember: You can always ask me about specific topics like grades, attendance, study strategies, or teaching methods!"""


# ========== AI CHATBOT (Offline-First, Optional Gemini Fallback) ==========
def ai_chatbot(user_message, context="general", student_data=None):
    """
    AI Chatbot with smart offline-first approach
    Works without any API key - instantly responsive
    Optional Gemini fallback if API is configured
    
    Args:
        user_message: User's question
        context: "student", "faculty", or "general"
        student_data: Optional student info dict
    """
    # Primary: Use efficient offline chatbot (no API needed)
    offline_response = generate_offline_response(user_message, context, student_data)
    
    # Only try Gemini if API is configured AND offline response is generic default
    # This provides optional enhancement without requiring API
    if GEMINI_AVAILABLE and init_gemini() and "That's a great question! While I don't have a specific response" in offline_response:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            system_prompt = f"""You are an AI Education Assistant for a Student Evaluation System.
Context: {context}"""
            if context == "student" and student_data:
                system_prompt += f"""\nStudent Info:
- GPA: {student_data.get('gpa', 'N/A')}
- Attendance: {student_data.get('attendance', 'N/A')}%"""
            elif context == "faculty":
                system_prompt += "\nYou are helping faculty with student performance analysis."
            
            response = model.generate_content(
                f"{system_prompt}\n\nQuestion: {user_message}",
                temperature=0.7,
                max_output_tokens=500
            )
            return response.text
        except Exception:
            # If Gemini fails, return offline response
            return offline_response
    
    # Return offline response (primary, always works)
    return offline_response

# ========== SENTIMENT ANALYSIS ==========
def analyze_feedback_sentiment(feedback_text):
    """
    Analyze sentiment of feedback text
    Returns: sentiment_score (-1 to 1), sentiment_label
    """
    try:
        blob = TextBlob(feedback_text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.1:
            sentiment = "Positive 😊"
        elif polarity < -0.1:
            sentiment = "Negative 😟"
        else:
            sentiment = "Neutral 😐"
        
        return polarity, sentiment, subjectivity
    except:
        return 0, "Neutral 😐", 0.5

def get_feedback_insights(feedback_df):
    """Get AI insights from feedback data"""
    if feedback_df.empty:
        return "No feedback data available."
    
    if 'feedback' not in feedback_df.columns:
        return "No feedback text found."
    
    sentiments = []
    positives = []
    negatives = []
    
    for feedback in feedback_df['feedback'].dropna():
        polarity, sentiment, _ = analyze_feedback_sentiment(str(feedback))
        sentiments.append(polarity)
        
        if polarity > 0.1:
            positives.append(feedback)
        elif polarity < -0.1:
            negatives.append(feedback)
    
    avg_sentiment = np.mean(sentiments) if sentiments else 0
    
    insights = f"""
**📊 Feedback Sentiment Analysis:**
- Average Sentiment Score: {avg_sentiment:.2f} (Range: -1 to 1)
- Positive Feedback: {len(positives)} responses
- Negative Feedback: {len(negatives)} responses
- Total Feedback: {len(sentiments)} responses

**Key Patterns:**
"""
    
    if avg_sentiment > 0.3:
        insights += "✅ Overall positive feedback trends\n"
    elif avg_sentiment < -0.3:
        insights += "⚠️ Significant concerns in feedback\n"
    else:
        insights += "➖ Mixed feedback with both positive and negative aspects\n"
    
    if positives:
        insights += f"\n**Top Positive Themes:**\n- {len(positives)} students expressed satisfaction\n"
    if negatives:
        insights += f"\n**Areas of Concern:**\n- {len(negatives)} students raised concerns\n"
    
    return insights

# ========== RISK DETECTION & PERFORMANCE ANALYSIS ==========
def detect_at_risk_students(grades_file="data/grades_db.csv"):
    """
    Detect students at risk of failing using Isolation Forest
    Returns: dict with risk levels and recommendations
    """
    if not os.path.exists(grades_file):
        return None
    
    try:
        df = pd.read_csv(grades_file)
        df.columns = df.columns.str.strip().str.lower()
        
        # Select numeric columns for analysis
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        
        if 'semester_gpa' in numeric_cols:
            numeric_cols.remove('semester_gpa')
        
        if not numeric_cols:
            return None
        
        X = df[numeric_cols].fillna(0)
        
        # Normalize data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Detect anomalies (at-risk students)
        iso_forest = IsolationForest(contamination=0.2, random_state=42)
        anomaly_scores = iso_forest.fit_predict(X_scaled)
        
        df['risk_score'] = iso_forest.score_samples(X_scaled)
        df['risk_status'] = ['At Risk ⚠️' if score < -1 else 'Normal ✅' 
                            for score in df['risk_score']]
        
        risk_students = df[df['risk_status'] == 'At Risk ⚠️'].copy()
        
        return {
            'all_students': df,
            'at_risk': risk_students,
            'risk_percentage': (len(risk_students) / len(df) * 100) if len(df) > 0 else 0,
            'recommendation': generate_risk_recommendation(risk_students)
        }
    except Exception as e:
        return None

def generate_risk_recommendation(risk_df):
    """Generate AI-powered recommendations for at-risk students"""
    if risk_df.empty:
        return "No at-risk students identified. Keep monitoring performance."
    
    avg_scores = risk_df.select_dtypes(include='number').mean()
    
    recommendations = f"""
**🎯 Intervention Recommendations:**

**Number of At-Risk Students:** {len(risk_df)}
**Percentage:** {len(risk_df)/10:.1f}% (approximate)

**Key Issues Identified:**
"""
    
    for col, score in avg_scores.head(3).items():
        if score < 40:
            recommendations += f"- 📍 Low performance in {col}\n"
    
    recommendations += """
**Suggested Actions:**
1. 👨‍🏫 Schedule counseling sessions
2. 📚 Increase tutoring support
3. 📞 Contact parents/guardians
4. 🔄 Consider course withdrawal if needed
5. 💪 Provide motivational support
"""
    
    return recommendations

# ========== PERSONALIZED RECOMMENDATIONS ==========
def generate_personalized_recommendations(student_data, grades_file="data/grades_db.csv"):
    """
    Generate AI-powered personalized recommendations for a student
    
    Args:
        student_data: dict with keys like gpa, attendance, weak_subjects, year
        grades_file: path to grades database
    """
    gpa = student_data.get('gpa', 0)
    attendance = student_data.get('attendance', 0)
    year = student_data.get('year', 1)
    semester = student_data.get('semester', 1)
    
    recommendations = f"""
**🎯 Personalized Academic Recommendations**

**Your Performance Summary:**
- Current GPA: {gpa:.2f}/10
- Attendance: {attendance:.1f}%
- Year {year}, Semester {semester}

"""
    
    # GPA-based recommendations
    if gpa >= 8.5:
        recommendations += """
**🏆 Excellent Performance!**
✅ Continue maintaining this excellence
✅ Consider taking advanced courses
✅ Prepare for leadership roles
✅ Look into research opportunities
"""
    elif gpa >= 7.5:
        recommendations += """
**📈 Good Performance**
✅ You're on a positive track
✅ Focus on consistency
✅ Identify 1-2 subjects for improvement
✅ Consider joining study groups
"""
    elif gpa >= 6.0:
        recommendations += """
**⚡ Average Performance - Opportunity for Growth**
✅ Increase study hours (2-3 hours daily)
✅ Identify weak subjects and get tutoring
✅ Attend all classes and labs
✅ Form study groups with peers
✅ Meet faculty during office hours
"""
    else:
        recommendations += """
**🆘 Below Average - Immediate Action Required**
❗ Schedule a meeting with academic advisor
❗ Get tutoring support immediately
❗ Increase study hours to 4-5+ daily
❗ Consider dropping non-essential activities
❗ Talk to your parents about academic plan
"""
    
    # Attendance-based recommendations
    recommendations += f"\n**📅 Attendance Tips:**\n"
    if attendance >= 90:
        recommendations += "✅ Excellent attendance! Keep it up.\n"
    elif attendance >= 75:
        recommendations += "⚠️ Aim for 90%+ attendance.\n"
    else:
        recommendations += f"❗ Critical: {attendance:.1f}% is below minimum. Improve immediately!\n"
    
    # Year-based recommendations
    if year >= 4:
        recommendations += """
**🎓 Final Year Focus:**
- Polish your resume
- Start placement preparation
- Network with alumni
- Complete internships/projects
"""
    elif year >= 2:
        recommendations += """
**📚 Mid-Year Development:**
- Build technical strengths
- Take up internships
- Start competitive programming
- Join clubs/societies
"""
    
    return recommendations

# ========== ATTENDANCE PREDICTION ==========
def predict_attendance_trend(student_rollno, attendance_file="data/attendance.csv"):
    """
    Predict attendance trends for a student
    """
    if not os.path.exists(attendance_file):
        return None
    
    try:
        df = pd.read_csv(attendance_file)
        student_att = df[df['rollno'].astype(str) == str(student_rollno)].copy()
        
        if student_att.empty:
            return None
        
        student_att['date'] = pd.to_datetime(student_att['date'])
        student_att = student_att.sort_values('date')
        
        # Calculate rolling average
        student_att['present_binary'] = (student_att['status'] == 'Present').astype(int)
        student_att['rolling_avg'] = student_att['present_binary'].rolling(window=7, min_periods=1).mean() * 100
        
        # Predict next 5 days trend
        recent_trend = student_att['rolling_avg'].iloc[-5:].mean() if len(student_att) > 0 else 0
        
        # Trend analysis
        if recent_trend < student_att['rolling_avg'].mean() - 10:
            trend = "📉 Declining - Attendance getting worse"
        elif recent_trend > student_att['rolling_avg'].mean() + 10:
            trend = "📈 Improving - Keep attending regularly"
        else:
            trend = "➡️ Stable - Maintain current attendance"
        
        prediction = {
            'current_percentage': student_att['present_binary'].mean() * 100,
            'rolling_average': recent_trend,
            'trend': trend,
            'pattern': analyze_attendance_pattern(student_att)
        }
        
        return prediction
    except Exception as e:
        return None

def analyze_attendance_pattern(att_df):
    """Analyze patterns in attendance"""
    if att_df.empty:
        return "No data to analyze"
    
    # Day-wise analysis (if available)
    try:
        att_df['date'] = pd.to_datetime(att_df['date'])
        att_df['day_of_week'] = att_df['date'].dt.day_name()
        
        day_stats = att_df.groupby('day_of_week')['status'].apply(
            lambda x: (x == 'Present').sum() / len(x) * 100
        )
        
        worst_day = day_stats.idxmin() if len(day_stats) > 0 else "Unknown"
        best_day = day_stats.idxmax() if len(day_stats) > 0 else "Unknown"
        
        pattern = f"Best attendance on {best_day}, Worst on {worst_day}"
        return pattern
    except:
        return "Pattern analysis unavailable"

# ========== AUTOMATED INSIGHTS & REPORTS ==========
def generate_ai_insights_report(student_rollno, grades_file="data/grades_db.csv", 
                               attendance_file="data/attendance.csv", feedback_file="data/student_feedback.csv"):
    """Generate comprehensive AI insights report for a student"""
    
    report = f"""
═══════════════════════════════════════════════════════
🤖 AI-POWERED STUDENT INSIGHTS REPORT
Roll No: {student_rollno}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
═══════════════════════════════════════════════════════

"""
    
    # Academic Performance
    if os.path.exists(grades_file):
        df_grades = pd.read_csv(grades_file)
        student_grades = df_grades[df_grades['rollno'].astype(str).str.lower() == str(student_rollno).lower()]
        
        if not student_grades.empty:
            report += "\n📊 ACADEMIC PERFORMANCE ANALYSIS\n"
            report += "─" * 50 + "\n"
            
            try:
                gpa = student_grades.select_dtypes(include='number').mean().mean()
                report += f"Overall GPA: {gpa:.2f}/10\n"
                
                if gpa >= 8.5:
                    report += "Status: ⭐ Excellent - Continue excellence\n"
                elif gpa >= 7.5:
                    report += "Status: ✅ Good - Maintain consistency\n"
                elif gpa >= 6.0:
                    report += "Status: ⚠️ Average - Room for improvement\n"
                else:
                    report += "Status: ❌ Below Average - Needs intervention\n"
            except:
                pass
    
    # Attendance Analysis
    if os.path.exists(attendance_file):
        att_prediction = predict_attendance_trend(student_rollno, attendance_file)
        if att_prediction:
            report += "\n📅 ATTENDANCE ANALYSIS\n"
            report += "─" * 50 + "\n"
            report += f"Current Attendance: {att_prediction['current_percentage']:.1f}%\n"
            report += f"Trend: {att_prediction['trend']}\n"
            report += f"Pattern: {att_prediction['pattern']}\n"
    
    # Feedback Analysis
    if os.path.exists(feedback_file):
        try:
            df_feedback = pd.read_csv(feedback_file)
            student_feedback = df_feedback[df_feedback['rollno'].astype(str).str.lower() == str(student_rollno).lower()]
            
            if not student_feedback.empty:
                report += "\n💬 FEEDBACK SENTIMENT ANALYSIS\n"
                report += "─" * 50 + "\n"
                sentiments = []
                for feedback in student_feedback['feedback'].dropna():
                    polarity, _, _ = analyze_feedback_sentiment(str(feedback))
                    sentiments.append(polarity)
                
                avg_sentiment = np.mean(sentiments)
                report += f"Average Sentiment: {avg_sentiment:.2f}/1.0\n"
                if avg_sentiment > 0.3:
                    report += "Sentiment: Positive ✅\n"
                elif avg_sentiment < -0.3:
                    report += "Sentiment: Negative ⚠️\n"
                else:
                    report += "Sentiment: Neutral ➖\n"
        except:
            pass
    
    # Recommendations
    report += "\n🎯 RECOMMENDATIONS\n"
    report += "─" * 50 + "\n"
    report += generate_personalized_recommendations({
        'gpa': 7.5,
        'attendance': 85,
        'year': 2,
        'semester': 1
    })
    
    report += "\n" + "═" * 50 + "\n"
    report += "Report generated by AI Evaluation System\n"
    
    return report

# ========== GRADE PREDICTION WITH ADVANCED ML ==========
def advanced_grade_prediction(student_rollno, grades_file="data/grades_db.csv"):
    """Advanced ML-based grade prediction"""
    if not os.path.exists(grades_file):
        return None, None, None
    
    try:
        df = pd.read_csv(grades_file)
        df.columns = df.columns.str.strip().str.lower()
        
        numeric_df = df.select_dtypes(include='number')
        
        if 'semester_gpa' not in numeric_df.columns or len(numeric_df) < 5:
            return None, None, None
        
        X = numeric_df.drop('semester_gpa', axis=1, errors='ignore')
        y = numeric_df['semester_gpa']
        
        if len(X) == 0 or len(X.columns) == 0:
            return None, None, None
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        model.fit(X_train, y_train)
        
        # R² score
        r2 = r2_score(y_test, model.predict(X_test))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values(by='importance', ascending=False)
        
        # Predict for student
        student_row = df[df['rollno'].astype(str).str.lower() == student_rollno.strip().lower()]
        if student_row.empty:
            pred = None
        else:
            X_student = student_row.select_dtypes(include='number').drop('semester_gpa', axis=1, errors='ignore')
            if len(X_student.columns) != len(X.columns):
                pred = None
            else:
                pred = model.predict(X_student)[0]
        
        return round(pred, 2) if pred else None, r2, feature_importance
    except Exception as e:
        return None, None, None

# ========== SUBJECT PERFORMANCE ANALYSIS ==========
def analyze_subject_performance(student_rollno, grades_file="data/grades_db.csv"):
    """Analyze performance by subject"""
    if not os.path.exists(grades_file):
        return None
    
    try:
        df = pd.read_csv(grades_file)
        student = df[df['rollno'].astype(str).str.lower() == student_rollno.strip().lower()]
        
        if student.empty:
            return None
        
        # Get non-numeric columns as subjects
        subject_cols = [col for col in student.columns if col.lower() not in ['rollno', 'name', 'id', 'semester_gpa']]
        
        analysis = {}
        for col in subject_cols:
            try:
                score = float(student[col].iloc[0])
                if score >= 85:
                    status = "Excellent 🌟"
                elif score >= 70:
                    status = "Good ✅"
                elif score >= 50:
                    status = "Average ⚠️"
                else:
                    status = "Needs Work ❌"
                analysis[col] = {'score': score, 'status': status}
            except:
                pass
        
        return analysis
    except Exception as e:
        return None
