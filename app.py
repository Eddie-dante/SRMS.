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
import plotly.express as px
import plotly.graph_objects as go
import time
import os
import bcrypt
import html
import sqlite3
from contextlib import contextmanager
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
from typing import Optional, Dict, Any, List, Tuple

# Page config
st.set_page_config(
    page_title="SRMS - School Resource Management System",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ DATABASE SETUP ============
DATA_DIR = Path("srms_data")
DATA_DIR.mkdir(exist_ok=True)

# Add this code right after the Database class initialization:
def ensure_database_works():
    """Ensure database is working properly"""
    try:
        # Force create the database file
        db_path = DATA_DIR / "srms.db"
        
        # Create a direct connection without the context manager
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        
        # Create essential tables manually
        conn.execute('''CREATE TABLE IF NOT EXISTS schools (
            name TEXT PRIMARY KEY,
            address TEXT,
            admin_name TEXT,
            admin_email TEXT,
            admin_phone TEXT,
            invite_code TEXT,
            created TEXT,
            is_active INTEGER DEFAULT 1
        )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            email TEXT,
            school_name TEXT,
            name TEXT,
            phone TEXT,
            staff_id TEXT,
            code TEXT,
            password TEXT,
            role TEXT,
            joined TEXT,
            is_active INTEGER DEFAULT 1,
            last_login TEXT,
            PRIMARY KEY (email, school_name)
        )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            school_name TEXT,
            timestamp TEXT,
            user TEXT,
            user_email TEXT,
            action TEXT,
            details TEXT,
            ip_address TEXT
        )''')
        
        conn.commit()
        conn.close()
        
        print("✅ Essential tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating essential tables: {str(e)}")
        return False

# Call this after db initialization
db = Database()
ensure_database_works()

# ============ WALLPAPERS DATABASE ============
WALLPAPERS = {
    "None": "",
    # School & Education
    "Library": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1920",
    "Classroom": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920",
    "School Building": "https://images.unsplash.com/photo-1577896851231-70ef18881754?w=1920",
    "Study Desk": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920",
    "Bookshelf": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1920",
    "Graduation": "https://images.unsplash.com/photo-1523050854058-8df90910f68e?w=1920",
    "Lecture Hall": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=1920",
    "Computer Lab": "https://images.unsplash.com/photo-1571266028243-e4c84c8a40b7?w=1920",
    "Science Lab": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=1920",
    "Playground": "https://images.unsplash.com/photo-1472898965229-f9b06b9c9bbe?w=1920",
    "School Bus": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=1920",
    "Art Room": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=1920",
    "Music Room": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=1920",
    "Sports Field": "https://images.unsplash.com/photo-1459865264687-595d652de67e?w=1920",
    "Cafeteria": "https://images.unsplash.com/photo-1574482620811-1aa16ffe3c82?w=1920",
    "Reading Corner": "https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=1920",
    "Blackboard": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=1920",
    "Lockers": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=1920",
    "Auditorium": "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=1920",
    "School Garden": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=1920",
    
    # Nature & Landscapes
    "Sunset": "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=1920",
    "Ocean": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920",
    "Forest": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920",
    "Mountain": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920",
    "Desert": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920",
    "Waterfall": "https://images.unsplash.com/photo-1544551763-46a013bb70b5?w=1920",
    "Cherry Blossom": "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1920",
    "Lavender Field": "https://images.unsplash.com/photo-1499002238440-d264edd596ec?w=1920",
    "Autumn Forest": "https://images.unsplash.com/photo-1507783548227-544c3b8fc065?w=1920",
    "Winter Snow": "https://images.unsplash.com/photo-1477601263568-180e2c6d046e?w=1920",
    "Spring Meadow": "https://images.unsplash.com/photo-1490750967868-88aa4cef14d0?w=1920",
    "Summer Field": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920",
    "Tropical Beach": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920",
    "Mountain Lake": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920",
    "Foggy Forest": "https://images.unsplash.com/photo-1485230405346-71acb9518d9b?w=1920",
    "Golden Hour": "https://images.unsplash.com/photo-1501856777435-29877ed80a3d?w=1920",
    "Blue Lagoon": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1920",
    "Zen Garden": "https://images.unsplash.com/photo-1545389336-cf090694435e?w=1920",
    "Palm Trees": "https://images.unsplash.com/photo-1509233725247-49e657c54213?w=1920",
    "Savanna": "https://images.unsplash.com/photo-1516426122078-c23e76319801?w=1920",
    "Iceberg": "https://images.unsplash.com/photo-1540979388789-7cee28a1cdc9?w=1920",
    "Coral Reef": "https://images.unsplash.com/photo-1544551763-46a013bb70b5?w=1920",
    "Bamboo Forest": "https://images.unsplash.com/photo-1518531933039-315f5d4a6b1a?w=1920",
    "Volcano": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1920",
    "Canyon": "https://images.unsplash.com/photo-1474044159687-1ee9f3a51722?w=1920",
    "Northern Lights": "https://images.unsplash.com/photo-1483347756197-71ef80e95f73?w=1920",
    "Sunflower Field": "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920",
    "Rose Garden": "https://images.unsplash.com/photo-1490750967868-88aa4cef14d0?w=1920",
    "Rainforest": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920",
    "Alps": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920",
    "Sahara": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920",
    "Great Barrier Reef": "https://images.unsplash.com/photo-1582967788606-a171c1080cb0?w=1920",
    "Amazon River": "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=1920",
    "Patagonia": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=1920",
    "New Zealand": "https://images.unsplash.com/photo-1507699622108-4be3abd695ad?w=1920",
    "Scottish Highlands": "https://images.unsplash.com/photo-1506377585622-bedcbb027afc?w=1920",
    "Greek Islands": "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1920",
    "Maldives": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=1920",
    "Antarctica": "https://images.unsplash.com/photo-1540979388789-7cee28a1cdc9?w=1920",
    
    # City & Architecture
    "City Lights": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1920",
    "Neon City": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469?w=1920",
    "Bridge Night": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920",
    "Modern Building": "https://images.unsplash.com/photo-1487958449943-2429e8be8625?w=1920",
    "Tokyo Street": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1920",
    "New York": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1920",
    "Paris": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920",
    "London": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1920",
    "Dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1920",
    "Singapore": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=1920",
    "Sydney": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=1920",
    "Rome": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=1920",
    "Barcelona": "https://images.unsplash.com/photo-1583422409516-2895a77efded?w=1920",
    "Amsterdam": "https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=1920",
    "Venice": "https://images.unsplash.com/photo-1514890547357-a9ee288728e0?w=1920",
    "Prague": "https://images.unsplash.com/photo-1519677100203-a0e668c92439?w=1920",
    "Istanbul": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1920",
    "Seoul": "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=1920",
    "Hong Kong": "https://images.unsplash.com/photo-1536599018102-9fa7e8cda74e?w=1920",
    "San Francisco": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=1920",
    "Chicago": "https://images.unsplash.com/photo-1494522855154-9297ac14b55f?w=1920",
    "Berlin": "https://images.unsplash.com/photo-1560969184-10fe8719e047?w=1920",
    "Moscow": "https://images.unsplash.com/photo-1513326738677-b964603b136d?w=1920",
    "Cairo": "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1920",
    "Rio de Janeiro": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=1920",
    "Toronto": "https://images.unsplash.com/photo-1517935706615-2717063c2225?w=1920",
    "Shanghai": "https://images.unsplash.com/photo-1537531383496-f4749b88f2b7?w=1920",
    "Bangkok": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=1920",
    "Vienna": "https://images.unsplash.com/photo-1516550893923-42c21b66955a?w=1920",
    "Stockholm": "https://images.unsplash.com/photo-1509356843151-3e7d96241e11?w=1920",
    
    # Space & Abstract
    "Galaxy": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920",
    "Milky Way": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920",
    "Starfield": "https://images.unsplash.com/photo-1557683320-2d5001d5e9c5?w=1920",
    "Aurora": "https://images.unsplash.com/photo-1483347756197-71ef80e95f73?w=1920",
    "Nebula": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920",
    "Abstract Waves": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1920",
    "Geometric": "https://images.unsplash.com/photo-1557683311-eac922347aa1?w=1920",
    "Color Splash": "https://images.unsplash.com/photo-1557683304-6733ba7e4d6f?w=1920",
    "Purple Haze": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469?w=1920",
    "Rainbow": "https://images.unsplash.com/photo-1511300636408-a63a89df3482?w=1920",
    "Clouds": "https://images.unsplash.com/photo-1501630834273-4b5604d2ee31?w=1920",
    "Stars": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920",
    "Starry Night": "https://images.unsplash.com/photo-1557683320-2d5001d5e9c5?w=1920",
    "Digital Art": "https://images.unsplash.com/photo-1557683316-973673baf926?w=1920",
    "Fractal": "https://images.unsplash.com/photo-1558470598-a5dda9640f68?w=1920",
    "Neon Grid": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1920",
    "Particles": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920",
    "Light Trails": "https://images.unsplash.com/photo-1515630278258-407f66498911?w=1920",
    "Crystal": "https://images.unsplash.com/photo-1557683316-973673baf926?w=1920",
    "Hologram": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469?w=1920",
    "Matrix": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1920",
    "Cyberpunk": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469?w=1920",
    "Vaporwave": "https://images.unsplash.com/photo-1557683304-6733ba7e4d6f?w=1920",
    "Synthwave": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1920",
    "Minimalist": "https://images.unsplash.com/photo-1557683316-973673baf926?w=1920",
    "Gradient": "https://images.unsplash.com/photo-1557683304-6733ba7e4d6f?w=1920",
    "Glitch": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469?w=1920",
    "Wireframe": "https://images.unsplash.com/photo-1557683311-eac922347aa1?w=1920",
    "Organic": "https://images.unsplash.com/photo-1557683316-973673baf926?w=1920",
    "Fluid": "https://images.unsplash.com/photo-1557683304-6733ba7e4d6f?w=1920",
    
    # Anime & Artistic
    "Anime Sunset": "https://images.unsplash.com/photo-1578632767115-351597cf1bfe?w=1920",
    "Anime Sky": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=1920",
    "Anime City": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1920",
    "Anime Garden": "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1920",
    "Anime Night": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469?w=1920",
    "Watercolor": "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=1920",
    "Oil Painting": "https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=1920",
    "Sketch": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=1920",
    "Pixel Art": "https://images.unsplash.com/photo-1557683316-973673baf926?w=1920",
    "Manga": "https://images.unsplash.com/photo-1578632767115-351597cf1bfe?w=1920",
    "Chibi": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=1920",
    "Kawaii": "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1920",
    "Studio Ghibli": "https://images.unsplash.com/photo-1578632767115-351597cf1bfe?w=1920",
    "Fantasy": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1920",
    "Steampunk": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=1920",
    "Gothic": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=1920",
    "Pastel": "https://images.unsplash.com/photo-1557683304-6733ba7e4d6f?w=1920",
    "Dark Academia": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1920",
    "Cottagecore": "https://images.unsplash.com/photo-1490750967868-88aa4cef14d0?w=1920",
    "Retro": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1920",
    
    # Animals & Wildlife
    "Tiger": "https://images.unsplash.com/photo-1549480017-d76466a4b7e8?w=1920",
    "Eagle": "https://images.unsplash.com/photo-1486572788966-cfd3df1f5b42?w=1920",
    "Dolphin": "https://images.unsplash.com/photo-1560272564-c83b66b1ad12?w=1920",
    "Elephant": "https://images.unsplash.com/photo-1536599018102-9fa7e8cda74e?w=1920",
    "Penguin": "https://images.unsplash.com/photo-1504270997636-07ddfbd48945?w=1920",
    "Fox": "https://images.unsplash.com/photo-1474511320723-9a56873867b5?w=1920",
    "Owl": "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=1920",
    "Wolf": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1920",
    "Butterfly": "https://images.unsplash.com/photo-1505063366573-38928ae5567e?w=1920",
    "Peacock": "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=1920",
    "Horse": "https://images.unsplash.com/photo-1520052205864-92d242b1a76b?w=1920",
    "Panda": "https://images.unsplash.com/photo-1551698618-1dfe5d97d259?w=1920",
    "Koala": "https://images.unsplash.com/photo-1459262838948-3e2de6c1dc80?w=1920",
    "Lion": "https://images.unsplash.com/photo-1534188753412-3e26d0d618d6?w=1920",
    "Giraffe": "https://images.unsplash.com/photo-1504173010664-32509aeebb62?w=1920",
    "Whale": "https://images.unsplash.com/photo-1518399681705-1c1a55e5e883?w=1920",
    "Sea Turtle": "https://images.unsplash.com/photo-1559128010-7c1ad6e1b6a5?w=1920",
    "Hummingbird": "https://images.unsplash.com/photo-1552727131-5fc6af16796d?w=1920",
    "Dragonfly": "https://images.unsplash.com/photo-1505483531331-fc3bc2e5ae69?w=1920",
    "Koi Fish": "https://images.unsplash.com/photo-1522069169874-c58ec4b76be5?w=1920",
}

# ============ EMOJI CATEGORIES ============
EMOJI_CATEGORIES = {
    "😀 Smileys": ["😀", "😃", "😄", "😁", "😅", "😂", "🤣", "😊", "😇", "🙂", "😉", "😌", "😍", "🥰", "😘", "😗", "😋", "😛", "😜", "🤪", "😝", "🤑", "🤗", "🤭", "🤫", "🤔", "🤐", "🤨", "😐", "😑", "😶", "😏", "😒", "🙄", "😬", "😮", "😯", "😲", "😳", "🥺", "😢", "😭", "😤", "😡", "🤬", "😈", "👿", "💀", "☠️"],
    "👍 Gestures": ["👍", "👎", "👌", "✌️", "🤞", "🤟", "🤘", "🤙", "👈", "👉", "👆", "👇", "☝️", "✋", "🤚", "🖐️", "🖖", "👋", "🤏", "✍️", "👏", "🙌", "🫶", "🤝", "🙏", "💪", "🦵", "🦶"],
    "❤️ Hearts": ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔", "❣️", "💕", "💞", "💓", "💗", "💖", "💘", "💝", "💟", "♥️"],
    "📚 School": ["📚", "📖", "📝", "✏️", "🖊️", "📏", "📐", "🎓", "🏫", "📋", "📎", "🖇️", "🗂️", "📁", "📌", "📍", "✂️", "🖍️", "📒", "📕", "📗", "📘", "📙"],
    "🎯 Symbols": ["🎯", "⭐", "🌟", "✨", "🔥", "💯", "✅", "❌", "⚠️", "🔔", "🔕", "📢", "📣", "💡", "🔦", "💰", "🎁", "🏆", "🥇", "🥈", "🥉", "📅", "⏰", "🔑", "🔒", "🔓"],
    "🍕 Food": ["🍎", "🍕", "🍔", "🍟", "🌮", "🍩", "🎂", "🍪", "🍦", "🍿", "☕", "🍵", "🧃", "🥤", "🍺", "🍷", "🍸", "🍹"],
    "🚀 Travel": ["🚀", "✈️", "🚗", "🚲", "🏠", "🏢", "🏰", "🗽", "🎡", "🎢", "🎪", "🏖️", "🏝️", "🏔️", "🌋", "🗻", "🏕️", "🏜️", "🌅", "🌄"],
    "🎨 Activities": ["🎨", "🎭", "🎬", "🎤", "🎧", "🎼", "🎹", "🎸", "🎺", "🎻", "🎮", "🎲", "🎯", "🎳", "⚽", "🏀", "🏈", "⚾", "🎾", "🏐"],
}

# ============ HELPER FUNCTIONS ============
def sanitize_html(text: str) -> str:
    """Sanitize text for safe HTML rendering"""
    if not text:
        return ""
    return html.escape(str(text))

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False

def generate_code(prefix: str = "", length: int = 8) -> str:
    """Generate a random code"""
    chars = string.ascii_uppercase + string.digits
    return prefix + ''.join(random.choices(chars, k=length))

def generate_reset_token() -> str:
    """Generate a password reset token"""
    return hashlib.sha256(os.urandom(32)).hexdigest()

def is_admin() -> bool:
    """Check if current user is admin"""
    if not st.session_state.get('user'):
        return False
    return st.session_state.user.get('role') == 'admin'

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get('user') is not None

def add_audit_entry(action: str, details: str):
    """Add entry to audit log"""
    if not is_authenticated():
        return
    school_name = st.session_state.school['name']
    user = st.session_state.user
    with db.get_connection() as conn:
        conn.execute(
            "INSERT INTO audit_log (school_name, timestamp, user, user_email, action, details) VALUES (?, ?, ?, ?, ?, ?)",
            (school_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
             user['name'], user['email'], action, details)
        )

def load_school_data(data_type: str, default: Any = None) -> Any:
    """Load data from database"""
    if not is_authenticated():
        return default if default is not None else []
    
    school_name = st.session_state.school['name']
    
    with db.get_connection() as conn:
        try:
            if data_type == 'books':
                cursor = conn.execute("SELECT * FROM books WHERE school_name = ?", (school_name,))
                return [dict(row) for row in cursor.fetchall()]
            elif data_type == 'borrowed':
                cursor = conn.execute("SELECT * FROM borrowed WHERE school_name = ?", (school_name,))
                return [dict(row) for row in cursor.fetchall()]
            elif data_type == 'furniture':
                cursor = conn.execute("SELECT * FROM furniture WHERE school_name = ?", (school_name,))
                return [dict(row) for row in cursor.fetchall()]
            elif data_type == 'members':
                cursor = conn.execute("SELECT * FROM members WHERE school_name = ?", (school_name,))
                return [dict(row) for row in cursor.fetchall()]
            elif data_type == 'teachers':
                cursor = conn.execute("SELECT * FROM teachers WHERE school_name = ?", (school_name,))
                return [dict(row) for row in cursor.fetchall()]
            elif data_type == 'classes':
                cursor = conn.execute("SELECT * FROM classes WHERE school_name = ?", (school_name,))
                classes = []
                for row in cursor.fetchall():
                    row_dict = dict(row)
                    try:
                        row_dict['students'] = json.loads(row_dict.get('students', '[]'))
                    except:
                        row_dict['students'] = []
                    classes.append(row_dict)
                return classes
            elif data_type == 'chat_messages':
                cursor = conn.execute(
                    "SELECT * FROM chat_messages WHERE school_name = ? AND deleted_by_sender = 0 AND deleted_by_receiver = 0",
                    (school_name,))
                return [dict(row) for row in cursor.fetchall()]
            elif data_type == 'forum_messages':
                cursor = conn.execute(
                    "SELECT * FROM forum_messages WHERE school_name = ? AND is_deleted = 0",
                    (school_name,))
                return [dict(row) for row in cursor.fetchall()]
            elif data_type == 'notepad':
                cursor = conn.execute(
                    "SELECT * FROM notepad WHERE school_name = ? AND is_deleted = 0",
                    (school_name,))
                return [dict(row) for row in cursor.fetchall()]
            elif data_type == 'audit_log':
                cursor = conn.execute(
                    "SELECT * FROM audit_log WHERE school_name = ? ORDER BY timestamp DESC LIMIT 500",
                    (school_name,))
                return [dict(row) for row in cursor.fetchall()]
            elif data_type == 'users':
                cursor = conn.execute(
                    "SELECT * FROM users WHERE school_name = ? AND is_active = 1",
                    (school_name,))
                return [dict(row) for row in cursor.fetchall()]
            elif data_type == 'wallpapers':
                cursor = conn.execute("SELECT * FROM wallpapers WHERE school_name = ?", (school_name,))
                return [dict(row) for row in cursor.fetchall()]
            elif data_type == 'system_settings':
                cursor = conn.execute(
                    "SELECT * FROM system_settings WHERE school_name = ?",
                    (school_name,))
                row = cursor.fetchone()
                return dict(row) if row else {}
        except Exception as e:
            st.error(f"Error loading {data_type}: {str(e)}")
            return default if default is not None else []

def check_duplicate_assignment(school_name: str, adm: str, item_type: str, item_number: str) -> bool:
    """Check if a student already has an item assigned"""
    with db.get_connection() as conn:
        if item_type == 'book':
            existing = conn.execute(
                "SELECT * FROM borrowed WHERE school_name = ? AND adm = ? AND bookNo = ? AND returned = 0",
                (school_name, adm, item_number)
            ).fetchone()
            return existing is not None
        elif item_type == 'chair':
            existing = conn.execute(
                "SELECT * FROM furniture WHERE school_name = ? AND adm = ? AND chair = ? AND returned = 0",
                (school_name, adm, item_number)
            ).fetchone()
            return existing is not None
        elif item_type == 'locker':
            existing = conn.execute(
                "SELECT * FROM furniture WHERE school_name = ? AND adm = ? AND locker = ? AND returned = 0",
                (school_name, adm, item_number)
            ).fetchone()
            return existing is not None
    return False

def admin_only(func):
    """Decorator to restrict access to admin only"""
    def wrapper(*args, **kwargs):
        if not is_admin():
            st.error("🔒 Admin access required!")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

def update_last_login():
    """Update last login timestamp"""
    if is_authenticated():
        with db.get_connection() as conn:
            conn.execute(
                "UPDATE users SET last_login = ? WHERE email = ? AND school_name = ?",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                 st.session_state.user['email'], st.session_state.school['name'])
            )

