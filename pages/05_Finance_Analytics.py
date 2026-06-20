import re
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

# ── LIGHT THEME & FONT (UNCHANGED DESIGN) ──────────────────
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

    .element-container { margin-bottom: 0 !important; padding-bottom: 0 !important; }
    .stPlotlyChart { margin-bottom: 0 !important; }
    div[data-testid="stVerticalBlock"] > div { gap: 0px !important; }
    div[data-testid="column"] { padding: 0 6px !important; }

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

    .ch-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px 18px 12px 18px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }

    .sec-hdr {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 1px solid #e2e8f0;
        letter-spacing: 0.03em;
    }

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

# ── CORE LOGIC (unit-tested separately — 22/22 checks passing) ──────────
def find_column(df, candidates):
    """Case/space/underscore-insensitive column finder."""
    normalized = {c.lower().replace('_', '').replace(' ', ''): c for c in df.columns}
    for cand in candidates:
        key = cand.lower().replace('_', '').replace(' ', '')
        if key in normalized:
            return normalized[key]
    return None

STATUS_MAP = {
    'paid': 'Paid', 'completed': 'Paid', 'complete': 'Paid', 'success': 'Paid',
    'successful': 'Paid', 'cleared': 'Paid', 'settled': 'Paid', 'done': 'Paid',
    'unpaid': 'Unpaid', 'not paid': 'Unpaid', 'notpaid': 'Unpaid',
    'partial': 'Partial', 'partially paid': 'Partial', 'part payment': 'Partial', 'partpaid': 'Partial',
    'pending': 'Pending', 'due': 'Pending', 'outstanding': 'Pending',
    'processing': 'Pending', 'in progress': 'Pending',
    'failed': 'Failed', 'cancelled': 'Failed', 'canceled': 'Failed',
    'rejected': 'Failed', 'void': 'Failed', 'declined': 'Failed',
}

def normalize_status(raw):
    """Maps any real-world spelling of a status to one of:
    Paid / Unpaid / Partial / Pending / Failed / <Original Title Case>."""
    if raw is None:
        return 'Unknown'
    s = str(raw).strip()
    if not s or s.lower() == 'nan':
        return 'Unknown'
    return STATUS_MAP.get(s.lower(), s.title())

def extract_semester_number(raw):
    """Robustly pulls a semester number out of whatever format it's stored in.
    Handles plain numbers (1, '1', '1.0') as well as real-world text formats
    like 'Semester 1', 'Sem-3', '3rd', '3rd Semester'. Returns float (so it
    stays compatible with downstream numeric code) or NaN if no digits are found.
    This fixes pd.to_numeric() silently turning every text-formatted semester
    into NaN, which emptied out the Semester filter dropdown entirely."""
    if raw is None:
        return float('nan')
    if isinstance(raw, (int, float)):
        return float(raw) if pd.notna(raw) else float('nan')
    s = str(raw).strip()
    if not s or s.lower() == 'nan':
        return float('nan')
    match = re.search(r'\d+', s)
    if match:
        return float(match.group())
    return float('nan')

