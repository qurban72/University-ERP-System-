import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2

st.set_page_config(
    page_title="Finance Analytics | Technify ERP",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── LIGHT THEME & FONT REPLICATION (FROM PAGE 1 & 2) ──────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #f8fafc !important;
        color: #0f172a !important;
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
        background: linear-gradient(90deg, #0ea5e9, #3b82f6, #6366f1);
    }
    .banner-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: #3b82f6;
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
        background: linear-gradient(90deg, #3b82f6, #0ea5e9);
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
        background: rgba(59, 130, 246, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.2);
        color: #3b82f6;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 8px;
    }

    /* ── KPI CARDS ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
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
        font-size: 1.6rem;
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
        color: #3b82f6;
        margin-bottom: 4px;
    }
    .footer-sub {
        font-size: 0.8rem;
        color: #64748b;
    }
    .footer-badge {
        display: inline-block;
        background: rgba(59, 130, 246, 0.05);
        border: 1px solid rgba(59, 130, 246, 0.15);
        color: #3b82f6;
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
def load_finance_data():
    c = get_conn()
    return (
        pd.read_sql("SELECT * FROM payments", c),
        pd.read_sql("SELECT * FROM students", c),
        pd.read_sql("SELECT * FROM departments", c),
    )

with st.spinner("⏳ Loading financial records from Supabase..."):
    payments, students, departments = load_finance_data()

# ── DYNAMIC COLUMN MAPPING FIX (AMOUNT & STATUS) ──────────────────
# Amount column auto-mapping
if 'amount_paid' not in payments.columns:
    for col in ['amount', 'fee_paid', 'amountpaid', 'total_amount']:
        if col in payments.columns:
            payments = payments.rename(columns={col: 'amount_paid'})
            break

# Status column auto-mapping (Fixes KeyError 'status')
if 'status' not in payments.columns:
    for col in ['payment_status', 'paymentstatus', 'invoice_status', 'state']:
        if col in payments.columns:
            payments = payments.rename(columns={col: 'status'})
            break

# Fallback agar phir bhi column nahi milta
if 'status' not in payments.columns:
    payments['status'] = 'Paid'

# Payment Date parsing safely
if 'payment_date' in payments.columns:
    payments['payment_date'] = pd.to_datetime(payments['payment_date'])
    payments['month_year'] = payments['payment_date'].dt.to_period('M').astype(str)
else:
    payments['month_year'] = "2026-06"

# Tables join karna architecture ke mutabiq
f_df = payments.merge(students[['student_id', 'name', 'department_id', 'semester']], on="student_id", how="left")
f_df = f_df.merge(departments[['department_id', 'department_name']], on="department_id", how="left")

# Safe column access for fillna
if 'amount_paid' in f_df.columns:
    f_df['amount_paid'] = f_df['amount_paid'].fillna(0)
else:
    f_df['amount_paid'] = 0

# ── BANNER ──────────────────────────────────────────────────────
st.markdown("""
<div class="top-banner">
    <div class="banner-label">🏛️ Technify University ERP &nbsp;·&nbsp; Data Science Team 1</div>
    <div class="banner-title">💰 Finance <span>Analytics</span> Dashboard</div>
    <div class="banner-sub">Revenue Streams · Fee Status · Collection Trends · Departmental Inflow</div>
    <div>
        <span class="banner-badge">📊 Module 3</span>
        <span class="banner-badge">🔴 Live Sync</span>
        <span class="banner-badge">🐘 Supabase PostgreSQL</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FILTERS ─────────────────────────────────────────────────────
st.markdown('<div class="filter-wrap">', unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns(3)
with fc1:
    d_opts = ['All Departments'] + sorted(departments['department_name'].dropna().tolist())
    sel_d  = st.selectbox("🏛️ Department Vector", d_opts)
with fc2:
    s_opts = ['All Semesters'] + [f"Semester {int(s)}" for s in sorted(students['semester'].dropna().unique().tolist())]
    sel_s  = st.selectbox("📅 Semester Filter", s_opts)
with fc3:
    # Ab 'status' safely accessible hai bina custom crash ke
    status_opts = ['All Statuses'] + sorted(payments['status'].dropna().unique().tolist())
    sel_status  = st.selectbox("💳 Payment Status", status_opts)
st.markdown('</div>', unsafe_allow_html=True)

# Filtering logic apply karna
filtered_fdf = f_df.copy()
if sel_d != 'All Departments':
    filtered_fdf = filtered_fdf[filtered_fdf['department_name'] == sel_d]
if sel_s != 'All Semesters':
    filtered_fdf = filtered_fdf[filtered_fdf['semester'] == int(sel_s.split()[1])]
if sel_status != 'All Statuses':
    filtered_fdf = filtered_fdf[filtered_fdf['status'] == sel_status]

# ── KPIs ────────────────────────────────────────────────────────
total_revenue   = filtered_fdf[filtered_fdf['status'].str.lower() == 'paid']['amount_paid'].sum() if not filtered_fdf.empty else 0
pending_amount  = filtered_fdf[filtered_fdf['status'].str.lower() == 'pending']['amount_paid'].sum() if not filtered_fdf.empty else 0
total_tx        = filtered_fdf['payment_id'].nunique() if 'payment_id' in filtered_fdf.columns else len(filtered_fdf)
paid_count      = filtered_fdf[filtered_fdf['status'].str.lower() == 'paid'].shape[0]
collection_rate = (paid_count / total_tx * 100) if total_tx > 0 else 0

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <span class="kpi-icon">💸</span>
    <span class="kpi-value" style="color:#16a34a;">PKR {total_revenue:,.0f}</span>
    <span class="kpi-label">Total Revenue Collected</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">⏳</span>
    <span class="kpi-value" style="color:#dc2626;">PKR {pending_amount:,.0f}</span>
    <span class="kpi-label">Outstanding Receivables</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">🧾</span>
    <span class="kpi-value">{total_tx:,}</span>
    <span class="kpi-label">Total Invoices Issued</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">📈</span>
    <span class="kpi-value" style="color:#3b82f6;">{collection_rate:.1f}%</span>
    <span class="kpi-label">Collection Efficiency</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">👨‍🎓</span>
    <span class="kpi-value">{filtered_fdf['student_id'].nunique():,}</span>
    <span class="kpi-label">Active Payees</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── LIGHT THEME CHART GLOBAL CONFIG ─────────────────────────────
BG  = 'rgba(0,0,0,0)'
GRD = dict(gridcolor='#e2e8f0', zerolinecolor='#e2e8f0') 
TXT = '#475569' 
LAY = dict(paper_bgcolor=BG, plot_bgcolor=BG,
           font=dict(color=TXT, family='Inter', size=12),
           margin=dict(l=10, r=20, t=10, b=10))

# ── ROW 1: COLLECTION TRENDS & STATUS SPLIT ──────────────────────
c1, c2 = st.columns([3, 2])
with c1:
    st.markdown('<div class="ch-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">📈 Monthly Inflow & Revenue Collection Trend</div>', unsafe_allow_html=True)
    trend = filtered_fdf[filtered_fdf['status'].str.lower() == 'paid'].groupby('month_year')['amount_paid'].sum().reset_index().sort_values('month_year')
    
    if not trend.empty:
        fig1 = px.line(trend, x='month_year', y='amount_paid', markers=True, line_shape='spline', color_discrete_sequence=['#3b82f6'])
        fig1.update_traces(marker=dict(size=8, color='#3b82f6', line=dict(color='#ffffff', width=2)), line=dict(width=3))
        fig1.update_layout(**LAY, height=340,
                           xaxis=dict(title='Timeline (Months)', **GRD),
                           yaxis=dict(title='Volume (PKR)', **GRD))
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No matching paid trends found for current filter metrics.")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="ch-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">💳 Fee Settlement Status Summary</div>', unsafe_allow_html=True)
    status_summary = filtered_fdf.groupby('status').size().reset_index(name='count')
    
    if not status_summary.empty:
        fig2 = go.Figure(go.Pie(
            labels=status_summary['status'], values=status_summary['count'], hole=0.55,
            marker=dict(colors=['#22c55e', '#ef4444', '#f59e0b'], line=dict(color='#ffffff', width=2)),
            textinfo='percent+label', textfont=dict(size=12, color='#ffffff'),
            sort=False, direction='clockwise'
        ))
        fig2.update_layout(**{k:v for k,v in LAY.items() if k != 'margin'},
                           height=340, margin=dict(l=20, r=20, t=30, b=40),
                           legend=dict(orientation='h', y=-0.1, font=dict(size=12)))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No status matrices available.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── ROW 2: DEPARTMENTAL REVENUE & FEE METHOD TYPE ─────────────────
c3, c4 = st.columns(2)
with c3:
    st.markdown('<div class="ch-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">🏛️ Total Revenue Generation by Department</div>', unsafe_allow_html=True)
    dept_rev = filtered_fdf[filtered_fdf['status'].str.lower() == 'paid'].groupby('department_name')['amount_paid'].sum().reset_index().sort_values('amount_paid', ascending=True)
    
    if not dept_rev.empty:
        fig3 = px.bar(dept_rev, x='amount_paid', y='department_name', orientation='h',
                      color='amount_paid', color_continuous_scale='Blues')
        fig3.update_layout(**LAY, height=340, coloraxis_showscale=False,
                           xaxis=dict(title='Collected Revenue (PKR)', **GRD),
                           yaxis=dict(title='', **GRD))
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No departmental collections to process.")
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="ch-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">🔌 Preferred Payment Method Distribution</div>', unsafe_allow_html=True)
    
    method_col = 'payment_method' if 'payment_method' in filtered_fdf.columns else 'status'
    method_df = filtered_fdf.groupby(method_col)['amount_paid'].sum().reset_index().sort_values('amount_paid', ascending=False)
    
    fig4 = px.bar(method_df, x=method_col, y='amount_paid', color='amount_paid', color_continuous_scale='Purples')
    fig4.update_layout(**LAY, height=340, coloraxis_showscale=False,
                       xaxis=dict(title='Method / Channel', **GRD),
                       yaxis=dict(title='Collected Volume (PKR)', **GRD))
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ──────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-title">🏛️ Technify University ERP</div>
    <div class="footer-sub">Data Science Team 1 &nbsp;·&nbsp; Module 3 — Finance Analytics Dashboard &nbsp;·&nbsp; Powered by Supabase PostgreSQL</div>
    <div>
        <span class="footer-badge">💵 Revenue Streams</span>
        <span class="footer-badge">💳 Collection Matrix</span>
        <span class="footer-badge">🏛️ Departmental Auditing</span>
    </div>
</div>
""", unsafe_allow_html=True)
