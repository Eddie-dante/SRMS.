# app.py - SRMS - School Resource Management System by WeGEM
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

# ============ WALLPAPERS ============
WALLPAPERS = {
    "None": "",
    "Abstract Waves": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1920",
    "Geometric Pattern": "https://images.unsplash.com/photo-1557683311-eac922347aa1?w=1920",
    "Nature Leaves": "https://images.unsplash.com/photo-1557683316-973673baf926?w=1920",
    "Starry Night": "https://images.unsplash.com/photo-1557683320-2d5001d5e9c5?w=1920",
    "Forest": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920",
    "Mountains": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920",
    "Ocean": "https://images.unsplash.com/photo-1507525425510-56b1e2d6c4f2?w=1920",
    "Desert": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920",
    "City Lights": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1920",
    "Aurora": "https://images.unsplash.com/photo-1483347756197-71ef80e95f73?w=1920",
    "Galaxy": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920",
    "Sunset": "https://images.unsplash.com/photo-1506815444479-bfdb1e96c566?w=1920",
    "Library": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1920",
    "Classroom": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920",
    "School Building": "https://images.unsplash.com/photo-1577896851231-70ef18881754?w=1920",
}

def get_premium_css(wallpaper=None):
    wallpaper_url = WALLPAPERS.get(wallpaper, "")
    bg_style = f"background-image: url('{wallpaper_url}'); background-size: cover; background-position: center; background-attachment: fixed;" if wallpaper_url else "background: linear-gradient(135deg, #0a0e27, #1a1f4e, #0f3460);"
    
    return f"""
    <style>
        .stApp {{ {bg_style} }}
        
        .stApp > header {{
            background: rgba(10, 14, 39, 0.85) !important;
            backdrop-filter: blur(30px) !important;
            border-bottom: 2px solid rgba(212, 175, 55, 0.3) !important;
        }}
        
        .main .block-container {{
            background: rgba(10, 14, 39, 0.5) !important;
            backdrop-filter: blur(25px) !important;
            border-radius: 20px !important;
            padding: 2rem !important;
            margin: 1rem !important;
            border: 1px solid rgba(212, 175, 55, 0.2) !important;
        }}
        
        /* SIDEBAR - DARK WITH VISIBLE TEXT */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0a0e27 0%, #1a1f4e 50%, #0f3460 100%) !important;
        }}
        
        section[data-testid="stSidebar"] > div {{
            background: rgba(0, 0, 0, 0.4) !important;
            padding: 1rem !important;
        }}
        
        /* ALL SIDEBAR TEXT - WHITE */
        section[data-testid="stSidebar"] * {{
            color: #FFFFFF !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5) !important;
        }}
        
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] .stMarkdown {{
            color: #FFFFFF !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5) !important;
        }}
        
        /* SIDEBAR BUTTONS */
        section[data-testid="stSidebar"] .stButton button {{
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
            color: #FFFFFF !important;
            text-align: left !important;
            padding: 10px 15px !important;
            margin: 2px 0 !important;
            font-size: 0.9rem !important;
            box-shadow: none !important;
        }}
        
        section[data-testid="stSidebar"] .stButton button:hover {{
            background: rgba(233, 69, 96, 0.4) !important;
            border-color: rgba(233, 69, 96, 0.6) !important;
        }}
        
        /* SIDEBAR EXPANDER */
        section[data-testid="stSidebar"] .streamlit-expanderHeader {{
            background: rgba(212, 175, 55, 0.2) !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
            color: #FFD700 !important;
            font-weight: 700 !important;
        }}
        
        section[data-testid="stSidebar"] .streamlit-expanderContent {{
            background: rgba(0, 0, 0, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }}
        
        /* SIDEBAR SELECTBOX */
        section[data-testid="stSidebar"] .stSelectbox > div > div {{
            background: rgba(255, 255, 255, 0.15) !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
        }}
        
        section[data-testid="stSidebar"] [data-baseweb="select"] * {{
            color: #FFFFFF !important;
        }}
        
        /* MAIN CONTENT TEXT */
        .main .block-container h1,
        .main .block-container h2,
        .main .block-container h3,
        .main .block-container h4 {{
            color: #FFFFFF !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6) !important;
        }}
        
        .main .block-container p,
        .main .block-container span,
        .main .block-container label {{
            color: #FFFFFF !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5) !important;
        }}
        
        /* GLASS CARDS */
        .glass-card {{
            background: rgba(255, 255, 255, 0.12) !important;
            backdrop-filter: blur(20px) !important;
            border-radius: 16px !important;
            padding: 25px !important;
            margin: 15px 0 !important;
            border: 1px solid rgba(212, 175, 55, 0.25) !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3) !important;
        }}
        
        /* STAT CARDS */
        .stat-card {{
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(15px) !important;
            padding: 25px !important;
            border-radius: 16px !important;
            border-left: 4px solid #e94560 !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            text-align: center !important;
            margin: 8px 0 !important;
        }}
        
        .stat-value {{
            font-size: 2.5em !important;
            font-weight: 900 !important;
            color: #FFFFFF !important;
        }}
        
        .stat-label {{
            color: rgba(255, 255, 255, 0.75) !important;
            font-size: 0.9em !important;
            font-weight: 600 !important;
        }}
        
        /* FORM INPUTS - WHITE BACKGROUND */
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stDateInput input {{
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px solid rgba(212, 175, 55, 0.4) !important;
            border-radius: 10px !important;
            padding: 10px 15px !important;
            color: #1a1a1a !important;
            font-weight: 500 !important;
        }}
        
        .stTextInput input::placeholder {{
            color: #999 !important;
        }}
        
        .stSelectbox > div > div {{
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px solid rgba(212, 175, 55, 0.4) !important;
            border-radius: 10px !important;
        }}
        
        .stSelectbox [data-baseweb="select"] * {{
            color: #1a1a1a !important;
        }}
        
        /* BUTTONS */
        .stButton button {{
            background: linear-gradient(135deg, #e94560, #c62a47) !important;
            border: none !important;
            border-radius: 10px !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3) !important;
        }}
        
        .stButton button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(233, 69, 96, 0.5) !important;
        }}
        
        /* TABLES */
        .stDataFrame {{
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(15px) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
        }}
        
        .stDataFrame th {{
            background: rgba(233, 69, 96, 0.8) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }}
        
        .stDataFrame td {{
            background: rgba(255, 255, 255, 0.05) !important;
            color: #FFFFFF !important;
        }}
        
        /* SCHOOL CODE BANNER */
        .school-code-banner {{
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            border: 2px dashed rgba(233, 69, 96, 0.4) !important;
            border-radius: 16px !important;
            padding: 25px !important;
            text-align: center !important;
        }}
        
        .invite-code {{
            font-family: 'Courier New', monospace !important;
            font-size: 2.5em !important;
            font-weight: 800 !important;
            letter-spacing: 8px !important;
            color: #FFFFFF !important;
        }}
        
        /* TABS */
        .stTabs [data-baseweb="tab-list"] {{
            background: rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 4px !important;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: rgba(255, 255, 255, 0.7) !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: #e94560 !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
        }}
        
        /* FOOTER */
        footer {{
            background: rgba(0, 0, 0, 0.3) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
            color: rgba(255, 255, 255, 0.6) !important;
        }}
        
        @media (max-width: 768px) {{
            .main .block-container {{
                padding: 1rem !important;
                margin: 0.5rem !important;
            }}
        }}
    </style>
    """

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'school' not in st.session_state:
    st.session_state.school = None
