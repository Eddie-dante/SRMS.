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
    "Mountain Lake": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920",
    "Night Sky": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920",
    "Purple Haze": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469?w=1920",
    "Green Valley": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920",
    "Autumn Road": "https://images.unsplash.com/photo-1507783548227-544c3b8fc065?w=1920",
    "Winter Snow": "https://images.unsplash.com/photo-1477601263568-180e2c6d046e?w=1920",
    "Spring Flowers": "https://images.unsplash.com/photo-1490750967868-88aa4cef14d0?w=1920",
    "Summer Field": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920",
    "Waterfall": "https://images.unsplash.com/photo-1544551763-46a013bb70b5?w=1920",
    "Lavender Field": "https://images.unsplash.com/photo-1499002238440-d264edd596ec?w=1920",
    "Cherry Blossom": "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1920",
    "Golden Hour": "https://images.unsplash.com/photo-1501856777435-29877ed80a3d?w=1920",
    "Blue Lagoon": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1920",
    "Zen Garden": "https://images.unsplash.com/photo-1545389336-cf090694435e?w=1920",
    "Neon City": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469?w=1920",
    "Milky Way": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920",
}

# ============ ULTRA PREMIUM CSS ============
def get_premium_css(wallpaper=None):
    wallpaper_url = WALLPAPERS.get(wallpaper, "")
    background_style = f"""
        background-image: url('{wallpaper_url}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    """ if wallpaper_url else """
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f4e 50%, #0f3460 100%);
    """
    
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800&display=swap');
        
        * {{
            font-family: 'Inter', 'Poppins', sans-serif;
        }}
        
        .stApp {{
            {background_style}
        }}
        
        .stApp > header {{
            background: rgba(10, 14, 39, 0.85) !important;
            backdrop-filter: blur(30px) !important;
            -webkit-backdrop-filter: blur(30px) !important;
            border-bottom: 2px solid rgba(212, 175, 55, 0.3) !important;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5) !important;
        }}
        
        .main .block-container {{
            background: rgba(10, 14, 39, 0.5) !important;
            backdrop-filter: blur(25px) !important;
            -webkit-backdrop-filter: blur(25px) !important;
            border-radius: 24px !important;
            padding: 2.5rem !important;
            margin: 1.5rem !important;
            border: 1px solid rgba(212, 175, 55, 0.2) !important;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4) !important;
        }}
        
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, 
                rgba(10, 14, 39, 0.95) 0%, 
                rgba(26, 31, 78, 0.95) 50%,
                rgba(15, 52, 96, 0.95) 100%) !important;
            backdrop-filter: blur(30px) !important;
            -webkit-backdrop-filter: blur(30px) !important;
            border-right: 2px solid rgba(212, 175, 55, 0.3) !important;
            box-shadow: 5px 0 40px rgba(0, 0, 0, 0.5) !important;
        }}
        
        section[data-testid="stSidebar"] > div {{
            background: transparent !important;
            padding: 1.2rem !important;
        }}
        
        .main .block-container h1,
        .main .block-container h2,
        .main .block-container h3,
        .main .block-container h4,
        .main .block-container h5,
        .main .block-container h6 {{
            color: #FFFFFF !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6) !important;
            font-weight: 700 !important;
        }}
        
        .main .block-container p,
        .main .block-container span,
        .main .block-container div,
        .main .block-container label,
        .main .block-container li {{
            color: #FFFFFF !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5) !important;
        }}
        
        .glass-card {{
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.15) 0%, 
                rgba(255, 255, 255, 0.05) 100%) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-radius: 20px !important;
            padding: 25px !important;
            margin: 15px 0 !important;
            border: 1px solid rgba(212, 175, 55, 0.25) !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        
        .glass-card:hover {{
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.2) 0%, 
                rgba(255, 255, 255, 0.1) 100%) !important;
            border-color: rgba(212, 175, 55, 0.5) !important;
            box-shadow: 0 15px 50px rgba(212, 175, 55, 0.2) !important;
            transform: translateY(-3px) !important;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, 
                rgba(233, 69, 96, 0.2) 0%, 
                rgba(233, 69, 96, 0.05) 100%) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            padding: 30px 20px !important;
            border-radius: 20px !important;
            border: 1px solid rgba(233, 69, 96, 0.3) !important;
            border-left: 5px solid #e94560 !important;
            box-shadow: 0 10px 40px rgba(233, 69, 96, 0.15) !important;
            text-align: center !important;
            transition: all 0.3s ease !important;
            margin: 10px 0 !important;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px) !important;
            box-shadow: 0 20px 60px rgba(233, 69, 96, 0.3) !important;
            border-color: rgba(233, 69, 96, 0.6) !important;
        }}
        
        .stat-value {{
            font-size: 3em !important;
            font-weight: 900 !important;
            background: linear-gradient(135deg, #FFFFFF 0%, #e94560 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            margin-bottom: 5px !important;
        }}
        
        .stat-label {{
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 0.95em !important;
            font-weight: 600 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
        }}
        
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stDateInput input {{
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 2px solid rgba(212, 175, 55, 0.4) !important;
            border-radius: 12px !important;
            padding: 12px 18px !important;
            color: #1a1a1a !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        }}
        
        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus {{
            background: #FFFFFF !important;
            border-color: #e94560 !important;
            box-shadow: 0 0 0 4px rgba(233, 69, 96, 0.2), 0 8px 25px rgba(0, 0, 0, 0.15) !important;
            color: #0a0a0a !important;
        }}
        
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {{
            color: #999999 !important;
            font-weight: 400 !important;
        }}
        
        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stDateInput label,
        .stNumberInput label,
        .stFileUploader label {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
            margin-bottom: 8px !important;
            letter-spacing: 0.5px !important;
        }}
        
        .stSelectbox > div > div {{
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px solid rgba(212, 175, 55, 0.4) !important;
            border-radius: 12px !important;
            color: #1a1a1a !important;
        }}
        
        .stSelectbox [data-baseweb="select"] {{
            background: rgba(255, 255, 255, 0.95) !important;
        }}
        
        .stSelectbox [data-baseweb="select"] * {{
            color: #1a1a1a !important;
        }}
        
        .stFileUploader > div {{
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px dashed rgba(212, 175, 55, 0.5) !important;
            border-radius: 15px !important;
            padding: 20px !important;
        }}
        
        .stButton button {{
            background: linear-gradient(135deg, #e94560 0%, #c62a47 100%) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            padding: 12px 28px !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 8px 25px rgba(233, 69, 96, 0.3) !important;
            text-transform: uppercase !important;
        }}
        
        .stButton button:hover {{
            background: linear-gradient(135deg, #ff5a7a 0%, #e94560 100%) !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 40px rgba(233, 69, 96, 0.5) !important;
        }}
        
        .stDataFrame {{
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
            overflow: hidden !important;
        }}
        
        .stDataFrame th {{
            background: linear-gradient(135deg, rgba(233, 69, 96, 0.8), rgba(198, 42, 71, 0.8)) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            padding: 15px !important;
            border-bottom: 2px solid rgba(212, 175, 55, 0.5) !important;
        }}
        
        .stDataFrame td {{
            background: rgba(255, 255, 255, 0.05) !important;
            color: #FFFFFF !important;
            padding: 12px 15px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        }}
        
        .streamlit-expanderHeader {{
            background: linear-gradient(135deg, 
                rgba(212, 175, 55, 0.2) 0%, 
                rgba(212, 175, 55, 0.05) 100%) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
            border-radius: 14px !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            padding: 15px 20px !important;
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-radius: 16px !important;
            padding: 5px !important;
            gap: 5px !important;
            border: 1px solid rgba(212, 175, 55, 0.2) !important;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: rgba(255, 255, 255, 0.7) !important;
            background: transparent !important;
            border-radius: 12px !important;
            padding: 12px 20px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            border: none !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, #e94560, #c62a47) !important;
            color: #FFFFFF !important;
            box-shadow: 0 8px 25px rgba(233, 69, 96, 0.4) !important;
        }}
        
        .stMetric {{
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.12) 0%, 
                rgba(255, 255, 255, 0.05) 100%) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border-radius: 16px !important;
            padding: 20px !important;
            border: 1px solid rgba(212, 175, 55, 0.25) !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
        }}
        
        .stSuccess {{
            background: linear-gradient(135deg, 
                rgba(40, 167, 69, 0.3) 0%, 
                rgba(40, 167, 69, 0.1) 100%) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(40, 167, 69, 0.4) !important;
            border-radius: 14px !important;
            color: #FFFFFF !important;
        }}
        
        .stError {{
            background: linear-gradient(135deg, 
                rgba(220, 53, 69, 0.3) 0%, 
                rgba(220, 53, 69, 0.1) 100%) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(220, 53, 69, 0.4) !important;
            border-radius: 14px !important;
            color: #FFFFFF !important;
        }}
        
        .school-code-banner {{
            background: linear-gradient(135deg, 
                rgba(212, 175, 55, 0.2) 0%, 
                rgba(212, 175, 55, 0.05) 100%) !important;
            backdrop-filter: blur(25px) !important;
            -webkit-backdrop-filter: blur(25px) !important;
            border: 2px solid rgba(212, 175, 55, 0.5) !important;
            border-radius: 20px !important;
            padding: 30px !important;
            text-align: center !important;
            margin: 25px 0 !important;
            box-shadow: 0 15px 50px rgba(212, 175, 55, 0.2) !important;
        }}
        
        .invite-code {{
            font-family: 'Courier New', monospace !important;
            font-size: 3em !important;
            font-weight: 900 !important;
            letter-spacing: 10px !important;
            background: linear-gradient(135deg, #FFFFFF 0%, #d4af37 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
        }}
        
        .chat-bubble {{
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border-radius: 18px !important;
            padding: 15px 20px !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
        }}
        
        .chat-message-mine {{
            background: linear-gradient(135deg, 
                rgba(233, 69, 96, 0.4) 0%, 
                rgba(233, 69, 96, 0.2) 100%) !important;
            border-color: rgba(233, 69, 96, 0.4) !important;
        }}
        
        footer {{
            background: rgba(10, 14, 39, 0.9) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-top: 2px solid rgba(212, 175, 55, 0.3) !important;
            color: rgba(255, 255, 255, 0.8) !important;
        }}
        
        ::-webkit-scrollbar {{
            width: 12px;
            height: 12px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, #e94560, #c62a47);
            border-radius: 10px;
            border: 2px solid rgba(255, 255, 255, 0.1);
        }}
        
        @media (max-width: 768px) {{
            .main .block-container {{
                padding: 1rem !important;
                margin: 0.5rem !important;
                border-radius: 16px !important;
            }}
            .stat-value {{
                font-size: 2em !important;
            }}
            .invite-code {{
                font-size: 1.8em !important;
                letter-spacing: 5px !important;
            }}
        }}
        
        /* Sidebar Navigation Buttons */
        section[data-testid="stSidebar"] .stButton button {{
            background: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
            font-size: 0.9rem !important;
            padding: 10px 15px !important;
            text-align: left !important;
            margin: 3px 0 !important;
            transition: all 0.3s ease !important;
            text-transform: none !important;
            letter-spacing: 0 !important;
            box-shadow: none !important;
        }}
        
        section[data-testid="stSidebar"] .stButton button:hover {{
            background: rgba(233, 69, 96, 0.3) !important;
            border-color: rgba(233, 69, 96, 0.5) !important;
            transform: translateX(5px) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        }}
        
        section[data-testid="stSidebar"] .stButton button[kind="primary"] {{
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%) !important;
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

# Apply premium CSS
st.markdown(get_premium_css(st.session_state.wallpaper), unsafe_allow_html=True)

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
    <div class="glass-card" style="text-align: center; max-width: 650px; margin: 60px auto;">
        <div style="width: 180px; height: 180px; background: linear-gradient(135deg, #d4af37 0%, #f0d060 50%, #b8941f 100%); 
             border-radius: 40px; display: inline-flex; align-items: center; justify-content: center; 
             font-size: 65px; font-weight: 900; color: #0a0e27; margin-bottom: 25px;
             box-shadow: 0 25px 80px rgba(212, 175, 55, 0.5), inset 0 2px 10px rgba(255,255,255,0.3);">
            SRMS
        </div>
        <h1 style="font-size: 4em; background: linear-gradient(180deg, #f0d060 0%, #d4af37 50%, #b8941f 100%); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 15px 0; font-weight: 900;">
            SRMS
        </h1>
        <p style="font-size: 1.5em; color: #FFFFFF; margin: 15px 0; font-weight: 300; letter-spacing: 2px;">
            School Resource Management System
        </p>
        <p style="color: #d4af37; font-size: 1.2em; margin: 15px 0; font-weight: 500;">
            by <span style="color: #f0d060; font-weight: 700;">WeGEM</span> (Edwin)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔑 Staff Login", use_container_width=True, key="startup_login"):
            st.session_state.action = 'login'
    
    with col2:
        if st.button("📝 Staff Sign Up", use_container_width=True, key="startup_signup"):
            st.session_state.action = 'signup'
    
    with col3:
        if st.button("🏫 Create School", use_container_width=True, key="startup_create"):
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
    st.markdown('<h3 style="color: #FFFFFF; text-align: center;">🔐 Staff Login</h3>', unsafe_allow_html=True)
    with st.form("login_form_1"):
        name = st.text_input("👤 Your Full Name", placeholder="Enter your registered name")
        school_name = st.text_input("🏢 School Name", placeholder="Enter your school name")
        invite_code = st.text_input("🔑 Invite Code", placeholder="Enter the invite code")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        if st.form_submit_button("🔑 Login Now", use_container_width=True):
            schools = load_data("schools.json", {})
            school = schools.get(school_name)
            
            if not school:
                st.error("❌ School not found!")
                return
            
            users = load_data(f"users_{school_name}.json", [])
            user = next((u for u in users if u['name'].lower() == name.lower() 
                        and u['code'] == invite_code.upper()), None)
            
            if not user or not (user['password'] == hash_password(password)):
                st.error("❌ Invalid credentials!")
                return
            
            st.session_state.user = user
            st.session_state.school = school
            st.session_state.page = 'dashboard'
            st.session_state.action = None
            st.rerun()

def signup_form():
    st.markdown('<h3 style="color: #FFFFFF; text-align: center;">📝 Staff Sign Up</h3>', unsafe_allow_html=True)
    with st.form("signup_form_1"):
        name = st.text_input("👤 Full Name", placeholder="Your full name")
        email = st.text_input("📧 Email Address", placeholder="your@email.com")
        phone = st.text_input("📞 Phone Number", placeholder="+1234567890")
        school_name = st.text_input("🏢 School Name", placeholder="Your school name")
        invite_code = st.text_input("🔑 Invite Code", placeholder="From your admin")
        staff_id = st.text_input("👤 Staff ID (Optional)", placeholder="Employee/Staff ID")
        password = st.text_input("🔒 Create Password", type="password", placeholder="Min 6 characters")
        
        if st.form_submit_button("📝 Sign Up Now", use_container_width=True):
            schools = load_data("schools.json", {})
            school = schools.get(school_name)
            
            if not school:
                st.error("❌ School not found!")
                return
            
            if school['invite_code'] != invite_code.upper():
                st.error("❌ Invalid invite code!")
                return
            
            if len(password) < 6:
                st.error("❌ Password must be at least 6 characters!")
                return
            
            users = load_data(f"users_{school_name}.json", [])
            if any(u['email'] == email for u in users):
                st.error("❌ Email already registered!")
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
            st.session_state.action = None
            st.success("✅ Registration successful!")
            st.rerun()

def create_school_form():
    st.markdown('<h3 style="color: #FFFFFF; text-align: center;">🏫 Create New School</h3>', unsafe_allow_html=True)
    with st.form("create_school_form_1"):
        school_name = st.text_input("🏢 School Name", placeholder="e.g., Sunshine High School")
        address = st.text_input("📍 School Address", placeholder="School location")
        admin_name = st.text_input("👤 Admin Full Name", placeholder="Your full name")
        admin_email = st.text_input("📧 Admin Email", placeholder="admin@school.edu")
        admin_phone = st.text_input("📞 Admin Phone", placeholder="+1234567890")
        password = st.text_input("🔒 Password", type="password", placeholder="Min 8 characters")
        confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter password")
        
        if st.form_submit_button("🚀 Create School Now", use_container_width=True):
            if password != confirm_password:
                st.error("❌ Passwords don't match!")
                return
            
            if len(password) < 8:
                st.error("❌ Password must be at least 8 characters!")
                return
            
            schools = load_data("schools.json", {})
            if school_name in schools:
                st.error("❌ School already exists!")
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
            st.session_state.action = None
            st.success(f"✅ School created! Invite Code: **{invite_code}**")
            st.info("💡 Save this code - staff will need it to join!")
            st.rerun()

# ============== DASHBOARD ==============
def dashboard_page():
    school_name = st.session_state.school['name']
    user = st.session_state.user
    
    # Premium Header
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; margin-bottom: 30px; padding: 30px;">
        <h1 style="font-size: 2.5em; margin-bottom: 10px;">🏫 {school_name}</h1>
        <p style="font-size: 1.3em; color: #FFFFFF; margin: 10px 0;">
            👤 {user['name']} 
            <span style="background: linear-gradient(135deg, {'#e94560' if user['role']=='admin' else '#0f3460'}, {'#c62a47' if user['role']=='admin' else '#0a2a4a'}); 
                  color: #FFFFFF; padding: 6px 15px; border-radius: 25px; font-size: 0.8em; margin-left: 15px;
                  border: 1px solid rgba(255,255,255,0.3);">
                {user['role'].upper()}
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if user['role'] == 'admin':
        st.markdown(f"""
        <div class="school-code-banner">
            <p style="color: #FFFFFF; font-size: 1.2em; margin-bottom: 15px;">🏫 School Invite Code - Share with Staff</p>
            <div class="invite-code">{st.session_state.school['invite_code']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ============ SIDEBAR WITH COLLAPSIBLE NAVIGATION ============
    with st.sidebar:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; margin-bottom: 20px; padding: 15px;">
            <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #d4af37, #f0d060); 
                 border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; 
                 font-size: 25px; margin-bottom: 8px; font-weight: 700; color: #0a0e27;">
                {user['name'][0].upper()}
            </div>
            <p style="color: #FFFFFF; font-size: 1em; margin: 3px 0;"><strong>{user['name']}</strong></p>
            <p style="color: #d4af37; font-size: 0.8em; margin: 3px 0;">{user['role'].upper()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Theme selector
        with st.expander("🎨 Theme & Wallpaper", expanded=False):
            wallpaper = st.selectbox("🖼️ Wallpaper", list(WALLPAPERS.keys()), 
                                     index=list(WALLPAPERS.keys()).index(st.session_state.wallpaper),
                                     key="sidebar_wallpaper")
            if wallpaper != st.session_state.wallpaper:
                st.session_state.wallpaper = wallpaper
                st.rerun()
        
        st.divider()
        
        # Collapsible Navigation Sections
        with st.expander("📊 MAIN", expanded=True):
            if st.button("📊 Dashboard", use_container_width=True, key="nav_dashboard"):
                st.session_state.current_section = 'dashboard'
                st.rerun()
        
        with st.expander("📖 LIBRARY", expanded=False):
            if st.button("📖 Book Issuing", use_container_width=True, key="nav_book_issue"):
                st.session_state.current_section = 'book_issuing'
                st.rerun()
            if st.button("👤 Lend Book", use_container_width=True, key="nav_lend"):
                st.session_state.current_section = 'lend_book'
                st.rerun()
            if st.button("↩️ Returns", use_container_width=True, key="nav_returns"):
                st.session_state.current_section = 'returns'
                st.rerun()
            if st.button("📋 Borrowed", use_container_width=True, key="nav_borrowed"):
                st.session_state.current_section = 'borrowed'
                st.rerun()
            if st.button("📚 Catalog", use_container_width=True, key="nav_catalog"):
                st.session_state.current_section = 'catalog'
                st.rerun()
        
        with st.expander("👥 PEOPLE", expanded=False):
            if st.button("👥 Members", use_container_width=True, key="nav_members"):
                st.session_state.current_section = 'members'
                st.rerun()
            if st.button("👨‍🏫 Teachers", use_container_width=True, key="nav_teachers"):
                st.session_state.current_section = 'teachers'
                st.rerun()
            if st.button("📋 Classes", use_container_width=True, key="nav_classes"):
                st.session_state.current_section = 'classes'
                st.rerun()
        
        with st.expander("🛠️ TOOLS", expanded=False):
            if st.button("🪑 Furniture", use_container_width=True, key="nav_furniture"):
                st.session_state.current_section = 'furniture'
                st.rerun()
            if st.button("📱 QR Codes", use_container_width=True, key="nav_qr"):
                st.session_state.current_section = 'qr'
                st.rerun()
            if st.button("💬 Chat", use_container_width=True, key="nav_chat"):
                st.session_state.current_section = 'chat'
                st.rerun()
        
        with st.expander("📈 ANALYTICS", expanded=False):
            if st.button("📝 Audit Log", use_container_width=True, key="nav_log"):
                st.session_state.current_section = 'log'
                st.rerun()
            if st.button("📈 Reports", use_container_width=True, key="nav_reports"):
                st.session_state.current_section = 'reports'
                st.rerun()
        
        with st.expander("⚙️ SYSTEM", expanded=False):
            if st.button("⚙️ Settings", use_container_width=True, key="nav_settings"):
                st.session_state.current_section = 'settings'
                st.rerun()
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True, type="primary", key="nav_logout"):
            st.session_state.user = None
            st.session_state.school = None
            st.session_state.page = 'startup'
            st.rerun()
        
        st.markdown("""
        <div style="text-align: center; margin-top: 20px; padding: 10px;">
            <p style="color: rgba(255,255,255,0.4); font-size: 0.7em;">
                SRMS v6.0<br>by WeGEM (Edwin)<br>© 2025
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ============ MAIN CONTENT AREA ============
    section = st.session_state.current_section
    
    if section == 'dashboard':
        render_dashboard()
    elif section == 'book_issuing':
        render_book_issuing()
    elif section == 'lend_book':
        render_individual_lending()
    elif section == 'furniture':
        render_furniture()
    elif section == 'returns':
        render_returns()
    elif section == 'borrowed':
        render_borrowed()
    elif section == 'members':
        render_members()
    elif section == 'catalog':
        render_catalog()
    elif section == 'teachers':
        render_teachers()
    elif section == 'classes':
        render_classes()
    elif section == 'qr':
        render_qr()
    elif section == 'chat':
        render_chat()
    elif section == 'log':
        render_audit_log()
    elif section == 'reports':
        render_reports()
    elif section == 'settings':
        render_settings()

# ============ RENDER FUNCTIONS ============
def render_dashboard():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #FFFFFF; text-align: center;">📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    
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
        st.markdown(f'<div class="stat-card"><div class="stat-value">{total_books}</div><div class="stat-label">Total Books</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{books_borrowed}</div><div class="stat-label">Borrowed</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{total_books - books_borrowed}</div><div class="stat-label">Available</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{overdue}</div><div class="stat-label">Overdue</div></div>', unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(members)}</div><div class="stat-label">Members</div></div>', unsafe_allow_html=True)
    with col6:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(teachers)}</div><div class="stat-label">Teachers</div></div>', unsafe_allow_html=True)
    with col7:
        active_furniture = len([f for f in furniture if not f.get('returned')])
        st.markdown(f'<div class="stat-card"><div class="stat-value">{active_furniture}</div><div class="stat-label">Furniture</div></div>', unsafe_allow_html=True)
    with col8:
        active_loans = len([b for b in borrowed if not b.get('returned', False)])
        st.markdown(f'<div class="stat-card"><div class="stat-value">{active_loans}</div><div class="stat-label">Active Loans</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_book_issuing():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">📖 Bulk Book Issuing to Class</h3>', unsafe_allow_html=True)
    
    school_name = st.session_state.school['name']
    books = load_data(f"books_{school_name}.json", [])
    classes = load_data(f"classes_{school_name}.json", [])
    
    col1, col2 = st.columns(2)
    with col1:
        selected_book = st.selectbox("📚 Select Book", [b['title'] for b in books if b.get('quantity', 0) > 0], key="bi_book")
    with col2:
        selected_class = st.selectbox("📋 Select Class", [c['name'] for c in classes], key="bi_class")
    
    col3, col4 = st.columns(2)
    with col3:
        issue_date = st.date_input("📅 Issue Date", datetime.now(), key="bi_issue_date")
    with col4:
        return_date = st.date_input("📅 Return Date", datetime.now() + timedelta(days=14), key="bi_return_date")
    
    if st.button("📋 Load Class Students", use_container_width=True, key="bi_load"):
        class_data = next((c for c in classes if c['name'] == selected_class), None)
        if class_data:
            st.session_state.current_class_students = class_data.get('students', [])
            st.success(f"✅ Loaded {len(st.session_state.current_class_students)} students!")
    
    if 'current_class_students' in st.session_state:
        students = st.session_state.current_class_students
        if students:
            df = pd.DataFrame(students)
            df['Book No'] = ""
            df['Issue'] = False
            edited_df = st.data_editor(df, use_container_width=True, num_rows="fixed", key="bi_editor")
            
            if st.button("✅ Issue Books to Selected", use_container_width=True, key="bi_issue"):
                issued_count = 0
                borrowed = load_data(f"borrowed_{school_name}.json", [])
                for idx, row in edited_df.iterrows():
                    if row['Issue'] and row['Book No']:
                        book = next((b for b in books if b['title'] == selected_book), None)
                        if book and book['quantity'] > 0:
                            borrowed.append({
                                "name": row['name'], "adm": row.get('adm', ''),
                                "bookTitle": selected_book, "bookNo": row['Book No'],
                                "borrowDate": issue_date.strftime('%Y-%m-%d'),
                                "returnDate": return_date.strftime('%Y-%m-%d'),
                                "returned": False, "id": generate_code("BOR")
                            })
                            book['quantity'] -= 1
                            issued_count += 1
                save_data(f"borrowed_{school_name}.json", borrowed)
                save_data(f"books_{school_name}.json", books)
                st.success(f"✅ Issued {issued_count} books successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

def render_individual_lending():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">👤 Individual Book Lending</h3>', unsafe_allow_html=True)
    
    school_name = st.session_state.school['name']
    books = load_data(f"books_{school_name}.json", [])
    
    with st.form("ind_lend_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Student Name", placeholder="Enter student name")
            adm = st.text_input("🔢 Admission Number", placeholder="e.g., ADM/24/1234")
            form = st.text_input("📚 Form/Class", placeholder="e.g., Form 1")
        with col2:
            stream = st.text_input("📋 Stream", placeholder="e.g., A")
            selected_book = st.selectbox("📖 Book", [b['title'] for b in books if b.get('quantity', 0) > 0], key="il_book")
            book_no = st.text_input("🔢 Book Number", placeholder="Enter book number")
        
        col3, col4 = st.columns(2)
        with col3:
            borrow_date = st.date_input("📅 Borrow Date", datetime.now(), key="il_borrow_date")
        with col4:
            return_date = st.date_input("📅 Return Date", datetime.now() + timedelta(days=14), key="il_return_date")
        
        if st.form_submit_button("📖 Lend Book Now", use_container_width=True):
            if name and selected_book and book_no:
                borrowed = load_data(f"borrowed_{school_name}.json", [])
                book = next((b for b in books if b['title'] == selected_book), None)
                if book and book['quantity'] > 0:
                    borrowed.append({
                        "name": name, "adm": adm, "form": form, "stream": stream,
                        "bookTitle": selected_book, "bookNo": book_no,
                        "borrowDate": borrow_date.strftime('%Y-%m-%d'),
                        "returnDate": return_date.strftime('%Y-%m-%d'),
                        "returned": False, "id": generate_code("BOR")
                    })
                    book['quantity'] -= 1
                    save_data(f"borrowed_{school_name}.json", borrowed)
                    save_data(f"books_{school_name}.json", books)
                    st.success("✅ Book lent successfully!")
                else:
                    st.error("❌ Book not available!")
    st.markdown('</div>', unsafe_allow_html=True)

def render_furniture():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">🪑 Furniture Allocation</h3>', unsafe_allow_html=True)
    
    school_name = st.session_state.school['name']
    classes = load_data(f"classes_{school_name}.json", [])
    
    selected_class = st.selectbox("📋 Select Class", [c['name'] for c in classes], key="fur_class")
    
    col1, col2 = st.columns(2)
    with col1:
        chair_prefix = st.text_input("🪑 Chair Prefix", "CH-")
        chair_start = st.number_input("Chair Start", 1, 1000, 1, key="fur_chair_start")
        chair_end = st.number_input("Chair End", 1, 1000, 10, key="fur_chair_end")
    with col2:
        locker_prefix = st.text_input("🔒 Locker Prefix", "LK-")
        locker_start = st.number_input("Locker Start", 1, 1000, 1, key="fur_lock_start")
        locker_end = st.number_input("Locker End", 1, 1000, 10, key="fur_lock_end")
    
    if st.button("📋 Load Class for Allocation", use_container_width=True, key="fur_load"):
        class_data = next((c for c in classes if c['name'] == selected_class), None)
        if class_data:
            st.session_state.furniture_data = {
                "students": class_data.get('students', []),
                "chair_range": list(range(chair_start, chair_end + 1)),
                "locker_range": list(range(locker_start, locker_end + 1))
            }
            st.success(f"✅ Loaded {len(class_data.get('students', []))} students!")
    
    if 'furniture_data' in st.session_state:
        students = st.session_state.furniture_data['students']
        if students:
            df = pd.DataFrame(students)
            df['Chair No'] = ""
            df['Locker No'] = ""
            df['Allocate'] = False
            edited_df = st.data_editor(df, use_container_width=True, key="fur_editor")
            
            if st.button("✅ Allocate Furniture", use_container_width=True, key="fur_allocate"):
                allocated = 0
                furniture = load_data(f"furniture_{school_name}.json", [])
                for idx, row in edited_df.iterrows():
                    if row['Allocate']:
                        furniture.append({
                            "name": row['name'], "adm": row.get('adm', ''),
                            "chair": f"{chair_prefix}{row['Chair No']}" if row['Chair No'] else "",
                            "locker": f"{locker_prefix}{row['Locker No']}" if row['Locker No'] else "",
                            "date": datetime.now().strftime('%Y-%m-%d'),
                            "returned": False, "id": generate_code("FUR")
                        })
                        allocated += 1
                save_data(f"furniture_{school_name}.json", furniture)
                st.success(f"✅ Allocated furniture to {allocated} students!")
    st.markdown('</div>', unsafe_allow_html=True)

def render_returns():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">↩️ Return Items</h3>', unsafe_allow_html=True)
    
    school_name = st.session_state.school['name']
    search = st.text_input("🔍 Search", placeholder="Search by name, admission number, or book number", key="ret_search")
    
    if st.button("🔍 Search Items", use_container_width=True, key="ret_search_btn"):
        borrowed = load_data(f"borrowed_{school_name}.json", [])
        furniture = load_data(f"furniture_{school_name}.json", [])
        
        active_borrowed = [b for b in borrowed if not b.get('returned') 
                          and (search.lower() in b.get('name', '').lower() 
                               or search in b.get('adm', '') 
                               or search in b.get('bookNo', ''))]
        
        st.markdown('<h4 style="color: #FFFFFF;">📚 Books</h4>', unsafe_allow_html=True)
        if active_borrowed:
            for item in active_borrowed:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f'<p style="color: #FFFFFF;"><strong>{item["name"]}</strong> - {item["bookTitle"]} (#{item["bookNo"]})</p>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<p style="color: #FFFFFF;">Due: {item["returnDate"]}</p>', unsafe_allow_html=True)
                with col3:
                    if st.button("↩️ Return", key=f"ret_book_{item['id']}"):
                        item['returned'] = True
                        item['actualReturnDate'] = datetime.now().strftime('%Y-%m-%d')
                        books = load_data(f"books_{school_name}.json", [])
                        book = next((b for b in books if b['title'] == item['bookTitle']), None)
                        if book:
                            book['quantity'] += 1
                        save_data(f"books_{school_name}.json", books)
                        save_data(f"borrowed_{school_name}.json", borrowed)
                        st.success("✅ Book returned!")
                        st.rerun()
        else:
            st.info("No matching borrowed books")
        
        active_furniture = [f for f in furniture if not f.get('returned')
                           and (search.lower() in f.get('name', '').lower()
                                or search in f.get('adm', '')
                                or search in f.get('chair', '')
                                or search in f.get('locker', ''))]
        
        st.markdown('<h4 style="color: #FFFFFF;">🪑 Furniture</h4>', unsafe_allow_html=True)
        if active_furniture:
            for item in active_furniture:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f'<p style="color: #FFFFFF;"><strong>{item["name"]}</strong> - Chair: {item.get("chair", "-")}, Locker: {item.get("locker", "-")}</p>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<p style="color: #FFFFFF;">Date: {item["date"]}</p>', unsafe_allow_html=True)
                with col3:
                    if st.button("↩️ Return", key=f"ret_fur_{item['id']}"):
                        item['returned'] = True
                        save_data(f"furniture_{school_name}.json", furniture)
                        st.success("✅ Furniture returned!")
                        st.rerun()
        else:
            st.info("No matching furniture allocations")
    st.markdown('</div>', unsafe_allow_html=True)

def render_borrowed():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">📋 Borrowed Books</h3>', unsafe_allow_html=True)
    
    school_name = st.session_state.school['name']
    borrowed = load_data(f"borrowed_{school_name}.json", [])
    
    filter_option = st.radio("🔍 Filter", ["📋 All", "✅ Active", "🔴 Overdue"], horizontal=True, key="bor_filter")
    
    today = datetime.now()
    
    if filter_option == "✅ Active":
        filtered = [b for b in borrowed if not b.get('returned', False)]
    elif filter_option == "🔴 Overdue":
        filtered = [b for b in borrowed if not b.get('returned', False) 
                   and datetime.strptime(b.get('returnDate', '2000-01-01'), '%Y-%m-%d') < today]
    else:
        filtered = borrowed
    
    if filtered:
        df = pd.DataFrame(filtered)
        st.dataframe(df, use_container_width=True)
        
        if st.button("📎 Export to Excel", use_container_width=True, key="bor_export"):
            towrite = BytesIO()
            with pd.ExcelWriter(towrite, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Borrowed Books')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="borrowed_books.xlsx" style="color: #28a745; font-weight: 600;">📥 Download Excel File</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.info("No records found")
    st.markdown('</div>', unsafe_allow_html=True)

def render_members():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">👥 Members</h3>', unsafe_allow_html=True)
    
    school_name = st.session_state.school['name']
    members = load_data(f"members_{school_name}.json", [])
    
    with st.form("add_member_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Name", placeholder="Enter member name")
        with col2:
            member_id = st.text_input("🔢 ID", placeholder="Enter member ID")
        
        if st.form_submit_button("➕ Add Member", use_container_width=True):
            if name:
                members.append({"name": name, "id": member_id or generate_code("MEM")})
                save_data(f"members_{school_name}.json", members)
                st.success("✅ Member added!")
                st.rerun()
    
    if members:
        for i, member in enumerate(members):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f'<p style="color: #FFFFFF;"><strong>{member["name"]}</strong> {f"- ID: {member["id"]}" if member.get("id") else ""}</p>', unsafe_allow_html=True)
            with col2:
                if st.button("✏️ Edit", key=f"edit_mem_{i}"):
                    st.session_state[f"editing_member_{i}"] = True
            with col3:
                if st.button("🗑️", key=f"del_mem_{i}"):
                    members.pop(i)
                    save_data(f"members_{school_name}.json", members)
                    st.rerun()
            
            if st.session_state.get(f"editing_member_{i}"):
                new_name = st.text_input("New name", member['name'], key=f"edit_name_{i}")
                if st.button("💾 Save", key=f"save_mem_{i}"):
                    members[i]['name'] = new_name
                    save_data(f"members_{school_name}.json", members)
                    st.session_state[f"editing_member_{i}"] = False
                    st.rerun()
    else:
        st.info("No members added yet")
    st.markdown('</div>', unsafe_allow_html=True)

def render_catalog():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">📚 Book Catalog</h3>', unsafe_allow_html=True)
    
    school_name = st.session_state.school['name']
    books = load_data(f"books_{school_name}.json", [])
    
    with st.form("add_book_form"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            title = st.text_input("📖 Book Title", placeholder="Enter book title")
        with col2:
            book_type = st.selectbox("📂 Type", ["Textbook", "Novel", "Reference", "Magazine", "Other"], key="cat_type")
        with col3:
            quantity = st.number_input("🔢 Quantity", 1, 1000, 1, key="cat_qty")
        
        if st.form_submit_button("📖 Add Book", use_container_width=True):
            if title:
                books.append({"title": title, "type": book_type, "quantity": quantity})
                save_data(f"books_{school_name}.json", books)
                st.success("✅ Book added!")
                st.rerun()
    
    if books:
        for i, book in enumerate(books):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.markdown(f'<p style="color: #FFFFFF;">📖 <strong>{book["title"]}</strong></p>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<p style="color: #FFFFFF;">{book["type"]}</p>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<p style="color: #FFFFFF;">Qty: {book["quantity"]}</p>', unsafe_allow_html=True)
            with col4:
                if st.button("🗑️", key=f"del_book_{i}"):
                    books.pop(i)
                    save_data(f"books_{school_name}.json", books)
                    st.rerun()
    else:
        st.info("No books in catalog")
    st.markdown('</div>', unsafe_allow_html=True)

def render_teachers():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">👨‍🏫 Teachers</h3>', unsafe_allow_html=True)
    
    school_name = st.session_state.school['name']
    teachers = load_data(f"teachers_{school_name}.json", [])
    
    with st.form("add_teacher_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("👤 Name", placeholder="Teacher name")
        with col2:
            subjects = st.text_input("📚 Subjects", placeholder="e.g., Math, English")
        with col3:
            class_assigned = st.text_input("📋 Class", placeholder="Assigned class")
        
        if st.form_submit_button("➕ Add Teacher", use_container_width=True):
            if name:
                teachers.append({"name": name, "subjects": subjects, "class_assigned": class_assigned, "id": generate_code("TCH")})
                save_data(f"teachers_{school_name}.json", teachers)
                st.success("✅ Teacher added!")
                st.rerun()
    
    if teachers:
        for i, teacher in enumerate(teachers):
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            with col1:
                st.markdown(f'<p style="color: #FFFFFF;"><strong>{teacher["name"]}</strong></p>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<p style="color: #FFFFFF;">{teacher.get("subjects", "-")}</p>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<p style="color: #FFFFFF;">{teacher.get("class_assigned", "-")}</p>', unsafe_allow_html=True)
            with col4:
                if st.button("🗑️", key=f"del_teacher_{i}"):
                    teachers.pop(i)
                    save_data(f"teachers_{school_name}.json", teachers)
                    st.rerun()
    else:
        st.info("No teachers added")
    st.markdown('</div>', unsafe_allow_html=True)

def render_classes():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">📋 Class Lists</h3>', unsafe_allow_html=True)
    
    school_name = st.session_state.school['name']
    classes = load_data(f"classes_{school_name}.json", [])
    
    uploaded_file = st.file_uploader("📥 Import Class List (Excel)", type=['xlsx', 'xls'], key="class_upload")
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.markdown('<p style="color: #FFFFFF; font-weight: 600;">Preview:</p>', unsafe_allow_html=True)
        st.dataframe(df.head(), use_container_width=True)
        
        class_name = st.text_input("💾 Save as Class Name", placeholder="e.g., Grade 4A", key="class_name_input")
        
        if st.button("💾 Save Class List", use_container_width=True, key="class_save"):
            if class_name:
                students = df.to_dict('records')
                classes.append({
                    "name": class_name,
                    "students": students,
                    "created": datetime.now().strftime("%Y-%m-%d")
                })
                save_data(f"classes_{school_name}.json", classes)
                st.success(f"✅ Saved class '{class_name}' with {len(students)} students!")
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
    st.markdown('<h3 style="color: #FFFFFF;">📱 QR Codes</h3>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📱 Generate QR", "📷 Scan QR"])
    
    with tab1:
        qr_type = st.selectbox("🏷️ QR Type", ["book", "chair", "locker"], key="qr_type")
        col1, col2 = st.columns(2)
        with col1:
            start_num = st.number_input("🔢 Start Number", 1, 10000, 1, key="qr_start")
        with col2:
            end_num = st.number_input("🔢 End Number", 1, 10000, 10, key="qr_end")
        
        if st.button("📱 Generate QR Codes", use_container_width=True, key="qr_generate"):
            qr_cols = st.columns(4)
            for i in range(start_num, min(end_num + 1, start_num + 20)):
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(f"{qr_type}-{i}")
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                col_idx = (i - start_num) % 4
                with qr_cols[col_idx]:
                    st.image(f"data:image/png;base64,{img_str}", caption=f"{qr_type.upper()}: {i}", width=150)
    
    with tab2:
        st.info("📷 Scan QR codes using the SRMS mobile scanner")
        qr_input = st.text_input("🔢 Or enter QR code manually", placeholder="e.g., book-5", key="qr_manual")
        if qr_input:
            st.success(f"✅ Scanned: {qr_input}")
    st.markdown('</div>', unsafe_allow_html=True)

def render_chat():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">💬 Staff Chat</h3>', unsafe_allow_html=True)
    
    school_name = st.session_state.school['name']
    user = st.session_state.user
    chat_messages = load_data(f"chat_messages_{school_name}.json", [])
    users = load_data(f"users_{school_name}.json", [])
    
    other_users = [u for u in users if u['email'] != user['email']]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown('<h4 style="color: #FFFFFF;">🟢 Staff Online</h4>', unsafe_allow_html=True)
        for u in other_users:
            if st.button(f"🟢 {u['name']}\n({u['role']})", key=f"chat_user_{u['email']}", use_container_width=True):
                st.session_state.chat_with = u['email']
    
    with col2:
        if 'chat_with' in st.session_state:
            chat_with = st.session_state.chat_with
            chat_user = next((u for u in users if u['email'] == chat_with), None)
            
            if chat_user:
                st.markdown(f'<h4 style="color: #FFFFFF;">💬 Chat with {chat_user["name"]}</h4>', unsafe_allow_html=True)
                
                msgs = [m for m in chat_messages 
                       if (m['from'] == user['email'] and m['to'] == chat_with) 
                       or (m['from'] == chat_with and m['to'] == user['email'])]
                
                for msg in sorted(msgs, key=lambda x: x['timestamp']):
                    is_mine = msg['from'] == user['email']
                    align = "flex-end" if is_mine else "flex-start"
                    
                    st.markdown(f"""
                    <div style="display: flex; justify-content: {align}; margin: 12px 0;">
                        <div class="chat-bubble {'chat-message-mine' if is_mine else ''}" 
                             style="max-width: 70%;">
                            <strong>{msg['from_name']}:</strong> {msg['message']}
                            <br><small style="color: rgba(255,255,255,0.5);">{msg['timestamp'][:16]}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with st.form("send_msg_form"):
                    msg_text = st.text_input("💬 Type a message...", key="chat_input", placeholder="Write your message here")
                    if st.form_submit_button("📤 Send", use_container_width=True):
                        if msg_text:
                            chat_messages.append({
                                "from": user['email'], "from_name": user['name'],
                                "to": chat_with, "message": msg_text,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "id": generate_code("MSG")
                            })
                            save_data(f"chat_messages_{school_name}.json", chat_messages)
                            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_audit_log():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">📝 Audit Log</h3>', unsafe_allow_html=True)
    
    school_name = st.session_state.school['name']
    audit_log = load_data(f"audit_log_{school_name}.json", [])
    
    if audit_log:
        df = pd.DataFrame(audit_log)
        st.dataframe(df, use_container_width=True)
        
        if st.button("📎 Export Log to Excel", use_container_width=True, key="log_export"):
            towrite = BytesIO()
            with pd.ExcelWriter(towrite, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Audit Log')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="audit_log.xlsx" style="color: #28a745; font-weight: 600;">📥 Download Excel File</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.info("No audit log entries")
    st.markdown('</div>', unsafe_allow_html=True)

def render_reports():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">📈 Reports</h3>', unsafe_allow_html=True)
    
    school_name = st.session_state.school['name']
    report_type = st.selectbox("📊 Report Type", ["Books", "Furniture", "Overdue", "Complete Summary"], key="report_type")
    
    if st.button("📊 Generate Report", use_container_width=True, key="report_gen"):
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
                st.success("✅ No overdue books!")
        elif report_type == "Complete Summary":
            books = load_data(f"books_{school_name}.json", [])
            borrowed = load_data(f"borrowed_{school_name}.json", [])
            members = load_data(f"members_{school_name}.json", [])
            teachers = load_data(f"teachers_{school_name}.json", [])
            furniture = load_data(f"furniture_{school_name}.json", [])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📚 Total Books", sum(b.get('quantity', 0) for b in books))
                st.metric("📖 Active Loans", len([b for b in borrowed if not b.get('returned')]))
            with col2:
                st.metric("👥 Members", len(members))
                st.metric("👨‍🏫 Teachers", len(teachers))
            with col3:
                active_furniture = len([f for f in furniture if not f.get('returned')])
                st.metric("🪑 Active Furniture", active_furniture)
                st.metric("📋 Classes", len(load_data(f"classes_{school_name}.json", [])))
            with col4:
                overdue_count = len([b for b in borrowed if not b.get('returned', False) 
                                    and datetime.strptime(b.get('returnDate', '2000-01-01'), '%Y-%m-%d') < datetime.now()])
                st.metric("🔴 Overdue", overdue_count)
                st.metric("📊 Total Transactions", len(borrowed) + len(furniture))
    st.markdown('</div>', unsafe_allow_html=True)

def render_settings():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFFFFF;">⚙️ Settings</h3>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🎨 Theme", "💾 Data", "🏫 School Info"])
    
    with tab1:
        st.markdown('<h4 style="color: #FFFFFF;">🎨 Theme Settings</h4>', unsafe_allow_html=True)
        wallpaper = st.selectbox("🖼️ Select Wallpaper", list(WALLPAPERS.keys()), 
                                 index=list(WALLPAPERS.keys()).index(st.session_state.wallpaper),
                                 key="settings_wallpaper")
        
        if st.button("🎨 Apply Theme", use_container_width=True, key="settings_apply_theme"):
            st.session_state.wallpaper = wallpaper
            st.rerun()
        
        if wallpaper != "None":
            st.image(WALLPAPERS[wallpaper], caption=f"Current: {wallpaper}", width=400)
    
    with tab2:
        st.markdown('<h4 style="color: #FFFFFF;">💾 Data Management</h4>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Backup Data", use_container_width=True, key="settings_backup"):
                school_name = st.session_state.school['name']
                all_data = {}
                for file in ["books", "members", "borrowed", "teachers", "classes", 
                           "furniture", "book_issues", "individual_lendings", 
                           "audit_log", "chat_messages"]:
                    all_data[file] = load_data(f"{file}_{school_name}.json", [])
                json_str = json.dumps(all_data, indent=2)
                b64 = base64.b64encode(json_str.encode()).decode()
                href = f'<a href="data:application/json;base64,{b64}" download="srms_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json" style="color: #28a745; font-weight: 600;">📥 Download Backup</a>'
                st.markdown(href, unsafe_allow_html=True)
        with col2:
            uploaded = st.file_uploader("📤 Restore Data", type=['json'], key="settings_restore")
            if uploaded:
                if st.button("📤 Restore Backup", use_container_width=True, key="settings_restore_btn"):
                    try:
                        data = json.load(uploaded)
                        school_name = st.session_state.school['name']
                        for file, file_data in data.items():
                            save_data(f"{file}_{school_name}.json", file_data)
                        st.success("✅ Data restored!")
                        st.rerun()
                    except:
                        st.error("❌ Invalid backup file!")
        with col3:
            st.markdown('<h5 style="color: #FF6B6B;">⚠️ Danger Zone</h5>', unsafe_allow_html=True)
            confirm = st.text_input("Type 'DELETE' to confirm", placeholder="DELETE", key="settings_delete_confirm")
            if st.button("⚠️ Clear All Data", use_container_width=True, key="settings_clear"):
                if confirm == "DELETE":
                    school_name = st.session_state.school['name']
                    for file in ["books", "members", "borrowed", "teachers", "classes", 
                               "furniture", "book_issues", "individual_lendings"]:
                        save_data(f"{file}_{school_name}.json", [])
                    st.error("🗑️ All data cleared!")
                    st.rerun()
                else:
                    st.warning("⚠️ Type 'DELETE' to confirm")
    
    with tab3:
        st.markdown('<h4 style="color: #FFFFFF;">🏫 School Information</h4>', unsafe_allow_html=True)
        school = st.session_state.school
        st.markdown(f"""
        <div class="glass-card">
            <p style="color: #FFFFFF;"><strong>🏫 School Name:</strong> {school['name']}</p>
            <p style="color: #FFFFFF;"><strong>📍 Address:</strong> {school.get('address', 'N/A')}</p>
            <p style="color: #FFFFFF;"><strong>👑 Admin:</strong> {school['admin_name']}</p>
            <p style="color: #FFFFFF;"><strong>📧 Email:</strong> {school['admin_email']}</p>
            <p style="color: #FFFFFF;"><strong>📞 Phone:</strong> {school.get('admin_phone', 'N/A')}</p>
            <p style="color: #FFFFFF;"><strong>🔑 Invite Code:</strong> <code style="font-size: 1.2em; background: rgba(212,175,55,0.2); padding: 5px 15px; border-radius: 8px;">{school['invite_code']}</code></p>
            <p style="color: #FFFFFF;"><strong>📅 Created:</strong> {school.get('created', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============== MAIN ==============
def main():
    if st.session_state.page == 'startup':
        startup_page()
    elif st.session_state.page == 'dashboard':
        dashboard_page()

if __name__ == "__main__":
    main()
