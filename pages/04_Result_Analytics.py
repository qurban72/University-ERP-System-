import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2

st.set_page_config(
    page_title="Result Analytics | Technify ERP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── LIGHT THEME & FONT REPLICATION (FROM PAGE 1 & 2) ──────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #f8fafc !important; /* Light background */
        color: #0f172a !important; /* Dark text */
    }
    .block-container {
        padding: 2rem 2.5rem 1rem 2.5rem !important;
        max-width: 100% !important;
    }

    /* Spacing optimization */
    .element-container { margin-bottom: 0 !important; padding-bottom: 0 !important; }
    .stPlotlyChart { margin-bottom: 0 !important; }
    div[data-testid="stVerticalBlock"] > div { gap: 0px !important; }
    div[data-testid="column"] { padding: 0 6px !important; }

    /* ── BANNER ── */
    .top-banner {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 32px 40px 28px 40px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
    .top-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #0891b2);
    }
    .banner-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: #4f46e5;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .banner-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.1;
        margin-bottom: 8px;
    }
    .banner-title span {
        background: linear-gradient(90deg, #4f46e5, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .banner-sub {
        font-size: 0.95rem;
        color: #475569;
        font-weight: 400;
        margin-bottom: 14px;
    }
    .banner-badge {
        display: inline-block;
        background: rgba(79, 70, 229, 0.08);
        border: 1px solid rgba(79, 70, 229, 0.2);
        color: #4f46e5;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 8px;
    }

    /* ── KPI CARDS ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 14px;
        margin-bottom: 20px;
    }
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 22px 14px 18px 14px;
        text-align: center;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card:hover {
        border-color: #cbd5e1;
        transform: translateY(-1px);
    }
    .kpi-icon { font-size: 1.3rem; margin-bottom: 8px; display:block; }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1;
        margin-bottom: 6px;
        display: block;
    }
    .kpi-label {
        font-size: 0.72rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        display: block;
    }

    /* ── FILTER BAR ── */
    .filter-wrap {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px 12px 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }
    .stSelectbox label {
        color: #475569 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        margin-bottom: 4px !important;
    }
    .stSelectbox > div > div {
        background-color: #f8fafc !important;
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
        border-radius: 8px !important;
    }

    /* ── CHART CARDS ── */
    .ch-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px 18px 12px 18px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }

    /* ── SECTION HEADER ── */
    .sec-hdr {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 1px solid #e2e8f0;
        letter-spacing: 0.03em;
    }

    /* ── FOOTER ── */
    .footer {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px 40px;
        margin-top: 24px;
        text-align: center;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }
    .footer-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #4f46e5;
        margin-bottom: 4px;
    }
    .footer-sub {
        font-size: 0.8rem;
        color: #64748b;
    }
    .footer-badge {
        display: inline-block;
        background: rgba(79, 70, 229, 0.05);
        border: 1px solid rgba(79, 70, 229, 0.15);
        color: #4f46e5;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        margin: 8px 4px 0 4px;
    }

    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── DB CONNECTION ────────────────────────────────────────────────
@st.cache_resource
def get_conn():
    return psycopg2.connect(
        host="aws-1-ap-southeast-1.pooler.supabase.com",
        port=5432, database="postgres",
        user="postgres.gxfixjysmdmyvycuyucs",
        password="databetatechnify", sslmode="require"
    )

@st.cache_data(ttl=300)
def load():
    c = get_conn()
    return (
        pd.read_sql("SELECT * FROM results", c),
        pd.read_sql("SELECT * FROM students", c),
        pd.read_sql("SELECT * FROM departments", c),
        pd.read_sql("SELECT * FROM programs", c),
        pd.read_sql("SELECT * FROM enrollments", c),
        pd.read_sql("SELECT * FROM exams", c),
    )

with st.spinner("⏳ Loading data from Supabase..."):
    results, students, departments, programs, enrollments, exams = load()

# ── MERGE & CLEAN (KeyError Fix Included) ─────────────────────────
df = results.merge(enrollments, on="enrollment_id", how="left")

# Duplicated semester column handle karne ke liye renaming logic
if 'semester' in df.columns:
    df = df.rename(columns={'semester': 'semester_enrollment'})