if 'page' not in st.session_state:
    st.session_state.page = 'startup'
if 'wallpaper' not in st.session_state:
    st.session_state.wallpaper = "Galaxy"
if 'current_section' not in st.session_state:
    st.session_state.current_section = 'dashboard'
if 'action' not in st.session_state:
    st.session_state.action = None

st.markdown(get_premium_css(st.session_state.wallpaper), unsafe_allow_html=True)

DATA_DIR = Path("srms_data")
DATA_DIR.mkdir(exist_ok=True)

def load_data(filename, default=None):
    if default is None:
        default = {}
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, 'r') as f:
            return json.load(f)
    return default

def save_data(filename, data):
    with open(DATA_DIR / filename, 'w') as f:
        json.dump(data, f, indent=2)

def generate_code(prefix="", length=8):
    chars = string.ascii_uppercase + string.digits
    return prefix + ''.join(random.choices(chars, k=length))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ============== STARTUP PAGE ==============
def startup_page():
    st.markdown("""
    <div class="glass-card" style="text-align: center; max-width: 600px; margin: 50px auto;">
        <div style="width: 160px; height: 160px; background: linear-gradient(135deg, #d4af37, #f0d060, #d4af37); 
             border-radius: 35px; display: inline-flex; align-items: center; justify-content: center; 
             font-size: 55px; font-weight: 900; color: #0a0e27; margin-bottom: 20px;
             box-shadow: 0 20px 60px rgba(212, 175, 55, 0.4);">
            SRMS
        </div>
        <h1 style="font-size: 3.5em; background: linear-gradient(180deg, #f0d060, #d4af37, #b8941f); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0;">
            SRMS
        </h1>
        <p style="font-size: 1.4em; color: #FFFFFF; margin: 10px 0;">School Resource Management System</p>
        <p style="color: #d4af37; font-size: 1.1em;">by <span style="color: #f0d060; font-weight: 700;">WeGEM</span> (Edwin)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔑 Staff Login", use_container_width=True, key="btn_login"):
            st.session_state.action = 'login'
    with col2:
        if st.button("📝 Staff Sign Up", use_container_width=True, key="btn_signup"):
            st.session_state.action = 'signup'
    with col3:
        if st.button("🏫 Create School", use_container_width=True, key="btn_create"):
            st.session_state.action = 'create'
    
    if st.session_state.action:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if st.session_state.action == 'login':
            login_form()
        elif st.session_state.action == 'signup':
            signup_form()
        elif st.session_state.action == 'create':
            create_school_form()
        st.markdown('</div>', unsafe_allow_html=True)

def login_form():
    st.markdown('<h3 style="color:#FFFFFF;">🔐 Staff Login</h3>', unsafe_allow_html=True)
    with st.form("frm_login"):
        name = st.text_input("👤 Your Full Name", placeholder="Enter your registered name")
        school_name = st.text_input("🏢 School Name", placeholder="Enter school name")
        invite_code = st.text_input("🔑 Invite Code", placeholder="Enter invite code")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
        if st.form_submit_button("🔑 Login", use_container_width=True):
            schools = load_data("schools.json", {})
            school = schools.get(school_name)
            if not school:
                st.error("School not found!")
                return
            users = load_data(f"users_{school_name}.json", [])
            user = next((u for u in users if u['name'].lower() == name.lower() and u['code'] == invite_code.upper()), None)
            if not user or user['password'] != hash_password(password):
                st.error("Invalid credentials!")
                return
            st.session_state.user = user
            st.session_state.school = school
            st.session_state.page = 'dashboard'
            st.session_state.action = None
            st.rerun()

def signup_form():
    st.markdown('<h3 style="color:#FFFFFF;">📝 Staff Sign Up</h3>', unsafe_allow_html=True)
    with st.form("frm_signup"):
        name = st.text_input("👤 Full Name", placeholder="Your full name")
        email = st.text_input("📧 Email", placeholder="your@email.com")
        phone = st.text_input("📞 Phone", placeholder="+1234567890")
        school_name = st.text_input("🏢 School Name", placeholder="Your school name")
        invite_code = st.text_input("🔑 Invite Code", placeholder="From your admin")
        staff_id = st.text_input("👤 Staff ID (Optional)", placeholder="Employee ID")
        password = st.text_input("🔒 Create Password", type="password", placeholder="Min 6 characters")
        if st.form_submit_button("📝 Sign Up", use_container_width=True):
            schools = load_data("schools.json", {})
            school = schools.get(school_name)
            if not school:
                st.error("School not found!")
                return
            if school['invite_code'] != invite_code.upper():
                st.error("Invalid invite code!")
                return
            if len(password) < 6:
                st.error("Password min 6 chars!")
                return
            users = load_data(f"users_{school_name}.json", [])
            if any(u['email'] == email for u in users):
                st.error("Email already registered!")
                return
            new_user = {"name": name, "email": email, "phone": phone, "staff_id": staff_id, "code": invite_code.upper(),
                       "password": hash_password(password), "role": "teacher", "joined": datetime.now().strftime("%Y-%m-%d")}
            users.append(new_user)
            save_data(f"users_{school_name}.json", users)
            st.session_state.user = new_user
            st.session_state.school = school
            st.session_state.page = 'dashboard'
            st.session_state.action = None
            st.success("Registration successful!")
            st.rerun()

def create_school_form():
    st.markdown('<h3 style="color:#FFFFFF;">🏫 Create New School</h3>', unsafe_allow_html=True)
    with st.form("frm_create"):
        school_name = st.text_input("🏢 School Name", placeholder="e.g., Sunshine High School")
        address = st.text_input("📍 School Address", placeholder="School location")
        admin_name = st.text_input("👤 Admin Full Name", placeholder="Your full name")
        admin_email = st.text_input("📧 Admin Email", placeholder="admin@school.edu")
        admin_phone = st.text_input("📞 Admin Phone", placeholder="+1234567890")
        password = st.text_input("🔒 Password", type="password", placeholder="Min 8 characters")
        confirm = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter password")
        if st.form_submit_button("🚀 Create School", use_container_width=True):
            if password != confirm:
                st.error("Passwords don't match!")
                return
            if len(password) < 8:
                st.error("Password min 8 chars!")
                return
            schools = load_data("schools.json", {})
            if school_name in schools:
                st.error("School already exists!")
                return
            invite_code = generate_code()
            school = {"name": school_name, "address": address, "admin_name": admin_name, "admin_email": admin_email,
                     "admin_phone": admin_phone, "invite_code": invite_code, "created": datetime.now().strftime("%Y-%m-%d")}
            schools[school_name] = school
            save_data("schools.json", schools)
            admin_user = {"name": admin_name, "email": admin_email, "phone": admin_phone, "staff_id": "ADMIN-001",
                         "code": invite_code, "password": hash_password(password), "role": "admin",
                         "joined": datetime.now().strftime("%Y-%m-%d")}
            save_data(f"users_{school_name}.json", [admin_user])
            for file in ["books", "members", "borrowed", "teachers", "classes", "furniture", "audit_log", "chat_messages"]:
                save_data(f"{file}_{school_name}.json", [])
            st.session_state.user = admin_user
            st.session_state.school = school
            st.session_state.page = 'dashboard'
            st.session_state.action = None
            st.success(f"School created! Code: {invite_code}")
            st.rerun()

# ============== DASHBOARD ==============
def dashboard_page():
    school_name = st.session_state.school['name']
    user = st.session_state.user
    
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;margin-bottom:25px;">
        <h1 style="font-size:2.2em;">🏫 {school_name}</h1>
        <p style="font-size:1.1em;color:#FFFFFF;">👤 {user['name']} 
        <span style="background:{'#e94560' if user['role']=='admin' else '#0f3460'};color:#FFF;padding:4px 12px;border-radius:20px;font-size:0.8em;margin-left:10px;">{user['role'].upper()}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    if user['role'] == 'admin':
        st.markdown(f"""
        <div class="school-code-banner">
            <p style="color:#FFF;">🏫 School Invite Code - Share with Staff</p>
            <div class="invite-code">{st.session_state.school['invite_code']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # SIDEBAR
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center;padding:15px;background:rgba(255,255,255,0.08);border-radius:12px;margin-bottom:15px;border:1px solid rgba(212,175,55,0.3);">
            <div style="width:50px;height:50px;background:linear-gradient(135deg,#d4af37,#f0d060);border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:22px;font-weight:700;color:#0a0e27;margin-bottom:8px;">{user['name'][0].upper()}</div>
            <p style="color:#FFFFFF;font-weight:700;margin:3px 0;">{user['name']}</p>
            <p style="color:#d4af37;font-size:0.8em;margin:3px 0;">{user['role'].upper()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🎨 Theme", expanded=False):
            wallpaper = st.selectbox("Wallpaper", list(WALLPAPERS.keys()), index=list(WALLPAPERS.keys()).index(st.session_state.wallpaper), key="side_wp")
            if wallpaper != st.session_state.wallpaper:
                st.session_state.wallpaper = wallpaper
                st.rerun()
        
        st.markdown("---")
        
        # Navigation matching original HTML exactly
        with st.expander("📊 MAIN", expanded=True):
            if st.button("📊 Dashboard", use_container_width=True, key="nav_dash"):
                st.session_state.current_section = 'dashboard'
                st.rerun()
        
        with st.expander("📖 LIBRARY", expanded=False):
            if st.button("📖 Book Issuing", use_container_width=True, key="nav_book_issue"):
                st.session_state.current_section = 'bookIssuing'
                st.rerun()
            if st.button("👤 Lend Book", use_container_width=True, key="nav_lend"):
                st.session_state.current_section = 'individualLending'
                st.rerun()
            if st.button("↩️ Returns", use_container_width=True, key="nav_returns"):
                st.session_state.current_section = 'return'
                st.rerun()
            if st.button("📋 Borrowed", use_container_width=True, key="nav_borrowed"):
                st.session_state.current_section = 'borrowedLog'
                st.rerun()
            if st.button("📚 Catalog", use_container_width=True, key="nav_catalog"):
                st.session_state.current_section = 'bookCatalog'
                st.rerun()
        
        with st.expander("🪑 RESOURCES", expanded=False):
            if st.button("🪑 Furniture", use_container_width=True, key="nav_furniture"):
                st.session_state.current_section = 'furnitureAllocation'
                st.rerun()
            if st.button("📱 QR Codes", use_container_width=True, key="nav_qr"):
                st.session_state.current_section = 'qr'
                st.rerun()
        
        with st.expander("👥 PEOPLE", expanded=False):
            if st.button("👥 Members", use_container_width=True, key="nav_members"):
                st.session_state.current_section = 'memberManagement'
                st.rerun()
            if st.button("👨‍🏫 Teachers", use_container_width=True, key="nav_teachers"):
                st.session_state.current_section = 'teacherAllocation'
                st.rerun()
            if st.button("📋 Classes", use_container_width=True, key="nav_classes"):
                st.session_state.current_section = 'classListManager'
                st.rerun()
        
        with st.expander("💬 SOCIAL", expanded=False):
            if st.button("💬 Chat", use_container_width=True, key="nav_chat"):
                st.session_state.current_section = 'chat'
                st.rerun()
        
        with st.expander("📈 TOOLS", expanded=False):
            if st.button("🔍 Overview", use_container_width=True, key="nav_overview"):
                st.session_state.current_section = 'systemOverview'
                st.rerun()
            if st.button("📝 Log", use_container_width=True, key="nav_log"):
                st.session_state.current_section = 'auditLog'
                st.rerun()
            if st.button("📈 Reports", use_container_width=True, key="nav_reports"):
                st.session_state.current_section = 'reports'
                st.rerun()
        
        with st.expander("⚙️ SYSTEM", expanded=False):
            if st.button("⚙️ Settings", use_container_width=True, key="nav_settings"):
                st.session_state.current_section = 'settings'
                st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, key="nav_logout", type="primary"):
            st.session_state.user = None
            st.session_state.school = None
            st.session_state.page = 'startup'
            st.rerun()
        
        st.markdown('<p style="color:rgba(255,255,255,0.4);font-size:0.7em;text-align:center;">SRMS v6.0 | by WeGEM (Edwin) | © 2025</p>', unsafe_allow_html=True)
    
    # MAIN CONTENT
    section = st.session_state.current_section
    
    if section == 'dashboard':
        render_dashboard()
    elif section == 'bookIssuing':
        render_book_issuing()
    elif section == 'individualLending':
        render_individual_lending()
    elif section == 'furnitureAllocation':
        render_furniture()
    elif section == 'return':
        render_returns()
    elif section == 'borrowedLog':
        render_borrowed()
    elif section == 'memberManagement':
        render_members()
    elif section == 'bookCatalog':
        render_catalog()
    elif section == 'teacherAllocation':
        render_teachers()
    elif section == 'classListManager':
        render_classes()
    elif section == 'qr':
        render_qr()
    elif section == 'chat':
        render_chat()
    elif section == 'systemOverview':
        render_system_overview()
    elif section == 'auditLog':
        render_audit_log()
    elif section == 'reports':
        render_reports()
    elif section == 'settings':
        render_settings()

# ============ RENDER FUNCTIONS ============
def render_dashboard():
    st.markdown('<div class="glass-card"><h2>📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    books = load_data(f"books_{school_name}.json", [])
    borrowed = load_data(f"borrowed_{school_name}.json", [])
    members = load_data(f"members_{school_name}.json", [])
    teachers = load_data(f"teachers_{school_name}.json", [])
    furniture = load_data(f"furniture_{school_name}.json", [])
    
    total_books = sum(b.get('quantity', 0) for b in books)
    books_borrowed = len([b for b in borrowed if not b.get('returned')])
    overdue = len([b for b in borrowed if not b.get('returned') and datetime.strptime(b.get('returnDate', '2000-01-01'), '%Y-%m-%d') < datetime.now()])
    
    cols = st.columns(4)
    vals = [total_books, books_borrowed, total_books - books_borrowed, overdue]
    labels = ['Total Books', 'Books Borrowed', 'Books Available', 'Overdue']
    for i, (v, l) in enumerate(zip(vals, labels)):
        with cols[i]:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{v}</div><div class="stat-label">{l}</div></div>', unsafe_allow_html=True)
    
    cols2 = st.columns(4)
    vals2 = [len(members), len(teachers), len([f for f in furniture if not f.get('returned')]), len([b for b in borrowed if not b.get('returned')])]
    labels2 = ['Members', 'Teachers', 'Furniture Items', 'Active Loans']
    for i, (v, l) in enumerate(zip(vals2, labels2)):
        with cols2[i]:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{v}</div><div class="stat-label">{l}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_book_issuing():
    st.markdown('<div class="glass-card"><h2>📖 Bulk Book Issuing to Class</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    books = load_data(f"books_{school_name}.json", [])
    classes = load_data(f"classes_{school_name}.json", [])
    
    col1, col2 = st.columns(2)
    with col1:
        selected_book = st.selectbox("Book:", [b['title'] for b in books if b.get('quantity', 0) > 0], key="bi_book")
    with col2:
        selected_class = st.selectbox("Class:", [c['name'] for c in classes], key="bi_class")
    
    col3, col4 = st.columns(2)
    with col3:
        issue_date = st.date_input("Issue Date:", datetime.now(), key="bi_idate")
    with col4:
        return_date = st.date_input("Return Date:", datetime.now() + timedelta(days=14), key="bi_rdate")
    
    if st.button("📋 Load", use_container_width=True, key="bi_load"):
        class_data = next((c for c in classes if c['name'] == selected_class), None)
        if class_data:
            st.session_state.bi_students = class_data.get('students', [])
            st.success(f"Loaded {len(st.session_state.bi_students)} students!")
    
    if 'bi_students' in st.session_state:
        students = st.session_state.bi_students
        if students:
            df = pd.DataFrame(students)
            df['Book No'] = ""
            df['Issue'] = False
            edited = st.data_editor(df, use_container_width=True, key="bi_editor")
            if st.button("✅ Issue", use_container_width=True, key="bi_issue"):
                count = 0                borrowed = load_data(f"borrowed_{school_name}.json", [])
                for _, row in edited.iterrows():
                    if row['Issue'] and row['Book No']:
                        book = next((b for b in books if b['title'] == selected_book), None)
                        if book and book['quantity'] > 0:
                            borrowed.append({"name": row['name'], "adm": row.get('adm', ''), "bookTitle": selected_book,
                                           "bookNo": row['Book No'], "borrowDate": issue_date.strftime('%Y-%m-%d'),
                                           "returnDate": return_date.strftime('%Y-%m-%d'), "returned": False, "id": generate_code("BOR")})
                            book['quantity'] -= 1
                            count += 1
                save_data(f"borrowed_{school_name}.json", borrowed)
                save_data(f"books_{school_name}.json", books)
                st.success(f"Issued {count} books!")
    st.markdown('</div>', unsafe_allow_html=True)

def render_individual_lending():
    st.markdown('<div class="glass-card"><h2>👤 Individual Book Lending</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    books = load_data(f"books_{school_name}.json", [])
    
    with st.form("frm_ind_lend"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Name:", placeholder="Student name")
            adm = st.text_input("ADM:", placeholder="Admission number")
            form = st.text_input("Form:", placeholder="Class/Form")
        with c2:
            stream = st.text_input("Stream:", placeholder="Stream")
            selected_book = st.selectbox("Book:", [b['title'] for b in books if b.get('quantity', 0) > 0], key="il_book")
            book_no = st.text_input("Book No:", placeholder="Book number")
        c3, c4 = st.columns(2)
        with c3:
            borrow_date = st.date_input("Borrow Date:", datetime.now(), key="il_bd")
        with c4:
            return_date = st.date_input("Return Date:", datetime.now() + timedelta(days=14), key="il_rd")
        if st.form_submit_button("📖 Lend Book", use_container_width=True):
            if name and selected_book:
                borrowed = load_data(f"borrowed_{school_name}.json", [])
                book = next((b for b in books if b['title'] == selected_book), None)
                if book and book['quantity'] > 0:
                    borrowed.append({"name": name, "adm": adm, "form": form, "stream": stream, "bookTitle": selected_book,
                                   "bookNo": book_no, "borrowDate": borrow_date.strftime('%Y-%m-%d'),
                                   "returnDate": return_date.strftime('%Y-%m-%d'), "returned": False, "id": generate_code("BOR")})
                    book['quantity'] -= 1
                    save_data(f"borrowed_{school_name}.json", borrowed)
                    save_data(f"books_{school_name}.json", books)
                    st.success("Book lent!")
                else:
                    st.error("Book not available!")
    st.markdown('</div>', unsafe_allow_html=True)

def render_furniture():
    st.markdown('<div class="glass-card"><h2>🪑 Furniture Allocation</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    classes = load_data(f"classes_{school_name}.json", [])
    
    selected_class = st.selectbox("Class:", [c['name'] for c in classes], key="fur_class")
    c1, c2 = st.columns(2)
    with c1:
        chair_prefix = st.text_input("Chair Prefix:", "CH-")
        chair_start = st.number_input("Chair Start:", 1, 1000, 1, key="fur_cs")
        chair_end = st.number_input("Chair End:", 1, 1000, 10, key="fur_ce")
    with c2:
        locker_prefix = st.text_input("Locker Prefix:", "LK-")
        locker_start = st.number_input("Locker Start:", 1, 1000, 1, key="fur_ls")
        locker_end = st.number_input("Locker End:", 1, 1000, 10, key="fur_le")
    
    alloc_date = st.date_input("Date:", datetime.now(), key="fur_date")
    
    if st.button("📋 Load Class", use_container_width=True, key="fur_load"):
        class_data = next((c for c in classes if c['name'] == selected_class), None)
        if class_data:
            st.session_state.fur_students = class_data.get('students', [])
            st.success(f"Loaded {len(st.session_state.fur_students)} students!")
    
    if 'fur_students' in st.session_state:
        students = st.session_state.fur_students
        if students:
            df = pd.DataFrame(students)
            df['Chair No'] = ""
            df['Locker No'] = ""
            df['Allocate'] = False
            edited = st.data_editor(df, use_container_width=True, key="fur_editor")
            if st.button("✅ Assign", use_container_width=True, key="fur_assign"):
                count = 0
                furniture = load_data(f"furniture_{school_name}.json", [])
                for _, row in edited.iterrows():
                    if row['Allocate']:
                        furniture.append({"name": row['name'], "adm": row.get('adm', ''),
                                        "chair": f"{chair_prefix}{row['Chair No']}" if row['Chair No'] else "",
                                        "locker": f"{locker_prefix}{row['Locker No']}" if row['Locker No'] else "",
                                        "date": alloc_date.strftime('%Y-%m-%d'), "returned": False, "id": generate_code("FUR")})
                        count += 1
                save_data(f"furniture_{school_name}.json", furniture)
                st.success(f"Allocated {count} items!")
    st.markdown('</div>', unsafe_allow_html=True)

def render_returns():
    st.markdown('<div class="glass-card"><h2>↩️ Return Items</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    search = st.text_input("Search...", placeholder="Search by name, ADM, or item number", key="ret_search")
    if st.button("🔍 Search", use_container_width=True, key="ret_btn"):
        borrowed = load_data(f"borrowed_{school_name}.json", [])
        furniture = load_data(f"furniture_{school_name}.json", [])
        
        active_books = [b for b in borrowed if not b.get('returned') and (search.lower() in b.get('name', '').lower() or search in b.get('adm', '') or search in b.get('bookNo', ''))]
        active_furniture = [f for f in furniture if not f.get('returned') and (search.lower() in f.get('name', '').lower() or search in f.get('adm', '') or search in f.get('chair', '') or search in f.get('locker', ''))]
        
        st.markdown("### 📚 Books")
        if active_books:
            for item in active_books:
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.write(f"{item['name']} - {item['bookTitle']} (#{item['bookNo']})")
                with c2:
                    st.write(f"Due: {item['returnDate']}")
                with c3:
                    if st.button("Return", key=f"rb_{item['id']}"):
                        item['returned'] = True
                        books = load_data(f"books_{school_name}.json", [])
                        book = next((b for b in books if b['title'] == item['bookTitle']), None)
                        if book:
                            book['quantity'] += 1
                        save_data(f"books_{school_name}.json", books)
                        save_data(f"borrowed_{school_name}.json", borrowed)
                        st.success("Returned!")
                        st.rerun()
        else:
            st.info("No matching books")
        
        st.markdown("### 🪑 Furniture")
        if active_furniture:
            for item in active_furniture:
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.write(f"{item['name']} - Chair: {item.get('chair', '-')}, Locker: {item.get('locker', '-')}")
                with c2:
                    st.write(f"Date: {item['date']}")
                with c3:
                    if st.button("Return", key=f"rf_{item['id']}"):
                        item['returned'] = True
                        save_data(f"furniture_{school_name}.json", furniture)
                        st.success("Returned!")
                        st.rerun()
        else:
            st.info("No matching furniture")
    st.markdown('</div>', unsafe_allow_html=True)

def render_borrowed():
    st.markdown('<div class="glass-card"><h2>📋 Borrowed Books</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    borrowed = load_data(f"borrowed_{school_name}.json", [])
    filt = st.radio("Filter:", ["All", "Active", "Overdue"], horizontal=True, key="bor_filt")
    today = datetime.now()
    
    if filt == "Active":
        filtered = [b for b in borrowed if not b.get('returned')]
    elif filt == "Overdue":
        filtered = [b for b in borrowed if not b.get('returned') and datetime.strptime(b.get('returnDate', '2000-01-01'), '%Y-%m-%d') < today]
    else:
        filtered = borrowed
    
    if filtered:
        st.dataframe(pd.DataFrame(filtered), use_container_width=True)
        if st.button("📎 Export", use_container_width=True, key="bor_exp"):
            towrite = BytesIO()
            pd.DataFrame(filtered).to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="borrowed.xlsx">📥 Download</a>', unsafe_allow_html=True)
    else:
        st.info("No records")
    st.markdown('</div>', unsafe_allow_html=True)

def render_members():
    st.markdown('<div class="glass-card"><h2>👥 Members</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    members = load_data(f"members_{school_name}.json", [])
    
    with st.form("frm_member"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Name:", placeholder="Member name")
        with c2:
            mid = st.text_input("ID:", placeholder="Member ID")
        if st.form_submit_button("➕ Add", use_container_width=True):
            if name:
                members.append({"name": name, "id": mid or generate_code("MEM")})
                save_data(f"members_{school_name}.json", members)
                st.success("Added!")
                st.rerun()
    
    search = st.text_input("Search...", placeholder="Search members", key="mem_search")
    filtered = [m for m in members if not search or search.lower() in m['name'].lower() or search in m.get('id', '')]
    for i, m in enumerate(filtered):
        c1, c2 = st.columns([4, 1])
        with c1:
            st.write(f"**{m['name']}** {f'({m["id"]})' if m.get('id') else ''}")
        with c2:
            if st.button("🗑️", key=f"del_mem_{i}"):
                members.remove(m)
                save_data(f"members_{school_name}.json", members)
                st.rerun()
        st.divider()
    st.markdown('</div>', unsafe_allow_html=True)

def render_catalog():
    st.markdown('<div class="glass-card"><h2>📚 Catalog</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    books = load_data(f"books_{school_name}.json", [])
    
    with st.form("frm_book"):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            title = st.text_input("Title:", placeholder="Book title")
        with c2:
            btype = st.selectbox("Type:", ["Textbook", "Novel", "Reference"], key="cat_type")
        with c3:
            qty = st.number_input("Qty:", 1, 1000, 1, key="cat_qty")
        if st.form_submit_button("📖 Add Book", use_container_width=True):
            if title:
                books.append({"title": title, "type": btype, "quantity": qty})
                save_data(f"books_{school_name}.json", books)
                st.success("Added!")
                st.rerun()
    
    for i, b in enumerate(books):
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        with c1:
            st.write(f"📖 **{b['title']}**")
        with c2:
            st.write(b['type'])
        with c3:
            st.write(f"Qty: {b['quantity']}")
        with c4:
            if st.button("🗑️", key=f"del_book_{i}"):
                books.pop(i)
                save_data(f"books_{school_name}.json", books)
                st.rerun()
        st.divider()
    st.markdown('</div>', unsafe_allow_html=True)

def render_teachers():
    st.markdown('<div class="glass-card"><h2>👨‍🏫 Teachers</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    teachers = load_data(f"teachers_{school_name}.json", [])
    
    with st.form("frm_teacher"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            name = st.text_input("Name:", placeholder="Teacher name")
        with c2:
            subject = st.text_input("Subjects:", placeholder="Subjects")
        with c3:
            classes = st.text_input("Classes:", placeholder="Classes")
        with c4:
            duty = st.text_input("Class Assigned:", placeholder="Class")
        if st.form_submit_button("➕ Add", use_container_width=True):
            if name:
                teachers.append({"name": name, "subject": subject, "classes": classes, "duty": duty})
                save_data(f"teachers_{school_name}.json", teachers)
                st.success("Added!")
                st.rerun()
    
    if teachers:
        for i, t in enumerate(teachers):
            c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 1, 1])
            with c1:
                st.write(f"**{t['name']}**")
            with c2:
                st.write(t.get('subject', '-'))
            with c3:
                st.write(t.get('duty', '-'))
            with c4:
                st.write(t.get('classes', '-'))
            with c5:
                if st.button("🗑️", key=f"del_tea_{i}"):
                    teachers.pop(i)
                    save_data(f"teachers_{school_name}.json", teachers)
                    st.rerun()
            st.divider()
    st.markdown('</div>', unsafe_allow_html=True)

def render_classes():
    st.markdown('<div class="glass-card"><h2>📋 Class Lists</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    classes = load_data(f"classes_{school_name}.json", [])
    
    uploaded = st.file_uploader("📥 Import Excel", type=['xlsx', 'xls'], key="cls_upload")
    if uploaded:
        df = pd.read_excel(uploaded)
        st.dataframe(df.head(), use_container_width=True)
        class_name = st.text_input("Class name:", placeholder="e.g., Grade 4A", key="cls_name")
        if st.button("💾 Save", use_container_width=True, key="cls_save"):
            if class_name:
                classes.append({"name": class_name, "students": df.to_dict('records'), "created": datetime.now().strftime("%Y-%m-%d")})
                save_data(f"classes_{school_name}.json", classes)
                st.success(f"Saved '{class_name}'!")
                st.rerun()
    
    if classes:
        st.markdown("### Saved Lists")
        for i, cls in enumerate(classes):
            with st.expander(f"📋 {cls['name']} ({len(cls.get('students', []))} students)"):
                if cls.get('students'):
                    st.dataframe(pd.DataFrame(cls['students']), use_container_width=True)
                if st.button("🗑️ Delete", key=f"del_cls_{i}"):
                    classes.pop(i)
                    save_data(f"classes_{school_name}.json", classes)
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_qr():
    st.markdown('<div class="glass-card"><h2>📱 QR Codes</h2>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["Generate", "Scan"])
    with t1:
        qr_type = st.selectbox("Type:", ["book", "chair", "locker"], key="qr_type")
        c1, c2 = st.columns(2)
        with c1:
            start = st.number_input("Start:", 1, 10000, 1, key="qr_start")
        with c2:
            end = st.number_input("End:", 1, 10000, 10, key="qr_end")
        if st.button("Generate", use_container_width=True, key="qr_gen"):
            cols = st.columns(4)
            for i in range(start, min(end + 1, start + 20)):
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(f"{qr_type}-{i}")
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buf = BytesIO()
                img.save(buf, format="PNG")
                b64 = base64.b64encode(buf.getvalue()).decode()
                with cols[(i - start) % 4]:
                    st.image(f"data:image/png;base64,{b64}", caption=f"{qr_type}:{i}", width=150)
    with t2:
        st.info("📷 Use device camera to scan QR codes")
        manual = st.text_input("Or enter code manually:", placeholder="e.g., book-5", key="qr_manual")
        if manual:
            st.success(f"Scanned: {manual}")
    st.markdown('</div>', unsafe_allow_html=True)

def render_chat():
    st.markdown('<div class="glass-card"><h2>💬 Staff Chat</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    user = st.session_state.user
    users = load_data(f"users_{school_name}.json", [])
    messages = load_data(f"chat_messages_{school_name}.json", [])
    
    other_users = [u for u in users if u['email'] != user['email']]
    
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown("### Staff Online")
        for u in other_users:
            if st.button(f"🟢 {u['name']} ({u['role']})", key=f"cu_{u['email']}", use_container_width=True):
                st.session_state.chat_with = u['email']
    
    with c2:
        if 'chat_with' in st.session_state:
            chat_with = st.session_state.chat_with
            chat_user = next((u for u in users if u['email'] == chat_with), None)
            if chat_user:
                st.markdown(f"### Chat with {chat_user['name']}")
                msgs = [m for m in messages if (m['from'] == user['email'] and m['to'] == chat_with) or (m['from'] == chat_with and m['to'] == user['email'])]
                for msg in sorted(msgs, key=lambda x: x['timestamp']):
                    is_mine = msg['from'] == user['email']
                    bg = "rgba(233,69,96,0.4)" if is_mine else "rgba(255,255,255,0.1)"
                    align = "flex-end" if is_mine else "flex-start"
                    st.markdown(f'<div style="display:flex;justify-content:{align};margin:8px 0;"><div style="background:{bg};padding:10px 16px;border-radius:16px;max-width:70%;color:#FFF;"><strong>{msg["from_name"]}:</strong> {msg["message"]}<br><small style="color:rgba(255,255,255,0.5);">{msg["timestamp"][:16]}</small></div></div>', unsafe_allow_html=True)
                
                with st.form("frm_chat", clear_on_submit=True):
                    msg_text = st.text_input("Type a message...", key="chat_input", placeholder="Write here...")
                    if st.form_submit_button("📤", use_container_width=True):
                        if msg_text:
                            messages.append({"from": user['email'], "from_name": user['name'], "to": chat_with, "message": msg_text,
                                           "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "id": generate_code("MSG")})
                            save_data(f"chat_messages_{school_name}.json", messages)
                            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_system_overview():
    st.markdown('<div class="glass-card"><h2>🔍 System Overview</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    books = load_data(f"books_{school_name}.json", [])
    borrowed = load_data(f"borrowed_{school_name}.json", [])
    members = load_data(f"members_{school_name}.json", [])
    teachers = load_data(f"teachers_{school_name}.json", [])
    furniture = load_data(f"furniture_{school_name}.json", [])
    users = load_data(f"users_{school_name}.json", [])
    classes = load_data(f"classes_{school_name}.json", [])
    messages = load_data(f"chat_messages_{school_name}.json", [])
    
    tb = sum(b.get('quantity', 0) for b in books)
    al = len([b for b in borrowed if not b.get('returned')])
    ov = len([b for b in borrowed if not b.get('returned') and datetime.strptime(b.get('returnDate', '2000-01-01'), '%Y-%m-%d') < datetime.now()])
    af = len([f for f in furniture if not f.get('returned')])
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat-card"><strong>🏫 School</strong><br>{st.session_state.school["name"]}<br>Admin: {st.session_state.school["admin_name"]}<br>Code: {st.session_state.school["invite_code"]}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><strong>📚 Books</strong><br>Total: {tb}<br>Active: {al}<br>Overdue: {ov}<br>Available: {tb - al}</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><strong>👥 People</strong><br>Staff: {len(users)}<br>Teachers: {len(teachers)}<br>Members: {len(members)}<br>Classes: {len(classes)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_audit_log():
    st.markdown('<div class="glass-card"><h2>📝 Audit Log</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    log = load_data(f"audit_log_{school_name}.json", [])
    if log:
        st.dataframe(pd.DataFrame(log), use_container_width=True)
        if st.button("📎 Export", use_container_width=True, key="log_exp"):
            towrite = BytesIO()
            pd.DataFrame(log).to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="audit_log.xlsx">📥 Download</a>', unsafe_allow_html=True)
    else:
        st.info("No entries")
    st.markdown('</div>', unsafe_allow_html=True)

def render_reports():
    st.markdown('<div class="glass-card"><h2>📈 Reports</h2>', unsafe_allow_html=True)
    school_name = st.session_state.school['name']
    report_type = st.selectbox("Report:", ["books", "furniture", "overdue", "complete"], key="rep_type")
    if st.button("📊 Generate", use_container_width=True, key="rep_gen"):
        if report_type == "books":
            data = load_data(f"borrowed_{school_name}.json", [])
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        elif report_type == "furniture":
            data = load_data(f"furniture_{school_name}.json", [])
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        elif report_type == "overdue":
            data = load_data(f"borrowed_{school_name}.json", [])
            overdue = [b for b in data if not b.get('returned') and datetime.strptime(b.get('returnDate', '2000-01-01'), '%Y-%m-%d') < datetime.now()]
            st.dataframe(pd.DataFrame(overdue), use_container_width=True) if overdue else st.success("No overdue!")
        else:
            borrowed = load_data(f"borrowed_{school_name}.json", [])
            st.write(f"Active: {len([b for b in borrowed if not b.get('returned')])} | Overdue: {len([b for b in borrowed if not b.get('returned') and datetime.strptime(b.get('returnDate', '2000-01-01'), '%Y-%m-%d') < datetime.now()])} | Teachers: {len(load_data(f'teachers_{school_name}.json', []))}")
    st.markdown('</div>', unsafe_allow_html=True)

def render_settings():
    st.markdown('<div class="glass-card"><h2>⚙️ Settings</h2>', unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["Theme", "Data", "Staff"])
    
    with t1:
        wp = st.selectbox("Wallpaper:", list(WALLPAPERS.keys()), index=list(WALLPAPERS.keys()).index(st.session_state.wallpaper), key="set_wp")
        if st.button("Apply", use_container_width=True, key="set_apply"):
            st.session_state.wallpaper = wp
            st.rerun()
        if wp != "None":
            st.image(WALLPAPERS[wp], width=400)
    
    with t2:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Backup", use_container_width=True, key="set_backup"):
                school_name = st.session_state.school['name']
                all_data = {}
                for f in ["books", "members", "borrowed", "teachers", "classes", "furniture", "audit_log", "chat_messages"]:
                    all_data[f] = load_data(f"{f}_{school_name}.json", [])
                b64 = base64.b64encode(json.dumps(all_data, indent=2).encode()).decode()
                st.markdown(f'<a href="data:application/json;base64,{b64}" download="srms_backup.json">📥 Download</a>', unsafe_allow_html=True)
        with col2:
            uploaded = st.file_uploader("Restore:", type=['json'], key="set_restore")
            if uploaded and st.button("📤 Restore", use_container_width=True, key="set_restore_btn"):
                data = json.load(uploaded)
                school_name = st.session_state.school['name']
                for f, fd in data.items():
                    save_data(f"{f}_{school_name}.json", fd)
                st.success("Restored!")
                st.rerun()
        with col3:
            if st.button("⚠️ Clear All", use_container_width=True, key="set_clear"):
                if st.text_input("Type DELETE:", key="set_del") == "DELETE":
                    school_name = st.session_state.school['name']
                    for f in ["books", "members", "borrowed", "teachers", "classes", "furniture"]:
                        save_data(f"{f}_{school_name}.json", [])
                    st.error("Cleared!")
                    st.rerun()
    
    with t3:
        with st.form("frm_staff"):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                email = st.text_input("Email:", placeholder="staff@school.edu")
            with c2:
                name = st.text_input("Name:", placeholder="Staff name")
            with c3:
                role = st.selectbox("Role:", ["teacher", "librarian", "admin"], key="set_role")
            with c4:
                pw = st.text_input("Password:", placeholder="Auto-generated", key="set_pw")
            if st.form_submit_button("➕ Create", use_container_width=True):
                if email and name:
                    users = load_data(f"users_{school_name}.json", [])
                    users.append({"name": name, "email": email, "role": role, "code": st.session_state.school['invite_code'],
                                 "password": hash_password(pw or generate_code("", 8)), "staff_id": f"{role.upper()}-{generate_code('', 4)}",
                                 "joined": datetime.now().strftime("%Y-%m-%d")})
                    save_data(f"users_{school_name}.json", users)
                    st.success(f"Created {role}!")
                    st.rerun()
        
        users = load_data(f"users_{school_name}.json", [])
        for i, u in enumerate(users):
            st.write(f"**{u['name']}** - {u['role']} - {u['email']}")
            if st.button("🗑️", key=f"del_staff_{i}"):
                users.pop(i)
                save_data(f"users_{school_name}.json", users)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ============== MAIN ==============
def main():
    if st.session_state.page == 'startup':
        startup_page()
    elif st.session_state.page == 'dashboard':
        dashboard_page()

if __name__ == "__main__":
    main()
