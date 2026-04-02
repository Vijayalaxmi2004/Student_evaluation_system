import streamlit as st
import pandas as pd
from auth import FEEDBACK_FILE, ANNOUNCEMENT_FILE
from datetime import datetime
import os
from attendance import faculty_attendance
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from utils import COURSE_STRUCTURE, plot_marks, plot_progress
import plotly.express as px

GRADES_FILE = "data/grades_db.csv"

# ---------- CSS ----------
def load_css():
    st.markdown("""
    <style> 
    /* Main Background with soft gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f4f7fb, #e9eff7);
    }
    
    /* Sidebar Styling to match theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3A8A, #2563EB);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Modern Card Container */
    .card {
        background: white; 
        padding: 25px; 
        border-radius: 18px; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.08); 
        margin-bottom: 20px;
    }

    /* Faculty Dashboard Buttons - main content cards */
    .stButton>button {
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

    .stButton>button:hover {
        background: linear-gradient(135deg,#2563EB,#60A5FA) !important;
        color: white !important;
        transform: translateY(-4px) !important;
        box-shadow: 0px 14px 32px rgba(37,99,235,0.3) !important;
        border: none !important;
    }

    /* Sidebar profile/logout button style (override global stButton) */
    [data-testid="stSidebar"] .stButton>button,
    [data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border-radius: 22px !important;
        border: none !important;
        min-height: 60px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 24px rgba(102,126,234,0.4) !important;
    }

    [data-testid="stSidebar"] .stButton>button:hover,
    [data-testid="stSidebar"] button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 12px 28px rgba(118,74,162,0.5) !important;
        background: linear-gradient(135deg, #5f72ff, #7b3fdd) !important;
    }
    

    /* Attendance Cards Styling */
    .attendance-card {
        border-radius: 12px !important;
        padding: 15px !important;
        margin: 8px 0 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
        border: 2px solid transparent !important;
    }

    .attendance-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
    }

    .present-card {
        background: linear-gradient(135deg, #d4edda, #c3e6cb) !important;
        border-color: #28a745 !important;
    }

    .absent-card {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb) !important;
        border-color: #dc3545 !important;
    }

    /* Bulk Action Buttons */
    .bulk-btn {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3) !important;
    }

    .bulk-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, #5a67d8, #6b46c1) !important;
    }

    /* Progress Bar Styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #48bb78, #38a169) !important;
        border-radius: 10px !important;
    }

    /* Submit Button Animation */
    .submit-btn {
        background: linear-gradient(135deg, #48bb78, #38a169) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 12px rgba(72, 187, 120, 0.3) !important;
        transition: all 0.3s ease !important;
        animation: pulse 2s infinite !important;
    }

    .submit-btn:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 16px rgba(72, 187, 120, 0.4) !important;
        background: linear-gradient(135deg, #38a169, #2f855a) !important;
    }

    @keyframes pulse {
        0% { box-shadow: 0 6px 12px rgba(72, 187, 120, 0.3); }
        50% { box-shadow: 0 8px 16px rgba(72, 187, 120, 0.5); }
        100% { box-shadow: 0 6px 12px rgba(72, 187, 120, 0.3); }
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- Faculty Attendance with Auto-Messaging ----------
def faculty_attendance_auto(df):
    st.subheader("📝 Smart Attendance Management System")

    # Initialize attendance file if it doesn't exist
    ATT_FILE = "data/attendance.csv"
    if not os.path.exists(ATT_FILE):
        pd.DataFrame(columns=["date", "rollno", "name", "year", "semester", "status"]).to_csv(ATT_FILE, index=False)

    # Check if attendance file has correct structure
    existing_attendance = pd.read_csv(ATT_FILE)
    required_columns = ["date", "rollno", "name", "year", "semester", "status"]

    if not all(col in existing_attendance.columns for col in required_columns):
        st.warning("⚠️ Attendance file structure is incorrect. Resetting attendance data.")
        pd.DataFrame(columns=required_columns).to_csv(ATT_FILE, index=False)
        existing_attendance = pd.DataFrame(columns=required_columns)

    # Get current date
    current_date = pd.Timestamp.now().strftime("%Y-%m-%d")

    # Check if attendance already marked for today
    today_attendance = existing_attendance[existing_attendance['date'] == current_date]

    if not today_attendance.empty:
        st.warning(f"⚠️ Attendance already marked for {current_date}. You can update existing records.")
        show_existing = st.checkbox("Show existing attendance")
        if show_existing:
            st.dataframe(today_attendance, use_container_width=True)

    # Filter students for current class
    year = st.selectbox("Select Year", sorted(df['year'].unique()), key="att_year")
    semester = st.selectbox("Select Semester", sorted(df['semester'].unique()), key="att_sem")

    class_students = df[(df['year'] == year) & (df['semester'] == semester)].copy()
    class_students = class_students[['rollno', 'name']].drop_duplicates()

    if class_students.empty:
        st.warning("No students found for the selected year and semester.")
        return

    st.markdown(f"### 📋 Attendance for Year {year}, Semester {semester}")
    st.markdown(f"**Total Students:** {len(class_students)}")

    # Add bulk action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("✅ Mark All Present", use_container_width=True):
            st.session_state['bulk_action'] = 'all_present'
            st.rerun()
    with col2:
        if st.button("❌ Mark All Absent", use_container_width=True):
            st.session_state['bulk_action'] = 'all_absent'
            st.rerun()
    with col3:
        if st.button("🔀 Random Check", use_container_width=True):
            st.session_state['bulk_action'] = 'random_check'
            st.rerun()
    with col4:
        if st.button("🔄 Reset All", use_container_width=True):
            st.session_state['bulk_action'] = 'reset'
            st.rerun()

    # Handle bulk actions
    if 'bulk_action' in st.session_state:
        if st.session_state['bulk_action'] == 'all_present':
            for idx in class_students.index:
                st.session_state[f'att_status_{idx}'] = True
            st.success("✅ All students marked as Present!")
        elif st.session_state['bulk_action'] == 'all_absent':
            for idx in class_students.index:
                st.session_state[f'att_status_{idx}'] = False
            st.success("❌ All students marked as Absent!")
        elif st.session_state['bulk_action'] == 'random_check':
            import random
            random_students = random.sample(list(class_students.index), min(3, len(class_students)))
            for idx in class_students.index:
                st.session_state[f'att_status_{idx}'] = idx in random_students
            st.info(f"🎯 Random check: {len(random_students)} students selected for verification!")
        elif st.session_state['bulk_action'] == 'reset':
            for idx in class_students.index:
                if f'att_status_{idx}' in st.session_state:
                    del st.session_state[f'att_status_{idx}']
            st.info("🔄 All selections reset!")
        del st.session_state['bulk_action']

    # Create attendance form with impressive UI
    st.markdown("---")

    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        col1, col2, col3 = st.columns(3)
        with col1:
            group_size = st.slider("Group Size for Sectioned Attendance", 5, 20, 10)
        with col2:
            show_stats = st.checkbox("Show Live Statistics", value=True)
        with col3:
            auto_save = st.checkbox("Auto-save Progress", value=False)

    # Sectioned attendance (divide students into groups)
    sections = [class_students[i:i + group_size] for i in range(0, len(class_students), group_size)]
    section_names = [f"Section {i+1} ({len(section)} students)" for i, section in enumerate(sections)]

    if len(sections) > 1:
        selected_section = st.selectbox("📚 Select Section to Mark", section_names, key="section_select")
        section_idx = section_names.index(selected_section)
        current_section = sections[section_idx]

        st.markdown(f"### 🎯 {selected_section}")
        # Show progress for current section
        section_progress = sum(1 for idx in current_section.index if f'att_status_{idx}' in st.session_state)
        st.progress(section_progress / len(current_section))
        st.caption(f"Section Progress: {section_progress}/{len(current_section)} students marked")
    else:
        current_section = class_students

    # Progress tracking
    total_students = len(class_students)
    marked_students = sum(1 for idx in class_students.index if f'att_status_{idx}' in st.session_state)
    progress = marked_students / total_students if total_students > 0 else 0

    st.markdown(f"**Progress:** {marked_students}/{total_students} students marked")
    st.progress(progress)

    # Quick attendance mode toggle
    quick_mode = st.checkbox("⚡ Quick Mode: Click student names to toggle attendance", value=False)

    if quick_mode:
        st.info("💡 Click on any student name below to quickly toggle their attendance status!")

    # Create a grid layout for attendance marking
    cols = st.columns(3)  # 3 columns for better space utilization

    attendance_data = []

    for idx, (_, row) in enumerate(current_section.iterrows()):
        col_idx = idx % 3
        with cols[col_idx]:
            with st.container():
                # Student card design
                status_key = f'att_status_{row.name}'

                # Check if student already has attendance for today
                existing_record = today_attendance[today_attendance['rollno'].astype(str) == str(row['rollno'])]
                default_present = existing_record.empty or existing_record.iloc[0]['status'] == 'Present'

                # Get current status from session state or default
                is_present = st.session_state.get(status_key, default_present)

                # Color-coded card based on status
                card_class = "present-card" if is_present else "absent-card"

                # Quick mode: clickable student name
                if quick_mode:
                    if st.button(f"{row['rollno']} - {row['name']}", key=f"quick_{row.name}", use_container_width=True):
                        st.session_state[status_key] = not is_present
                        st.rerun()
                    is_present = st.session_state.get(status_key, default_present)

                st.markdown(f"""
                <div class="attendance-card {card_class}">
                    <strong style="font-size: 14px; color: #333;">{row['rollno']}</strong><br>
                    <span style="font-size: 12px; color: #666;">{row['name']}</span>
                    <div style="margin-top: 8px; font-size: 16px; font-weight: bold;">
                        {'✅ Present' if is_present else '❌ Absent'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Checkbox for attendance (only show if not in quick mode)
                if not quick_mode:
                    is_present = st.checkbox(
                        f"Toggle Status",
                        value=is_present,
                        key=status_key,
                        label_visibility="collapsed"
                    )

                attendance_data.append({
                    "date": current_date,
                    "rollno": str(row['rollno']),
                    "name": row['name'],
                    "year": year,
                    "semester": semester,
                    "status": "Present" if is_present else "Absent"
                })

    # Live statistics (if enabled)
    if show_stats and marked_students > 0:
        st.markdown("### 📊 Live Attendance Statistics")
        stats_cols = st.columns(4)
        with stats_cols[0]:
            st.metric("Marked", marked_students)
        with stats_cols[1]:
            present_now = sum(1 for data in attendance_data if data['status'] == 'Present')
            st.metric("Present", present_now)
        with stats_cols[2]:
            absent_now = sum(1 for data in attendance_data if data['status'] == 'Absent')
            st.metric("Absent", absent_now)
        with stats_cols[3]:
            attendance_rate = (present_now / len(attendance_data) * 100) if attendance_data else 0
            st.metric("Rate", f"{attendance_rate:.1f}%")

    # Submit section with enhanced UI
    st.markdown("---")

    # Summary before submission
    present_count = sum(1 for data in attendance_data if data['status'] == 'Present')
    absent_count = total_students - present_count

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Present", present_count, delta=f"{present_count/total_students*100:.1f}%" if total_students > 0 else "0%")
    with col2:
        st.metric("Absent", absent_count, delta=f"{absent_count/total_students*100:.1f}%" if total_students > 0 else "0%")
    with col3:
        st.metric("Total", total_students)

    # Submit button with confirmation
    if marked_students == total_students:
        if st.button("🚀 Submit Attendance", type="primary", use_container_width=True):
            try:
                # Remove existing records for today to avoid duplicates
                existing_attendance = existing_attendance[existing_attendance['date'] != current_date]

                # Add new attendance records
                new_attendance_df = pd.DataFrame(attendance_data)
                updated_attendance = pd.concat([existing_attendance, new_attendance_df], ignore_index=True)
                updated_attendance.to_csv(ATT_FILE, index=False)

                st.success("✅ Attendance submitted successfully!")

                # Show fireworks animation
                st.balloons()

                # Auto-send messages to students
                if st.checkbox("📤 Send notification messages to students?", value=True):
                    send_attendance_messages(new_attendance_df)

                # Clear session state
                for idx in class_students.index:
                    if f'att_status_{idx}' in st.session_state:
                        del st.session_state[f'att_status_{idx}']

            except Exception as e:
                st.error(f"❌ Error saving attendance: {str(e)}")
    else:
        st.warning(f"⚠️ Please mark attendance for all {total_students} students before submitting. ({marked_students}/{total_students} completed)")

    # Attendance Analytics Dashboard
    st.markdown("---")
    st.markdown("### 📈 Attendance Analytics Dashboard")

    if st.button("🔍 Generate Analytics Report", use_container_width=True):
        try:
            # Load attendance data
            attendance_df = pd.read_csv(ATT_FILE)

            # Convert date column to datetime
            attendance_df['date'] = pd.to_datetime(attendance_df['date'])

            # Filter for current class
            class_attendance = attendance_df[(attendance_df['year'] == year) & (attendance_df['semester'] == semester)]

            if not class_attendance.empty:
                # Overall statistics
                total_days = class_attendance['date'].nunique()
                total_students = class_attendance['rollno'].nunique()

                # Calculate attendance percentage for each student
                student_stats = class_attendance.groupby('rollno').agg({
                    'status': lambda x: (x == 'Present').sum(),
                    'name': 'first'
                }).reset_index()

                student_stats['total_classes'] = total_days
                student_stats['attendance_percentage'] = (student_stats['status'] / student_stats['total_classes'] * 100).round(1)

                # Display analytics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    avg_attendance = student_stats['attendance_percentage'].mean()
                    st.metric("Average Attendance", f"{avg_attendance:.1f}%")
                with col2:
                    highest_attendance = student_stats['attendance_percentage'].max()
                    st.metric("Highest Attendance", f"{highest_attendance:.1f}%")
                with col3:
                    lowest_attendance = student_stats['attendance_percentage'].min()
                    st.metric("Lowest Attendance", f"{lowest_attendance:.1f}%")
                with col4:
                    perfect_attendance = (student_stats['attendance_percentage'] == 100).sum()
                    st.metric("Perfect Attendance", f"{perfect_attendance} students")

                # Top 5 performers
                st.markdown("#### 🏆 Top 5 Attendance Performers")
                top_performers = student_stats.nlargest(5, 'attendance_percentage')[['name', 'rollno', 'attendance_percentage']]
                st.dataframe(top_performers, use_container_width=True)

                # Students needing attention (below 75%)
                low_attendance = student_stats[student_stats['attendance_percentage'] < 75]
                if not low_attendance.empty:
                    st.markdown("#### ⚠️ Students Needing Attention (< 75%)")
                    st.dataframe(low_attendance[['name', 'rollno', 'attendance_percentage']], use_container_width=True)

                # Daily attendance trend (last 7 days)
                last_week = class_attendance[class_attendance['date'] >= (pd.Timestamp.now() - pd.Timedelta(days=7))]
                if not last_week.empty:
                    daily_stats = last_week.groupby('date')['status'].apply(lambda x: (x == 'Present').sum()).reset_index()
                    daily_stats.columns = ['Date', 'Present Count']

                    st.markdown("#### 📅 Last 7 Days Trend")
                    st.line_chart(daily_stats.set_index('Date'))

            else:
                st.info("No attendance data available for the selected class yet.")

        except Exception as e:
            st.error(f"Error generating analytics: {str(e)}")

def send_attendance_messages(attendance_df):
    """Send attendance notification messages to students"""
    try:
        MESSAGES_FILE = "data/messages.csv"
        if not os.path.exists(MESSAGES_FILE):
            pd.DataFrame(columns=["sender","receiver","message","date"]).to_csv(MESSAGES_FILE, index=False)

        messages_df = pd.read_csv(MESSAGES_FILE)

        faculty_name = st.session_state.get("username", "Faculty")

        for _, row in attendance_df.iterrows():
            if row['status'] == 'Absent':
                msg = f"📌 Attendance Alert: You were marked {row['status']} for {row['date']} (Year {row['year']}, Sem {row['semester']})"
            else:
                msg = f"✅ Attendance Confirmed: You were marked {row['status']} for {row['date']} (Year {row['year']}, Sem {row['semester']})"

            new_msg = pd.DataFrame([{
                "sender": faculty_name,
                "receiver": str(row['rollno']),
                "message": msg,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }])

            messages_df = pd.concat([messages_df, new_msg], ignore_index=True)

        messages_df.to_csv(MESSAGES_FILE, index=False)
        st.success("📤 Attendance notifications sent to all students!")

    except Exception as e:
        st.error(f"❌ Error sending messages: {str(e)}")

# ---------- Dashboard ----------
def faculty_dashboard():
    load_css()
    
    # Enhanced Gradient Header
    st.markdown(f"""
    <div class="card" style="
        text-align:center;
        background: linear-gradient(135deg, #1E3A8A, #2563EB);
        color: white;
        border: none;
    ">
        <h1 style="font-size:45px; margin:0; color: white;">🛡️ Faculty Dashboard</h1>
        <p style="font-size:20px; opacity: 0.9;">Welcome back, 👤 {st.session_state.username}</p>
    </div>
    """, unsafe_allow_html=True)

    if "faculty_tab" not in st.session_state:
        st.session_state.faculty_tab = None

    # 🚨 HIGHLIGHT: Balanced 3-Column Grid Layout
    # This fixes the "scattered" look from your screenshot
    row1_c1, row1_c2, row1_c3 = st.columns(3)
    with row1_c1:
        if st.button("📊 Performance"):
            st.session_state.faculty_tab = "performance"
    with row1_c2:
        if st.button("📬 Feedback"):
            st.session_state.faculty_tab = "feedback"
    with row1_c3:
        if st.button("📌 Announcements"):
            st.session_state.faculty_tab = "announcements"
    
    row2_c1, row2_c2, row2_c3 = st.columns(3)
    with row2_c1:
        if st.button("📝 Attendance"):
            st.session_state.faculty_tab = "attendance"
    with row2_c2:
        if st.button("💬 Messages"):
            st.session_state.faculty_tab = "messages"
    with row2_c3:
        if st.button("📈 Analytics"):
            st.session_state.faculty_tab = "analytics"

    st.divider()

    # ================= STUDENT PERFORMANCE =================
    if st.session_state.faculty_tab == "performance":
        st.subheader("📊 Student Performance")
        file = st.sidebar.file_uploader("📂 Upload Class Database", type=["csv","xlsx"])
        if file:
            df = pd.read_csv(file) if file.name.endswith(".csv") else pd.concat(
                pd.read_excel(file, sheet_name=None)
            )
            df.columns = df.columns.str.strip().str.lower()
            year = st.selectbox("Select Year", sorted(df['year'].unique()))
            sem = st.selectbox("Select Semester", sorted(df['semester'].unique()))
            roll_search = st.text_input("🔍 Search by Roll Number")

            filtered_df = df[(df['year'] == year) & (df['semester'] == sem)]
            if roll_search:
                filtered_df = filtered_df[
                    filtered_df['rollno'].astype(str) == roll_search
                ]
            st.dataframe(filtered_df, use_container_width=True)
            if filtered_df.empty:
                st.warning("No data found")
                return

            cgpa_col = 'calculated_cgpa' if 'calculated_cgpa' in filtered_df.columns else 'cgpa'
            c1, c2, c3 = st.columns(3)
            c1.metric("Students", len(filtered_df))
            c2.metric("Average CGPA", round(filtered_df[cgpa_col].mean(), 2))
            c3.metric("Top CGPA", round(filtered_df[cgpa_col].max(), 2))

            # ===== RANDOM FOREST AI PREDICTION (per student) =====
            st.subheader("🔮 Predict Next Semester SGPA (Random Forest)")
            num_df = filtered_df.select_dtypes(include="number")
            if "semester_gpa" not in num_df.columns or len(num_df) <= 5:
                st.info("Not enough numeric data for AI prediction.")
            else:
                X = num_df.drop("semester_gpa", axis=1, errors='ignore')
                y = num_df["semester_gpa"]
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = RandomForestRegressor(
                    n_estimators=300,
                    max_depth=10,
                    min_samples_split=5,    
                    random_state=42
                )
                model.fit(X_train, y_train)
                r2 = r2_score(y_test, model.predict(X_test))
                st.info(f"Model Accuracy (R² Score): {round(r2,2)}")
                feat_imp = pd.DataFrame({'Feature': X.columns,'Importance': model.feature_importances_}).sort_values(by='Importance', ascending=False)

                st.markdown("**Enter Roll Number for Prediction**")
                student_roll = st.text_input("Roll Number")
                if student_roll:
                    student_row = filtered_df[filtered_df['rollno'].astype(str) == student_roll]
                    if not student_row.empty:
                        sample = student_row[X.columns].iloc[[0]]
                        pred = model.predict(sample)[0]
                        st.success(f"Predicted SGPA for {student_roll}: {round(pred,2)}")
                        st.subheader(f"Feature Importance for {student_roll}")
                        fig = px.bar(feat_imp, x='Feature', y='Importance', title=f"Feature Importance for {student_roll}")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Roll number not found.")

    # ================= FEEDBACK =================
    elif st.session_state.faculty_tab == "feedback":
        st.subheader("📬 Student Feedback")
        if os.path.exists(FEEDBACK_FILE):
            df = pd.read_csv(FEEDBACK_FILE)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No feedback yet.")

    # ================= ANNOUNCEMENTS =================
    elif st.session_state.faculty_tab == "announcements":
        st.subheader("📌 Announcements")
        if not os.path.exists(ANNOUNCEMENT_FILE):
            pd.DataFrame(columns=["date","title","message","posted_by"]).to_csv(ANNOUNCEMENT_FILE, index=False)
        with st.form("announce"):
            title = st.text_input("Title")
            msg = st.text_area("Message")
            if st.form_submit_button("Post"):
                df = pd.read_csv(ANNOUNCEMENT_FILE)
                new = pd.DataFrame([{"date": datetime.now(),"title": title,"message": msg,"posted_by": st.session_state.get("username","faculty")}])
                pd.concat([df,new]).to_csv(ANNOUNCEMENT_FILE,index=False)
                st.success("Posted!")
        st.dataframe(pd.read_csv(ANNOUNCEMENT_FILE))

    # ================= ATTENDANCE =================
    elif st.session_state.faculty_tab == "attendance":
        st.subheader("📝 Student Attendance Management")

        # Load student data from grades database
        if os.path.exists(GRADES_FILE):
            df = pd.read_csv(GRADES_FILE)
            df.columns = df.columns.str.strip().str.lower()

            # Check if required columns exist
            required_cols = ['rollno', 'name', 'year', 'semester']
            if all(col in df.columns for col in required_cols):
                faculty_attendance_auto(df)
            else:
                st.error("❌ Grades database is missing required columns (rollno, name, year, semester)")
                st.info("Please ensure your grades database has all required student information.")
        else:
            st.warning("⚠️ Grades database not found. Please upload student data first.")
            st.info("💡 Upload student grades data in the Performance tab to enable attendance management.")

            # Fallback: Allow manual upload
            file = st.file_uploader("📂 Upload Student List (CSV/Excel)", type=["csv","xlsx"], key="att_fallback")
            if file:
                df = pd.read_csv(file) if file.name.endswith(".csv") else pd.concat(pd.read_excel(file, sheet_name=None))
                df.columns = df.columns.str.strip().str.lower()
                faculty_attendance_auto(df)

    # ================= MESSAGES =================
    elif st.session_state.faculty_tab == "messages":
        st.subheader("💬 Send Message to Student")
        users = pd.read_csv("data/users_db.csv")
        students = users[users["role"] == "Student"]["username"].tolist()
        receiver = st.selectbox("Select Student", students)
        msg = st.text_area("Message")
        if st.button("Send"):
            df = pd.read_csv("data/messages.csv")
            new = pd.DataFrame([{"sender": st.session_state.username,"receiver": receiver,"message": msg,"date": datetime.now()}])
            pd.concat([df,new]).to_csv("data/messages.csv", index=False)
            st.success("Message sent!")

    # ================= ANALYTICS / RISK =================
    elif st.session_state.faculty_tab == "analytics":
        tab1, tab2 = st.tabs(["📊 Performance Analytics", "📋 Attendance Reports"])

        with tab1:
            if os.path.exists(GRADES_FILE):
                df = pd.read_csv(GRADES_FILE)
                df.columns = df.columns.str.strip().str.lower()

                # Risk analysis for students
                st.subheader("🚨 At-Risk Students Analysis")

                if 'semester_gpa' in df.columns:
                    risk_threshold = st.slider("Risk Threshold (SGPA)", 0.0, 10.0, 7.0, 0.1)

                    risk_df = df[df['semester_gpa'] < risk_threshold].copy()
                    risk_df = risk_df[['rollno', 'name', 'year', 'semester', 'semester_gpa']].sort_values('semester_gpa')

                    if not risk_df.empty:
                        st.dataframe(risk_df, use_container_width=True)

                        # Risk distribution chart
                        risk_by_year_sem = risk_df.groupby(['year', 'semester']).size().reset_index(name='count')
                        fig = px.bar(risk_by_year_sem, x='year', y='count', color='semester',
                                   title=f'Students Below {risk_threshold} SGPA')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.success(f"✅ No students below {risk_threshold} SGPA!")
                else:
                    st.warning("Semester GPA data not found in grades database.")

                st.subheader("📊 Department-wise Analytics")
                if 'department' in df.columns:
                    fig = px.pie(df, names='department', title="Students by Department")
                    st.plotly_chart(fig)
                if 'semester' in df.columns:
                    avg_gpa = df.groupby('semester')['semester_gpa'].mean().reset_index()
                    fig2 = px.bar(avg_gpa, x='semester', y='semester_gpa', title="Average GPA per Semester")
                    st.plotly_chart(fig2)
            else:
                st.info("Upload grades data to view analytics.")

        with tab2:
            st.subheader("📋 Attendance Reports")

            ATTENDANCE_FILE = "data/attendance.csv"
            if os.path.exists(ATTENDANCE_FILE):
                try:
                    att_df = pd.read_csv(ATTENDANCE_FILE)
                    required_columns = ["date", "rollno", "name", "year", "semester", "status"]

                    if not all(col in att_df.columns for col in required_columns):
                        st.error("❌ Attendance data structure is incorrect. Please reset attendance records.")
                    else:
                        # Attendance summary
                        total_records = len(att_df)
                        present_count = len(att_df[att_df['status'] == 'Present'])
                        absent_count = total_records - present_count

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Records", total_records)
                        with col2:
                            st.metric("Present", present_count)
                        with col3:
                            st.metric("Absent", absent_count)

                        # Class-wise attendance
                        if not att_df.empty:
                            st.markdown("### 📊 Class-wise Attendance Summary")

                            class_summary = att_df.groupby(['year', 'semester']).agg({
                                'status': lambda x: (x == 'Present').sum(),
                                'rollno': 'count'
                            }).rename(columns={'status': 'present', 'rollno': 'total'}).reset_index()

                            class_summary['absent'] = class_summary['total'] - class_summary['present']
                            class_summary['attendance_rate'] = round((class_summary['present'] / class_summary['total']) * 100, 2)

                            st.dataframe(class_summary, use_container_width=True)

                            # Low attendance alert
                            low_attendance_classes = class_summary[class_summary['attendance_rate'] < 75]
                            if not low_attendance_classes.empty:
                                st.warning("⚠️ Classes with low attendance (< 75%):")
                                for _, row in low_attendance_classes.iterrows():
                                    st.write(f"- Year {row['year']}, Semester {row['semester']}: {row['attendance_rate']}%")

                            # Individual student attendance
                            st.markdown("### 👤 Individual Student Attendance")

                            # Get unique students
                            students = att_df[['rollno', 'name']].drop_duplicates()

                            student_attendance = []
                            for _, student in students.iterrows():
                                student_records = att_df[att_df['rollno'].astype(str) == str(student['rollno'])]
                                total = len(student_records)
                                present = len(student_records[student_records['status'] == 'Present'])
                                percentage = round((present / total) * 100, 2) if total > 0 else 0

                                student_attendance.append({
                                    'rollno': student['rollno'],
                                    'name': student['name'],
                                    'total_classes': total,
                                    'present': present,
                                    'absent': total - present,
                                    'attendance_percentage': percentage
                                })

                            student_df = pd.DataFrame(student_attendance).sort_values('attendance_percentage')

                            # Color coding for attendance percentage
                            def color_attendance(val):
                                if val >= 85:
                                    return 'color: green'
                                elif val >= 75:
                                    return 'color: orange'
                                else:
                                    return 'color: red'

                            styled_df = student_df.style.applymap(color_attendance, subset=['attendance_percentage'])
                            st.dataframe(styled_df, use_container_width=True)

                            # Export option
                            if st.button("📥 Export Attendance Report"):
                                csv_data = student_df.to_csv(index=False)
                                st.download_button(
                                    label="Download CSV",
                                    data=csv_data,
                                    file_name=f"attendance_report_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                                    mime="text/csv"
                                )
                except Exception as e:
                    st.error(f"❌ Error reading attendance file: {str(e)}")
            else:
                st.info("No attendance data available yet.")
