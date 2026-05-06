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

# ============ ENHANCED WALLPAPERS ============
WALLPAPERS = {
    "None": "",
    "Abstract Waves": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1920",
    "Geometric Pattern": "https://images.unsplash.com/photo-1557683311-eac922347aa1?w=1920",
    "Nature Leaves": "https://images.unsplash.com/photo-1557683316-973673baf926?w=1920",
    "Starry Night": "https://images.unsplash.com/photo-1557683320-2d5001d5e9c5?w=1920",
    "Color Splash": "https://images.unsplash.com/photo-1557683304-6733ba7e4d6f?w=1920",
    "Forest": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920",
    "Mountains": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920",
    "Ocean": "https://images.unsplash.com/photo-1507525425510-56b1e2d6c4f2?w=1920",
    "Desert": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920",
    "City Lights": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1920",
    "Aurora": "https://images.unsplash.com/photo-1483347756197-71ef80e95f73?w=1920",
    "Galaxy": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920",
    "Sunset": "https://images.unsplash.com/photo-1506815444479-bfdb1e96c566?w=1920",
    "Rainbow": "https://images.unsplash.com/photo-1511300636408-a63a89df3482?w=1920",
    "Clouds": "https://images.unsplash.com/photo-1501630834273-4b5604d2ee31?w=1920",
    "Stars": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920",
    "Library": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1920",
    "Classroom": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920",
    "School Building": "https://images.unsplash.com/photo-1577896851231-70ef18881754?w=1920",
    "Study Desk": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920",
    "Sunset Mountains": "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=1920",
    "Tropical Beach": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920",
    "Misty Forest": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920",
    "Mountain Lake": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920",
    "Night Sky": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920",
    "Purple Haze": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469?w=1920",
    "Green Valley": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920",
    "Autumn Road": "https://images.unsplash.com/photo-1507783548227-544c3b8fc065?w=1920",
    "Winter Snow": "https://images.unsplash.com/photo-1477601263568-180e2c6d046e?w=1920",
    "Spring Flowers": "https://images.unsplash.com/photo-1490750967868-88aa4cef14d0?w=1920",
    "Summer Field": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920",
    "Waterfall": "https://images.unsplash.com/photo-1544551763-46a013bb70b5?w=1920",
    "Canyon": "https://images.unsplash.com/photo-1474044159687-1ee9f3a51722?w=1920",
    "Lavender Field": "https://images.unsplash.com/photo-1499002238440-d264edd596ec?w=1920",
    "Cherry Blossom": "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1920",
    "Palm Trees": "https://images.unsplash.com/photo-1509233725247-49e657c54213?w=1920",
    "Foggy Morning": "https://images.unsplash.com/photo-1485230405346-71acb9518d9b?w=1920",
    "Golden Hour": "https://images.unsplash.com/photo-1501856777435-29877ed80a3d?w=1920",
    "Blue Lagoon": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1920",
    "Coral Reef": "https://images.unsplash.com/photo-1544551763-46a013bb70b5?w=1920",
    "Savanna": "https://images.unsplash.com/photo-1516426122078-c23e76319801?w=1920",
    "Iceberg": "https://images.unsplash.com/photo-1540979388789-7cee28a1cdc9?w=1920",
    "Volcano": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1920",
    "Bamboo Forest": "https://images.unsplash.com/photo-1518531933039-315f5d4a6b1a?w=1920",
    "Zen Garden": "https://images.unsplash.com/photo-1545389336-cf090694435e?w=1920",
    "Modern Architecture": "https://images.unsplash.com/photo-1487958449943-2429e8be8625?w=1920",
    "Bridge at Night": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920",
    "Neon City": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469?w=1920",
    "Underwater": "https://images.unsplash.com/photo-1544551763-46a013bb70b5?w=1920",
    "Space Nebula": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920",
    "Milky Way": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920",
}

