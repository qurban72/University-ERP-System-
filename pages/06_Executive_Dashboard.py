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
    page_title="Executive Dashboard | University ERP",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "# Executive Level Analytics Dashboard\nVersion 3.0\nStrategic Intelligence Team"
    }
)

# ============================================================================
# UNIFIED LIGHT BACKGROUND CSS - WHITE THEME WITH BLACK SIDEBAR TEXT
# ============================================================================
st.markdown("""
    <style>
    /* Main app background - clean white */
    .stApp {
        background: #ffffff !important;
    }
    
    /* Sidebar background - keep as is */
    [data-testid="stSidebar"] {
        background: #f8fafc !important;
        border-right: 1px solid #e8edf3 !important;
    }
    
    /* SIDEBAR TEXT COLOR - BLACK FOR VISIBILITY */
    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
    /* Sidebar headings - black */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5, 
    [data-testid="stSidebar"] h6 {
        color: #000000 !important;
    }
    
    /* Sidebar labels - black */
    [data-testid="stSidebar"] label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar paragraphs - black */
    [data-testid="stSidebar"] p {
        color: #000000 !important;
    }
    
    /* Sidebar select box text - black */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        color: #000000 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox select {
        color: #000000 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox option {
        color: #000000 !important;
    }
    
    /* Sidebar radio buttons text - black */
    [data-testid="stSidebar"] .stRadio > div {
        background-color: #ffffff !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #000000 !important;
    }
    
    /* Sidebar button text - white (keep as is) */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
    }
    
    /* Role badge in sidebar - keep green */
    .role-badge {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 0.4rem 1.2rem;
        border-radius: 50px;
        color: #2e7d32 !important;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    /* Main content area - transparent */
    .main > div {
        background: transparent !important;
    }
    
    /* Block container */
    .block-container {
        background: transparent !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* All st elements transparent */
    .stMarkdown, .stPlotlyChart, .stDataFrame, 
    .stSelectbox, .stRadio, .stButton, .stExpander {
        background: transparent !important;
    }
    
    /* Headings styling */
    h1, h2, h3, h4, h5, h6 {
        color: #2c5270 !important;
        font-weight: 500 !important;
    }
    
    /* Main content text */
    p, li, span, div {
        color: #1a1a2e !important;
    }
    
    /* Metric Cards - White background with soft shadow */
    .metric-card {
        background: #ffffff !important;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        text-align: center;
        border-top: 4px solid #90caf9;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }
    
    .metric-card h3 {
        color: #64b5f6 !important;
        margin: 0;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    .metric-card h2 {
        color: #1e3a5f !important;
        margin: 0.6rem 0;
        font-size: 2.2rem;
    }
    
    .metric-card p {
        color: #78909c !important;
        font-size: 0.85rem;
        margin: 0;
    }
    
    /* Navigation Menu System Override */
    .nav-link-selected {
        background: linear-gradient(135deg, #bbdefb 0%, #e1f5fe 100%) !important;
        color: #0d47a1 !important;
    }

    /* Banner Badge */
    .banner-badge {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        padding: 0.3rem 1rem;
        border-radius: 50px;
        color: #0d47a1;
        font-weight: 500;
        display: inline-block;
        margin: 0 0.3rem;
        font-size: 0.9rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 2rem;
        border-top: 1px solid #e8edf3;
        color: #78909c;
    }
    
    /* Fix any dark elements */
    .st-emotion-cache-1r6slb0 {
        background-color: #ffffff !important;
    }
    
    .st-emotion-cache-1wmy9hl {
        background-color: #ffffff !important;
    }
    
    .st-emotion-cache-1v0mbdj {
        background-color: #ffffff !important;
    }
    
    .st-emotion-cache-1r4qj8v {
        background-color: #ffffff !important;
    }
    
    /* Sidebar image container */
    .stImage {
        background: transparent !important;
    }
    
    /* Streamlit option menu customization */
    .st-emotion-cache-16idsys {
        background: #ffffff !important;
    }
    
    /* Sidebar divider lines */
    hr {
        border-color: #d1d5db !important;
    }
            
        /* Sidebar divider lines */
    hr {
        border-color: #d1d5db !important;
    }
    
    /* DEPLOYMENT BAR FIX - ADD THIS */
    header[data-testid="stHeader"] {
        background: #f8fafc !important;
        border-bottom: 1px solid #e8edf3 !important;
    }
    
    header[data-testid="stHeader"] * {
        color: #1a1a2e !important;
    }

        /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 2rem;
        border-top: 1px solid #e8edf3;
        color: #78909c;
    }
    
    .footer p {
        margin: 0.3rem 0;
    }        

    </style>
""", unsafe_allow_html=True)

