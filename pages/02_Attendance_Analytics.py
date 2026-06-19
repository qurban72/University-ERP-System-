import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import random
import warnings
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Attendance Analytics - Technify University",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════
#  SIMPLE THEME WITH STOCK FONTS
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
    /* Simple theme with stock fonts */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif !important;
    }
    
    .stApp {
        background-color: #f5f5f5;
    }
    
    [data-testid="stHeader"] {
        background: white !important;
        border-bottom: 1px solid #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #333333 !important;
    }
    
    .main .block-container {
        padding: 1.5rem 2rem 3rem !important;
        max-width: 1400px !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a2e !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #1a1a2e !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        color: #666 !important;
    }
    
    [data-testid="stMetricContainer"] {
        background: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 1rem 1.2rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
    }
    
    [data-testid="stSelectbox"] > div > div {
        background: white !important;
        border: 1px solid #d0d0d0 !important;
        border-radius: 6px !important;
        color: #333 !important;
    }
    
    [data-testid="stSelectbox"] > div > div:hover {
        border-color: #2563EB !important;
    }
    
    .stButton > button {
        background: #2563EB !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.2s !important;
    }
    
    .stButton > button:hover {
        background: #1d4ed8 !important;
        box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
        transform: translateY(-1px) !important;
    }
    
    [data-testid="stDataFrame"] {
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
    }
    
    .page-header {
        background: white;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    
    .page-header h1 {
        font-size: 1.8rem !important;
        margin: 0;
        color: #1a1a2e !important;
    }
    
    .page-header p {
        color: #666 !important;
        margin: 0.3rem 0 0 0 !important;
        font-size: 0.95rem !important;
    }
    
    .page-header-badge {
        display: inline-block;
        background: #e8f0fe;
        color: #2563EB;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        letter-spacing: 0.3px;
    }
    
    .sdiv {
        display: flex;
        align-items: center;
        gap: 14px;
        margin: 2rem 0 1.2rem;
    }
    
    .sdiv-line {
        flex: 1;
        height: 1px;
        background: #e0e0e0;
    }
    
    .sdiv-text {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #888 !important;
    }
    
    .alert {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 16px;
        border-radius: 8px;
        border: 1px solid;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    .alert.warn {
        background: #fef3c7;
        border-color: #f59e0b;
        color: #92400e !important;
    }
    
    .alert.ok {
        background: #d1fae5;
        border-color: #10b981;
        color: #065f46 !important;
    }
    
    .alert.err {
        background: #fee2e2;
        border-color: #ef4444;
        color: #991b1b !important;
    }
    
    .brand {
        padding: 1.5rem 1rem 1rem;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 0.5rem;
    }
    
    .brand-mark {
        width: 40px;
        height: 40px;
        background: #2563EB;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        margin-bottom: 0.7rem;
    }
    
    .brand h2 {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        color: #1a1a2e !important;
    }
    
    .brand p {
        font-size: 0.75rem !important;
        color: #888 !important;
        margin: 2px 0 0 0 !important;
        font-weight: 500;
    }
    
    .sidebar-nav-label {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #999 !important;
        padding: 0 0.5rem;
        margin: 1.2rem 0 0.6rem;
    }
    
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.65rem;
        font-weight: 600;
    }
    
    .bg { background: #d1fae5; color: #065f46 !important; }
    .ba { background: #fef3c7; color: #92400e !important; }
    .br { background: #fee2e2; color: #991b1b !important; }
    .bb { background: #dbeafe; color: #1e40af !important; }
    
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f0f0f0;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c0c0c0;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a0a0a0;
    }
    
    hr {
        border: none;
        border-top: 1px solid #e0e0e0;
        margin: 0.75rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  PLOTLY LAYOUT DEFAULTS
# ══════════════════════════════════════════════════════
CHART_LAYOUT = dict(
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(
        family='-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif',
        color='#333333',
        size=12
    ),
    xaxis=dict(
        gridcolor='#f0f0f0',
        zeroline=False,
        tickfont=dict(size=11, color='#666'),
        title_font=dict(size=12, color='#666'),
    ),
    yaxis=dict(
        gridcolor='#f0f0f0',
        zeroline=False,
        tickfont=dict(size=11, color='#666'),
        title_font=dict(size=12, color='#666'),
    ),
    hoverlabel=dict(
        bgcolor='white',
        bordercolor='#d0d0d0',
        font=dict(family='-apple-system, sans-serif', size=12, color='#333'),
    ),
    legend=dict(
        bgcolor='white',
        bordercolor='#e0e0e0',
        font=dict(color='#666', size=11),
    ),
    margin=dict(t=40, b=20, l=0, r=0),
    title_font=dict(
        family='-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif',
        size=14,
        color='#1a1a2e'
    ),
)

def apply_chart(fig, height=400, title=None, **kwargs):
    """Apply global chart defaults with optional title."""
    layout = {**CHART_LAYOUT, 'height': height, **kwargs}
    if title:
        layout['title'] = dict(text=title, x=0.5, xanchor='center')
    fig.update_layout(**layout)
    fig.update_traces(marker=dict(line=dict(color='white', width=1)))
    return fig

# ══════════════════════════════════════════════════════
#  ONLINE DATA FETCHING FUNCTIONS
# ══════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def fetch_online_data():
    """Fetch data from various online APIs and generate attendance data."""
    
    # ─── FETCH STUDENTS FROM API ──────────────────────
    try:
        response = requests.get('https://randomuser.me/api/?results=80&nat=us,gb,ca,au')
        user_data = response.json()
        students_list = []
        
        departments = ['Computer Science', 'Software Engineering', 'Data Science', 
                      'AI & Machine Learning', 'Cybersecurity', 'Business Administration',
                      'Marketing', 'Finance', 'Accounting', 'Economics']
        
        programs = ['BS Computer Science', 'BS Software Engineering', 'BS Data Science',
                   'MS AI & ML', 'BS Cybersecurity', 'BBA', 'BS Marketing', 'BS Finance',
                   'BS Accounting', 'BS Economics']
        
        for i, user in enumerate(user_data['results'], 1):
            student = {
                'student_id': f'STU{i:04d}',
                'name': f"{user['name']['first']} {user['name']['last']}",
                'gender': user['gender'].capitalize(),
                'email': user['email'],
                'dept_id': random.randint(1, len(departments)),
                'dept_name': random.choice(departments),
                'program_id': random.randint(1, len(programs)),
                'program_name': random.choice(programs),
                'semester': random.randint(1, 8),
                'status': random.choices(['active', 'inactive', 'graduated'], weights=[0.7, 0.2, 0.1])[0],
            }
            students_list.append(student)
        
        students_df = pd.DataFrame(students_list)
        
    except Exception as e:
        students_df = generate_sample_students()
    
    # ─── FETCH FACULTY FROM API ──────────────────────
    try:
        response = requests.get('https://randomuser.me/api/?results=15&nat=us,gb,ca,au')
        user_data = response.json()
        faculty_list = []
        
        for i, user in enumerate(user_data['results'], 1):
            faculty = {
                'faculty_id': f'FAC{i:03d}',
                'name': f"{user['name']['first']} {user['name']['last']}",
                'email': user['email'],
                'dept_id': random.randint(1, len(departments)),
                'dept_name': random.choice(departments),
                'designation': random.choice(['Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer']),
                'qualification': random.choice(['PhD', 'MS/MPhil', 'MS']),
            }
            faculty_list.append(faculty)
        
        faculty_df = pd.DataFrame(faculty_list)
        
    except:
        faculty_df = generate_sample_faculty()
    
    # ─── GENERATE COURSES ────────────────────────────
    courses_df = generate_sample_courses(faculty_df)
    
    # ─── GENERATE ATTENDANCE DATA ────────────────────
    attendance_data = generate_attendance_data(students_df, courses_df, faculty_df)
    
    return students_df, faculty_df, courses_df, departments, attendance_data

def generate_sample_students():
    """Generate sample student data as fallback."""
    departments = ['Computer Science', 'Software Engineering', 'Data Science', 
                  'AI & Machine Learning', 'Cybersecurity', 'Business Administration']
    programs = ['BS Computer Science', 'BS Software Engineering', 'BS Data Science',
               'MS AI & ML', 'BS Cybersecurity', 'BBA']
    
    students = []
    for i in range(1, 81):
        student = {
            'student_id': f'STU{i:04d}',
            'name': f'Student {i}',
            'gender': random.choice(['Male', 'Female']),
            'email': f'student{i}@university.edu',
            'dept_id': random.randint(1, len(departments)),
            'dept_name': random.choice(departments),
            'program_id': random.randint(1, len(programs)),
            'program_name': random.choice(programs),
            'semester': random.randint(1, 8),
            'status': random.choices(['active', 'inactive', 'graduated'], weights=[0.7, 0.2, 0.1])[0],
        }
        students.append(student)
    return pd.DataFrame(students)

def generate_sample_faculty():
    """Generate sample faculty data as fallback."""
    faculty = []
    for i in range(1, 16):
        fac = {
            'faculty_id': f'FAC{i:03d}',
            'name': f'Professor {i}',
            'email': f'prof{i}@university.edu',
            'dept_id': random.randint(1, 6),
            'dept_name': random.choice(['Computer Science', 'Software Engineering', 'Data Science']),
            'designation': random.choice(['Professor', 'Associate Professor', 'Assistant Professor']),
            'qualification': random.choice(['PhD', 'MS/MPhil']),
        }
        faculty.append(fac)
    return pd.DataFrame(faculty)

def generate_sample_courses(faculty_df):
    """Generate sample course data."""
    courses = []
    course_names = [
        'Introduction to Programming', 'Data Structures & Algorithms', 'Database Systems', 
        'Operating Systems', 'Computer Networks', 'Software Engineering',
        'Machine Learning', 'Deep Learning', 'Data Mining', 'Cloud Computing',
        'Web Development', 'Mobile App Development', 'Cybersecurity', 'Blockchain',
        'Financial Accounting', 'Marketing Management', 'Business Analytics',
        'Strategic Management', 'Entrepreneurship', 'International Business'
    ]
    
    faculty_ids = faculty_df['faculty_id'].tolist() if not faculty_df.empty else ['FAC001']
    
    for i, course_name in enumerate(course_names[:20], 1):
        course = {
            'course_id': f'C{i:03d}',
            'course_code': f'CS{random.randint(100, 500)}',
            'course_name': course_name,
            'dept_id': random.randint(1, 6),
            'dept_name': random.choice(['Computer Science', 'Software Engineering', 'Data Science', 
                                       'Business Administration', 'Finance', 'Marketing']),
            'faculty_id': random.choice(faculty_ids),
            'credits': random.randint(2, 4),
        }
        courses.append(course)
    
    return pd.DataFrame(courses)

def generate_attendance_data(students_df, courses_df, faculty_df):
    """Generate realistic attendance data."""
    attendance_records = []
    start_date = datetime.now() - timedelta(days=60)
    end_date = datetime.now()
    
    faculty_names = faculty_df.set_index('faculty_id')['name'].to_dict() if not faculty_df.empty else {}
    
    for _, course in courses_df.iterrows():
        selected_students = students_df.sample(frac=0.7, random_state=42)
        
        for _, student in selected_students.iterrows():
            current_date = start_date
            
            while current_date <= end_date:
                if current_date.weekday() < 5:
                    if random.random() < 0.55:
                        present = random.random() < random.uniform(0.75, 0.95)
                        
                        record = {
                            'student_id': student['student_id'],
                            'student_name': student['name'],
                            'course_id': course['course_id'],
                            'course_name': course['course_name'],
                            'course_code': course['course_code'],
                            'dept_id': course['dept_id'],
                            'dept_name': course['dept_name'],
                            'faculty_id': course['faculty_id'],
                            'faculty_name': faculty_names.get(course['faculty_id'], 'Unknown'),
                            'date': current_date,
                            'present': 1 if present else 0,
                            'day_name': current_date.strftime('%A'),
                            'month': current_date.strftime('%B'),
                            'week': current_date.isocalendar().week,
                        }
                        attendance_records.append(record)
                
                current_date += timedelta(days=1)
    
    return pd.DataFrame(attendance_records)

# ══════════════════════════════════════════════════════
#  ATTENDANCE CALCULATION FUNCTIONS
# ══════════════════════════════════════════════════════
def calculate_attendance_rate(data, group_by=None, present_col='present'):
    """Calculate attendance rate grouped by specified column."""
    if data.empty:
        return pd.DataFrame()
    
    if group_by:
        attendance_stats = data.groupby(group_by).agg({
            present_col: ['count', 'sum']
        }).reset_index()
        attendance_stats.columns = [group_by, 'total_classes', 'present_count']
        attendance_stats['attendance_rate'] = (attendance_stats['present_count'] / 
                                               attendance_stats['total_classes'] * 100).round(2)
        return attendance_stats
    else:
        total = len(data)
        present = data[present_col].sum()
        rate = (present / total * 100) if total > 0 else 0
        return {'total_classes': total, 'present_count': present, 'attendance_rate': rate}

def get_students_below_threshold(data, threshold=75):
    """Get list of students with attendance below threshold."""
    student_attendance = data.groupby(['student_id', 'student_name']).agg({
        'present': ['count', 'sum']
    }).reset_index()
    student_attendance.columns = ['student_id', 'student_name', 'total_classes', 'present_count']
    student_attendance['attendance_rate'] = (student_attendance['present_count'] / 
                                             student_attendance['total_classes'] * 100).round(2)
    below_threshold = student_attendance[student_attendance['attendance_rate'] < threshold]
    return below_threshold.sort_values('attendance_rate')

# ══════════════════════════════════════════════════════
#  PAGE HELPERS
# ══════════════════════════════════════════════════════
def page_header(icon, title, em_word, subtitle, badge="Attendance Module"):
    st.markdown(f"""
        <div class="page-header">
            <div class="page-header-badge">⬡ {badge}</div>
            <h1>{icon} {title} <em style="color:#2563EB;">{em_word}</em></h1>
            <p>{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)

def sdivider(text):
    st.markdown(f'<div class="sdiv"><div class="sdiv-line"></div><span class="sdiv-text">{text}</span><div class="sdiv-line"></div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  MAIN DASHBOARD
# ══════════════════════════════════════════════════════
def main():
    # ─── FETCH DATA ──────────────────────────────────
    with st.spinner('🔄 Fetching university data...'):
        students_df, faculty_df, courses_df, departments, attendance = fetch_online_data()
    
    if attendance.empty:
        st.error("No attendance data available. Please try refreshing.")
        return
    
    # ─── SIDEBAR ──────────────────────────────────────
    with st.sidebar:
        st.markdown("""
            <div class="brand">
                <div class="brand-mark">📊</div>
                <h2>Attendance</h2>
                <p>Analytics Dashboard</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.info("🌐 Data Source: Online APIs")
        
        st.markdown('<div class="sidebar-nav-label">Filters</div>', unsafe_allow_html=True)
        
        dept_options = ['All Departments'] + sorted(attendance['dept_name'].unique().tolist())
        selected_dept = st.selectbox("Department", dept_options, key="dept_filter")
        
        if 'date' in attendance.columns and not attendance['date'].empty:
            min_date = attendance['date'].min().date()
            max_date = attendance['date'].max().date()
            date_range = st.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key="date_filter"
            )
        else:
            date_range = None
        
        course_options = ['All Courses'] + sorted(attendance['course_name'].unique().tolist())
        selected_course = st.selectbox("Course", course_options, key="course_filter")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown('---')
        st.markdown(f"""
            <div style="text-align:center;font-size:0.7rem;color:#999;line-height:1.6;">
                <div style="font-family:monospace;font-size:0.65rem;
                            background:#f0f0f0;border:1px solid #e0e0e0;
                            color:#666;border-radius:4px;padding:3px 8px;
                            display:inline-block;margin-bottom:4px;">v2.0</div><br>
                Technify University<br>
                <span style="font-size:0.6rem;">Updated: {datetime.now().strftime("%H:%M:%S")}</span>
            </div>
        """, unsafe_allow_html=True)
    
    # ─── FILTER DATA ──────────────────────────────────
    filtered_data = attendance.copy()
    
    if selected_dept != 'All Departments':
        filtered_data = filtered_data[filtered_data['dept_name'] == selected_dept]
    
    if selected_course != 'All Courses':
        filtered_data = filtered_data[filtered_data['course_name'] == selected_course]
    
    if date_range and isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_data = filtered_data[
            (filtered_data['date'].dt.date >= start_date) & 
            (filtered_data['date'].dt.date <= end_date)
        ]
    
    # ─── MAIN CONTENT ────────────────────────────────
    page_header("📈", "Attendance", "Analytics", 
                "Comprehensive monitoring of student attendance patterns, department performance, and risk alerts",
                "Attendance Module")
    
    # ─── OVERALL ATTENDANCE STATS ────────────────────
    sdivider("Overall Attendance")
    
    total_records = len(filtered_data)
    total_present = filtered_data['present'].sum()
    overall_rate = (total_present / total_records * 100) if total_records > 0 else 0
    
    unique_students = filtered_data['student_id'].nunique()
    unique_courses = filtered_data['course_id'].nunique()
    unique_faculty = filtered_data['faculty_id'].nunique()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Records", f"{total_records:,}")
    with col2:
        st.metric("Present Count", f"{total_present:,}")
    with col3:
        st.metric("Attendance Rate", f"{overall_rate:.1f}%")
    with col4:
        st.metric("Active Students", unique_students)
    with col5:
        st.metric("Active Courses", unique_courses)
    
    # ─── ATTENDANCE OVER TIME ────────────────────────
    if 'date' in filtered_data.columns and not filtered_data.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📈 Attendance Trend")
            daily_attendance = filtered_data.groupby('date').agg({
                'present': ['count', 'sum']
            }).reset_index()
            daily_attendance.columns = ['date', 'total', 'present']
            daily_attendance['rate'] = (daily_attendance['present'] / daily_attendance['total'] * 100).round(2)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_attendance['date'],
                y=daily_attendance['rate'],
                mode='lines+markers',
                name='Attendance Rate',
                line=dict(color='#2563EB', width=2.5),
                marker=dict(size=7, color='#2563EB'),
                fill='tozeroy',
                fillcolor='rgba(37,99,235,0.1)',
                hovertemplate='%{x|%b %d, %Y}<br>Attendance: <b>%{y:.1f}%</b><extra></extra>'
            ))
            
            fig.add_hline(y=75, line_dash='dash', line_color='#ef4444',
                         annotation_text='75% Threshold', 
                         annotation_font_color='#ef4444')
            
            apply_chart(fig, 380, title="Daily Attendance Rate Trend")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📅 By Day of Week")
            if 'day_name' in filtered_data.columns:
                day_attendance = filtered_data.groupby('day_name').agg({
                    'present': ['count', 'sum']
                }).reset_index()
                day_attendance.columns = ['day', 'total', 'present']
                day_attendance['rate'] = (day_attendance['present'] / day_attendance['total'] * 100).round(2)
                
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_attendance['day'] = pd.Categorical(day_attendance['day'], categories=day_order, ordered=True)
                day_attendance = day_attendance.sort_values('day')
                
                fig = px.bar(day_attendance, x='day', y='rate',
                            color='rate', color_continuous_scale='Blues',
                            text=day_attendance['rate'].round(1))
                fig.update_traces(texttemplate='%{text}%', textposition='outside')
                fig.update_coloraxes(showscale=False)
                apply_chart(fig, 380, title="Attendance by Day of Week")
                st.plotly_chart(fig, use_container_width=True)
    
    # ─── DEPARTMENT ATTENDANCE ───────────────────────
    sdivider("Department Attendance")
    
    dept_stats = calculate_attendance_rate(filtered_data, group_by='dept_name')
    
    if not dept_stats.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            colors = ['#10b981' if rate >= 85 else '#f59e0b' if rate >= 75 else '#ef4444' 
                     for rate in dept_stats['attendance_rate']]
            
            fig = go.Figure(go.Bar(
                x=dept_stats['attendance_rate'],
                y=dept_stats['dept_name'],
                orientation='h',
                marker_color=colors,
                text=[f"{rate:.1f}%" for rate in dept_stats['attendance_rate']],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Attendance: %{x:.1f}%<br>Total Classes: %{customdata[0]}<br>Present: %{customdata[1]}<extra></extra>',
                customdata=dept_stats[['total_classes', 'present_count']].values
            ))
            
            fig.add_vline(x=75, line_dash='dash', line_color='#ef4444',
                         annotation_text='Target 75%', 
                         annotation_font_color='#ef4444')
            
            apply_chart(fig, 380, title="Attendance Rate by Department")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            dept_display = dept_stats.copy()
            dept_display['attendance_rate'] = dept_display['attendance_rate'].round(1).astype(str) + '%'
            dept_display['status'] = dept_display['attendance_rate'].str.rstrip('%').astype(float).apply(
                lambda x: '✅ Good' if x >= 85 else '⚠️ Needs Attention' if x >= 75 else '❌ Critical'
            )
            dept_display = dept_display.rename(columns={
                'dept_name': 'Department',
                'total_classes': 'Total Classes',
                'present_count': 'Present',
                'attendance_rate': 'Attendance Rate'
            })
            
            st.dataframe(dept_display[['Department', 'Total Classes', 'Present', 'Attendance Rate', 'status']], 
                        use_container_width=True, hide_index=True)
    
    # ─── COURSE ATTENDANCE ──────────────────────────
    sdivider("Course Attendance")
    
    course_stats = calculate_attendance_rate(filtered_data, group_by='course_name')
    
    if not course_stats.empty:
        top_courses = course_stats.nlargest(10, 'attendance_rate')
        bottom_courses = course_stats.nsmallest(10, 'attendance_rate')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Top 10 Courses")
            fig = px.bar(top_courses, x='attendance_rate', y='course_name',
                        orientation='h', color='attendance_rate',
                        color_continuous_scale='Greens',
                        text=top_courses['attendance_rate'].round(1))
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_coloraxes(showscale=False)
            apply_chart(fig, 380, title="Highest Attendance Courses")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⚠️ Bottom 10 Courses")
            fig = px.bar(bottom_courses, x='attendance_rate', y='course_name',
                        orientation='h', color='attendance_rate',
                        color_continuous_scale='Reds_r',
                        text=bottom_courses['attendance_rate'].round(1))
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_coloraxes(showscale=False)
            
            fig.add_vline(x=75, line_dash='dash', line_color='#ef4444',
                         annotation_text='75% Threshold', 
                         annotation_font_color='#ef4444')
            
            apply_chart(fig, 380, title="Lowest Attendance Courses")
            st.plotly_chart(fig, use_container_width=True)
    
    # ─── FACULTY ATTENDANCE ──────────────────────────
    sdivider("Faculty Attendance Performance")
    
    faculty_stats = calculate_attendance_rate(filtered_data, group_by='faculty_name')
    
    if not faculty_stats.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            faculty_stats_sorted = faculty_stats.sort_values('attendance_rate', ascending=False)
            
            colors = ['#10b981' if rate >= 85 else '#f59e0b' if rate >= 75 else '#ef4444' 
                     for rate in faculty_stats_sorted['attendance_rate']]
            
            fig = go.Figure(go.Bar(
                x=faculty_stats_sorted['attendance_rate'],
                y=faculty_stats_sorted['faculty_name'],
                orientation='h',
                marker_color=colors,
                text=[f"{rate:.1f}%" for rate in faculty_stats_sorted['attendance_rate']],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Attendance: %{x:.1f}%<br>Total Classes: %{customdata[0]}<br>Present: %{customdata[1]}<extra></extra>',
                customdata=faculty_stats_sorted[['total_classes', 'present_count']].values
            ))
            
            fig.add_vline(x=75, line_dash='dash', line_color='#ef4444',
                         annotation_text='75% Threshold', 
                         annotation_font_color='#ef4444')
            
            apply_chart(fig, 450, title="Attendance Rate by Faculty Member")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            avg_faculty_rate = faculty_stats['attendance_rate'].mean()
            faculty_above_75 = len(faculty_stats[faculty_stats['attendance_rate'] >= 75])
            faculty_below_75 = len(faculty_stats[faculty_stats['attendance_rate'] < 75])
            
            st.metric("📊 Avg Faculty Attendance", f"{avg_faculty_rate:.1f}%")
            st.metric("✅ Faculty Above 75%", faculty_above_75)
            st.metric("⚠️ Faculty Below 75%", faculty_below_75)
            
            faculty_display = faculty_stats.nlargest(5, 'attendance_rate')[['faculty_name', 'attendance_rate']]
            faculty_display.columns = ['Faculty Member', 'Attendance Rate']
            faculty_display['Attendance Rate'] = faculty_display['Attendance Rate'].round(1).astype(str) + '%'
            
            st.caption("🏅 Top 5 Faculty Members")
            st.dataframe(faculty_display, use_container_width=True, hide_index=True)
    
    # ─── STUDENTS BELOW 75% ──────────────────────────
    sdivider("Students Below 75% Attendance")
    
    threshold = 75
    below_threshold = get_students_below_threshold(filtered_data, threshold)
    
    if not below_threshold.empty:
        st.markdown(f"""
            <div class="alert warn">
                ⚠️ <strong>{len(below_threshold)} students</strong> have attendance below {threshold}% — 
                immediate intervention recommended.
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(below_threshold.head(20), 
                        x='attendance_rate', 
                        y='student_name',
                        orientation='h',
                        color='attendance_rate',
                        color_continuous_scale='Reds_r',
                        text=below_threshold['attendance_rate'].round(1))
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_coloraxes(showscale=False)
            apply_chart(fig, 450, title=f"Students Below {threshold}% Attendance")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            display_cols = ['student_id', 'student_name', 'total_classes', 'present_count', 'attendance_rate']
            if all(col in below_threshold.columns for col in display_cols):
                student_display = below_threshold[display_cols].copy()
                student_display['attendance_rate'] = student_display['attendance_rate'].round(1).astype(str) + '%'
                student_display.columns = ['Student ID', 'Student Name', 'Total Classes', 'Present', 'Attendance Rate']
                
                st.dataframe(student_display.head(20), use_container_width=True, hide_index=True)
                
                csv = below_threshold.to_csv(index=False)
                st.download_button(
                    label="📥 Download Report",
                    data=csv,
                    file_name=f"students_below_{threshold}_percent.csv",
                    mime="text/csv"
                )
    else:
        st.markdown(f"""
            <div class="alert ok">
                ✅ <strong>Excellent!</strong> All students have attendance above {threshold}% — great performance!
            </div>
        """, unsafe_allow_html=True)
    
    # ─── ATTENDANCE DISTRIBUTION ─────────────────────
    sdivider("Attendance Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Attendance Rate Distribution")
        student_categories = filtered_data.groupby(['student_id', 'student_name']).agg({
            'present': ['count', 'sum']
        }).reset_index()
        student_categories.columns = ['student_id', 'student_name', 'total', 'present']
        student_categories['rate'] = (student_categories['present'] / student_categories['total'] * 100).round(2)
        
        fig = px.histogram(student_categories, 
                          x='rate',
                          nbins=20,
                          color_discrete_sequence=['#2563EB'],
                          opacity=0.7,
                          labels={'rate': 'Attendance Rate (%)', 'count': 'Number of Students'})
        fig.add_vline(x=75, line_dash='dash', line_color='#ef4444',
                     annotation_text='75% Threshold', 
                     annotation_font_color='#ef4444')
        apply_chart(fig, 380, title="Distribution of Student Attendance Rates")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Performance Categories")
        
        student_categories['category'] = pd.cut(
            student_categories['rate'],
            bins=[0, 60, 75, 85, 100],
            labels=['Poor (0-60%)', 'Needs Improvement (60-75%)', 'Good (75-85%)', 'Excellent (85-100%)']
        )
        
        cat_counts = student_categories['category'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Count']
        
        colors = ['#ef4444', '#f59e0b', '#3b82f6', '#10b981']
        fig = px.pie(cat_counts, values='Count', names='Category',
                    color='Category', color_discrete_sequence=colors,
                    title="Student Performance Categories")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        apply_chart(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
        
    # ── Footer ─────────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div style="
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0;
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
        box-shadow: var(--shadow);
        margin-top: 2rem;
    ">
        <div style="padding: 16px 20px; background: var(--card); border-right: 1px solid var(--border);">
            <p style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
                    color:var(--muted);margin:0 0 10px;">Developer</p>
            <p style="font-size:15px;font-weight:700;color:var(--text);margin:0 0 5px;">Jawad Larik</p>
            <p style="font-size:12px;color:var(--muted);margin:0 0 3px;">🎓 BSIT · Sindh University, Hyderabad</p>
            <p style="font-size:12px;color:var(--muted);margin:0;">📍 Hyderabad, Pakistan</p>
        </div>
        <div style="padding: 16px 20px; background: var(--card);">
            <p style="font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
                    color:var(--muted);margin:0 0 10px;">Internship</p>
            <p style="font-size:15px;font-weight:700;color:var(--text);margin:0 0 5px;">Technify Institute</p>
            <p style="font-size:12px;color:var(--muted);margin:0 0 3px;">🪪 ID: Tech-DS-100-26</p>
            <p style="font-size:12px;color:var(--muted);margin:0;">📊 Data Science Internship · Module 2</p>
        </div>
    </div>

    <div style="
        margin-top: 10px;
        padding: 10px 16px;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div style="display:flex;gap:16px;align-items:center;">
            <a href="https://github.com/Jawad-Larik" target="_blank"
            style="font-size:12px;color:var(--accent);text-decoration:none;">
                🐙 github.com/Jawad-Larik
            </a>
            <span style="color:var(--border);">|</span>
            <a href="https://linkedin.com/in/jawad-larik01" target="_blank"
            style="font-size:12px;color:var(--accent);text-decoration:none;">
                💼 linkedin.com/in/Jawad-Larik
            </a>
        </div>
        <span style="font-size:11px;color:var(--muted);">© 2026 Jawad Larik · All rights reserved</span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  RUN APP
# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
