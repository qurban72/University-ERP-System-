import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import psycopg2
from streamlit_option_menu import option_menu
import warnings
warnings.filterwarnings('ignore')

# Advanced Page Configuration
st.set_page_config(
    page_title="CBT Examination Analytics | University ERP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "# CBT Examination Analytics Dashboard\nVersion 2.0\nData Science Team 1"
    }
)

# ============================================================================
# LIGHT & SOFT CSS - GENTLE COLORS, NO DARK TEXT
# ============================================================================
st.markdown("""
    <style>
    /* Main Header - Soft gradient with light colors */
    .main-header {
        background: linear-gradient(135deg, #a8e6cf 0%, #d4f1f4 50%, #ffe6f0 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .main-header h1 {
        color: #2c5f8a !important;
        margin: 0 !important;
    }
    
    .main-header p {
        color: #4a6f8a !important;
    }
    
    /* ALL Headings - Soft blue-gray */
    h1, h2, h3, h4, h5, h6 {
        color: #3a7ca5 !important;
        font-weight: 500 !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #3a7ca5 !important;
    }
    
    /* Subheaders - Soft blue */
    .stSubheader, .stHeader {
        color: #4a8bb5 !important;
    }
    
    /* Tab Headers - Soft gray-blue */
    .stTabs [data-baseweb="tab-list"] button p {
        color: #5a7d9a !important;
        font-weight: 500 !important;
    }
    
    /* Selected Tab - Soft pastel gradient */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #b8e1fc 0%, #d4f1f9 100%) !important;
        border-radius: 12px !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] p {
        color: #2c5f8a !important;
        font-weight: 600 !important;
    }
    
    /* Metric Cards - Light pastel backgrounds */
    .metric-card {
        background: linear-gradient(135deg, #ffffff, #f8fbfe);
        padding: 1.2rem;
        border-radius: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        text-align: center;
        border-top: 4px solid #a8e6cf;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    }
    
    .metric-card h3 {
        color: #7a9cbb !important;
        margin: 0 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.5px;
    }
    
    .metric-card h2 {
        color: #3a7ca5 !important;
        margin: 0.5rem 0 !important;
        font-size: 2.2rem !important;
        font-weight: 600 !important;
    }
    
    .metric-card p {
        color: #8aaec9 !important;
        margin: 0 !important;
        font-size: 0.85rem !important;
    }
    
    /* Info Box - Soft pastel */
    .info-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e8f4fd 100%);
        padding: 1rem;
        border-radius: 16px;
        margin: 1rem 0;
        border-left: 4px solid #a8e6cf;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    
    .info-box strong, .info-box p {
        color: #4a7ba8 !important;
    }
    
    /* Navigation Menu */
    .nav-link {
        color: #5a7d9a !important;
        transition: all 0.2s;
    }
    
    .nav-link:hover {
        background: #e8f4f9 !important;
        border-radius: 10px;
    }
    
    .nav-link-selected {
        background: linear-gradient(135deg, #c5e8f7 0%, #daf2fa 100%) !important;
        color: #2c5f8a !important;
        border-radius: 10px;
    }
    
    .nav-link-selected span {
        color: #2c5f8a !important;
    }
    
    /* Metrics */
    .stMetric label, .stMetric .stMetricLabel {
        color: #5a8bb5 !important;
        font-weight: 500 !important;
    }
    
    .stMetric .stMetricValue {
        color: #4a9fd5 !important;
        font-size: 1.6rem !important;
    }
    
    /* DataTable - Light headers */
    .dataframe {
        color: #4a6f8a !important;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #c5e8f7 0%, #daf2fa 100%) !important;
        color: #2c5f8a !important;
        font-weight: 600;
    }
    
    .dataframe td {
        color: #5a7d9a !important;
    }
    
    /* Buttons - Soft gradient */
    .stButton > button {
        background: linear-gradient(135deg, #b8dff0 0%, #cce8f5 100%);
        color: #3a7ca5 !important;
        border: none;
        border-radius: 12px;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #c5e5f5 0%, #d8edf8 100%);
    }
    
    /* All text elements - Soft colors */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #5a7d9a !important;
    }
    
    /* Alert boxes - Soft pastel */
    .stAlert {
        border-radius: 12px;
    }
    
    .stAlert p, .stSuccess p, .stWarning p, .stError p, .stInfo p {
        color: #4a7ba8 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        color: #5a8bb5 !important;
        font-weight: 500 !important;
        background: #f5fafd;
        border-radius: 10px;
    }
    
    /* Form labels */
    .stSelectbox label, .stMultiSelect label, .stRadio label, .stCheckbox label {
        color: #5a8bb5 !important;
        font-weight: 500 !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid #e0eff5;
        background: linear-gradient(135deg, #fafdfe, #ffffff);
        border-radius: 16px;
    }
    
    .footer p, .footer strong {
        color: #8aaec9 !important;
    }
    
    /* Input fields */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background-color: #fafcfd;
        color: #4a6f8a;
        border: 1px solid #d4e6f0;
    }
    </style>
""", unsafe_allow_html=True)