def get_live_datetime():
    return datetime.now().strftime("%A, %B %d, %Y | %I:%M:%S %p")

# ============================================================================
# SUPABASE/POSTGRESQL DATABASE CONNECTION
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
    except Exception:
        return None

@st.cache_data(ttl=300)
def load_executive_data(_conn, table_name):
    try:
        query = f'SELECT * FROM "{table_name}"'
        df = pd.read_sql(query, _conn)
        return df
    except Exception:
        return None

# ============================================================================
# SIMULATED STRATEGIC ENGINE GENERATOR
# ============================================================================
def generate_executive_mock_data():
    np.random.seed(101)
    departments = ['Engineering', 'Business School', 'Medical Sciences', 'Computing', 'Social Sciences']
    data = []
    
    # Simulating 5000 analytical records
    for i in range(5000):
        allocated_fee = np.random.uniform(50000, 150000)
        collection_rate = np.random.choice([1.0, 1.0, 0.9, 0.85, 0.5, 0.0], p=[0.5, 0.2, 0.15, 0.08, 0.05, 0.02])
        fee_collected = allocated_fee * collection_rate
        
        data.append({
            'student_id': f"REG-{np.random.randint(100000, 999999)}",
            'department': np.random.choice(departments),
            'attendance': np.random.beta(a=7, b=2) * 100,
            'gpa': np.clip(np.random.normal(3.1, 0.5), 0.0, 4.0),
            'fee_allocated': allocated_fee,
            'fee_collected': fee_collected,
            'semester': f"Semester {np.random.randint(1, 9)}"
        })
    return pd.DataFrame(data)

