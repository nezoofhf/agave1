import streamlit as st
import pandas as pd
import sqlite3
import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="CoreHR | Multi-Branch Quantum Suite",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Database Engineering & Initialization (Multi-Branch Database Support)
def get_db_connection():
    conn = sqlite3.connect('corehr_database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Table 1: Branches and Budgets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS branches (
            branch_name TEXT PRIMARY KEY,
            budget REAL
        )
    ''')
    
    # Default initial branch for Fajita Express
    cursor.execute("INSERT OR IGNORE INTO branches (branch_name, budget) VALUES ('San Antonio Downtown', 60000.0)")
    cursor.execute("INSERT OR IGNORE INTO branches (branch_name, budget) VALUES ('Northside Express', 40000.0)")
    
    # Table 2: Employee Records with Branch Association
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id TEXT PRIMARY KEY,
            name TEXT,
            dept TEXT,
            base_salary REAL,
            bonus REAL,
            deductions REAL,
            performance TEXT,
            status TEXT,
            branch_name TEXT,
            FOREIGN KEY (branch_name) REFERENCES branches (branch_name)
        )
    ''')
    
    # Insert Mock Data linked to branches if empty
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        mock_data = [
            ('HR-001', 'John Doe', 'Kitchen', 4500.0, 200.0, 100.0, 'Excellent', 'Active', 'San Antonio Downtown'),
            ('HR-002', 'Jane Smith', 'Front Desk', 3800.0, 150.0, 0.0, 'Good', 'Active', 'San Antonio Downtown'),
            ('HR-003', 'Carlos Ramos', 'Kitchen', 4100.0, 0.0, 250.0, 'Needs Improvement', 'Active', 'Northside Express'),
            ('HR-004', 'Aisha Khan', 'Management', 6000.0, 500.0, 0.0, 'Excellent', 'Active', 'Northside Express')
        ]
        cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", mock_data)
        
    # Table 3: Attendance Logs with Branch Tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            employee_name TEXT,
            status TEXT,
            branch_name TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Run database setup
init_db()

# 3. Premium Cyber Dark Theme Customization
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
    st.markdown("<h2 style='text-align: center; margin-top: 140px;'>🔒 Fajita Express Enterprise Hub</h2>", unsafe_allow_html=True)
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

# Load Branches List for Global Filters
conn = get_db_connection()
branch_rows = conn.execute("SELECT * FROM branches").fetchall()
branches_list = [row['branch_name'] for row in branch_rows]
conn.close()

# ----------------- SIDEBAR: MULTI-BRANCH CONTROLS -----------------
st.sidebar.markdown("## 🏢 Branch Network Management")

# Feature A: Add New Branch with Dedicated Budget
with st.sidebar.form("Add Branch Form"):
    st.write("### Create New Branch")
    new_b_name = st.text_input("Branch Location / Name")
    new_b_budget = st.number_input("Initial Branch Budget ($)", min_value=0.0, value=30000.0, step=5000.0)
    if st.form_submit_button("Deploy New Branch"):
        if new_b_name:
            conn = get_db_connection()
            try:
                conn.execute("INSERT INTO branches (branch_name, budget) VALUES (?, ?)", (new_b_name, new_b_budget))
                conn.commit()
                st.sidebar.success(f"Branch '{new_b_name}' deployed!")
            except sqlite3.IntegrityError:
                st.sidebar.error("Branch location already exists.")
            finally:
                conn.close()
            st.rerun()

st.sidebar.markdown("---")

# Feature B: Global Switcher (Select Branch or View All)
st.sidebar.markdown("## 🕹️ Global Scope Selection")
selected_scope = st.sidebar.selectbox("Active View Scope", ["All Locations"] + branches_list)

# ----------------- RE-LOAD EMPLOYEES & ATTENDANCE BASED ON FILTER -----------------
conn = get_db_connection()
if selected_scope == "All Locations":
    emp_cursor = conn.execute("SELECT * FROM employees")
    budget_res = conn.execute("SELECT SUM(value) as total FROM config WHERE key='corporate_budget'").fetchone() # dynamic legacy fallback
    branch_budget_sum = conn.execute("SELECT SUM(budget) as total FROM branches").fetchone()['total']
    active_budget = branch_budget_sum if branch_budget_sum else 100000.0
else:
    emp_cursor = conn.execute("SELECT * FROM employees WHERE branch_name = ?", (selected_scope,))
    b_budget_res = conn.execute("SELECT budget FROM branches WHERE branch_name = ?", (selected_scope,)).fetchone()
    active_budget = b_budget_res['budget'] if b_budget_res else 0.0

df = pd.DataFrame([dict(row) for row in emp_cursor.fetchall()])
conn.close()

