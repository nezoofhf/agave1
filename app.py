import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة بنظام العرض العريض (Wide) لتقليل السكرول
st.set_page_config(
    page_title="CoreHR | Advanced Dynamic Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. الألوان الزاهية والعصرية (Vibrant & High-Contrast Corporate UI)
st.markdown("""
<style>
    /* تحسين الخلفية العامة والخطوط */
    .stApp {
        background-color: #f0f4f8;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* القائمة الجانبية المودرن */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%) !important;
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    /* كروت إحصائيات زاهية وبارزة (Vibrant KPI Cards) */
    .vibrant-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(31, 38, 135, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-left: 6px solid #6366f1; /* Indigo Neon */
        transition: transform 0.2s ease;
    }
    .vibrant-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(31, 38, 135, 0.08);
    }
    .card-label { color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; }
    .card-num { color: #0f172a; font-size: 1.8rem; font-weight: 700; margin-top: 5px; }
    
    /* أزرار مخصصة ملونة وزاهية */
    .stButton>button {
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        transition: all 0.2s ease !important;
    }
    
    /* تنسيق خاص لزر الـ Fire / الرفد ليكون بلون تحذيري زاهي */
    div.stButton > button:has(div:contains("Terminate")) {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. نظام الحماية الذكي (Session State)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("<h2 style='text-align: center; color: #1e1b4b; margin-top: 120px;'>🔒 CoreHR Enterprise Security</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("Login"):
            user = st.text_input("Corporate ID")
            pas = st.text_input("Access Token", type="password")
            if st.form_submit_button("Verify & Grant Entry"):
                if user == "admin" and pas == "texas2026":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else: st.error("Access Denied.")
    st.stop()

# 4. بناء البيانات الحية وتجهيز الحسابات التلقائية (Deductions & Allowances)
if 'employees' not in st.session_state:
    st.session_state['employees'] = pd.DataFrame([
        {'ID': 'HR-001', 'Name': 'John Doe', 'Dept': 'Engineering', 'Base Salary': 8000, 'Allowances': 1200, 'Deductions': 300, 'Tax %': 10, 'Status': 'Active'},
        {'ID': 'HR-002', 'Name': 'Jane Smith', 'Dept': 'Marketing', 'Base Salary': 6500, 'Allowances': 800, 'Deductions': 150, 'Tax %': 8, 'Status': 'Active'},
        {'ID': 'HR-003', 'Name': 'Carlos Ramos', 'Dept': 'Operations', 'Base Salary': 5000, 'Allowances': 600, 'Deductions': 400, 'Tax %': 5, 'Status': 'Active'},
        {'ID': 'HR-004', 'Name': 'Aisha Khan', 'Dept': 'Finance', 'Base Salary': 7500, 'Allowances': 1000, 'Deductions': 0, 'Tax %': 10, 'Status': 'Active'}
    ])

df = st.session_state['employees']

# حساب صافي المرتبات بشكل فوري (Net Salary Formula)
# Net = (Base + Allowances - Deductions) * (1 - Tax/100)
df['Net Salary ($)'] = (df['Base Salary'] + df['Allowances'] - df['Deductions']) * (1 - df['Tax %'] / 100)

# القائمة الجانبية الشيك
st.sidebar.markdown("### ⚡ CoreHR Navigation")
menu = st.sidebar.radio("Switch View", ["📊 HR Insights & Payroll", "🔥 Termination Hub (Fire System)"])

# ----------------- VIEW 1: DASHBOARD & PAYROLL -----------------
if menu == "📊 HR Insights & Payroll":
    st.markdown("<h1 style='color: #1e1b4b;'>Workforce & Payroll Intelligence</h1>", unsafe_allow_html=True)
    
    # صف كروت الـ KPIs زاهية الألوان وموزعة عرضياً لتقليل السكرول
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f'<div class="vibrant-card"><div class="card-label">Active Headcount</div><div class="card-num">{len(df[df["Status"]=="Active"])}</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="vibrant-card" style="border-left-color: #10b981;"><div class="card-label">Total Net Payroll</div><div class="card-num">${df[df["Status"]=="Active"]["Net Salary ($)"].sum():,.2f}</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown('<div class="vibrant-card" style="border-left-color: #f59e0b;"><div class="card-label">Avg Absence Rate</div><div class="card-num">2.4%</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown('<div class="vibrant-card" style="border-left-color: #ec4899;"><div class="card-label">Pending Leave Requests</div><div class="card-num">5 Tasks</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # تقسيم الصفحة لعمودين (شمال ويمين) لإنهاء مشكلة السكرول الكتير
    col_left, col_right = st.columns([1.8, 1.2])
    
    with col_left:
        st.markdown("### 👥 Active Employee Ledger (Calculated)")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # تصدير البيانات السريع
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Financial Report", data=csv, file_name="HR_Financial_Report.csv", mime="text/csv")

    with col_right:
        st.markdown("### 💸 Instant Adjustments (Allowances / Deductions)")
        with st.form("Adjustment Form"):
            target_emp = st.selectbox("Select Employee", df[df['Status']=='Active']['Name'])
            adj_type = st.radio("Type", ["Allowance (زيادة/بدل)", "Deduction (خصم/جزاء)"])
            amount = st.number_input("Amount ($)", min_value=0, step=50)
            
            if st.form_submit_button("Apply Live & Recalculate"):
                if adj_type == "Allowance (زيادة/بدل)":
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == target_emp, 'Allowances'] += amount
                else:
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == target_emp, 'Deductions'] += amount
                st.success(f"Successfully processed {adj_type} for {target_emp}!")
                st.rerun()

# ----------------- VIEW 2: FIRE SYSTEM (TERMINATION) -----------------
elif menu == "🔥 Termination Hub (Fire System)":
    st.markdown("<h1 style='color: #7f1d1d;'>Corporate Termination Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b;'>Offboarding dashboard for processing employee exit contracts, severance pay, and immediate revoking of system access.</p>", unsafe_allow_html=True)
    
    col_fire1, col_fire2 = st.columns([1.5, 1.5])
    
    with col_fire1:
        st.markdown("### ⚠️ Initiate Offboarding Protocol")
        active_emps = df[df['Status'] == 'Active']
        
        if active_emps.empty:
            st.info("No active employees found in ledger.")
        else:
            with st.form("Termination Protocol"):
                fire_emp = st.selectbox("Employee to Terminate", active_emps['Name'])
                reason = st.selectbox("Reason for Offboarding", ["Voluntary Resignation", "Performance Issues", "Redundancy / Restructuring", "Policy Violation"])
                months_served = st.number_input("Months Served (For Severance Calculation)", min_value=1, value=12)
                
                # صياعة البيزنس: حساب مكافأة نهاية الخدمة تلقائياً (نصف شهر عن كل سنة مثلاً)
                base_sal = df[df['Name'] == fire_emp]['Base Salary'].values[0]
                calculated_severance = (base_sal / 2) * (months_served / 12)
                
                st.markdown(f"**Estimated Severance Pay (مكافأة نهاية الخدمة):** `${calculated_severance:,.2f}`")
                
                # زرار تحذيري زاهي للرفد وفصل الموظف
                submit_fire = st.form_submit_button("🚨 Execute Termination & Cut Access")
                
                if submit_fire:
                    # تحديث الحالة لـ Terminated وحفظ مكافأة نهاية الخدمة في قاعدة البيانات المؤقتة
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == fire_emp, 'Status'] = 'Terminated'
                    st.session_state['employees'].loc[st.session_state['employees']['Name'] == fire_emp, 'Base Salary'] = calculated_severance # تحويل حسابه لمستحقاته الأخيرة
                    st.error(f"Protocol Executed. {fire_emp} has been set to Terminated. Legal severance of ${calculated_severance:.2f} finalized.")
                    st.rerun()

    with col_fire2:
        st.markdown("### 📄 Offboarded / Terminated Records")
        terminated_df = df[df['Status'] == 'Terminated']
        if terminated_df.empty:
            st.info("No terminated records for this period.")
        else:
            st.dataframe(terminated_df[['ID', 'Name', 'Dept', 'Status']], use_container_width=True, hide_index=True)

# زر تسجيل الخروج
st.sidebar.markdown("---")
if st.sidebar.button("🔒 Secure Logout"):
    st.session_state['authenticated'] = False
    st.rerun()