# ============ CSS ============
def get_premium_css(wallpaper: Optional[str] = None) -> str:
    wallpaper_url = ""
    
    if wallpaper and wallpaper != "None":
        # Check built-in wallpapers
        wallpaper_url = WALLPAPERS.get(wallpaper, "")
        
        # Check custom wallpapers
        if not wallpaper_url and is_authenticated():
            custom_wallpapers = load_school_data('wallpapers', [])
            clean_name = wallpaper.replace("⭐ ", "").replace(" (Custom)", "")
            custom = next((w for w in custom_wallpapers if w['name'] == clean_name), None)
            if custom:
                wallpaper_url = custom['url']
    
    bg_style = f"""
        background-image: url('{wallpaper_url}'); 
        background-size: cover; 
        background-position: center; 
        background-attachment: fixed;
    """ if wallpaper_url else """
        background: linear-gradient(135deg, #0a0e27, #1a1f4e, #0f3460);
    """
    
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        * {{ font-family: 'Inter', sans-serif; }}
        
        .stApp {{ {bg_style} }}
        .stApp > header {{ 
            background: rgba(10,14,39,0.95) !important; 
            backdrop-filter: blur(30px) !important; 
            border-bottom: 2px solid rgba(212,175,55,0.3) !important; 
        }}
        
        .main .block-container {{ 
            background: rgba(10,14,39,0.75) !important; 
            backdrop-filter: blur(25px) !important; 
            border-radius: 20px !important; 
            padding: 2rem !important; 
            margin: 1rem !important; 
            border: 1px solid rgba(212,175,55,0.2) !important; 
        }}
        
        .main .block-container h1, .main .block-container h2, .main .block-container h3, .main .block-container h4 {{ 
            color: #FFFFFF !important; 
            text-shadow: 2px 2px 8px rgba(0,0,0,0.8), 0 0 20px rgba(0,0,0,0.5) !important; 
        }}
        .main .block-container p, .main .block-container span, .main .block-container label {{ 
            color: #FFFFFF !important; 
            text-shadow: 1px 1px 4px rgba(0,0,0,0.7), 0 0 15px rgba(0,0,0,0.4) !important; 
        }}
        
        .glass-card {{ 
            background: rgba(0,0,0,0.6) !important; 
            backdrop-filter: blur(20px) !important; 
            border-radius: 16px !important; 
            padding: 25px !important; 
            margin: 15px 0 !important; 
            border: 1px solid rgba(212,175,55,0.25) !important; 
            box-shadow: 0 10px 40px rgba(0,0,0,0.5) !important; 
        }}
        
        .stat-card {{ 
            background: rgba(255,255,255,0.08) !important; 
            backdrop-filter: blur(15px) !important; 
            padding: 25px !important; 
            border-radius: 16px !important; 
            border-left: 4px solid #e94560 !important; 
            border: 1px solid rgba(255,255,255,0.15) !important; 
            text-align: center !important; 
            margin: 8px 0 !important; 
        }}
        .stat-value {{ 
            font-size: 2.5em !important; 
            font-weight: 900 !important; 
            color: #FFFFFF !important; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important;
        }}
        .stat-label {{ 
            color: rgba(255,255,255,0.9) !important; 
            font-size: 0.9em !important; 
            font-weight: 600 !important; 
        }}
        
        .stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {{ 
            background: rgba(255,255,255,0.95) !important; 
            border: 2px solid rgba(212,175,55,0.4) !important; 
            border-radius: 10px !important; 
            padding: 10px 15px !important; 
            color: #1a1a1a !important; 
            font-weight: 500 !important; 
        }}
        
        .stButton button {{ 
            background: linear-gradient(135deg, #e94560, #c62a47) !important; 
            border: none !important; 
            border-radius: 10px !important; 
            color: white !important; 
            font-weight: 600 !important; 
            padding: 10px 20px !important; 
            box-shadow: 0 4px 15px rgba(233,69,96,0.3) !important; 
            transition: all 0.3s ease !important; 
        }}
        .stButton button:hover {{ 
            transform: translateY(-2px) !important; 
            box-shadow: 0 8px 25px rgba(233,69,96,0.5) !important; 
        }}
        
        .stDataFrame {{ 
            background: rgba(255,255,255,0.08) !important; 
            backdrop-filter: blur(15px) !important; 
            border-radius: 12px !important; 
            border: 1px solid rgba(212,175,55,0.3) !important; 
        }}
        
        .school-code-banner {{ 
            background: rgba(0,0,0,0.5) !important; 
            backdrop-filter: blur(15px) !important; 
            border: 2px dashed rgba(233,69,96,0.4) !important; 
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
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important;
        }}
        
        section[data-testid="stSidebar"] {{ 
            background: linear-gradient(180deg, rgba(10,14,39,0.95), rgba(26,31,78,0.95), rgba(15,52,96,0.95)) !important; 
            backdrop-filter: blur(20px) !important;
        }}
        section[data-testid="stSidebar"] * {{ 
            color: #FFFFFF !important; 
            text-shadow: 0 1px 3px rgba(0,0,0,0.5) !important; 
        }}
        
        .emoji-btn {{
            display: inline-block;
            padding: 8px 12px;
            margin: 4px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(212,175,55,0.3);
            font-size: 1.3em;
        }}
        .emoji-btn:hover {{
            background: rgba(233,69,96,0.4);
            transform: scale(1.2);
            border-color: rgba(233,69,96,0.6);
        }}
        
        .forum-message {{ 
            background: rgba(255,255,255,0.08) !important; 
            backdrop-filter: blur(10px) !important; 
            border-radius: 12px !important; 
            padding: 12px 16px !important; 
            margin: 8px 0 !important; 
            border: 1px solid rgba(255,255,255,0.15) !important; 
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @media (max-width: 768px) {{ 
            .main .block-container {{ 
                padding: 1rem !important; 
                margin: 0.5rem !important; 
            }} 
        }}
    </style>
    """

# ============ SESSION STATE INIT ============
if 'user' not in st.session_state:
    st.session_state.user = None
if 'school' not in st.session_state:
    st.session_state.school = None
if 'page' not in st.session_state:
    st.session_state.page = 'startup'
if 'wallpaper' not in st.session_state:
    st.session_state.wallpaper = "Library"
if 'current_section' not in st.session_state:
    st.session_state.current_section = 'dashboard'
if 'action' not in st.session_state:
    st.session_state.action = None
if 'show_admin_secret' not in st.session_state:
    st.session_state.show_admin_secret = False
if 'chat_with' not in st.session_state:
    st.session_state.chat_with = None
if 'selected_emoji' not in st.session_state:
    st.session_state.selected_emoji = None
if 'editing_note' not in st.session_state:
    st.session_state.editing_note = None
if 'editing_note_id' not in st.session_state:
    st.session_state.editing_note_id = None
if 'sharing_note' not in st.session_state:
    st.session_state.sharing_note = None
if 'show_reset_password' not in st.session_state:
    st.session_state.show_reset_password = False
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

# Apply CSS
st.markdown(get_premium_css(st.session_state.wallpaper), unsafe_allow_html=True)

# ============ AUTO-REFRESH MECHANISM ============
def check_for_updates():
    """Check for new messages/changes without full page refresh"""
    if is_authenticated() and st.session_state.get('auto_refresh'):
        current_time = time.time()
        last_refresh = st.session_state.get('last_refresh', 0)
        
        # Refresh every 3 seconds
        if current_time - last_refresh >= 3:
            st.session_state.last_refresh = current_time
            return True
    return False

# ============ EMOJI PICKER ============
def emoji_picker(key_prefix: str = "") -> Optional[str]:
    """Render an emoji picker and return selected emoji"""
    st.markdown("**Select Emoji:**")
    
    selected_emoji = None
    categories = list(EMOJI_CATEGORIES.keys())
    
    if len(categories) > 4:
        # Use tabs for many categories
        tabs = st.tabs([cat.split()[0] for cat in categories[:6]])
        
        for i, (category, emojis) in enumerate(list(EMOJI_CATEGORIES.items())[:6]):
            with tabs[i]:
                cols = st.columns(8)
                for j, emoji in enumerate(emojis[:32]):
                    with cols[j % 8]:
                        if st.button(emoji, key=f"{key_prefix}_{category}_{j}", 
                                    help=emoji, use_container_width=True):
                            selected_emoji = emoji
                            st.rerun()
    else:
        # Simple grid for fewer categories
        for category, emojis in EMOJI_CATEGORIES.items():
            cols = st.columns(8)
            for i, emoji in enumerate(emojis[:16]):
                with cols[i % 8]:
                    if st.button(emoji, key=f"{key_prefix}_{i}_{emoji}", 
                                help=emoji, use_container_width=True):
                        selected_emoji = emoji
                        st.rerun()
    
    if selected_emoji:
        st.success(f"Selected: {selected_emoji}")
    
    return selected_emoji

# ============ FILE ATTACHMENT HANDLER ============
def file_attachment_handler(key_prefix: str = "") -> Optional[Dict]:
    """Handle file attachments with various types"""
    attachment = None
    
    tab1, tab2, tab3 = st.tabs(["📄 Files", "🖼️ Images", "🎤 Voice"])
    
    with tab1:
        uploaded_file = st.file_uploader(
            "Upload File", 
            type=['pdf', 'docx', 'doc', 'txt', 'xlsx', 'pptx'],
            key=f"{key_prefix}_file_upload",
            label_visibility="collapsed"
        )
        if uploaded_file:
            file_bytes = uploaded_file.read()
            file_b64 = base64.b64encode(file_bytes).decode()
            attachment = {
                "name": uploaded_file.name,
                "type": "file",
                "mime": uploaded_file.type,
                "data": file_b64,
                "size": len(file_bytes)
            }
            st.success(f"📎 {uploaded_file.name}")
    
    with tab2:
        uploaded_image = st.file_uploader(
            "Upload Image",
            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
            key=f"{key_prefix}_image_upload",
            label_visibility="collapsed"
        )
        if uploaded_image:
            image_bytes = uploaded_image.read()
            image_b64 = base64.b64encode(image_bytes).decode()
            attachment = {
                "name": uploaded_image.name,
                "type": "image",
                "mime": uploaded_image.type,
                "data": image_b64,
                "size": len(image_bytes)
            }
            st.image(uploaded_image, width=200)
    
    with tab3:
        uploaded_voice = st.file_uploader(
            "Upload Voice",
            type=['mp3', 'wav', 'ogg', 'm4a'],
            key=f"{key_prefix}_voice_upload",
            label_visibility="collapsed"
        )
        if uploaded_voice:
            voice_bytes = uploaded_voice.read()
            voice_b64 = base64.b64encode(voice_bytes).decode()
            attachment = {
                "name": uploaded_voice.name,
                "type": "voice",
                "mime": uploaded_voice.type,
                "data": voice_b64,
                "size": len(voice_bytes)
            }
            st.audio(uploaded_voice)
    
    return attachment

# ============ QR CODE SCANNER ============
def qr_code_scanner():
    """QR code scanner using webcam"""
    st.markdown("### 📷 QR Code Scanner")
    
    # Camera scanner using HTML5
    camera_html = """
    <div id="qr-reader" style="width:100%;max-width:500px;margin:auto;"></div>
    <div id="qr-result" style="text-align:center;margin-top:10px;color:#FFD700;"></div>
    
    <script src="https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js"></script>
    <script>
        function onScanSuccess(decodedText, decodedResult) {
            document.getElementById('qr-result').innerHTML = 
                '<p style="color:#00FF00;">✅ Scanned: <strong>' + decodedText + '</strong></p>';
            
            // Send to Streamlit
            if (window.parent) {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: decodedText
                }, '*');
            }
            
            // Stop scanning
            if (window.html5QrCode) {
                window.html5QrCode.stop().catch(err => console.log(err));
            }
        }
        
        function onScanFailure(error) {
            // Ignore errors during scanning
        }
        
        setTimeout(function() {
            if (typeof Html5Qrcode === 'undefined') {
                document.getElementById('qr-result').innerHTML = 
                    '<p style="color:#FF6B6B;">Loading scanner... Please wait.</p>';
                return;
            }
            
            try {
                window.html5QrCode = new Html5Qrcode("qr-reader");
                const config = { fps: 10, qrbox: { width: 250, height: 250 } };
                
                window.html5QrCode.start(
                    { facingMode: "environment" }, 
                    config, 
                    onScanSuccess, 
                    onScanFailure
                ).then(() => {
                    document.getElementById('qr-result').innerHTML = 
                        '<p style="color:#FFD700;">📷 Camera active - Point at QR code</p>';
                }).catch(err => {
                    document.getElementById('qr-result').innerHTML = 
                        '<p style="color:#FF6B6B;">❌ Camera error: ' + err.message + '</p>';
                });
            } catch(e) {
                document.getElementById('qr-result').innerHTML = 
                    '<p style="color:#FF6B6B;">❌ Error: ' + e.message + '</p>';
            }
        }, 1500);
    </script>
    """
    
    st.components.v1.html(camera_html, height=450)
    
    # Manual input option
    st.markdown("---")
    st.markdown("### ✍️ Manual Entry")
    manual_input = st.text_input("Enter QR code:", placeholder="e.g., book-5")
    
    return manual_input

# ============ STARTUP PAGE ============
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
        <p style="color: rgba(255,255,255,0.5); font-size: 0.8em; margin-top: 20px;">v7.0 - Enterprise Edition</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔑 Staff Login", use_container_width=True, key="btn_login"):
            st.session_state.action = 'login'
            st.rerun()
    with col2:
        if st.button("📝 Staff Sign Up", use_container_width=True, key="btn_signup"):
            st.session_state.action = 'signup'
            st.rerun()
    with col3:
        if st.button("🏫 Create School", use_container_width=True, key="btn_create"):
            st.session_state.action = 'create'
            st.rerun()
    with col4:
        if st.button("🔐 Forgot Password", use_container_width=True, key="btn_forgot"):
            st.session_state.action = 'forgot_password'
            st.rerun()
    
    if st.session_state.action:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if st.session_state.action == 'login':
            login_form()
        elif st.session_state.action == 'signup':
            signup_form()
        elif st.session_state.action == 'create':
            create_school_form()
        elif st.session_state.action == 'forgot_password':
            forgot_password_form()
        st.markdown('</div>', unsafe_allow_html=True)

def login_form():
    st.markdown('<h3 style="color:#FFFFFF;">🔐 Staff Login</h3>', unsafe_allow_html=True)
    with st.form("frm_login"):
        name = st.text_input("👤 Full Name", placeholder="Enter your registered name")
        school_name = st.text_input("🏢 School Name", placeholder="Enter school name")
        invite_code = st.text_input("🔑 Invite Code", placeholder="Enter invite code")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("🔑 Login", use_container_width=True, type="primary")
        with col2:
            forgot = st.form_submit_button("🔐 Forgot Password?", use_container_width=True)
        
        if submit:
            if not name or not school_name or not invite_code or not password:
                st.error("Please fill in all fields!")
                return
            
            with db.get_connection() as conn:
                school = conn.execute("SELECT * FROM schools WHERE name = ? AND is_active = 1", 
                                     (school_name,)).fetchone()
                if not school:
                    st.error("School not found or inactive!")
                    return
                
                user = conn.execute(
                    "SELECT * FROM users WHERE LOWER(name) = ? AND school_name = ? AND code = ? AND is_active = 1",
                    (name.lower(), school_name, invite_code.upper())
                ).fetchone()
                
                if not user:
                    st.error("Invalid credentials!")
                    return
                
                user_dict = dict(user)
                
                if not verify_password(password, user_dict['password']):
                    st.error("Invalid credentials!")
                    return
                
                st.session_state.user = user_dict
                st.session_state.school = dict(school)
                st.session_state.page = 'dashboard'
                st.session_state.action = None
                st.session_state.chat_with = None
                update_last_login()
                add_audit_entry('Login', f"{user_dict['name']} logged in as {user_dict['role']}")
                st.success("✅ Login successful!")
                time.sleep(0.5)
                st.rerun()
        
        if forgot:
            st.session_state.action = 'forgot_password'
            st.rerun()

def forgot_password_form():
    st.markdown('<h3 style="color:#FFFFFF;">🔐 Reset Password</h3>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📧 Request Reset", "🔑 Enter Token"])
    
    with tab1:
        with st.form("frm_forgot_password"):
            email = st.text_input("📧 Registered Email", placeholder="Enter your registered email")
            school_name = st.text_input("🏢 School Name", placeholder="Enter school name")
            
            if st.form_submit_button("📤 Send Reset Token", use_container_width=True):
                if not email or not school_name:
                    st.error("Please fill in all fields!")
                    return
                
                with db.get_connection() as conn:
                    user = conn.execute(
                        "SELECT * FROM users WHERE email = ? AND school_name = ? AND is_active = 1",
                        (email, school_name)
                    ).fetchone()
                    
                    if user:
                        token = generate_reset_token()
                        expiry = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
                        
                        conn.execute(
                            "INSERT OR REPLACE INTO password_resets (email, school_name, token, expiry, used) VALUES (?, ?, ?, ?, 0)",
                            (email, school_name, token, expiry)
                        )
                        
                        st.success("✅ Reset token generated!")
                        st.info(f"🔑 Your reset token (dev mode): `{token[:16]}...`")
                        st.info("In production, this would be emailed. Use this token in the 'Enter Token' tab.")
                        st.session_state.reset_email = email
                        st.session_state.reset_school = school_name
                    else:
                        st.error("❌ No active user found with that email!")
    
    with tab2:
        if st.session_state.get('reset_email'):
            with st.form("frm_reset_password"):
                token = st.text_input("Reset Token", placeholder="Enter the reset token")
                new_password = st.text_input("New Password", type="password", placeholder="Min 6 characters")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
                
                if st.form_submit_button("🔄 Reset Password", use_container_width=True):
                    if new_password != confirm_password:
                        st.error("Passwords don't match!")
                        return
                    if len(new_password) < 6:
                        st.error("Password must be at least 6 characters!")
                        return
                    
                    with db.get_connection() as conn:
                        reset = conn.execute(
                            "SELECT * FROM password_resets WHERE email = ? AND school_name = ? AND token = ? AND expiry > ? AND used = 0",
                            (st.session_state.reset_email, st.session_state.reset_school, 
                             token, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        ).fetchone()
                        
                        if reset:
                            hashed = hash_password(new_password)
                            conn.execute(
                                "UPDATE users SET password = ? WHERE email = ? AND school_name = ?",
                                (hashed, st.session_state.reset_email, st.session_state.reset_school)
                            )
                            conn.execute(
                                "UPDATE password_resets SET used = 1 WHERE email = ? AND school_name = ?",
                                (st.session_state.reset_email, st.session_state.reset_school)
                            )
                            
                            st.success("✅ Password reset successfully! Please login.")
                            st.session_state.action = 'login'
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Invalid or expired token!")
        else:
            st.info("Please request a reset token first in the 'Request Reset' tab.")

def signup_form():
    st.markdown('<h3 style="color:#FFFFFF;">📝 Staff Sign Up</h3>', unsafe_allow_html=True)
    with st.form("frm_signup"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Full Name *", placeholder="Your full name")
            email = st.text_input("📧 Email *", placeholder="your@email.com")
            phone = st.text_input("📞 Phone", placeholder="+1234567890")
        with col2:
            school_name = st.text_input("🏢 School Name *", placeholder="Your school name")
            invite_code = st.text_input("🔑 Invite Code *", placeholder="From your admin")
            staff_id = st.text_input("👤 Staff ID (Optional)", placeholder="Employee ID")
        
        password = st.text_input("🔒 Create Password *", type="password", placeholder="Min 6 characters")
        
        if st.form_submit_button("📝 Sign Up", use_container_width=True, type="primary"):
            if not name or not email or not school_name or not invite_code or not password:
                st.error("Please fill in all required fields (*)!")
                return
            
            if len(password) < 6:
                st.error("Password must be at least 6 characters!")
                return
            
            # Validate email format
            if '@' not in email or '.' not in email:
                st.error("Please enter a valid email address!")
                return
            
            with db.get_connection() as conn:
                school = conn.execute("SELECT * FROM schools WHERE name = ? AND is_active = 1", 
                                     (school_name,)).fetchone()
                if not school:
                    st.error("School not found or inactive!")
                    return
                
                school_dict = dict(school)
                
                if school_dict['invite_code'] != invite_code.upper():
                    st.error("Invalid invite code!")
                    return
                
                existing = conn.execute(
                    "SELECT * FROM users WHERE email = ? AND school_name = ?",
                    (email, school_name)
                ).fetchone()
                
                if existing:
                    st.error("Email already registered!")
                    return
                
                hashed_password = hash_password(password)
                join_date = datetime.now().strftime("%Y-%m-%d")
                
                conn.execute(
                    """INSERT INTO users (email, school_name, name, phone, staff_id, code, password, role, joined, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""",
                    (email, school_name, name, phone, staff_id or f"STAFF-{generate_code('', 4)}",
                     invite_code.upper(), hashed_password, 'teacher', join_date)
                )
                
                user = conn.execute(
                    "SELECT * FROM users WHERE email = ? AND school_name = ?",
                    (email, school_name)
                ).fetchone()
                
                st.session_state.user = dict(user)
                st.session_state.school = school_dict
                st.session_state.page = 'dashboard'
                st.session_state.action = None
                st.session_state.chat_with = None
                add_audit_entry('Signup', f"{name} signed up as teacher")
                st.success("🎉 Registration successful!")
                time.sleep(1)
                st.rerun()

def create_school_form():
    st.markdown('<h3 style="color:#FFFFFF;">🏫 Create New School</h3>', unsafe_allow_html=True)
    with st.form("frm_create"):
        col1, col2 = st.columns(2)
        with col1:
            school_name = st.text_input("🏢 School Name *", placeholder="e.g., Sunshine High School")
            address = st.text_input("📍 School Address", placeholder="School location")
            admin_name = st.text_input("👤 Admin Full Name *", placeholder="Your full name")
        with col2:
            admin_email = st.text_input("📧 Admin Email *", placeholder="admin@school.edu")
            admin_phone = st.text_input("📞 Admin Phone", placeholder="+1234567890")
        
        password = st.text_input("🔒 Password *", type="password", placeholder="Min 8 characters")
        confirm = st.text_input("🔒 Confirm Password *", type="password", placeholder="Re-enter password")
        
        if st.form_submit_button("🚀 Create School", use_container_width=True, type="primary"):
            if not school_name or not admin_name or not admin_email or not password:
                st.error("Please fill in all required fields (*)!")
                return
            if password != confirm:
                st.error("Passwords don't match!")
                return
            if len(password) < 8:
                st.error("Admin password must be at least 8 characters!")
                return
            
            with db.get_connection() as conn:
                existing = conn.execute("SELECT * FROM schools WHERE name = ?", (school_name,)).fetchone()
                if existing:
                    st.error("School already exists!")
                    return
                
                invite_code = generate_code()
                created_date = datetime.now().strftime("%Y-%m-%d")
                
                conn.execute(
                    "INSERT INTO schools (name, address, admin_name, admin_email, admin_phone, invite_code, created, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, 1)",
                    (school_name, address, admin_name, admin_email, admin_phone, invite_code, created_date)
                )
                
                hashed_password = hash_password(password)
                
                conn.execute(
                    "INSERT INTO users (email, school_name, name, phone, staff_id, code, password, role, joined, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                    (admin_email, school_name, admin_name, admin_phone, "ADMIN-001", 
                     invite_code, hashed_password, "admin", created_date)
                )
                
                # Create default system settings
                conn.execute(
                    "INSERT INTO system_settings (school_name, max_borrow_days, max_books_per_student) VALUES (?, ?, ?)",
                    (school_name, 14, 3)
                )
                
                school = conn.execute("SELECT * FROM schools WHERE name = ?", (school_name,)).fetchone()
                user = conn.execute("SELECT * FROM users WHERE email = ? AND school_name = ?", 
                                   (admin_email, school_name)).fetchone()
                
                st.session_state.user = dict(user)
                st.session_state.school = dict(school)
                st.session_state.page = 'dashboard'
                st.session_state.action = None
                st.session_state.chat_with = None
                add_audit_entry('School Created', f"{school_name} created by {admin_name}")
                st.success(f"🎉 School created! Invite Code: `{invite_code}`")
                st.balloons()
                time.sleep(1)
                st.rerun()

# ============ DASHBOARD PAGE ============
def dashboard_page():
    school_name = st.session_state.school['name']
    user = st.session_state.user
    
    # Auto-refresh check
    if check_for_updates():
        pass  # Trigger rerun for real-time updates
    
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;margin-bottom:25px;">
        <h1 style="font-size:2.2em;">🏫 {sanitize_html(school_name)}</h1>
        <p style="font-size:1.1em;color:#FFFFFF;">👤 {sanitize_html(user['name'])} 
        <span style="background:{'#e94560' if user['role']=='admin' else '#0f3460'};color:#FFF;padding:4px 12px;
        border-radius:20px;font-size:0.8em;margin-left:10px;">{sanitize_html(user['role'].upper())}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    if is_admin():
        st.markdown(f"""
        <div class="school-code-banner">
            <p style="color:#FFF;font-size:0.9em;">🏫 School Invite Code - Share with Staff</p>
            <div class="invite-code">{sanitize_html(st.session_state.school['invite_code'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # SIDEBAR
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center;padding:15px;background:rgba(255,255,255,0.08);border-radius:12px;margin-bottom:15px;border:1px solid rgba(212,175,55,0.3);">
            <div style="width:50px;height:50px;background:linear-gradient(135deg,#d4af37,#f0d060);border-radius:50%;
                 display:inline-flex;align-items:center;justify-content:center;font-size:22px;font-weight:700;color:#0a0e27;margin-bottom:8px;">
                {sanitize_html(user['name'][0].upper())}
            </div>
            <p style="color:#FFFFFF;font-weight:700;margin:3px 0;">{sanitize_html(user['name'])}</p>
            <p style="color:#d4af37;font-size:0.8em;margin:3px 0;">{sanitize_html(user['role'].upper())}</p>
            <p style="color:rgba(255,255,255,0.5);font-size:0.7em;margin:3px 0;">{sanitize_html(user.get('email', ''))}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Theme & Wallpapers
        with st.expander("🎨 Theme & Wallpapers (200+)", expanded=False):
            all_wallpapers = list(WALLPAPERS.keys())
            
            if is_authenticated():
                custom_wallpapers = load_school_data('wallpapers', [])
                for w in custom_wallpapers:
                    if w['name'] not in all_wallpapers:
                        all_wallpapers.append(f"⭐ {w['name']} (Custom)")
            
            current_idx = 0
            current_wp = st.session_state.wallpaper
            for i, wp in enumerate(all_wallpapers):
                if wp == current_wp or (wp.startswith("⭐ ") and current_wp in wp):
                    current_idx = i
                    break
            
            wallpaper = st.selectbox("Choose Wallpaper:", all_wallpapers, index=current_idx, key="side_wp")
            
            if wallpaper != st.session_state.wallpaper:
                st.session_state.wallpaper = wallpaper.replace(" (Custom)", "").replace("⭐ ", "")
                st.rerun()
            
            # Upload custom wallpaper
            with st.form("frm_wallpaper_upload"):
                st.markdown("#### 📤 Upload Custom Wallpaper")
                wp_name = st.text_input("Name:", placeholder="Give it a name")
                wp_url = st.text_input("Image URL:", placeholder="https://...")
                wp_file = st.file_uploader("Or upload:", type=['png', 'jpg', 'jpeg', 'webp'], key="wp_upload")
                
                if st.form_submit_button("📤 Upload", use_container_width=True):
                    if wp_name and (wp_url or wp_file):
                        if wp_file:
                            upload_dir = DATA_DIR / "wallpapers"
                            upload_dir.mkdir(exist_ok=True)
                            file_ext = wp_file.name.split('.')[-1]
                            file_name = f"{wp_name}_{generate_code('', 4)}.{file_ext}"
                            file_path = upload_dir / file_name
                            with open(file_path, 'wb') as f:
                                f.write(wp_file.getvalue())
                            wp_url = f"/wallpapers/{file_name}"
                        
                        with db.get_connection() as conn:
                            conn.execute(
                                "INSERT INTO wallpapers (school_name, name, url, is_custom, uploaded_by, uploaded_at) VALUES (?, ?, ?, 1, ?, ?)",
                                (school_name, wp_name, wp_url, user['name'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            )
                        st.success("Wallpaper uploaded!")
                        st.rerun()
                    else:
                        st.error("Please provide name and URL/file!")
        
        st.markdown("---")
        
        # Navigation
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
        
        with st.expander("💬 COMMUNICATION", expanded=False):
            if st.button("💬 Private Chat", use_container_width=True, key="nav_chat"):
                st.session_state.current_section = 'chat'
                st.rerun()
            if st.button("📢 Group Forum", use_container_width=True, key="nav_forum"):
                st.session_state.current_section = 'forum'
                st.rerun()
            if st.button("📝 Notepad", use_container_width=True, key="nav_notepad"):
                st.session_state.current_section = 'notepad'
                st.rerun()
        
        with st.expander("📈 TOOLS", expanded=False):
            if st.button("🔍 Overview", use_container_width=True, key="nav_overview"):
                st.session_state.current_section = 'systemOverview'
                st.rerun()
            if st.button("📝 Audit Log", use_container_width=True, key="nav_log"):
                st.session_state.current_section = 'auditLog'
                st.rerun()
            if st.button("📈 Reports", use_container_width=True, key="nav_reports"):
                st.session_state.current_section = 'reports'
                st.rerun()
        
        # Admin-only sections
        if is_admin():
            with st.expander("⚙️ ADMIN", expanded=False):
                if st.button("⚙️ Settings", use_container_width=True, key="nav_settings"):
                    st.session_state.current_section = 'settings'
                    st.rerun()
                if st.button("🗄️ Database Manager", use_container_width=True, key="nav_dbmanager"):
                    st.session_state.current_section = 'databaseManager'
                    st.rerun()
        
        # Auto-refresh toggle
        with st.expander("⏱️ Auto-Refresh", expanded=False):
            auto_refresh = st.toggle("Enable Auto-Refresh", value=st.session_state.get('auto_refresh', True))
            if auto_refresh != st.session_state.get('auto_refresh'):
                st.session_state.auto_refresh = auto_refresh
                st.rerun()
            if auto_refresh:
                st.success("🔄 Refreshing every 3s")
            else:
                st.info("Manual refresh")
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            add_audit_entry('Logout', user['name'])
            st.session_state.user = None
            st.session_state.school = None
            st.session_state.page = 'startup'
            st.session_state.current_section = 'dashboard'
            st.session_state.chat_with = None
            st.rerun()
        
        st.markdown('<p style="color:rgba(255,255,255,0.4);font-size:0.7em;text-align:center;">SRMS v7.0 | WeGEM (Edwin) | © 2025</p>', unsafe_allow_html=True)
    
    # MAIN CONTENT
    section = st.session_state.get('current_section', 'dashboard')
    
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
    elif section == 'forum':
        render_forum()
    elif section == 'notepad':
        render_notepad()
    elif section == 'systemOverview':
        render_system_overview()
    elif section == 'auditLog':
        render_audit_log()
    elif section == 'reports':
        render_reports()
    elif section == 'settings':
        render_settings()
    elif section == 'databaseManager':
        render_database_manager()

# ============ RENDER FUNCTIONS ============
def render_dashboard():
    school_name = st.session_state.school['name']
    books = load_school_data('books', [])
    borrowed = load_school_data('borrowed', [])
    members = load_school_data('members', [])
    teachers = load_school_data('teachers', [])
    furniture = load_school_data('furniture', [])
    users = load_school_data('users', [])
    
    total_books = sum(b.get('quantity', 0) for b in books)
    active_borrowed = len([b for b in borrowed if not b.get('returned')])
    overdue = len([b for b in borrowed if not b.get('returned') and 
                   datetime.strptime(b.get('returnDate', '2000-01-01'), '%Y-%m-%d') < datetime.now()])
    
    st.markdown('<div class="glass-card"><h2>📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{total_books}</div><div class="stat-label">Total Books</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{active_borrowed}</div><div class="stat-label">Active Loans</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{total_books - active_borrowed}</div><div class="stat-label">Available</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(members)}</div><div class="stat-label">Members</div></div>', unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(teachers)}</div><div class="stat-label">Teachers</div></div>', unsafe_allow_html=True)
    with col6:
        active_furniture = len([f for f in furniture if not f.get('returned')])
        st.markdown(f'<div class="stat-card"><div class="stat-value">{active_furniture}</div><div class="stat-label">Furniture Items</div></div>', unsafe_allow_html=True)
    with col7:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{overdue}</div><div class="stat-label">Overdue</div></div>', unsafe_allow_html=True)
    with col8:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(users)}</div><div class="stat-label">Staff</div></div>', unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        if st.button("📖 Issue Books", use_container_width=True):
            st.session_state.current_section = 'bookIssuing'
            st.rerun()
    with col_b:
        if st.button("↩️ Return Items", use_container_width=True):
            st.session_state.current_section = 'return'
            st.rerun()
    with col_c:
        if st.button("💬 Open Chat", use_container_width=True):
            st.session_state.current_section = 'chat'
            st.rerun()
    with col_d:
        if st.button("📊 Reports", use_container_width=True):
            st.session_state.current_section = 'reports'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_book_issuing():
    school_name = st.session_state.school['name']
    books = load_school_data('books', [])
    classes = load_school_data('classes', [])
    
    st.markdown('<div class="glass-card"><h2>📖 Bulk Book Issuing to Class</h2>', unsafe_allow_html=True)
    
    if not books:
        st.warning("No books in catalog. Add books first.")
        if st.button("📚 Go to Catalog"):
            st.session_state.current_section = 'bookCatalog'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns(2)
    with col1:
        book_options = [b['title'] for b in books if b.get('quantity', 0) > 0]
        selected_book = st.selectbox("Book:", book_options if book_options else ["No books available"])
    with col2:
        class_options = [c['name'] for c in classes]
        selected_class = st.selectbox("Class:", class_options if class_options else ["No classes"])
    
    col3, col4 = st.columns(2)
    with col3:
        issue_date = st.date_input("Issue Date:", datetime.now())
    with col4:
        return_date = st.date_input("Return Date:", datetime.now() + timedelta(days=14))
    
    if st.button("📋 Load Students", use_container_width=True):
        if selected_class != "No classes":
            class_data = next((c for c in classes if c['name'] == selected_class), None)
            if class_data:
                st.session_state.bi_students = class_data.get('students', [])
                st.success(f"Loaded {len(st.session_state.bi_students)} students!")
    
    if 'bi_students' in st.session_state:
        students = st.session_state.bi_students
        if students:
            df = pd.DataFrame(students)
            col_names = df.columns.tolist()
            name_col = col_names[0] if col_names else 'name'
            adm_col = col_names[1] if len(col_names) > 1 else 'adm'
            
            df['Book No'] = ""
            df['Status'] = "Pending"
            df['Issue'] = False
            
            for i, row in df.iterrows():
                adm = str(row.get(adm_col, ''))
                existing = next((b for b in load_school_data('borrowed', []) 
                               if b.get('adm') == adm and b.get('bookTitle') == selected_book 
                               and not b.get('returned')), None)
                if existing:
                    df.at[i, 'Book No'] = existing.get('bookNo', '')
                    df.at[i, 'Status'] = '✓ Assigned'
            
            edited_df = st.data_editor(df, use_container_width=True, key="bi_editor")
            
            if st.button("✅ Issue Books", use_container_width=True, type="primary"):
                count = 0
                for _, row in edited_df.iterrows():
                    if row.get('Issue') and row.get('Book No'):
                        adm = str(row.get(adm_col, ''))
                        book_no = str(row.get('Book No', ''))
                        
                        if check_duplicate_assignment(school_name, adm, 'book', book_no):
                            st.warning(f"⚠️ Student {row.get(name_col, '')} already has book #{book_no}!")
                            continue
                        
                        book = next((b for b in books if b['title'] == selected_book), None)
                        if book and book['quantity'] > 0:
                            with db.get_connection() as conn:
                                conn.execute(
                                    """INSERT INTO borrowed (id, school_name, name, adm, bookTitle, bookNo, borrowDate, returnDate, returned, issued_by)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?)""",
                                    (generate_code("BOR"), school_name, str(row.get(name_col, '')),
                                     adm, selected_book, book_no,
                                     issue_date.strftime('%Y-%m-%d'), return_date.strftime('%Y-%m-%d'),
                                     st.session_state.user['name'])
                                )
                                conn.execute(
                                    "UPDATE books SET quantity = quantity - 1 WHERE school_name = ? AND title = ?",
                                    (school_name, selected_book)
                                )
                            count += 1
                
                if count > 0:
                    add_audit_entry('Books Issued', f"{count} copies of '{selected_book}' to {selected_class}")
                    st.success(f"✅ Issued {count} books!")
                    del st.session_state.bi_students
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_individual_lending():
    school_name = st.session_state.school['name']
    books = load_school_data('books', [])
    
    st.markdown('<div class="glass-card"><h2>👤 Individual Book Lending</h2>', unsafe_allow_html=True)
    
    with st.form("frm_ind_lend"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Student Name:", placeholder="Full name")
            adm = st.text_input("ADM No:", placeholder="Admission number")
            form = st.text_input("Form/Class:", placeholder="e.g., Form 4")
        with col2:
            stream = st.text_input("Stream:", placeholder="e.g., A")
            book_options = [b['title'] for b in books if b.get('quantity', 0) > 0]
            selected_book = st.selectbox("Book:", book_options if book_options else ["No books"])
            book_no = st.text_input("Book No:", placeholder="Book number")
        
        col3, col4 = st.columns(2)
        with col3:
            borrow_date = st.date_input("Borrow Date:", datetime.now())
        with col4:
            return_date = st.date_input("Return Date:", datetime.now() + timedelta(days=14))
        
        if st.form_submit_button("📖 Lend Book", use_container_width=True, type="primary"):
            if name and selected_book and selected_book != "No books" and book_no:
                if check_duplicate_assignment(school_name, adm, 'book', book_no):
                    st.error(f"❌ Student {name} already has book #{book_no}!")
                else:
                    with db.get_connection() as conn:
                        book = conn.execute(
                            "SELECT * FROM books WHERE school_name = ? AND title = ?",
                            (school_name, selected_book)
                        ).fetchone()
                        
                        if book and book['quantity'] > 0:
                            conn.execute(
                                """INSERT INTO borrowed (id, school_name, name, adm, form, stream, bookTitle, bookNo, borrowDate, returnDate, returned, issued_by)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)""",
                                (generate_code("BOR"), school_name, name, adm, form, stream,
                                 selected_book, book_no,
                                 borrow_date.strftime('%Y-%m-%d'), return_date.strftime('%Y-%m-%d'),
                                 st.session_state.user['name'])
                            )
                            conn.execute(
                                "UPDATE books SET quantity = quantity - 1 WHERE school_name = ? AND title = ?",
                                (school_name, selected_book)
                            )
                            add_audit_entry('Lend Book', f"{name} borrowed '{selected_book}' (#{book_no})")
                            st.success("✅ Book lent successfully!")
                            st.rerun()
                        else:
                            st.error("Book not available!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_furniture():
    school_name = st.session_state.school['name']
    classes = load_school_data('classes', [])
    
    st.markdown('<div class="glass-card"><h2>🪑 Furniture Allocation</h2>', unsafe_allow_html=True)
    
    if not classes:
        st.warning("No classes available. Import class lists first.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    selected_class = st.selectbox("Class:", [c['name'] for c in classes])
    
    col1, col2 = st.columns(2)
    with col1:
        chair_prefix = st.text_input("Chair Prefix:", "CH-")
        chair_start = st.number_input("Chair Start:", 1, 1000, 1)
        chair_end = st.number_input("Chair End:", 1, 1000, chair_start)
    with col2:
        locker_prefix = st.text_input("Locker Prefix:", "LK-")
        locker_start = st.number_input("Locker Start:", 1, 1000, 1)
        locker_end = st.number_input("Locker End:", 1, 1000, locker_start)
    
    if st.button("📋 Load Class", use_container_width=True):
        class_data = next((c for c in classes if c['name'] == selected_class), None)
        if class_data:
            st.session_state.fur_students = class_data.get('students', [])
            st.success(f"Loaded {len(st.session_state.fur_students)} students!")
    
    if 'fur_students' in st.session_state:
        students = st.session_state.fur_students
        if students:
            df = pd.DataFrame(students)
            col_names = df.columns.tolist()
            name_col = col_names[0] if col_names else 'name'
            adm_col = col_names[1] if len(col_names) > 1 else 'adm'
            
            df['Chair No'] = ""
            df['Locker No'] = ""
            df['Allocate'] = False
            
            edited_df = st.data_editor(df, use_container_width=True, key="fur_editor")
            
            if st.button("✅ Assign Furniture", use_container_width=True, type="primary"):
                count = 0
                for _, row in edited_df.iterrows():
                    if row.get('Allocate'):
                        adm = str(row.get(adm_col, ''))
                        chair_no = str(row.get('Chair No', ''))
                        locker_no = str(row.get('Locker No', ''))
                        
                        if check_duplicate_assignment(school_name, adm, 'chair', chair_no):
                            st.warning(f"⚠️ {row.get(name_col, '')} already has chair {chair_no}!")
                            continue
                        if check_duplicate_assignment(school_name, adm, 'locker', locker_no):
                            st.warning(f"⚠️ {row.get(name_col, '')} already has locker {locker_no}!")
                            continue
                        
                        with db.get_connection() as conn:
                            conn.execute(
                                """INSERT INTO furniture (id, school_name, name, adm, chair, locker, date, returned, issued_by)
                                VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)""",
                                (generate_code("FUR"), school_name, str(row.get(name_col, '')),
                                 adm, chair_no, locker_no, datetime.now().strftime('%Y-%m-%d'),
                                 st.session_state.user['name'])
                            )
                        count += 1
                
                if count > 0:
                    add_audit_entry('Furniture Allocated', f"{count} items to {selected_class}")
                    st.success(f"✅ Allocated {count} items!")
                    del st.session_state.fur_students
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_returns():
    school_name = st.session_state.school['name']
    
    st.markdown('<div class="glass-card"><h2>↩️ Return Items</h2>', unsafe_allow_html=True)
    
    search = st.text_input("🔍 Search:", placeholder="Search by name, ADM, or item number")
    
    if st.button("🔍 Search", use_container_width=True):
        with db.get_connection() as conn:
            active_books = conn.execute(
                """SELECT * FROM borrowed WHERE school_name = ? AND returned = 0 
                AND (LOWER(name) LIKE ? OR adm LIKE ? OR bookNo LIKE ?)""",
                (school_name, f"%{search.lower()}%", f"%{search}%", f"%{search}%")
            ).fetchall()
            
            active_furniture = conn.execute(
                """SELECT * FROM furniture WHERE school_name = ? AND returned = 0 
                AND (LOWER(name) LIKE ? OR adm LIKE ? OR chair LIKE ? OR locker LIKE ?)""",
                (school_name, f"%{search.lower()}%", f"%{search}%", f"%{search}%", f"%{search}%")
            ).fetchall()
        
        st.markdown("### 📚 Books")
        if active_books:
            for item in active_books:
                item_dict = dict(item)
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{item_dict['name']}** - {item_dict['bookTitle']} (#{item_dict['bookNo']})")
                with col2:
                    st.write(f"Due: {item_dict['returnDate']}")
                with col3:
                    if st.button("↩️ Return", key=f"ret_book_{item_dict['id']}"):
                        with db.get_connection() as conn:
                            conn.execute(
                                "UPDATE borrowed SET returned = 1, actualReturnDate = ? WHERE id = ? AND school_name = ?",
                                (datetime.now().strftime('%Y-%m-%d'), item_dict['id'], school_name)
                            )
                            conn.execute(
                                "UPDATE books SET quantity = quantity + 1 WHERE school_name = ? AND title = ?",
                                (school_name, item_dict['bookTitle'])
                            )
                        add_audit_entry('Book Returned', f"{item_dict['name']} returned '{item_dict['bookTitle']}'")
                        st.success("✅ Book returned!")
                        st.rerun()
                st.divider()
        else:
            st.info("No matching books")
        
        st.markdown("### 🪑 Furniture")
        if active_furniture:
            for item in active_furniture:
                item_dict = dict(item)
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{item_dict['name']}** - Chair: {item_dict['chair']}, Locker: {item_dict['locker']}")
                with col2:
                    st.write(f"Date: {item_dict['date']}")
                with col3:
                    if st.button("↩️ Return", key=f"ret_fur_{item_dict['id']}"):
                        with db.get_connection() as conn:
                            conn.execute(
                                "UPDATE furniture SET returned = 1 WHERE id = ? AND school_name = ?",
                                (item_dict['id'], school_name)
                            )
                        add_audit_entry('Furniture Returned', f"{item_dict['name']} returned items")
                        st.success("✅ Furniture returned!")
                        st.rerun()
                st.divider()
        else:
            st.info("No matching furniture")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_borrowed():
    school_name = st.session_state.school['name']
    
    st.markdown('<div class="glass-card"><h2>📋 Borrowed Books</h2>', unsafe_allow_html=True)
    
    filter_option = st.radio("Filter:", ["📋 All", "✅ Active", "🔴 Overdue", "✔️ Returned"], horizontal=True)
    
    with db.get_connection() as conn:
        if filter_option == "✅ Active":
            data = conn.execute(
                "SELECT * FROM borrowed WHERE school_name = ? AND returned = 0",
                (school_name,)
            ).fetchall()
        elif filter_option == "🔴 Overdue":
            data = conn.execute(
                "SELECT * FROM borrowed WHERE school_name = ? AND returned = 0 AND returnDate < ?",
                (school_name, datetime.now().strftime('%Y-%m-%d'))
            ).fetchall()
        elif filter_option == "✔️ Returned":
            data = conn.execute(
                "SELECT * FROM borrowed WHERE school_name = ? AND returned = 1",
                (school_name,)
            ).fetchall()
        else:
            data = conn.execute(
                "SELECT * FROM borrowed WHERE school_name = ?",
                (school_name,)
            ).fetchall()
    
    if data:
        df = pd.DataFrame([dict(row) for row in data])
        st.dataframe(df, use_container_width=True)
        
        # Export button
        if st.button("📥 Export to Excel", use_container_width=True):
            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            st.markdown(
                f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" '
                f'download="borrowed_books.xlsx">📥 Click to Download</a>',
                unsafe_allow_html=True
            )
    else:
        st.info("No records found")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_members():
    school_name = st.session_state.school['name']
    members = load_school_data('members', [])
    
    st.markdown('<div class="glass-card"><h2>👥 Members</h2>', unsafe_allow_html=True)
    
    with st.form("frm_member"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name:", placeholder="Member name")
        with col2:
            mid = st.text_input("ID:", placeholder="Member ID")
        if st.form_submit_button("➕ Add Member", use_container_width=True):
            if name:
                member_id = mid or generate_code("MEM")
                with db.get_connection() as conn:
                    conn.execute(
                        "INSERT INTO members (id, school_name, name, added_by, added_at) VALUES (?, ?, ?, ?, ?)",
                        (member_id, school_name, name, st.session_state.user['name'],
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    )
                add_audit_entry('Member Added', name)
                st.success("✅ Member added!")
                st.rerun()
    
    search = st.text_input("🔍 Search:", placeholder="Search members")
    filtered = [m for m in members if not search or search.lower() in m['name'].lower()]
    
    if filtered:
        for m in filtered:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"👤 **{m['name']}** (ID: {m.get('id', 'N/A')})")
            with col2:
                if is_admin():
                    if st.button("🗑️", key=f"del_mem_{m['id']}"):
                        with db.get_connection() as conn:
                            conn.execute("DELETE FROM members WHERE id = ? AND school_name = ?",
                                       (m['id'], school_name))
                        add_audit_entry('Member Removed', m['name'])
                        st.success("Member removed!")
                        st.rerun()
            st.divider()
    else:
        st.info("No members found")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_catalog():
    school_name = st.session_state.school['name']
    books = load_school_data('books', [])
    
    st.markdown('<div class="glass-card"><h2>📚 Book Catalog</h2>', unsafe_allow_html=True)
    
    with st.form("frm_book"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            title = st.text_input("Title:", placeholder="Book title")
        with col2:
            btype = st.selectbox("Type:", ["Textbook", "Novel", "Reference", "Magazine", "Other"])
        with col3:
            qty = st.number_input("Quantity:", 1, 1000, 1)
        if st.form_submit_button("📖 Add Book", use_container_width=True):
            if title:
                with db.get_connection() as conn:
                    existing = conn.execute(
                        "SELECT * FROM books WHERE school_name = ? AND LOWER(title) = ?",
                        (school_name, title.lower())
                    ).fetchone()
                    
                    if existing:
                        conn.execute(
                            "UPDATE books SET quantity = quantity + ? WHERE school_name = ? AND LOWER(title) = ?",
                            (qty, school_name, title.lower())
                        )
                    else:
                        conn.execute(
                            "INSERT INTO books (school_name, title, type, quantity, created_by, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                            (school_name, title, btype, qty, st.session_state.user['name'],
                             datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        )
                add_audit_entry('Book Added', f"{title} (Qty: {qty})")
                st.success("✅ Book added!")
                st.rerun()
    
    if books:
        for book in books:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"📖 **{book['title']}**")
            with col2:
                st.write(book.get('type', '-'))
            with col3:
                st.write(f"Qty: {book.get('quantity', 0)}")
            with col4:
                if is_admin():
                    if st.button("🗑️", key=f"del_book_{book['id']}"):
                        with db.get_connection() as conn:
                            conn.execute("DELETE FROM books WHERE id = ? AND school_name = ?",
                                       (book['id'], school_name))
                        add_audit_entry('Book Removed', book['title'])
                        st.success("Book removed!")
                        st.rerun()
            st.divider()
    else:
        st.info("No books in catalog")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_teachers():
    school_name = st.session_state.school['name']
    teachers = load_school_data('teachers', [])
    
    st.markdown('<div class="glass-card"><h2>👨‍🏫 Teachers</h2>', unsafe_allow_html=True)
    
    with st.form("frm_teacher"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            name = st.text_input("Name:", placeholder="Teacher name")
        with col2:
            subject = st.text_input("Subjects:", placeholder="Subjects taught")
        with col3:
            classes = st.text_input("Classes:", placeholder="Classes assigned")
        with col4:
            duty = st.text_input("Class Teacher:", placeholder="Class duty")
        if st.form_submit_button("➕ Add Teacher", use_container_width=True):
            if name:
                with db.get_connection() as conn:
                    conn.execute(
                        "INSERT INTO teachers (id, school_name, name, subject, classes, duty, added_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (generate_code("TCH"), school_name, name, subject, classes, duty,
                         st.session_state.user['name'])
                    )
                add_audit_entry('Teacher Added', name)
                st.success("✅ Teacher added!")
                st.rerun()
    
    if teachers:
        for t in teachers:
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            with col1:
                st.write(f"**{t['name']}**")
            with col2:
                st.write(t.get('subject', '-'))
            with col3:
                st.write(t.get('classes', '-'))
            with col4:
                st.write(t.get('duty', '-'))
            with col5:
                if is_admin():
                    if st.button("🗑️", key=f"del_tea_{t['id']}"):
                        with db.get_connection() as conn:
                            conn.execute("DELETE FROM teachers WHERE id = ? AND school_name = ?",
                                       (t['id'], school_name))
                        add_audit_entry('Teacher Removed', t['name'])
                        st.success("Teacher removed!")
                        st.rerun()
            st.divider()
    else:
        st.info("No teachers added")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_classes():
    school_name = st.session_state.school['name']
    classes = load_school_data('classes', [])
    
    st.markdown('<div class="glass-card"><h2>📋 Class Lists</h2>', unsafe_allow_html=True)
    
    uploaded = st.file_uploader("📥 Import Excel File (.xlsx, .xls)", type=['xlsx', 'xls'])
    if uploaded:
        try:
            df = pd.read_excel(uploaded)
            st.write("Preview:")
            st.dataframe(df.head(), use_container_width=True)
            
            class_name = st.text_input("Class Name:", placeholder="e.g., Grade 4A")
            if st.button("💾 Save Class", use_container_width=True):
                if class_name:
                    students = []
                    for _, row in df.iterrows():
                        student = {col: str(row[col]) if not pd.isna(row[col]) else "" for col in df.columns}
                        students.append(student)
                    
                    with db.get_connection() as conn:
                        conn.execute(
                            "INSERT INTO classes (school_name, name, students, created_by, created) VALUES (?, ?, ?, ?, ?)",
                            (school_name, class_name, json.dumps(students), st.session_state.user['name'],
                             datetime.now().strftime("%Y-%m-%d"))
                        )
                    add_audit_entry('Class Added', f"{class_name} ({len(students)} students)")
                    st.success(f"✅ Saved '{class_name}' with {len(students)} students!")
                    st.rerun()
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    if classes:
        for cls in classes:
            with st.expander(f"📋 {cls['name']} ({len(cls.get('students', []))} students) - by {cls.get('created_by', 'Unknown')}"):
                if cls.get('students'):
                    st.dataframe(pd.DataFrame(cls['students']), use_container_width=True)
                if is_admin():
                    if st.button("🗑️ Delete Class", key=f"del_cls_{cls['id']}"):
                        with db.get_connection() as conn:
                            conn.execute("DELETE FROM classes WHERE id = ? AND school_name = ?",
                                       (cls['id'], school_name))
                        add_audit_entry('Class Removed', cls['name'])
                        st.success("Class removed!")
                        st.rerun()
    else:
        st.info("No saved class lists")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_qr():
    st.markdown('<div class="glass-card"><h2>📱 QR Codes</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📷 Scan QR", "🔧 Generate QR"])
    
    with tab1:
        st.info("📷 Point your camera at a QR code")
        scanned_code = qr_code_scanner()
        
        if scanned_code:
            st.success(f"✅ Scanned: {scanned_code}")
            
            if '-' in scanned_code:
                parts = scanned_code.split('-', 1)
                if len(parts) == 2:
                    qr_type, qr_number = parts
                    school_name = st.session_state.school['name']
                    
                    if qr_type == 'book':
                        with db.get_connection() as conn:
                            book = conn.execute(
                                "SELECT * FROM borrowed WHERE school_name = ? AND bookNo = ? AND returned = 0",
                                (school_name, qr_number)
                            ).fetchone()
                            if book:
                                st.info(f"📚 Borrowed by: {book['name']}")
                            else:
                                st.success("📚 Book is available!")
                    elif qr_type == 'chair':
                        with db.get_connection() as conn:
                            chair = conn.execute(
                                "SELECT * FROM furniture WHERE school_name = ? AND chair = ? AND returned = 0",
                                (school_name, scanned_code)
                            ).fetchone()
                            if chair:
                                st.info(f"🪑 Assigned to: {chair['name']}")
                            else:
                                st.success("🪑 Chair is available!")
                    elif qr_type == 'locker':
                        with db.get_connection() as conn:
                            locker = conn.execute(
                                "SELECT * FROM furniture WHERE school_name = ? AND locker = ? AND returned = 0",
                                (school_name, scanned_code)
                            ).fetchone()
                            if locker:
                                st.info(f"🔒 Assigned to: {locker['name']}")
                            else:
                                st.success("🔒 Locker is available!")
    
    with tab2:
        qr_type = st.selectbox("QR Type:", ["book", "chair", "locker"])
        col1, col2 = st.columns(2)
        with col1:
            start_num = st.number_input("Start Number:", 1, 10000, 1)
        with col2:
            end_num = st.number_input("End Number:", 1, 10000, min(start_num, 10))
        
        if st.button("Generate QR Codes", use_container_width=True):
            cols = st.columns(4)
            for i in range(start_num, min(end_num + 1, start_num + 20)):
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H,
                                   box_size=10, border=5)
                qr_data = f"{qr_type}-{i}"
                qr.add_data(qr_data)
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                buf = BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)
                img_b64 = base64.b64encode(buf.read()).decode()
                
                with cols[(i - start_num) % 4]:
                    st.image(f"data:image/png;base64,{img_b64}", 
                            caption=f"{qr_type.upper()}: {i}", width=150)
                    st.download_button("📥", data=buf, file_name=f"{qr_type}_{i}.png",
                                     mime="image/png", key=f"dl_qr_{i}", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_chat():
    school_name = st.session_state.school['name']
    user = st.session_state.user
    users = load_school_data('users', [])
    
    st.markdown('<div class="glass-card"><h2>💬 Private Chat</h2>', unsafe_allow_html=True)
    
    other_users = [u for u in users if u['email'] != user['email']]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### 👥 Staff")
        
        if other_users:
            for u in other_users:
                role_icon = "👑" if u['role'] == 'admin' else "👨‍🏫" if u['role'] == 'teacher' else "📚"
                
                # Unread count
                unread = 0
                with db.get_connection() as conn:
                    count = conn.execute(
                        "SELECT COUNT(*) as cnt FROM chat_messages WHERE school_name = ? AND from_email = ? AND to_email = ? AND read_status = 0",
                        (school_name, u['email'], user['email'])
                    ).fetchone()
                    unread = count['cnt'] if count else 0
                
                unread_badge = f" 🔴({unread})" if unread > 0 else ""
                
                if st.button(f"{role_icon} {u['name']}{unread_badge}", key=f"chat_user_{u['email']}", use_container_width=True):
                    st.session_state.chat_with = u['email']
                    # Mark as read
                    with db.get_connection() as conn:
                        conn.execute(
                            "UPDATE chat_messages SET read_status = 1 WHERE school_name = ? AND from_email = ? AND to_email = ?",
                            (school_name, u['email'], user['email'])
                        )
                    st.rerun()
        else:
            st.info("No other staff")
    
    with col2:
        if st.session_state.get('chat_with'):
            chat_with = st.session_state.chat_with
            chat_user = next((u for u in users if u['email'] == chat_with), None)
            
            if chat_user:
                st.markdown(f"### 💬 {chat_user['name']}")
                
                # Messages
                with db.get_connection() as conn:
                    msgs = conn.execute(
                        """SELECT * FROM chat_messages WHERE school_name = ? 
                        AND ((from_email = ? AND to_email = ?) OR (from_email = ? AND to_email = ?))
                        AND deleted_by_sender = 0 AND deleted_by_receiver = 0
                        ORDER BY timestamp ASC""",
                        (school_name, user['email'], chat_with, chat_with, user['email'])
                    ).fetchall()
                
                chat_container = st.container()
                
                with chat_container:
                    for msg in msgs:
                        msg_dict = dict(msg)
                        is_mine = msg_dict['from_email'] == user['email']
                        bg_color = "rgba(233,69,96,0.4)" if is_mine else "rgba(255,255,255,0.15)"
                        align = "flex-end" if is_mine else "flex-start"
                        
                        # Attachment
                        attachment_html = ""
                        if msg_dict.get('attachment'):
                            try:
                                att = json.loads(msg_dict['attachment']) if isinstance(msg_dict['attachment'], str) else msg_dict['attachment']
                                if att.get('type') == 'image':
                                    attachment_html = f'<br><img src="data:{att.get("mime","image/png")};base64,{att["data"]}" style="max-width:200px;border-radius:8px;margin-top:8px;">'
                                elif att.get('type') == 'file':
                                    attachment_html = f'<br>📎 <a href="data:{att.get("mime")};base64,{att["data"]}" download="{att["name"]}" style="color:#FFD700;">{att["name"]}</a>'
                                elif att.get('type') == 'voice':
                                    attachment_html = f'<br>🎤 <audio controls style="max-width:200px;height:30px;"><source src="data:{att.get("mime")};base64,{att["data"]}"></audio>'
                            except:
                                pass
                        
                        emoji_html = f" {msg_dict.get('emoji', '')}" if msg_dict.get('emoji') else ""
                        
                        st.markdown(f"""
                        <div style="display:flex;justify-content:{align};margin:8px 0;animation:fadeIn 0.3s ease;">
                            <div style="background:{bg_color};padding:12px 16px;border-radius:18px;max-width:70%;color:#FFF;word-wrap:break-word;">
                                <strong style="font-size:0.85em;">{sanitize_html(msg_dict.get('from_name', ''))}:</strong>
                                <div>{sanitize_html(msg_dict.get('message', ''))}{emoji_html}</div>
                                {attachment_html}
                                <div style="font-size:0.7em;color:rgba(255,255,255,0.5);margin-top:5px;text-align:right;">
                                    {msg_dict.get('timestamp', '')[:16]}
                                    {' ✓✓' if is_mine and msg_dict.get('read_status') else ' ✓' if is_mine else ''}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Input area
                st.markdown("---")
                
                with st.expander("😀 Emoji", expanded=False):
                    selected_emoji = emoji_picker("chat")
                
                with st.expander("📎 Attachment", expanded=False):
                    attachment = file_attachment_handler("chat_msg")
                
                col_a, col_b = st.columns([5, 1])
                with col_a:
                    msg_text = st.text_input("Message", key="chat_msg_input", 
                                           placeholder=f"Type message... {selected_emoji if selected_emoji else ''}",
                                           label_visibility="collapsed")
                with col_b:
                    if st.button("📤", use_container_width=True, key="chat_send_btn"):
                        final_msg = msg_text + (f" {selected_emoji}" if selected_emoji else "")
                        if final_msg or attachment:
                            msg_id = generate_code("MSG")
                            with db.get_connection() as conn:
                                conn.execute(
                                    """INSERT INTO chat_messages (id, school_name, from_email, from_name, to_email, message, timestamp, attachment, emoji, read_status)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)""",
                                    (msg_id, school_name, user['email'], user['name'],
                                     chat_with, final_msg,
                                     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                     json.dumps(attachment) if attachment else "",
                                     selected_emoji if selected_emoji else "")
                                )
                            st.success("Sent!")
                            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_forum():
    school_name = st.session_state.school['name']
    user = st.session_state.user
    
    st.markdown('<div class="glass-card"><h2>📢 Group Forum</h2>', unsafe_allow_html=True)
    st.info("Messages visible to all staff members")
    
    with db.get_connection() as conn:
        msgs = conn.execute(
            "SELECT * FROM forum_messages WHERE school_name = ? AND is_deleted = 0 ORDER BY timestamp DESC LIMIT 50",
            (school_name,)
        ).fetchall()
    
    for msg in msgs:
        msg_dict = dict(msg)
        role_icon = "👑" if msg_dict['role'] == 'admin' else "👨‍🏫" if msg_dict['role'] == 'teacher' else "📚"
        
        attachment_html = ""
        if msg_dict.get('attachment'):
            try:
                att = json.loads(msg_dict['attachment']) if isinstance(msg_dict['attachment'], str) else msg_dict['attachment']
                if att.get('type') == 'image':
                    attachment_html = f'<br><img src="data:{att.get("mime","image/png")};base64,{att["data"]}" style="max-width:200px;border-radius:8px;">'
                elif att.get('type') == 'file':
                    attachment_html = f'<br>📎 <a href="data:{att.get("mime")};base64,{att["data"]}" download="{att["name"]}" style="color:#FFD700;">{att["name"]}</a>'
            except:
                pass
        
        emoji_html = f" {msg_dict.get('emoji', '')}" if msg_dict.get('emoji') else ""
        
        col1, col2 = st.columns([20, 1])
        with col1:
            st.markdown(f"""
            <div class="forum-message">
                <strong>{role_icon} {sanitize_html(msg_dict['from_name'])}</strong>
                <small>({msg_dict['timestamp'][:16]})</small>
                <br>{sanitize_html(msg_dict['message'])}{emoji_html}
                {attachment_html}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if is_admin() or msg_dict['from_email'] == user['email']:
                if st.button("🗑️", key=f"del_forum_{msg_dict['id']}"):
                    with db.get_connection() as conn:
                        conn.execute(
                            "UPDATE forum_messages SET is_deleted = 1 WHERE id = ? AND school_name = ?",
                            (msg_dict['id'], school_name)
                        )
                    st.success("Message deleted!")
                    st.rerun()
    
    # Post new message
    st.markdown("---")
    
    with st.expander("😀 Emoji", expanded=False):
        selected_emoji = emoji_picker("forum")
    
    with st.expander("📎 Attachment", expanded=False):
        attachment = file_attachment_handler("forum")
    
    col_a, col_b = st.columns([5, 1])
    with col_a:
        with st.form("frm_forum_post"):
            forum_msg = st.text_area("Message:", key="forum_msg", height=100, 
                                    placeholder="Share with everyone...")
            if st.form_submit_button("📢 Post", use_container_width=True):
                final_msg = forum_msg + (f" {selected_emoji}" if selected_emoji else "")
                if final_msg or attachment:
                    msg_id = generate_code("FRM")
                    with db.get_connection() as conn:
                        conn.execute(
                            """INSERT INTO forum_messages (id, school_name, from_email, from_name, role, message, timestamp, attachment, emoji)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (msg_id, school_name, user['email'], user['name'], user['role'],
                             final_msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             json.dumps(attachment) if attachment else "",
                             selected_emoji if selected_emoji else "")
                        )
                    st.success("Posted!")
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_notepad():
    school_name = st.session_state.school['name']
    user = st.session_state.user
    notepad_notes = load_school_data('notepad', [])
    
    st.markdown('<div class="glass-card"><h2>📝 Private Notepad</h2>', unsafe_allow_html=True)
    
    user_notes = [n for n in notepad_notes if n.get('author_email') == user['email']]
    shared_notes = [n for n in notepad_notes if n.get('author_email') != user['email'] 
                    and n.get('is_private') == 0 
                    and user['email'] in (n.get('shared_with', '') or '').split(',')]
    
    tab1, tab2, tab3 = st.tabs(["📝 My Notes", "👥 Shared", "➕ New"])
    
    with tab1:
        if user_notes:
            for note in sorted(user_notes, key=lambda x: x.get('timestamp', ''), reverse=True):
                with st.expander(f"📝 {note.get('title', 'Untitled')} - {note.get('timestamp', '')[:16]}"):
                    st.markdown(note.get('content', ''))
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button("✏️ Edit", key=f"edit_note_{note['id']}"):
                            st.session_state.editing_note = dict(note)
                            st.rerun()
                    with col2:
                        if st.button("📥 DOCX", key=f"dl_note_{note['id']}"):
                            doc = docx.Document()
                            doc.add_heading(note.get('title', 'Note'), 0)
                            for para in note.get('content', '').split('\n'):
                                doc.add_paragraph(para)
                            buf = BytesIO()
                            doc.save(buf)
                            buf.seek(0)
                            b64 = base64.b64encode(buf.read()).decode()
                            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="{note.get("title","note")}.docx">📥 Download</a>', unsafe_allow_html=True)
                    with col3:
                        if st.button("👥 Share", key=f"share_note_{note['id']}"):
                            st.session_state.sharing_note = dict(note)
                            st.rerun()
                    with col4:
                        if st.button("🗑️", key=f"del_note_{note['id']}"):
                            with db.get_connection() as conn:
                                conn.execute(
                                    "UPDATE notepad SET is_deleted = 1 WHERE id = ? AND school_name = ?",
                                    (note['id'], school_name)
                                )
                            st.success("Deleted!")
                            st.rerun()
                    
                    if st.session_state.get('sharing_note') and st.session_state.sharing_note['id'] == note['id']:
                        with st.form(f"share_{note['id']}"):
                            users = load_school_data('users', [])
                            user_emails = [u['email'] for u in users if u['email'] != user['email']]
                            selected = st.multiselect("Share with:", user_emails)
                            if st.form_submit_button("💾 Save"):
                                with db.get_connection() as conn:
                                    conn.execute(
                                        "UPDATE notepad SET is_private = 0, shared_with = ? WHERE id = ? AND school_name = ?",
                                        (','.join(selected), note['id'], school_name)
                                    )
                                st.success("Shared!")
                                st.session_state.sharing_note = None
                                st.rerun()
        else:
            st.info("No notes yet")
    
    with tab2:
        if shared_notes:
            for note in shared_notes:
                with st.expander(f"📝 {note.get('title', 'Untitled')} - by {note.get('author', 'Unknown')}"):
                    st.markdown(note.get('content', ''))
        else:
            st.info("No shared notes")
    
    with tab3:
        editing_note = st.session_state.get('editing_note')
        
        with st.form("frm_notepad"):
            title = st.text_input("Title:", value=editing_note.get('title', '') if editing_note else '')
            content = st.text_area("Content:", value=editing_note.get('content', '') if editing_note else '',
                                  height=300, placeholder="Write your note...")
            
            if st.form_submit_button("💾 Save", use_container_width=True):
                if content:
                    note_id = editing_note['id'] if editing_note else generate_code("NOTE")
                    with db.get_connection() as conn:
                        if editing_note:
                            conn.execute(
                                "UPDATE notepad SET title = ?, content = ?, timestamp = ? WHERE id = ? AND school_name = ?",
                                (title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 note_id, school_name)
                            )
                        else:
                            conn.execute(
                                """INSERT INTO notepad (id, school_name, author, author_email, content, title, timestamp, is_private)
                                VALUES (?, ?, ?, ?, ?, ?, ?, 1)""",
                                (note_id, school_name, user['name'], user['email'], content,
                                 title or "Untitled", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            )
                    st.success("Saved!")
                    st.session_state.editing_note = None
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_system_overview():
    school_name = st.session_state.school['name']
    
    st.markdown('<div class="glass-card"><h2>🔍 System Overview</h2>', unsafe_allow_html=True)
    
    books = load_school_data('books', [])
    borrowed = load_school_data('borrowed', [])
    members = load_school_data('members', [])
    teachers = load_school_data('teachers', [])
    users = load_school_data('users', [])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-card"><strong>🏫 School</strong><br>{school_name}<br>Code: {st.session_state.school["invite_code"]}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><strong>📚 Books</strong><br>Total: {sum(b.get("quantity",0) for b in books)}<br>Active: {len([b for b in borrowed if not b.get("returned")])}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><strong>👥 People</strong><br>Staff: {len(users)}<br>Members: {len(members)}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_audit_log():
    if not is_admin():
        st.error("🔒 Admin access required!")
        return
    
    audit_log = load_school_data('audit_log', [])
    
    st.markdown('<div class="glass-card"><h2>📝 Audit Log</h2>', unsafe_allow_html=True)
    
    if audit_log:
        df = pd.DataFrame(audit_log)
        st.dataframe(df, use_container_width=True)
        
        if st.button("📥 Export Audit Log", use_container_width=True):
            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="audit_log.xlsx">📥 Download</a>', unsafe_allow_html=True)
    else:
        st.info("No audit log entries")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_reports():
    school_name = st.session_state.school['name']
    
    st.markdown('<div class="glass-card"><h2>📈 Reports & Analytics</h2>', unsafe_allow_html=True)
    
    report_type = st.selectbox("Report Type:", ["📚 Books Overview", "🪑 Furniture Overview", "🔴 Overdue Analysis", "📊 Complete Dashboard"])
    
    if st.button("📊 Generate", use_container_width=True):
        if report_type == "📚 Books Overview":
            with db.get_connection() as conn:
                data = conn.execute("SELECT * FROM borrowed WHERE school_name = ?", (school_name,)).fetchall()
            if data:
                df = pd.DataFrame([dict(row) for row in data])
                st.dataframe(df, use_container_width=True)
                
                status_counts = df['returned'].value_counts()
                fig = px.bar(x=['Active', 'Returned'], y=[status_counts.get(0, 0), status_counts.get(1, 0)],
                            title="Books by Status", color_discrete_sequence=['#e94560', '#28a745'])
                st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "🪑 Furniture Overview":
            with db.get_connection() as conn:
                data = conn.execute("SELECT * FROM furniture WHERE school_name = ?", (school_name,)).fetchall()
            if data:
                df = pd.DataFrame([dict(row) for row in data])
                st.dataframe(df, use_container_width=True)
                
                status_counts = df['returned'].value_counts()
                fig = px.pie(values=[status_counts.get(0, 0), status_counts.get(1, 0)],
                            names=['Active', 'Returned'], title="Furniture Status",
                            color_discrete_sequence=['#e94560', '#28a745'])
                st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "🔴 Overdue Analysis":
            with db.get_connection() as conn:
                data = conn.execute(
                    "SELECT * FROM borrowed WHERE school_name = ? AND returned = 0 AND returnDate < ?",
                    (school_name, datetime.now().strftime('%Y-%m-%d'))
                ).fetchall()
            if data:
                df = pd.DataFrame([dict(row) for row in data])
                st.dataframe(df, use_container_width=True)
                st.metric("🔴 Overdue", len(data))
            else:
                st.success("No overdue books!")
        
        elif report_type == "📊 Complete Dashboard":
            books = load_school_data('books', [])
            borrowed = load_school_data('borrowed', [])
            members = load_school_data('members', [])
            teachers = load_school_data('teachers', [])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📚 Total Books", sum(b.get('quantity', 0) for b in books))
            with col2:
                st.metric("📖 Active Loans", len([b for b in borrowed if not b.get('returned')]))
            with col3:
                st.metric("👥 Members", len(members))
            with col4:
                st.metric("👨‍🏫 Teachers", len(teachers))
            
            total = sum(b.get('quantity', 0) for b in books)
            active = len([b for b in borrowed if not b.get('returned')])
            fig = px.pie(values=[active, max(total - active, 0)], names=['Borrowed', 'Available'],
                        title="Distribution", color_discrete_sequence=['#e94560', '#28a745'])
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

@admin_only
def render_settings():
    school_name = st.session_state.school['name']
    
    st.markdown('<div class="glass-card"><h2>⚙️ Admin Settings</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🎨 Theme", "💾 Data", "👥 Staff Management"])
    
    with tab1:
        st.markdown("### 🎨 Wallpapers")
        wallpaper = st.selectbox("Choose:", list(WALLPAPERS.keys()), 
                                index=list(WALLPAPERS.keys()).index(st.session_state.wallpaper) 
                                if st.session_state.wallpaper in WALLPAPERS else 0)
        if st.button("Apply Theme", use_container_width=True):
            st.session_state.wallpaper = wallpaper
            st.rerun()
        if wallpaper != "None":
            st.image(WALLPAPERS[wallpaper], width=400)
    
    with tab2:
        st.markdown("### 💾 Data Management")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Backup All Data", use_container_width=True):
                with db.get_connection() as conn:
                    tables = ['schools', 'users', 'books', 'borrowed', 'furniture', 'members', 
                             'teachers', 'classes', 'audit_log', 'forum_messages', 'system_settings']
                    backup = {}
                    for table in tables:
                        rows = conn.execute(f"SELECT * FROM {table} WHERE school_name = ?", (school_name,)).fetchall()
                        backup[table] = [dict(row) for row in rows]
                
                b64 = base64.b64encode(json.dumps(backup, indent=2, default=str).encode()).decode()
                st.markdown(f'<a href="data:application/json;base64,{b64}" download="srms_backup_{school_name}.json">📥 Download Backup</a>', unsafe_allow_html=True)
                st.success("Backup ready!")
        
        with col2:
            uploaded = st.file_uploader("📤 Restore Backup", type=['json'])
            if uploaded and st.button("Restore", use_container_width=True):
                try:
                    data = json.load(uploaded)
                    with db.get_connection() as conn:
                        for table, rows in data.items():
                            if rows and isinstance(rows, list):
                                for row in rows:
                                    columns = ', '.join(row.keys())
                                    placeholders = ', '.join(['?' for _ in row])
                                    conn.execute(
                                        f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})",
                                        list(row.values())
                                    )
                    st.success("✅ Restored!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col3:
            if st.button("⚠️ Clear All Data", use_container_width=True):
                confirm = st.text_input("Type 'DELETE ALL DATA' to confirm:", key="confirm_clear")
                if confirm == "DELETE ALL DATA":
                    tables = ['books', 'borrowed', 'furniture', 'members', 'teachers', 
                             'classes', 'audit_log', 'chat_messages', 'forum_messages', 'notepad']
                    with db.get_connection() as conn:
                        for table in tables:
                            conn.execute(f"DELETE FROM {table} WHERE school_name = ?", (school_name,))
                    st.error("All data cleared!")
                    st.rerun()
    
    with tab3:
        st.markdown("### 👥 Staff Management")
        
        # Create staff
        with st.form("frm_create_staff"):
            col1, col2, col3 = st.columns(3)
            with col1:
                email = st.text_input("Email:")
            with col2:
                name = st.text_input("Name:")
            with col3:
                role = st.selectbox("Role:", ["teacher", "librarian"])
            
            password = st.text_input("Password:", placeholder="Leave empty for auto-generate")
            
            if st.form_submit_button("➕ Create Staff", use_container_width=True):
                if email and name:
                    with db.get_connection() as conn:
                        existing = conn.execute(
                            "SELECT * FROM users WHERE email = ? AND school_name = ?",
                            (email, school_name)
                        ).fetchone()
                        
                        if existing:
                            st.error("Email exists!")
                        else:
                            gen_pw = password if password else generate_code("", 8)
                            hashed = hash_password(gen_pw)
                            
                            conn.execute(
                                """INSERT INTO users (email, school_name, name, code, password, role, joined, is_active)
                                VALUES (?, ?, ?, ?, ?, ?, ?, 1)""",
                                (email, school_name, name, st.session_state.school['invite_code'],
                                 hashed, role, datetime.now().strftime("%Y-%m-%d"))
                            )
                            add_audit_entry('Staff Created', f"{name} as {role}")
                            st.success(f"✅ Created! Password: `{gen_pw}`")
                            st.rerun()
        
        # List staff
        users = load_school_data('users', [])
        for u in users:
            role_icon = "👑" if u['role'] == 'admin' else "👨‍🏫" if u['role'] == 'teacher' else "📚"
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(f"{role_icon} **{u['name']}** ({u['role']})")
            with col2:
                st.write(u.get('email', ''))
            with col3:
                if u['email'] != st.session_state.user['email'] and u['role'] != 'admin':
                    if st.button("👑 Promote", key=f"promote_{u['email']}"):
                        with db.get_connection() as conn:
                            conn.execute(
                                "UPDATE users SET role = 'admin' WHERE email = ? AND school_name = ?",
                                (u['email'], school_name)
                            )
                        add_audit_entry('Staff Promoted', u['name'])
                        st.success(f"{u['name']} is now admin!")
                        st.rerun()
            with col4:
                if u['email'] != st.session_state.user['email']:
                    if st.button("🗑️", key=f"del_staff_{u['email']}"):
                        with db.get_connection() as conn:
                            conn.execute(
                                "UPDATE users SET is_active = 0 WHERE email = ? AND school_name = ?",
                                (u['email'], school_name)
                            )
                        add_audit_entry('Staff Deactivated', u['name'])
                        st.success(f"{u['name']} deactivated!")
                        st.rerun()
            st.divider()
    
    st.markdown('</div>', unsafe_allow_html=True)

@admin_only
def render_database_manager():
    """Admin-only database manager to view all data"""
    school_name = st.session_state.school['name']
    
    st.markdown('<div class="glass-card"><h2>🗄️ Database Manager (Admin Only)</h2>', unsafe_allow_html=True)
    st.warning("⚠️ This section contains all database records. Handle with care!")
    
    tables = {
        "🏫 Schools": "schools",
        "👥 Users": "users",
        "📚 Books": "books",
        "📖 Borrowed": "borrowed",
        "🪑 Furniture": "furniture",
        "👤 Members": "members",
        "👨‍🏫 Teachers": "teachers",
        "📋 Classes": "classes",
        "💬 Chat Messages": "chat_messages",
        "📢 Forum Messages": "forum_messages",
        "📝 Notepad": "notepad",
        "📊 Audit Log": "audit_log",
        "🎨 Wallpapers": "wallpapers",
        "🔐 Password Resets": "password_resets",
        "⚙️ System Settings": "system_settings"
    }
    
    selected_table = st.selectbox("Select Table:", list(tables.keys()))
    table_name = tables[selected_table]
    
    with db.get_connection() as conn:
        # Get row count
        count = conn.execute(f"SELECT COUNT(*) as cnt FROM {table_name} WHERE school_name = ?", 
                           (school_name,)).fetchone()
        st.metric("Total Records", count['cnt'])
        
        # Fetch all data
        data = conn.execute(f"SELECT * FROM {table_name} WHERE school_name = ? ORDER BY rowid DESC LIMIT 200", 
                          (school_name,)).fetchall()
        
        if data:
            df = pd.DataFrame([dict(row) for row in data])
            st.dataframe(df, use_container_width=True, height=400)
            
            # Export
            if st.button(f"📥 Export {selected_table}", use_container_width=True):
                towrite = BytesIO()
                df.to_excel(towrite, index=False, engine='openpyxl')
                towrite.seek(0)
                b64 = base64.b64encode(towrite.read()).decode()
                st.markdown(
                    f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" '
                    f'download="{table_name}.xlsx">📥 Download Excel</a>',
                    unsafe_allow_html=True
                )
            
            # Delete records
            if st.button(f"⚠️ Delete All Records in {selected_table}", use_container_width=True):
                confirm = st.text_input(f"Type 'DELETE {table_name.upper()}' to confirm:")
                if confirm == f"DELETE {table_name.upper()}":
                    table = table_name
                    if table != 'users':  # Protect users table
                        with db.get_connection() as conn:
                            conn.execute(f"DELETE FROM {table} WHERE school_name = ?", (school_name,))
                        add_audit_entry('Database Cleanup', f"Deleted all records from {table}")
                        st.error(f"All records in {selected_table} deleted!")
                        st.rerun()
                    else:
                        st.error("Cannot delete all users! Deactivate users individually.")
        else:
            st.info("No records found in this table")
    
    # Database statistics
    st.markdown("---")
    st.markdown("### 📊 Database Statistics")
    
    with db.get_connection() as conn:
        stats = {}
        for display_name, table in tables.items():
            count = conn.execute(f"SELECT COUNT(*) as cnt FROM {table} WHERE school_name = ?", 
                               (school_name,)).fetchone()
            stats[display_name] = count['cnt']
    
    # Display stats in columns
    cols = st.columns(3)
    for i, (name, count) in enumerate(stats.items()):
        with cols[i % 3]:
            st.metric(name, count)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============== MAIN ==============
def main():
    if st.session_state.page == 'startup':
        startup_page()
    elif st.session_state.page == 'dashboard':
        dashboard_page()
    else:
        startup_page()

if __name__ == "__main__":
    main()
