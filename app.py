# app.py - SRMS - School Resource Management System by WeGEM
# Complete Version with Separated Allocation Views
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

def init_sqlite_db():
    """Initialize SQLite database with all required tables"""
    db_path = DATA_DIR / "srms.db"
    
    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Schools table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schools (
                name TEXT PRIMARY KEY,
                address TEXT,
                admin_name TEXT,
                admin_email TEXT,
                admin_phone TEXT,
                invite_code TEXT UNIQUE,
                created TEXT,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
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
            )
        ''')
        
        # Books table - with available count
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT,
                title TEXT,
                type TEXT,
                quantity INTEGER,
                available INTEGER,
                created_by TEXT,
                created_at TEXT,
                UNIQUE(school_name, title)
            )
        ''')
        
        # Borrowed books table - with academic year and term
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowed (
                id TEXT PRIMARY KEY,
                school_name TEXT,
                student_name TEXT,
                adm TEXT,
                form TEXT,
                stream TEXT,
                book_title TEXT,
                book_no TEXT,
                borrow_date TEXT,
                return_date TEXT,
                returned INTEGER DEFAULT 0,
                actual_return_date TEXT,
                issued_by TEXT,
                academic_year TEXT,
                term TEXT
            )
        ''')
        
        # Furniture allocations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS furniture (
                id TEXT PRIMARY KEY,
                school_name TEXT,
                student_name TEXT,
                adm TEXT,
                form TEXT,
                stream TEXT,
                chair_no TEXT,
                locker_no TEXT,
                allocation_date TEXT,
                returned INTEGER DEFAULT 0,
                return_date TEXT,
                issued_by TEXT,
                academic_year TEXT,
                term TEXT
            )
        ''')
        
        # Furniture inventory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS furniture_inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT,
                item_type TEXT,
                item_code TEXT UNIQUE,
                condition TEXT DEFAULT 'Good',
                status TEXT DEFAULT 'Available',
                location TEXT,
                notes TEXT,
                added_by TEXT,
                added_date TEXT
            )
        ''')
        
        # Members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id TEXT PRIMARY KEY,
                school_name TEXT,
                name TEXT,
                student_class TEXT,
                stream TEXT,
                added_by TEXT,
                added_at TEXT,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Teachers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id TEXT PRIMARY KEY,
                school_name TEXT,
                name TEXT,
                subject TEXT,
                classes TEXT,
                duty TEXT,
                added_by TEXT,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Classes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT,
                name TEXT,
                stream TEXT,
                students TEXT,
                created_by TEXT,
                created TEXT,
                academic_year TEXT,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Academic terms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS academic_terms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT,
                name TEXT,
                start_date TEXT,
                end_date TEXT,
                is_current INTEGER DEFAULT 0,
                created_by TEXT
            )
        ''')
        
        # Audit log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT,
                timestamp TEXT,
                user TEXT,
                user_email TEXT,
                action TEXT,
                details TEXT,
                ip_address TEXT
            )
        ''')
        
        # Chat messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id TEXT PRIMARY KEY,
                school_name TEXT,
                from_email TEXT,
                from_name TEXT,
                to_email TEXT,
                message TEXT,
                timestamp TEXT,
                attachment TEXT,
                emoji TEXT,
                read_status INTEGER DEFAULT 0,
                deleted_by_sender INTEGER DEFAULT 0,
                deleted_by_receiver INTEGER DEFAULT 0
            )
        ''')
        
        # Forum messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS forum_messages (
                id TEXT PRIMARY KEY,
                school_name TEXT,
                from_email TEXT,
                from_name TEXT,
                role TEXT,
                message TEXT,
                timestamp TEXT,
                attachment TEXT,
                emoji TEXT,
                is_deleted INTEGER DEFAULT 0
            )
        ''')
        
        # Notepad table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notepad (
                id TEXT PRIMARY KEY,
                school_name TEXT,
                author TEXT,
                author_email TEXT,
                content TEXT,
                title TEXT,
                timestamp TEXT,
                is_private INTEGER DEFAULT 1,
                shared_with TEXT,
                is_deleted INTEGER DEFAULT 0
            )
        ''')
        
        # Wallpapers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallpapers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT,
                name TEXT,
                url TEXT,
                is_custom INTEGER DEFAULT 0,
                uploaded_by TEXT,
                uploaded_at TEXT
            )
        ''')
        
        # Password resets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS password_resets (
                email TEXT,
                school_name TEXT,
                token TEXT,
                expiry TEXT,
                used INTEGER DEFAULT 0,
                PRIMARY KEY (email, school_name)
            )
        ''')
        
        # System settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_settings (
                school_name TEXT PRIMARY KEY,
                max_borrow_days INTEGER DEFAULT 14,
                max_books_per_student INTEGER DEFAULT 3,
                auto_return_reminders INTEGER DEFAULT 0,
                allow_student_registration INTEGER DEFAULT 0,
                maintenance_mode INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Database initialization error: {str(e)}")
        return False

# Initialize database
init_sqlite_db()

def get_db_connection():
    """Get a database connection"""
    db_path = DATA_DIR / "srms.db"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

# ============ 200+ WALLPAPERS ============
WALLPAPERS = {
    "None": "",
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
    "Sunset": "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=1920",
    "Ocean": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920",
    "Forest": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920",
    "Mountain": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920",
    "Desert": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920",
    "Waterfall": "https://images.unsplash.com/photo-1544551763-46a013bb70b5?w=1920",
    "Cherry Blossom": "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1920",
    "Northern Lights": "https://images.unsplash.com/photo-1483347756197-71ef80e95f73?w=1920",
    "Galaxy": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920",
    "City Lights": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1920",
    "Tokyo": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1920",
    "New York": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1920",
    "Paris": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920",
    "London": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1920",
    "Dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1920",
}

