# attendance.py
import streamlit as st
import pandas as pd
import os

ATTENDANCE_FILE = "data/attendance.csv"

# ================= FACULTY =================
def faculty_attendance(df):
    st.subheader("📝 Mark Student Attendance")

    # Choose attendance type
    att_type = st.radio(
        "Choose Attendance Type",
        ["Daily Attendance", "Subject-wise Attendance"]
    )

    if not os.path.exists(ATTENDANCE_FILE):
        pd.DataFrame(
            columns=["date", "rollno", "name", "year", "semester", "subject", "status", "type"]
        ).to_csv(ATTENDANCE_FILE, index=False)

    year = st.selectbox("Select Year", sorted(df['year'].unique()))
    sem = st.selectbox("Select Semester", sorted(df['semester'].unique()))

    subject = None
    if att_type == "Subject-wise Attendance":
        subject = st.text_input("Enter Subject Name")

    class_df = df[(df['year'] == year) & (df['semester'] == sem)]
    if 'name' in class_df.columns:
        class_df = class_df[['rollno', 'name']].drop_duplicates()
    else:
        class_df = class_df[['rollno']].drop_duplicates()

    attendance_records = []

    st.markdown("### Mark Attendance")

    for idx, row in class_df.iterrows():
        col1, col2 = st.columns([2, 2])
        with col1:
            st.write(row["rollno"])
        with col2:
            status = st.selectbox(
                "Status",
                ["Present", "Absent"],
                key=f"att_{att_type}_{year}_{sem}_{idx}"
            )

        attendance_records.append({
            "date": pd.Timestamp.now().strftime("%Y-%m-%d"),
            "rollno": str(row["rollno"]),
            "name": str(row.get("name", "")).strip() if "name" in row else "",
            "year": year,
            "semester": sem,
            "subject": subject if subject else "Overall",
            "status": status,
            "type": att_type
        })

    if st.button("💾 Save Attendance"):
        att_df = pd.read_csv(ATTENDANCE_FILE)
        new_df = pd.DataFrame(attendance_records)
        pd.concat([att_df, new_df]).to_csv(ATTENDANCE_FILE, index=False)
        st.success("✅ Attendance saved successfully!")


# ================= STUDENT =================
def student_attendance():
    st.subheader("📊 My Attendance Report")

    ATTENDANCE_FILE = "data/attendance.csv"
    if not os.path.exists(ATTENDANCE_FILE):
        st.info("📝 No attendance records found yet.")
        return

    # Check if attendance file has correct structure
    try:
        df = pd.read_csv(ATTENDANCE_FILE)
        required_columns = ["date", "rollno", "year", "semester", "status"]

        if not all(col in df.columns for col in required_columns):
            st.error("❌ Attendance data structure is incorrect. Please contact faculty to reset attendance records.")
            return

        # Add missing optional column for compatibility
        if 'name' not in df.columns:
            df['name'] = ""

    except Exception as e:
        st.error(f"❌ Error reading attendance file: {str(e)}")
        return

    roll = str(st.session_state.username).strip().lower()

    # Filter student's attendance (case-insensitive)
    my_df = df[df['rollno'].astype(str).str.strip().str.lower() == roll].copy()

    if my_df.empty:
        st.info("📝 No attendance records found for your account.")
        return

    # Convert date column to datetime for better analysis
    my_df['date'] = pd.to_datetime(my_df['date'])

    # Choose attendance view
    view_type = st.radio(
        "📋 View Options",
        ["Overall Summary", "Detailed Records", "Monthly Analysis"],
        horizontal=True
    )

    if view_type == "Overall Summary":
        # Overall attendance statistics
        total_classes = len(my_df)
        present_count = len(my_df[my_df['status'] == "Present"])
        absent_count = total_classes - present_count

        if total_classes > 0:
            attendance_percentage = round((present_count / total_classes) * 100, 2)
        else:
            attendance_percentage = 0.0

        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📚 Total Classes", total_classes)
        with col2:
            st.metric("✅ Present", present_count)
        with col3:
            st.metric("❌ Absent", absent_count)
        with col4:
            st.metric("📊 Attendance %", f"{attendance_percentage}%")

        # Attendance status indicator
        if attendance_percentage >= 85:
            st.success("🎉 Excellent attendance! Keep it up!")
        elif attendance_percentage >= 75:
            st.warning("⚠️ Good attendance, but try to attend more classes.")
        else:
            st.error("🚨 Low attendance! Please improve your attendance.")

        # Recent attendance (last 10 records)
        st.markdown("### 🕐 Recent Attendance")
        recent_df = my_df.sort_values('date', ascending=False).head(10)
        recent_df['date'] = recent_df['date'].dt.strftime('%Y-%m-%d')

        # Color coding for status
        def color_status(val):
            color = 'green' if val == 'Present' else 'red'
            return f'color: {color}'

        styled_df = recent_df[['date', 'status']].style.applymap(color_status, subset=['status'])
        st.dataframe(styled_df, use_container_width=True)

    elif view_type == "Detailed Records":
        # Filter options
        col1, col2 = st.columns(2)

        with col1:
            year_filter = st.multiselect(
                "Filter by Year",
                options=sorted(my_df['year'].unique()),
                default=sorted(my_df['year'].unique())
            )

        with col2:
            semester_filter = st.multiselect(
                "Filter by Semester",
                options=sorted(my_df['semester'].unique()),
                default=sorted(my_df['semester'].unique())
            )

        # Apply filters
        filtered_df = my_df[
            my_df['year'].isin(year_filter) &
            my_df['semester'].isin(semester_filter)
        ].copy()

        if filtered_df.empty:
            st.warning("No records found for the selected filters.")
            return

        # Sort by date (newest first)
        filtered_df = filtered_df.sort_values('date', ascending=False)
        filtered_df['date'] = filtered_df['date'].dt.strftime('%Y-%m-%d')

        st.markdown(f"### 📋 Detailed Records ({len(filtered_df)} entries)")

        # Color coding for status
        def color_status(val):
            color = 'green' if val == 'Present' else 'red'
            return f'color: {color}'

        styled_df = filtered_df[['date', 'year', 'semester', 'status']].style.applymap(color_status, subset=['status'])
        st.dataframe(styled_df, use_container_width=True)

        # Export option
        if st.button("📥 Export to CSV"):
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"attendance_{roll}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    elif view_type == "Monthly Analysis":
        # Monthly attendance analysis
        my_df['month_year'] = my_df['date'].dt.to_period('M').astype(str)

        monthly_stats = my_df.groupby('month_year').agg({
            'status': lambda x: (x == 'Present').sum(),
            'date': 'count'
        }).rename(columns={'status': 'present', 'date': 'total'}).reset_index()

        monthly_stats['absent'] = monthly_stats['total'] - monthly_stats['present']
        monthly_stats['percentage'] = round((monthly_stats['present'] / monthly_stats['total']) * 100, 2)

        st.markdown("### 📈 Monthly Attendance Analysis")

        if not monthly_stats.empty:
            # Display monthly statistics
            st.dataframe(
                monthly_stats[['month_year', 'total', 'present', 'absent', 'percentage']],
                use_container_width=True
            )

            # Monthly attendance chart
            import plotly.express as px

            fig = px.bar(
                monthly_stats,
                x='month_year',
                y='percentage',
                title='Monthly Attendance Percentage',
                labels={'month_year': 'Month-Year', 'percentage': 'Attendance %'},
                color='percentage',
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data for monthly analysis.")