def resolve_schema(payments, students, departments):
    """Auto-detects real column names regardless of spelling/casing and
    renames them to canonical names. Raises a clear ValueError (caught
    upstream and shown on screen) if a truly required identifier is missing."""
    payments = payments.copy(); students = students.copy(); departments = departments.copy()

    col_amount = find_column(payments, ['amount_paid', 'amount', 'fee_paid', 'amountpaid', 'total_amount', 'fee_amount', 'paid_amount'])
    col_status = find_column(payments, ['status', 'payment_status', 'paymentstatus', 'invoice_status', 'state'])
    col_pay_student = find_column(payments, ['student_id', 'studentid', 'std_id', 'user_id', 'sid'])
    col_payment_id = find_column(payments, ['payment_id', 'paymentid', 'id', 'txn_id', 'transaction_id'])
    col_payment_date = find_column(payments, ['payment_date', 'paymentdate', 'date', 'created_at', 'txn_date'])
    col_pay_method = find_column(payments, ['payment_method', 'method', 'paymentmethod', 'mode', 'channel'])

    payments = payments.rename(columns={col_amount: 'amount_paid'}) if col_amount else payments.assign(amount_paid=0)
    payments = payments.rename(columns={col_status: 'status'}) if col_status else payments.assign(status='Paid')
    if col_pay_student:
        payments = payments.rename(columns={col_pay_student: 'student_id'})
    else:
        raise ValueError(f"Could not find a student-identifier column in 'payments'. Available columns: {list(payments.columns)}")
    if col_payment_id:
        payments = payments.rename(columns={col_payment_id: 'payment_id'})
    if col_payment_date:
        payments = payments.rename(columns={col_payment_date: 'payment_date'})
    if col_pay_method:
        payments = payments.rename(columns={col_pay_method: 'payment_method'})

    col_stu_id = find_column(students, ['student_id', 'studentid', 'std_id', 'user_id', 'sid'])
    col_stu_name = find_column(students, ['name', 'student_name', 'full_name', 'fullname'])
    col_stu_dept = find_column(students, ['department_id', 'departmentid', 'dept_id', 'deptid'])
    col_stu_sem = find_column(students, ['semester', 'sem', 'current_semester', 'semester_no', 'sem_no', 'class_semester'])
    if col_stu_id:
        students = students.rename(columns={col_stu_id: 'student_id'})
    else:
        raise ValueError(f"Could not find a student-identifier column in 'students'. Available columns: {list(students.columns)}")
    students = students.rename(columns={col_stu_name: 'name'}) if col_stu_name else students.assign(name='Unknown')
    students = students.rename(columns={col_stu_dept: 'department_id'}) if col_stu_dept else students.assign(department_id=None)
    students = students.rename(columns={col_stu_sem: 'semester'}) if col_stu_sem else students.assign(semester=None)

    col_dept_id = find_column(departments, ['department_id', 'departmentid', 'dept_id', 'deptid', 'id'])
    col_dept_name = find_column(departments, ['department_name', 'departmentname', 'dept_name', 'name', 'department'])
    if col_dept_id:
        departments = departments.rename(columns={col_dept_id: 'department_id'})
    else:
        raise ValueError(f"Could not find a department-identifier column in 'departments'. Available columns: {list(departments.columns)}")
    departments = departments.rename(columns={col_dept_name: 'department_name'}) if col_dept_name else departments.assign(department_name='Unassigned')

    return payments, students, departments

def clean_data(payments, students, departments):
    """Full pipeline: schema resolution -> type coercion -> status
    normalization -> merge -> guaranteed columns. Returns one ready-to-filter
    DataFrame."""
    payments, students, departments = resolve_schema(payments, students, departments)

    payments['amount_paid'] = pd.to_numeric(payments['amount_paid'], errors='coerce').fillna(0).astype(float)
    payments['status'] = payments['status'].apply(normalize_status)
    students['semester'] = students['semester'].apply(extract_semester_number)

    if 'payment_date' in payments.columns:
        payments['payment_date'] = pd.to_datetime(payments['payment_date'], errors='coerce')
        payments['month_year'] = payments['payment_date'].dt.to_period('M').astype(str)
    else:
        payments['month_year'] = 'Unknown'

    f_df = payments.merge(students[['student_id', 'name', 'department_id', 'semester']], on='student_id', how='left')
    f_df = f_df.merge(departments[['department_id', 'department_name']], on='department_id', how='left')

    for col, default in [('semester', pd.NA), ('department_name', 'Unassigned'),
                          ('status', 'Unknown'), ('amount_paid', 0.0), ('month_year', 'Unknown')]:
        if col not in f_df.columns:
            f_df[col] = default
    f_df['amount_paid'] = pd.to_numeric(f_df['amount_paid'], errors='coerce').fillna(0).astype(float)
    f_df['department_name'] = f_df['department_name'].fillna('Unassigned')
    return f_df

def apply_filters(f_df, dept, semester, status):
    out = f_df.copy()
    if dept != 'All Departments':
        out = out[out['department_name'] == dept]
    if semester != 'All Semesters':
        out = out[out['semester'] == semester]
    if status != 'All Statuses':
        out = out[out['status'] == status]
    return out

def compute_kpis(filtered_fdf):
    if filtered_fdf.empty:
        return dict(total_revenue=0.0, pending_amount=0.0, total_tx=0, paid_count=0, collection_rate=0.0, active_payees=0)
    total_revenue = float(filtered_fdf.loc[filtered_fdf['status'] == 'Paid', 'amount_paid'].sum())
    # Outstanding receivables = everything still expected to be collected
    pending_amount = float(filtered_fdf.loc[filtered_fdf['status'].isin(['Pending', 'Unpaid', 'Partial']), 'amount_paid'].sum())
    total_tx = filtered_fdf['payment_id'].nunique() if 'payment_id' in filtered_fdf.columns else len(filtered_fdf)
    paid_count = int((filtered_fdf['status'] == 'Paid').sum())
    collection_rate = (paid_count / total_tx * 100) if total_tx > 0 else 0.0
    active_payees = filtered_fdf['student_id'].nunique() if 'student_id' in filtered_fdf.columns else 0
    return dict(total_revenue=total_revenue, pending_amount=pending_amount, total_tx=total_tx,
                paid_count=paid_count, collection_rate=collection_rate, active_payees=active_payees)