def get_live_datetime():
    return datetime.now().strftime("%A, %B %d, %Y | %I:%M:%S %p")

# ============================================================================
# DATABASE CONNECTION
# ============================================================================
@st.cache_resource
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres.gxfixjysmdmyvycuyucs",
            password="databetatechnify",
            host="aws-1-ap-southeast-1.pooler.supabase.com",
            port="5432",
            sslmode="require",
            connect_timeout=10
        )
        return conn
    except Exception as e:
        return None

@st.cache_data(ttl=300)
def load_examination_data(_conn, table_name):
    try:
        cursor = _conn.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        total_rows = cursor.fetchone()[0]
        
        st.sidebar.info(f"📊 Database has {total_rows:,} total records")
        
        query = f'SELECT * FROM "{table_name}"'
        df = pd.read_sql(query, _conn)
        return df, len(df)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, 0

# ============================================================================
# ADVANCED DATA PROCESSING
# ============================================================================
def process_examination_data(df):
    if df is None or df.empty:
        return None
    
    df_processed = df.copy()
    
    for col in df_processed.columns:
        col_lower = col.lower()
        if 'mark' in col_lower or 'score' in col_lower or 'grade' in col_lower:
            try:
                df_processed['marks'] = pd.to_numeric(df_processed[col], errors='coerce')
                break
            except:
                continue
    
    if 'marks' not in df_processed.columns:
        df_processed['marks'] = np.random.uniform(30, 100, len(df_processed))
    
    df_processed['marks'] = df_processed['marks'].fillna(df_processed['marks'].median()).clip(0, 100)
    df_processed['status'] = df_processed['marks'].apply(lambda x: 'Pass' if x >= 40 else 'Fail')
    df_processed['grade'] = df_processed['marks'].apply(lambda x: 
        'A+' if x >= 90 else 'A' if x >= 80 else 'B+' if x >= 70 else 
        'B' if x >= 60 else 'C' if x >= 50 else 'D' if x >= 40 else 'F')
    
    if 'student_id' not in df_processed.columns:
        df_processed['student_id'] = [f"S{abs(hash(str(i)))%10000:04d}" for i in range(len(df_processed))]
    if 'course_name' not in df_processed.columns:
        df_processed['course_name'] = [f"Course_{i%30 + 1}" for i in range(len(df_processed))]
    if 'department' not in df_processed.columns:
        df_processed['department'] = "General"
    if 'semester' not in df_processed.columns:
        df_processed['semester'] = np.random.randint(1, 9, len(df_processed))
    
    return df_processed

# ============================================================================
# ADVANCED ANALYTICS FUNCTIONS
# ============================================================================
def calculate_advanced_metrics(df):
    return {
        'pass_rate': (df['marks'] >= 40).mean() * 100,
        'avg_marks': df['marks'].mean(),
        'highest': df['marks'].max(),
        'lowest': df['marks'].min()
    }

def calculate_performance_score(df):
    pass_rate = (df['marks'] >= 40).mean() * 100
    avg_marks = df['marks'].mean()
    distinction_rate = (df['marks'] >= 75).mean() * 100
    return min(100, (pass_rate * 0.5) + (avg_marks * 0.3) + (distinction_rate * 0.2))

def generate_trend_forecast(df):
    semester_avg = df.groupby('semester')['marks'].mean()
    if len(semester_avg) >= 2:
        trend = semester_avg.diff().mean()
        forecast = semester_avg.iloc[-1] + trend
        return max(0, min(100, forecast)), trend
    return df['marks'].mean(), 0

# ============================================================================
# ADVANCED VISUALIZATIONS (PASTEL THEMING APPLIED HERE)
# ============================================================================
def create_gauge_chart(value, title, max_value=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 16, 'color': '#3a7ca5'}},
        gauge={
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "#8aaec9"},
            'bar': {'color': "#7acce0"},
            'bgcolor': "#ffffff",
            'borderwidth': 1,
            'bordercolor': "#d4e6f0",
            'steps': [
                {'range': [0, 40], 'color': '#ffe6f0'},
                {'range': [40, 75], 'color': '#fff8e7'},
                {'range': [75, 100], 'color': '#a8e6cf'}
            ]
        }
    ))
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', font_color='#5a7d9a')
    return fig

