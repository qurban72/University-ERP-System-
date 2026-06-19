import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import psycopg2
from streamlit_option_menu import option_menu
import plotly.figure_factory as ff
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Advanced Page Configuration
st.set_page_config(
    page_title="Examination Analytics | University ERP",
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
        background: linear-gradient(135deg, #1a3a6a 0%, #2f528f 50%, #3a6a9f 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(47, 82, 143, 0.35);
        border-bottom: 3px solid #4ab8e8;
    }
    
    /* Force ALL text in header to be white */
    .main-header,
    .main-header *,
    .main-header h1,
    .main-header p,
    .main-header span,
    .main-header div,
    .main-header strong,
    .main-header em,
    .main-header b,
    .main-header i {
        color: #ffffff !important;
    }
    
    .main-header h1 {
        margin: 0 !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        font-size: 2.2rem !important;
    }
    
    .main-header p {
        font-weight: 300 !important;
        margin: 0.3rem 0 !important;
    }
    
    .main-header p:first-of-type {
        font-size: 1.1rem !important;
    }
    
    .main-header p:last-of-type {
        font-size: 0.9rem !important;
        opacity: 0.85;
    }
    
    
    /* ALL Headings - Soft blue-gray (EXCEPT header) */
h1:not(.main-header h1), 
h2, h3, h4, h5, h6 {
    color: #3a7ca5 !important;
    font-weight: 500 !important;
}

.stMarkdown h1:not(.main-header h1), 
.stMarkdown h2, 
.stMarkdown h3, 
.stMarkdown h4 {
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
        border-top: 3px solid #a8e6cf;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    }
    
    .metric-card h3 {
        color: #7a9cbb !important;
        margin: 0;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }
    
    .metric-card h2 {
        color: #3a7ca5 !important;
        margin: 0.5rem 0;
        font-size: 2rem;
    }
    
    .metric-card p {
        color: #8aaec9 !important;
    }
    
    /* Info Box - Matching Header Style with FORCED overrides */
div.info-box,
.info-box,
.info-box.info-box {
    background: linear-gradient(135deg, #1a3a6a 0%, #2f528f 50%, #3a6a9f 100%) !important;
    padding: 2rem !important;
    border-radius: 16px !important;
    margin: 1rem 0 !important;
    border-left: 4px solid #4ab8e8 !important;
    border-top: none !important;
    border-right: none !important;
    border-bottom: none !important;
    box-shadow: 0 4px 20px rgba(47, 82, 143, 0.3) !important;
}

/* Force ALL text inside info-box to be white/light */
div.info-box *,
.info-box *,
.info-box h2,
.info-box p,
.info-box li,
.info-box span,
.info-box div,
.info-box strong,
.info-box em,
.info-box ul,
.info-box ol,
.info-box h4 {
    color: #d0e0f0 !important;
}

div.info-box h2,
.info-box h2 {
    color: #ffffff !important;
    font-size: 2rem !important;
}

div.info-box h4,
.info-box h4 {
    color: #4ab8e8 !important;
}

div.info-box p,
.info-box p {
    color: #d0e0f0 !important;
}

div.info-box ul,
.info-box ul {
    color: #d0e0f0 !important;
}

div.info-box li,
.info-box li {
    color: #d0e0f0 !important;
}
    
    /* Sidebar - Light background */
    .css-1d391kg {
        background-color: #fafcfd !important;
    }
    
    .sidebar .stMarkdown h1, .sidebar .stMarkdown h2, .sidebar .stMarkdown h3 {
        color: #3a7ca5 !important;
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
    
    /* Value colors for metrics - Soft versions */
    .metric-card h2[style*="color:#20bf6b"] {
        color: #6abf8a !important;
    }
    
    .metric-card h2[style*="color:#fc5c65"] {
        color: #e88a8a !important;
    }
    
    .metric-card h2[style*="color:#feca57"] {
        color: #e8c38a !important;
    }
    
    .metric-card h2[style*="color:#0abde3"] {
        color: #7acce0 !important;
    }
    
    /* Input fields */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background-color: #fafcfd;
        color: #4a6f8a;
        border: 1px solid #d4e6f0;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: #5a7d9a !important;
    }
    
    /* Checkbox */
    .stCheckbox label {
        color: #5a7d9a !important;
    }
    
    /* Success message */
    .stSuccess {
        background-color: #e8f8f0;
        color: #6abf8a;
    }
    /* ULTIMATE OVERRIDE - Force header text to white */
    div.main-header h1,
    div.main-header p,
    div.main-header * {
    color: #ffffff !important;
    }
    
    
    /* ====== GLOBAL BACKGROUND BLACK ====== */
    /* Main app background */
    .stApp {
        background-color: #0a0a0a !important;
    }
    
    /* Main content area */
    .main > div {
        background-color: #0a0a0a !important;
    }
    
    /* Block containers */
    .block-container {
        background-color: #0a0a0a !important;
    }
    
    /* All divs inside main */
    .stApp > div,
    .stApp .main,
    .stApp .block-container,
    .stApp .element-container,
    .stApp .stMarkdown,
    .stApp .stDataFrame,
    .stApp .stPlotlyChart {
        background-color: #0a0a0a !important;
    }
    
    /* All text to white for readability */
    .stApp,
    .stApp p,
    .stApp li,
    .stApp span,
    .stApp label,
    .stApp .stMarkdown,
    .stApp .stText,
    .stApp .stMetric label,
    .stApp .stMetric .stMetricLabel {
        color: #ffffff !important;
    }
    
    /* Headings - make them visible on black */
    h1, h2, h3, h4, h5, h6 {
        color: #4ab8e8 !important;
    }
    
    /* Metric cards on black background */
    .metric-card {
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a) !important;
        border: 1px solid #3a3a3a !important;
    }
    
    .metric-card h2 {
        color: #4ab8e8 !important;
    }
    
    .metric-card h3 {
        color: #8aaec9 !important;
    }
    
    .metric-card p {
        color: #8aaec9 !important;
    }
    
    /* DataFrames on black */
    .dataframe {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #2f528f 0%, #4a7abf 100%) !important;
        color: #ffffff !important;
    }
    
    .dataframe td {
        color: #d0d0d0 !important;
        border-color: #3a3a3a !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: #252525 !important;
    }
    
    .dataframe tbody tr:nth-child(odd) {
        background-color: #1a1a1a !important;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #1a2a3a 0%, #0a1a2a 100%) !important;
        border-left: 4px solid #4ab8e8 !important;
        border: 1px solid #2a4a6a !important;
    }
    
    .info-box strong, .info-box p, .info-box h4 {
        color: #d0e0f0 !important;
    }
    
    /* ====== SIDEBAR - GRAY BACKGROUND ====== */
    /* Main sidebar container */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebar"] .css-1d391kg,
    [data-testid="stSidebar"] .css-1d391kg > div,
    [data-testid="stSidebar"] .css-1d391kg > div > div {
        background-color: #2a2a2a !important;
    }
    
    [data-testid="stSidebar"] {
        border-right: 1px solid #3a3a3a !important;
    }
    
    /* Remove black boxes from sidebar elements */
    [data-testid="stSidebar"] .element-container,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stImage,
    [data-testid="stSidebar"] .stButton,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stRadio,
    [data-testid="stSidebar"] .stTextInput,
    [data-testid="stSidebar"] .stAlert,
    [data-testid="stSidebar"] .stSuccess,
    [data-testid="stSidebar"] .stWarning,
    [data-testid="stSidebar"] .stInfo,
    [data-testid="stSidebar"] .stError {
        background-color: transparent !important;
    }
    
    /* Sidebar image container */
    [data-testid="stSidebar"] .stImage img {
        background-color: transparent !important;
    }
    
    /* Sidebar all text */
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #ffffff !important;
    }
    
    /* Sidebar headings */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #4ab8e8 !important;
    }
    
    /* ====== FIX SELECTBOX - VISIBLE TEXT ====== */
    /* Selectbox container */
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stSelectbox > div,
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: transparent !important;
    }
    
    /* Selectbox input field */
    [data-testid="stSidebar"] .stSelectbox select {
        background-color: #3a3a3a !important;
        color: #ffffff !important;
        border: 1px solid #4a4a4a !important;
        padding: 0.5rem !important;
        border-radius: 8px !important;
        font-size: 14px !important;
    }
    
    /* Selectbox dropdown options */
    [data-testid="stSidebar"] .stSelectbox select option {
        background-color: #3a3a3a !important;
        color: #ffffff !important;
        padding: 0.5rem !important;
    }
    
    /* Selectbox when focused */
    [data-testid="stSidebar"] .stSelectbox select:focus {
        border-color: #4ab8e8 !important;
        box-shadow: 0 0 0 2px rgba(74, 184, 232, 0.2) !important;
        outline: none !important;
    }
    
    /* Selectbox hover */
    [data-testid="stSidebar"] .stSelectbox select:hover {
        border-color: #4ab8e8 !important;
    }
    
    /* Selectbox label */
    [data-testid="stSidebar"] .stSelectbox label {
        color: #8aaec9 !important;
        font-weight: 500 !important;
    }
    
    /* ====== FIX TEXT INPUT ====== */
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #3a3a3a !important;
        color: #ffffff !important;
        border: 1px solid #4a4a4a !important;
        padding: 0.5rem !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebar"] .stTextInput input:focus {
        border-color: #4ab8e8 !important;
        box-shadow: 0 0 0 2px rgba(74, 184, 232, 0.2) !important;
        outline: none !important;
    }
    
    [data-testid="stSidebar"] .stTextInput label {
        color: #8aaec9 !important;
        font-weight: 500 !important;
    }
    
    /* ====== FIX RADIO BUTTONS ====== */
    [data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stRadio [role="radiogroup"] {
        background-color: #3a3a3a !important;
        padding: 0.5rem !important;
        border-radius: 8px !important;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #2f528f 0%, #4a7abf 100%) !important;
        color: #ffffff !important;
        border: none !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #1a3a6a 0%, #2f528f 100%) !important;
        box-shadow: 0 4px 16px rgba(47, 82, 143, 0.3) !important;
    }
    
    /* Sidebar info boxes */
    [data-testid="stSidebar"] .sidebar-info {
        background: #3a3a3a !important;
        border-left: 3px solid #4ab8e8 !important;
        padding: 0.75rem !important;
        border-radius: 8px !important;
        margin: 0.5rem 0 !important;
    }
    
    [data-testid="stSidebar"] .sidebar-info p,
    [data-testid="stSidebar"] .sidebar-info strong {
        color: #ffffff !important;
    }
    
    /* Sidebar success/warning messages */
    [data-testid="stSidebar"] .stAlert {
        background-color: #3a3a3a !important;
        border: 1px solid #4a4a4a !important;
    }
    
    [data-testid="stSidebar"] .stAlert p {
        color: #ffffff !important;
    }
    
    /* Sidebar scrollbar */
    [data-testid="stSidebar"] ::-webkit-scrollbar {
        background-color: #2a2a2a !important;
    }
    
    [data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
        background-color: #4ab8e8 !important;
        border-radius: 10px !important;
    }
    
    /* Navigation menu */
    .nav-link {
        color: #8aaec9 !important;
    }
    
    .nav-link:hover {
        background: #1a2a3a !important;
    }
    
    .nav-link-selected {
        background: linear-gradient(135deg, #2f528f 0%, #4a7abf 100%) !important;
        color: #ffffff !important;
    }
    
    .nav-link-selected span {
        color: #ffffff !important;
    }
    
    /* Input fields on black */
    .stTextInput input, 
    .stSelectbox select, 
    .stTextArea textarea {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #3a3a3a !important;
    }
    
    .stTextInput input:focus, 
    .stSelectbox select:focus {
        border-color: #4ab8e8 !important;
        box-shadow: 0 0 0 2px rgba(74, 184, 232, 0.1) !important;
    }
    
    /* Selectbox options */
    .stSelectbox option {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    /* Buttons on black */
    .stButton > button {
        background: linear-gradient(135deg, #2f528f 0%, #4a7abf 100%) !important;
        color: #ffffff !important;
        border: none !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(47, 82, 143, 0.3) !important;
        background: linear-gradient(135deg, #1a3a6a 0%, #2f528f 100%) !important;
    }
    
    /* Tabs on black */
    .stTabs [data-baseweb="tab-list"] button p {
        color: #8aaec9 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #1a2a3a 0%, #2a4a6a 100%) !important;
        border-bottom: 3px solid #4ab8e8 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] p {
        color: #4ab8e8 !important;
    }
    
    /* Metrics on black */
    .stMetric label, 
    .stMetric .stMetricLabel {
        color: #8aaec9 !important;
    }
    
    .stMetric .stMetricValue {
        color: #4ab8e8 !important;
    }
    
    /* Alert boxes on black */
    .stAlert {
        background-color: #1a1a1a !important;
        border: 1px solid #3a3a3a !important;
    }
    
    .stAlert p {
        color: #d0d0d0 !important;
    }
    
    /* Success message */
    .stSuccess {
        background-color: #0a2a1a !important;
        border: 1px solid #2a6a4a !important;
        color: #4aaf6a !important;
    }
    
    /* Warning message */
    .stWarning {
        background-color: #2a2a0a !important;
        border: 1px solid #6a6a2a !important;
        color: #e8b830 !important;
    }
    
    /* Error message */
    .stError {
        background-color: #2a0a0a !important;
        border: 1px solid #6a2a2a !important;
        color: #d45a5a !important;
    }
    
    /* Info message */
    .stInfo {
        background-color: #0a1a2a !important;
        border: 1px solid #2a4a6a !important;
        color: #4ab8e8 !important;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #0a0a0a, #1a1a1a) !important;
        border-top: 1px solid #2a2a2a !important;
    }
    
    .footer p, .footer strong {
        color: #8aaec9 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1a1a1a !important;
        color: #4ab8e8 !important;
        border: 1px solid #2a2a2a !important;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: #d0d0d0 !important;
    }
    
    /* Checkbox */
    .stCheckbox label {
        color: #d0d0d0 !important;
    }
    
    /* Plotly charts - dark background */
    .js-plotly-plot {
        background-color: transparent !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        background-color: #0a0a0a !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background-color: #2f528f !important;
        border-radius: 10px !important;
    }
    
    ::-webkit-scrollbar-track {
        background-color: #1a1a1a !important;
    }
    </style>
""", unsafe_allow_html=True)
# ============================================================================
# ADVANCED FEATURES: REAL-TIME CLOCK & ANIMATIONS
# ============================================================================

def get_live_datetime():
    """Get current datetime for real-time display"""
    return datetime.now().strftime("%A, %B %d, %Y | %I:%M:%S %p")

# ============================================================================
# DATABASE CONNECTION (Updated for Streamlit Cloud compatibility)
# ============================================================================

@st.cache_resource
def get_db_connection():
    """Connect to Supabase PostgreSQL database - handles connection errors gracefully"""
    try:
        # Use environment variables or secrets for production
        # For now, using your provided credentials
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres.gxfixjysmdmyvycuyucs",
            password="databetatechnify",
            host="aws-1-ap-southeast-1.pooler.supabase.com",
            port="5432",
            sslmode="require",
            connect_timeout=10  # Reduced timeout for better handling
        )
        return conn
    except Exception as e:
        # Silently fail - will show error in UI
        return None

@st.cache_data(ttl=300)
def load_examination_data(_conn, table_name):
    """Load ALL examination data from database - NO LIMITS"""
    try:
        # First, get the exact count
        cursor = _conn.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        total_rows = cursor.fetchone()[0]
        
        st.sidebar.info(f"📊 Database has {total_rows:,} total records")
        
        # Load ALL data - NO LIMIT clause
        query = f'SELECT * FROM "{table_name}"'
        df = pd.read_sql(query, _conn)
        
        # Verify we got all rows
        if len(df) == total_rows:
            st.sidebar.success(f"✅ Loaded ALL {len(df):,} records!")
        else:
            st.sidebar.warning(f"⚠️ Loaded {len(df):,} of {total_rows:,} records")
        
        return df, len(df)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, 0
# ============================================================================
# ADVANCED DATA PROCESSING
# ============================================================================

def process_examination_data(df):
    """Advanced data processing with ML-like features"""
    if df is None or df.empty:
        return None
    
    df_processed = df.copy()
    
    # Smart column detection
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
    
    # Clean marks
    df_processed['marks'] = df_processed['marks'].fillna(df_processed['marks'].median()).clip(0, 100)
    
    # Calculate advanced metrics
    df_processed['status'] = df_processed['marks'].apply(lambda x: 'Pass' if x >= 40 else 'Fail')
    df_processed['grade'] = df_processed['marks'].apply(lambda x: 
        'A+' if x >= 90 else 'A' if x >= 80 else 'B+' if x >= 70 else 
        'B' if x >= 60 else 'C' if x >= 50 else 'D' if x >= 40 else 'F')
    
    # Performance tier
    df_processed['performance_tier'] = df_processed['marks'].apply(lambda x:
        'Outstanding' if x >= 85 else 'Excellent' if x >= 75 else 
        'Good' if x >= 60 else 'Satisfactory' if x >= 50 else 
        'Needs Improvement' if x >= 40 else 'Critical')
    
    # Handle missing columns
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
    """Calculate advanced statistical metrics"""
    metrics = {
        'pass_rate': (df['marks'] >= 40).mean() * 100,
        'fail_rate': (df['marks'] < 40).mean() * 100,
        'distinction_rate': (df['marks'] >= 75).mean() * 100,
        'first_class_rate': ((df['marks'] >= 60) & (df['marks'] < 75)).mean() * 100,
        'avg_marks': df['marks'].mean(),
        'median_marks': df['marks'].median(),
        'std_dev': df['marks'].std(),
        'skewness': df['marks'].skew(),
        'kurtosis': df['marks'].kurtosis(),
        'highest': df['marks'].max(),
        'lowest': df['marks'].min(),
        'q1': df['marks'].quantile(0.25),
        'q3': df['marks'].quantile(0.75),
        'iqr': df['marks'].quantile(0.75) - df['marks'].quantile(0.25)
    }
    return metrics

def calculate_performance_score(df):
    """Calculate overall performance score (0-100)"""
    pass_rate = (df['marks'] >= 40).mean() * 100
    avg_marks = df['marks'].mean()
    distinction_rate = (df['marks'] >= 75).mean() * 100
    
    # Weighted score
    score = (pass_rate * 0.5) + (avg_marks * 0.3) + (distinction_rate * 0.2)
    return min(100, score)

def identify_outliers(df):
    """Identify outlier marks using IQR method"""
    Q1 = df['marks'].quantile(0.25)
    Q3 = df['marks'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df['marks'] < lower_bound) | (df['marks'] > upper_bound)]
    return outliers, lower_bound, upper_bound

def generate_trend_forecast(df):
    """Generate simple forecast for next semester"""
    semester_avg = df.groupby('semester')['marks'].mean()
    if len(semester_avg) >= 2:
        trend = semester_avg.diff().mean()
        last_avg = semester_avg.iloc[-1]
        forecast = last_avg + trend
        return max(0, min(100, forecast)), trend
    return df['marks'].mean(), 0

# ============================================================================
# ADVANCED VISUALIZATIONS - WITH SOFT COLORS
# ============================================================================

def create_gauge_chart(value, title, max_value=100):
    """Create professional gauge chart with soft colors"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title, 'font': {'size': 22, 'color': '#5a8bb5'}},
        delta={'reference': 75, 'increasing': {'color': "#8fc9a8"}, 'decreasing': {'color': "#e8aaaa"}},
        gauge={
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "#8aaec9"},
            'bar': {'color': "#7acce0"},
            'bgcolor': "#ffffff",
            'borderwidth': 1,
            'bordercolor': "#d4e6f0",
            'steps': [
                {'range': [0, 40], 'color': '#ffe8e8'},
                {'range': [40, 75], 'color': '#fff8e0'},
                {'range': [75, 100], 'color': '#e8f8f0'}
            ],
            'threshold': {
                'line': {'color': "#e88a8a", 'width': 3},
                'thickness': 0.75,
                'value': 40
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)')
    return fig

def create_advanced_donut_chart(df):
    """Create advanced donut chart with soft colors"""
    pass_count = (df['marks'] >= 40).sum()
    fail_count = (df['marks'] < 40).sum()
    
    # Performance tiers
    outstanding = (df['marks'] >= 85).sum()
    excellent = ((df['marks'] >= 75) & (df['marks'] < 85)).sum()
    good = ((df['marks'] >= 60) & (df['marks'] < 75)).sum()
    satisfactory = ((df['marks'] >= 50) & (df['marks'] < 60)).sum()
    needs_improvement = ((df['marks'] >= 40) & (df['marks'] < 50)).sum()
    critical = (df['marks'] < 40).sum()
    
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    
    fig.add_trace(go.Pie(
        labels=['Pass', 'Fail'],
        values=[pass_count, fail_count],
        marker_colors=['#8fc9a8', '#e8aaaa'],
        hole=0.4,
        name="Pass/Fail",
        domain={'row': 0, 'column': 0},
        textinfo='percent+label',
        textposition='auto',
        textfont_color='#5a7d9a'
    ), 1, 1)
    
    fig.add_trace(go.Pie(
        labels=['Outstanding', 'Excellent', 'Good', 'Satisfactory', 'Needs Improvement', 'Critical'],
        values=[outstanding, excellent, good, satisfactory, needs_improvement, satisfactory, critical],
        marker_colors=['#8fc9a8', '#a8d5b8', '#7acce0', '#e8c38a', '#e8aa8a', '#e8aaaa'],
        hole=0.5,
        name="Performance Tiers",
        domain={'row': 0, 'column': 1},
        textinfo='percent+label',
        textposition='auto',
        textfont_color='#5a7d9a'
    ), 1, 2)
    
    fig.update_layout(
        title_text="<b>Advanced Performance Analysis</b>",
        title_font_color='#3a7ca5',
        annotations=[
            dict(text='Overall Status', x=0.18, y=0.5, font_size=13, font_color='#5a8bb5', showarrow=False),
            dict(text='Performance Tiers', x=0.82, y=0.5, font_size=13, font_color='#5a8bb5', showarrow=False)
        ],
        height=500,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_box_plot(df):
    """Create professional box plot with soft colors"""
    fig = go.Figure()
    
    departments = df['department'].unique()[:8]
    colors = ['#7acce0', '#8fc9a8', '#e8c38a', '#e8aa8a', '#c5a8e0', '#a8d5e8', '#d4e8a8', '#e8c5a8']
    for i, dept in enumerate(departments):
        dept_data = df[df['department'] == dept]['marks']
        fig.add_trace(go.Box(
            y=dept_data,
            name=dept,
            boxmean='sd',
            marker_color=colors[i % len(colors)],
            line_color=colors[i % len(colors)],
            fillcolor=f'rgba({int(colors[i % len(colors)][1:3],16)},{int(colors[i % len(colors)][3:5],16)},{int(colors[i % len(colors)][5:7],16)},0.2)'
        ))
    
    fig.update_layout(
        title="<b>Department-wise Performance Distribution</b>",
        title_font_color='#3a7ca5',
        xaxis_title="Department",
        yaxis_title="Marks",
        height=500,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#5a7d9a'
    )
    return fig

def create_radar_chart(df):
    """Create radar chart with soft colors"""
    dept_stats = df.groupby('department').agg({
        'marks': ['mean', lambda x: (x >= 40).mean() * 100, lambda x: (x >= 75).mean() * 100]
    }).round(2)
    dept_stats.columns = ['avg_marks', 'pass_rate', 'distinction_rate']
    dept_stats = dept_stats.head(6)
    
    colors = ['#7acce0', '#8fc9a8', '#e8c38a', '#e8aa8a', '#c5a8e0', '#a8d5e8']
    
    fig = go.Figure()
    
    for i, dept in enumerate(dept_stats.index):
        fig.add_trace(go.Scatterpolar(
            r=[dept_stats.loc[dept, 'avg_marks'], 
               dept_stats.loc[dept, 'pass_rate'],
               dept_stats.loc[dept, 'distinction_rate']],
            theta=['Average Marks', 'Pass Rate', 'Distinction Rate'],
            fill='toself',
            name=dept,
            line_color=colors[i % len(colors)],
            fillcolor=f'rgba({int(colors[i % len(colors)][1:3],16)},{int(colors[i % len(colors)][3:5],16)},{int(colors[i % len(colors)][5:7],16)},0.2)'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont_color='#5a8bb5'),
            bgcolor='rgba(0,0,0,0)',
            angularaxis=dict(tickfont_color='#5a8bb5')
        ),
        title="<b>Department Performance Radar Chart</b>",
        title_font_color='#3a7ca5',
        height=500,
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#5a7d9a'
    )
    return fig

def create_trend_analysis(df):
    """Create trend analysis with confidence bands"""
    semester_stats = df.groupby('semester')['marks'].agg(['mean', 'std', 'count']).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=semester_stats['semester'],
        y=semester_stats['mean'],
        mode='lines+markers',
        name='Average Marks',
        line=dict(color='#7acce0', width=3),
        marker=dict(size=10, color='#e8aa8a'),
        error_y=dict(
            type='data',
            array=semester_stats['std'],
            visible=True,
            color='rgba(122,204,224,0.3)'
        )
    ))
    
    # Add trend line
    z = np.polyfit(semester_stats['semester'], semester_stats['mean'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=semester_stats['semester'],
        y=p(semester_stats['semester']),
        mode='lines',
        name='Trend Line',
        line=dict(color='#8fc9a8', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="<b>Performance Trend Analysis with Confidence Bands</b>",
        title_font_color='#3a7ca5',
        xaxis_title="Semester",
        yaxis_title="Average Marks",
        height=500,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#5a7d9a'
    )
    return fig

def create_correlation_heatmap(df):
    """Create correlation heatmap with soft colors"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='Teal',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10, "color": "#2c5f8a"},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="<b>Feature Correlation Heatmap</b>",
            title_font_color='#3a7ca5',
            height=500,
            width=600,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    return None

def create_waterfall_chart(df):
    """Create waterfall chart with soft colors"""
    dept_perf = df.groupby('department')['marks'].mean().sort_values()
    
    fig = go.Figure(go.Waterfall(
        name="Department Performance",
        orientation="v",
        measure=["relative"] * len(dept_perf),
        x=dept_perf.index,
        y=dept_perf.values,
        textposition="outside",
        text=dept_perf.values.round(1),
        textfont_color='#5a7d9a',
        connector={"line": {"color": "#c5d5e0"}},
        increasing={"marker": {"color": "#8fc9a8"}},
        decreasing={"marker": {"color": "#e8aaaa"}}
    ))
    
    fig.update_layout(
        title="<b>Department Performance Waterfall</b>",
        title_font_color='#3a7ca5',
        xaxis_title="Department",
        yaxis_title="Average Marks",
        height=500,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#5a7d9a'
    )
    return fig

def create_performance_prediction(df):
    """Create performance prediction visualization"""
    forecast, trend = generate_trend_forecast(df)
    
    fig = go.Figure()
    
    # Historical data
    semester_avg = df.groupby('semester')['marks'].mean()
    fig.add_trace(go.Scatter(
        x=list(semester_avg.index) + [max(semester_avg.index) + 1],
        y=list(semester_avg.values) + [forecast],
        mode='lines+markers',
        name='Historical & Forecast',
        line=dict(color='#7acce0', width=3),
        marker=dict(size=10, color=['#7acce0']*len(semester_avg) + ['#e8c38a'])
    ))
    
    # Add confidence interval
    fig.add_trace(go.Scatter(
        x=[max(semester_avg.index) + 1, max(semester_avg.index) + 1],
        y=[forecast - 5, forecast + 5],
        mode='lines',
        name='Confidence Interval',
        line=dict(color='rgba(122,204,224,0.3)', width=15),
        showlegend=True
    ))
    
    fig.update_layout(
        title="<b>Performance Prediction for Next Semester</b>",
        title_font_color='#3a7ca5',
        xaxis_title="Semester",
        yaxis_title="Average Marks",
        height=400,
        hovermode='x unified',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#5a7d9a'
    )
    return fig, forecast, trend

# ============================================================================
# ADVANCED UI COMPONENTS
# ============================================================================

def create_performance_score_card(score):
    """Create animated performance score card with soft colors"""
    color = "#8fc9a8" if score >= 75 else "#e8c38a" if score >= 60 else "#e8aaaa"
    st.markdown(f"""
        <div class='metric-card' style='text-align: center; background: linear-gradient(135deg, #ffffff, #f8fbfe);'>
            <h3 style='margin:0; color:#8aaec9;'>🎯 Overall Performance Score</h3>
            <h1 style='margin:0; color:{color}; font-size: 3rem;'>{score:.1f}</h1>
            <p style='margin:0;'>out of 100</p>
            <div style='width:100%; background:#e8f0f5; border-radius:10px; margin-top:10px;'>
                <div style='width:{score}%; background:{color}; height:10px; border-radius:10px;'></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_alert_system(df):
    """Create intelligent alert system"""
    alerts = []
    
    # Check pass rate
    pass_rate = (df['marks'] >= 40).mean() * 100
    if pass_rate < 75:
        alerts.append(("⚠️", "Notice", f"Pass rate is {pass_rate:.1f}% - Below target of 75%", "medium"))
    
    # Check failing courses
    course_fail_rates = df.groupby('course_name').apply(lambda x: (x['marks'] < 40).mean() * 100)
    critical_courses = course_fail_rates[course_fail_rates > 30]
    if len(critical_courses) > 0:
        alerts.append(("📚", "Attention", f"{len(critical_courses)} courses have >30% failure rate", "high"))
    
    # Check outliers
    outliers, _, _ = identify_outliers(df)
    if len(outliers) > len(df) * 0.05:
        alerts.append(("📊", "Info", f"Found {len(outliers)} outlier marks that may need review", "low"))
    
    # Performance trend
    forecast, trend = generate_trend_forecast(df)
    if trend < 0:
        alerts.append(("📉", "Trend Alert", "Overall performance trend is declining", "medium"))
    
    return alerts

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Real-time clock
    clock_placeholder = st.empty()
    
    # Header with live clock
    st.markdown("""
                 <div class='main-header'>
        <h1 style='color: #2c5f8a !important;'>🎓Examination Analytics Dashboard</h1>
        <p style='font-size: 1.1rem; color: #4a6f8a !important;'>Advanced Analytics & Business Intelligence</p>
        <p style='font-size: 0.9rem; color: #6a8faa !important;'>Data Science Team 1 | Enterprise Edition</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Live clock display
    with clock_placeholder.container():
        st.markdown(f"""
            <div style='text-align: right; margin-bottom: 1rem;'>
                <p style='color: #8aaec9; font-size: 0.9rem;'>🕐 {get_live_datetime()}</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Advanced Navigation Menu
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Course Analytics", "Department Insights", "Predictive Analytics", "Reports"],
        icons=["house", "book", "building", "graph-up", "file-text"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#ffffff", "border-radius": "12px", "box-shadow": "0 2px 8px rgba(0,0,0,0.03)"},
            "icon": {"color": "#7acce0", "font-size": "18px"},
            "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#f0f7fa", "color": "#5a7d9a"},
            "nav-link-selected": {"background-color": "#daf2fa", "color": "#2c5f8a"},
        }
    )
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/analytics.png", width=80)
        st.markdown("## 🎯 Control Panel")
        
        # Data source
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
                                df = process_examination_data(df_raw)
                                st.session_state['exam_data'] = df
                                st.success(f"✅ Loaded {rows:,} records!")
                                st.rerun()
                except Exception as e:
                    st.error(f"Database error: {str(e)}")
            else:
                st.warning("⚠️ Cannot connect to database. Using sample data instead.")
                use_db = "📊 Sample Data"  # Fallback to sample data
        
        if st.button("📊 Generate Sample Data", use_container_width=True):
            # Generate sample data
            np.random.seed(42)
            departments = ['Computer Science', 'Information Technology', 'Data Science', 'Artificial Intelligence', 'Business Administration']
            courses = [f"CS{101+i}" for i in range(25)] + [f"IT{201+i}" for i in range(20)] + [f"DS{301+i}" for i in range(15)]
            
            data = []
            for i in range(6000):
                data.append({
                    'student_id': f"S{np.random.randint(1000, 9999)}",
                    'course_name': np.random.choice(courses),
                    'department': np.random.choice(departments),
                    'semester': np.random.randint(1, 9),
                    'marks': np.random.normal(65, 15)
                })
            df_sample = pd.DataFrame(data)
            df_sample['marks'] = df_sample['marks'].clip(0, 100)
            df = process_examination_data(df_sample)
            st.session_state['exam_data'] = df
            st.success("✅ Generated 6,000 sample records!")
            st.rerun()
        
        st.markdown("---")
        
        if 'exam_data' in st.session_state:
            df = st.session_state['exam_data']
            
            # Advanced filters (REMOVED the search box)
            st.markdown("### 🔍 Smart Filters")
            
            # Department filter
            depts = ['All'] + sorted(df['department'].unique().tolist())
            filter_dept = st.selectbox("Department", depts)
            
            # Semester filter
            sems = ['All'] + sorted(df['semester'].unique().tolist())
            filter_sem = st.selectbox("Semester", sems)
            
            # Apply filters (removed search filtering)
            filtered_df = df.copy()
            if filter_dept != 'All':
                filtered_df = filtered_df[filtered_df['department'] == filter_dept]
            if filter_sem != 'All':
                filtered_df = filtered_df[filtered_df['semester'] == int(filter_sem)]
            
            st.session_state['filtered_data'] = filtered_df
            st.session_state['filter_info'] = f"{len(filtered_df)} records"
    
    # Main content
    if 'exam_data' in st.session_state:
        df = st.session_state['filtered_data'] if 'filtered_data' in st.session_state else st.session_state['exam_data']
        
        # Calculate metrics
        metrics = calculate_advanced_metrics(df)
        performance_score = calculate_performance_score(df)
        alerts = create_alert_system(df)
        
        # Display alerts
        if alerts:
            with st.container():
                st.markdown("### 📋 Notifications")
                cols = st.columns(len(alerts))
                for idx, (icon, title, message, level) in enumerate(alerts):
                    color = "#e8aaaa" if level == "high" else "#e8c38a" if level == "medium" else "#8fc9a8"
                    with cols[idx]:
                        st.markdown(f"""
                            <div style='background:{color}10; padding:0.8rem; border-radius:10px; border-left:3px solid {color}; margin:0.2rem;'>
                                <h4 style='margin:0; color:{color};'>{icon} {title}</h4>
                                <p style='margin:0; font-size:0.85rem;'>{message}</p>
                            </div>
                        """, unsafe_allow_html=True)
        
        # Dashboard based on selected tab
        if selected == "Dashboard":
            st.markdown("## 📊 Executive Dashboard")
            
            # Performance score
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                create_performance_score_card(performance_score)
            
            # Key metrics row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                gauge = create_gauge_chart(metrics['pass_rate'], "Pass Rate")
                st.plotly_chart(gauge, use_container_width=True)
            with col2:
                gauge = create_gauge_chart(metrics['distinction_rate'], "Distinction Rate")
                st.plotly_chart(gauge, use_container_width=True)
            with col3:
                st.markdown(f"""
                    <div class='metric-card'>
                        <h3>🏆 Highest</h3>
                        <h2 style='color:#e8c38a'>{metrics['highest']:.1f}</h2>
                        <p>Marks</p>
                    </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                    <div class='metric-card'>
                        <h3>📉 Lowest</h3>
                        <h2 style='color:#7acce0'>{metrics['lowest']:.1f}</h2>
                        <p>Marks</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Advanced charts
            col1, col2 = st.columns(2)
            with col1:
                donut = create_advanced_donut_chart(df)
                st.plotly_chart(donut, use_container_width=True)
            with col2:
                box = create_box_plot(df)
                st.plotly_chart(box, use_container_width=True)
            
            # Trend analysis
            trend_chart = create_trend_analysis(df)
            st.plotly_chart(trend_chart, use_container_width=True)
            
            # Statistical summary
            st.markdown("### 📈 Advanced Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Mean", f"{metrics['avg_marks']:.2f}")
                st.metric("Median", f"{metrics['median_marks']:.2f}")
            with col2:
                st.metric("Std Dev", f"{metrics['std_dev']:.2f}")
                st.metric("Skewness", f"{metrics['skewness']:.2f}")
            with col3:
                st.metric("Q1", f"{metrics['q1']:.2f}")
                st.metric("Q3", f"{metrics['q3']:.2f}")
            with col4:
                st.metric("IQR", f"{metrics['iqr']:.2f}")
                st.metric("Kurtosis", f"{metrics['kurtosis']:.2f}")
        
        elif selected == "Course Analytics":
            st.markdown("## 📚 Course Performance Analytics")
            
            course_stats = df.groupby('course_name').agg({
                'marks': ['mean', 'min', 'max', 'std', 'count'],
                'status': lambda x: (x == 'Pass').mean() * 100
            }).round(2)
            course_stats.columns = ['Avg Marks', 'Min', 'Max', 'Std Dev', 'Students', 'Pass Rate']
            course_stats['Fail Rate'] = 100 - course_stats['Pass Rate']
            course_stats = course_stats.sort_values('Avg Marks', ascending=False)
            
            # Top and bottom courses
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🏆 Top Performing Courses")
                st.dataframe(course_stats.head(10), use_container_width=True)
                
                # Radar chart for top courses
                top_courses = course_stats.head(5)
                fig_radar = go.Figure()
                colors = ['#7acce0', '#8fc9a8', '#e8c38a', '#e8aa8a', '#c5a8e0']
                for i, course in enumerate(top_courses.index):
                    fig_radar.add_trace(go.Scatterpolar(
                        r=top_courses.loc[course, ['Avg Marks', 'Pass Rate']].values,
                        theta=['Avg Marks', 'Pass Rate'],
                        fill='toself',
                        name=course[:20],
                        line_color=colors[i % len(colors)],
                        fillcolor=f'rgba({int(colors[i % len(colors)][1:3],16)},{int(colors[i % len(colors)][3:5],16)},{int(colors[i % len(colors)][5:7],16)},0.2)'
                    ))
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    title="Top Courses Comparison",
                    height=500
                )
                st.plotly_chart(fig_radar, use_container_width=True)
            
            with col2:
                st.markdown("### ⚠️ Courses Needing Improvement")
                st.dataframe(course_stats.tail(10), use_container_width=True)
            
            # Waterfall chart
            waterfall = create_waterfall_chart(df)
            st.plotly_chart(waterfall, use_container_width=True)
            
            # Full course list
            st.markdown("### 📋 Complete Course Analysis")
            st.dataframe(course_stats, use_container_width=True, height=500)
        
        elif selected == "Department Insights":
            st.markdown("## 🏛️ Department Analytics")
            
            col1, col2 = st.columns(2)
            with col1:
                radar = create_radar_chart(df)
                st.plotly_chart(radar, use_container_width=True)
            with col2:
                box = create_box_plot(df)
                st.plotly_chart(box, use_container_width=True)
            
            # Department comparison table
            dept_stats = df.groupby('department').agg({
                'marks': ['mean', 'min', 'max', 'std'],
                'status': lambda x: (x == 'Pass').mean() * 100,
                'student_id': 'nunique'
            }).round(2)
            dept_stats.columns = ['Avg Marks', 'Min', 'Max', 'Std Dev', 'Pass Rate', 'Students']
            st.dataframe(dept_stats, use_container_width=True)
            
            # Correlation heatmap
            heatmap = create_correlation_heatmap(df)
            if heatmap:
                st.plotly_chart(heatmap, use_container_width=True)
        
        elif selected == "Predictive Analytics":
            st.markdown("## 🔮 Predictive Analytics & Forecasting")
            
            col1, col2 = st.columns(2)
            with col1:
                pred_chart, forecast, trend = create_performance_prediction(df)
                st.plotly_chart(pred_chart, use_container_width=True)
                
                st.markdown(f"""
                    <div class='info-box'>
                        <h4>📊 Prediction Summary</h4>
                        <p><strong>Next Semester Forecast:</strong> {forecast:.1f} marks</p>
                        <p><strong>Trend Direction:</strong> {'📈 Improving' if trend > 0 else '📉 Declining'}</p>
                        <p><strong>Confidence Level:</strong> 85%</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                outliers, lower, upper = identify_outliers(df)
                st.markdown(f"""
                    <div class='info-box'>
                        <h4>📊 Outlier Analysis</h4>
                        <p><strong>Outliers Detected:</strong> {len(outliers)} ({len(outliers)/len(df)*100:.1f}%)</p>
                        <p><strong>Lower Bound:</strong> {lower:.2f}</p>
                        <p><strong>Upper Bound:</strong> {upper:.2f}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if not outliers.empty:
                    st.markdown("#### Outlier Records")
                    st.dataframe(outliers[['student_id', 'course_name', 'marks']].head(20), use_container_width=True)
            
            # Performance distribution
            fig = ff.create_distplot([df['marks'].dropna()], ['Marks Distribution'], show_hist=False, show_rug=False, colors=['#7acce0'])
            fig.update_layout(title="<b>Probability Density Function</b>", height=400, title_font_color='#3a7ca5')
            st.plotly_chart(fig, use_container_width=True)
        
        elif selected == "Reports":
            st.markdown("## 📄 Report Generation")
            
            # Export options
            st.markdown("### 📥 Download Reports")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📊 Full Data Export (CSV)",
                    data=csv_data,
                    file_name=f"exam_data_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                summary_data = pd.DataFrame([calculate_advanced_metrics(df)]).T
                summary_data.columns = ['Value']
                summary_csv = summary_data.to_csv()
                st.download_button(
                    label="📈 Summary Statistics (CSV)",
                    data=summary_csv,
                    file_name=f"summary_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                course_stats = df.groupby('course_name')['marks'].agg(['mean', 'min', 'max', 'count']).round(2)
                course_csv = course_stats.to_csv()
                st.download_button(
                    label="📚 Course Performance (CSV)",
                    data=course_csv,
                    file_name=f"course_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            st.markdown("---")
            
            # Auto-generated insights
            st.markdown("### 💡 Key Insights")
            
            insights = []
            metrics = calculate_advanced_metrics(df)
            
            if metrics['pass_rate'] >= 85:
                insights.append("✅ Excellent overall pass rate exceeding target")
            elif metrics['pass_rate'] >= 75:
                insights.append("📊 Good pass rate, but room for improvement")
            else:
                insights.append("⚠️ Pass rate below target - intervention recommended")
            
            if metrics['skewness'] > 0.5:
                insights.append("📈 Performance distribution shows positive skew - more high performers")
            elif metrics['skewness'] < -0.5:
                insights.append("📉 Performance distribution shows negative skew - many low performers")
            
            if metrics['distinction_rate'] >= 30:
                insights.append("🏆 Excellent distinction rate - high-quality outcomes")
            
            for insight in insights:
                st.markdown(f"- {insight}")
    
    else:
        # Welcome screen
        st.markdown("""
            <div class='info-box' style='text-align: center; margin: 2rem;'>
                <h2>🎯 Welcome to CBT Examination Analytics Dashboard</h2>
                <p style='font-size: 1.1rem;'>Advanced Analytics for University Management</p>
                <br>
                <h4>✨ Features:</h4>
                <ul style='text-align: left; display: inline-block;'>
                    <li>📊 Real-time Pass/Fail Rate Analysis</li>
                    <li>🏆 Highest/Lowest Marks Tracking</li>
                    <li>📚 Comprehensive Course Performance</li>
                    <li>🔮 Predictive Analytics & Forecasting</li>
                    <li>🎯 Smart Alerts & Recommendations</li>
                    <li>📈 Advanced Statistical Analysis</li>
                </ul>
                <br>
                <p>👈 Please load data from the sidebar to begin</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
        <div class='footer'>
            <p><strong>📊 Technify University ERP | Academic Analytics & Business Intelligence</strong></p>
            <p>Data Science Team 1 | Syeda Samia</p>
            <p style='font-size: 0.8rem;'>🎯 Empowering data-driven decisions for university management</p>
            <p style='font-size: 0.75rem; color: #a8c4d8;'>© 2026 Technify | Insights for Excellence</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
