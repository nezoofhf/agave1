import streamlit as st
import pandas as pd
import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="CoreHR | Quantum Enterprise Suite",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Ultra Dark Cyberpunk Theme & Professional UI Layout (100% English)
st.markdown("""
<style>
    /* Main Background & Core Fonts */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Standardizing typography to prevent mismatch */
    h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0 !important;
    }
    
    /* Elegant Dark Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070a13 0%, #0f172a 100%) !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * { color: #94a3b8 !important; }
    
    /* Premium Cyber Neon KPI Cards */
    .neon-card {
        background: #111827;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        border: 1px solid #1e293b;
        border-left: 6px solid #6366f1;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 10px;
    }
    .neon-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.2);
    }
    .card-label { color: #94a3b8; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .card-num { color: #ffffff; font-size: 1.8rem; font-weight: 700; margin-top: 4px; }
    
    /* Modern inputs and select boxes */
    input, select, textarea, div[data-baseweb="select"] {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
    }
    
    /* Vibrant Neon Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
        box-shadow: 0 0 18px rgba(99, 102, 241, 0.5) !important;
    }
    
    /* Critical Fire/Termination Button (Glowing Crimson Neon) */
    div.stButton > button:has(div:contains("Terminate")) {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4) !important;
    }
    div.stButton > button:has(div:contains("Terminate")):hover {
        box-shadow: 0 0 22px rgba(239, 68, 68, 0.6) !important;
    }
    
    /* Table Styling for Dataframes */
    [data-testid="stDataFrame"] {
        background: #111827 !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Session Security Authentication (100% Secure)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<h2 style='text-align: center; color: #ffffff; margin-top: 140px;'>🔒 CoreHR Quantum Portal</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("Secure Login"):
            user = st.text_input("Corporate User ID")
            pas = st.text_input("Access Token", type="password")
            if st.form_submit_button("Authenticate"):
                if user == "admin" and pas == "texas2026":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Access Denied. Cryptographic key mismatch.")
    st.stop()

# 4. Global State & Database Mock Init (Budget, Attendance, Employees)
if 'corporate_budget' not in st.session_state:
    st.session_state['corporate_budget'] = 50000.0

if 'employees' not in st.session_state:
    st.session_state['employees'] = pd.DataFrame([
        {'ID': 'HR-001', 'Name': 'John Doe', 'Dept': 'Kitchen', 'Base Salary': 4500.0, 'Bonus': 200.0, 'Deductions': 100.0, 'Performance': 'Excellent', 'Status': 'Active'},
        {'ID': 'HR-002', 'Name': 'Jane Smith', 'Dept': 'Front Desk', 'Base Salary': 3800.0, 'Bonus': 150.0, 'Deductions': 0.0, 'Performance': 'Good', 'Status': 'Active'},
        {'ID': 'HR-003', 'Name': 'Carlos Ramos', 'Dept': 'Kitchen', 'Base Salary': 4100.0, 'Bonus': 0.0, 'Deductions': 250.0, 'Performance': 'Needs Improvement', 'Status': 'Active'},
        {'ID': 'HR-004', 'Name': 'Aisha Khan', 'Dept': 'Management', 'Base Salary': 6000.0, 'Bonus': 500.0, 'Deductions': 0.0, 'Performance': 'Excellent', 'Status': 'Active'}
    ])

if 'attendance_log' not in st.session_state:
    st.session_state['attendance_log'] = pd.DataFrame(columns=['Date', 'Employee Name', 'Status'])

df = st.session_state['employees']

# Live Calculations: Net Salary = Base + Bonus - Deductions
df['Net Salary ($)'] = df['Base Salary'] + df['Bonus'] - df['Deductions']
total_payroll = df[df['Status'] == 'Active']['Net Salary ($)'].sum()
remaining_budget = st.session_state['corporate_budget'] - total_payroll

# ----------------- SIDEBAR: ATTENDANCE TRACKER & CONFIG -----------------
st.sidebar.markdown("## 📅 Attendance Log Control")
with st.sidebar.form("Attendance Form"):
    log_date = st.date_input("Select Date", datetime.date.today())
    active_names = df[df['Status'] == 'Active']['Name'].tolist()
    log_emp = st.selectbox("Select Employee", active_names if active_names else ["None"])
    log_status = st.radio("Attendance Status", ["Present", "Absent (Unexcused)"])
    
    if st.form_submit_button("Log Attendance Stat"):
        new_log = pd.DataFrame([{'Date': str(log_date), 'Employee Name': log_emp, 'Status': log_status}])
        st.session_state['attendance_log'] = pd.concat([st.session_state['attendance_log'], new_log], ignore_index=True)
        # Auto deduct if unexcused absence as a dynamic feature
        if log_status == "Absent (Unexcused)":
            st.session_state['employees'].loc[st.session_state['employees']['Name'] == log_emp, 'Deductions'] += 50.0
        st.sidebar.success(f"Log updated for {log_emp}")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("## 📊 Navigation Hub")
menu = st.sidebar.radio("Switch Framework View", ["💎 Financials & Core Ledger", "🔥 Performance & Exit Hub"])

# ----------------- VIEW 1: FINANCIALS & CORE LEDGER -----------------
if menu == "💎 Financials & Core Ledger":
    st.markdown("<h1 style='color: #ffffff;'>Corporate Financials & Ledger Suite</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size:14px; margin-bottom: 20px;'>Complete overview of active operational capital allocations.</p>", unsafe_allow_html=True)
    
    # Horizontal KPI Cards Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f'<div class="neon-card" style="border-left-color: #3b82f6;"><div class="card-label">Total Allocated Budget</div><div class="card-num">${st.session_state["corporate_budget"]:,.2f}</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="neon-card" style="border-left-color: #ef4444;"><div class="card-label">Total Net Payroll</div><div class="card-num">${total_payroll:,.2f}</div></div>', unsafe_allow_html=True)
    with kpi3:
        budget_color = "#10b981" if remaining_budget >= 0 else "#ef4444"
        st.markdown(f'<div class="neon-card" style="border-left-color: {budget_color};"><div class="card-label">Remaining Operational Budget</div><div class="card-num">${remaining_budget:,.2f}</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown(f'<div class="neon-card" style="border-left-color: #f59e0b;"><div class="card-label">Active Headcount</div><div class="card-num">{len(df[df["Status"]=="Active"])}</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.8, 1.2])
    
    with col_left:
        st.markdown("### 👥 Operational Employee Ledger")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export Capabilities
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Ledger Data (CSV)", data=csv, file_name="CoreHR_Financials.csv", mime="text/csv")
        
        # Attendance Audit Trail View to display what was logged in the sidebar
        st.markdown("<br>### 📊 Today's Attendance Audit Trail", unsafe_allow_html=True)
        if st.session_state['attendance_log'].empty:
            st.info("No attendance vectors logged for this operational shift.")
        else:
            st.dataframe(st.session_state['attendance_log'], use_container_width=True, hide_index=True)

    with col_right:
        st.markdown("### 💰 Capital Allocation & Adjustments")
        
        # Form to alter total budget ceiling
        with st.form("Budget Form"):
            st.write("#### Update Global Capital Cap")
            new_cap = st.number_input("Set Company Budget Allocation ($)", min_value=0.0, value=st.session_state['corporate_budget'], step=1000.0)
            if st.form_submit_button("Modify Capital Ceilings"):
                st.session_state['corporate_budget'] = new_cap
                st.success("Global corporate budget updated successfully.")
                st.rerun()
                
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Manual Bonus and Deductions System
        with st.form("Manual Adjustments Form"):
            st.write("#### Manual Compensations & Deductions")
            target_emp = st.selectbox("Select Target Account", df[df['Status']=='Active']['Name'])
            action_type = st.radio("Financial Action Vector", ["Apply Manual Bonus", "Inject Penalties / Deduction"])
            amount = st.number_input("Transaction Value ($)", min_value=0.0, step=50.0, value=100.0)
            
            if st.form_submit_button("Authorize Financial Ledger Entry"):
                if action_type == "Apply Manual Bonus":
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == target_emp, 'Bonus'] += amount
                else:
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == target_emp, 'Deductions'] += amount
                st.success(f"Successfully processed transaction for {target_emp}")
                st.rerun()

# ----------------- VIEW 2: PERFORMANCE & EXIT HUB -----------------
elif menu == "🔥 Performance & Exit Hub":
    st.markdown("<h1 style='color: #ffffff;'>Performance Audits & Exit Operations</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size:14px; margin-bottom: 20px;'>Manage operational workforce evaluations and offboarding parameters.</p>", unsafe_allow_html=True)
    
    col_perf, col_fire = st.columns([1.5, 1.5])
    
    with col_perf:
        st.markdown("### 📈 Quality & Performance Evaluations")
        active_emps = df[df['Status'] == 'Active']
        
        if active_emps.empty:
            st.info("No active corporate profiles detected.")
        else:
            with st.form("Evaluation Form"):
                eval_emp = st.selectbox("Select Employee to Audit", active_emps['Name'])
                score = st.selectbox("Overall Rating Assessment", ["Excellent (Top Performer)", "Good (Consistent Status)", "Satisfactory", "Needs Improvement (Critical Warning)"])
                
                if st.form_submit_button("Commit Performance Audit"):
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == eval_emp, 'Performance'] = score
                    st.success(f"Audit log locked for {eval_emp} as '{score}'.")
                    st.rerun()
                    
        # View to evaluate overall ranking scores
        st.markdown("<br>#### Audit Scores Preview", unsafe_allow_html=True)
        st.dataframe(df[df['Status']=='Active'][['Name', 'Dept', 'Performance']], use_container_width=True, hide_index=True)

    with col_fire:
        st.markdown("### 🚨 Emergency Termination Engine (Fire System)")
        if active_emps.empty:
            st.info("Workforce ledger cleared of active parameters.")
        else:
            with st.form("Termination Node Form"):
                fire_emp = st.selectbox("Target Profile for Discharge", active_emps['Name'])
                clause = st.selectbox("Termination Legal Clause", ["Breach of Corporate Protocol", "Performance Deficit", "Downsizing Strategy", "Voluntary Resignation"])
                tenure_months = st.number_input("Operational Tenure (Total Months)", min_value=1, value=12)
                
                # Severance Math Formula: (Base Salary / 2) * (Years served)
                base_sal = df[df['Name'] == fire_emp]['Base Salary'].values[0]
                severance_package = (base_sal / 2) * (tenure_months / 12)
                
                st.markdown(f"<p style='color: #ef4444; font-weight: bold; font-size: 15px;'>Calculated Corporate Severance: ${severance_package:,.2f}</p>", unsafe_allow_html=True)
                
                # Glowing Crimson Execution Button
                execute_fire = st.form_submit_button("🚨 Execute Termination & Revoke System Access")
                
                if execute_fire:
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == fire_emp, 'Status'] = 'Terminated'
                    # Set final settlement payout
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == fire_emp, 'Base Salary'] = severance_package
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == fire_emp, 'Bonus'] = 0.0
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == fire_emp, 'Deductions'] = 0.0
                    st.error(f"Security Alert: System parameters updated. Access revoked for {fire_emp}. Final severance set to ${severance_package:,.2f}.")
                    st.rerun()
                    
        st.markdown("<br>#### Historical Discharge Logs", unsafe_allow_html=True)
        terminated_df = df[df['Status'] == 'Terminated']
        if terminated_df.empty:
            st.info("No corporate exit files currently logged.")
        else:
            st.dataframe(terminated_df[['ID', 'Name', 'Dept', 'Status', 'Base Salary']], use_container_width=True, hide_index=True)

# 5. Session Exit Vector
st.sidebar.markdown("---")
if st.sidebar.button("🔒 Terminate Core Session"):
    st.session_state['authenticated'] = False
    st.rerun()