df = df.merge(students[['student_id','name','department_id','program_id','semester','cgpa','status']], on="student_id", how="left")
df = df.merge(departments, on="department_id", how="left")
df = df.merge(programs[['program_id','program_name','degree_level']], on="program_id", how="left")
df = df.merge(exams[['exam_id','exam_type','total_marks']], on="exam_id", how="left")

df['percentage'] = (df['marks_obtained'] / df['total_marks']) * 100
df['pass_fail']  = df['percentage'].apply(lambda x: 'Pass' if x >= 50 else 'Fail')

def assign_grade(pct):
    if pct >= 80: return 'A'
    elif pct >= 70: return 'B'
    elif pct >= 60: return 'C'
    elif pct >= 50: return 'D'
    else: return 'F'

if 'grade' not in df.columns:
    df['grade'] = df['percentage'].apply(assign_grade)

# ── BANNER ──────────────────────────────────────────────────────
st.markdown("""
<div class="top-banner">
    <div class="banner-label">🏛️ Technify University ERP &nbsp;·&nbsp; Data Science Team 1</div>
    <div class="banner-title">🎓 Result <span>Analytics</span> Dashboard</div>
    <div class="banner-sub">Academic performance insights — GPA · CGPA · Semester · Department</div>
    <div>
        <span class="banner-badge">📊 Module 4</span>
        <span class="banner-badge">🔴 Live Data</span>
        <span class="banner-badge">🐘 Supabase PostgreSQL</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FILTERS ─────────────────────────────────────────────────────
st.markdown('<div class="filter-wrap">', unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns(3)
with fc1:
    d_opts = ['All Departments'] + sorted(departments['department_name'].dropna().tolist())
    sel_d  = st.selectbox("🏛️ Filter by Department", d_opts)
with fc2:
    s_opts = ['All Semesters'] + [f"Semester {int(s)}" for s in sorted(df['semester'].dropna().unique().tolist())]
    sel_s  = st.selectbox("📅 Filter by Semester", s_opts)
with fc3:
    e_opts = ['All Exam Types'] + sorted(df['exam_type'].dropna().unique().tolist())
    sel_e  = st.selectbox("📝 Filter by Exam Type", e_opts)
st.markdown('</div>', unsafe_allow_html=True)

fdf = df.copy()
if sel_d != 'All Departments':
    fdf = fdf[fdf['department_name'] == sel_d]
if sel_s != 'All Semesters':
    fdf = fdf[fdf['semester'] == int(sel_s.split()[1])]
if sel_e != 'All Exam Types':
    fdf = fdf[fdf['exam_type'] == sel_e]

# ── KPIs ────────────────────────────────────────────────────────
total_stu   = fdf['student_id'].nunique()
avg_marks   = fdf['percentage'].mean() if not fdf.empty else 0
pass_rate   = (fdf['pass_fail'] == 'Pass').mean() * 100 if not fdf.empty else 0
fail_rate   = 100 - pass_rate
avg_cgpa    = students['cgpa'].mean()
top_scorers = fdf[fdf['percentage'] >= 80]['student_id'].nunique()

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <span class="kpi-icon">👨‍🎓</span>
    <span class="kpi-value">{total_stu:,}</span>
    <span class="kpi-label">Total Students</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">📈</span>
    <span class="kpi-value" style="color:#4f46e5;">{avg_cgpa:.2f}</span>
    <span class="kpi-label">Avg CGPA</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">📊</span>
    <span class="kpi-value">{avg_marks:.1f}%</span>
    <span class="kpi-label">Avg Score</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">✅</span>
    <span class="kpi-value" style="color:#16a34a;">{pass_rate:.1f}%</span>
    <span class="kpi-label">Pass Rate</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">❌</span>
    <span class="kpi-value" style="color:#dc2626;">{fail_rate:.1f}%</span>
    <span class="kpi-label">Fail Rate</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">🏆</span>
    <span class="kpi-value" style="color:#d97706;">{top_scorers:,}</span>
    <span class="kpi-label">Top Scorers ≥80%</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── LIGHT THEME CHART GLOBAL CONFIG ─────────────────────────────
BG  = 'rgba(0,0,0,0)'
GRD = dict(gridcolor='#e2e8f0', zerolinecolor='#e2e8f0') # Light grids
TXT = '#475569' # Clean slate text
LAY = dict(paper_bgcolor=BG, plot_bgcolor=BG,
           font=dict(color=TXT, family='Inter', size=12),
           margin=dict(l=10, r=20, t=10, b=10))

# ── ROW 1 ───────────────────────────────────────────────────────
c1, c2 = st.columns([3, 2])
with c1:
    st.markdown('<div class="ch-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">📊 Avg CGPA by Department</div>', unsafe_allow_html=True)
    dc = students.merge(departments, on="department_id", how="left") \
        .groupby('department_name')['cgpa'].mean().reset_index() \
        .sort_values('cgpa', ascending=True)
    dc.columns = ['Department','Avg CGPA']
    fig1 = px.bar(dc, x='Avg CGPA', y='Department', orientation='h',
                  color='Avg CGPA', color_continuous_scale='Blues',
                  text=dc['Avg CGPA'].round(2))
    fig1.update_traces(textposition='outside', textfont=dict(color='#0f172a', size=12))
    fig1.update_layout(**LAY, height=360, coloraxis_showscale=False,
                       xaxis=dict(range=[0,4.5], title='Avg CGPA', **GRD),
                       yaxis=dict(title='', **GRD))
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="ch-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">✅ Pass vs Fail Rate</div>', unsafe_allow_html=True)
    pass_count = (fdf['pass_fail'] == 'Pass').sum()
    fail_count = (fdf['pass_fail'] == 'Fail').sum()
    pf = pd.DataFrame({'Status': ['Pass', 'Fail'], 'Count': [pass_count, fail_count]})
    fig2 = go.Figure(go.Pie(
        labels=pf['Status'], values=pf['Count'], hole=0.55,
        marker=dict(colors=['#22c55e', '#ef4444'], line=dict(color='#ffffff', width=2)),
        textinfo='percent+label', textfont=dict(size=13, color='#ffffff'),
        sort=False, direction='clockwise'
    ))
    fig2.update_layout(**{k:v for k,v in LAY.items() if k != 'margin'},
                       height=360, margin=dict(l=20, r=20, t=30, b=40),
                       legend=dict(orientation='h', y=-0.1, font=dict(size=12)))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── ROW 2 ───────────────────────────────────────────────────────
c3, c4 = st.columns(2)
with c3:
    st.markdown('<div class="ch-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">📈 Semester-wise Avg Score</div>', unsafe_allow_html=True)
    sp = fdf.groupby('semester')['percentage'].mean().reset_index()
    sp.columns = ['Semester','Avg Score']
    sp = sp.sort_values('Semester')
    fig3 = px.line(sp, x='Semester', y='Avg Score', markers=True,
                   line_shape='spline', color_discrete_sequence=['#4f46e5'])
    fig3.update_traces(marker=dict(size=9, color='#4f46e5', line=dict(color='#ffffff', width=2)), line=dict(width=2.5))
    fig3.add_hline(y=50, line_dash="dash", line_color="#ef4444",
                   annotation_text="Pass Line 50%", annotation_font=dict(color="#ef4444", size=11))
    fig3.update_layout(**LAY, height=340,
                       xaxis=dict(title='Semester', dtick=1, **GRD),
                       yaxis=dict(title='Avg Score (%)', range=[0,105], **GRD))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="ch-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">🏛️ Department Pass Rate</div>', unsafe_allow_html=True)
    dp = fdf.groupby('department_name').apply(lambda x: (x['pass_fail']=='Pass').mean()*100).reset_index()
    dp.columns = ['Department','Pass Rate']
    dp = dp.sort_values('Pass Rate', ascending=False)
    fig4 = px.bar(dp, x='Department', y='Pass Rate', color='Pass Rate', color_continuous_scale='Greens', text=dp['Pass Rate'].round(1))
    fig4.update_traces(texttemplate='%{text}%', textposition='outside', textfont=dict(color='#0f172a', size=11))
    fig4.update_layout(**LAY, height=340, coloraxis_showscale=False,
                       xaxis=dict(tickangle=-25, title='Department', **GRD),
                       yaxis=dict(range=[0,115], title='Pass Rate (%)', **GRD))
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── ROW 3 ───────────────────────────────────────────────────────
c5, c6 = st.columns([1, 2])
with c5:
    st.markdown('<div class="ch-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">🅰️ Grade Distribution</div>', unsafe_allow_html=True)
    GRADE_COLORS = {'A':'#22c55e','B':'#3b82f6','C':'#eab308','D':'#f97316','F':'#ef4444'}
    all_grades   = ['A','B','C','D','F']
    gc = fdf['grade'].value_counts().reset_index()
    gc.columns = ['Grade','Count']
    gc = pd.DataFrame({'Grade': all_grades}).merge(gc, on='Grade', how='left').fillna(0)
    gc = gc[gc['Count'] > 0]
    fig5 = go.Figure(go.Pie(
        labels=gc['Grade'], values=gc['Count'], hole=0.5,
        marker=dict(colors=[GRADE_COLORS.get(g, '#3b82f6') for g in gc['Grade']], line=dict(color='#ffffff', width=2)),
        textinfo='percent+label', textfont=dict(size=12, color='#ffffff'),
        sort=False, direction='clockwise'
    ))
    fig5.update_layout(**{k:v for k,v in LAY.items() if k != 'margin'},
                       height=340, margin=dict(l=20, r=20, t=30, b=50),
                       legend=dict(orientation='h', y=-0.12, font=dict(size=12)))
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c6:
    st.markdown('<div class="ch-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">🏆 Top 10 Students by CGPA</div>', unsafe_allow_html=True)
    top10 = students.merge(departments, on="department_id", how="left") \
        .sort_values('cgpa', ascending=False).head(10).reset_index(drop=True)
    colors = ['#d97706','#94a3b8','#b45309','#6366f1','#6366f1', '#4f46e5','#4f46e5','#4338ca','#4338ca','#3730a3']
    fig6 = go.Figure(go.Bar(
        x=top10['cgpa'], y=top10['name'], orientation='h',
        marker=dict(color=colors, line=dict(color='#ffffff', width=1)),
        text=top10['cgpa'].round(2), textposition='outside',
        textfont=dict(color='#0f172a', size=12),
        hovertemplate='<b>%{y}</b><br>CGPA: %{x}<extra></extra>'
    ))
    fig6.update_layout(**LAY, height=340,
                       xaxis=dict(range=[0,4.8], title='CGPA', **GRD),
                       yaxis=dict(title='', **GRD))
    fig6.update_yaxis(autorange="reversed")
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── ROW 4 ───────────────────────────────────────────────────────
st.markdown('<div class="ch-card">', unsafe_allow_html=True)
st.markdown('<div class="sec-hdr">📉 CGPA Trend — Semester Progression by Department</div>', unsafe_allow_html=True)
ds = students.merge(departments, on="department_id", how="left") \
    .groupby(['department_name','semester'])['cgpa'].mean().reset_index()
ds.columns = ['Department','Semester','Avg CGPA']
fig7 = px.line(ds, x='Semester', y='Avg CGPA', color='Department', markers=True, line_shape='spline', color_discrete_sequence=px.colors.qualitative.Safe)
fig7.update_traces(marker=dict(size=7), line=dict(width=2))
fig7.update_layout(**LAY, height=400,
                   xaxis=dict(title='Semester', dtick=1, **GRD),
                   yaxis=dict(title='Avg CGPA', range=[0,4.5], **GRD),
                   legend=dict(orientation='h', y=-0.15, font=dict(size=12), title=dict(text='Department ')))
st.plotly_chart(fig7, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ──────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-title">🏛️ Technify University ERP</div>
    <div class="footer-sub">Data Science Team 1 &nbsp;·&nbsp; Module 4 — Result Analytics Dashboard &nbsp;·&nbsp; Powered by Supabase PostgreSQL</div>
    <div>
        <span class="footer-badge">📊 GPA Trends</span>
        <span class="footer-badge">📈 CGPA Trends</span>
        <span class="footer-badge">🎓 Semester Performance</span>
        <span class="footer-badge">🏛️ Department Performance</span>
    </div>
</div>
""", unsafe_allow_html=True)