def create_advanced_donut_chart(df):
    pass_count = (df['marks'] >= 40).sum()
    fail_count = (df['marks'] < 40).sum()
    
    outstanding = (df['marks'] >= 85).sum()
    excellent = ((df['marks'] >= 75) & (df['marks'] < 85)).sum()
    good = ((df['marks'] >= 60) & (df['marks'] < 75)).sum()
    satisfactory = ((df['marks'] >= 40) & (df['marks'] < 60)).sum()
    critical = (df['marks'] < 40).sum()
    
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    
    fig.add_trace(go.Pie(
        labels=['Pass', 'Fail'],
        values=[pass_count, fail_count],
        marker_colors=['#a8e6cf', '#ffe6f0'],
        hole=0.45,
        name="Pass/Fail",
        textinfo='percent+label'
    ), 1, 1)
    
    fig.add_trace(go.Pie(
        labels=['Outstanding', 'Excellent', 'Good', 'Satisfactory', 'Critical'],
        values=[outstanding, excellent, good, satisfactory, critical],
        marker_colors=['#a8e6cf', '#b8dff0', '#7acce0', '#fff8e7', '#ffe6f0'],
        hole=0.45,
        name="Tiers",
        textinfo='percent'
    ), 1, 2)
    
    fig.update_layout(
        title_text="<b>Performance Distribution Metrics</b>",
        title_font=dict(size=16, color='#3a7ca5'),
        height=350,
        showlegend=True,
        legend=dict(orientation="h", y=-0.1, x=0.1),
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#5a7d9a'
    )
    return fig

def create_box_plot(df):
    fig = go.Figure()
    departments = df['department'].unique()[:5]
    colors = ['#7acce0', '#a8e6cf', '#fff8e7', '#ffe6f0', '#b8dff0']
    
    for i, dept in enumerate(departments):
        dept_data = df[df['department'] == dept]['marks']
        fig.add_trace(go.Box(
            y=dept_data,
            name=dept,
            boxmean='sd',
            marker_color=colors[i % len(colors)],
            line_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        title="<b>Departmental Spread (Box Plot)</b>",
        title_font=dict(size=16, color='#3a7ca5'),
        yaxis_title="Marks",
        height=350,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#5a7d9a'
    )
    return fig

def create_radar_chart(df):
    dept_stats = df.groupby('department').agg({
        'marks': ['mean', lambda x: (x >= 40).mean() * 100]
    }).round(2)
    dept_stats.columns = ['avg_marks', 'pass_rate']
    dept_stats = dept_stats.head(5)
    
    colors = ['#7acce0', '#a8e6cf', '#fff8e7', '#ffe6f0', '#b8dff0']
    fig = go.Figure()
    
    for i, dept in enumerate(dept_stats.index):
        fig.add_trace(go.Scatterpolar(
            r=[dept_stats.loc[dept, 'avg_marks'], dept_stats.loc[dept, 'pass_rate'], dept_stats.loc[dept, 'avg_marks'] * 1.1],
            theta=['Avg Marks', 'Pass Rate', 'Efficiency'],
            fill='toself',
            name=dept,
            line_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100]), bgcolor='rgba(0,0,0,0)'),
        title="<b>Department Matrix Breakdown</b>",
        title_font=dict(size=16, color='#3a7ca5'),
        height=380,
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#5a7d9a'
    )
    return fig

def create_trend_analysis(df):
    semester_stats = df.groupby('semester')['marks'].mean().reset_index()
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=semester_stats['semester'], y=semester_stats['marks'],
        mode='lines+markers', name='Average Marks',
        line=dict(color='#7acce0', width=3),
        marker=dict(size=8, color='#e8aa8a')
    ))
    
    fig.update_layout(
        title="<b>Academic Timeline Performance Trend</b>",
        title_font=dict(size=16, color='#3a7ca5'),
        xaxis_title="Semester", yaxis_title="Average Marks",
        height=380,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#5a7d9a'
    )
    return fig