# Custom CSS with glass cards and wallpaper support
def get_custom_css(wallpaper=None):
    wallpaper_url = WALLPAPERS.get(wallpaper, "")
    background_style = f"""
        background-image: url('{wallpaper_url}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    """ if wallpaper_url else """
        background: linear-gradient(135deg, #0a0e27, #1a1f4e, #0f3460);
    """
    
    return f"""
    <style>
        /* Global Styles */
        .stApp {{
            {background_style}
        }}
        
        /* Glass Card Effect - Applied to all containers */
        .stApp > header {{
            background: rgba(10, 14, 39, 0.7) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        }}
        
        /* Main content area */
        .main .block-container {{
            background: rgba(10, 14, 39, 0.6) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border-radius: 20px !important;
            padding: 2rem !important;
            margin: 1rem !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        }}
        
        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background: rgba(10, 14, 39, 0.8) !important;
            backdrop-filter: blur(25px) !important;
            -webkit-backdrop-filter: blur(25px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        }}
        
        section[data-testid="stSidebar"] > div {{
            background: transparent !important;
            padding: 1rem !important;
        }}
        
        /* Text Styles - Ensure visibility */
        .main .block-container h1,
        .main .block-container h2,
        .main .block-container h3,
        .main .block-container h4,
        .main .block-container h5,
        .main .block-container h6,
        .main .block-container p,
        .main .block-container span,
        .main .block-container div,
        .main .block-container label {{
            color: rgba(255, 255, 255, 0.95) !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
        }}
        
        /* Glass Cards */
        .glass-card {{
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border-radius: 16px !important;
            padding: 20px !important;
            margin: 10px 0 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
            transition: all 0.3s ease !important;
        }}
        
        .glass-card:hover {{
            background: rgba(255, 255, 255, 0.15) !important;
            border-color: rgba(212, 175, 55, 0.5) !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3) !important;
            transform: translateY(-2px) !important;
        }}
        
        .glass-card h1,
        .glass-card h2,
        .glass-card h3,
        .glass-card h4,
        .glass-card h5,
        .glass-card h6,
        .glass-card p,
        .glass-card span,
        .glass-card div,
        .glass-card label {{
            color: rgba(255, 255, 255, 0.95) !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
        }}
        
        /* Stat Cards */
        .stat-card {{
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            padding: 25px !important;
            border-radius: 16px !important;
            border-left: 4px solid #e94560 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
            margin: 10px 0 !important;
        }}
        
        .stat-value {{
            font-size: 2.5em !important;
            font-weight: 800 !important;
            color: rgba(255, 255, 255, 0.95) !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
        }}
        
        .stat-label {{
            color: rgba(255, 255, 255, 0.75) !important;
            font-size: 0.95em !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        }}
        
        /* Form Elements */
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox select,
        .stDateInput input,
        .stNumberInput input,
        .stFileUploader {{
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px !important;
            color: white !important;
        }}
        
        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stSelectbox select:focus {{
            border-color: rgba(212, 175, 55, 0.5) !important;
            box-shadow: 0 0 10px rgba(212, 175, 55, 0.2) !important;
        }}
        
        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stDateInput label,
        .stNumberInput label {{
            color: rgba(255, 255, 255, 0.9) !important;
            font-weight: 600 !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
        }}
        
        /* Buttons */
        .stButton button {{
            background: rgba(233, 69, 96, 0.7) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.5rem 1.2rem !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton button:hover {{
            background: rgba(233, 69, 96, 0.9) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(233, 69, 96, 0.3) !important;
        }}
        
        .golden-button button {{
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.8), rgba(184, 148, 31, 0.8)) !important;
            color: #0a0e27 !important;
            font-weight: 700 !important;
        }}
        
        /* DataFrames and Tables */
        .stDataFrame {{
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }}
        
        .stDataFrame th {{
            background: rgba(10, 14, 39, 0.8) !important;
            color: white !important;
        }}
        
        .stDataFrame td {{
            color: white !important;
            background: rgba(255, 255, 255, 0.05) !important;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px !important;
            color: white !important;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 12px !important;
            padding: 0.3rem !important;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: white !important;
            background: transparent !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: rgba(233, 69, 96, 0.5) !important;
            border-radius: 8px !important;
        }}
        
        /* Radio Buttons */
        .stRadio label {{
            color: white !important;
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 8px !important;
            padding: 8px 12px !important;
            margin: 4px 0 !important;
        }}
        
        /* Metrics */
        .stMetric {{
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 12px !important;
            padding: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }}
        
        .stMetric label,
        .stMetric div {{
            color: white !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
        }}
        
        /* School Code Banner */
        .school-code-banner {{
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border: 2px dashed rgba(233, 69, 96, 0.4) !important;
            border-radius: 16px !important;
            padding: 25px !important;
            text-align: center !important;
            margin: 20px 0 !important;
        }}
        
        .invite-code {{
            font-family: 'Courier New', monospace !important;
            font-size: 2.5em !important;
            font-weight: 800 !important;
            letter-spacing: 8px !important;
            color: white !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5) !important;
        }}
        
        /* Chat Messages */
        .chat-bubble {{
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 15px !important;
            padding: 12px 18px !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }}
        
        .chat-message-mine {{
            background: rgba(233, 69, 96, 0.4) !important;
            border-color: rgba(233, 69, 96, 0.3) !important;
        }}
        
        /* Notification */
        .notification {{
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border-radius: 12px !important;
            padding: 15px !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }}
        
        /* Success/Error/Warning Messages */
        .stSuccess, .stError, .stWarning, .stInfo {{
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }}
        
        /* Footer */
        footer {{
            background: rgba(10, 14, 39, 0.7) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: rgba(255, 255, 255, 0.7) !important;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: rgba(233, 69, 96, 0.5);
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(233, 69, 96, 0.8);
        }}
        
        /* Mobile Responsive */
        @media (max-width: 768px) {{
            .main .block-container {{
                padding: 1rem !important;
                margin: 0.5rem !important;
            }}
            
            .stat-value {{
                font-size: 1.8em !important;
            }}
            
            .invite-code {{
                font-size: 1.8em !important;
                letter-spacing: 4px !important;
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
    st.session_state.wallpaper = "None"

# Apply custom CSS
st.markdown(get_custom_css(st.session_state.wallpaper), unsafe_allow_html=True)

# Data storage setup
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
    filepath = DATA_DIR / filename
    with open(filepath, 'w') as f:
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
        <p style="font-size: 1.4em; color: white; margin: 10px 0;">School Resource Management System</p>
        <p style="color: #d4af37; font-size: 1.1em; margin: 10px 0;">by <span style="color: #f0d060; font-weight: 700;">WeGEM</span> (Edwin)</p>
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
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            login_form()
            st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.action == 'signup':
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            signup_form()
            st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.action == 'create':
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            create_school_form()
            st.markdown('</div>', unsafe_allow_html=True)

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
    <div class="glass-card" style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: white;">🏫 {school_name}</h1>
        <p style="color: white; font-size: 1.2em;">
            👤 {user['name']} 
            <span style="background: {'#e94560' if user['role']=='admin' else '#0f3460'}; 
                  color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.8em; margin-left: 10px;">
                {user['role'].upper()}
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Invite code banner (admin only)
    if user['role'] == 'admin':
        st.markdown(f"""
        <div class="school-code-banner">
            <p style="color: white; font-size: 1.1em;">🏫 School Invite Code - Share with Staff</p>
            <div class="invite-code">{st.session_state.school['invite_code']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; margin-bottom: 20px;">
            <p style="color: white; font-size: 1.1em;"><strong>{user['name']}</strong></p>
            <p style="color: #d4af37; font-size: 0.9em;">{user['role'].upper()}</p>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.8em;">{school_name}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Wallpaper selector
        st.markdown("### 🖼️ Theme")
        wallpaper = st.selectbox("Choose Wallpaper", list(WALLPAPERS.keys()), 
                                 index=list(WALLPAPERS.keys()).index(st.session_state.wallpaper))
        if wallpaper != st.session_state.wallpaper:
            st.session_state.wallpaper = wallpaper
            st.rerun()
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.school = None
            st.session_state.page = 'startup'
            st.rerun()
    
    # Navigation tabs
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
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_books}</div>
            <div class="stat-label">Total Books</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{books_borrowed}</div>
            <div class="stat-label">Books Borrowed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(members)}</div>
            <div class="stat-label">Members</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{overdue}</div>
            <div class="stat-label">Overdue</div>
        </div>
        """, unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_books - books_borrowed}</div>
            <div class="stat-label">Books Available</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(teachers)}</div>
            <div class="stat-label">Teachers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col7:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(furniture)}</div>
            <div class="stat-label">Furniture Items</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col8:
        active_loans = len([b for b in borrowed if not b.get('returned', False)])
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{active_loans}</div>
            <div class="stat-label">Active Loans</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_book_issuing():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

def render_individual_lending():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

def render_furniture():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

def render_returns():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("↩️ Return Items")
    
    school_name = st.session_state.school['name']
    search = st.text_input("🔍 Search by name, admission number, or book number")
    
    if st.button("Search", use_container_width=True):
        borrowed = load_data(f"borrowed_{school_name}.json", [])
        furniture = load_data(f"furniture_{school_name}.json", [])
        
        active_borrowed = [b for b in borrowed if not b.get('returned') 
                          and (search.lower() in b.get('name', '').lower() 
                               or search in b.get('adm', '') 
                               or search in b.get('bookNo', ''))]
        
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
                    st.write(f"**{item['name']}** - {item['bookTitle']} (#{item['bookNo']})")
                with col2:
                    st.write(f"Due: {item['returnDate']}")
                with col3:
                    if st.button("Return", key=f"ret_book_{item['id']}"):
                        item['returned'] = True
                        item['actualReturnDate'] = datetime.now().strftime('%Y-%m-%d')
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
                    st.write(f"**{item['name']}** - Chair: {item.get('chair', '-')}, Locker: {item.get('locker', '-')}")
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
    st.markdown('</div>', unsafe_allow_html=True)

def render_borrowed():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
            towrite = BytesIO()
            with pd.ExcelWriter(towrite, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Borrowed Books')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="borrowed_books.xlsx">📥 Download Excel File</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.info("No records found")
    st.markdown('</div>', unsafe_allow_html=True)

def render_members():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
                st.markdown(f"""
                <div style="color: white;">
                    <strong>{member['name']}</strong>
                    {f"<br><small>ID: {member['id']}</small>" if member.get('id') else ""}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("✏️ Edit", key=f"edit_mem_{i}"):
                    st.session_state[f"editing_member_{i}"] = True
            with col3:
                if st.button("🗑️ Delete", key=f"del_mem_{i}"):
                    members.pop(i)
                    save_data(f"members_{school_name}.json", members)
                    st.rerun()
            
            if st.session_state.get(f"editing_member_{i}"):
                new_name = st.text_input("New name", member['name'], key=f"edit_name_{i}")
                if st.button("Save", key=f"save_mem_{i}"):
                    members[i]['name'] = new_name
                    save_data(f"members_{school_name}.json", members)
                    st.session_state[f"editing_member_{i}"] = False
                    st.rerun()
            st.divider()
    else:
        st.info("No members added yet")
    st.markdown('</div>', unsafe_allow_html=True)

