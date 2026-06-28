import streamlit as st
import pandas as pd
import sqlite3
import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="CoreHR | Persistent Quantum Suite",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Database Engineering & Initialization (SQLite3 Persistence)
def get_db_connection():
    conn = sqlite3.connect('corehr_database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Table 1: Configuration / Budget
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value REAL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO config (key, value) VALUES ('corporate_budget', 50000.0)")
    
    # Table 2: Employee Records
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id TEXT PRIMARY KEY,
            name TEXT,
            dept TEXT,
            base_salary REAL,
            bonus REAL,
            deductions REAL,
            performance TEXT,
            status TEXT
        )
    ''')
    
    # Insert Mock Data if table is empty
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        mock_data = [
            ('HR-001', 'John Doe', 'Kitchen', 4500.0, 200.0, 100.0, 'Excellent', 'Active'),
            ('HR-002', 'Jane Smith', 'Front Desk', 3800.0, 150.0, 0.0, 'Good', 'Active'),
            ('HR-003', 'Carlos Ramos', 'Kitchen', 4100.0, 0.0, 250.0, 'Needs Improvement', 'Active'),
            ('HR-004', 'Aisha Khan', 'Management', 6000.0, 500.0, 0.0, 'Excellent', 'Active')
        ]
        cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?)", mock_data)
        
    # Table 3: Attendance Logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            employee_name TEXT,
            status TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Run database setup
init_db()

# 3. Premium Cyber Dark Theme (100% English)
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] p { color: #e2e8f0 !important; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #070a13 0%, #0f172a 100%) !important; border-right: 1px solid #1e293b; }
    [data-testid="stSidebar"] * { color: #94a3b8 !important; }
    .neon-card {
        background: #111827; padding: 20px; border-radius: 14px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        border: 1px solid #1e293b; border-left: 6px solid #6366f1; margin-bottom: 10px;
    }
    .card-label { color: #94a3b8; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }
    .card-num { color: #ffffff; font-size: 1.8rem; font-weight: 700; margin-top: 4px; }
    input, select, textarea, div[data-baseweb="select"] { background-color: #1f2937 !important; color: #ffffff !important; border: 1px solid #374151 !important; }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important; color: white !important;
        border-radius: 8px !important; padding: 8px 20px !important; font-weight: bold !important; border: none !important;
    }
    div.stButton > button:has(div:contains("Terminate")) {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4) !important;
    }
    [data-testid="stDataFrame"] { background: #111827 !important; border: 1px solid #1e293b !important; }
</style>
""", unsafe_allow_html=True)

# 4. Session Authentication Protocol
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<h2 style='text-align: center; margin-top: 140px;'>🔒 CoreHR Quantum Portal</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("Secure Login"):
            user = st.text_input("Corporate User ID")
            pas = st.text_input("Access Token", type="password")
            if st.form_submit_button("Authenticate"):
                if user == "admin" and pas == "texas2026":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else: st.error("Access Denied.")
    st.stop()

# 5. Load Real Data from SQLite3 Database for Live Display
conn = get_db_connection()
budget_res = conn.execute("SELECT value FROM config WHERE key='corporate_budget'").fetchone()
corporate_budget = budget_res['value'] if budget_res else 50000.0

emp_cursor = conn.execute("SELECT * FROM employees")
df = pd.DataFrame([dict(row) for row in emp_cursor.fetchall()])
conn.close()

# Calculations based on persistent data
if not df.empty:
    df['Net Salary ($)'] = df['base_salary'] + df['bonus'] - df['deductions']
    total_payroll = df[df['status'] == 'Active']['Net Salary ($)'].sum()
else:
    total_payroll = 0.0
remaining_budget = corporate_budget - total_payroll

# Rename columns for premium UI presentation
df_display = df.rename(columns={
    'id': 'ID', 'name': 'Full Name', 'dept': 'Department', 
    'base_salary': 'Base Salary ($)', 'bonus': 'Bonus ($)', 
    'deductions': 'Deductions ($)', 'performance': 'Performance Score', 'status': 'Status'
})

# ----------------- SIDEBAR: PERSISTENT ATTENDANCE -----------------
st.sidebar.markdown("## 📅 Attendance Log Control")
with st.sidebar.form("Attendance Form"):
    log_date = st.date_input("Select Date", datetime.date.today())
    active_names = df[df['status'] == 'Active']['name'].tolist() if not df.empty else []
    log_emp = st.selectbox("Select Employee", active_names if active_names else ["None"])
    log_status = st.radio("Attendance Status", ["Present", "Absent (Unexcused)"])
    
    if st.form_submit_button("Log Attendance Stat"):
        conn = get_db_connection()
        conn.execute("INSERT INTO attendance (date, employee_name, status) VALUES (?, ?, ?)", (str(log_date), log_emp, log_status))
        if log_status == "Absent (Unexcused)":
            conn.execute("UPDATE employees SET deductions = deductions + 50.0 WHERE name = ?", (log_emp,))
        conn.commit()
        conn.close()
        st.sidebar.success(f"Saved into SQLite for {log_emp}")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("## 📊 Navigation Hub")
menu = st.sidebar.radio("Switch Framework View", ["💎 Financials & Core Ledger", "🔥 Performance & Exit Hub"])

# ----------------- VIEW 1: FINANCIALS & CORE LEDGER -----------------
if menu == "💎 Financials & Core Ledger":
    st.markdown("<h1>Corporate Financials & Ledger Suite</h1>", unsafe_allow_html=True)
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1: st.markdown(f'<div class="neon-card"><div class="card-label">Total Budget</div><div class="card-num">${corporate_budget:,.2f}</div></div>', unsafe_allow_html=True)
    with kpi2: st.markdown(f'<div class="neon-card" style="border-left-color: #ef4444;"><div class="card-label">Total Payroll</div><div class="card-num">${total_payroll:,.2f}</div></div>', unsafe_allow_html=True)
    with kpi3:
        b_color = "#10b981" if remaining_budget >= 0 else "#ef4444"
        st.markdown(f'<div class="neon-card" style="border-left-color: {b_color};"><div class="card-label">Remaining Budget</div><div class="card-num">${remaining_budget:,.2f}</div></div>', unsafe_allow_html=True)
    with kpi4: st.markdown(f'<div class="neon-card" style="border-left-color: #f59e0b;"><div class="card-label">Active Headcount</div><div class="card-num">{len(df[df["status"]=="Active"]) if not df.empty else 0}</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1.8, 1.2])
    
    with col_left:
        st.markdown("### 👥 Operational Employee Ledger")
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Attendance Audit Trail View
        st.markdown("<br>### 📊 Historical Attendance Database Records (SQLite3)", unsafe_allow_html=True)
        conn = get_db_connection()
        att_df = pd.read_sql_query("SELECT date, employee_name, status FROM attendance ORDER BY id DESC", conn)
        conn.close()
        if att_df.empty: st.info("No logs saved in SQLite3 file yet.")
        else: st.dataframe(att_df, use_container_width=True, hide_index=True)

    with col_right:
        st.markdown("### 💰 Capital Allocation & Adjustments")
        with st.form("Budget Form"):
            st.write("#### Update Global Capital Cap")
            new_cap = st.number_input("Set Company Budget Allocation ($)", min_value=0.0, value=corporate_budget, step=1000.0)
            if st.form_submit_button("Modify Capital Ceilings"):
                conn = get_db_connection()
                conn.execute("UPDATE config SET value = ? WHERE key = 'corporate_budget'", (new_cap,))
                conn.commit()
                conn.close()
                st.success("Budget locked in SQL!")
                st.rerun()
                
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("Manual Adjustments Form"):
            st.write("#### Manual Compensations & Deductions")
            target_emp = st.selectbox("Select Target Account", df[df['status']=='Active']['name'].tolist() if not df.empty else ["None"])
            action_type = st.radio("Financial Action Vector", ["Apply Manual Bonus", "Inject Penalties / Deduction"])
            amount = st.number_input("Transaction Value ($)", min_value=0.0, step=50.0, value=100.0)
            
            if st.form_submit_button("Authorize Financial Ledger Entry"):
                conn = get_db_connection()
                if action_type == "Apply Manual Bonus":
                    conn.execute("UPDATE employees SET bonus = bonus + ? WHERE name = ?", (amount, target_emp))
                else:
                    conn.execute("UPDATE employees SET deductions = deductions + ? WHERE name = ?", (amount, target_emp))
                conn.commit()
                conn.close()
                st.success("Ledger entry committed!")
                st.rerun()

# ----------------- VIEW 2: PERFORMANCE & EXIT HUB -----------------
elif menu == "🔥 Performance & Exit Hub":
    st.markdown("<h1>Performance Audits & Exit Operations</h1>", unsafe_allow_html=True)
    col_perf, col_fire = st.columns([1.5, 1.5])
    
    with col_perf:
        st.markdown("### 📈 Quality & Performance Evaluations")
        active_names = df[df['status'] == 'Active']['name'].tolist() if not df.empty else []
        if not active_names: st.info("No active profiles.")
        else:
            with st.form("Evaluation Form"):
                eval_emp = st.selectbox("Select Employee to Audit", active_names)
                score = st.selectbox("Overall Rating Assessment", ["Excellent (Top Performer)", "Good (Consistent Status)", "Satisfactory", "Needs Improvement (Critical Warning)"])
                if st.form_submit_button("Commit Performance Audit"):
                    conn = get_db_connection()
                    conn.execute("UPDATE employees SET performance = ? WHERE name = ?", (score, eval_emp))
                    conn.commit()
                    conn.close()
                    st.success("Performance matrix saved!")
                    st.rerun()

    with col_fire:
        st.markdown("### 🚨 Emergency Termination Engine (Fire System)")
        if not active_names: st.info("Workforce ledger cleared.")
        else:
            with st.form("Termination Node Form"):
                fire_emp = st.selectbox("Target Profile for Discharge", active_names)
                tenure_months = st.number_input("Operational Tenure (Total Months)", min_value=1, value=12)
                base_sal = df[df['name'] == fire_emp]['base_salary'].values[0]
                severance_package = (base_sal / 2) * (tenure_months / 12)
                
                st.markdown(f"<p style='color: #ef4444; font-weight: bold;'>Computed Corporate Severance: ${severance_package:,.2f}</p>", unsafe_allow_html=True)
                
                if st.form_submit_button("🚨 Terminate Employee & Revoke System Access"):
                    conn = get_db_connection()
                    conn.execute("UPDATE employees SET status = 'Terminated', base_salary = ?, bonus = 0.0, deductions = 0.0 WHERE name = ?", (severance_package, fire_emp))
                    conn.commit()
                    conn.close()
                    st.error("Access revoked. Final data archived.")
                    st.rerun()

# 6. Session Exit
st.sidebar.markdown("---")
if st.sidebar.button("🔒 Terminate Core Session"):
    st.session_state['authenticated'] = False
    st.rerun()
