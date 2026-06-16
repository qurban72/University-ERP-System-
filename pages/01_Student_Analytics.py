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

st.set_page_config(
    page_title="Technify University ERP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_CONFIG = {
    "host": "aws-1-ap-southeast-1.pooler.supabase.com",
    "port": 5432,
    "database": "postgres",
    "user": "postgres.gxfixjysmdmyvycuyucs",
    "password": "databetatechnify"
}

@st.cache_resource
def init_connection_pool():
    """Initialize connection pool"""
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
    """Execute query and return DataFrame using connection pool"""
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
    """Load all data from Supabase PostgreSQL with proper joins"""
    
    with st.spinner('🔄 Loading data from Supabase database...'):
        
        # Load all tables
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
            # Merge students with departments using department_id
            students = students.merge(
                departments[['department_id', 'department_name']], 
                left_on='department_id', 
                right_on='department_id', 
                how='left'
            )
        
        if not students.empty and not programs.empty:
            # Merge students with programs using program_id
            students = students.merge(
                programs[['program_id', 'program_name']], 
                left_on='program_id', 
                right_on='program_id', 
                how='left'
            )
        
        return students, faculty, departments, programs, courses, attendance, exams, results, payments


# Load the data
students, faculty, departments, programs, courses, attendance, exams, results, payments = load_all_data()

# Debug: Check status column values
if not students.empty and 'status' in students.columns:
    unique_status = students['status'].unique()
    # st.sidebar.success(f"📊 Status values in DB: {list(unique_status)}")