def render_catalog():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📚 Book Catalog")
    
    school_name = st.session_state.school['name']
    books = load_data(f"books_{school_name}.json", [])
    
    with st.form("add_book"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            title = st.text_input("Book Title")
        with col2:
            book_type = st.selectbox("Type", ["Textbook", "Novel", "Reference", "Magazine", "Other"])
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
                st.markdown(f"""
                <div style="color: white;">
                    📖 <strong>{book['title']}</strong>
                </div>
                """, unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

def render_teachers():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("👨‍🏫 Teachers")
    
    school_name = st.session_state.school['name']
    teachers = load_data(f"teachers_{school_name}.json", [])
    
    with st.form("add_teacher"):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Name")
        with col2:
            subjects = st.text_input("Subjects (comma separated)")
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
        for i, teacher in enumerate(teachers):
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            with col1:
                st.markdown(f"""
                <div style="color: white;">
                    <strong>{teacher['name']}</strong>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.write(f"Subjects: {teacher.get('subjects', '-')}")
            with col3:
                st.write(f"Class: {teacher.get('class_assigned', '-')}")
            with col4:
                if st.button("🗑️", key=f"del_teacher_{i}"):
                    teachers.pop(i)
                    save_data(f"teachers_{school_name}.json", teachers)
                    st.rerun()
            st.divider()
    else:
        st.info("No teachers added")
    st.markdown('</div>', unsafe_allow_html=True)

def render_classes():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📋 Class Lists")
    
    school_name = st.session_state.school['name']
    classes = load_data(f"classes_{school_name}.json", [])
    
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
    st.markdown('</div>', unsafe_allow_html=True)

def render_qr():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
            qr_cols = st.columns(4)
            for i in range(start_num, min(end_num + 1, start_num + 20)):  # Limit to 20
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(f"{qr_type}-{i}")
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                col_idx = (i - start_num) % 4
                with qr_cols[col_idx]:
                    st.image(f"data:image/png;base64,{img_str}", 
                            caption=f"{qr_type.upper()}: {i}", width=150)
    
    with tab2:
        st.info("📷 Scan QR codes using the SRMS mobile scanner")
        qr_input = st.text_input("Or enter QR code manually")
        if qr_input:
            st.success(f"Scanned: {qr_input}")
    st.markdown('</div>', unsafe_allow_html=True)

def render_chat():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💬 Staff Chat")
    
    school_name = st.session_state.school['name']
    user = st.session_state.user
    chat_messages = load_data(f"chat_messages_{school_name}.json", [])
    users = load_data(f"users_{school_name}.json", [])
    
    other_users = [u for u in users if u['email'] != user['email']]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Staff Online")
        for u in other_users:
            if st.button(f"🟢 {u['name']}\n({u['role']})", key=f"chat_user_{u['email']}", use_container_width=True):
                st.session_state.chat_with = u['email']
    
    with col2:
        if 'chat_with' in st.session_state:
            chat_with = st.session_state.chat_with
            chat_user = next((u for u in users if u['email'] == chat_with), None)
            
            if chat_user:
                st.markdown(f"### 💬 Chat with {chat_user['name']}")
                
                msgs = [m for m in chat_messages 
                       if (m['from'] == user['email'] and m['to'] == chat_with) 
                       or (m['from'] == chat_with and m['to'] == user['email'])]
                
                for msg in sorted(msgs, key=lambda x: x['timestamp']):
                    is_mine = msg['from'] == user['email']
                    align = "flex-end" if is_mine else "flex-start"
                    bg = "rgba(233,69,96,0.4)" if is_mine else "rgba(255,255,255,0.15)"
                    
                    st.markdown(f"""
                    <div style="display: flex; justify-content: {align}; margin: 10px 0;">
                        <div class="chat-bubble {'chat-message-mine' if is_mine else ''}" 
                             style="max-width: 70%;">
                            <strong>{msg['from_name']}:</strong> {msg['message']}
                            <br><small style="color: rgba(255,255,255,0.5);">{msg['timestamp'][:16]}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
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
    st.markdown('</div>', unsafe_allow_html=True)

def render_audit_log():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📝 Audit Log")
    
    school_name = st.session_state.school['name']
    audit_log = load_data(f"audit_log_{school_name}.json", [])
    
    if audit_log:
        df = pd.DataFrame(audit_log)
        st.dataframe(df, use_container_width=True)
        
        if st.button("📎 Export Log", use_container_width=True):
            towrite = BytesIO()
            with pd.ExcelWriter(towrite, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Audit Log')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="audit_log.xlsx">📥 Download Excel File</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.info("No audit log entries")
    st.markdown('</div>', unsafe_allow_html=True)

def render_reports():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
            if overdue:
                df = pd.DataFrame(overdue)
                st.dataframe(df, use_container_width=True)
            else:
                st.success("No overdue books!")
            
        elif report_type == "Complete Summary":
            books = load_data(f"books_{school_name}.json", [])
            borrowed = load_data(f"borrowed_{school_name}.json", [])
            members = load_data(f"members_{school_name}.json", [])
            teachers = load_data(f"teachers_{school_name}.json", [])
            furniture = load_data(f"furniture_{school_name}.json", [])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Books", sum(b.get('quantity', 0) for b in books))
                st.metric("Active Loans", len([b for b in borrowed if not b.get('returned')]))
            with col2:
                st.metric("Members", len(members))
                st.metric("Teachers", len(teachers))
            with col3:
                active_furniture = len([f for f in furniture if not f.get('returned')])
                st.metric("Active Furniture", active_furniture)
                st.metric("Classes", len(load_data(f"classes_{school_name}.json", [])))
            with col4:
                overdue_count = len([b for b in borrowed if not b.get('returned', False) 
                                    and datetime.strptime(b.get('returnDate', '2000-01-01'), '%Y-%m-%d') < datetime.now()])
                st.metric("Overdue Books", overdue_count)
                st.metric("Total Transactions", len(borrowed) + len(furniture))
    st.markdown('</div>', unsafe_allow_html=True)

def render_settings():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["Theme", "Data Management", "School Info"])
    
    with tab1:
        st.markdown("### 🖼️ Theme Settings")
        wallpaper = st.selectbox("Select Wallpaper", list(WALLPAPERS.keys()), 
                                 index=list(WALLPAPERS.keys()).index(st.session_state.wallpaper))
        if st.button("Apply Theme", use_container_width=True):
            st.session_state.wallpaper = wallpaper
            st.rerun()
        
        if wallpaper != "None":
            st.image(WALLPAPERS[wallpaper], caption=f"Current: {wallpaper}", width=400)
    
    with tab2:
        st.markdown("### 💾 Data Management")
        
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
                href = f'<a href="data:application/json;base64,{b64}" download="srms_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json">📥 Download Backup</a>'
                st.markdown(href, unsafe_allow_html=True)
        
        with col2:
            uploaded = st.file_uploader("📤 Restore Data", type=['json'])
            if uploaded:
                if st.button("Restore Backup", use_container_width=True):
                    try:
                        data = json.load(uploaded)
                        school_name = st.session_state.school['name']
                        for file, file_data in data.items():
                            save_data(f"{file}_{school_name}.json", file_data)
                        st.success("Data restored successfully!")
                        st.rerun()
                    except:
                        st.error("Invalid backup file!")
        
        with col3:
            st.markdown("#### ⚠️ Danger Zone")
            confirm_delete = st.text_input("Type 'DELETE' to clear all data")
            if st.button("⚠️ Clear All Data", use_container_width=True, type="primary"):
                if confirm_delete == "DELETE":
                    school_name = st.session_state.school['name']
                    for file in ["books", "members", "borrowed", "teachers", "classes", 
                               "furniture", "book_issues", "individual_lendings"]:
                        save_data(f"{file}_{school_name}.json", [])
                    st.error("All data cleared!")
                    st.rerun()
                else:
                    st.warning("Type 'DELETE' to confirm")
    
    with tab3:
        st.markdown("### 🏫 School Information")
        school = st.session_state.school
        
        st.markdown(f"""
        <div class="glass-card">
            <p><strong>School Name:</strong> {school['name']}</p>
            <p><strong>Address:</strong> {school.get('address', 'N/A')}</p>
            <p><strong>Admin:</strong> {school['admin_name']}</p>
            <p><strong>Email:</strong> {school['admin_email']}</p>
            <p><strong>Phone:</strong> {school.get('admin_phone', 'N/A')}</p>
            <p><strong>Invite Code:</strong> <code style="font-size: 1.2em;">{school['invite_code']}</code></p>
            <p><strong>Created:</strong> {school.get('created', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============== MAIN APP ==============
def main():
    if st.session_state.page == 'startup':
        startup_page()
    elif st.session_state.page == 'dashboard':
        dashboard_page()

if __name__ == "__main__":
    main()
