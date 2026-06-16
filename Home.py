import streamlit as st
import base64
import os

# ============================================================================
# 1. PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Technify University ERP",
    page_icon="🎓",  
    layout="wide"
)

# ============================================================================
# 2. IMAGE PROCESSING (For 100% Guaranteed Logo Loading)
# ============================================================================
def get_base64_image(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 'logo.png' ko read karne ki koshish karein
logo_base64 = get_base64_image("logo.png")

if logo_base64:
    # Local Image Source
    logo_html_src = f"data:image/png;base64,{logo_base64}"
else:
    # Live URL Fallback (Backup agar file project folder mein na mile)
    logo_html_src = "https://technifyltd.com/wp-content/uploads/2024/03/technify-Logo-1.png"

# ============================================================================
# 3. CUSTOM CSS FOR THEME & LAYOUT
# ============================================================================
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .header-logo {
        max-width: 240px;
        height: auto;
        margin-bottom: 1.2rem;
        background: rgba(255, 255, 255, 0.15);
        padding: 12px 25px;
        border-radius: 8px;
        display: inline-block;
    }
    .dashboard-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# 4. BRANDED MAIN HEADER UI
# ============================================================================
st.markdown(f"""
    <div class="main-header">
        <img src="{logo_html_src}" class="header-logo">
        <h1 style="margin: 0; font-size: 2.3rem; font-weight: 700; letter-spacing: 0.5px;">Technify ERP System</h1>
        <h3 style="margin-top: 0.5rem; opacity: 0.85; font-weight: 400; font-size: 1.2rem;">Academic Analytics & Business Intelligence Dashboard</h3>
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# 5. KEY INSTUTIONAL METRICS
# ============================================================================
st.subheader("📊 University at a Glance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👨‍🎓 Total Students",
        value="12,847",
        delta="+5.2%",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="💰 Revenue Collected",
        value="$24.5M",
        delta="+8.1%",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="📋 Overall Attendance",
        value="87.3%",
        delta="-1.2%",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="🎯 Average GPA",
        value="3.42",
        delta="+0.05",
        delta_color="normal"
    )

st.markdown("---")

# ============================================================================
# 6. DASHBOARD NAVIGATION GATEWAY
# ============================================================================
st.subheader("📊 Select a Dashboard to Explore")

# Row 1: Student, Attendance, Examination
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="dashboard-card">
            <h3>👨‍🎓 Student Analytics</h3>
            <ul>
                <li>Total Students by Department</li>
                <li>Program Distribution</li>
                <li>Semester-wise Analysis</li>
                <li>Active/Inactive Students</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Open Student Dashboard", key="btn_student", use_container_width=True):
        st.switch_page("pages/01_Student_Analytics.py")

with col2:
    st.markdown("""
        <div class="dashboard-card">
            <h3>📋 Attendance Analytics</h3>
            <ul>
                <li>Overall Attendance Rate</li>
                <li>Department-wise Performance</li>
                <li>Course-wise Analysis</li>
                <li>Students Below 75%</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Open Attendance Dashboard", key="btn_attendance", use_container_width=True):
        st.switch_page("pages/02_Attendance_Analytics.py")

with col3:
    st.markdown("""
        <div class="dashboard-card">
            <h3>📝 Examination Analytics</h3>
            <ul>
                <li>Pass/Failure Rates</li>
                <li>Highest/Lowest Marks</li>
                <li>Course Performance</li>
                <li>Subject-wise Analysis</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Open Examination Dashboard", key="btn_exam", use_container_width=True):
        st.switch_page("pages/03_Examination_Analytics.py")

# Row 2: Result, Finance, Executive
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
        <div class="dashboard-card">
            <h3>📊 Result Analytics</h3>
            <ul>
                <li>GPA & CGPA Trends</li>
                <li>Semester Performance</li>
                <li>Department Performance</li>
                <li>Student Progress</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Open Result Dashboard", key="btn_result", use_container_width=True):
        st.switch_page("pages/04_Result_Analytics.py")

with col5:
    st.markdown("""
        <div class="dashboard-card">
            <h3>💰 Finance Analytics</h3>
            <ul>
                <li>Fee Collection Status</li>
                <li>Outstanding Fees</li>
                <li>Revenue Trends</li>
                <li>Payment Statistics</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Open Finance Dashboard", key="btn_finance", use_container_width=True):
        st.switch_page("pages/05_Finance_Analytics.py")

with col6:
    st.markdown("""
        <div class="dashboard-card">
            <h3>👔 Executive Dashboard</h3>
            <ul>
                <li>Key University KPIs</li>
                <li>Overall Performance</li>
                <li>Management Reports</li>
                <li>Strategic Insights</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Open Executive Dashboard", key="btn_executive", use_container_width=True):
        st.switch_page("pages/06_Executive_Dashboard.py")

st.markdown("---")

# ============================================================================
# 7. BULLETIN BOARD & ACTIONS
# ============================================================================
st.subheader("📢 Recent Updates")

col_news, col_actions = st.columns(2)

with col_news:
    with st.expander("📌 University News", expanded=True):
        st.info("✅ New semester registration is now open")
        st.info("📈 Finance report for Q4 2025 is available")
        st.info("📋 Attendance policy has been updated")
        st.info("📝 Examination schedule published")

with col_actions:
    with st.expander("⚡ Quick Actions", expanded=True):
        st.success("📊 View all dashboards from sidebar")
        st.success("🔍 Use filters for specific data")
        st.success("📥 Export reports as needed")
        st.success("🔄 Data updates automatically")

st.markdown("---")

# ============================================================================
# 8. FOOTER ARCHITECTURE
# ============================================================================
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p> Technify University ERP System v1.0 | Academic Analytics & Business Intelligence</p>
        <p style="font-size: 0.8rem;">Last Updated: June 2026 | Data refreshed daily</p>
    </div>
""", unsafe_allow_html=True)
