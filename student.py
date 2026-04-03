import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils import get_department_courses, plot_marks, plot_progress
from auth import FEEDBACK_FILE, ANNOUNCEMENT_FILE, USERS_FILE
from attendance import student_attendance
from mid_marks import student_mid_marks_analysis
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# ---------- CSS ----------
def load_css():
    st.markdown("""
    <style>
    /* ---------- Background ---------- */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(120deg,#89f7fe,#66a6ff);
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,#2b1055,#7597de);
    }

    section[data-testid="stSidebar"] * {
        color:white !important;
    }

    /* ---------- Cards ---------- */
    .card {
        background:white;
        padding:25px;
        border-radius:20px;
        box-shadow:0px 15px 40px rgba(0,0,0,0.2);
        margin-bottom:20px;
    }

    /* ---------- Student Dashboard Buttons (Large) ---------- */
    .student-btn button {
        width: 100% !important;
        min-height: 210px !important;
        font-size: 26px !important;
        font-weight: 800 !important;
        border-radius: 24px !important;
        background-color: white !important;
        color: #1E3A8A !important;
        border: 2px solid #c7dbed !important;
        box-shadow: 0px 8px 22px rgba(0,0,0,0.12) !important;
        transition: all 0.2s ease-in-out !important;
    }

    .student-btn button:hover {
        background: linear-gradient(135deg,#2563EB,#60A5FA) !important;
        color: white !important;
        transform: translateY(-4px) !important;
        box-shadow: 0px 14px 32px rgba(37,99,235,0.3) !important;
        border: none !important;
    }

    /* Same larger size for all student feature buttons */
    .student-btn-0 button, .student-btn-1 button, .student-btn-2 button, .student-btn-3 button,
    .student-btn-4 button, .student-btn-5 button, .student-btn-6 button, .student-btn-7 button {
        min-height: 210px !important; font-size: 26px !important;
    }

    /* ---------- Other Dashboard Tab Buttons ---------- */
    .dashboard-tab button {
        width: 100% !important;
        height: 65px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 14px !important;
        background: linear-gradient(135deg,#667eea,#764ba2) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
        transition: 0.3s ease-in-out !important;
    }

    .dashboard-tab button:hover {
        transform: scale(1.05) !important;
        background: linear-gradient(135deg,#89f7fe,#66a6ff) !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.35) !important;
    }

    /* ---------- Generic Buttons (Keep Small Buttons) ---------- */
    .stButton>button {
        border-radius:14px;
        height:50px;
        font-size:16px;
        background:linear-gradient(135deg,#667eea,#764ba2);
        color:white;
        border:none;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        background:linear-gradient(135deg,#89f7fe,#66a6ff);
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }
                
    .student-btn-0 button { height:160px; font-size:24px; }
.student-btn-1 button { height:150px; font-size:22px; }
.student-btn-2 button { height:140px; font-size:22px; }
.student-btn-3 button { height:145px; font-size:22px; }
.student-btn-4 button { height:160px; font-size:24px; }
.student-btn-5 button { height:150px; font-size:22px; }
.student-btn-6 button { height:140px; font-size:22px; }
.student-btn-7 button { height:145px; font-size:22px; }
.student-btn-8 button { height:160px; font-size:24px; }
    </style>
    """, unsafe_allow_html=True)
# ---------- Helper Functions ----------
def get_feedback(gpa, marks):
    status = "Excellent" if gpa >= 8.5 else "Good" if gpa >= 7.5 else "Average" if gpa >= 6.0 else "Needs Improvement"
    strength = "Strong performance across subjects" if gpa >= 8.0 else "Consistent performance"
    weakness = "Focus on weaker subjects" if gpa < 7.0 else "Maintain current level"
    advice = "Keep up the excellent work" if gpa >= 8.5 else "Work on improving weak areas" if gpa < 7.0 else "Continue steady progress"
    return {"status": status, "strength": strength, "weakness": weakness, "advice": advice}

# ---------- Attendance Helper ----------
def get_attendance_progress_for_student(student_rollno):
    attendance_file = "data/attendance.csv"

    if not os.path.exists(attendance_file):
        return None

    try:
        df = pd.read_csv(attendance_file)
        required_columns = ["date", "rollno", "name", "year", "semester", "status"]
        if not all(col in df.columns for col in required_columns):
            return None

        my_df = df[df['rollno'].astype(str) == str(student_rollno)].copy()
        if my_df.empty:
            return None

        present_count = len(my_df[my_df['status'] == 'Present'])
        total_count = len(my_df)

        if total_count == 0:
            return None

        attendance_percentage = round((present_count / total_count) * 100, 2)
        return {
            'total': total_count,
            'present': present_count,
            'absent': total_count - present_count,
            'percentage': attendance_percentage
        }

    except Exception:
        return None

