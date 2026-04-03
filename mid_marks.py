import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

MID_MARKS_FILE = "data/mid_marks.csv"

# ================= Initialize Mid Marks Database =================
def init_mid_marks_db():
    """Initialize the mid marks database if it doesn't exist"""
    if not os.path.exists(MID_MARKS_FILE):
        pd.DataFrame(columns=[
            "rollno", "name", "year", "semester", "subject", 
            "mid1_marks", "mid2_marks", "mid_average", "date_updated"
        ]).to_csv(MID_MARKS_FILE, index=False)

# ================= FACULTY - Enter Mid Marks =================
def faculty_mid_marks_entry(df):
    """Faculty interface to enter mid exam marks"""
    st.subheader("📝 Mid Exam Marks Entry")
    
    init_mid_marks_db()
    
    # Create tabs for upload or manual entry
    tab1, tab2 = st.tabs(["📤 Upload Marks File", "✍️ Manual Entry"])
    
    # ===== TAB 1: FILE UPLOAD =====
    with tab1:
        st.markdown("### 📤 Upload Mid Marks from File")
        st.info("📋 Upload a CSV or Excel file with mid mark data. Format should have columns: rollno, name, year, semester, subject, mid1_marks, mid2_marks")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose mid marks file (CSV/Excel)",
            type=["csv", "xlsx", "xls"],
            key="mid_marks_upload"
        )
        
        if uploaded_file is not None:
            try:
                # Read the file
                if uploaded_file.name.endswith('.csv'):
                    file_df = pd.read_csv(uploaded_file)
                else:
                    file_df = pd.read_excel(uploaded_file)
                
                # Clean column names (strip whitespace, lowercase)
                file_df.columns = file_df.columns.str.strip().str.lower()
                
                # Validate required columns
                required_cols = ['rollno', 'year', 'semester', 'subject', 'mid1_marks', 'mid2_marks']
                missing_cols = [col for col in required_cols if col not in file_df.columns]
                
                if missing_cols:
                    st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                    st.info("Required columns: rollno, year, semester, subject, mid1_marks, mid2_marks")
                    return
                
                # Add name if not present
                if 'name' not in file_df.columns:
                    # Try to get names from main dataframe
                    file_df['name'] = file_df['rollno'].apply(
                        lambda x: df[df['rollno'].astype(str) == str(x)]['name'].iloc[0] 
                        if not df[df['rollno'].astype(str) == str(x)].empty 
                        else ""
                    )
                
                # Calculate mid_average
                file_df['mid_average'] = round((file_df['mid1_marks'] + file_df['mid2_marks']) / 2, 2)
                file_df['date_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Validate marks range
                invalid_rows = file_df[
                    ((file_df['mid1_marks'] < 0) | (file_df['mid1_marks'] > 100)) |
                    ((file_df['mid2_marks'] < 0) | (file_df['mid2_marks'] > 100))
                ]
                
                if not invalid_rows.empty:
                    st.warning("⚠️ Some rows have marks outside 0-100 range:")
                    st.dataframe(invalid_rows, use_container_width=True)
                    st.info("Please fix these values in your file and re-upload.")
                    return
                
                # Display preview
                st.markdown("### 📋 Preview of Uploaded Data")
                st.dataframe(file_df, use_container_width=True)
                
                st.markdown(f"**Total Records:** {len(file_df)}")
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Avg Mid 1", f"{file_df['mid1_marks'].mean():.2f}")
                with col2:
                    st.metric("Avg Mid 2", f"{file_df['mid2_marks'].mean():.2f}")
                with col3:
                    st.metric("Overall Avg", f"{file_df['mid_average'].mean():.2f}")
                
                # Confirm and save
                if st.button("✅ Confirm & Save All Marks", type="primary", use_container_width=True):
                    try:
                        # Load existing marks
                        mid_df = pd.read_csv(MID_MARKS_FILE)
                        
                        # Get unique year-semester-subject combinations from upload
                        for (year, sem, subject), group in file_df.groupby(['year', 'semester', 'subject']):
                            # Remove existing marks for this combination
                            mid_df = mid_df[
                                ~((mid_df['year'] == year) & 
                                  (mid_df['semester'] == sem) & 
                                  (mid_df['subject'] == subject))
                            ]
                        
                        # Add new marks
                        final_df = pd.concat([mid_df, file_df[['rollno', 'name', 'year', 'semester', 'subject', 'mid1_marks', 'mid2_marks', 'mid_average', 'date_updated']]], ignore_index=True)
                        final_df.to_csv(MID_MARKS_FILE, index=False)
                        
                        st.success(f"✅ Successfully uploaded {len(file_df)} mark records!")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"❌ Error saving uploaded marks: {str(e)}")
            
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
        
        # Download template
        st.markdown("---")
        st.markdown("### 📥 Download Template")
        
        template_df = pd.DataFrame({
            'rollno': ['HT1001', 'HT1002', 'HT1003'],
            'name': ['Student 1', 'Student 2', 'Student 3'],
            'year': [1, 1, 1],
            'semester': [1, 1, 1],
            'subject': ['Matrices and Calculus', 'Matrices and Calculus', 'Matrices and Calculus'],
            'mid1_marks': [85.5, 90.0, 78.5],
            'mid2_marks': [87.0, 92.5, 80.0]
        })
        
        csv_template = template_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV Template",
            data=csv_template,
            file_name="mid_marks_template.csv",
            mime="text/csv"
        )
    
    # ===== TAB 2: MANUAL ENTRY =====
    with tab2:
        st.markdown("### ✍️ Manual Entry of Mid Marks")
        
        # Select year and semester
        col1, col2 = st.columns(2)
        with col1:
            year = st.selectbox("Select Year", sorted(df['year'].unique()), key="mid_year_manual")
        with col2:
            semester = st.selectbox("Select Semester", sorted(df['semester'].unique()), key="mid_sem_manual")
        
        # Filter students for selected year and semester
        class_df = df[(df['year'] == year) & (df['semester'] == semester)].copy()
        if 'name' in class_df.columns:
            class_df = class_df[['rollno', 'name']].drop_duplicates()
        else:
            class_df = class_df[['rollno']].drop_duplicates()
        
        if class_df.empty:
            st.warning("No students found for selected year and semester.")
            return
        
        # Get subjects for this semester
        from utils import get_department_courses
        
        # Get a sample student to determine department (assuming department info available)
        sample_student = class_df.iloc[0]['rollno']
        
        # Try to get department from the main dataframe
        sample_row = df[df['rollno'].astype(str) == str(sample_student)]
        if 'department' in df.columns and not sample_row.empty:
            department = sample_row.iloc[0]['department']
        else:
            department = "CSE"  # Default department
        
        subjects = get_department_courses(department, year, semester)
        
        if not subjects:
            st.warning("No subjects configured for this year and semester.")
            return
        
        st.markdown(f"### 📋 Mid Exam Marks | Year {year}, Semester {semester}")
        st.markdown(f"**Total Students:** {len(class_df)} | **Total Subjects:** {len(subjects)}")
        
        # Select subject
        subject = st.selectbox("Select Subject", subjects, key="mid_subject")
        
        # Load existing mid marks
        mid_df = pd.read_csv(MID_MARKS_FILE)
        
        st.markdown("---")
        st.markdown(f"### Enter marks for **{subject}**")
        
        # Create input form
        mid_marks_data = []
        cols = st.columns(4)
        
        for idx, (_, student) in enumerate(class_df.iterrows()):
            rollno = str(student['rollno'])
            name = student.get('name', '') if pd.notna(student.get('name', '')) else ""
            
            # Get existing marks if any
            existing = mid_df[
                (mid_df['rollno'].astype(str) == rollno) & 
                (mid_df['subject'] == subject) &
                (mid_df['year'] == year) &
                (mid_df['semester'] == semester)
            ]
            
            default_mid1 = existing.iloc[0]['mid1_marks'] if not existing.empty and pd.notna(existing.iloc[0]['mid1_marks']) else 0.0
            default_mid2 = existing.iloc[0]['mid2_marks'] if not existing.empty and pd.notna(existing.iloc[0]['mid2_marks']) else 0.0
            
            col_idx = idx % 4
            if col_idx == 0:
                cols = st.columns(4)
            
            with cols[col_idx]:
                with st.container(border=True):
                    st.markdown(f"**{rollno}**")
                    if name:
                        st.caption(f"*{name}*")
                    
                    mid1 = st.number_input(
                        "Mid 1",
                        min_value=0.0, max_value=100.0,
                        value=float(default_mid1),
                        step=0.5,
                        key=f"mid1_{rollno}_{subject}"
                    )
                    
                    mid2 = st.number_input(
                        "Mid 2",
                        min_value=0.0, max_value=100.0,
                        value=float(default_mid2),
                        step=0.5,
                        key=f"mid2_{rollno}_{subject}"
                    )
                    
                    mid_avg = round((mid1 + mid2) / 2, 2)
                    st.metric("Avg", f"{mid_avg}")
                    
                    mid_marks_data.append({
                        "rollno": rollno,
                        "name": name,
                        "year": year,
                        "semester": semester,
                        "subject": subject,
                        "mid1_marks": mid1,
                        "mid2_marks": mid2,
                        "mid_average": mid_avg,
                        "date_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
        
        st.markdown("---")
        
        # Submit button
        if st.button("💾 Save Mid Marks", type="primary", use_container_width=True):
            try:
                # Remove existing marks for this subject/year/semester combo
                updated_mid_df = mid_df[
                    ~((mid_df['year'] == year) & 
                      (mid_df['semester'] == semester) & 
                      (mid_df['subject'] == subject))
                ]
                
                # Add new marks
                new_marks_df = pd.DataFrame(mid_marks_data)
                final_df = pd.concat([updated_mid_df, new_marks_df], ignore_index=True)
                final_df.to_csv(MID_MARKS_FILE, index=False)
                
                st.success("✅ Mid marks saved successfully!")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error saving marks: {str(e)}")


# ================= FACULTY - Mid Marks Analytics =================
def faculty_mid_marks_analytics(df):
    """Faculty analytics dashboard for mid marks"""
    st.subheader("📊 Mid Exam Analytics Dashboard")
    
    init_mid_marks_db()
    mid_df = pd.read_csv(MID_MARKS_FILE)
    
    if mid_df.empty:
        st.info("📭 No mid marks data available yet.")
        return
    
    # Select year and semester for analytics
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Select Year", sorted(mid_df['year'].unique()), key="ana_year")
    with col2:
        semester = st.selectbox("Select Semester", sorted(mid_df['semester'].unique()), key="ana_sem")
    
    # Filter data
    class_mid_df = mid_df[(mid_df['year'] == year) & (mid_df['semester'] == semester)]
    
    if class_mid_df.empty:
        st.warning("No mid marks data for selected year and semester.")
        return
    
    # Overall statistics
    st.markdown(f"### 📈 Year {year}, Semester {semester} - Overall Statistics")
    
    avg_mid1 = class_mid_df['mid1_marks'].mean()
    avg_mid2 = class_mid_df['mid2_marks'].mean()
    avg_overall = class_mid_df['mid_average'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Mid 1", f"{avg_mid1:.2f}", "out of 100")
    with col2:
        st.metric("Avg Mid 2", f"{avg_mid2:.2f}", "out of 100")
    with col3:
        st.metric("Avg Overall", f"{avg_overall:.2f}", "out of 100")
    with col4:
        total_records = len(class_mid_df)
        st.metric("Total Records", total_records)
    
    st.markdown("---")
    
    # Subject-wise analysis
    st.markdown("### 📚 Subject-wise Analysis")
    
    subject_stats = class_mid_df.groupby('subject').agg({
        'mid1_marks': 'mean',
        'mid2_marks': 'mean',
        'mid_average': 'mean'
    }).round(2).reset_index()
    
    subject_stats.columns = ['Subject', 'Avg Mid1', 'Avg Mid2', 'Avg Overall']
    st.dataframe(subject_stats, use_container_width=True)
    
    # Subject-wise trend chart
    fig = px.bar(
        subject_stats,
        x='Subject',
        y=['Avg Mid1', 'Avg Mid2', 'Avg Overall'],
        title=f"Subject-wise Mid Marks Comparison (Year {year}, Sem {semester})",
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Student-wise performance
    st.markdown("### 👤 Student-wise Performance")
    
    student_mid_stats = class_mid_df.groupby(['rollno', 'name']).agg({
        'mid_average': 'mean'
    }).round(2).reset_index().sort_values('mid_average', ascending=False)
    
    student_mid_stats.columns = ['Roll No', 'Name', 'Average Mid Marks']
    st.dataframe(student_mid_stats, use_container_width=True)
    
    # Top performers
    st.markdown("#### 🏆 Top 5 Performers")
    top_5 = student_mid_stats.head(5)
    st.dataframe(top_5, use_container_width=True)
    
    # Students needing improvement (< 50%)
    st.markdown("#### ⚠️ Students Needing Improvement (< 50%)")
    low_performers = student_mid_stats[student_mid_stats['Average Mid Marks'] < 50]
    if low_performers.empty:
        st.success("✅ All students performing well!")
    else:
        st.dataframe(low_performers, use_container_width=True)
    
    # Student distribution chart
    fig2 = px.histogram(
        class_mid_df,
        x='mid_average',
        nbins=10,
        title=f"Mid Marks Distribution (Year {year}, Sem {semester})",
        labels={'mid_average': 'Mid Average Marks', 'count': 'Number of Students'}
    )
    st.plotly_chart(fig2, use_container_width=True)

# ================= STUDENT - Mid Marks Analysis =================
def student_mid_marks_analysis():
    """Student interface to view their mid exam marks and analysis"""
    st.subheader("📊 My Mid Exam Analysis")
    
    init_mid_marks_db()
    mid_df = pd.read_csv(MID_MARKS_FILE)
    
    roll = str(st.session_state.username).strip().lower()
    
    # Filter student's mid marks
    my_mid_df = mid_df[mid_df['rollno'].astype(str).str.strip().str.lower() == roll].copy()
    
    if my_mid_df.empty:
        st.info("📭 No mid exam marks recorded yet. Please check back after the mid exams.")
        return
    
    # Overall statistics
    st.markdown("### 📈 Mid Exam Summary")
    
    avg_mid1 = my_mid_df['mid1_marks'].mean()
    avg_mid2 = my_mid_df['mid2_marks'].mean()
    avg_overall = my_mid_df['mid_average'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Mid 1", f"{avg_mid1:.2f}", "out of 100")
    with col2:
        st.metric("Avg Mid 2", f"{avg_mid2:.2f}", "out of 100")
    with col3:
        st.metric("Avg Overall", f"{avg_overall:.2f}", "out of 100")
    with col4:
        total_subjects = len(my_mid_df)
        st.metric("Subjects", total_subjects)
    
    st.markdown("---")
    
    # View options
    view_type = st.radio(
        "📋 View Options",
        ["All Marks", "By Semester", "Subject Comparison"],
        horizontal=True
    )
    
    if view_type == "All Marks":
        st.markdown("### 📋 All Mid Exam Marks")
        
        # Prepare display dataframe
        display_df = my_mid_df[['year', 'semester', 'subject', 'mid1_marks', 'mid2_marks', 'mid_average']].copy()
        display_df.columns = ['Year', 'Semester', 'Subject', 'Mid 1', 'Mid 2', 'Average']
        display_df = display_df.sort_values(['Year', 'Semester', 'Subject'])
        
        st.dataframe(display_df, use_container_width=True)
        
        # Chart: All subjects comparison
        fig = px.bar(
            my_mid_df.sort_values('mid_average', ascending=True),
            x='subject',
            y=['mid1_marks', 'mid2_marks', 'mid_average'],
            title="Mid Marks Comparison - All Subjects",
            barmode='group',
            labels={'value': 'Marks', 'variable': 'Exam'},
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif view_type == "By Semester":
        st.markdown("### 📅 Mid Marks by Semester")
        
        semesters = sorted(my_mid_df[['year', 'semester']].drop_duplicates().values)
        
        for year, semester in semesters:
            sem_data = my_mid_df[(my_mid_df['year'] == year) & (my_mid_df['semester'] == semester)]
            
            with st.expander(f"Year {year}, Semester {semester}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                avg_m1 = sem_data['mid1_marks'].mean()
                avg_m2 = sem_data['mid2_marks'].mean()
                avg_overall_sem = sem_data['mid_average'].mean()
                
                with col1:
                    st.metric(f"Mid 1 Avg", f"{avg_m1:.2f}")
                with col2:
                    st.metric(f"Mid 2 Avg", f"{avg_m2:.2f}")
                with col3:
                    st.metric(f"Overall Avg", f"{avg_overall_sem:.2f}")
                
                # Display marks table
                display_sem = sem_data[['subject', 'mid1_marks', 'mid2_marks', 'mid_average']].copy()
                display_sem.columns = ['Subject', 'Mid 1', 'Mid 2', 'Average']
                st.dataframe(display_sem, use_container_width=True)
    
    elif view_type == "Subject Comparison":
        st.markdown("### 🎯 Subject-wise Comparison")
        
        # Get unique subjects
        subjects = sorted(my_mid_df['subject'].unique())
        selected_subjects = st.multiselect(
            "Select subjects to compare",
            subjects,
            default=subjects[:min(5, len(subjects))]
        )
        
        if selected_subjects:
            comparison_df = my_mid_df[my_mid_df['subject'].isin(selected_subjects)].copy()
            
            # Chart
            fig = px.bar(
                comparison_df,
                x='subject',
                y='mid_average',
                color='mid_average',
                color_continuous_scale='RdYlGn',
                title="Mid Average Marks - Subject Comparison",
                labels={'mid_average': 'Average Marks'},
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            display_comp = comparison_df[['subject', 'year', 'semester', 'mid1_marks', 'mid2_marks', 'mid_average']].copy()
            display_comp.columns = ['Subject', 'Year', 'Semester', 'Mid 1', 'Mid 2', 'Average']
            st.dataframe(display_comp, use_container_width=True)
    
    st.markdown("---")
    
    # Performance feedback
    st.markdown("### 💡 Performance Feedback")
    
    if avg_overall >= 80:
        st.success("🌟 Excellent performance in mid exams! Keep up the great work!")
    elif avg_overall >= 70:
        st.info("👍 Good performance! You're on track.")
    elif avg_overall >= 60:
        st.warning("⚠️ Average performance. Focus on weaker subjects.")
    else:
        st.error("🚨 Below average performance. Please seek academic support.")
    
    # Weakest and strongest subjects
    weakest_subject = my_mid_df.loc[my_mid_df['mid_average'].idxmin()]
    strongest_subject = my_mid_df.loc[my_mid_df['mid_average'].idxmax()]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Strongest Subject",
            weakest_subject['subject'],
            f"{weakest_subject['mid_average']:.2f}"
        )
    with col2:
        st.metric(
            "Needs Improvement",
            strongest_subject['subject'],
            f"{strongest_subject['mid_average']:.2f}"
        )