def create_performance_prediction(df):
    forecast, trend = generate_trend_forecast(df)
    semester_avg = df.groupby('semester')['marks'].mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(semester_avg.index) + [max(semester_avg.index) + 1],
        y=list(semester_avg.values) + [forecast],
        mode='lines+markers',
        name='Trajectory Plan',
        line=dict(color='#7acce0', width=3),
        marker=dict(size=8, color=['#7acce0']*len(semester_avg) + ['#e8c38a'])
    ))
    
    fig.update_layout(
        title="<b>Next Term Forward Forecast Model</b>",
        title_font=dict(size=16, color='#3a7ca5'),
        xaxis_title="Semester", yaxis_title="Average Marks",
        height=380,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#5a7d9a'
    )
    return fig, forecast, trend

def create_alert_system(df):
    alerts = []
    pass_rate = (df['marks'] >= 40).mean() * 100
    if pass_rate < 75:
        alerts.append(("⚠️", "Notice", f"Pass rate is running at {pass_rate:.1f}% (Under Target Margin).", "medium"))
    
    course_fail_rates = df.groupby('course_name').apply(lambda x: (x['marks'] < 40).mean() * 100)
    critical_courses = course_fail_rates[course_fail_rates > 30]
    if len(critical_courses) > 0:
        alerts.append(("📚", "Attention", f"{len(critical_courses)} specific evaluation tracks show structural risks.", "high"))
    
    return alerts

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    clock_placeholder = st.empty()
    
    st.markdown("""
        <div class='main-header'>
            <h1>🎓 CBT Examination Analytics Dashboard</h1>
            <p style='font-size: 1.1rem; margin-top: 0.5rem;'>Advanced Analytics & Business Intelligence</p>
            <p style='font-size: 0.9rem; opacity: 0.8;'>Data Science Team 1 | Enterprise Edition</p>
        </div>
    """, unsafe_allow_html=True)
    
    with clock_placeholder.container():
        st.markdown(f"""
            <div style='text-align: right; margin-bottom: 1rem;'>
                <p style='color: #8aaec9; font-size: 0.9rem; margin: 0;'>🕐 {get_live_datetime()}</p>
            </div>
        """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Course Analytics", "Department Insights", "Predictive Analytics", "Reports"],
        icons=["house", "book", "building", "graph-up", "file-text"],
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#ffffff", "border-radius": "12px", "box-shadow": "0 2px 8px rgba(0,0,0,0.03)"},
            "icon": {"color": "#7acce0", "font-size": "18px"},
            "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#f0f7fa", "color": "#5a7d9a"},
            "nav-link-selected": {"background-color": "#daf2fa", "color": "#2c5f8a"},
        }
    )
    
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/analytics.png", width=80)
        st.markdown("## 🎯 Control Panel")
        use_db = st.radio("Data Source", ["📊 Sample Data", "📡 Live Database"], index=0)
        
        if use_db == "📡 Live Database":
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                    tables = [t[0] for t in cursor.fetchall()]
                    if tables:
                        selected_table = st.selectbox("Select Table", tables)
                        if st.button("🚀 Load Data", use_container_width=True):
                            df_raw, rows = load_examination_data(conn, selected_table)
                            if df_raw is not None:
                                st.session_state['exam_data'] = process_examination_data(df_raw)
                                st.rerun()
                except Exception as e:
                    st.error(f"Database error: {str(e)}")
            else:
                st.warning("⚠️ Cannot connect. Falling back to Sample Engine.")
                use_db = "📊 Sample Data"
        
        if st.button("📊 Generate Sample Data", use_container_width=True) or 'exam_data' not in st.session_state:
            np.random.seed(42)
            departments = ['Computer Science', 'Information Technology', 'Data Science', 'Artificial Intelligence', 'Business Admin']
            courses = [f"CS-{101+i}" for i in range(15)] + [f"DS-{301+i}" for i in range(10)]
            
            data = []
            for i in range(4000):
                data.append({
                    'student_id': f"S{np.random.randint(1000, 9999)}",
                    'course_name': np.random.choice(courses),
                    'department': np.random.choice(departments),
                    'semester': np.random.randint(1, 9),
                    'marks': np.random.normal(67, 13)
                })
            df_sample = pd.DataFrame(data)
            df_sample['marks'] = df_sample['marks'].clip(0, 100)
            st.session_state['exam_data'] = process_examination_data(df_sample)

        df = st.session_state['exam_data']
        st.markdown("### 🔍 Smart Filters")
        search = st.text_input("🔎 Search Track ID", placeholder="Search course/student...")
        filter_dept = st.selectbox("Department Filter", ['All'] + sorted(df['department'].unique().tolist()))
        filter_sem = st.selectbox("Semester Filter", ['All'] + sorted(df['semester'].unique().tolist()))
        
        filtered_df = df.copy()
        if filter_dept != 'All':
            filtered_df = filtered_df[filtered_df['department'] == filter_dept]
        if filter_sem != 'All':
            filtered_df = filtered_df[filtered_df['semester'] == int(filter_sem)]
        if search:
            filtered_df = filtered_df[
                filtered_df['student_id'].str.contains(search, case=False, na=False) |
                filtered_df['course_name'].str.contains(search, case=False, na=False)
            ]

    # Calculate Data States
    metrics = calculate_advanced_metrics(filtered_df)
    perf_score = calculate_performance_score(filtered_df)
    
    # ============================================================================
    # VIEW MAPPING
    # ============================================================================
    if selected == "Dashboard":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='metric-card'><h3>📊 Total Enrollments</h3><h2>{len(filtered_df):,}</h2><p>Active Datasets</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><h3>📈 Average Score</h3><h2>{metrics['avg_marks']:.1f}</h2><p>Class Matrix Median</p></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><h3>🟢 Pass Rate</h3><h2>{metrics['pass_rate']:.1f}%</h2><p>Base Threshold: 75%</p></div>", unsafe_allow_html=True)
        with col4:
            color = "#a8e6cf" if perf_score >= 75 else "#fff8e7" if perf_score >= 60 else "#ffe6f0"
            st.markdown(f"""
                <div class='metric-card' style='border-top: 4px solid {color};'>
                    <h3>🎯 Overall Performance</h3>
                    <h2 style='color: #2c5f8a !important;'>{perf_score:.1f}</h2>
                    <p>Calculated index ranking</p>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("### 🚨 Live Action Logs")
        alerts = create_alert_system(filtered_df)
        if alerts:
            for icon, title, msg, level in alerts:
                if level == "high": st.error(f"{icon} **{title}**: {msg}")
                else: st.warning(f"{icon} **{title}**: {msg}")
        else:
            st.success("✅ Operational statuses remain fully within baseline pastel bounds.")

        g1, g2 = st.columns(2)
        with g1:
            st.plotly_chart(create_advanced_donut_chart(filtered_df), use_container_width=True)
        with g2:
            st.plotly_chart(create_box_plot(filtered_df), use_container_width=True)

    elif selected == "Course Analytics":
        st.subheader("📚 Subject Performance Mapping")
        course_summary = filtered_df.groupby('course_name').agg({
            'student_id': 'count', 'marks': ['mean', 'max', 'min']
        }).reset_index()
        course_summary.columns = ['Course', 'Students', 'Average', 'Highest', 'Lowest']
        
        st.dataframe(course_summary.style.background_gradient(cmap='Pastel1', subset=['Average']), use_container_width=True)
        
        fig_bar = px.bar(course_summary.sort_values(by='Average', ascending=False).head(15), 
                         x='Course', y='Average', color='Average',
                         color_continuous_scale=['#b8dff0', '#7acce0', '#a8e6cf'], 
                         title="Top Performance Matrix per Evaluation Module")
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#5a7d9a')
        st.plotly_chart(fig_bar, use_container_width=True)

    elif selected == "Department Insights":
        st.subheader("🏢 Cross-Departmental Matrix Evaluation")
        d1, d2 = st.columns(2)
        with d1:
            st.plotly_chart(create_radar_chart(filtered_df), use_container_width=True)
        with d2:
            st.plotly_chart(create_trend_analysis(filtered_df), use_container_width=True)

    elif selected == "Predictive Analytics":
        st.subheader("🔮 Predictive Diagnostics & Trend Projections")
        p1, p2 = st.columns([2, 1])
        with p1:
            fig_pred, forecast, trend = create_performance_prediction(filtered_df)
            st.plotly_chart(fig_pred, use_container_width=True)
        with p2:
            st.plotly_chart(create_gauge_chart(forecast, "Next Sem Target Forecast"), use_container_width=True)
            if trend < 0:
                st.error(f"📉 Shift trajectory sliding by negative {abs(trend):.2f} units.")
            else:
                st.success(f"📈 Trajectory target showing positive growth value: +{trend:.2f}")

    elif selected == "Reports":
        st.subheader("📋 Structural Data Extraction Matrix")
        st.dataframe(filtered_df.head(100), use_container_width=True)
        
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Filtered Dataset as CSV",
            data=csv, file_name='CBT_Pastel_Export.csv', mime='text/csv',
            use_container_width=True
        )

    st.markdown("""
        <div class='footer'>
            <p><strong>CBT Examination Analytics Platform</strong> | Powered by Streamlit & Premium Pastel UI Engine</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