# Calculations for the current visible scope
if not df.empty:
    df['Net Salary ($)'] = df['base_salary'] + df['bonus'] - df['deductions']
    total_payroll = df[df['status'] == 'Active']['Net Salary ($)'].sum()
else:
    total_payroll = 0.0
remaining_budget = active_budget - total_payroll

# ----------------- SIDEBAR: ATTENDANCE (CONTEXT-AWARE) -----------------
st.sidebar.markdown("---")
st.sidebar.markdown("## 📅 Shift Attendance Logger")
with st.sidebar.form("Attendance Form"):
    log_date = st.date_input("Select Shift Date", datetime.date.today())
    active_names = df[df['status'] == 'Active']['name'].tolist() if not df.empty else []
    log_emp = st.selectbox("Select Employee", active_names if active_names else ["No Active Staff in Scope"])
    log_status = st.radio("Status", ["Present", "Absent (Unexcused)"])
    
    if st.form_submit_button("Log Attendance Stat"):
        if active_names and log_emp != "No Active Staff in Scope":
            conn = get_db_connection()
            # Fetch employee branch to lock it accurately
            emp_b = conn.execute("SELECT branch_name FROM employees WHERE name = ?", (log_emp,)).fetchone()['branch_name']
            conn.execute("INSERT INTO attendance (date, employee_name, status, branch_name) VALUES (?, ?, ?, ?)", (str(log_date), log_emp, log_status, emp_b))
            if log_status == "Absent (Unexcused)":
                conn.execute("UPDATE employees SET deductions = deductions + 50.0 WHERE name = ?", (log_emp,))
            conn.commit()
            conn.close()
            st.sidebar.success(f"Saved for {log_emp}")
            st.rerun()

st.sidebar.markdown("---")
menu = st.sidebar.radio("Switch Dashboard View", ["💎 Financials & Core Ledger", "🔥 Performance & Exit Hub"])

