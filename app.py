import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import plotly.express as px

# ---------------------------------------------------------
# DATABASE SETUP & FUNCTIONS
# ---------------------------------------------------------
DB_NAME = "hr_system.db"

def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول الأساسية إن لم تكن موجودة"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # جدول الموظفين
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL,
            salary REAL NOT NULL,
            join_date TEXT NOT NULL,
            performance_score TEXT DEFAULT 'Good'
        )
    """)
    
    # جدول طلبات الإجازات
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_email TEXT NOT NULL,
            leave_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)
    
    # إدخال بيانات تجريبية إذا كانت قاعدة البيانات فارغة
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        sample_employees = [
            ('Nezar Mohammed', 'nezar@company.com', 'Engineering', 'Software Engineer', 15000, '2025-01-15', 'Excellent'),
            ('Shady Hany', 'shady@company.com', 'Marketing', 'Growth Specialist', 12000, '2025-03-10', 'Excellent'),
            ('Ahmed Ali', 'ahmed@company.com', 'HR', 'HR Specialist', 9000, '2024-11-01', 'Good'),
            ('Sara Omar', 'sara@company.com', 'Engineering', 'UI/UX Designer', 11000, '2025-05-20', 'Very Good')
        ]
        cursor.executemany("""
            INSERT INTO employees (name, email, department, role, salary, join_date, performance_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_employees)
        
        sample_leaves = [
            ('sara@company.com', 'Sick Leave', '2026-06-01', '2026-06-03', 'Pending'),
            ('ahmed@company.com', 'Annual Leave', '2026-07-10', '2026-07-15', 'Approved')
        ]
        cursor.executemany("""
            INSERT INTO leave_requests (employee_email, leave_type, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, sample_leaves)
        
    conn.commit()
    conn.close()

# دالة مساعدة لتنفيذ الاستعلامات وجلب البيانات كـ DataFrame
def run_query(query, params=()):
    with sqlite3.connect(DB_NAME) as conn:
        return pd.read_sql_query(query, conn, params=params)

# دالة مساعدة لتعديل البيانات (Insert, Update, Delete)
def run_cmd(cmd, params=()):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(cmd, params)
        conn.commit()

# ---------------------------------------------------------
# STREAMLIT INTERFACE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="CoreHR | Enterprise Portal", page_icon="💼", layout="wide")
init_db()

# تخصيص واجهة المستخدم بـ CSS بسيط ومحترف
st.markdown("""
    <style>
    .main-title { font-size:2.4rem !important; font-weight: 700; color: #1E3A8A; }
    .metric-card { background-color: #F3F4F6; padding: 15px; border-radius: 10px; border-left: 5px solid #3B82F6; }
    </style>
""", unsafe_allow_html=True)

# الـ Sidebar الرئيسي للتحكم في نوع الواجهة والأقسام
st.sidebar.title("💼 CoreHR System")
app_mode = st.sidebar.selectbox("Choose Portal View:", ["👤 Employee Portal", "👑 Admin Dashboard"])

# ---------------------------------------------------------
# MODE 1: EMPLOYEE PORTAL
# ---------------------------------------------------------
if app_mode == "👤 Employee Portal":
    st.markdown("<h1 class='main-title'>Employee Self-Service Portal</h1>", unsafe_allow_html=True)
    st.write("Welcome to your corporate space. Submit requests and check your profile.")
    
    tab1, tab2 = st.tabs(["📝 Submit Leave Request", "📋 My Request History"])
    
    with tab1:
        st.subheader("New Leave Request Form")
        with st.form("leave_form", clear_on_submit=True):
            emp_email = st.selectbox("Confirm Your Email:", run_query("SELECT email FROM employees")['email'].tolist())
            leave_type = st.selectbox("Leave Type:", ["Annual Leave", "Sick Leave", "Unpaid Leave", "Maternity/Paternity"])
            start_d = st.date_input("Start Date", min_value=datetime.today())
            end_d = st.date_input("End Date", min_value=datetime.today())
            
            submit_btn = st.form_submit_button("Submit Request")
            if submit_btn:
                if start_d > end_d:
                    st.error("Error: Start date cannot be after end date.")
                else:
                    run_cmd("""
                        INSERT INTO leave_requests (employee_email, leave_type, start_date, end_date, status)
                        VALUES (?, ?, ?, ?, 'Pending')
                    """, (emp_email, leave_type, str(start_d), str(end_d)))
                    st.success("Your request has been submitted successfully for HR review!")
                    
    with tab2:
        st.subheader("Track Your Requests")
        search_email = st.selectbox("Select email to view history:", run_query("SELECT email FROM employees")['email'].tolist(), key="search_emp")
        history_df = run_query("SELECT leave_type, start_date, end_date, status FROM leave_requests WHERE employee_email = ?", (search_email,))
        if not history_df.empty:
            st.dataframe(history_df, use_container_width=True)
        else:
            st.info("No leave history found for this email.")

# ---------------------------------------------------------
# MODE 2: ADMIN DASHBOARD (المكان المليء بالشغل الاحترافي)
# ---------------------------------------------------------
else:
    st.markdown("<h1 class='main-title'>HR Executive Admin Dashboard</h1>", unsafe_allow_html=True)
    
    # 1. جلب البيانات المحدثة للحسابات السريعة
    df_emp = run_query("SELECT * FROM employees")
    df_leaves = run_query("SELECT * FROM leave_requests")
    
    total_employees = len(df_emp)
    pending_leaves = len(df_leaves[df_leaves['status'] == 'Pending'])
    total_departments = df_emp['department'].nunique()
    total_payroll = df_emp['salary'].sum()
    
    # 2. كروت المؤشرات العليا (KPIs Top Order)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><h4>Total Headcount</h4><h2>{total_employees} Employees</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card' style='border-left-color:#EF4444;'><h4>Pending Leaves</h4><h2>{pending_leaves} Actions</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card' style='border-left-color:#10B981;'><h4>Active Departments</h4><h2>{total_departments} Units</h2></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card' style='border-left-color:#F59E0B;'><h4>Monthly Payroll</h4><h2>{total_payroll:,.2f} $</h2></div>", unsafe_allow_html=True)
        
    st.write("---")
    
    # 3. تنظيم الأقسام الداخلية للـ Admin باستخدام Tabs احترافية
    adm_tab1, adm_tab2, adm_tab3, adm_tab4 = st.tabs([
        "📊 Analytics & Insights", 
        "🗂️ Employee Management", 
        "⏳ Leave Approval Workflow",
        "➕ Add New Employee"
    ])
    
    # Tab 1: الإحصائيات والرسم البياني
    with adm_tab1:
        st.subheader("Workforce Distribution & Analytics")
        if not df_emp.empty:
            g_col1, g_col2 = st.columns(2)
            with g_col1:
                # توزيع الموظفين حسب القسم
                fig_dept = px.bar(df_emp, x='department', title="Headcount by Department", 
                                  labels={'department': 'Department', 'index': 'Count'},
                                  color='department', color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_dept, use_container_width=True)
            with g_col2:
                # توزيع مستويات الأداء
                fig_perf = px.pie(df_emp, names='performance_score', title="Performance Overview",
                                  color_discrete_sequence=px.colors.qualitative.Safe)
                st.plotly_chart(fig_perf, use_container_width=True)
        else:
            st.warning("No data available to render charts.")

    # Tab 2: إدارة وعرض جدول الموظفين الفعلي مع الفلترة
    with adm_tab2:
        st.subheader("Employee Master Directory")
        
        # فلاتر سريعة للبحث
        dept_filter = st.multiselect("Filter by Department:", options=df_emp['department'].unique().tolist(), default=df_emp['department'].unique().tolist())
        filtered_df = df_emp[df_emp['department'].isin(dept_filter)]
        
        st.dataframe(filtered_df[['id', 'name', 'email', 'department', 'role', 'salary', 'join_date', 'performance_score']], use_container_width=True)
        
        # إمكانية تعديل تقييم الأداء لموظف ما مباشرة
        st.write("---")
        st.write("**Quick Update: Employee Performance Evaluation**")
        up_col1, up_col2 = st.columns(2)
        with up_col1:
            target_emp = st.selectbox("Select Employee:", df_emp['email'].tolist())
        with up_col2:
            new_score = st.selectbox("New Performance Score:", ["Excellent", "Very Good", "Good", "Needs Improvement"])
        if st.button("Update Evaluation"):
            run_cmd("UPDATE employees SET performance_score = ? WHERE email = ?", (new_score, target_emp))
            st.success(f"Performance updated for {target_emp} to {new_score}!")
            st.rerun()

    # Tab 3: سير العمل للموافقة على الإجازات (Workflow Action)
    with adm_tab3:
        st.subheader("Pending Leave Requests Workflow")
        pending_df = run_query("""
            SELECT leave_requests.id, employees.name, leave_requests.employee_email, leave_requests.leave_type, leave_requests.start_date, leave_requests.end_date 
            FROM leave_requests 
            JOIN employees ON leave_requests.employee_email = employees.email
            WHERE leave_requests.status = 'Pending'
        """)
        
        if pending_df.empty:
            st.success("All caught up! No pending leave requests to process.")
        else:
            st.dataframe(pending_df, use_container_width=True)
            
            # أخذ إجراء (موافقة / رفض) بناءً على الرقم التعريفي للطلب
            st.write("**Action Center:**")
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                req_id = st.selectbox("Select Request ID to process:", pending_df['id'].tolist())
            with act_col2:
                action = st.radio("Decision:", ["Approve", "Reject"], horizontal=True)
                
            if st.button("Execute Decision"):
                final_status = "Approved" if action == "Approve" else "Rejected"
                run_cmd("UPDATE leave_requests SET status = ? WHERE id = ?", (final_status, req_id))
                st.success(f"Request ID {req_id} has been {final_status} successfully.")
                st.rerun()

    # Tab 4: إضافة موظف جديد لقاعدة البيانات
    with adm_tab4:
        st.subheader("Onboard New Employee")
        with st.form("add_employee_form"):
            new_name = st.text_input("Full Name:")
            new_email = st.text_input("Corporate Email:")
            new_dept = st.selectbox("Department:", ["Engineering", "HR", "Marketing", "Sales", "Finance", "chief", "waiter", "office boy", "supervisor"])
            new_role = st.text_input("Job Title / Role:")
            new_salary = st.number_input("Monthly Salary ($):", min_value=0.0, step=500.0)
            new_join = st.date_input("Hiring / Join Date:")
            
            add_btn = st.form_submit_button("Confirm Onboarding")
            if add_btn:
                if not new_name or not new_email or not new_role:
                    st.error("Please fill out all mandatory fields.")
                else:
                    try:
                        run_cmd("""
                            INSERT INTO employees (name, email, department, role, salary, join_date)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (new_name, new_email, new_dept, new_role, new_salary, str(new_join)))
                        st.success(f"Welcome aboard! {new_name} has been successfully added to the system.")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("An employee with this email already exists in the records.")