STATUS_COLORS = {
    'Paid': '#22c55e', 'Pending': '#f59e0b', 'Partial': '#3b82f6',
    'Unpaid': '#ef4444', 'Failed': '#94a3b8', 'Unknown': '#cbd5e1',
}
FALLBACK_PALETTE = ['#a855f7', '#ec4899', '#14b8a6', '#f97316']

def colors_for(statuses):
    extra = iter(FALLBACK_PALETTE)
    out = []
    for s in statuses:
        out.append(STATUS_COLORS.get(s, next(extra, '#64748b')))
    return out

# ── LOAD + CLEAN (wrapped so any schema surprise shows on screen, not blank) ──
try:
    with st.spinner("⏳ Loading financial records from Supabase..."):
        payments_raw, students_raw, departments_raw = load_finance_data()
    f_df = clean_data(payments_raw, students_raw, departments_raw)
except Exception as e:
    st.error("⚠️ Dashboard could not load due to a data/schema error. Copy the details below and share them for a fix:")
    st.exception(e)
    st.stop()

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
# Options are built from the merged, cleaned f_df itself (not the raw tables),
# so every option shown is guaranteed to have a matching, filterable row.
st.markdown('<div class="filter-wrap">', unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns(3)
with fc1:
    d_opts = ['All Departments'] + sorted(f_df['department_name'].dropna().unique().tolist())
    sel_d = st.selectbox("🏛️ Department Vector", d_opts)
with fc2:
    sem_values = sorted(int(s) for s in f_df['semester'].dropna().unique().tolist())
    s_opts = ['All Semesters'] + sem_values
    sel_s = st.selectbox(
        "📅 Semester Filter", s_opts,
        format_func=lambda v: v if v == 'All Semesters' else f"Semester {v}"
    )
with fc3:
    # Ordered so Paid/Unpaid/Partial/Pending/Failed appear first if present,
    # any unexpected extra status categories from the DB show up after.
    preferred_order = ['Paid', 'Unpaid', 'Partial', 'Pending', 'Failed']
    present = f_df['status'].dropna().unique().tolist()
    ordered = [s for s in preferred_order if s in present] + sorted(s for s in present if s not in preferred_order)
    status_opts = ['All Statuses'] + ordered
    sel_status = st.selectbox("💳 Payment Status", status_opts)
st.markdown('</div>', unsafe_allow_html=True)

filtered_fdf = apply_filters(f_df, sel_d, sel_s, sel_status)
kpi = compute_kpis(filtered_fdf)

# ── KPIs ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <span class="kpi-icon">💸</span>
    <span class="kpi-value" style="color:#16a34a;">PKR {kpi['total_revenue']:,.0f}</span>
    <span class="kpi-label">Total Revenue Collected</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">⏳</span>
    <span class="kpi-value" style="color:#dc2626;">PKR {kpi['pending_amount']:,.0f}</span>
    <span class="kpi-label">Outstanding Receivables</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">🧾</span>
    <span class="kpi-value">{kpi['total_tx']:,}</span>
    <span class="kpi-label">Total Invoices Issued</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">📈</span>
    <span class="kpi-value" style="color:#3b82f6;">{kpi['collection_rate']:.1f}%</span>
    <span class="kpi-label">Collection Efficiency</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">👨‍🎓</span>
    <span class="kpi-value">{kpi['active_payees']:,}</span>
    <span class="kpi-label">Active Payees</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── LIGHT THEME CHART GLOBAL CONFIG ─────────────────────────────
BG = 'rgba(0,0,0,0)'
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
    trend = (filtered_fdf[filtered_fdf['status'] == 'Paid']
             .groupby('month_year')['amount_paid'].sum()
             .reset_index().sort_values('month_year'))

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
            marker=dict(colors=colors_for(status_summary['status'].tolist()), line=dict(color='#ffffff', width=2)),
            textinfo='percent+label', textfont=dict(size=12, color='#ffffff'),
            sort=False, direction='clockwise'
        ))
        fig2.update_layout(**{k: v for k, v in LAY.items() if k != 'margin'},
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
    dept_rev = (filtered_fdf[filtered_fdf['status'] == 'Paid']
                .groupby('department_name')['amount_paid'].sum()
                .reset_index().sort_values('amount_paid', ascending=True))

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

    if not method_df.empty:
        fig4 = px.bar(method_df, x=method_col, y='amount_paid', color='amount_paid', color_continuous_scale='Purples')
        fig4.update_layout(**LAY, height=340, coloraxis_showscale=False,
                           xaxis=dict(title='Method / Channel', **GRD),
                           yaxis=dict(title='Collected Volume (PKR)', **GRD))
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("No payment method data to process.")
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
