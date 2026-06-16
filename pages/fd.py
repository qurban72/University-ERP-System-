import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text, inspect
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="University EPR — Finance",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0f1117; color: #e8eaed; }
    [data-testid="stSidebar"] { background-color: #1a1d27; border-right: 1px solid #2e3244; }
    .metric-card {
        background: linear-gradient(135deg, #1e2235 0%, #252a3d 100%);
        border: 1px solid #2e3244; border-radius: 12px;
        padding: 20px 24px; margin-bottom: 12px;
        position: relative; overflow: hidden;
    }
    .metric-card::before {
        content: ''; position: absolute;
        top: 0; left: 0; width: 4px; height: 100%; border-radius: 4px 0 0 4px;
    }
    .metric-card.green::before  { background: #00c853; }
    .metric-card.blue::before   { background: #2979ff; }
    .metric-card.amber::before  { background: #ffab00; }
    .metric-card.red::before    { background: #ff1744; }
    .metric-label { font-size: 11px; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: #8892a4; margin-bottom: 6px; }
    .metric-value { font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 700; color: #ffffff; line-height: 1.1; }
    .metric-sub   { font-size: 12px; color: #6b7585; margin-top: 4px; }
    .section-title { font-size: 13px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: #4a90d9; padding-bottom: 8px; border-bottom: 1px solid #2e3244; margin-bottom: 16px; }
    .page-title    { font-family: 'Playfair Display', serif; font-size: 36px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px; }
    .page-subtitle { font-size: 13px; color: #6b7585; margin-top: 2px; }
    hr { border-color: #2e3244; }
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATABASE CONNECTION
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_engine():
    url = (
        "postgresql+psycopg2://"
        "postgres.gxfixjysmdmyvycuyucs:databetatechnify"
        "@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"
        "?sslmode=require"
    )
    return create_engine(url, pool_pre_ping=True)

@st.cache_data(ttl=120, show_spinner=False)
def get_columns(table: str):
    """Return real column names from the database for a given table."""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(
            f"SELECT column_name FROM information_schema.columns "
            f"WHERE table_name='{table}' ORDER BY ordinal_position"
        ))
        return [r[0] for r in result]

@st.cache_data(ttl=120, show_spinner=False)
def load_query(query: str) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)

def find_col(cols, keywords):
    """Find first column matching any keyword (case-insensitive)."""
    for kw in keywords:
        for c in cols:
            if kw.lower() in c.lower():
                return c
    return None

# ─────────────────────────────────────────────
# LOAD DATA WITH AUTO COLUMN DETECTION
# ─────────────────────────────────────────────
@st.cache_data(ttl=120, show_spinner=False)
def load_all():
    # --- payments ---
    pay_cols  = get_columns("payments")
    payments  = load_query("SELECT * FROM payments")

    # --- students: detect name column automatically ---
    stu_cols  = get_columns("students")
    stu_id    = find_col(stu_cols, ["student_id", "id"])
    stu_name  = find_col(stu_cols, ["name", "full_name", "student_name", "fname"])
    stu_prog  = find_col(stu_cols, ["program_id", "program"])
    stu_dept  = find_col(stu_cols, ["department_id", "department", "dept"])

    stu_select = [c for c in [stu_id, stu_name, stu_prog, stu_dept] if c]
    students   = load_query(f"SELECT {', '.join(stu_select)} FROM students")

    # Standardise column names for merging
    rename_stu = {}
    if stu_id   and stu_id   != "student_id":   rename_stu[stu_id]   = "student_id"
    if stu_name and stu_name != "student_name":  rename_stu[stu_name] = "student_name"
    if stu_prog and stu_prog != "program_id":    rename_stu[stu_prog] = "program_id"
    if stu_dept and stu_dept != "department_id": rename_stu[stu_dept] = "department_id"
    students.rename(columns=rename_stu, inplace=True)

    # --- programs ---
    prog_cols = get_columns("programs")
    prog_id   = find_col(prog_cols, ["program_id", "id"])
    prog_name = find_col(prog_cols, ["program_name", "name", "title"])
    prog_sel  = [c for c in [prog_id, prog_name] if c]
    programs  = load_query(f"SELECT {', '.join(prog_sel)} FROM programs")
    rename_prog = {}
    if prog_id   and prog_id   != "program_id":   rename_prog[prog_id]   = "program_id"
    if prog_name and prog_name != "program_name":  rename_prog[prog_name] = "program_name"
    programs.rename(columns=rename_prog, inplace=True)

    # --- departments ---
    dept_cols = get_columns("departments")
    dept_id   = find_col(dept_cols, ["department_id", "dept_id", "id"])
    dept_name = find_col(dept_cols, ["department_name", "dept_name", "name"])
    dept_sel  = [c for c in [dept_id, dept_name] if c]
    depts     = load_query(f"SELECT {', '.join(dept_sel)} FROM departments")
    rename_dept = {}
    if dept_id   and dept_id   != "department_id":   rename_dept[dept_id]   = "department_id"
    if dept_name and dept_name != "department_name":  rename_dept[dept_name] = "department_name"
    depts.rename(columns=rename_dept, inplace=True)

    return payments, students, programs, depts

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏛️ University EPR")
    st.markdown("**Finance Module**")
    st.markdown("---")
    st.markdown("#### Filters")

    with st.spinner("Connecting to database…"):
        try:
            payments, students, programs, depts = load_all()
            db_ok = True
        except Exception as e:
            db_ok = False
            st.error(f"DB Error: {e}")
            payments = students = programs = depts = pd.DataFrame()

    if db_ok and not payments.empty:
        df = payments.copy()
        if "student_id" in students.columns:
            df = df.merge(students, on="student_id", how="left")
        if "program_id" in programs.columns and "program_id" in df.columns:
            df = df.merge(programs, on="program_id", how="left")
        if "department_id" in depts.columns and "department_id" in df.columns:
            df = df.merge(depts, on="department_id", how="left")

        date_col   = find_col(df.columns.tolist(), ["date", "created_at", "paid_at", "payment_date"])
        amount_col = find_col(df.columns.tolist(), ["amount", "fee", "total", "paid_amount"])
        status_col = find_col(df.columns.tolist(), ["status", "payment_status", "state"])

        if date_col:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

        # Filters
        if status_col:
            opts = ["All"] + sorted(df[status_col].dropna().unique().tolist())
            selected_status = st.selectbox("Payment Status", opts)
        else:
            selected_status = "All"; status_col = None

        if "department_name" in df.columns:
            dopts = ["All"] + sorted(df["department_name"].dropna().unique().tolist())
            selected_dept = st.selectbox("Department", dopts)
        else:
            selected_dept = "All"

        if "program_name" in df.columns:
            popts = ["All"] + sorted(df["program_name"].dropna().unique().tolist())
            selected_prog = st.selectbox("Program", popts)
        else:
            selected_prog = "All"

        if date_col and df[date_col].notna().any():
            min_d = df[date_col].min().date()
            max_d = df[date_col].max().date()
            date_range = st.date_input("Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
        else:
            date_range = None

        st.markdown("---")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        st.markdown(f"<div style='font-size:11px;color:#555;margin-top:12px'>Last updated: {datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
    else:
        df = pd.DataFrame()
        date_col = amount_col = status_col = None
        date_range = None
        selected_status = selected_dept = selected_prog = "All"

# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
def apply_filters(df):
    fdf = df.copy()
    if selected_status != "All" and status_col and status_col in fdf.columns:
        fdf = fdf[fdf[status_col] == selected_status]
    if selected_dept != "All" and "department_name" in fdf.columns:
        fdf = fdf[fdf["department_name"] == selected_dept]
    if selected_prog != "All" and "program_name" in fdf.columns:
        fdf = fdf[fdf["program_name"] == selected_prog]
    if date_range and date_col and len(date_range) == 2:
        s, e = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        fdf = fdf[(fdf[date_col] >= s) & (fdf[date_col] <= e)]
    return fdf

# ─────────────────────────────────────────────
# CHART THEME
# ─────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#8892a4", size=12),
    margin=dict(l=16, r=16, t=32, b=16),
    xaxis=dict(gridcolor="#2e3244", zerolinecolor="#2e3244"),
    yaxis=dict(gridcolor="#2e3244", zerolinecolor="#2e3244"),
)
PALETTE = ["#2979ff", "#00c853", "#ffab00", "#ff1744", "#aa00ff", "#00bcd4"]

# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
st.markdown('<div class="page-title">Finance Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">University EPR System — Payment & Revenue Analytics</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if not db_ok or df.empty:
    st.warning("⚠️ No data loaded. Check your database connection.")
    st.stop()

fdf = apply_filters(df)

if fdf.empty:
    st.info("No records match the selected filters.")
    st.stop()

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">Key Metrics</div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

total_records  = len(fdf)
paid_mask      = fdf[status_col].str.lower() == "paid"   if status_col and status_col in fdf.columns else pd.Series([False]*len(fdf))
pending_mask   = fdf[status_col].str.lower() == "pending" if status_col and status_col in fdf.columns else pd.Series([False]*len(fdf))
overdue_mask   = fdf[status_col].str.lower() == "overdue" if status_col and status_col in fdf.columns else pd.Series([False]*len(fdf))

paid_count     = paid_mask.sum()
pending_count  = pending_mask.sum()
overdue_count  = overdue_mask.sum()

total_revenue  = fdf.loc[paid_mask, amount_col].sum()    if amount_col else 0
total_amount   = fdf[amount_col].sum()                   if amount_col else 0
pending_amount = fdf.loc[pending_mask, amount_col].sum() if amount_col else 0
collection_rate = (total_revenue / total_amount * 100)   if total_amount > 0 else 0

with k1:
    st.markdown(f"""<div class="metric-card green">
        <div class="metric-label">Total Revenue Collected</div>
        <div class="metric-value">PKR {total_revenue:,.0f}</div>
        <div class="metric-sub">{paid_count} paid transactions</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="metric-card blue">
        <div class="metric-label">Collection Rate</div>
        <div class="metric-value">{collection_rate:.1f}%</div>
        <div class="metric-sub">of PKR {total_amount:,.0f} total billed</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="metric-card amber">
        <div class="metric-label">Pending Payments</div>
        <div class="metric-value">PKR {pending_amount:,.0f}</div>
        <div class="metric-sub">{pending_count} transactions pending</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="metric-card red">
        <div class="metric-label">Overdue Accounts</div>
        <div class="metric-value">{overdue_count}</div>
        <div class="metric-sub">students with overdue payments</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHARTS ROW 1
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">Revenue Analysis</div>', unsafe_allow_html=True)
c1, c2 = st.columns([1.4, 1])

with c1:
    if date_col and amount_col and fdf[date_col].notna().any():
        monthly = fdf.groupby(fdf[date_col].dt.to_period("M"))[amount_col].sum().reset_index()
        monthly[date_col] = monthly[date_col].astype(str)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=monthly[date_col], y=monthly[amount_col], marker_color="#2979ff", marker_line_width=0))
        fig.update_layout(title="Monthly Revenue", **CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No date column detected for monthly chart.")

with c2:
    if status_col and amount_col and status_col in fdf.columns:
        sg = fdf.groupby(status_col)[amount_col].sum().reset_index()
        fig = px.pie(sg, values=amount_col, names=status_col, color_discrete_sequence=PALETTE, hole=0.55)
        fig.update_layout(title="Revenue by Status", **CHART_LAYOUT)
        fig.update_traces(textfont_color="#ffffff")
        st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
# CHARTS ROW 2
# ─────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    if "department_name" in fdf.columns and amount_col:
        dg = fdf.groupby("department_name")[amount_col].sum().reset_index().sort_values(amount_col, ascending=True)
        fig = go.Figure(go.Bar(x=dg[amount_col], y=dg["department_name"], orientation="h", marker_color="#00c853", marker_line_width=0))
        fig.update_layout(title="Revenue by Department", **CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

with c4:
    if "program_name" in fdf.columns and amount_col:
        pg = fdf.groupby("program_name")[amount_col].sum().reset_index().sort_values(amount_col, ascending=False).head(8)
        fig = px.bar(pg, x="program_name", y=amount_col, color_discrete_sequence=["#ffab00"])
        fig.update_layout(title="Top Programs by Revenue", xaxis_tickangle=-35, **CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
# STATUS BREAKDOWN
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Payment Status Breakdown</div>', unsafe_allow_html=True)

if status_col and status_col in fdf.columns:
    sc1, sc2, sc3 = st.columns(3)
    for col_w, status, color in zip([sc1, sc2, sc3], ["paid", "pending", "overdue"], ["green", "amber", "red"]):
        subset = fdf[fdf[status_col].str.lower() == status]
        amt = subset[amount_col].sum() if amount_col else 0
        cnt = len(subset)
        with col_w:
            st.markdown(f"""<div class="metric-card {color}">
                <div class="metric-label">{status.upper()}</div>
                <div class="metric-value">PKR {amt:,.0f}</div>
                <div class="metric-sub">{cnt} transactions</div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TRANSACTIONS TABLE
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Transaction Records</div>', unsafe_allow_html=True)

possible = ["payment_id","student_id","student_name","program_name","department_name",
            amount_col, status_col, date_col]
show_cols = [c for c in possible if c and c in fdf.columns]
display_df = fdf[show_cols].copy()

rename_map = {amount_col:"Amount (PKR)", status_col:"Status", date_col:"Date",
              "student_name":"Student Name","program_name":"Program",
              "department_name":"Department","payment_id":"Payment ID","student_id":"Student ID"}
display_df.rename(columns={k:v for k,v in rename_map.items() if k and k in display_df.columns}, inplace=True)

st.dataframe(display_df.reset_index(drop=True), use_container_width=True, height=400)

csv = display_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download as CSV", data=csv,
    file_name=f"finance_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")

st.markdown("---")
st.markdown("<div style='text-align:center;font-size:11px;color:#3a4055'>University EPR System — Finance Module &nbsp;|&nbsp; Supabase PostgreSQL</div>", unsafe_allow_html=True)
