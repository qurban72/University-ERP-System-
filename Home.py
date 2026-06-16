import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Technify University ERP",
    page_icon="🏛️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .dashboard-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>🏛️ Technify University ERP System</h1>
        <h3>Academic Analytics & Business Intelligence Dashboard</h3>
    </div>
""", unsafe_allow_html=True)

# Key Metrics Row
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

# Dashboard Navigation
st.subheader("📊 Select a Dashboard to Explore")

# Row 1: First 3 dashboards
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

# Row 2: Next 3 dashboards
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

# Recent Updates / Notifications
st.subheader("📢 Recent Updates")

col1, col2 = st.columns(2)

with col1:
    with st.expander("📌 University News", expanded=True):
        st.info("✅ New semester registration is now open")
        st.info("📈 Finance report for Q4 2025 is available")
        st.info("📋 Attendance policy has been updated")
        st.info("📝 Examination schedule published")

with col2:
    with st.expander("⚡ Quick Actions", expanded=True):
        st.success("📊 View all dashboards from sidebar")
        st.success("🔍 Use filters for specific data")
        st.success("📥 Export reports as needed")
        st.success("🔄 Data updates automatically")

st.markdown("---")

# Footer
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🏛️ Technify University ERP System v1.0 | Academic Analytics & Business Intelligence</p>
        <p style="font-size: 0.8rem;">Last Updated: June 2026 | Data refreshed daily</p>
    </div>
""", unsafe_allow_html=True)
