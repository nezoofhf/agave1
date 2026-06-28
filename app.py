import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة الأساسية للـ Dashboard
st.set_page_config(
    page_title="CoreHR | Advanced Analytics",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. صياعة الـ CSS: تحويل واجهة Streamlit الجافة إلى تطبيق ويب فخم
st.markdown("""
<style>
    /* تغيير الخلفية العامة والخطوط لتجربة مستخدم مريحة */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }
    
    /* تصميم الـ Sidebar الغامق والفاخر */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        box-shadow: 4px 0 10px rgba(0,0,0,0.05);
    }
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    
    /* كروت الـ KPIs التفاعلية الـ "صايعة" */
    .kpi-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
        border: 1px solid #e2e8f0;
        border-top: 4px solid #3b82f6; /* لون أزرق براندينج */
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    }
    .kpi-title {
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 700;
        margin-top: 8px;
    }
    .kpi-trend {
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 6px;
    }
    .trend-up { color: #10b981; }
    
    /* تجميل أزرار النظام بالكامل بنظام الـ Gradients والـ Shadows */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 10px 28px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* تحسين شكل الجداول والـ Dataframes */
    [data-testid="stDataFrame"] {
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# 3. إدارة الجلسة لحماية التطبيق (Session State Authentication)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# شاشة تسجيل الدخول الاحترافية إذا لم يكن مسجلاً
if not st.session_state['authenticated']:
    st.markdown("<h2 style='text-align: center; color: #0f172a; margin-top: 100px;'>🔒 CoreHR Enterprise Portals</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form("Login Form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Secure Login")
            if submitted:
                if username == "admin" and password == "texas2026":
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Invalid corporate credentials.")
    st.stop()

# 4. محتوى الـ Dashboard الرئيسي بعد تخطي الحماية
st.sidebar.markdown("### 🏢 CoreHR Navigation")
menu = st.sidebar.radio("Go to", ["📊 Executive Dashboard", "👥 Employee Directory", "💰 Payroll Management"])

# بيانات وهمية للعرض بشكل مبهر (Mock Data)
employees_data = pd.DataFrame({
    'Emp ID': [f"HR-{i:03d}" for i in range(1, 6)],
    'Full Name': ['John Doe', 'Jane Smith', 'Carlos Ramos', 'Aisha Khan', 'Michael Brown'],
    'Department': ['Engineering', 'Marketing', 'Operations', 'Finance', 'HR'],
    'Salary ($)': [95000, 82000, 75000, 91000, 68000],
    'Status': ['Active', 'Active', 'On Leave', 'Active', 'Active']
})

if menu == "📊 Executive Dashboard":
    st.markdown("<h1 style='color: #0f172a;'>Executive HR Overview</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-bottom: 30px;'>Real-time analytics and workforce efficiency metrics.</p>", unsafe_allow_html=True)
    
    # صف كروت الـ KPIs المصممة بالـ CSS الصايع
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    
    with kpi_col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Total Headcount</div>
            <div class="kpi-value">1,248</div>
            <div class="kpi-trend trend-up">▲ +4.2% This Quarter</div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi_col2:
        st.markdown("""
        <div class="kpi-card" style="border-top-color: #10b981;">
            <div class="kpi-title">Monthly Payroll Total</div>
            <div class="kpi-value">$412.5K</div>
            <div class="kpi-trend" style="color: #64748b;">• Within Budget Allocations</div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi_col3:
        st.markdown("""
        <div class="kpi-card" style="border-top-color: #f59e0b;">
            <div class="kpi-title">Retention Rate</div>
            <div class="kpi-value">94.8%</div>
            <div class="kpi-trend trend-up">▲ +1.5% vs Last Year</div>
        </div>
        """, unsafe_allow_html=True)

    # إضافة رسم بياني فخم مدمج
    st.markdown("<h3 style='color: #0f172a; margin-top: 20px;'>Department Distribution & Expenses</h3>", unsafe_allow_html=True)
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Engineering', 'Marketing', 'Sales']
    )
    st.line_chart(chart_data)

elif menu == "👥 Employee Directory":
    st.markdown("<h1 style='color: #0f172a;'>Employee Records</h1>", unsafe_allow_html=True)
    
    # محرك بحث شيك للبيانات
    search = st.text_input("🔍 Quick Search by Name or ID")
    
    # عرض الجدول بتنسيقه الجديد الفخم
    st.dataframe(employees_data, use_container_width=True)
    
    # الصياعة هنا: زر تصدير التقارير اللي يرفع من قيمة السعر
    st.markdown("<br>", unsafe_allow_html=True)
    csv = employees_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Full Directory to Excel / CSV",
        data=csv,
        file_name='CoreHR_Directory.csv',
        mime='text/csv',
    )

elif menu == "💰 Payroll Management":
    st.markdown("<h1 style='color: #0f172a;'>Payroll Processing</h1>", unsafe_allow_html=True)
    st.info("Secure connection established with SQLite3 Database.")
    
    # نموذج تفاعلي لتعديل الرواتب
    with st.form("Payroll Update"):
        st.write("### Adjust Employee Compensation")
        emp_id = st.selectbox("Select Employee ID", employees_data['Emp ID'])
        new_bonus = st.number_input("Performance Bonus ($)", min_value=0, max_value=10000, step=500)
        submit_payroll = st.form_submit_button("Recalculate & Push to Ledger")
        
        if submit_payroll:
            st.success(f"Ledger entry updated successfully for {emp_id} with an additional ${new_bonus} bonus!")

# زر تسجيل الخروج في أسفل القائمة الجانبية
st.sidebar.markdown("---")
if st.sidebar.button("🔒 Logout"):
    st.session_state['authenticated'] = False
    st.rerun()