# ---------- AI Prediction ----------
def ai_prediction(student_rollno):
    GRADES_FILE = "data/grades_db.csv"
    if not os.path.exists(GRADES_FILE):
        return None, None, None

    df = pd.read_csv(GRADES_FILE)
    df.columns = df.columns.str.strip().str.lower()
    num_df = df.select_dtypes(include='number')

    if 'semester_gpa' not in num_df.columns or len(num_df) < 5:
        return None, None, None

    X = num_df.drop('semester_gpa', axis=1, errors='ignore')
    y = num_df['semester_gpa']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # R² score
    r2 = r2_score(y_test, model.predict(X_test))

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values(by='importance', ascending=False)

    # Predict for the student
    student_row = df[df['rollno'].astype(str).str.lower() == student_rollno.strip().lower()]
    if student_row.empty:
        pred = None
    else:
        X_student = student_row.select_dtypes(include='number').drop('semester_gpa', axis=1, errors='ignore')
        if len(X_student.columns) != len(X.columns):
            pred = None
        else:
            pred = model.predict(X_student)[0]

    return round(pred,2) if pred else None, r2, feature_importance

# ---------- Student Dashboard ----------
def student_dashboard():
    load_css()
    st.markdown(f"""
    <div class="card" style="
        background: linear-gradient(135deg,#1E3A8A,#2563EB);
        color:white;
        display:flex;
        justify-content:space-between;
        align-items:center;
    ">
        <h2 style="margin:0;">🎓 Student Dashboard</h2>
        <h4 style="margin:0;">Roll No: {st.session_state.username}</h4>
    </div>
    """, unsafe_allow_html=True)

    if "student_tab" not in st.session_state:
        st.session_state.student_tab = "📊 Marks"

    # Tabs
    tabs = ["📊 Marks","📅 Attendance","� Mid Exams","�📈 Progress","📝 Feedback",
        "📢 Announcements","💬 Messages","⚠️ Alerts","🤖 AI Prediction"]
    
    # Split tabs into rows of 3 for better layout (9 tabs = 3 rows of 3)
    rows = [tabs[i:i+3] for i in range(0, len(tabs), 3)]
    
    # Wrap in student-buttons for CSS
    st.markdown('<div class="student-buttons">', unsafe_allow_html=True)
    for row_idx, row in enumerate(rows):
        cols = st.columns(len(row))  # Create columns dynamically based on row length
        for i, t in enumerate(row):
            with cols[i]:
                # Only the button, no extra nested divs
                st.markdown(f'<div class="student-btn student-btn-{i}">', unsafe_allow_html=True)
                if st.button(t, key=f"student_tab_{t}"):
                    st.session_state.student_tab = t
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Load student data
    GRADES_FILE = "data/grades_db.csv"
    if not os.path.exists(GRADES_FILE) or os.stat(GRADES_FILE).st_size == 0:
        st.info("📭 Faculty has not uploaded grades yet.")
        return

    df = pd.read_csv(GRADES_FILE)
    df.columns = df.columns.str.strip().str.lower()
    my_data = df[df['rollno'].astype(str).str.lower() == st.session_state.username.strip().lower()]
    if my_data.empty:
        st.warning("No records found for your roll number.")
        return

    tab = st.session_state.student_tab

    # ---------- Risk / Alerts ----------
    if tab == "⚠️ Alerts":
        st.subheader("⚠️ Alerts / Risk Detection")
        risk_df = my_data[my_data['semester_gpa'] < 6.0]
        if risk_df.empty:
            st.success("No risks detected. Keep up the good work! ✅")
        else:
            for _, row in risk_df.iterrows():
                st.error(f"Semester {row['semester']}, SGPA: {row['semester_gpa']} – At Risk! ⚠️")

    # ---------- Marks ----------
    elif tab == "📊 Marks":
        # Get student's department
        users_df = pd.read_csv(USERS_FILE)
        user_row = users_df[users_df["username"].str.strip().str.lower() == st.session_state.username.strip().lower()]
        student_department = user_row.iloc[0]["department"] if not user_row.empty else "CSE"

        y = st.selectbox("Year", sorted(my_data['year'].unique()))
        s = st.selectbox("Semester", sorted(my_data[my_data['year']==y]['semester'].unique()))
        row = my_data[(my_data['year']==y)&(my_data['semester']==s)].iloc[0]

        st.metric("Semester GPA", row.get("semester_gpa",0))

        # Use department-specific courses
        semester_subjects = get_department_courses(student_department, y, s)
        marks = {sub: row.get(sub.lower(),0) for sub in semester_subjects}
        st.plotly_chart(plot_marks(marks), use_container_width=True)

        fb = get_feedback(row.get("semester_gpa",0), marks)
        st.info(f"**Status:** {fb['status']}  \n**Strength:** {fb['strength']}  \n**Weakness:** {fb['weakness']}  \n**Advice:** {fb['advice']}")

        # ---------- Analytics ----------
        st.subheader("📊 Your Analytics")
        st.bar_chart(my_data[['semester','semester_gpa']].set_index('semester'))

    # ---------- Progress ----------
    elif tab == "📈 Progress":
        labels, perf = [], []
        for y in sorted(my_data['year'].unique()):
            for s in sorted(my_data[my_data['year']==y]['semester'].unique()):
                labels.append(f"Y{y} S{s}")
                sgpa = my_data[(my_data['year']==y)&(my_data['semester']==s)].iloc[0]['semester_gpa']
                perf.append(sgpa)

        st.subheader("📈 Academic Progress")
        st.plotly_chart(plot_progress(labels, perf), use_container_width=True)

        attendance_progress = get_attendance_progress_for_student(st.session_state.username)
        if attendance_progress is not None:
            st.subheader("📊 Attendance Progress")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Classes", attendance_progress['total'])
            with col2:
                st.metric("Present", attendance_progress['present'])
            with col3:
                st.metric("Absent", attendance_progress['absent'])
            with col4:
                st.metric("Attendance %", f"{attendance_progress['percentage']}%")

            st.progress(min(attendance_progress['percentage'] / 100.0, 1.0))

            if attendance_progress['percentage'] >= 85:
                st.success("🎉 Excellent attendance! Keep it up!")
            elif attendance_progress['percentage'] >= 75:
                st.warning("⚠️ Good attendance; try to reach 85%+")
            else:
                st.error("🚨 Low attendance; please improve your attendance")
        else:
            st.info("No attendance data available yet.")

    # ---------- Attendance ----------
    elif tab == "📅 Attendance":
        student_attendance()

    # ---------- Mid Exams ----------
    elif tab == "📊 Mid Exams":
        student_mid_marks_analysis()

    # ---------- Feedback ----------
    elif tab == "📝 Feedback":
        if not os.path.exists(FEEDBACK_FILE):
            pd.DataFrame(columns=["rollno","year","semester","feedback"]).to_csv(FEEDBACK_FILE, index=False)

        with st.form("feedback_form"):
            year = st.selectbox("Year", [1,2,3,4])
            semester = st.selectbox("Semester", [1,2])
            feedback_text = st.text_area("Your Feedback")

            if st.form_submit_button("Submit"):
                df_fb = pd.read_csv(FEEDBACK_FILE)
                new = pd.DataFrame([{
                    "rollno": st.session_state.username,
                    "year": year,
                    "semester": semester,
                    "feedback": feedback_text
                }])
                pd.concat([df_fb, new]).to_csv(FEEDBACK_FILE, index=False)
                st.success("Feedback submitted successfully ✅")

    # ---------- Announcements ----------
    elif tab == "📢 Announcements":
        df_ann = pd.read_csv(ANNOUNCEMENT_FILE)
        for _, row in df_ann.iterrows():
            st.markdown(f"### {row['title']}\n**By:** {row['posted_by']} | **Date:** {row['date']}\n{row['message']}\n---")

    # ---------- Messages (Attendance + Faculty) ----------
    elif tab == "💬 Messages":
        st.subheader("💬 Messages from Faculty / Attendance Alerts")
        if os.path.exists("data/messages.csv"):
            df_msg = pd.read_csv("data/messages.csv")
            my_msgs = df_msg[df_msg["receiver"].astype(str).str.lower() == st.session_state.username.strip().lower()]
            if my_msgs.empty:
                st.info("No messages yet.")
            else:
                for _, row in my_msgs.iterrows():
                    st.markdown(f"**From:** {row['sender']}  \n**Date:** {row['date']}  \n{row['message']}\n---")
        else:
            st.info("No messages yet.")

    # ---------- AI Prediction ----------
    elif tab == "🤖 AI Prediction":
        st.subheader("🤖 Next Semester SGPA Prediction")
        pred, r2, feat_imp = ai_prediction(st.session_state.username)
        if pred is not None:
            st.success(f"Predicted Next Semester SGPA: {pred} (R² Score: {round(r2,2)})")
            st.subheader("Feature Importance")
            st.dataframe(feat_imp)
        else:
            st.info("Not enough data for AI prediction yet.")