# ══════════════════════════════════════════════════════
#  DESIGN SYSTEM & THEME
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-deep:        #060A12;
        --bg-mid:         #0C1220;
        --bg-card:        rgba(255,255,255,0.035);
        --bg-card-hover:  rgba(255,255,255,0.065);
        --border:         rgba(255,255,255,0.07);
        --border-hi:      rgba(255,255,255,0.13);
        --blue:    #2563EB;
        --cyan:    #06B6D4;
        --violet:  #7C3AED;
        --green:   #10B981;
        --amber:   #F59E0B;
        --rose:    #F43F5E;
        --text-1: rgba(255,255,255,0.95);
        --text-2: rgba(255,255,255,0.55);
        --text-3: rgba(255,255,255,0.28);
        --r-sm: 8px;  --r-md: 14px;  --r-lg: 20px;  --r-xl: 28px;
        --ease: all 0.22s cubic-bezier(0.4,0,0.2,1);
        --font-d: 'Syne', sans-serif;
        --font-b: 'Space Grotesk', sans-serif;
        --font-m: 'JetBrains Mono', monospace;
    }

    *, *::before, *::after { box-sizing: border-box; }
    html, body, [data-testid="stAppViewContainer"] {
        font-family: var(--font-b) !important;
        color: var(--text-1) !important;
    }

    .stApp {
        background:
            radial-gradient(ellipse 80% 50% at 15% -5%,  rgba(37,99,235,0.16) 0%, transparent 55%),
            radial-gradient(ellipse 55% 45% at 85% 105%, rgba(124,58,237,0.13) 0%, transparent 55%),
            radial-gradient(ellipse 90% 70% at 50% 55%,  rgba(6,182,212,0.04)  0%, transparent 65%),
            var(--bg-deep) !important;
        background-attachment: fixed !important;
    }

    .stApp::before {
        content: '';
        position: fixed; inset: 0;
        background-image: radial-gradient(rgba(37,99,235,0.25) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
        opacity: 0.45;
    }

    [data-testid="stAppViewContainer"] > .main { background: transparent !important; position: relative; z-index: 1; }
    [data-testid="stHeader"] { background: rgba(6,10,18,0.88) !important; backdrop-filter: blur(24px) !important; border-bottom: 1px solid var(--border) !important; }
    .main .block-container { padding: 1.75rem 2.25rem 4rem !important; max-width: 1700px !important; }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(160deg, rgba(37,99,235,0.07) 0%, transparent 45%),
            rgba(6,10,18,0.97) !important;
        backdrop-filter: blur(30px) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text-1) !important; }

    [data-testid="stMetricValue"] {
        font-family: var(--font-d) !important;
        font-size: 2rem !important; font-weight: 800 !important;
        color: white !important; letter-spacing: -1px !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.72rem !important; font-weight: 600 !important;
        color: var(--text-2) !important; text-transform: uppercase !important;
        letter-spacing: 0.9px !important;
    }
    [data-testid="stMetricContainer"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--r-md) !important;
        padding: 1.2rem 1.4rem !important;
        transition: var(--ease) !important;
    }
    [data-testid="stMetricContainer"]:hover {
        border-color: var(--border-hi) !important;
        transform: translateY(-2px) !important;
        background: var(--bg-card-hover) !important;
    }

    [data-testid="stSelectbox"] > div > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--r-sm) !important; color: white !important;
        transition: var(--ease) !important;
    }
    [data-testid="stSelectbox"] > div > div:hover { border-color: var(--blue) !important; }

    .stButton > button {
        background: linear-gradient(135deg, var(--blue), #1D4ED8) !important;
        color: white !important; border: 1px solid rgba(37,99,235,0.35) !important;
        border-radius: var(--r-sm) !important;
        font-family: var(--font-b) !important; font-weight: 600 !important;
        font-size: 0.875rem !important; padding: 0.55rem 1.4rem !important;
        transition: var(--ease) !important; letter-spacing: 0.2px;
    }
    .stButton > button:hover {
        box-shadow: 0 0 22px rgba(37,99,235,0.4) !important;
        transform: translateY(-1px) !important;
    }

    h1,h2,h3 { font-family: var(--font-d) !important; color: white !important; letter-spacing: -0.5px !important; }
    h2 { font-size: 1.35rem !important; font-weight: 700 !important; margin-top: 1rem !important; margin-bottom: 1rem !important; }
    h3 { font-size: 1.05rem !important; font-weight: 700 !important; }

    [data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: var(--r-md) !important; overflow: hidden !important; }

    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg-deep); }
    ::-webkit-scrollbar-thumb { background: rgba(37,99,235,0.4); border-radius: 3px; }

    .page-header {
        position: relative; overflow: hidden;
        padding: 2.2rem 2.5rem 1.9rem;
        margin-bottom: 1.75rem;
        border-radius: var(--r-xl);
        border: 1px solid var(--border-hi);
        background: linear-gradient(120deg, rgba(37,99,235,0.14) 0%, rgba(6,182,212,0.06) 50%, transparent 80%);
    }
    .page-header h1 {
        font-family: var(--font-d) !important; font-size: 2.3rem !important;
        font-weight: 800 !important; color: white !important;
        line-height: 1.1 !important; letter-spacing: -1.2px !important;
    }
    .page-header h1 em {
        font-style: normal;
        background: linear-gradient(120deg, var(--cyan) 0%, #818CF8 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .page-header p {
        font-size: 0.92rem !important; color: var(--text-2) !important;
        margin-top: 0.4rem !important;
    }
    .live-pill {
        display: inline-flex; align-items: center; gap: 6px;
        font-size: 0.7rem; font-weight: 700; color: #34D399 !important;
        background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.22);
        padding: 3px 10px; border-radius: 100px; margin-left: 12px;
        vertical-align: middle;
    }
    .live-dot { width: 6px; height: 6px; background: #34D399; border-radius: 50%; display:inline-block; animation: blink 2s infinite; }
    @keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

    .kpi {
        position: relative; overflow: hidden;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--r-lg);
        padding: 1.35rem 1.5rem 1.2rem;
        transition: var(--ease);
        text-align: center;
    }
    .kpi:hover { background: var(--bg-card-hover); border-color: var(--border-hi); transform: translateY(-3px); }
    .kpi.b::before { background: linear-gradient(90deg,var(--blue),var(--cyan)); }
    .kpi.g::before { background: linear-gradient(90deg,var(--green),#34D399); }
    .kpi.v::before { background: linear-gradient(90deg,var(--violet),#A855F7); }
    .kpi.a::before { background: linear-gradient(90deg,var(--amber),#FCD34D); }
    .kpi.r::before { background: linear-gradient(90deg,var(--rose),#FB7185); }
    .kpi::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; }
    .kpi-val { font-family:var(--font-d)!important; font-size:2.5rem!important; font-weight:800!important; line-height:1!important; letter-spacing:-1.5px!important; margin-bottom:0.5rem; }
    .kpi.b .kpi-val { color:#67E8F9!important; }
    .kpi.g .kpi-val { color:#6EE7B7!important; }
    .kpi.v .kpi-val { color:#C4B5FD!important; }
    .kpi.a .kpi-val { color:#FDE68A!important; }
    .kpi.r .kpi-val { color:#FCA5A5!important; }
    .kpi-lbl { font-size:0.75rem!important; font-weight:600!important; color:var(--text-2)!important; text-transform:uppercase!important; letter-spacing:1px!important; }

    .sdiv { display:flex; align-items:center; gap:14px; margin:2rem 0 1.5rem; }
    .sdiv-line { flex:1; height:1px; background:linear-gradient(90deg,rgba(37,99,235,0.35),transparent); }
    .sdiv-text { font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:2px; color:var(--text-3)!important; }

    .brand { padding:1.6rem 1.4rem 1.2rem; border-bottom:1px solid var(--border); margin-bottom:0.5rem; text-align:center; }
    .brand-mark { width:50px; height:50px; background:linear-gradient(135deg,var(--blue),var(--cyan)); border-radius:var(--r-md); display:flex; align-items:center; justify-content:center; font-size:1.8rem; margin:0 auto 0.9rem; }
    .brand h2 { font-family:var(--font-d)!important; font-size:1.3rem!important; font-weight:800!important; color:white!important; margin:0; }
    .brand p { font-size:0.7rem!important; color:var(--text-2)!important; margin-top:0.2rem; }
    .sidebar-nav-label { font-size:0.65rem; font-weight:700; text-transform:uppercase; letter-spacing:1.6px; color:var(--text-3)!important; padding:0 0.5rem; margin:1.4rem 0 0.6rem; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  PLOTLY LAYOUT DEFAULTS
# ══════════════════════════════════════════════════════
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Space Grotesk, sans-serif', color='rgba(255,255,255,0.7)', size=12),
    xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zeroline=False, tickfont=dict(size=11, color='rgba(255,255,255,0.5)')),
    yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zeroline=False, tickfont=dict(size=11, color='rgba(255,255,255,0.5)')),
    hoverlabel=dict(bgcolor='rgba(13,20,37,0.95)', bordercolor='rgba(37,99,235,0.4)', font=dict(color='white')),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='rgba(255,255,255,0.6)')),
    margin=dict(t=40, b=20, l=0, r=0),
)

MIXED_SEQ = ['#2563EB','#7C3AED','#10B981','#F59E0B','#F43F5E','#06B6D4','#8B5CF6']

def apply_chart(fig, height=400, title=None):
    layout = {**CHART_LAYOUT, 'height': height}
    if title:
        layout['title'] = dict(text=title, x=0.5, xanchor='center', font=dict(family='Syne', size=16, color='white'))
    fig.update_layout(**layout)
    return fig

# ══════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════
from streamlit_option_menu import option_menu

with st.sidebar:
    st.markdown("""
        <div class="brand">
            <div class="brand-mark">🎓</div>
            <h2>Technify</h2>
            <p>University ERP Analytics</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-nav-label">Navigation</div>', unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Student Analytics Dashboard"],
        icons=["people-fill"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding":"0","background-color":"transparent"},
            "icon": {"color":"rgba(255,255,255,0.6)","font-size":"18px"},
            "nav-link": {"font-size":"0.9rem","text-align":"left","margin":"2px 0","color":"rgba(255,255,255,0.7)","border-radius":"8px","padding":"10px 15px"},
            "nav-link:hover": {"background-color":"rgba(255,255,255,0.07)"},
            "nav-link-selected": {"background":"linear-gradient(135deg,rgba(37,99,235,0.3),rgba(6,182,212,0.15))","color":"white","font-weight":"600","border":"1px solid rgba(37,99,235,0.35)"},
        }
    )

    st.markdown('---')
    if not students.empty:
        st.markdown(f"""
            <div style="text-align:center;font-size:0.7rem;color:rgba(255,255,255,0.3);">
                <div style="background:rgba(37,99,235,0.12);border:1px solid rgba(37,99,235,0.2);border-radius:4px;padding:4px 8px;display:inline-block;margin-bottom:6px;">🚀 SUPABASE LIVE</div><br>
                {len(students)} Students Loaded<br>
                DEVELOPED BY AHMER ALI
            </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════
def page_header(title, subtitle):
    st.markdown(f"""
        <div class="page-header">
            <h1>📊 {title} <em>{subtitle}</em>
                <span class="live-pill">
                    <span class="live-dot"></span> LIVE
                </span>
            </h1>
            <p>Real-time student analytics and demographic insights</p>
        </div>
    """, unsafe_allow_html=True)

def kpi_card(icon, value, label, color="b"):
    return f"""
        <div class="kpi {color}">
            <div class="kpi-val">{value}</div>
            <div class="kpi-lbl">{icon} {label}</div>
        </div>
    """

def sdivider(text):
    st.markdown(f'<div class="sdiv"><div class="sdiv-line"></div><span class="sdiv-text">{text}</span><div class="sdiv-line"></div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  STUDENT ANALYTICS DASHBOARD
# ══════════════════════════════════════════════════════
def student_analytics_dashboard():
    page_header("Student Analytics", "Dashboard")
    
    if students.empty:
        st.error("❌ No student data available. Please check database connection.")
        return
    
    # ──────────────────────────────────────────────────────────
    # SECTION 1: KEY METRICS (FIXED)
    # ──────────────────────────────────────────────────────────
    total_students = len(students)
    
    # Check for status column and get actual counts
    if 'status' in students.columns:
        # Count each status type
        status_counts = students['status'].value_counts().to_dict()
        status_list = list(status_counts.keys())
        
        # Show debug in sidebar
        # st.sidebar.info(f"📊 Status Distribution: {status_counts}")
        
        # Active students - look for 'active' or 'Active'
        active_students = 0
        inactive_students = 0
        
        for status, count in status_counts.items():
            if status.lower() == 'active':
                active_students = count
            else:
                inactive_students += count
        
        # If no 'active' status found, assume first status is active
        if active_students == 0 and len(status_list) > 0:
            active_students = status_counts[status_list[0]]
            inactive_students = total_students - active_students
    else:
        active_students = total_students
        inactive_students = 0
        st.sidebar.warning("⚠️ No 'status' column found in database")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(kpi_card("👨‍🎓", f"{total_students:,}", "TOTAL STUDENTS", "b"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("✅", f"{active_students:,}", "ACTIVE STUDENTS", "g"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("❌", f"{inactive_students:,}", "INACTIVE STUDENTS", "r"), unsafe_allow_html=True)
    
    sdivider("Distribution Analysis")
    
    # ──────────────────────────────────────────────────────────
    # SECTION 2: DEPARTMENT CHART
    # ──────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Students by Department")
        
        # Check for department column
        if 'department_name' in students.columns:
            dept_counts = students['department_name'].value_counts()
            if not dept_counts.empty:
                fig = px.pie(values=dept_counts.values, names=dept_counts.index, 
                            hole=0.4, color_discrete_sequence=MIXED_SEQ)
                fig.update_traces(textposition='inside', textinfo='percent+label',
                                 marker=dict(line=dict(color='rgba(0,0,0,0.4)', width=2)))
                apply_chart(fig, 450, "Department-wise Student Distribution")
                st.plotly_chart(fig, use_container_width=True)
                
                # Bar chart view
                fig2 = px.bar(x=dept_counts.index, y=dept_counts.values,
                             color=dept_counts.values, color_continuous_scale='Blues',
                             text=dept_counts.values)
                fig2.update_traces(textposition='outside')
                fig2.update_coloraxes(showscale=False)
                apply_chart(fig2, 400, "Department Enrollment (Bar View)")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No department data available")
        else:
            st.info("Department column not found. Available columns: " + ", ".join(students.columns))
    
    with col2:
        st.subheader("📚 Students by Program")
        
        # Check for program column
        if 'program_name' in students.columns:
            prog_counts = students['program_name'].value_counts().head(10)
            if not prog_counts.empty:
                fig = px.bar(x=prog_counts.values, y=prog_counts.index, orientation='h',
                            color=prog_counts.values, color_continuous_scale='Teal',
                            text=prog_counts.values)
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_coloraxes(showscale=False)
                apply_chart(fig, 450, "Top 10 Programs by Enrollment")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No program data available")
        else:
            st.info("Program column not found. Available columns: " + ", ".join(students.columns))
    
    # ──────────────────────────────────────────────────────────
    # SECTION 3: SEMESTER AND STATUS CHARTS
    # ──────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎓 Students by Semester")
        
        # Check for semester column
        if 'semester' in students.columns:
            semester_counts = students['semester'].value_counts().sort_index()
            if not semester_counts.empty:
                fig = px.bar(x=semester_counts.index, y=semester_counts.values,
                            color=semester_counts.values, color_continuous_scale='Viridis',
                            text=semester_counts.values)
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_coloraxes(showscale=False)
                apply_chart(fig, 450, "Semester-wise Student Distribution")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No semester data available")
        else:
            st.info("Semester column not found")
    
    with col2:
        st.subheader("📈 Student Status Breakdown")
        
        if 'status' in students.columns:
            status_counts = students['status'].value_counts()
            if not status_counts.empty:
                # Dynamic colors based on status types
                color_map = {
                    'active': '#10B981', 'Active': '#10B981',
                    'inactive': '#F43F5E', 'Inactive': '#F43F5E',
                    'graduated': '#8B5CF6', 'Graduated': '#8B5CF6',
                    'probation': '#F59E0B', 'Probation': '#F59E0B'
                }
                colors = [color_map.get(s, '#3B82F6') for s in status_counts.index]
                
                fig = px.pie(values=status_counts.values, names=status_counts.index,
                            hole=0.4, color_discrete_sequence=colors)
                fig.update_traces(textposition='inside', textinfo='percent+label',
                                 marker=dict(line=dict(color='rgba(0,0,0,0.4)', width=2)))
                apply_chart(fig, 450, "Student Status Distribution")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No status data available")
        else:
            # Create a default pie chart
            fig = px.pie(values=[total_students], names=['All Students'], 
                        hole=0.4, color_discrete_sequence=['#3B82F6'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            apply_chart(fig, 450, "Student Population")
            st.plotly_chart(fig, use_container_width=True)
    
    # ──────────────────────────────────────────────────────────
    # SECTION 4: DATA TABLE WITH FILTERS
    # ──────────────────────────────────────────────────────────
    sdivider("Student Records")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'department_name' in students.columns:
            dept_options = ['All'] + sorted(students['department_name'].dropna().unique().tolist())
            dept_filter = st.selectbox("🏛️ Department", dept_options)
        else:
            dept_filter = 'All'
    
    with col2:
        if 'program_name' in students.columns:
            prog_options = ['All'] + sorted(students['program_name'].dropna().unique().tolist())
            prog_filter = st.selectbox("📚 Program", prog_options)
        else:
            prog_filter = 'All'
    
    with col3:
        if 'semester' in students.columns:
            sem_options = ['All'] + sorted(students['semester'].dropna().unique().tolist())
            sem_filter = st.selectbox("🎓 Semester", sem_options)
        else:
            sem_filter = 'All'
    
    with col4:
        if 'status' in students.columns:
            status_options = ['All'] + sorted(students['status'].dropna().unique().tolist())
            status_filter = st.selectbox("✅ Status", status_options)
        else:
            status_filter = 'All'
    
    # Apply filters
    filtered_df = students.copy()
    if dept_filter != 'All' and 'department_name' in students.columns:
        filtered_df = filtered_df[filtered_df['department_name'] == dept_filter]
    if prog_filter != 'All' and 'program_name' in students.columns:
        filtered_df = filtered_df[filtered_df['program_name'] == prog_filter]
    if sem_filter != 'All' and 'semester' in students.columns:
        filtered_df = filtered_df[filtered_df['semester'] == sem_filter]
    if status_filter != 'All' and 'status' in students.columns:
        filtered_df = filtered_df[filtered_df['status'] == status_filter]
    
    st.caption(f"📊 Showing {len(filtered_df):,} of {len(students):,} students")
    
    # Select columns to display
    display_cols = ['student_id', 'name', 'email']
    if 'department_name' in students.columns:
        display_cols.append('department_name')
    if 'program_name' in students.columns:
        display_cols.append('program_name')
    if 'semester' in students.columns:
        display_cols.append('semester')
    if 'status' in students.columns:
        display_cols.append('status')
    if 'gender' in students.columns:
        display_cols.append('gender')
    if 'cgpa' in students.columns:
        display_cols.append('cgpa')
    
    available_cols = [c for c in display_cols if c in filtered_df.columns]
    if available_cols:
        st.dataframe(filtered_df[available_cols].reset_index(drop=True), use_container_width=True, height=400)
    else:
        st.dataframe(filtered_df, use_container_width=True, height=400)
    
    # ──────────────────────────────────────────────────────────
    # SECTION 5: EXPORT
    # ──────────────────────────────────────────────────────────
    sdivider("Export Data")
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"students_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )


# ══════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════
student_analytics_dashboard()
