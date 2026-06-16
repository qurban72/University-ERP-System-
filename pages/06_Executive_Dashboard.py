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
# LIGHT & SOFT CSS - GENTLE COLORS, EXECUTIVE PASTELS
# ============================================================================
st.markdown("""
    <style>
    /* Main Header - Soft Executive gradient */
    .main-header {
        background: linear-gradient(135deg, #e3f2fd 0%, #e0f7fa 50%, #f3e5f5 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .main-header h1 {
        color: #1a446c !important;
        margin: 0 !important;
    }
    
    .main-header p {
        color: #4a6f8a !important;
    }
    
    /* Headings styling */
    h1, h2, h3, h4, h5, h6 {
        color: #2c5270 !important;
        font-weight: 500 !important;
    }
    
    /* Metric Cards - Light luxury pastel system */
    .metric-card {
        background: linear-gradient(135deg, #ffffff, #fcfdfe);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        text-align: center;
        border-top: 4px solid #90caf9;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
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

    /* Strategic Role Badge Custom Style */
    .role-badge {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 0.4rem 1.2rem;
        border-radius: 50px;
        color: #2e7d32 !important;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    /* Navigation Menu System Override */
    .nav-link-selected {
        background: linear-gradient(135deg, #bbdefb 0%, #e1f5fe 100%) !important;
        color: #0d47a1 !important;
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
            'attendance': np.random.beta(a=7, b=2) * 100, # Realistic skewed attendance
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
        <div style='text-align: right; margin-bottom: -1rem;'>
            <p style='color: #78909c; font-size: 0.85rem;'>👑 System Status: Secure | Operational 🕐 {get_live_datetime()}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='main-header'>
            <h1>🏛️ Executive Command Dashboard</h1>
            <p style='font-size: 1.1rem; margin-top: 0.5rem;'>Strategic Institutional KPIs & Resource Planning Analytics</p>
        </div>
    """, unsafe_allow_html=True)
    
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
                color_discrete_sequence=px.colors.pastel.Pastel,
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
            st.markdown("#### 💸 Institutional Collection R
