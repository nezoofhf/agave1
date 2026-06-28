import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة الاحترافية بنظام الـ Wide
st.set_page_config(
    page_title="CoreHR | Quantum Dark Suite",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. هندسة الـ Dark Mode الفخم باستخدام الـ CSS المخصص
st.markdown("""
<style>
    /* تغيير خلفية التطبيق بالكامل للون الأسود الكربوني الفاخر */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* ضبط نصوص العناوين الافتراضية لتبدو متناسقة */
    h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0 !important;
    }
    
    /* الـ Sidebar الغامق مع تباين النيون */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070a13 0%, #0f172a 100%) !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * { color: #94a3b8 !important; }
    
    /* كروت إحصائيات زاهية وبارزة في خلفية غامقة (Neon Cyber Cards) */
    .neon-card {
        background: #111827;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border: 1px solid #1e293b;
        border-left: 6px solid #6366f1; /* خط نيون نيلي */
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 15px;
    }
    .neon-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.2);
    }
    .card-label { color: #94a3b8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .card-num { color: #ffffff; font-size: 2rem; font-weight: 700; margin-top: 6px; }
    
    /* تجميل المدخلات (Inputs) لتناسب المود المظلم */
    input, select, textarea, div[data-baseweb="select"] {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
    }
    
    /* أزرار النظام الملونة والزاهية جداً للتفاعل والسحب */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
        box-shadow: 0 0 18px rgba(99, 102, 241, 0.5) !important;
    }
    
    /* صياعة الـ Fire Button: كود مخصص لزر الرفد بلون أحمر نيون متوهج */
    div.stButton > button:has(div:contains("Terminate")) {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4) !important;
    }
    div.stButton > button:has(div:contains("Terminate")):hover {
        box-shadow: 0 0 22px rgba(239, 68, 68, 0.6) !important;
    }
    
    /* تجميل الـ Dataframes والجداول بالـ Dark Mode */
    [data-testid="stDataFrame"] {
        background: #111827 !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. نظام الحماية الذكي للتطبيقات الكبرى (Enterprise Security Session)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<h2 style='text-align: center; color: #ffffff; margin-top: 120px;'>🔒 CoreHR Quantum Portal</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("Login"):
            user = st.text_input("Corporate User ID")
            pas = st.text_input("Access Token", type="password")
            if st.form_submit_button("Grant Secure Access"):
                if user == "admin" and pas == "texas2026":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else: st.error("Authentication failed. Invalid cryptographic credentials.")
    st.stop()

# 4. بناء مخزن البيانات الداخلي وحساب الـ Deductions والـ Allowances تلقائياً
if 'employees' not in st.session_state:
    st.session_state['employees'] = pd.DataFrame([
        {'ID': 'HR-001', 'Name': 'John Doe', 'Dept': 'Engineering', 'Base Salary': 9500, 'Allowances': 1500, 'Deductions': 400, 'Tax %': 12, 'Status': 'Active'},
        {'ID': 'HR-002', 'Name': 'Jane Smith', 'Dept': 'Marketing', 'Base Salary': 7200, 'Allowances': 900, 'Deductions': 200, 'Tax %': 10, 'Status': 'Active'},
        {'ID': 'HR-003', 'Name': 'Carlos Ramos', 'Dept': 'Operations', 'Base Salary': 5800, 'Allowances': 700, 'Deductions': 500, 'Tax %': 8, 'Status': 'Active'},
        {'ID': 'HR-004', 'Name': 'Aisha Khan', 'Dept': 'Finance', 'Base Salary': 8800, 'Allowances': 1100, 'Deductions': 0, 'Tax %': 12, 'Status': 'Active'}
    ])

df = st.session_state['employees']

# معالجة وصياغة صافي الرواتب فورياً (Automated Payroll Logic)
df['Net Salary ($)'] = (df['Base Salary'] + df['Allowances'] - df['Deductions']) * (1 - df['Tax %'] / 100)

# القائمة الجانبية للتنقل الذكي
st.sidebar.markdown("### ⚡ Navigation Hub")
menu = st.sidebar.radio("Switch View", ["📊 Live Core Metrics & Payroll", "🔥 Executive Termination (Fire System)"])

# ----------------- VIEW 1: DASHBOARD & PAYROLL -----------------
if menu == "📊 Live Core Metrics & Payroll":
    st.markdown("<h1 style='color: #ffffff;'>Workforce & Payroll Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size:14px; margin-bottom: 25px;'>Advanced system metrics updated in real-time.</p>", unsafe_allow_html=True)
    
    # توزيع الكروت عرضياً لمنع السكرول المزعج
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f'<div class="neon-card"><div class="card-label">Active Headcount</div><div class="card-num">{len(df[df["Status"]=="Active"])}</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="neon-card" style="border-left-color: #10b981;"><div class="card-label">Total Monthly Payroll</div><div class="card-num">${df[df["Status"]=="Active"]["Net Salary ($)"].sum():,.2f}</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown('<div class="neon-card" style="border-left-color: #f59e0b;"><div class="card-label">Absence Index</div><div class="card-num">1.8%</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown('<div class="neon-card" style="border-left-color: #ec4899;"><div class="card-label">Pending Exit Protocols</div><div class="card-num">' + str(len(df[df["Status"]=="Terminated"])) + ' Archive</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # تقسيم الشاشة لعمودين متوازنين (يمين وشمال) لمنع السكرول نهائياً
    col_left, col_right = st.columns([1.8, 1.2])
    
    with col_left:
        st.markdown("### 👥 Dynamic Employee Ledger")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # ميزة تصدير التقارير الفورية للـ Management
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Quantum Ledger to CSV", data=csv, file_name="CoreHR_Quantum_Ledger.csv", mime="text/csv")

    with col_right:
        st.markdown("### 💸 Quick Adjustments")
        with st.form("Adjustment Form"):
            target_emp = st.selectbox("Choose Employee", df[df['Status']=='Active']['Name'])
            adj_type = st.radio("Financial Vector", ["Add Allowance (بدلات/مكافأة)", "Apply Deduction (خصومات/جزاءات)"])
            amount = st.number_input("Amount ($)", min_value=0, step=100, value=100)
            
            if st.form_submit_button("Inject to Ledger & Recalculate"):
                if adj_type == "Add Allowance (بدلات/مكافأة)":
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == target_emp, 'Allowances'] += amount
                else:
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == target_emp, 'Deductions'] += amount
                st.success(f"Financial adjustment applied for {target_emp}!")
                st.rerun()

# ----------------- VIEW 2: FIRE SYSTEM (TERMINATION HUB) -----------------
elif menu == "🔥 Executive Termination (Fire System)":
    st.markdown("<h1 style='color: #ef4444;'>Corporate Termination Core</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size:14px; margin-bottom: 25px;'>Immediate contract settlement, automated severance pay computation, and access revocation.</p>", unsafe_allow_html=True)
    
    col_fire1, col_fire2 = st.columns([1.4, 1.6])
    
    with col_fire1:
        st.markdown("### ⚠️ Execute Offboarding")
        active_emps = df[df['Status'] == 'Active']
        
        if active_emps.empty:
            st.info("No active workforce profiles detected.")
        else:
            with st.form("Termination Core Form"):
                fire_emp = st.selectbox("Select Target Employee", active_emps['Name'])
                reason = st.selectbox("Legal Termination Clause", ["Performance Non-Compliance", "Corporate Restructuring", "Policy & Security Violation", "Voluntary Departure"])
                tenure_months = st.number_input("Total Tenure (Months Served)", min_value=1, value=24)
                
                # صياعة الحساب: حساب مستحقات نهاية الخدمة بدقة (نصف شهر عن كل سنة خدمة)
                base_sal = df[df['Name'] == fire_emp]['Base Salary'].values[0]
                severance_package = (base_sal / 2) * (tenure_months / 12)
                
                st.markdown(f"<p style='color: #ef4444; font-weight: bold; font-size: 16px;'>Computed Severance Package: ${severance_package:,.2f}</p>", unsafe_allow_html=True)
                
                # زرار الإعدام الوظيفي بالـ Red Neon Style
                execute = st.form_submit_button("🚨 Terminate Employee & Revoke Access")
                
                if execute:
                    # تحديث الحالة وحفظ الحساب المالي
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == fire_emp, 'Status'] = 'Terminated'
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == fire_emp, 'Base Salary'] = severance_package
                    st.error(f"Access Revoked. {fire_emp} has been moved to offboarded archive with a final settlement of ${severance_package:,.2f}.")
                    st.rerun()

    with col_fire2:
        st.markdown("### 📂 Offboarded Audit Trail (الموظفين المفصولين)")
        terminated_df = df[df['Status'] == 'Terminated']
        if terminated_df.empty:
            st.info("No active termination protocols recorded in this cycle.")
        else:
            st.dataframe(terminated_df[['ID', 'Name', 'Dept', 'Status']], use_container_width=True, hide_index=True)

# زرار تسجيل الخروج الفاخر
st.sidebar.markdown("---")
if st.sidebar.button("🔒 Terminate Session"):
    st.session_state['authenticated'] = False
    st.rerun()