# ----------------- VIEW 1: FINANCIALS & CORE LEDGER -----------------
if menu == "💎 Financials & Core Ledger":
    st.markdown(f"<h1>Network Intelligence Hub: <span style='color:#6366f1;'>{selected_scope}</span></h1>", unsafe_allow_html=True)
    
    # KPIs Dynamic Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1: st.markdown(f'<div class="neon-card"><div class="card-label">Visible Budget Cap</div><div class="card-num">${active_budget:,.2f}</div></div>', unsafe_allow_html=True)
    with kpi2: st.markdown(f'<div class="neon-card" style="border-left-color: #ef4444;"><div class="card-label">Active Payroll Burden</div><div class="card-num">${total_payroll:,.2f}</div></div>', unsafe_allow_html=True)
    with kpi3:
        b_color = "#10b981" if remaining_budget >= 0 else "#ef4444"
        st.markdown(f'<div class="neon-card" style="border-left-color: {b_color};"><div class="card-label">Remaining Operational Runway</div><div class="card-num">${remaining_budget:,.2f}</div></div>', unsafe_allow_html=True)
    with kpi4: st.markdown(f'<div class="neon-card" style="border-left-color: #f59e0b;"><div class="card-label">Staff Headcount</div><div class="card-num">{len(df[df["status"]=="Active"]) if not df.empty else 0}</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1.8, 1.2])
    
    with col_left:
        st.markdown("### 👥 Branch Roster Ledger")
        if df.empty:
            st.info("No employee accounts registered under this scope.")
        else:
            df_display = df.rename(columns={
                'id': 'ID', 'name': 'Full Name', 'dept': 'Department', 
                'base_salary': 'Base Salary ($)', 'bonus': 'Bonus ($)', 
                'deductions': 'Deductions ($)', 'performance': 'Performance Score', 'status': 'Status', 'branch_name': 'Assigned Branch'
            })
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Branch-Aware Attendance Records
        st.markdown("<br>### 📊 Attendance History Logs", unsafe_allow_html=True)
        conn = get_db_connection()
        if selected_scope == "All Locations":
            att_df = pd.read_sql_query("SELECT date, employee_name, status, branch_name FROM attendance ORDER BY id DESC", conn)
        else:
            att_df = pd.read_sql_query("SELECT date, employee_name, status, branch_name FROM attendance WHERE branch_name = ? ORDER BY id DESC", (selected_scope,), conn)
        conn.close()
        if att_df.empty: st.info("No attendance records logged under this parameters.")
        else: st.dataframe(att_df, use_container_width=True, hide_index=True)

    with col_right:
        st.markdown("### ⚙️ Scope Adjustments")
        
        # Form to alter budget of the selected branch (Disabled for "All Locations")
        if selected_scope != "All Locations":
            with st.form("Branch Budget Form"):
                st.write(f"#### Edit Budget Allocation for {selected_scope}")
                new_b_cap = st.number_input("Set Branch Capital Cap ($)", min_value=0.0, value=active_budget, step=1000.0)
                if st.form_submit_button("Lock New Capital Ceiling"):
                    conn = get_db_connection()
                    conn.execute("UPDATE branches SET budget = ? WHERE branch_name = ?", (new_b_cap, selected_scope))
                    conn.commit()
                    conn.close()
                    st.success("Branch configuration updated locally.")
                    st.rerun()
        else:
            st.warning("⚠️ Select a specific branch from the sidebar to modify budget allocation ceilings.")
                
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Form to add worker directly into a specific branch
        with st.form("Add Employee Form"):
            st.write("#### Add New Staff Member")
            new_id = st.text_input("Employee ID (e.g., HR-105)")
            new_name = st.text_input("Full Name")
            new_dept = st.selectbox("Department", ["Kitchen", "Front Desk", "Management", "Delivery"])
            new_salary = st.number_input("Base Monthly Salary ($)", min_value=0.0, value=30000.0, step=500.0)
            target_branch = st.selectbox("Assign to Branch", branches_list)
            
            if st.form_submit_button("Register Staff Account"):
                if new_id and new_name:
                    conn = get_db_connection()
                    try:
                        conn.execute("INSERT INTO employees VALUES (?, ?, ?, ?, 0.0, 0.0, 'Satisfactory', 'Active', ?)", 
                                     (new_id, new_name, new_dept, new_salary, target_branch))
                        conn.commit()
                        st.success(f"{new_name} added to {target_branch}!")
                    except sqlite3.IntegrityError:
                        st.error("Employee ID conflict detected.")
                    finally:
                        conn.close()
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Financial adjustments form
        with st.form("Manual Adjustments Form"):
            st.write("#### Manual Compensations & Deductions")
            active_names_form = df[df['status']=='Active']['name'].tolist() if not df.empty else ["None"]
            target_emp = st.selectbox("Select Target Account", active_names_form)
            action_type = st.radio("Financial Action Vector", ["Apply Manual Bonus", "Inject Penalties / Deduction"])
            amount = st.number_input("Transaction Value ($)", min_value=0.0, step=50.0, value=100.0)
            
            if st.form_submit_button("Authorize Financial Ledger Entry"):
                if active_names_form and target_emp != "None":
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
    
    active_names_global = df[df['status'] == 'Active']['name'].tolist() if not df.empty else []
    
    with col_perf:
        st.markdown("### 📈 Performance Assessment Evaluations")
        if not active_names_global: st.info("No active profiles in current scope.")
        else:
            with st.form("Evaluation Form"):
                eval_emp = st.selectbox("Select Employee to Audit", active_names_global)
                score = st.selectbox("Overall Rating Assessment", ["Excellent (Top Performer)", "Good (Consistent Status)", "Satisfactory", "Needs Improvement (Critical Warning)"])
                if st.form_submit_button("Commit Performance Audit"):
                    conn = get_db_connection()
                    conn.execute("UPDATE employees SET performance = ? WHERE name = ?", (score, eval_emp))
                    conn.commit()
                    conn.close()
                    st.success("Performance metrics synced successfully.")
                    st.rerun()

    with col_fire:
        st.markdown("### 🚨 Emergency Termination Engine (Fire System)")
        if not active_names_global: st.info("Workforce ledger cleared of active parameters.")
        else:
            with st.form("Termination Node Form"):
                fire_emp = st.selectbox("Target Profile for Discharge", active_names_global)
                tenure_months = st.number_input("Operational Tenure (Total Months)", min_value=1, value=12)
                base_sal = df[df['name'] == fire_emp]['base_salary'].values[0]
                severance_package = (base_sal / 2) * (tenure_months / 12)
                
                st.markdown(f"<p style='color: #ef4444; font-weight: bold;'>Computed Corporate Severance: ${severance_package:,.2f}</p>", unsafe_allow_html=True)
                
                if st.form_submit_button("🚨 Terminate Employee & Revoke System Access"):
                    conn = get_db_connection()
                    conn.execute("UPDATE employees SET status = 'Terminated', base_salary = ?, bonus = 0.0, deductions = 0.0 WHERE name = ?", (severance_package, fire_emp))
                    conn.commit()
                    conn.close()
                    st.error("Profile disabled. Severance locked into SQLite database.")
                    st.rerun()

# 6. Session Exit
st.sidebar.markdown("---")
if st.sidebar.button("🔒 Terminate Core Session"):
    st.session_state['authenticated'] = False
    st.rerun()
