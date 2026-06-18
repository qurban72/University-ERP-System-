import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import psycopg2
from psycopg2 import pool
import warnings
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════
#  UNIFIED ERP DESIGN SYSTEM (LIGHT MODE Corporate Style)
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Technify University ERP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* 1. Global Typography & Reset */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        background-color: #F8FAFC !important; /* Soft Institutional Off-White */
        color: #1E293B !important; /* Dark Charcoal Slate */
    }

    /* Main container handling */
    .main .block-container { 
        padding: 2.5rem 3.5rem 4rem !important; 
        max-width: 1600px !important; 
    }

    /* 2. Top Header Restyling */
    [data-testid="stHeader"] { 
        background: #FFFFFF !important; 
        border-bottom: 1px solid #E2E8F0 !important; 
    }

    /* 3. Corporate Page Header Container */
    .page-header {
        position: relative;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        background: linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 100%);
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .page-header h1 {
        font-size: 2.2rem !important;
        font-weight: 800 !important; 
        color: #1E3A8A !important; /* Deep University Blue */
        margin: 0 !important;
        line-height: 1.2 !important;
    }
    .page-header h1 em {
        font-style: normal;
        color: #2563EB !important; /* Accent Bright Blue */
    }
    .page-header p {
        font-size: 0.95rem !important; 
        color: #64748B !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0 !important;
    }

    /* Live Pill indicator */
    .live-pill {
        display: inline-flex; align-items: center; gap: 6px;
        font-size: 0.75rem; font-weight: 700; color: #10B981 !important;
        background: #E6F4EA; border: 1px solid #A7F3D0;
        padding: 4px 12px; border-radius: 100px; margin-left: 14px;
        vertical-align: middle;
    }
    .live-dot { width: 8px; height: 8px; background: #10B981; border-radius: 50%; display:inline-block; animation: blink 2s infinite; }
    @keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

    /* 4. ERP Modern Section Dividers */
    .sdiv { display:flex; align-items:center; gap:16px; margin: 2.5rem 0 1.5rem; }
    .sdiv-line { flex:1; height:1px; background: #E2E8F0; }
    .sdiv-text { font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; color: #94A3B8 !important; }

    /* 5. Clean Institutional Buttons (No heavy box shadows) */
    .stButton > button {
        background: #1E40AF !important;
        color: white !important; 
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important; 
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: #1D4ED8 !important;
        transform: translateY(-1px);
    }

    /* 6. Professional Data Tables */
    div[data-testid="stDataFrame"] { 
        border: 1px solid #E2E8F0 !important; 
        border-radius: 8px !important; 
        box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
    }

    /* 7. Sidebar Aesthetics */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    .brand { padding: 2rem 1rem 1.5rem; border-bottom:1px solid #F1F5F9; margin-bottom:1rem; text-align:center; }
    .brand-mark { width:54px; height:54px; background:#EFF6FF; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:1.8rem; margin:0 auto 0.75rem; border: 1px solid #BFDBFE; }
    .brand h2 { font-size:1.4rem!important; font-weight:800!important; color:#1E3A8A!important; margin:0; }
    .brand p { font-size:0.75rem!important; color:#64748B!important; margin-top:0.2rem; }
    .sidebar-nav-label { font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; color:#94A3B8!important; padding:0 0.75rem; margin:1.5rem 0 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  DATABASE CONFIGURATION
# ══════════════════════════════════════════════════════
DB_CONFIG = {
    "host": "aws-1-ap-southeast-1.pooler.supabase.com",
    "port": 5432,
    "database": "postgres",
    "user": "postgres.gxfixjysmdmyvycuyucs",
    "password": "databetatechnify"
}

@st.cache_resource
def init_connection_pool():
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            sslmode='require',
            connect_timeout=30
        )
        return connection_pool
    except Exception as e:
        st.error(f"❌ Failed to create connection pool: {str(e)}")
        return None

def execute_query(query):
    pool = init_connection_pool()
    if pool is None:
        return pd.DataFrame()
    
    conn = None
    try:
        conn = pool.getconn()
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"❌ Query failed: {str(e)}")
        return pd.DataFrame()
    finally:
        if conn:
            pool.putconn(conn)

@st.cache_data(ttl=300)
def load_all_data():
    with st.spinner('🔄 Fetching institutional data from campus servers...'):
        departments = execute_query("SELECT * FROM departments;")
        programs = execute_query("SELECT * FROM programs;")
        students = execute_query("SELECT * FROM students;")
        faculty = execute_query("SELECT * FROM faculty;")
        courses = execute_query("SELECT * FROM courses;")
        attendance = execute_query("SELECT * FROM attendance;")
        exams = execute_query("SELECT * FROM exams;")
        results = execute_query("SELECT * FROM results;")
        payments = execute_query("SELECT * FROM payments;")
        
        if not students.empty and not departments.empty:
            students = students.merge(
                departments[['department_id', 'department_name']], 
                left_on='department_id', 
                right_on='department_id', 
                how='left'
            )
        
        if not students.empty and not programs.empty:
            students = students.merge(
                programs[['program_id', 'program_name']], 
                left_on='program_id', 
                right_on='program_id', 
                how='left'
            )
        
        return students, faculty, departments, programs, courses, attendance, exams, results, payments

# Data Loading Execution
students, faculty, departments, programs, courses, attendance, exams, results, payments = load_all_data()

# ══════════════════════════════════════════════════════
#  PLOTLY INSTITUTIONAL THEME RULES
# ══════════════════════════════════════════════════════
# Light-mode optimized analytics palette
ERP_CHART_COLORS = ['#1E40AF', '#0EA5E9', '#10B981', '#F59E0B', '#6366F1', '#EC4899', '#8B5CF6']

CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Segoe UI, sans-serif', color='#475569', size=12),
    xaxis=dict(gridcolor='#F1F5F9', zeroline=False, tickfont=dict(size=11, color='#64748B')),
    yaxis=dict(gridcolor='#F1F5F9', zeroline=False, tickfont=dict(size=11, color='#64748B')),
    hoverlabel=dict(bgcolor='#FFFFFF', bordercolor='#CBD5E1', font=dict(color='#1E293B')),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#475569')),
    margin=dict(t=50, b=20, l=10, r=10),
)

def apply_chart(fig, height=400, title=None):
    layout = {**CHART_LAYOUT, 'height': height}
    if title:
        layout['title'] = dict(
            text=title, x=0.05, xanchor='left', 
            font=dict(family='Segoe UI', size=15, color='#1E3A8A', weight='bold')
        )
    fig.update_layout(**layout)
    return fig

# ══════════════════════════════════════════════════════
#  SIDEBAR COMPONENT
# ══════════════════════════════════════════════════════
from streamlit_option_menu import option_menu

with st.sidebar:
    st.markdown("""
        <div class="brand">
            <div class="brand-mark">🎓</div>
            <h2>SU-ERP Portal</h2>
            <p>University Analytics Desk</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-nav-label">Main Matrix</div>', unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Student Analytics Dashboard"],
        icons=["people-fill"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding":"0","background-color":"transparent"},
            "icon": {"color":"#64748B","font-size":"16px"},
            "nav-link": {"font-size":"0.9rem","text-align":"left","margin":"4px 8px","color":"#475569","border-radius":"6px","padding":"10px 12px"},
            "nav-link:hover": {"background-color":"#F1F5F9"},
            "nav-link-selected": {"background":"#EFF6FF","color":"#1E40AF","font-weight":"600","border":"1px solid #BFDBFE"},
        }
    )

    st.markdown('---')
    if not students.empty:
        st.markdown(f"""
            <div style="text-align:center;font-size:0.75rem;color:#94A3B8;">
                <div style="background:#F0FDF4;border:1px solid #BBF7D0;color:#166534;border-radius:4px;padding:4px 8px;display:inline-block;margin-bottom:6px;font-weight:600;">📡 CONNECTED TO SERVER</div><br>
                <strong>{len(students)}</strong> Records Active<br>
                <span style="font-size:0.7rem; color:#CBD5E1; margin-top:5px; display:block;">SYSTEM COMPLIANCE PASSED</span>
            </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  UI HELPERS
# ══════════════════════════════════════════════════════
def page_header(title, subtitle):
    st.markdown(f"""
        <div class="page-header">
            <h1>{title} <em>{subtitle}</em>
                <span class="live-pill">
                    <span class="live-dot"></span> SECURE
                </span>
            </h1>
            <p>Real-time campus administration reporting and data tracking systems.</p>
        </div>
    """, unsafe_allow_html=True)

def sdivider(text):
    st.markdown(f'<div class="sdiv"><div class="sdiv-line"></div><span class="sdiv-text">{text}</span><div class="sdiv-line"></div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  STUDENT ANALYTICS DASHBOARD
# ══════════════════════════════════════════════════════
def student_analytics_dashboard():
    page_header("Student Registration", "Overview")
    
    if students.empty:
        st.error("❌ No student data available. Please check database connection.")
        return
    
    # ──────────────────────────────────────────────────────────
    # SECTION 1: METRIC CARDS (Standard Streamlit metrics customized via layout)
    # ──────────────────────────────────────────────────────────
    total_students = len(students)
    active_students = total_students
    inactive_students = 0
    
    if 'status' in students.columns:
        status_counts = students['status'].value_counts().to_dict()
        status_list = list(status_counts.keys())
        
        active_students = 0
        inactive_students = 0
        for status, count in status_counts.items():
            if status.lower() == 'active':
                active_students = count
            else:
                inactive_students += count
        
        if active_students == 0 and len(status_list) > 0:
            active_students = status_counts[status_list[0]]
            inactive_students = total_students - active_students

    # We use native st.metric which is now fully white and corporate styled through our CSS injector
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Enrolled Strengths", value=f"{total_students:,}")
    with col2:
        st.metric(label="Active Academic Roll", value=f"{active_students:,}")
    with col3:
        st.metric(label="Inactive/Suspended Logs", value=f"{inactive_students:,}")
    
    sdivider("Academic Structure Distribution")
    
    # ──────────────────────────────────────────────────────────
    # SECTION 2: CHARTS (Converted to Institutional Light Palettes)
    # ──────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    
    with col1:
        if 'department_name' in students.columns:
            dept_counts = students['department_name'].value_counts()
            if not dept_counts.empty:
                fig = px.pie(values=dept_counts.values, names=dept_counts.index, 
                             hole=0.4, color_discrete_sequence=ERP_CHART_COLORS)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                apply_chart(fig, 400, "Facultywise Distribution share")
                st.plotly_chart(fig, use_container_width=True)
                
                fig2 = px.bar(x=dept_counts.index, y=dept_counts.values,
                             color=dept_counts.values, color_continuous_scale='Blues',
                             text=dept_counts.values)
                fig2.update_traces(textposition='outside')
                fig2.update_coloraxes(showscale=False)
                apply_chart(fig2, 350, "Department Registration (Headcount)")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No department data available")
    
    with col2:
        if 'program_name' in students.columns:
            prog_counts = students['program_name'].value_counts().head(10)
            if not prog_counts.empty:
                fig = px.bar(x=prog_counts.values, y=prog_counts.index, orientation='h',
                             color=prog_counts.values, color_continuous_scale='Blugrn',
                             text=prog_counts.values)
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_coloraxes(showscale=False)
                apply_chart(fig, 450, "Top 10 High Demand Degree Offerings")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No program data available")

    # ──────────────────────────────────────────────────────────
    # SECTION 3: SEMESTER BREAKDOWN
    # ──────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        if 'semester' in students.columns:
            semester_counts = students['semester'].value_counts().sort_index()
            if not semester_counts.empty:
                fig = px.bar(x=semester_counts.index, y=semester_counts.values,
                             color=semester_counts.values, color_continuous_scale='Blues',
                             text=semester_counts.values)
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_coloraxes(showscale=False)
                apply_chart(fig, 400, "Semester-wise Load Factor")
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'status' in students.columns:
            status_counts = students['status'].value_counts()
            if not status_counts.empty:
                status_colors = ['#10B981', '#F43F5E', '#8B5CF6', '#F59E0B']
                fig = px.pie(values=status_counts.values, names=status_counts.index,
                             hole=0.4, color_discrete_sequence=status_colors)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                apply_chart(fig, 400, "Compliance / Discipline Categories")
                st.plotly_chart(fig, use_container_width=True)

    # ──────────────────────────────────────────────────────────
    # SECTION 4: STUDENT RECORDS DATAFRAME
    # ──────────────────────────────────────────────────────────
    sdivider("Search & Filter Student Archives")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        dept_filter = st.selectbox("🏛️ Faculty Department", ['All'] + sorted(students['department_name'].dropna().unique().tolist())) if 'department_name' in students.columns else 'All'
    with col2:
        prog_filter = st.selectbox("📚 Active Program", ['All'] + sorted(students['program_name'].dropna().unique().tolist())) if 'program_name' in students.columns else 'All'
    with col3:
        sem_filter = st.selectbox("🎓 Current Semester", ['All'] + sorted(students['semester'].dropna().unique().tolist())) if 'semester' in students.columns else 'All'
    with col4:
        status_filter = st.selectbox("✅ Status State", ['All'] + sorted(students['status'].dropna().unique().tolist())) if 'status' in students.columns else 'All'
    
    filtered_df = students.copy()
    if dept_filter != 'All': filtered_df = filtered_df[filtered_df['department_name'] == dept_filter]
    if prog_filter != 'All': filtered_df = filtered_df[filtered_df['program_name'] == prog_filter]
    if sem_filter != 'All': filtered_df = filtered_df[filtered_df['semester'] == sem_filter]
    if status_filter != 'All': filtered_df = filtered_df[filtered_df['status'] == status_filter]
    
    st.caption(f"📑 Query returned {len(filtered_df):,} records out of matrix.")
    
    display_cols = ['student_id', 'name', 'email', 'department_name', 'program_name', 'semester', 'status', 'gender', 'cgpa']
    available_cols = [c for c in display_cols if c in filtered_df.columns]
    
    st.dataframe(filtered_df[available_cols].reset_index(drop=True), use_container_width=True, height=380)
    
    # ──────────────────────────────────────────────────────────
    # SECTION 5: EXPORT COMPLIANCE
    # ──────────────────────────────────────────────────────────
    sdivider("Administrative Actions")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Sheet (CSV)",
        data=csv,
        file_name=f"ERP_Student_Extract_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Router Execution
student_analytics_dashboard()