# ============ EMOJI CATEGORIES ============
EMOJI_CATEGORIES = {
    "😀 Smileys": ["😀", "😃", "😄", "😁", "😅", "😂", "🤣", "😊", "😇", "🙂", "😉", "😌", "😍", "🥰", "😘"],
    "👍 Gestures": ["👍", "👎", "👌", "✌️", "🤞", "🤟", "🤘", "🤙", "👈", "👉", "👆", "👇", "☝️", "✋", "🤚"],
    "❤️ Hearts": ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔", "❣️", "💕", "💞", "💓", "💗"],
    "📚 School": ["📚", "📖", "📝", "✏️", "🖊️", "📏", "📐", "🎓", "🏫", "📋", "📎", "🖇️", "🗂️", "📁", "📌"],
    "🎯 Symbols": ["🎯", "⭐", "🌟", "✨", "🔥", "💯", "✅", "❌", "⚠️", "🔔", "📢", "📣", "💡", "🔑", "🔒"],
    "🍕 Food": ["🍎", "🍕", "🍔", "🍟", "🌮", "🍩", "🎂", "🍪", "🍦", "🍿", "☕", "🍵", "🧃", "🥤", "🍺"],
    "🚀 Travel": ["🚀", "✈️", "🚗", "🚲", "🏠", "🏢", "🏰", "🗽", "🎡", "🎢", "🎪", "🏖️", "🏝️", "🏔️", "🌋"],
    "🎨 Activities": ["🎨", "🎭", "🎬", "🎤", "🎧", "🎼", "🎹", "🎸", "🎺", "🎻", "🎮", "🎲", "🎯", "⚽", "🏀"],
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
    return st.session_state.get('user') is not None and st.session_state.get('school') is not None

def add_audit_entry(action: str, details: str):
    """Add entry to audit log"""
    try:
        school_name = "Unknown"
        user_name = "System"
        user_email = "system@srms.local"
        
        if is_authenticated():
            school_name = st.session_state.school.get('name', 'Unknown')
            user_name = st.session_state.user.get('name', 'Unknown')
            user_email = st.session_state.user.get('email', 'unknown@srms.local')
        
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO audit_log (school_name, timestamp, user, user_email, action, details, ip_address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (school_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                 user_name, user_email, action, details, '127.0.0.1')
            )
            conn.commit()
        except Exception as e:
            print(f"Audit log error (non-critical): {str(e)}")
        finally:
            conn.close()
    except Exception as e:
        print(f"Audit log function error: {str(e)}")

def get_current_term(school_name: str) -> Dict:
    """Get current academic term"""
    conn = get_db_connection()
    try:
        term = conn.execute(
            "SELECT * FROM academic_terms WHERE school_name = ? AND is_current = 1",
            (school_name,)
        ).fetchone()
        return dict(term) if term else {}
    finally:
        conn.close()

def get_academic_year() -> str:
    """Get current academic year string"""
    now = datetime.now()
    if now.month >= 9:
        return f"{now.year}-{now.year + 1}"
    else:
        return f"{now.year - 1}-{now.year}"

def load_school_data(data_type: str, default: Any = None) -> Any:
    """Load data from database"""
    if not is_authenticated():
        return default if default is not None else []
    
    school_name = st.session_state.school['name']
    conn = get_db_connection()
    
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
        elif data_type == 'furniture_inventory':
            cursor = conn.execute("SELECT * FROM furniture_inventory WHERE school_name = ?", (school_name,))
            return [dict(row) for row in cursor.fetchall()]
        elif data_type == 'members':
            cursor = conn.execute("SELECT * FROM members WHERE school_name = ? AND is_active = 1", (school_name,))
            return [dict(row) for row in cursor.fetchall()]
        elif data_type == 'teachers':
            cursor = conn.execute("SELECT * FROM teachers WHERE school_name = ? AND is_active = 1", (school_name,))
            return [dict(row) for row in cursor.fetchall()]
        elif data_type == 'classes':
            cursor = conn.execute("SELECT * FROM classes WHERE school_name = ? AND is_active = 1", (school_name,))
            classes = []
            for row in cursor.fetchall():
                row_dict = dict(row)
                try:
                    row_dict['students'] = json.loads(row_dict.get('students', '[]'))
                except:
                    row_dict['students'] = []
                classes.append(row_dict)
            return classes
        elif data_type == 'academic_terms':
            cursor = conn.execute("SELECT * FROM academic_terms WHERE school_name = ? ORDER BY start_date DESC", (school_name,))
            return [dict(row) for row in cursor.fetchall()]
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
        else:
            return default if default is not None else []
    except Exception as e:
        print(f"Error loading {data_type}: {str(e)}")
        return default if default is not None else []
    finally:
        conn.close()

def check_duplicate_assignment(school_name: str, adm: str, item_type: str, item_number: str) -> bool:
    """Check if a student already has an item assigned"""
    conn = get_db_connection()
    try:
        if item_type == 'book':
            existing = conn.execute(
                "SELECT * FROM borrowed WHERE school_name = ? AND adm = ? AND book_no = ? AND returned = 0",
                (school_name, adm, item_number)
            ).fetchone()
            return existing is not None
        elif item_type == 'chair':
            existing = conn.execute(
                "SELECT * FROM furniture WHERE school_name = ? AND adm = ? AND chair_no = ? AND returned = 0",
                (school_name, adm, item_number)
            ).fetchone()
            return existing is not None
        elif item_type == 'locker':
            existing = conn.execute(
                "SELECT * FROM furniture WHERE school_name = ? AND adm = ? AND locker_no = ? AND returned = 0",
                (school_name, adm, item_number)
            ).fetchone()
            return existing is not None
    finally:
        conn.close()
    return False

# ============ CSS ============
def get_premium_css(wallpaper: Optional[str] = None) -> str:
    wallpaper_url = ""
    
    if wallpaper and wallpaper != "None":
        wallpaper_url = WALLPAPERS.get(wallpaper, "")
        
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
        .stDataFrame th {{ 
            background: rgba(233,69,96,0.8) !important; 
            color: #FFFFFF !important; 
            font-weight: 700 !important; 
        }}
        .stDataFrame td {{ 
            background: rgba(255,255,255,0.05) !important; 
            color: #FFFFFF !important; 
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
if 'chat_with' not in st.session_state:
    st.session_state.chat_with = None
if 'selected_emoji' not in st.session_state:
    st.session_state.selected_emoji = None
if 'editing_note' not in st.session_state:
    st.session_state.editing_note = None

# Apply CSS
st.markdown(get_premium_css(st.session_state.wallpaper), unsafe_allow_html=True)

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
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔑 Staff Login", use_container_width=True):
            st.session_state.action = 'login'
            st.rerun()
    with col2:
        if st.button("📝 Staff Sign Up", use_container_width=True):
            st.session_state.action = 'signup'
            st.rerun()
    with col3:
        if st.button("🏫 Create School", use_container_width=True):
            st.session_state.action = 'create'
            st.rerun()
    with col4:
        if st.button("🔐 Forgot Password", use_container_width=True):
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
            
            conn = get_db_connection()
            try:
                school = conn.execute(
                    "SELECT * FROM schools WHERE name = ? AND is_active = 1", 
                    (school_name,)
                ).fetchone()
                
                if not school:
                    st.error(f"❌ School '{school_name}' not found! Please check the school name.")
                    all_schools = conn.execute("SELECT name FROM schools WHERE is_active = 1").fetchall()
                    if all_schools:
                        st.info(f"Available schools: {', '.join([s['name'] for s in all_schools])}")
                    return
                
                user = conn.execute(
                    "SELECT * FROM users WHERE LOWER(name) = ? AND school_name = ? AND code = ? AND is_active = 1",
                    (name.lower(), school_name, invite_code.upper())
                ).fetchone()
                
                if not user:
                    st.error("❌ User not found! Check your name and invite code.")
                    return
                
                user_dict = dict(user)
                
                if not verify_password(password, user_dict['password']):
                    st.error("❌ Invalid password!")
                    return
                
                st.session_state.user = user_dict
                st.session_state.school = dict(school)
                st.session_state.page = 'dashboard'
                st.session_state.action = None
                st.session_state.chat_with = None
                
                # Update last login
                conn.execute(
                    "UPDATE users SET last_login = ? WHERE email = ? AND school_name = ?",
                    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_dict['email'], school_name)
                )
                conn.commit()
                
                add_audit_entry('Login', f"{user_dict['name']} logged in as {user_dict['role']}")
                st.success("✅ Login successful!")
                time.sleep(0.5)
                st.rerun()
            except Exception as e:
                st.error(f"Login error: {str(e)}")
            finally:
                conn.close()
        
        if forgot:
            st.session_state.action = 'forgot_password'
            st.rerun()

def forgot_password_form():
    st.markdown('<h3 style="color:#FFFFFF;">🔐 Reset Password</h3>', unsafe_allow_html=True)
    
    with st.form("frm_forgot_password"):
        email = st.text_input("📧 Registered Email", placeholder="Enter your registered email")
        school_name = st.text_input("🏢 School Name", placeholder="Enter school name")
        
        if st.form_submit_button("📤 Send Reset Token", use_container_width=True):
            if not email or not school_name:
                st.error("Please fill in all fields!")
                return
            
            conn = get_db_connection()
            try:
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
                    conn.commit()
                    
                    st.success("✅ Reset token generated!")
                    st.info(f"🔑 Token: `{token[:16]}...` (In production, this would be emailed)")
                    st.session_state.reset_email = email
                    st.session_state.reset_school = school_name
                else:
                    st.error("❌ No active user found with that email!")
            finally:
                conn.close()

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
            
            if '@' not in email or '.' not in email:
                st.error("Please enter a valid email address!")
                return
            
            conn = get_db_connection()
            try:
                school = conn.execute(
                    "SELECT * FROM schools WHERE name = ? AND is_active = 1", 
                    (school_name,)
                ).fetchone()
                
                if not school:
                    st.error(f"❌ School '{school_name}' not found! Please check the school name or create a new school.")
                    all_schools = conn.execute("SELECT name FROM schools WHERE is_active = 1").fetchall()
                    if all_schools:
                        st.info(f"Available schools: {', '.join([s['name'] for s in all_schools])}")
                    else:
                        st.info("No schools exist yet. Please create a school first.")
                    return
                
                school_dict = dict(school)
                
                if school_dict.get('invite_code', '') != invite_code.upper():
                    st.error(f"❌ Invalid invite code! Please check with your administrator.")
                    return
                
                existing = conn.execute(
                    "SELECT * FROM users WHERE email = ? AND school_name = ?",
                    (email, school_name)
                ).fetchone()
                
                if existing:
                    st.error("❌ Email already registered in this school!")
                    return
                
                hashed_password = hash_password(password)
                join_date = datetime.now().strftime("%Y-%m-%d")
                
                conn.execute(
                    """INSERT INTO users (email, school_name, name, phone, staff_id, code, password, role, joined, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""",
                    (email, school_name, name, phone, staff_id or f"STAFF-{generate_code('', 4)}",
                     invite_code.upper(), hashed_password, 'teacher', join_date)
                )
                conn.commit()
                
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
            except Exception as e:
                st.error(f"Signup error: {str(e)}")
            finally:
                conn.close()

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
            
            conn = get_db_connection()
            try:
                existing = conn.execute(
                    "SELECT * FROM schools WHERE name = ?", (school_name,)
                ).fetchone()
                
                if existing:
                    st.error(f"❌ School '{school_name}' already exists!")
                    return
                
                invite_code = generate_code()
                created_date = datetime.now().strftime("%Y-%m-%d")
                academic_year = get_academic_year()
                
                conn.execute(
                    """INSERT INTO schools (name, address, admin_name, admin_email, admin_phone, invite_code, created, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1)""",
                    (school_name, address, admin_name, admin_email, admin_phone, invite_code, created_date)
                )
                
                hashed_password = hash_password(password)
                
                conn.execute(
                    """INSERT INTO users (email, school_name, name, phone, staff_id, code, password, role, joined, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""",
                    (admin_email, school_name, admin_name, admin_phone, "ADMIN-001", 
                     invite_code, hashed_password, "admin", created_date)
                )
                
                # Create default term
                conn.execute(
                    """INSERT INTO academic_terms (school_name, name, start_date, end_date, is_current, created_by)
                    VALUES (?, ?, ?, ?, 1, ?)""",
                    (school_name, 'Term 1', created_date, 
                     (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'), admin_name)
                )
                
                conn.execute(
                    "INSERT INTO system_settings (school_name, max_borrow_days, max_books_per_student) VALUES (?, ?, ?)",
                    (school_name, 14, 3)
                )
                conn.commit()
                
                school = conn.execute(
                    "SELECT * FROM schools WHERE name = ?", (school_name,)
                ).fetchone()
                user = conn.execute(
                    "SELECT * FROM users WHERE email = ? AND school_name = ?", 
                    (admin_email, school_name)
                ).fetchone()
                
                st.session_state.user = dict(user)
                st.session_state.school = dict(school)
                st.session_state.page = 'dashboard'
                st.session_state.action = None
                st.session_state.chat_with = None
                
                add_audit_entry('School Created', f"{school_name} created by {admin_name}")
                st.success(f"🎉 School created successfully!")
                st.info(f"🔑 Invite Code: `{invite_code}`")
                st.balloons()
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Error creating school: {str(e)}")
            finally:
                conn.close()

# ============ DASHBOARD PAGE ============
def dashboard_page():
    school_name = st.session_state.school['name']
    user = st.session_state.user
    academic_year = get_academic_year()
    current_term = get_current_term(school_name)
    term_name = current_term.get('name', 'Current Term')
    
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;margin-bottom:25px;">
        <h1 style="font-size:2.2em;">🏫 {sanitize_html(school_name)}</h1>
        <p style="font-size:1.1em;color:#FFFFFF;">👤 {sanitize_html(user['name'])} 
        <span style="background:{'#e94560' if user['role']=='admin' else '#0f3460'};color:#FFF;padding:4px 12px;
        border-radius:20px;font-size:0.8em;margin-left:10px;">{sanitize_html(user['role'].upper())}</span>
        | 📅 {academic_year} | 📖 {term_name}</p>
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
        </div>
        """, unsafe_allow_html=True)
        
        # Theme
        with st.expander("🎨 Theme", expanded=False):
            all_wallpapers = list(WALLPAPERS.keys())
            current_idx = list(WALLPAPERS.keys()).index(st.session_state.wallpaper) if st.session_state.wallpaper in WALLPAPERS else 0
            wallpaper = st.selectbox("Wallpaper:", all_wallpapers, index=current_idx)
            if wallpaper != st.session_state.wallpaper:
                st.session_state.wallpaper = wallpaper
                st.rerun()
        
        st.markdown("---")
        
        # Navigation
        with st.expander("📊 MAIN", expanded=True):
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.current_section = 'dashboard'
                st.rerun()
        
        with st.expander("📖 LIBRARY", expanded=False):
            if st.button("📖 Book Issuing", use_container_width=True):
                st.session_state.current_section = 'bookIssuing'
                st.rerun()
            if st.button("👤 Lend Book", use_container_width=True):
                st.session_state.current_section = 'individualLending'
                st.rerun()
            if st.button("↩️ Returns", use_container_width=True):
                st.session_state.current_section = 'return'
                st.rerun()
            if st.button("📋 Borrowed", use_container_width=True):
                st.session_state.current_section = 'borrowedLog'
                st.rerun()
            if st.button("📚 Catalog", use_container_width=True):
                st.session_state.current_section = 'bookCatalog'
                st.rerun()
        
        with st.expander("🪑 RESOURCES", expanded=False):
            if st.button("🪑 Furniture", use_container_width=True):
                st.session_state.current_section = 'furnitureAllocation'
                st.rerun()
            if st.button("📊 Furniture Records", use_container_width=True):
                st.session_state.current_section = 'furnitureRecords'
                st.rerun()
            if st.button("📱 QR Codes", use_container_width=True):
                st.session_state.current_section = 'qr'
                st.rerun()
        
        with st.expander("👥 PEOPLE", expanded=False):
            if st.button("👥 Members", use_container_width=True):
                st.session_state.current_section = 'memberManagement'
                st.rerun()
            if st.button("👨‍🏫 Teachers", use_container_width=True):
                st.session_state.current_section = 'teacherAllocation'
                st.rerun()
            if st.button("📋 Classes", use_container_width=True):
                st.session_state.current_section = 'classListManager'
                st.rerun()
            if st.button("📅 Terms", use_container_width=True):
                st.session_state.current_section = 'academicTerms'
                st.rerun()
        
        with st.expander("💬 COMMUNICATION", expanded=False):
            if st.button("💬 Private Chat", use_container_width=True):
                st.session_state.current_section = 'chat'
                st.rerun()
            if st.button("📢 Group Forum", use_container_width=True):
                st.session_state.current_section = 'forum'
                st.rerun()
            if st.button("📝 Notepad", use_container_width=True):
                st.session_state.current_section = 'notepad'
                st.rerun()
        
        with st.expander("📈 TOOLS", expanded=False):
            if st.button("🔍 Overview", use_container_width=True):
                st.session_state.current_section = 'systemOverview'
                st.rerun()
            if st.button("📝 Audit Log", use_container_width=True):
                st.session_state.current_section = 'auditLog'
                st.rerun()
            if st.button("📈 Reports", use_container_width=True):
                st.session_state.current_section = 'reports'
                st.rerun()
        
        if is_admin():
            with st.expander("⚙️ ADMIN", expanded=False):
                if st.button("⚙️ Settings", use_container_width=True):
                    st.session_state.current_section = 'settings'
                    st.rerun()
                if st.button("🗄️ Database Manager", use_container_width=True):
                    st.session_state.current_section = 'databaseManager'
                    st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            add_audit_entry('Logout', user['name'])
            st.session_state.user = None
            st.session_state.school = None
            st.session_state.page = 'startup'
            st.rerun()
        
        st.markdown('<p style="color:rgba(255,255,255,0.4);font-size:0.7em;text-align:center;">SRMS v8.0 | WeGEM | © 2025</p>', unsafe_allow_html=True)
    
    # MAIN CONTENT
    section = st.session_state.get('current_section', 'dashboard')
    
    if section == 'dashboard':
        render_dashboard()
    elif section == 'bookIssuing':
        render_book_issuing()
    elif section == 'individualLending':
        render_individual_lending()
    elif section == 'furnitureAllocation':
        render_furniture_allocation()
    elif section == 'furnitureRecords':
        render_furniture_records()
    elif section == 'return':
        render_returns()
    elif section == 'borrowedLog':
        render_borrowed_records()
    elif section == 'memberManagement':
        render_members()
    elif section == 'bookCatalog':
        render_catalog()
    elif section == 'teacherAllocation':
        render_teachers()
    elif section == 'classListManager':
        render_classes()
    elif section == 'academicTerms':
        render_academic_terms()
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
    """Dashboard with separated allocation views by class and date"""
    school_name = st.session_state.school['name']
    academic_year = get_academic_year()
    current_term = get_current_term(school_name)
    term_name = current_term.get('name', 'Current Term')
    
    books = load_school_data('books', [])
    borrowed = load_school_data('borrowed', [])
    furniture = load_school_data('furniture', [])
    members = load_school_data('members', [])
    classes = load_school_data('classes', [])
    
    total_books = sum(b.get('quantity', 0) for b in books)
    available_books = sum(b.get('available', 0) for b in books)
    active_borrowed = len([b for b in borrowed if not b.get('returned')])
    active_furniture = len([f for f in furniture if not f.get('returned')])
    overdue_books = len([b for b in borrowed if not b.get('returned') and b.get('return_date', '') < datetime.now().strftime('%Y-%m-%d')])
    
    st.markdown(f'<div class="glass-card"><h2>📊 Dashboard - {term_name} ({academic_year})</h2>', unsafe_allow_html=True)
    
    # Stats row
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{total_books}</div><div class="stat-label">Total Books</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{available_books}</div><div class="stat-label">Available</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{active_borrowed}</div><div class="stat-label">Book Loans</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{overdue_books}</div><div class="stat-label">⚠️ Overdue</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{active_furniture}</div><div class="stat-label">Furniture</div></div>', unsafe_allow_html=True)
    with col6:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(members)}</div><div class="stat-label">Members</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown('<div class="glass-card"><h3>⚡ Quick Actions</h3>', unsafe_allow_html=True)
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
        if st.button("🪑 Allocate Furniture", use_container_width=True):
            st.session_state.current_section = 'furnitureAllocation'
            st.rerun()
    with col_d:
        if st.button("📊 Reports", use_container_width=True):
            st.session_state.current_section = 'reports'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SEPARATED ALLOCATIONS BY CLASS
    st.markdown('<div class="glass-card"><h3>📋 Allocations by Class</h3>', unsafe_allow_html=True)
    
    if classes:
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            selected_class = st.selectbox("Select Class:", ["All Classes"] + [f"{c['name']} {c.get('stream', '')}" for c in classes], key="dash_class")
        with filter_col2:
            view_type = st.radio("View:", ["📖 Books", "🪑 Furniture", "Both"], horizontal=True, key="dash_view")
        with filter_col3:
            date_filter = st.selectbox("Time Period:", ["All Time", "Today", "This Week", "This Month", "This Term"], key="dash_date")
        
        now = datetime.now()
        if date_filter == "Today":
            date_limit = now.strftime('%Y-%m-%d')
            date_field_book = 'borrow_date'
            date_field_furn = 'allocation_date'
        elif date_filter == "This Week":
            date_limit = (now - timedelta(days=now.weekday())).strftime('%Y-%m-%d')
            date_field_book = 'borrow_date'
            date_field_furn = 'allocation_date'
        elif date_filter == "This Month":
            date_limit = now.replace(day=1).strftime('%Y-%m-%d')
            date_field_book = 'borrow_date'
            date_field_furn = 'allocation_date'
        elif date_filter == "This Term":
            date_limit = current_term.get('start_date', '2000-01-01')
            date_field_book = 'borrow_date'
            date_field_furn = 'allocation_date'
        else:
            date_limit = "2000-01-01"
            date_field_book = 'borrow_date'
            date_field_furn = 'allocation_date'
        
        # Process each class
        for cls in classes:
            class_display = f"{cls['name']} {cls.get('stream', '')}"
            if selected_class != "All Classes" and class_display != selected_class:
                continue
            
            students = cls.get('students', [])
            if not students:
                continue
            
            # Get student identifiers
            student_names = [s.get('name', s.get('Name', '')) for s in students]
            student_adms = [str(s.get('adm', s.get('ADM', ''))) for s in students]
            
            # Filter allocations for this class
            class_books = []
            class_furniture = []
            
            if view_type in ["📖 Books", "Both"]:
                for b in borrowed:
                    name_match = b.get('student_name', '') in student_names or b.get('name', '') in student_names
                    adm_match = str(b.get('adm', '')) in student_adms
                    form_match = b.get('form', '') == cls['name']
                    date_match = b.get(date_field_book, '') >= date_limit
                    
                    if (name_match or adm_match or form_match) and date_match and not b.get('returned'):
                        class_books.append(b)
            
            if view_type in ["🪑 Furniture", "Both"]:
                for f in furniture:
                    name_match = f.get('student_name', '') in student_names or f.get('name', '') in student_names
                    adm_match = str(f.get('adm', '')) in student_adms
                    form_match = f.get('form', '') == cls['name']
                    date_match = f.get(date_field_furn, '') >= date_limit
                    
                    if (name_match or adm_match or form_match) and date_match and not f.get('returned'):
                        class_furniture.append(f)
            
            # Display class card
            with st.expander(f"📋 {class_display} - 📖 {len(class_books)} books | 🪑 {len(class_furniture)} furniture | 👨‍🎓 {len(students)} students"):
                tab1, tab2 = st.tabs(["📖 Books", "🪑 Furniture"])
                
                with tab1:
                    if class_books:
                        books_df = pd.DataFrame(class_books)
                        display_cols = ['student_name', 'adm', 'book_title', 'book_no', 'borrow_date', 'return_date']
                        available_cols = [c for c in display_cols if c in books_df.columns]
                        if not available_cols:
                            available_cols = books_df.columns.tolist()
                        st.dataframe(books_df[available_cols], use_container_width=True)
                    else:
                        st.info("No active book loans for this class")
                
                with tab2:
                    if class_furniture:
                        furn_df = pd.DataFrame(class_furniture)
                        display_cols = ['student_name', 'adm', 'chair_no', 'locker_no', 'allocation_date']
                        available_cols = [c for c in display_cols if c in furn_df.columns]
                        if not available_cols:
                            available_cols = furn_df.columns.tolist()
                        st.dataframe(furn_df[available_cols], use_container_width=True)
                    else:
                        st.info("No active furniture allocations for this class")
    else:
        st.info("No classes found. Add classes first in the Class List Manager.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Overdue alerts
    if overdue_books > 0:
        st.markdown(f'<div class="glass-card" style="border-left: 4px solid #ff4444;"><h3>⚠️ Overdue Books ({overdue_books})</h3>', unsafe_allow_html=True)
        overdue_list = [b for b in borrowed if not b.get('returned') and b.get('return_date', '') < datetime.now().strftime('%Y-%m-%d')]
        if overdue_list:
            overdue_df = pd.DataFrame(overdue_list)
            display_cols = ['student_name', 'book_title', 'book_no', 'return_date', 'form']
            available_cols = [c for c in display_cols if c in overdue_df.columns]
            st.dataframe(overdue_df[available_cols].head(10), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_book_issuing():
    """Book issuing with class-based allocation"""
    school_name = st.session_state.school['name']
    books = load_school_data('books', [])
    classes = load_school_data('classes', [])
    academic_year = get_academic_year()
    current_term = get_current_term(school_name)
    
    st.markdown('<div class="glass-card"><h2>📖 Book Issuing (Class-Based)</h2>', unsafe_allow_html=True)
    
    if not books:
        st.warning("No books in catalog. Add books first.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    if not classes:
        st.warning("No classes available. Add classes first.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        class_options = [f"{c['name']} {c.get('stream', '')}" for c in classes]
        selected_class_str = st.selectbox("Select Class:", class_options)
        selected_class = classes[class_options.index(selected_class_str)]
    with col2:
        book_options = [b['title'] for b in books if b.get('available', b.get('quantity', 0)) > 0]
        selected_book = st.selectbox("Select Book:", book_options if book_options else ["No books available"])
    with col3:
        issue_date = st.date_input("Issue Date:", datetime.now())
    
    col4, col5 = st.columns(2)
    with col4:
        return_date = st.date_input("Return Date:", datetime.now() + timedelta(days=14))
    with col5:
        term_name = st.text_input("Term:", value=current_term.get('name', 'Term 1'))
    
    if selected_class and selected_class.get('students'):
        students = selected_class['students']
        class_name = selected_class['name']
        class_stream = selected_class.get('stream', '')
        
        st.markdown(f"### Students in {class_name} {class_stream} ({len(students)} students)")
        
        student_data = []
        for student in students:
            student_data.append({
                'Name': student.get('name', student.get('Name', '')),
                'ADM': str(student.get('adm', student.get('ADM', ''))),
                'Form': class_name,
                'Stream': class_stream,
                'Book No': '',
                'Issue': False
            })
        
        df = pd.DataFrame(student_data)
        
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Name": st.column_config.TextColumn("Name", disabled=True),
                "ADM": st.column_config.TextColumn("ADM", disabled=True),
                "Form": st.column_config.TextColumn("Form", disabled=True),
                "Stream": st.column_config.TextColumn("Stream", disabled=True),
                "Book No": st.column_config.TextColumn("Book No", help="Enter book number"),
                "Issue": st.column_config.CheckboxColumn("Issue")
            },
            key="book_issue_editor"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ Issue Selected Books", use_container_width=True, type="primary"):
                issued_count = 0
                conn = get_db_connection()
                try:
                    for _, row in edited_df.iterrows():
                        if row['Issue'] and row['Book No']:
                            adm = str(row['ADM'])
                            book_no = str(row['Book No'])
                            
                            if check_duplicate_assignment(school_name, adm, 'book', book_no):
                                st.warning(f"⚠️ {row['Name']} already has book #{book_no}!")
                                continue
                            
                            conn.execute(
                                """INSERT INTO borrowed (id, school_name, student_name, adm, form, stream, 
                                book_title, book_no, borrow_date, return_date, returned, issued_by, academic_year, term)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)""",
                                (generate_code("BOR"), school_name, str(row['Name']), adm,
                                 class_name, class_stream, selected_book, book_no,
                                 issue_date.strftime('%Y-%m-%d'), return_date.strftime('%Y-%m-%d'),
                                 st.session_state.user['name'], academic_year, term_name)
                            )
                            
                            conn.execute(
                                "UPDATE books SET available = available - 1 WHERE school_name = ? AND title = ? AND available > 0",
                                (school_name, selected_book)
                            )
                            issued_count += 1
                    
                    conn.commit()
                    if issued_count > 0:
                        add_audit_entry('Books Issued', f"{issued_count} copies of '{selected_book}' to {class_name} {class_stream}")
                        st.success(f"✅ Issued {issued_count} books!")
                        st.rerun()
                    else:
                        st.warning("No books selected.")
                finally:
                    conn.close()
        
        with col_btn2:
            if st.button("📋 Auto-Assign Books", use_container_width=True):
                book = next((b for b in books if b['title'] == selected_book), None)
                if book:
                    available = book.get('available', book.get('quantity', 0))
                    st.info(f"📚 {available} copies available for {len(students)} students")
                    if available >= len(students):
                        st.success("Sufficient copies available for all students!")
                    else:
                        st.warning(f"Only {available} copies available. Consider limiting or getting more books.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_individual_lending():
    """Individual book lending"""
    school_name = st.session_state.school['name']
    books = load_school_data('books', [])
    classes = load_school_data('classes', [])
    academic_year = get_academic_year()
    current_term = get_current_term(school_name)
    
    st.markdown('<div class="glass-card"><h2>👤 Individual Lending</h2>', unsafe_allow_html=True)
    
    with st.form("frm_ind_lend"):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Student Name:")
            adm = st.text_input("ADM No:")
        with col2:
            form = st.selectbox("Form/Class:", [""] + [c['name'] for c in classes])
            stream = st.text_input("Stream:")
        with col3:
            book_options = [b['title'] for b in books if b.get('available', b.get('quantity', 0)) > 0]
            selected_book = st.selectbox("Book:", book_options if book_options else ["No books"])
            book_no = st.text_input("Book No:")
        
        col4, col5, col6 = st.columns(3)
        with col4:
            borrow_date = st.date_input("Borrow Date:", datetime.now())
        with col5:
            return_date = st.date_input("Return Date:", datetime.now() + timedelta(days=14))
        with col6:
            term_name = st.text_input("Term:", value=current_term.get('name', 'Term 1'))
        
        if st.form_submit_button("📖 Lend Book", use_container_width=True, type="primary"):
            if name and selected_book and selected_book != "No books" and book_no:
                if check_duplicate_assignment(school_name, adm, 'book', book_no):
                    st.error(f"❌ Student already has book #{book_no}!")
                else:
                    conn = get_db_connection()
                    try:
                        conn.execute(
                            """INSERT INTO borrowed (id, school_name, student_name, adm, form, stream, 
                            book_title, book_no, borrow_date, return_date, returned, issued_by, academic_year, term)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)""",
                            (generate_code("BOR"), school_name, name, adm, form, stream,
                             selected_book, book_no,
                             borrow_date.strftime('%Y-%m-%d'), return_date.strftime('%Y-%m-%d'),
                             st.session_state.user['name'], academic_year, term_name)
                        )
                        conn.execute(
                            "UPDATE books SET available = available - 1 WHERE school_name = ? AND title = ? AND available > 0",
                            (school_name, selected_book)
                        )
                        conn.commit()
                        add_audit_entry('Lend Book', f"{name} borrowed '{selected_book}' (#{book_no})")
                        st.success("✅ Book lent!")
                        st.rerun()
                    finally:
                        conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_furniture_allocation():
    """Furniture allocation with class-based view"""
    school_name = st.session_state.school['name']
    classes = load_school_data('classes', [])
    academic_year = get_academic_year()
    current_term = get_current_term(school_name)
    
    st.markdown('<div class="glass-card"><h2>🪑 Furniture Allocation (Class-Based)</h2>', unsafe_allow_html=True)
    
    if not classes:
        st.warning("No classes available. Add classes first.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        class_options = [f"{c['name']} {c.get('stream', '')}" for c in classes]
        selected_class_str = st.selectbox("Select Class:", class_options)
        selected_class = classes[class_options.index(selected_class_str)]
    with col2:
        allocation_date = st.date_input("Allocation Date:", datetime.now())
    with col3:
        term_name = st.text_input("Term:", value=current_term.get('name', 'Term 1'))
    
    st.markdown("### Furniture Settings")
    col4, col5 = st.columns(2)
    with col4:
        chair_prefix = st.text_input("Chair Prefix:", "CH-")
        chair_start = st.number_input("Chair Start:", 1, 10000, 1)
    with col5:
        locker_prefix = st.text_input("Locker Prefix:", "LK-")
        locker_start = st.number_input("Locker Start:", 1, 10000, 1)
    
    if selected_class and selected_class.get('students'):
        students = selected_class['students']
        class_name = selected_class['name']
        class_stream = selected_class.get('stream', '')
        
        st.markdown(f"### Students in {class_name} {class_stream} ({len(students)} students)")
        
        student_data = []
        for i, student in enumerate(students):
            student_data.append({
                'Name': student.get('name', student.get('Name', '')),
                'ADM': str(student.get('adm', student.get('ADM', ''))),
                'Form': class_name,
                'Stream': class_stream,
                'Chair No': f"{chair_prefix}{chair_start + i}",
                'Locker No': f"{locker_prefix}{locker_start + i}",
                'Allocate': True
            })
        
        df = pd.DataFrame(student_data)
        
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Name": st.column_config.TextColumn("Name", disabled=True),
                "ADM": st.column_config.TextColumn("ADM", disabled=True),
                "Form": st.column_config.TextColumn("Form", disabled=True),
                "Stream": st.column_config.TextColumn("Stream", disabled=True),
                "Chair No": st.column_config.TextColumn("Chair No"),
                "Locker No": st.column_config.TextColumn("Locker No"),
                "Allocate": st.column_config.CheckboxColumn("Allocate")
            },
            key="furniture_editor"
        )
        
        if st.button("✅ Allocate Furniture", use_container_width=True, type="primary"):
            allocated = 0
            conn = get_db_connection()
            try:
                for _, row in edited_df.iterrows():
                    if row['Allocate']:
                        adm = str(row['ADM'])
                        chair_no = str(row['Chair No'])
                        locker_no = str(row['Locker No'])
                        
                        if chair_no and check_duplicate_assignment(school_name, adm, 'chair', chair_no):
                            st.warning(f"⚠️ {row['Name']} already has chair {chair_no}!")
                            continue
                        if locker_no and check_duplicate_assignment(school_name, adm, 'locker', locker_no):
                            st.warning(f"⚠️ {row['Name']} already has locker {locker_no}!")
                            continue
                        
                        conn.execute(
                            """INSERT INTO furniture (id, school_name, student_name, adm, form, stream,
                            chair_no, locker_no, allocation_date, returned, issued_by, academic_year, term)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)""",
                            (generate_code("FUR"), school_name, str(row['Name']), adm,
                             class_name, class_stream, chair_no, locker_no,
                             allocation_date.strftime('%Y-%m-%d'),
                             st.session_state.user['name'], academic_year, term_name)
                        )
                        allocated += 1
                
                conn.commit()
                if allocated > 0:
                    add_audit_entry('Furniture Allocated', f"{allocated} items to {class_name} {class_stream}")
                    st.success(f"✅ Allocated {allocated} furniture items!")
                    st.rerun()
            finally:
                conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_furniture_records():
    """View furniture records with class/date filters"""
    school_name = st.session_state.school['name']
    furniture = load_school_data('furniture', [])
    classes = load_school_data('classes', [])
    
    st.markdown('<div class="glass-card"><h2>📊 Furniture Records</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        class_options = ["All Classes"] + [f"{c['name']} {c.get('stream', '')}" for c in classes]
        filter_class = st.selectbox("Class:", class_options)
    with col2:
        filter_status = st.selectbox("Status:", ["All", "Active", "Returned"])
    with col3:
        filter_date = st.selectbox("Date:", ["All", "Today", "This Week", "This Month", "This Term"])
    
    filtered = furniture
    now = datetime.now()
    
    if filter_class != "All Classes":
        class_name = filter_class.split(" ")[0]
        filtered = [f for f in filtered if f.get('form') == class_name]
    
    if filter_status == "Active":
        filtered = [f for f in filtered if not f.get('returned')]
    elif filter_status == "Returned":
        filtered = [f for f in filtered if f.get('returned')]
    
    if filter_date == "Today":
        filtered = [f for f in filtered if f.get('allocation_date') == now.strftime('%Y-%m-%d')]
    elif filter_date == "This Week":
        week_start = (now - timedelta(days=now.weekday())).strftime('%Y-%m-%d')
        filtered = [f for f in filtered if f.get('allocation_date', '') >= week_start]
    elif filter_date == "This Month":
        month_start = now.replace(day=1).strftime('%Y-%m-%d')
        filtered = [f for f in filtered if f.get('allocation_date', '') >= month_start]
    elif filter_date == "This Term":
        current_term = get_current_term(school_name)
        term_start = current_term.get('start_date', '2000-01-01')
        filtered = [f for f in filtered if f.get('allocation_date', '') >= term_start]
    
    if filtered:
        df = pd.DataFrame(filtered)
        st.dataframe(df, use_container_width=True)
        
        st.metric("Records", len(filtered))
        
        if st.button("📥 Export", use_container_width=True):
            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="furniture_records.xlsx">📥 Download</a>', unsafe_allow_html=True)
    else:
        st.info("No records found")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_returns():
    """Return items with class filter"""
    school_name = st.session_state.school['name']
    classes = load_school_data('classes', [])
    
    st.markdown('<div class="glass-card"><h2>↩️ Return Items</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        search = st.text_input("🔍 Search:", placeholder="Name, ADM, or item number")
    with col2:
        filter_class = st.selectbox("Class:", ["All"] + [c['name'] for c in classes])
    
    if st.button("🔍 Search", use_container_width=True):
        conn = get_db_connection()
        try:
            # Search books
            query = """SELECT * FROM borrowed WHERE school_name = ? AND returned = 0 
                      AND (LOWER(student_name) LIKE ? OR adm LIKE ? OR book_no LIKE ?)"""
            params = [school_name, f"%{search.lower()}%", f"%{search}%", f"%{search}%"]
            
            if filter_class != "All":
                query += " AND form = ?"
                params.append(filter_class)
            
            active_books = conn.execute(query, params).fetchall()
            
            # Search furniture
            query = """SELECT * FROM furniture WHERE school_name = ? AND returned = 0 
                      AND (LOWER(student_name) LIKE ? OR adm LIKE ? OR chair_no LIKE ? OR locker_no LIKE ?)"""
            params = [school_name, f"%{search.lower()}%", f"%{search}%", f"%{search}%", f"%{search}%"]
            
            if filter_class != "All":
                query += " AND form = ?"
                params.append(filter_class)
            
            active_furniture = conn.execute(query, params).fetchall()
        finally:
            conn.close()
        
        st.markdown("### 📚 Books")
        if active_books:
            for item in active_books:
                item_dict = dict(item)
                is_overdue = item_dict.get('return_date', '') < datetime.now().strftime('%Y-%m-%d')
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{item_dict['student_name']}** - {item_dict['book_title']} (#{item_dict['book_no']})")
                    st.write(f"Class: {item_dict.get('form', '')} {item_dict.get('stream', '')}")
                with col2:
                    if is_overdue:
                        st.write(f"⚠️ Due: {item_dict.get('return_date', '')}")
                    else:
                        st.write(f"Due: {item_dict.get('return_date', '')}")
                with col3:
                    if st.button("↩️ Return", key=f"ret_book_{item_dict['id']}"):
                        conn = get_db_connection()
                        try:
                            conn.execute(
                                "UPDATE borrowed SET returned = 1, actual_return_date = ? WHERE id = ?",
                                (datetime.now().strftime('%Y-%m-%d'), item_dict['id'])
                            )
                            conn.execute(
                                "UPDATE books SET available = available + 1 WHERE school_name = ? AND title = ?",
                                (school_name, item_dict['book_title'])
                            )
                            conn.commit()
                            add_audit_entry('Book Returned', item_dict['student_name'])
                            st.success("✅ Returned!")
                            st.rerun()
                        finally:
                            conn.close()
                st.divider()
        else:
            st.info("No matching books")
        
        st.markdown("### 🪑 Furniture")
        if active_furniture:
            for item in active_furniture:
                item_dict = dict(item)
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{item_dict['student_name']}** - Chair: {item_dict['chair_no']}, Locker: {item_dict['locker_no']}")
                with col2:
                    st.write(f"Date: {item_dict.get('allocation_date', '')}")
                with col3:
                    if st.button("↩️ Return", key=f"ret_fur_{item_dict['id']}"):
                        conn = get_db_connection()
                        try:
                            conn.execute(
                                "UPDATE furniture SET returned = 1, return_date = ? WHERE id = ?",
                                (datetime.now().strftime('%Y-%m-%d'), item_dict['id'])
                            )
                            conn.commit()
                            add_audit_entry('Furniture Returned', item_dict['student_name'])
                            st.success("✅ Returned!")
                            st.rerun()
                        finally:
                            conn.close()
                st.divider()
        else:
            st.info("No matching furniture")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_borrowed_records():
    """View borrowed records with filters"""
    school_name = st.session_state.school['name']
    borrowed = load_school_data('borrowed', [])
    classes = load_school_data('classes', [])
    
    st.markdown('<div class="glass-card"><h2>📋 Borrowed Records</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_class = st.selectbox("Class:", ["All"] + [c['name'] for c in classes])
    with col2:
        filter_status = st.selectbox("Status:", ["All", "Active", "Returned", "Overdue"])
    with col3:
        search = st.text_input("Search:", placeholder="Name, ADM, book")
    
    filtered = borrowed
    now = datetime.now()
    
    if filter_class != "All":
        filtered = [b for b in filtered if b.get('form') == filter_class]
    
    if filter_status == "Active":
        filtered = [b for b in filtered if not b.get('returned')]
    elif filter_status == "Returned":
        filtered = [b for b in filtered if b.get('returned')]
    elif filter_status == "Overdue":
        filtered = [b for b in filtered if not b.get('returned') and b.get('return_date', '') < now.strftime('%Y-%m-%d')]
    
    if search:
        s = search.lower()
        filtered = [b for b in filtered if s in b.get('student_name', '').lower() or s in b.get('adm', '').lower() or s in b.get('book_title', '').lower() or s in b.get('book_no', '').lower()]
    
    if filtered:
        df = pd.DataFrame(filtered)
        st.dataframe(df, use_container_width=True)
        
        active = len([b for b in filtered if not b.get('returned')])
        st.metric("Active", active)
        
        if st.button("📥 Export", use_container_width=True):
            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="borrowed.xlsx">📥 Download</a>', unsafe_allow_html=True)
    else:
        st.info("No records")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_members():
    """Member management"""
    school_name = st.session_state.school['name']
    members = load_school_data('members', [])
    
    st.markdown('<div class="glass-card"><h2>👥 Members</h2>', unsafe_allow_html=True)
    
    with st.form("frm_member"):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Name:")
        with col2:
            student_class = st.text_input("Class:")
        with col3:
            stream = st.text_input("Stream:")
        
        if st.form_submit_button("➕ Add", use_container_width=True):
            if name:
                conn = get_db_connection()
                try:
                    conn.execute(
                        "INSERT INTO members (id, school_name, name, student_class, stream, added_by, added_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, 1)",
                        (generate_code("MEM"), school_name, name, student_class, stream, 
                         st.session_state.user['name'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    )
                    conn.commit()
                    add_audit_entry('Member Added', name)
                    st.success("✅ Added!")
                    st.rerun()
                finally:
                    conn.close()
    
    if members:
        st.dataframe(pd.DataFrame(members), use_container_width=True)
    else:
        st.info("No members")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_catalog():
    """Book catalog"""
    school_name = st.session_state.school['name']
    books = load_school_data('books', [])
    
    st.markdown('<div class="glass-card"><h2>📚 Catalog</h2>', unsafe_allow_html=True)
    
    with st.form("frm_book"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            title = st.text_input("Title:")
        with col2:
            btype = st.selectbox("Type:", ["Textbook", "Novel", "Reference", "Magazine", "Other"])
        with col3:
            qty = st.number_input("Qty:", 1, 1000, 1)
        
        if st.form_submit_button("📖 Add", use_container_width=True):
            if title:
                conn = get_db_connection()
                try:
                    existing = conn.execute(
                        "SELECT * FROM books WHERE school_name = ? AND LOWER(title) = ?",
                        (school_name, title.lower())
                    ).fetchone()
                    
                    if existing:
                        conn.execute(
                            "UPDATE books SET quantity = quantity + ?, available = available + ? WHERE id = ?",
                            (qty, qty, existing['id'])
                        )
                    else:
                        conn.execute(
                            "INSERT INTO books (school_name, title, type, quantity, available, created_by, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (school_name, title, btype, qty, qty, st.session_state.user['name'],
                             datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        )
                    conn.commit()
                    add_audit_entry('Book Added', title)
                    st.success("✅ Added!")
                    st.rerun()
                finally:
                    conn.close()
    
    if books:
        search = st.text_input("🔍 Search:", placeholder="Filter by title")
        filtered = books
        if search:
            s = search.lower()
            filtered = [b for b in books if s in b.get('title', '').lower()]
        
        for book in filtered:
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            with col1:
                st.write(f"📖 **{book['title']}**")
            with col2:
                st.write(book.get('type', '-'))
            with col3:
                st.write(f"Total: {book.get('quantity', 0)}")
            with col4:
                st.write(f"Avail: {book.get('available', book.get('quantity', 0))}")
            with col5:
                if is_admin():
                    if st.button("🗑️", key=f"del_book_{book['id']}"):
                        conn = get_db_connection()
                        try:
                            conn.execute("DELETE FROM books WHERE id = ?", (book['id'],))
                            conn.commit()
                            st.success("Deleted!")
                            st.rerun()
                        finally:
                            conn.close()
            st.divider()
    else:
        st.info("No books")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_teachers():
    """Teacher management"""
    school_name = st.session_state.school['name']
    teachers = load_school_data('teachers', [])
    
    st.markdown('<div class="glass-card"><h2>👨‍🏫 Teachers</h2>', unsafe_allow_html=True)
    
    with st.form("frm_teacher"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name:")
            subject = st.text_input("Subjects:")
        with col2:
            classes = st.text_input("Classes:")
            duty = st.text_input("Duty:")
        
        if st.form_submit_button("➕ Add", use_container_width=True):
            if name:
                conn = get_db_connection()
                try:
                    conn.execute(
                        "INSERT INTO teachers (id, school_name, name, subject, classes, duty, added_by, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, 1)",
                        (generate_code("TCH"), school_name, name, subject, classes, duty, st.session_state.user['name'])
                    )
                    conn.commit()
                    add_audit_entry('Teacher Added', name)
                    st.success("✅ Added!")
                    st.rerun()
                finally:
                    conn.close()
    
    if teachers:
        st.dataframe(pd.DataFrame(teachers), use_container_width=True)
    else:
        st.info("No teachers")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_classes():
    """Class list management"""
    school_name = st.session_state.school['name']
    classes = load_school_data('classes', [])
    academic_year = get_academic_year()
    
    st.markdown('<div class="glass-card"><h2>📋 Class Lists</h2>', unsafe_allow_html=True)
    
    uploaded = st.file_uploader("📥 Import Excel", type=['xlsx', 'xls'])
    if uploaded:
        try:
            df = pd.read_excel(uploaded)
            st.dataframe(df.head(), use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                class_name = st.text_input("Class Name:")
            with col2:
                stream = st.text_input("Stream:")
            
            if st.button("💾 Save", use_container_width=True):
                if class_name:
                    students = [{col: str(row[col]) if not pd.isna(row[col]) else "" for col in df.columns} for _, row in df.iterrows()]
                    conn = get_db_connection()
                    try:
                        conn.execute(
                            "INSERT INTO classes (school_name, name, stream, students, created_by, created, academic_year, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, 1)",
                            (school_name, class_name, stream, json.dumps(students), st.session_state.user['name'],
                             datetime.now().strftime("%Y-%m-%d"), academic_year)
                        )
                        conn.commit()
                        add_audit_entry('Class Added', f"{class_name} {stream}")
                        st.success(f"✅ Saved!")
                        st.rerun()
                    finally:
                        conn.close()
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    if classes:
        for cls in classes:
            with st.expander(f"📋 {cls['name']} {cls.get('stream', '')} ({len(cls.get('students', []))} students)"):
                if cls.get('students'):
                    st.dataframe(pd.DataFrame(cls['students']), use_container_width=True)
                if is_admin():
                    if st.button("🗑️ Delete", key=f"del_cls_{cls['id']}"):
                        conn = get_db_connection()
                        try:
                            conn.execute("UPDATE classes SET is_active = 0 WHERE id = ?", (cls['id'],))
                            conn.commit()
                            st.success("Deleted!")
                            st.rerun()
                        finally:
                            conn.close()
    else:
        st.info("No classes")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_academic_terms():
    """Academic terms management"""
    school_name = st.session_state.school['name']
    terms = load_school_data('academic_terms', [])
    
    st.markdown('<div class="glass-card"><h2>📅 Academic Terms</h2>', unsafe_allow_html=True)
    
    with st.form("frm_term"):
        col1, col2, col3 = st.columns(3)
        with col1:
            term_name = st.text_input("Term Name:", placeholder="Term 1")
        with col2:
            start_date = st.date_input("Start:", datetime.now())
        with col3:
            end_date = st.date_input("End:", datetime.now() + timedelta(days=90))
        
        if st.form_submit_button("➕ Add", use_container_width=True):
            if term_name:
                conn = get_db_connection()
                try:
                    conn.execute("UPDATE academic_terms SET is_current = 0 WHERE school_name = ?", (school_name,))
                    conn.execute(
                        """INSERT INTO academic_terms (school_name, name, start_date, end_date, is_current, created_by)
                        VALUES (?, ?, ?, ?, 1, ?)""",
                        (school_name, term_name, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'),
                         st.session_state.user['name'])
                    )
                    conn.commit()
                    st.success(f"✅ Added!")
                    st.rerun()
                finally:
                    conn.close()
    
    if terms:
        for term in terms:
            is_current = term.get('is_current')
            st.markdown(f"""
            <div style="padding:10px;margin:5px 0;border-left:4px solid {'#28a745' if is_current else '#666'};background:rgba(255,255,255,0.05);border-radius:8px;">
                <strong>{term['name']}</strong> {'✅ Current' if is_current else ''}<br>
                {term.get('start_date', '')} → {term.get('end_date', '')}
            </div>
            """, unsafe_allow_html=True)
            if not is_current and is_admin():
                if st.button("✅ Set Current", key=f"set_term_{term['id']}"):
                    conn = get_db_connection()
                    try:
                        conn.execute("UPDATE academic_terms SET is_current = 0 WHERE school_name = ?", (school_name,))
                        conn.execute("UPDATE academic_terms SET is_current = 1 WHERE id = ?", (term['id'],))
                        conn.commit()
                        st.success("Updated!")
                        st.rerun()
                    finally:
                        conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_qr():
    """QR Code generation"""
    st.markdown('<div class="glass-card"><h2>📱 QR Codes</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Generate", "Manual"])
    
    with tab1:
        qr_type = st.selectbox("Type:", ["book", "chair", "locker"])
        col1, col2 = st.columns(2)
        with col1:
            start = st.number_input("Start:", 1, 10000, 1)
        with col2:
            end = st.number_input("End:", 1, 10000, start)
        
        if st.button("Generate", use_container_width=True):
            cols = st.columns(4)
            for i in range(start, min(end + 1, start + 20)):
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(f"{qr_type}-{i}")
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buf = BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)
                img_b64 = base64.b64encode(buf.read()).decode()
                with cols[(i - start) % 4]:
                    st.image(f"data:image/png;base64,{img_b64}", caption=f"{qr_type}: {i}", width=150)
    
    with tab2:
        manual = st.text_input("Code:", placeholder="e.g., book-5")
        if manual:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(manual)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode()
            st.image(f"data:image/png;base64,{img_b64}", caption=manual, width=200)
            st.success(f"✅ {manual}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_chat():
    """Private chat"""
    school_name = st.session_state.school['name']
    user = st.session_state.user
    users = load_school_data('users', [])
    
    st.markdown('<div class="glass-card"><h2>💬 Private Chat</h2>', unsafe_allow_html=True)
    
    other_users = [u for u in users if u['email'] != user['email']]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### 👥 Staff")
        for u in other_users:
            role_icon = "👑" if u['role'] == 'admin' else "👨‍🏫"
            if st.button(f"{role_icon} {u['name']}", key=f"chat_{u['email']}", use_container_width=True):
                st.session_state.chat_with = u['email']
                st.rerun()
    
    with col2:
        if st.session_state.get('chat_with'):
            chat_user = next((u for u in users if u['email'] == st.session_state.chat_with), None)
            if chat_user:
                st.markdown(f"### 💬 {chat_user['name']}")
                
                conn = get_db_connection()
                try:
                    msgs = conn.execute(
                        """SELECT * FROM chat_messages WHERE school_name = ? 
                        AND ((from_email = ? AND to_email = ?) OR (from_email = ? AND to_email = ?))
                        ORDER BY timestamp ASC""",
                        (school_name, user['email'], chat_user['email'], chat_user['email'], user['email'])
                    ).fetchall()
                finally:
                    conn.close()
                
                for msg in msgs:
                    msg_dict = dict(msg)
                    is_mine = msg_dict['from_email'] == user['email']
                    bg = "rgba(233,69,96,0.4)" if is_mine else "rgba(255,255,255,0.15)"
                    align = "flex-end" if is_mine else "flex-start"
                    
                    st.markdown(f"""
                    <div style="display:flex;justify-content:{align};margin:8px 0;">
                        <div style="background:{bg};padding:10px 16px;border-radius:16px;max-width:70%;color:#FFF;">
                            <strong>{sanitize_html(msg_dict['from_name'])}:</strong> {sanitize_html(msg_dict['message'])}
                            <br><small>{msg_dict['timestamp'][:16]}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with st.form(f"chat_form_{chat_user['email']}"):
                    msg = st.text_input("Message:", key="chat_msg")
                    if st.form_submit_button("📤 Send"):
                        if msg:
                            conn = get_db_connection()
                            try:
                                conn.execute(
                                    """INSERT INTO chat_messages (id, school_name, from_email, from_name, to_email, message, timestamp)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                    (generate_code("MSG"), school_name, user['email'], user['name'],
                                     chat_user['email'], msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                )
                                conn.commit()
                                st.rerun()
                            finally:
                                conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_forum():
    """Group forum"""
    school_name = st.session_state.school['name']
    user = st.session_state.user
    
    st.markdown('<div class="glass-card"><h2>📢 Group Forum</h2>', unsafe_allow_html=True)
    
    forum = load_school_data('forum_messages', [])
    
    for msg in forum[-20:]:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.08);padding:10px;border-radius:8px;margin:5px 0;">
            <strong>{sanitize_html(msg['from_name'])}</strong> <small>({msg['timestamp'][:16]})</small><br>
            {sanitize_html(msg['message'])}
        </div>
        """, unsafe_allow_html=True)
    
    with st.form("frm_forum"):
        msg = st.text_area("Message:", key="forum_msg", height=100)
        if st.form_submit_button("📢 Post"):
            if msg:
                conn = get_db_connection()
                try:
                    conn.execute(
                        """INSERT INTO forum_messages (id, school_name, from_email, from_name, role, message, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (generate_code("FRM"), school_name, user['email'], user['name'], user['role'],
                         msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    )
                    conn.commit()
                    st.success("Posted!")
                    st.rerun()
                finally:
                    conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_notepad():
    """Notepad"""
    school_name = st.session_state.school['name']
    user = st.session_state.user
    
    st.markdown('<div class="glass-card"><h2>📝 Notes</h2>', unsafe_allow_html=True)
    
    notes = load_school_data('notepad', [])
    my_notes = [n for n in notes if n.get('author_email') == user['email']]
    
    with st.form("frm_note"):
        title = st.text_input("Title:")
        content = st.text_area("Content:", height=200)
        if st.form_submit_button("💾 Save"):
            if content:
                conn = get_db_connection()
                try:
                    conn.execute(
                        """INSERT INTO notepad (id, school_name, author, author_email, content, title, timestamp, is_private)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 1)""",
                        (generate_code("NOTE"), school_name, user['name'], user['email'],
                         content, title or "Untitled", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    )
                    conn.commit()
                    st.success("Saved!")
                    st.rerun()
                finally:
                    conn.close()
    
    if my_notes:
        for note in my_notes:
            with st.expander(f"📝 {note.get('title', 'Untitled')} - {note.get('timestamp', '')[:16]}"):
                st.markdown(note.get('content', ''))
                if st.button("🗑️", key=f"del_note_{note['id']}"):
                    conn = get_db_connection()
                    try:
                        conn.execute("UPDATE notepad SET is_deleted = 1 WHERE id = ?", (note['id'],))
                        conn.commit()
                        st.rerun()
                    finally:
                        conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_system_overview():
    """System overview"""
    school_name = st.session_state.school['name']
    books = load_school_data('books', [])
    borrowed = load_school_data('borrowed', [])
    furniture = load_school_data('furniture', [])
    members = load_school_data('members', [])
    users = load_school_data('users', [])
    classes = load_school_data('classes', [])
    
    st.markdown('<div class="glass-card"><h2>🔍 Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Books", sum(b.get('quantity', 0) for b in books))
    with col2:
        st.metric("📖 Active", len([b for b in borrowed if not b.get('returned')]))
    with col3:
        st.metric("🪑 Furniture", len([f for f in furniture if not f.get('returned')]))
    with col4:
        st.metric("👥 Staff", len(users))
    
    # Charts
    if classes:
        class_data = []
        for cls in classes:
            class_name = cls['name']
            class_books = len([b for b in borrowed if b.get('form') == class_name and not b.get('returned')])
            class_furniture = len([f for f in furniture if f.get('form') == class_name and not f.get('returned')])
            class_data.append({'Class': class_name, 'Books': class_books, 'Furniture': class_furniture})
        
        if class_data:
            df = pd.DataFrame(class_data)
            fig = px.bar(df, x='Class', y=['Books', 'Furniture'], barmode='group',
                        color_discrete_sequence=['#e94560', '#28a745'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_audit_log():
    """Audit log (admin only)"""
    if not is_admin():
        st.error("🔒 Admin access required!")
        return
    
    audit = load_school_data('audit_log', [])
    
    st.markdown('<div class="glass-card"><h2>📝 Audit Log</h2>', unsafe_allow_html=True)
    
    if audit:
        df = pd.DataFrame(audit)
        st.dataframe(df, use_container_width=True)
        
        if st.button("📥 Export", use_container_width=True):
            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="audit_log.xlsx">📥 Download</a>', unsafe_allow_html=True)
    else:
        st.info("No entries")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_reports():
    """Reports"""
    st.markdown('<div class="glass-card"><h2>📈 Reports</h2>', unsafe_allow_html=True)
    
    report_type = st.selectbox("Type:", ["Books Overview", "Furniture Overview", "Class Allocations", "Overdue Items"])
    
    if st.button("Generate", use_container_width=True):
        school_name = st.session_state.school['name']
        
        if report_type == "Books Overview":
            conn = get_db_connection()
            try:
                data = conn.execute("SELECT * FROM borrowed WHERE school_name = ?", (school_name,)).fetchall()
            finally:
                conn.close()
            if data:
                df = pd.DataFrame([dict(r) for r in data])
                st.dataframe(df, use_container_width=True)
                
                counts = df['returned'].value_counts()
                fig = px.pie(values=[counts.get(0, 0), counts.get(1, 0)], names=['Active', 'Returned'],
                            color_discrete_sequence=['#e94560', '#28a745'])
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "Overdue Items":
            conn = get_db_connection()
            try:
                overdue = conn.execute(
                    "SELECT * FROM borrowed WHERE school_name = ? AND returned = 0 AND return_date < ?",
                    (school_name, datetime.now().strftime('%Y-%m-%d'))
                ).fetchall()
            finally:
                conn.close()
            if overdue:
                st.dataframe(pd.DataFrame([dict(r) for r in overdue]), use_container_width=True)
                st.warning(f"⚠️ {len(overdue)} overdue!")
            else:
                st.success("No overdue!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_settings():
    """Admin settings"""
    if not is_admin():
        st.error("🔒 Admin access required!")
        return
    
    school_name = st.session_state.school['name']
    
    st.markdown('<div class="glass-card"><h2>⚙️ Settings</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Staff", "Terms", "Data"])
    
    with tab1:
        st.markdown("### 👥 Staff Management")
        
        with st.form("frm_staff"):
            col1, col2, col3 = st.columns(3)
            with col1:
                email = st.text_input("Email:")
            with col2:
                name = st.text_input("Name:")
            with col3:
                role = st.selectbox("Role:", ["teacher", "librarian"])
            pwd = st.text_input("Password:", placeholder="Auto if empty")
            
            if st.form_submit_button("➕ Create"):
                if email and name:
                    conn = get_db_connection()
                    try:
                        existing = conn.execute(
                            "SELECT * FROM users WHERE email = ? AND school_name = ?",
                            (email, school_name)
                        ).fetchone()
                        
                        if existing:
                            st.error("Email exists!")
                        else:
                            gen_pw = pwd if pwd else generate_code("", 8)
                            conn.execute(
                                """INSERT INTO users (email, school_name, name, code, password, role, joined, is_active)
                                VALUES (?, ?, ?, ?, ?, ?, ?, 1)""",
                                (email, school_name, name, st.session_state.school['invite_code'],
                                 hash_password(gen_pw), role, datetime.now().strftime("%Y-%m-%d"))
                            )
                            conn.commit()
                            st.success(f"✅ Created! PW: `{gen_pw}`")
                            st.rerun()
                    finally:
                        conn.close()
        
        users = load_school_data('users', [])
        for u in users:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"{'👑' if u['role']=='admin' else '👨‍🏫'} **{u['name']}** ({u['role']})")
            with col2:
                if u['email'] != st.session_state.user['email'] and u['role'] != 'admin':
                    if st.button("👑 Promote", key=f"prom_{u['email']}"):
                        conn = get_db_connection()
                        try:
                            conn.execute("UPDATE users SET role = 'admin' WHERE email = ? AND school_name = ?",
                                       (u['email'], school_name))
                            conn.commit()
                            st.success("Promoted!")
                            st.rerun()
                        finally:
                            conn.close()
            with col3:
                if u['email'] != st.session_state.user['email']:
                    if st.button("🗑️", key=f"del_{u['email']}"):
                        conn = get_db_connection()
                        try:
                            conn.execute("UPDATE users SET is_active = 0 WHERE email = ? AND school_name = ?",
                                       (u['email'], school_name))
                            conn.commit()
                            st.success("Deactivated!")
                            st.rerun()
                        finally:
                            conn.close()
            st.divider()
    
    with tab2:
        render_academic_terms()
    
    with tab3:
        if st.button("📥 Backup", use_container_width=True):
            conn = get_db_connection()
            try:
                tables = ['schools', 'users', 'books', 'borrowed', 'furniture', 'members', 'teachers', 'classes', 'audit_log']
                backup = {}
                for table in tables:
                    rows = conn.execute(f"SELECT * FROM {table} WHERE school_name = ?", (school_name,)).fetchall()
                    backup[table] = [dict(r) for r in rows]
                
                b64 = base64.b64encode(json.dumps(backup, indent=2, default=str).encode()).decode()
                st.markdown(f'<a href="data:application/json;base64,{b64}" download="backup.json">📥 Download</a>', unsafe_allow_html=True)
                st.success("✅ Ready!")
            finally:
                conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_database_manager():
    """Database manager (admin only)"""
    if not is_admin():
        st.error("🔒 Admin access required!")
        return
    
    school_name = st.session_state.school['name']
    
    st.markdown('<div class="glass-card"><h2>🗄️ Database Manager</h2>', unsafe_allow_html=True)
    st.warning("⚠️ Admin only - Handle with care!")
    
    tables = {
        "Schools": "schools", "Users": "users", "Books": "books",
        "Borrowed": "borrowed", "Furniture": "furniture", "Members": "members",
        "Teachers": "teachers", "Classes": "classes", "Terms": "academic_terms",
        "Audit Log": "audit_log", "Chat": "chat_messages", "Forum": "forum_messages"
    }
    
    selected = st.selectbox("Table:", list(tables.keys()))
    table = tables[selected]
    
    conn = get_db_connection()
    try:
        count = conn.execute(f"SELECT COUNT(*) as c FROM {table} WHERE school_name = ?", (school_name,)).fetchone()
        st.metric("Records", count['c'])
        
        data = conn.execute(f"SELECT * FROM {table} WHERE school_name = ? LIMIT 200", (school_name,)).fetchall()
        
        if data:
            df = pd.DataFrame([dict(r) for r in data])
            st.dataframe(df, use_container_width=True, height=400)
            
            if st.button(f"📥 Export", use_container_width=True):
                towrite = BytesIO()
                df.to_excel(towrite, index=False, engine='openpyxl')
                towrite.seek(0)
                b64 = base64.b64encode(towrite.read()).decode()
                st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{table}.xlsx">📥 Download</a>', unsafe_allow_html=True)
        else:
            st.info("No records")
    finally:
        conn.close()
    
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
