# app.py - School Resource Management System (SRMS) by WeGEM
import streamlit as st
import pandas as pd
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import random
import string
import base64
from io import BytesIO
import qrcode
from PIL import Image

# Page config
st.set_page_config(
    page_title="SRMS - School Resource Management System",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching your HTML style
st.markdown("""
<style>
    /* Your existing CSS styles */
    :root {
        --primary: #0a0e27;
        --accent: #e94560;
        --gold: #d4af37;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27, #1a1f4e, #0f3460);
    }
    
    .main-header {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.15);
    }
    
    .school-code-banner {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border: 2px dashed rgba(233,69,96,0.4);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
    }
    
    .stat-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 12px;
        border-left: 4px solid #e94560;
        border: 1px solid rgba(255,255,255,0.15);
    }
    
    .golden-button {
        background: linear-gradient(135deg, #d4af37, #b8941f);
        color: #0a0e27;
        font-weight: 700;
        border: none;
    }
    
    h1, h2, h3 {
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'school' not in st.session_state:
    st.session_state.school = None
if 'page' not in st.session_state:
    st.session_state.page = 'startup'
if 'current_section' not in st.session_state:
    st.session_state.current_section = 'dashboard'

# Data storage setup
DATA_DIR = Path("srms_data")
DATA_DIR.mkdir(exist_ok=True)

def load_data(filename, default=None):
    """Load data from JSON file"""
    if default is None:
        default = {}
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, 'r') as f:
            return json.load(f)
    return default

def save_data(filename, data):
    """Save data to JSON file"""
    filepath = DATA_DIR / filename
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def generate_code(prefix="", length=8):
    """Generate a random code"""
    chars = string.ascii_uppercase + string.digits
    return prefix + ''.join(random.choices(chars, k=length))

def hash_password(password):
    """Hash a password"""
    return hashlib.sha256(password.encode()).hexdigest()

# ============== STARTUP PAGE ==============
def startup_page():
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px;">
        <div style="width: 160px; height: 160px; background: linear-gradient(135deg, #d4af37, #f0d060, #d4af37); 
             border-radius: 35px; display: inline-flex; align-items: center; justify-content: center; 
             font-size: 55px; font-weight: 900; color: #0a0e27; margin-bottom: 20px;
             box-shadow: 0 20px 60px rgba(212, 175, 55, 0.4);">
            SRMS
        </div>
        <h1 style="font-size: 3.5em; background: linear-gradient(180deg, #f0d060, #d4af37, #b8941f); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            SRMS
        </h1>
        <p style="font-size: 1.4em; color: rgba(255,255,255,0.8);">School Resource Management System</p>
        <p style="color: rgba(212,175,55,0.9); font-size: 1.1em;">by <span style="color: #f0d060;">WeGEM</span> (Edwin)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔑 Staff Login", use_container_width=True, key="login_btn"):
            st.session_state.action = 'login'
    
    with col2:
        if st.button("📝 Staff Sign Up", use_container_width=True, key="signup_btn"):
            st.session_state.action = 'signup'
    
    with col3:
        if st.button("🏫 Create School", use_container_width=True, key="create_btn"):
            st.session_state.action = 'create'
    
    if 'action' not in st.session_state:
        st.session_state.action = None
    
    if st.session_state.action == 'login':
        login_form()
    elif st.session_state.action == 'signup':
        signup_form()
    elif st.session_state.action == 'create':
        create_school_form()

def login_form():
    st.markdown("### 🔐 Staff Login")
    with st.form("login_form"):
        name = st.text_input("👤 Your Full Name")
        school_name = st.text_input("🏢 School Name")
        invite_code = st.text_input("🔑 Invite Code")
        password = st.text_input("🔒 Password", type="password")
        
        if st.form_submit_button("Login", use_container_width=True):
            schools = load_data("schools.json", {})
            school = schools.get(school_name)
            
            if not school:
                st.error("School not found!")
                return
            
            users = load_data(f"users_{school_name}.json", [])
            user = next((u for u in users if u['name'].lower() == name.lower() 
                        and u['code'] == invite_code.upper()), None)
            
            if not user or not (user['password'] == hash_password(password)):
                st.error("Invalid credentials!")
                return
            
            st.session_state.user = user
            st.session_state.school = school
            st.session_state.page = 'dashboard'
            st.rerun()

def signup_form():
    st.markdown("### 📝 Staff Sign Up")
    with st.form("signup_form"):
        name = st.text_input("👤 Full Name")
        email = st.text_input("📧 Email Address")
        phone = st.text_input("📞 Phone Number")
        school_name = st.text_input("🏢 School Name")
        invite_code = st.text_input("🔑 Invite Code (from admin)")
        staff_id = st.text_input("👤 Staff ID (Optional)")
        password = st.text_input("🔒 Create Password", type="password")
        
        if st.form_submit_button("Sign Up", use_container_width=True):
            schools = load_data("schools.json", {})
            school = schools.get(school_name)
            
            if not school:
                st.error("School not found!")
                return
            
            if school['invite_code'] != invite_code.upper():
                st.error("Invalid invite code!")
                return
            
            users = load_data(f"users_{school_name}.json", [])
            if any(u['email'] == email for u in users):
                st.error("Email already registered!")
                return
            
            new_user = {
                "name": name,
                "email": email,
                "phone": phone,
                "staff_id": staff_id,
                "code": invite_code.upper(),
                "password": hash_password(password),
                "role": "teacher",
                "joined": datetime.now().strftime("%Y-%m-%d")
            }
            users.append(new_user)
            save_data(f"users_{school_name}.json", users)
            
            st.session_state.user = new_user
            st.session_state.school = school
            st.session_state.page = 'dashboard'
            st.success("Registration successful!")
            st.rerun()

def create_school_form():
    st.markdown("### 🏫 Create New School")
    with st.form("create_school_form"):
        school_name = st.text_input("🏢 School Name")
        address = st.text_input("📍 School Address")
        admin_name = st.text_input("👤 Admin Full Name")
        admin_email = st.text_input("📧 Admin Email")
        admin_phone = st.text_input("📞 Admin Phone")
        password = st.text_input("🔒 Password", type="password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password")
        
        if st.form_submit_button("Create School", use_container_width=True):
            if password != confirm_password:
                st.error("Passwords don't match!")
                return
            
            if len(password) < 8:
                st.error("Password must be at least 8 characters!")
                return
            
            schools = load_data("schools.json", {})
            if school_name in schools:
                st.error("School already exists!")
                return
            
            invite_code = generate_code()
            school = {
                "name": school_name,
                "address": address,
                "admin_name": admin_name,
                "admin_email": admin_email,
                "admin_phone": admin_phone,
                "invite_code": invite_code,
                "created": datetime.now().strftime("%Y-%m-%d")
            }
            schools[school_name] = school
            save_data("schools.json", schools)
            
            admin_user = {
                "name": admin_name,
                "email": admin_email,
                "phone": admin_phone,
                "staff_id": "ADMIN-001",
                "code": invite_code,
                "password": hash_password(password),
                "role": "admin",
                "joined": datetime.now().strftime("%Y-%m-%d")
            }
            save_data(f"users_{school_name}.json", [admin_user])
            
            # Initialize all data files
            for file in ["books", "members", "borrowed", "teachers", "classes", 
                        "furniture", "book_issues", "individual_lendings", 
                        "audit_log", "chat_messages"]:
                save_data(f"{file}_{school_name}.json", [])
            
            st.session_state.user = admin_user
            st.session_state.school = school
            st.session_state.page = 'dashboard'
            st.success(f"School created! Invite Code: {invite_code}")
            st.info("Save this code - staff will need it to join!")
            st.rerun()

# ============== DASHBOARD ==============
def dashboard_page():
    school_name = st.session_state.school['name']
    user = st.session_state.user
    
    # Header
    st.markdown(f"""
    <div class="main-header" style="text-align: center;">
        <h1>🏫 {school_name}</h1>
        <p style="color: white;">👤 {user['name']} 
        <span style="background: {'#e94560' if user['role']=='admin' else '#0f3460'}; 
              color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.8em;">
            {user['role'].upper()}
        </span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Invite code banner (admin only)
    if user['role'] == 'admin':
        st.markdown(f"""
        <div class="school-code-banner">
            <p style="color: white;">🏫 School Invite Code - Share with Staff</p>
            <h2 style="font-family: 'Courier New', monospace; letter-spacing: 8px;">
                {st.session_state.school['invite_code']}
            </h2>
            <button onclick="navigator.clipboard.writeText('{st.session_state.school['invite_code']}')">
                📋 Copy Code
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation tabs matching your HTML sections
    tabs = st.tabs([
        "📊 Dashboard", "📖 Book Issuing", "👤 Lend Book", "🪑 Furniture",
        "↩️ Returns", "📋 Borrowed", "👥 Members", "📚 Catalog",
        "👨‍🏫 Teachers", "📋 Classes", "📱 QR", "💬 Chat",
        "📝 Log", "📈 Reports", "⚙️ Settings"
    ])
    
    with tabs[0]:
        render_dashboard()
    with tabs[1]:
        render_book_issuing()
    with tabs[2]:
        render_individual_lending()
    with tabs[3]:
        render_furniture()
    with tabs[4]:
        render_returns()
    with tabs[5]:
        render_borrowed()
    with tabs[6]:
        render_members()
    with tabs[7]:
        render_catalog()
    with tabs[8]:
        render_teachers()
    with tabs[9]:
        render_classes()
    with tabs[10]:
        render_qr()
    with tabs[11]:
        render_chat()
    with tabs[12]:
        render_audit_log()
    with tabs[13]:
        render_reports()
    with tabs[14]:
        render_settings()
    
    # Logout button
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.school = None
        st.session_state.page = 'startup'
        st.rerun()

def render_dashboard():
    school_name = st.session_state.school['name']
    
    books = load_data(f"books_{school_name}.json", [])
    borrowed = load_data(f"borrowed_{school_name}.json", [])
    members = load_data(f"members_{school_name}.json", [])
    teachers = load_data(f"teachers_{school_name}.json", [])
    furniture = load_data(f"furniture_{school_name}.json", [])
    
    total_books = sum(b.get('quantity', 0) for b in books)
    books_borrowed = len([b for b in borrowed if not b.get('returned', False)])
    overdue = len([b for b in borrowed if not b.get('returned', False) 
                   and datetime.strptime(b.get('returnDate', '2000-01-01'), '%Y-%m-%d') < datetime.now()])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2em; font-weight: 800;">{total_books}</div>
            <div style="color: rgba(255,255,255,0.75);">Total Books</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2em; font-weight: 800;">{books_borrowed}</div>
            <div style="color: rgba(255,255,255,0.75);">Books Borrowed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2em; font-weight: 800;">{len(members)}</div>
            <div style="color: rgba(255,255,255,0.75);">Members</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2em; font-weight: 800;">{overdue}</div>
            <div style="color: rgba(255,255,255,0.75);">Overdue</div>
        </div>
        """, unsafe_allow_html=True)

def render_book_issuing():
    st.subheader("📖 Bulk Book Issuing to Class")
    
    school_name = st.session_state.school['name']
    books = load_data(f"books_{school_name}.json", [])
    classes = load_data(f"classes_{school_name}.json", [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_book = st.selectbox("Select Book", [b['title'] for b in books if b.get('quantity', 0) > 0])
    
    with col2:
        selected_class = st.selectbox("Select Class", [c['name'] for c in classes])
    
    col3, col4 = st.columns(2)
    with col3:
        issue_date = st.date_input("Issue Date", datetime.now())
    with col4:
        return_date = st.date_input("Return Date", datetime.now() + timedelta(days=14))
    
    if st.button("Load Class Students", use_container_width=True):
        class_data = next((c for c in classes if c['name'] == selected_class), None)
        if class_data:
            st.session_state.current_class_students = class_data.get('students', [])
            st.success(f"Loaded {len(st.session_state.current_class_students)} students")
    
    if 'current_class_students' in st.session_state:
        students = st.session_state.current_class_students
        if students:
            # Create a DataFrame for bulk operations
            df = pd.DataFrame(students)
            df['Book No'] = ""
            df['Issue'] = False
            
            edited_df = st.data_editor(df, use_container_width=True, num_rows="fixed")
            
            if st.button("✅ Issue Books to Selected", use_container_width=True):
                issued_count = 0
                borrowed = load_data(f"borrowed_{school_name}.json", [])
                
                for idx, row in edited_df.iterrows():
                    if row['Issue'] and row['Book No']:
                        book = next((b for b in books if b['title'] == selected_book), None)
                        if book and book['quantity'] > 0:
                            borrowed.append({
                                "name": row['name'],
                                "adm": row.get('adm', ''),
                                "bookTitle": selected_book,
                                "bookNo": row['Book No'],
                                "borrowDate": issue_date.strftime('%Y-%m-%d'),
                                "returnDate": return_date.strftime('%Y-%m-%d'),
                                "returned": False,
                                "id": generate_code("BOR")
                            })
                            book['quantity'] -= 1
                            issued_count += 1
                
                save_data(f"borrowed_{school_name}.json", borrowed)
                save_data(f"books_{school_name}.json", books)
                st.success(f"Issued {issued_count} books!")

def render_individual_lending():
    st.subheader("👤 Individual Book Lending")
    
    school_name = st.session_state.school['name']
    books = load_data(f"books_{school_name}.json", [])
    
    with st.form("individual_lend"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Student Name")
            adm = st.text_input("Admission Number")
            form = st.text_input("Form/Class")
        with col2:
            stream = st.text_input("Stream")
            selected_book = st.selectbox("Book", [b['title'] for b in books if b.get('quantity', 0) > 0])
            book_no = st.text_input("Book Number")
        
        col3, col4 = st.columns(2)
        with col3:
            borrow_date = st.date_input("Borrow Date", datetime.now())
        with col4:
            return_date = st.date_input("Return Date", datetime.now() + timedelta(days=14))
        
        if st.form_submit_button("📖 Lend Book", use_container_width=True):
            if name and selected_book and book_no:
                borrowed = load_data(f"borrowed_{school_name}.json", [])
                book = next((b for b in books if b['title'] == selected_book), None)
                
                if book and book['quantity'] > 0:
                    borrowed.append({
                        "name": name,
                        "adm": adm,
                        "form": form,
                        "stream": stream,
                        "bookTitle": selected_book,
                        "bookNo": book_no,
                        "borrowDate": borrow_date.strftime('%Y-%m-%d'),
                        "returnDate": return_date.strftime('%Y-%m-%d'),
                        "returned": False,
                        "id": generate_code("BOR")
                    })
                    book['quantity'] -= 1
                    save_data(f"borrowed_{school_name}.json", borrowed)
                    save_data(f"books_{school_name}.json", books)
                    st.success("Book lent successfully!")
                else:
                    st.error("Book not available!")

def render_furniture():
    st.subheader("🪑 Furniture Allocation")
    
    school_name = st.session_state.school['name']
    classes = load_data(f"classes_{school_name}.json", [])
    
    selected_class = st.selectbox("Select Class", [c['name'] for c in classes])
    
    col1, col2 = st.columns(2)
    with col1:
        chair_prefix = st.text_input("Chair Number Prefix", "CH-")
        chair_start = st.number_input("Chair Start Number", 1, 1000, 1)
        chair_end = st.number_input("Chair End Number", 1, 1000, 10)
    with col2:
        locker_prefix = st.text_input("Locker Number Prefix", "LK-")
        locker_start = st.number_input("Locker Start Number", 1, 1000, 1)
        locker_end = st.number_input("Locker End Number", 1, 1000, 10)
    
    if st.button("📋 Load Class for Allocation", use_container_width=True):
        class_data = next((c for c in classes if c['name'] == selected_class), None)
        if class_data:
            furniture = load_data(f"furniture_{school_name}.json", [])
            st.session_state.furniture_data = {
                "students": class_data.get('students', []),
                "chair_range": list(range(chair_start, chair_end + 1)),
                "locker_range": list(range(locker_start, locker_end + 1))
            }
            st.success(f"Loaded {len(class_data.get('students', []))} students")
    
    if 'furniture_data' in st.session_state:
        students = st.session_state.furniture_data['students']
        if students:
            df = pd.DataFrame(students)
            df['Chair No'] = ""
            df['Locker No'] = ""
            df['Allocate'] = False
            
            edited_df = st.data_editor(df, use_container_width=True)
            
            if st.button("✅ Allocate Furniture", use_container_width=True):
                allocated = 0
                furniture = load_data(f"furniture_{school_name}.json", [])
                
                for idx, row in edited_df.iterrows():
                    if row['Allocate']:
                        furniture.append({
                            "name": row['name'],
                            "adm": row.get('adm', ''),
                            "chair": f"{chair_prefix}{row['Chair No']}" if row['Chair No'] else "",
                            "locker": f"{locker_prefix}{row['Locker No']}" if row['Locker No'] else "",
                            "date": datetime.now().strftime('%Y-%m-%d'),
                            "returned": False,
                            "id": generate_code("FUR")
                        })
                        allocated += 1
                
                save_data(f"furniture_{school_name}.json", furniture)
                st.success(f"Allocated furniture to {allocated} students!")

def render_returns():
    st.subheader("↩️ Return Items")
    
    school_name = st.session_state.school['name']
    search = st.text_input("🔍 Search by name, admission number, or book number")
    
    if st.button("Search", use_container_width=True):
        borrowed = load_data(f"borrowed_{school_name}.json", [])
        furniture = load_data(f"furniture_{school_name}.json", [])
        
        # Search in borrowed books
        active_borrowed = [b for b in borrowed if not b.get('returned') 
                          and (search.lower() in b.get('name', '').lower() 
                               or search in b.get('adm', '') 
                               or search in b.get('bookNo', ''))]
        
        # Search in furniture
        active_furniture = [f for f in furniture if not f.get('returned')
                           and (search.lower() in f.get('name', '').lower()
                                or search in f.get('adm', '')
                                or search in f.get('chair', '')
                                or search in f.get('locker', ''))]
        
        st.subheader("📚 Books")
        if active_borrowed:
            for item in active_borrowed:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"{item['name']} - {item['bookTitle']} (#{item['bookNo']})")
                with col2:
                    st.write(f"Due: {item['returnDate']}")
                with col3:
                    if st.button("Return", key=f"ret_book_{item['id']}"):
                        item['returned'] = True
                        books = load_data(f"books_{school_name}.json", [])
                        book = next((b for b in books if b['title'] == item['bookTitle']), None)
                        if book:
                            book['quantity'] += 1
                        save_data(f"books_{school_name}.json", books)
                        save_data(f"borrowed_{school_name}.json", borrowed)
                        st.success("Book returned!")
                        st.rerun()
        else:
            st.info("No matching borrowed books")
        
        st.subheader("🪑 Furniture")
        if active_furniture:
            for item in active_furniture:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"{item['name']} - Chair: {item.get('chair', '-')}, Locker: {item.get('locker', '-')}")
                with col2:
                    st.write(f"Date: {item['date']}")
                with col3:
                    if st.button("Return", key=f"ret_fur_{item['id']}"):
                        item['returned'] = True
                        save_data(f"furniture_{school_name}.json", furniture)
                        st.success("Furniture returned!")
                        st.rerun()
        else:
            st.info("No matching furniture allocations")

def render_borrowed():
    st.subheader("📋 Borrowed Books")
    
    school_name = st.session_state.school['name']
    borrowed = load_data(f"borrowed_{school_name}.json", [])
    
    filter_option = st.radio("Filter", ["All", "Active", "Overdue"], horizontal=True)
    
    today = datetime.now()
    
    if filter_option == "Active":
        filtered = [b for b in borrowed if not b.get('returned', False)]
    elif filter_option == "Overdue":
        filtered = [b for b in borrowed if not b.get('returned', False) 
                   and datetime.strptime(b.get('returnDate', '2000-01-01'), '%Y-%m-%d') < today]
    else:
        filtered = borrowed
    
    if filtered:
        df = pd.DataFrame(filtered)
        st.dataframe(df, use_container_width=True)
        
        if st.button("📎 Export to Excel", use_container_width=True):
            # Convert to Excel and download
            towrite = BytesIO()
            df.to_excel(towrite, index=False)
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="borrowed_books.xlsx">Download Excel File</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.info("No records found")

def render_members():
    st.subheader("👥 Members")
    
    school_name = st.session_state.school['name']
    members = load_data(f"members_{school_name}.json", [])
    
    with st.form("add_member"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
        with col2:
            member_id = st.text_input("ID")
        
        if st.form_submit_button("➕ Add Member", use_container_width=True):
            if name:
                members.append({"name": name, "id": member_id or generate_code("MEM")})
                save_data(f"members_{school_name}.json", members)
                st.success("Member added!")
                st.rerun()
    
    if members:
        for i, member in enumerate(members):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{member['name']}**")
                if member.get('id'):
                    st.write(f"ID: {member['id']}")
            with col2:
                if st.button("✏️ Edit", key=f"edit_mem_{i}"):
                    new_name = st.text_input("New name", member['name'], key=f"edit_name_{i}")
                    if st.button("Save", key=f"save_mem_{i}"):
                        members[i]['name'] = new_name
                        save_data(f"members_{school_name}.json", members)
                        st.rerun()
            with col3:
                if st.button("🗑️ Delete", key=f"del_mem_{i}"):
                    members.pop(i)
                    save_data(f"members_{school_name}.json", members)
                    st.rerun()
            st.divider()

def render_catalog():
    st.subheader("📚 Book Catalog")
    
    school_name = st.session_state.school['name']
    books = load_data(f"books_{school_name}.json", [])
    
    with st.form("add_book"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            title = st.text_input("Book Title")
        with col2:
            book_type = st.selectbox("Type", ["Textbook", "Novel", "Reference"])
        with col3:
            quantity = st.number_input("Quantity", 1, 1000, 1)
        
        if st.form_submit_button("📖 Add Book", use_container_width=True):
            if title:
                books.append({"title": title, "type": book_type, "quantity": quantity})
                save_data(f"books_{school_name}.json", books)
                st.success("Book added!")
                st.rerun()
    
    if books:
        for i, book in enumerate(books):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"📖 **{book['title']}**")
            with col2:
                st.write(f"Type: {book['type']}")
            with col3:
                st.write(f"Qty: {book['quantity']}")
            with col4:
                if st.button("🗑️", key=f"del_book_{i}"):
                    books.pop(i)
                    save_data(f"books_{school_name}.json", books)
                    st.rerun()
            st.divider()
    else:
        st.info("No books in catalog")

def render_teachers():
    st.subheader("👨‍🏫 Teachers")
    
    school_name = st.session_state.school['name']
    teachers = load_data(f"teachers_{school_name}.json", [])
    
    with st.form("add_teacher"):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Name")
        with col2:
            subjects = st.text_input("Subjects")
        with col3:
            class_assigned = st.text_input("Class Assigned")
        
        if st.form_submit_button("➕ Add Teacher", use_container_width=True):
            if name:
                teachers.append({
                    "name": name,
                    "subjects": subjects,
                    "class_assigned": class_assigned,
                    "id": generate_code("TCH")
                })
                save_data(f"teachers_{school_name}.json", teachers)
                st.success("Teacher added!")
                st.rerun()
    
    if teachers:
        df = pd.DataFrame(teachers)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No teachers added")

def render_classes():
    st.subheader("📋 Class Lists")
    
    school_name = st.session_state.school['name']
    classes = load_data(f"classes_{school_name}.json", [])
    
    # Import from Excel
    uploaded_file = st.file_uploader("📥 Import Class List (Excel)", type=['xlsx', 'xls'])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("Preview:")
        st.dataframe(df.head(), use_container_width=True)
        
        class_name = st.text_input("Save as Class Name")
        if st.button("💾 Save Class List", use_container_width=True):
            if class_name:
                students = df.to_dict('records')
                classes.append({
                    "name": class_name,
                    "students": students,
                    "created": datetime.now().strftime("%Y-%m-%d")
                })
                save_data(f"classes_{school_name}.json", classes)
                st.success(f"Saved class '{class_name}' with {len(students)} students!")
                st.rerun()
    
    if classes:
        for i, cls in enumerate(classes):
            with st.expander(f"📋 {cls['name']} ({len(cls.get('students', []))} students)"):
                if cls.get('students'):
                    st.dataframe(pd.DataFrame(cls['students']), use_container_width=True)
                if st.button("🗑️ Delete Class", key=f"del_cls_{i}"):
                    classes.pop(i)
                    save_data(f"classes_{school_name}.json", classes)
                    st.rerun()

def render_qr():
    st.subheader("📱 QR Codes")
    
    tab1, tab2 = st.tabs(["Generate QR", "Scan QR"])
    
    with tab1:
        qr_type = st.selectbox("QR Type", ["book", "chair", "locker"])
        col1, col2 = st.columns(2)
        with col1:
            start_num = st.number_input("Start Number", 1, 10000, 1)
        with col2:
            end_num = st.number_input("End Number", 1, 10000, 10)
        
        if st.button("Generate QR Codes", use_container_width=True):
            for i in range(start_num, end_num + 1):
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(f"{qr_type}-{i}")
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                st.image(f"data:image/png;base64,{img_str}", 
                        caption=f"{qr_type.upper()}: {i}", width=200)
    
    with tab2:
        st.info("📷 QR Scanner - Use your device camera to scan QR codes")
        st.write("This feature requires camera access. Use the mobile version for scanning.")
        qr_input = st.text_input("Or enter QR code manually")
        if qr_input:
            st.success(f"Scanned: {qr_input}")

def render_chat():
    st.subheader("💬 Staff Chat")
    
    school_name = st.session_state.school['name']
    user = st.session_state.user
    chat_messages = load_data(f"chat_messages_{school_name}.json", [])
    users = load_data(f"users_{school_name}.json", [])
    
    # Chat user selection
    other_users = [u for u in users if u['email'] != user['email']]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Staff")
        for u in other_users:
            if st.button(f"{u['name']} ({u['role']})", key=f"chat_user_{u['email']}", use_container_width=True):
                st.session_state.chat_with = u['email']
    
    with col2:
        if 'chat_with' in st.session_state:
            chat_with = st.session_state.chat_with
            chat_user = next((u for u in users if u['email'] == chat_with), None)
            
            if chat_user:
                st.subheader(f"Chat with {chat_user['name']}")
                
                # Display messages
                msgs = [m for m in chat_messages 
                       if (m['from'] == user['email'] and m['to'] == chat_with) 
                       or (m['from'] == chat_with and m['to'] == user['email'])]
                
                for msg in sorted(msgs, key=lambda x: x['timestamp']):
                    is_mine = msg['from'] == user['email']
                    align = "right" if is_mine else "left"
                    bg_color = "rgba(233,69,96,0.4)" if is_mine else "rgba(255,255,255,0.1)"
                    
                    st.markdown(f"""
                    <div style="text-align: {align}; margin: 10px 0;">
                        <div style="display: inline-block; background: {bg_color}; 
                             padding: 10px 15px; border-radius: 15px; color: white; max-width: 70%;">
                            <strong>{msg['from_name']}:</strong> {msg['message']}
                            <br><small style="color: rgba(255,255,255,0.5);">{msg['timestamp'][:16]}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Send message
                with st.form("send_message", clear_on_submit=True):
                    msg_text = st.text_input("Type a message...", key="chat_input")
                    if st.form_submit_button("📤 Send", use_container_width=True):
                        if msg_text:
                            chat_messages.append({
                                "from": user['email'],
                                "from_name": user['name'],
                                "to": chat_with,
                                "message": msg_text,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "id": generate_code("MSG")
                            })
                            save_data(f"chat_messages_{school_name}.json", chat_messages)
                            st.rerun()

def render_audit_log():
    st.subheader("📝 Audit Log")
    
    school_name = st.session_state.school['name']
    audit_log = load_data(f"audit_log_{school_name}.json", [])
    
    if audit_log:
        df = pd.DataFrame(audit_log)
        st.dataframe(df, use_container_width=True)
        
        if st.button("📎 Export Log", use_container_width=True):
            towrite = BytesIO()
            df.to_excel(towrite, index=False)
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="audit_log.xlsx">Download Excel File</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.info("No audit log entries")

def render_reports():
    st.subheader("📈 Reports")
    
    school_name = st.session_state.school['name']
    
    report_type = st.selectbox("Report Type", ["Books", "Furniture", "Overdue", "Complete Summary"])
    
    if st.button("📊 Generate Report", use_container_width=True):
        if report_type == "Books":
            borrowed = load_data(f"borrowed_{school_name}.json", [])
            df = pd.DataFrame(borrowed)
            st.dataframe(df, use_container_width=True)
            
        elif report_type == "Furniture":
            furniture = load_data(f"furniture_{school_name}.json", [])
            df = pd.DataFrame(furniture)
            st.dataframe(df, use_container_width=True)
            
        elif report_type == "Overdue":
            borrowed = load_data(f"borrowed_{school_name}.json", [])
            today = datetime.now()
            overdue = [b for b in borrowed if not b.get('returned', False) 
                      and datetime.strptime(b.get('returnDate', '2000-01-01'), '%Y-%m-%d') < today]
            df = pd.DataFrame(overdue)
            st.dataframe(df, use_container_width=True)
            
        elif report_type == "Complete Summary":
            books = load_data(f"books_{school_name}.json", [])
            borrowed = load_data(f"borrowed_{school_name}.json", [])
            members = load_data(f"members_{school_name}.json", [])
            teachers = load_data(f"teachers_{school_name}.json", [])
            furniture = load_data(f"furniture_{school_name}.json", [])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Books", sum(b.get('quantity', 0) for b in books))
                st.metric("Active Loans", len([b for b in borrowed if not b.get('returned')]))
            with col2:
                st.metric("Members", len(members))
                st.metric("Teachers", len(teachers))
            with col3:
                st.metric("Furniture Items", len([f for f in furniture if not f.get('returned')]))

def render_settings():
    st.subheader("⚙️ Settings")
    
    tab1, tab2 = st.tabs(["Data Management", "School Info"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Backup All Data", use_container_width=True):
                school_name = st.session_state.school['name']
                all_data = {}
                for file in ["books", "members", "borrowed", "teachers", "classes", 
                           "furniture", "book_issues", "individual_lendings", 
                           "audit_log", "chat_messages"]:
                    all_data[file] = load_data(f"{file}_{school_name}.json", [])
                
                json_str = json.dumps(all_data, indent=2)
                b64 = base64.b64encode(json_str.encode()).decode()
                href = f'<a href="data:application/json;base64,{b64}" download="srms_backup_{datetime.now().strftime("%Y%m%d")}.json">Download Backup</a>'
                st.markdown(href, unsafe_allow_html=True)
        
        with col2:
            uploaded = st.file_uploader("📤 Restore Data", type=['json'])
            if uploaded:
                if st.button("Restore", use_container_width=True):
                    data = json.load(uploaded)
                    school_name = st.session_state.school['name']
                    for file, file_data in data.items():
                        save_data(f"{file}_{school_name}.json", file_data)
                    st.success("Data restored!")
                    st.rerun()
        
        with col3:
            if st.button("⚠️ Clear All Data", use_container_width=True, type="primary"):
                confirm = st.text_input("Type 'DELETE' to confirm")
                if confirm == "DELETE":
                    school_name = st.session_state.school['name']
                    for file in ["books", "members", "borrowed", "teachers", "classes", 
                               "furniture", "book_issues", "individual_lendings"]:
                        save_data(f"{file}_{school_name}.json", [])
                    st.warning("All data cleared!")
    
    with tab2:
        school = st.session_state.school
        st.write(f"**School Name:** {school['name']}")
        st.write(f"**Address:** {school.get('address', 'N/A')}")
        st.write(f"**Admin:** {school['admin_name']}")
        st.write(f"**Email:** {school['admin_email']}")
        if school.get('admin_phone'):
            st.write(f"**Phone:** {school['admin_phone']}")
        st.write(f"**Invite Code:** {school['invite_code']}")
        st.write(f"**Created:** {school['created']}")

# ============== MAIN APP ==============
def main():
    if st.session_state.page == 'startup':
        startup_page()
    elif st.session_state.page == 'dashboard':
        dashboard_page()

if __name__ == "__main__":
    main()