# ============================================================================
# SYSTEM CORE LOGIC & DASHBOARD INTERFACE
# ============================================================================
def main():
    # Real-time Strategic Clock Interface
    st.markdown(f"""
        <div style='text-align: right; padding: 1rem 0 0.5rem 0;'>
            <p style='color: #78909c; font-size: 0.85rem;'>👑 System Status: Secure | Operational 🕐 {get_live_datetime()}</p>
        </div>
    """, unsafe_allow_html=True)
    # NEW HEADER WITH EXAMINATION ANALYTICS STYLE
    st.markdown(
        f"""
        <div style='background: white; padding: 2rem 2.5rem; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 2px 12px rgba(0,0,0,0.06); border-left: 6px solid #4f46e5;'>
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 0.5rem;'>
                <span style='
                    font-size: 1.1rem;
                    font-weight: 700;
                    color: #4f46e5;
                '>
                    🏛️ Executive Command Dashboard
                </span>
                <span style='
                    font-size: 0.9rem;
                    font-weight: 500;
                    color: #4f46e5;
                '>
                    Data Science Team 1
                </span>
            </div>
            <h1 style="
                margin:0;
                font-size:3rem;
                font-weight:800;
                line-height:1.05;
                letter-spacing:-1px;
            ">
                <span style="color:#0f172a; font-weight:800;">🏛️ Executive</span>
                <span style="
                    background: linear-gradient(90deg, #6366f1, #0ea5e9);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    font-weight:800;
                ">Command</span><br>
                <span style="color:#0f172a; font-weight:800;">Dashboard</span>
            </h1>
            <p style='color: #6a7a8a; margin: 0 0 0.5rem 0; font-size: 1rem; font-weight: 400;'>
                Strategic Institutional KPIs & Resource Planning Analytics
            </p>
            <div style='display: flex; align-items: center; gap: 12px; flex-wrap: nowrap; margin-top: 0.5rem; white-space: nowrap;'>
                <span style='
                    background: #eef3f7;
                    padding: 4px 14px;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    color: #4f46e5;
                    font-weight: 500;
                '>
                    📊 Live System
                </span>
                <span style="
                    display:flex;
                    align-items:center;
                    height:32px;
                    gap:6px;
                    padding:0 14px;
                    background:#eef3f7;
                    border-radius:20px;
                    font-size:0.8rem;
                    color:#4f46e5;
                    font-weight:500;
                    position:relative;
                    top:1px;
                ">
                    <span style="
                        width:8px;
                        height:8px;
                        background:#2962FF;
                        border-radius:50%;
                    "></span>
                    Real-time
                </span>
                <span style="
                    display:flex;
                    align-items:center;
                    height:32px;
                    padding:0 14px;
                    background:#eef3f7;
                    border-radius:20px;
                    font-size:0.8rem;
                    color:#4f46e5;
                    font-weight:500;
                    position:relative;
                    top:8px;
                ">
                    🐘 PostgreSQL
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # ------------------------------------------------------------------------
    # CONTROLLER SIDEBAR: EXECUTIVE PRIVILEGES
    # ------------------------------------------------------------------------
    with st.sidebar:
        st.image("https://img.icons8.com/fluent/96/000000/manager.png", width=75)
        st.markdown("### 🔒 Security Clearances")
        
        # User Persona Selector Integration
        active_user = st.selectbox(
            "Select Governance Role",
            ["Rector", "Vice Chancellor", "Dean", "HOD", "University Admin"]
        )
        
        st.markdown(f"<div class='role-badge'>🛡️ Access Level: {active_user}</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Data Pipeline Connector Configuration
        data_mode = st.radio("Pipeline Stream", ["📊 Simulation Engine", "📡 Production Datastore"])
        loaded_df = None
        
        if data_mode == "📡 Production Datastore":
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                    tables = [t[0] for t in cursor.fetchall()]
                    if tables:
                        target_table = st.selectbox("Target Analytical Schema", tables)
                        if st.button("Synchronize Architecture", use_container_width=True):
                            raw = load_executive_data(conn, target_table)
                            if raw is not None:
                                st.session_state['exec_data_store'] = raw
                                st.success("Data Pipeline Synchronized!")
                except Exception as ex:
                    st.error(f"Schema Connection Aborted: {str(ex)}")
            else:
                st.warning("Production Cloud unreachable. Defaulting safely to Simulation Engine.")
                data_mode = "📊 Simulation Engine"
                
        if data_mode == "📊 Simulation Engine" or 'exec_data_store' not in st.session_state:
            if 'exec_data_store' not in st.session_state or data_mode == "📊 Simulation Engine":
                st.session_state['exec_data_store'] = generate_executive_mock_data()
        
        # Pull master frame out of state
        df_master = st.session_state['exec_data_store']
        
        # Global Interactive Control Filters
        st.markdown("### 🛠️ Global Filters")
        selected_dept = st.selectbox("Department Focus", ["All Strategic Sectors"] + sorted(list(df_master['department'].unique())))
        selected_sem = st.selectbox("Academic Phase Timeline", ["Full Matrix View"] + sorted(list(df_master['semester'].unique())))
        
        # Algorithmic Filtering Pipeline
        df_filtered = df_master.copy()
        if selected_dept != "All Strategic Sectors":
            df_filtered = df_filtered[df_filtered['department'] == selected_dept]
        if selected_sem != "Full Matrix View":
            df_filtered = df_filtered[df_filtered['semester'] == selected_sem]

    # ------------------------------------------------------------------------
    # SYSTEM EXECUTIVE NAVIGATION SYSTEM
    # ------------------------------------------------------------------------
    menu_tabs = option_menu(
        menu_title=None,
        options=["Command Center", "Financial Performance", "Academic Profiles", "Departmental Grid"],
        icons=["sliders", "currency-dollar", "mortarboard", "grid-3x3-gap"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#ffffff", "border-radius": "14px", "box-shadow": "0 2px 10px rgba(0,0,0,0.02)"},
            "icon": {"color": "#4fc3f7", "font-size": "16px"},
            "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "color": "#4a6f8a", "--hover-color": "#f1f8ff"},
            "nav-link-selected": {"background-color": "#e3f2fd", "color": "#0d47a1", "font-weight": "600"}
        }
    )

    # ------------------------------------------------------------------------
    # KPI INTERFACE MATRICES COMPILATION
    # ------------------------------------------------------------------------
    # Metric Calculations Engine
    total_students = len(df_filtered['student_id'].unique())
    gross_revenue = df_filtered['fee_allocated'].sum()
    collected_fee = df_filtered['fee_collected'].sum()
    fee_collection_efficiency = (collected_fee / gross_revenue * 100) if gross_revenue > 0 else 0.0
    institutional_gpa = df_filtered['gpa'].mean()
    institutional_attendance = df_filtered['attendance'].mean()

    # ============================================================================
    # TAB VIEW 1: CENTRAL COMMAND EXECUTIVE OVERVIEW
    # ============================================================================
    if menu_tabs == "Command Center":
        st.markdown(f"### 📊 Analytical Scope Dashboard for: *{active_user}*")
        
        # 5 High-Level Strategic Core KPI Cards Display
        kpi_cols = st.columns(5)
        
        with kpi_cols[0]:
            st.markdown(f"""
                <div class='metric-card' style='border-top-color: #64b5f6;'>
                    <h3>👥 Total Enrolment</h3>
                    <h2>{total_students:,}</h2>
                    <p>Active Registered Profiles</p>
                </div>
            """, unsafe_allow_html=True)
            
        with kpi_cols[1]:
            st.markdown(f"""
                <div class='metric-card' style='border-top-color: #81c784;'>
                    <h3>💰 Gross Revenue Target</h3>
                    <h2>${gross_revenue/1000000:.2f}M</h2>
                    <p>Total Billing Allocation</p>
                </div>
            """, unsafe_allow_html=True)
            
        with kpi_cols[2]:
            st.markdown(f"""
                <div class='metric-card' style='border-top-color: #4db6ac;'>
                    <h3>📊 Institutional GPA</h3>
                    <h2>{institutional_gpa:.2f} / 4.0</h2>
                    <p>Current Academic Quality</p>
                </div>
            """, unsafe_allow_html=True)
            
        with kpi_cols[3]:
            st.markdown(f"""
                <div class='metric-card' style='border-top-color: #ffb74d;'>
                    <h3>📅 Mean Attendance</h3>
                    <h2>{institutional_attendance:.1f}%</h2>
                    <p>Classroom Engagement Factor</p>
                </div>
            """, unsafe_allow_html=True)
            
        with kpi_cols[4]:
            st.markdown(f"""
                <div class='metric-card' style='border-top-color: #ba68c8;'>
                    <h3>📈 Fee Collection Rate</h3>
                    <h2>{fee_collection_efficiency:.1f}%</h2>
                    <p>Liquidity Operational Ratio</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Visual Matrices Layout
        graph_cols = st.columns([3, 2])
        
        with graph_cols[0]:
            st.markdown("#### ⏳ Structural Performance Framework Scatter Matrix")
            # Strategic Quadrant Charting: GPA vs Attendance vs Department Allocation
            fig_quad = px.scatter(
                df_filtered.sample(min(len(df_filtered), 1000)),
                x='attendance',
                y='gpa',
                color='department',
                size='fee_allocated',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                labels={'attendance': 'Attendance (%)', 'gpa': 'Student Cumulative GPA'},
                opacity=0.6
            )
            fig_quad.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=400)
            st.plotly_chart(fig_quad, use_container_width=True)
            
        with graph_cols[1]:
            st.markdown("#### 🏛️ Governance Risk Profile Monitor")
            # Executive Gauges System For Financial and Academic Health Indicators
            gauge_fig = make_subplots(rows=2, cols=1, specs=[[{'type': 'indicator'}], [{'type': 'indicator'}]])
            
            gauge_fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=fee_collection_efficiency,
                title={'text': "Collection Efficiency Index", 'font': {'size': 14}},
                gauge={'bar': {'color': "#81c784"}, 'steps': [{'range': [0, 75], 'color': "#ffebee"}, {'range': [75, 100], 'color': "#e8f5e9"}]}
            ), row=1, col=1)
            
            gauge_fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=institutional_attendance,
                title={'text': "Critical Core Attendance Threshold", 'font': {'size': 14}},
                gauge={'bar': {'color': "#4fc3f7"}, 'steps': [{'range': [0, 75], 'color': "#fff3e0"}, {'range': [75, 100], 'color': "#e1f5fe"}]}
            ), row=2, col=1)
            
            gauge_fig.update_layout(height=400, margin=dict(t=30, b=10))
            st.plotly_chart(gauge_fig, use_container_width=True)

    # ============================================================================
    # TAB VIEW 2: FINANCIAL HEALTH PERFORMANCE ARCHITECTURE
    # ============================================================================
    elif menu_tabs == "Financial Performance":
        st.markdown("### 💳 Liquidity Allocation & Revenue Auditing Engine")
        
        fin_cols = st.columns([2, 1])
        
        with fin_cols[0]:
            st.markdown("#### 📊 Sector-Wise Revenue Allocation Breakdown")
            # Stacked Comparative Performance Charting
            rev_dept = df_filtered.groupby('department')[['fee_allocated', 'fee_collected']].sum().reset_index()
            fig_rev = go.Figure()
            fig_rev.add_trace(go.Bar(name='Invoiced Billing', x=rev_dept['department'], y=rev_dept['fee_allocated'], marker_color='#bbdefb'))
            fig_rev.add_trace(go.Bar(name='Realized Liquidity', x=rev_dept['department'], y=rev_dept['fee_collected'], marker_color='#c8e6c9'))
            fig_rev.update_layout(barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=450)
            st.plotly_chart(fig_rev, use_container_width=True)
            
        with fin_cols[1]:
            st.markdown("#### 💸 Institutional Collection Ratios")
            # Donut distribution overview
            outstanding_val = gross_revenue - collected_fee
            fig_donut = px.pie(
                names=['Liquidity Realized', 'Outstanding Receivables'],
                values=[collected_fee, outstanding_val],
                hole=0.5,
                color_discrete_sequence=['#a5d6a7', '#ef9a9a']
            )
            fig_donut.update_layout(height=450, showlegend=True, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_donut, use_container_width=True)

    # ============================================================================
    # TAB VIEW 3: ACADEMIC QUALITY PROFILE MATRIX
    # ============================================================================
    elif menu_tabs == "Academic Profiles":
        st.markdown("### 🎓 Institutional Intelligence & Academic Assessment Profiles")
        
        acad_cols = st.columns(2)
        
        with acad_cols[0]:
            st.markdown("#### 📈 Cumulative Student GPA Density Vector Distribution")
            # Trend Profile distributions density curve mapping 
            fig_gpa = px.histogram(
                df_filtered, 
                x='gpa', 
                nbins=30, 
                color_discrete_sequence=['#b3e5fc'],
                marginal="box"
            )
            fig_gpa.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=450)
            st.plotly_chart(fig_gpa, use_container_width=True)
            
        with acad_cols[1]:
            st.markdown("#### ⏳ Institutional Engagement Framework Analysis")
            # Box distributions analyzing Department vs Attendance metrics
            fig_box = px.box(
                df_filtered,
                x='department',
                y='attendance',
                color='department',
                color_discrete_sequence=px.colors.pastel.Pastel1
            )
            fig_box.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=450, showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)

    # ============================================================================
    # TAB VIEW 4: STRATEGIC DEPARTMENTAL DATA MATRIX GRID
    # ============================================================================
    elif menu_tabs == "Departmental Grid":
        st.markdown("### 🏢 Departmental Matrix Scorecard")
        
        # Algorithmic compilation grouping processing of operations
        dept_summary = df_filtered.groupby('department').agg(
            Enrolled_Students=('student_id', 'count'),
            Average_GPA=('gpa', 'mean'),
            Attendance_Rate=('attendance', 'mean'),
            Target_Revenue=('fee_allocated', 'sum'),
            Collected_Revenue=('fee_collected', 'sum')
        ).reset_index()
        
        # Formatting computations
        dept_summary['Collection_Efficiency'] = (dept_summary['Collected_Revenue'] / dept_summary['Target_Revenue'] * 100).round(2).astype(str) + '%'
        dept_summary['Average_GPA'] = dept_summary['Average_GPA'].round(2)
        dept_summary['Attendance_Rate'] = dept_summary['Attendance_Rate'].round(1).astype(str) + '%'
        dept_summary['Target_Revenue'] = dept_summary['Target_Revenue'].map('${:,.2f}'.format)
        dept_summary['Collected_Revenue'] = dept_summary['Collected_Revenue'].map('${:,.2f}'.format)
        
        # Displaying Core Matrix Architecture
        st.dataframe(dept_summary, use_container_width=True, hide_index=True)
        
        # System Executive Level Data Export Control Matrix Architecture Block
        st.markdown("---")
        st.markdown("#### 📥 Secure Audit Logging Export Module")
        csv_buffer = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="🔒 Export Comprehensive Audit Data Stream as CSV",
            data=csv_buffer,
            file_name=f"EXECUTIVE_AUDIT_LOG_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

        # Footer - Place this at the end of your main() function
    st.markdown("""
        <div class='footer' style='display: block !important; visibility: visible !important; opacity: 1 !important;'>
            <p><strong style='color: #4f46e5; display: inline-block;'>University Enterprise Resource Planning System (ERP)</strong></p>
            <p style='font-size:0.8rem; color: #78909c;'>Protected Under Institutional Cryptographic Architecture Level V Enterprise Governance Suite</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

