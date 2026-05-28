# app.py - SRMS - School Resource Management System by WeGEM
# Complete Fixed Version
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
import calendar

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
        
        cursor.execute("PRAGMA journal_mode=WAL")
        
        # Schools table - simplified
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
        
        # Books table - fixed column order
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT,
                title TEXT,
                author TEXT,
                isbn TEXT,
                type TEXT,
                subject TEXT,
                quantity INTEGER,
                available INTEGER,
                location TEXT,
                created_by TEXT,
                created_at TEXT,
                UNIQUE(school_name, title)
            )
        ''')
        
        # Borrowed books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowed (
                id TEXT PRIMARY KEY,
                school_name TEXT,
                student_name TEXT,
                adm TEXT,
                form TEXT,
                stream TEXT,
                gender TEXT,
                book_title TEXT,
                book_no TEXT,
                borrow_date TEXT,
                return_date TEXT,
                returned INTEGER DEFAULT 0,
                actual_return_date TEXT,
                issued_by TEXT,
                issued_by_email TEXT,
                academic_year TEXT,
                term TEXT,
                status TEXT DEFAULT 'active'
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
                gender TEXT,
                chair_no TEXT,
                locker_no TEXT,
                allocation_date TEXT,
                returned INTEGER DEFAULT 0,
                return_date TEXT,
                issued_by TEXT,
                issued_by_email TEXT,
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
                item_code TEXT,
                condition TEXT DEFAULT 'Good',
                status TEXT DEFAULT 'Available',
                location TEXT,
                notes TEXT,
                added_by TEXT,
                added_date TEXT,
                UNIQUE(school_name, item_code)
            )
        ''')
        
        # Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                adm TEXT,
                school_name TEXT,
                name TEXT,
                form TEXT,
                stream TEXT,
                gender TEXT,
                dob TEXT,
                parent_name TEXT,
                parent_phone TEXT,
                parent_email TEXT,
                address TEXT,
                added_by TEXT,
                added_at TEXT,
                is_active INTEGER DEFAULT 1,
                PRIMARY KEY (adm, school_name)
            )
        ''')
        
        # Teachers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id TEXT PRIMARY KEY,
                school_name TEXT,
                name TEXT,
                email TEXT,
                phone TEXT,
                subjects TEXT,
                classes TEXT,
                duty TEXT,
                tsc_no TEXT,
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
                teacher TEXT,
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
                maintenance_mode INTEGER DEFAULT 0,
                school_motto TEXT
            )
        ''')
        
        # Events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT,
                title TEXT,
                description TEXT,
                event_date TEXT,
                event_type TEXT,
                created_by TEXT,
                created_at TEXT
            )
        ''')
        
        # Fees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fees (
                id TEXT PRIMARY KEY,
                school_name TEXT,
                student_adm TEXT,
                student_name TEXT,
                form TEXT,
                amount REAL,
                paid REAL,
                balance REAL,
                term TEXT,
                academic_year TEXT,
                last_payment_date TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        # Timetable table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timetable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT,
                class_name TEXT,
                day TEXT,
                period TEXT,
                subject TEXT,
                teacher TEXT,
                room TEXT,
                created_by TEXT
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
    "Library Classic": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1920&q=80",
    "Modern Classroom": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80",
    "School Building": "https://images.unsplash.com/photo-1577896851231-70ef18881754?w=1920&q=80",
    "Study Desk": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920&q=80",
    "Bookshelf Heaven": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1920&q=80",
    "Graduation Day": "https://images.unsplash.com/photo-1523050854058-8df90910f68e?w=1920&q=80",
    "Lecture Hall": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=1920&q=80",
    "Computer Lab": "https://images.unsplash.com/photo-1571266028243-e4c84c8a40b7?w=1920&q=80",
    "Science Lab": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=1920&q=80",
    "Playground Fun": "https://images.unsplash.com/photo-1472898965229-f9b06b9c9bbe?w=1920&q=80",
    "School Bus": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=1920&q=80",
    "Art Studio": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=1920&q=80",
    "Music Room": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=1920&q=80",
    "Sports Field": "https://images.unsplash.com/photo-1459865264687-595d652de67e?w=1920&q=80",
    "Cafeteria": "https://images.unsplash.com/photo-1574482620811-1aa16ffe3c82?w=1920&q=80",
    "Sunset Campus": "https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=1920&q=80",
    "Ocean View": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80",
    "Forest Path": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920&q=80",
    "Mountain Peak": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    "Desert Dunes": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920&q=80",
    "Waterfall": "https://images.unsplash.com/photo-1544551763-46a013bb70b5?w=1920&q=80",
    "Cherry Blossom": "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=1920&q=80",
    "Northern Lights": "https://images.unsplash.com/photo-1483347756197-71ef80e95f73?w=1920&q=80",
    "Galaxy Stars": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920&q=80",
    "City Lights": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1920&q=80",
    "Tokyo Night": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1920&q=80",
    "New York": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1920&q=80",
    "Paris": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920&q=80",
    "London": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1920&q=80",
    "Dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1920&q=80",
    "Autumn Leaves": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    "Winter Snow": "https://images.unsplash.com/photo-1477601263568-180e2c6d046e?w=1920&q=80",
    "Spring Flowers": "https://images.unsplash.com/photo-1490750967868-88aa4f44baee?w=1920&q=80",
    "Summer Beach": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80",
    "Rainy Window": "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?w=1920&q=80",
    "Starry Night": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920&q=80",
    "Golden Hour": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=80",
    "Abstract Art": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=1920&q=80",
    "Geometric": "https://images.unsplash.com/photo-1550859492-d5da9d8e45f3?w=1920&q=80",
    "Minimalist": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=1920&q=80",
    "Dark Gradient": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1920&q=80",
    "Blue Abstract": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=1920&q=80",
    "Purple Haze": "https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=1920&q=80",
    "Green Nature": "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=1920&q=80",
    "Sunrise Mountains": "https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=1920&q=80",
    "Architecture": "https://images.unsplash.com/photo-1487958449943-2429e8be8625?w=1920&q=80",
    "Technology": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=80",
    "Knowledge": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1920&q=80",
    "Success": "https://images.unsplash.com/photo-1494178270175-e96de2971df9?w=1920&q=80",
    "Peaceful Garden": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1920&q=80",
    "Math Blackboard": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1920&q=80",
    "Chemistry Lab": "https://images.unsplash.com/photo-1603126857599-f6e157fa2fe6?w=1920&q=80",
    "Physics Lab": "https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?w=1920&q=80",
    "Biology Lab": "https://images.unsplash.com/photo-1530026405186-ed1f139313f8?w=1920&q=80",
    "Geography Class": "https://images.unsplash.com/photo-1526495124232-a04e1849168c?w=1920&q=80",
    "History Museum": "https://images.unsplash.com/photo-1569590034708-18b27e8cb06e?w=1920&q=80",
    "Language Class": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1920&q=80",
    "Drama Theater": "https://images.unsplash.com/photo-1514306191717-452ec28c7814?w=1920&q=80",
    "Dance Studio": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=1920&q=80",
    "Swimming Pool": "https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?w=1920&q=80",
    "Basketball Court": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=1920&q=80",
    "Soccer Field": "https://images.unsplash.com/photo-1459865264687-595d652de67e?w=1920&q=80",
    "Track Field": "https://images.unsplash.com/photo-1461896836934-bd45ba9cf0a5?w=1920&q=80",
    "School Garden": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1920&q=80",
    "School Entrance": "https://images.unsplash.com/photo-1577896851231-70ef18881754?w=1920&q=80",
    "School Hallway": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=1920&q=80",
    "School Lockers": "https://images.unsplash.com/photo-1588072432836-e10032774350?w=1920&q=80",
    "School Bell": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1920&q=80",
    "Reading Corner": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920&q=80",
    "Study Group": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1920&q=80",
    "Graduation Caps": "https://images.unsplash.com/photo-1523050854058-8df90910f68e?w=1920&q=80",
    "Diploma": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80",
    "Pencil Case": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=1920&q=80",
    "Notebook": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920&q=80",
    "Calculator": "https://images.unsplash.com/photo-1587145820266-a5951ee6f620?w=1920&q=80",
    "Microscope": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=1920&q=80",
    "Telescope": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920&q=80",
    "Globe": "https://images.unsplash.com/photo-1526495124232-a04e1849168c?w=1920&q=80",
    "World Map": "https://images.unsplash.com/photo-1524666643752-b381eb00effb?w=1920&q=80",
    "Alphabet Blocks": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1920&q=80",
    "Colored Pencils": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=1920&q=80",
    "Watercolors": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=1920&q=80",
    "Easel": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=1920&q=80",
    "School Trophy": "https://images.unsplash.com/photo-1494178270175-e96de2971df9?w=1920&q=80",
    "Medal": "https://images.unsplash.com/photo-1494178270175-e96de2971df9?w=1920&q=80",
    "Certificate": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920&q=80",
    "Science Fair": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=1920&q=80",
    "Robotics Club": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=80",
    "Chess Club": "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=1920&q=80",
    "Debate Team": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=1920&q=80",
    "School Band": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=1920&q=80",
    "Choir": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=1920&q=80",
    "School Play": "https://images.unsplash.com/photo-1514306191717-452ec28c7814?w=1920&q=80",
    "Career Day": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=1920&q=80",
    "Field Trip": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=1920&q=80",
    "School Assembly": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=1920&q=80",
    "Morning Dew": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=80",
    "Cloudy Sky": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    "Rainbow": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    "Lightning": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    "Foggy Morning": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    "Full Moon": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920&q=80",
    "Solar Eclipse": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920&q=80",
    "Milky Way": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920&q=80",
    "Nebula": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920&q=80",
    "Space Station": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920&q=80",
    "Coral Reef": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80",
    "Underwater": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80",
    "Tropical Island": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80",
    "Palm Trees": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80",
    "Bamboo Forest": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920&q=80",
    "Maple Trees": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    "Pine Forest": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920&q=80",
    "Meadow": "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=1920&q=80",
    "Lavender Field": "https://images.unsplash.com/photo-1490750967868-88aa4f44baee?w=1920&q=80",
    "Sunflower Field": "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=1920&q=80",
    "Rose Garden": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1920&q=80",
    "Tulip Field": "https://images.unsplash.com/photo-1490750967868-88aa4f44baee?w=1920&q=80",
    "Orchid": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1920&q=80",
    "Lotus Pond": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1920&q=80",
    "Zen Garden": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1920&q=80",
    "Koi Pond": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1920&q=80",
    "Pagoda": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1920&q=80",
    "Temple": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1920&q=80",
    "Castle": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1920&q=80",
    "Cathedral": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920&q=80",
    "Mosque": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1920&q=80",
    "Bridge": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920&q=80",
    "Lighthouse": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80",
    "Windmill": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=80",
    "Hot Air Balloon": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=80",
    "Airplane Wing": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    "Train Tracks": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920&q=80",
    "Vintage Car": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=80",
}

# ============ EMOJI CATEGORIES ============
EMOJI_CATEGORIES = {
    "😀 Smileys": ["😀", "😃", "😄", "😁", "😅", "😂", "🤣", "😊", "😇", "🙂", "😉", "😌", "😍", "🥰", "😘"],
    "👍 Gestures": ["👍", "👎", "👌", "✌️", "🤞", "🤟", "🤘", "🤙", "👈", "👉", "👆", "👇", "☝️", "✋", "🤚"],
    "❤️ Hearts": ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔", "❣️", "💕", "💞", "💓", "💗"],
    "📚 School": ["📚", "📖", "📝", "✏️", "🖊️", "📏", "📐", "🎓", "🏫", "📋", "📎", "🖇️", "🗂️", "📁", "📌"],
    "🎯 Symbols": ["🎯", "⭐", "🌟", "✨", "🔥", "💯", "✅", "❌", "⚠️", "🔔", "📢", "📣", "💡", "🔑", "🔒"],
}

# ============ HELPER FUNCTIONS ============
def sanitize_html(text: str) -> str:
    if not text:
        return ""
    return html.escape(str(text))

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False

def generate_code(prefix: str = "", length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits
    return prefix + ''.join(random.choices(chars, k=length))

def generate_reset_token() -> str:
    return hashlib.sha256(os.urandom(32)).hexdigest()

def is_admin() -> bool:
    if not st.session_state.get('user'):
        return False
    return st.session_state.user.get('role') == 'admin'

def is_authenticated() -> bool:
    return st.session_state.get('user') is not None and st.session_state.get('school') is not None

def get_current_date_display() -> str:
    """Get formatted current date like 'Monday, January 5th 2026'"""
    now = datetime.now()
    day_name = now.strftime("%A")
    month_name = now.strftime("%B")
    day = now.day
    year = now.year
    
    # Add ordinal suffix
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    
    return f"{day_name}, {month_name} {day}{suffix} {year}"

def add_audit_entry(action: str, details: str):
    try:
        school_name = st.session_state.school.get('name', 'Unknown') if is_authenticated() else "Unknown"
        user_name = st.session_state.user.get('name', 'System') if st.session_state.get('user') else "System"
        user_email = st.session_state.user.get('email', 'system@srms.local') if st.session_state.get('user') else "system@srms.local"
        
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO audit_log (school_name, timestamp, user, user_email, action, details, ip_address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (school_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                 user_name, user_email, action, details, '127.0.0.1')
            )
            conn.commit()
        finally:
            conn.close()
    except Exception as e:
        print(f"Audit log error: {str(e)}")

def get_current_term(school_name: str) -> Dict:
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
    now = datetime.now()
    if now.month >= 9:
        return f"{now.year}-{now.year + 1}"
    else:
        return f"{now.year - 1}-{now.year}"

def load_school_data(data_type: str, default: Any = None) -> Any:
    if not is_authenticated():
        return default if default is not None else []
    
    school_name = st.session_state.school['name']
    user_email = st.session_state.user['email']
    is_user_admin = is_admin()
    
    conn = get_db_connection()
    
    try:
        if data_type == 'books':
            cursor = conn.execute("SELECT * FROM books WHERE school_name = ?", (school_name,))
            return [dict(row) for row in cursor.fetchall()]
        elif data_type == 'borrowed':
            if is_user_admin:
                cursor = conn.execute("SELECT * FROM borrowed WHERE school_name = ? ORDER BY borrow_date DESC", (school_name,))
            else:
                cursor = conn.execute("SELECT * FROM borrowed WHERE school_name = ? AND issued_by_email = ? ORDER BY borrow_date DESC", 
                                    (school_name, user_email))
            return [dict(row) for row in cursor.fetchall()]
        elif data_type == 'furniture':
            if is_user_admin:
                cursor = conn.execute("SELECT * FROM furniture WHERE school_name = ? ORDER BY allocation_date DESC", (school_name,))
            else:
                cursor = conn.execute("SELECT * FROM furniture WHERE school_name = ? AND issued_by_email = ? ORDER BY allocation_date DESC", 
                                    (school_name, user_email))
            return [dict(row) for row in cursor.fetchall()]
        elif data_type == 'students':
            cursor = conn.execute("SELECT * FROM students WHERE school_name = ? AND is_active = 1", (school_name,))
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
                "SELECT * FROM notepad WHERE school_name = ? AND is_deleted = 0 AND (author_email = ? OR is_private = 0)",
                (school_name, user_email))
            return [dict(row) for row in cursor.fetchall()]
        elif data_type == 'audit_log':
            if is_user_admin:
                cursor = conn.execute(
                    "SELECT * FROM audit_log WHERE school_name = ? ORDER BY timestamp DESC LIMIT 500",
                    (school_name,))
            else:
                cursor = conn.execute(
                    "SELECT * FROM audit_log WHERE school_name = ? AND user_email = ? ORDER BY timestamp DESC LIMIT 100",
                    (school_name, user_email))
            return [dict(row) for row in cursor.fetchall()]
        elif data_type == 'users':
            cursor = conn.execute(
                "SELECT * FROM users WHERE school_name = ? AND is_active = 1",
                (school_name,))
            return [dict(row) for row in cursor.fetchall()]
        elif data_type == 'system_settings':
            cursor = conn.execute(
                "SELECT * FROM system_settings WHERE school_name = ?",
                (school_name,))
            row = cursor.fetchone()
            return dict(row) if row else {}
        elif data_type == 'events':
            cursor = conn.execute("SELECT * FROM events WHERE school_name = ? ORDER BY event_date", (school_name,))
            return [dict(row) for row in cursor.fetchall()]
        elif data_type == 'fees':
            cursor = conn.execute("SELECT * FROM fees WHERE school_name = ?", (school_name,))
            return [dict(row) for row in cursor.fetchall()]
        elif data_type == 'timetable':
            cursor = conn.execute("SELECT * FROM timetable WHERE school_name = ? ORDER BY day, period", (school_name,))
            return [dict(row) for row in cursor.fetchall()]
        else:
            return default if default is not None else []
    except Exception as e:
        print(f"Error loading {data_type}: {str(e)}")
        return default if default is not None else []
    finally:
        conn.close()

def check_duplicate_assignment(school_name: str, adm: str, item_type: str, item_number: str) -> bool:
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

# ============ CSS WITH DYNAMIC TEXT CONTRAST ============
def get_premium_css(wallpaper: Optional[str] = None) -> str:
    wallpaper_url = ""
    has_wallpaper = False
    
    if wallpaper and wallpaper != "None":
        wallpaper_url = WALLPAPERS.get(wallpaper, "")
        if wallpaper_url:
            has_wallpaper = True
    
    if has_wallpaper:
        bg_style = f"""
            background-image: url('{wallpaper_url}'); 
            background-size: cover; 
            background-position: center; 
            background-attachment: fixed;
        """
        # Darker overlay for better text readability with wallpapers
        overlay_opacity = "0.8"
        card_bg = "rgba(0,0,0,0.75)"
        card_border = "rgba(255,255,255,0.2)"
    else:
        bg_style = """
            background: linear-gradient(135deg, #0a0e27, #1a1f4e, #0f3460);
        """
        overlay_opacity = "0.75"
        card_bg = "rgba(0,0,0,0.6)"
        card_border = "rgba(212,175,55,0.25)"
    
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        * {{ font-family: 'Inter', sans-serif; }}
        
        .stApp {{ {bg_style} }}
        .stApp > header {{ 
            background: rgba(0,0,0,0.85) !important; 
            backdrop-filter: blur(30px) !important; 
            border-bottom: 2px solid rgba(212,175,55,0.3) !important; 
        }}
        
        .main .block-container {{ 
            background: rgba(0,0,0,{overlay_opacity}) !important; 
            backdrop-filter: blur(25px) !important; 
            border-radius: 20px !important; 
            padding: 2rem !important; 
            margin: 1rem !important; 
            border: 1px solid {card_border} !important; 
        }}
        
        .main .block-container h1, .main .block-container h2, .main .block-container h3, .main .block-container h4 {{ 
            color: #FFFFFF !important; 
            text-shadow: 2px 2px 8px rgba(0,0,0,0.9), 0 0 30px rgba(0,0,0,0.7) !important; 
        }}
        .main .block-container p, .main .block-container span, .main .block-container label, .main .block-container div {{ 
            color: #FFFFFF !important; 
            text-shadow: 1px 1px 4px rgba(0,0,0,0.8), 0 0 20px rgba(0,0,0,0.5) !important; 
        }}
        
        .glass-card {{ 
            background: {card_bg} !important; 
            backdrop-filter: blur(20px) !important; 
            border-radius: 16px !important; 
            padding: 25px !important; 
            margin: 15px 0 !important; 
            border: 1px solid {card_border} !important; 
            box-shadow: 0 10px 40px rgba(0,0,0,0.5) !important; 
        }}
        
        .stat-card {{ 
            background: rgba(0,0,0,0.7) !important; 
            backdrop-filter: blur(15px) !important; 
            padding: 20px !important; 
            border-radius: 16px !important; 
            border-left: 4px solid #e94560 !important; 
            border: 1px solid rgba(255,255,255,0.15) !important; 
            text-align: center !important; 
            margin: 8px 0 !important; 
        }}
        .stat-value {{ 
            font-size: 2.2em !important; 
            font-weight: 900 !important; 
            color: #FFFFFF !important; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
        }}
        .stat-label {{ 
            color: rgba(255,255,255,0.95) !important; 
            font-size: 0.9em !important; 
            font-weight: 600 !important; 
            text-shadow: 1px 1px 3px rgba(0,0,0,0.7) !important;
        }}
        
        .stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input, .stSelectbox > div {{ 
            background: rgba(0,0,0,0.7) !important; 
            border: 2px solid rgba(255,255,255,0.3) !important; 
            border-radius: 10px !important; 
            padding: 10px 15px !important; 
            color: #FFFFFF !important; 
            font-weight: 500 !important; 
        }}
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {{ 
            color: rgba(255,255,255,0.5) !important; 
        }}
        
        .stButton button {{ 
            background: linear-gradient(135deg, #e94560, #c62a47) !important; 
            border: none !important; 
            border-radius: 10px !important; 
            color: white !important; 
            font-weight: 600 !important; 
            padding: 10px 20px !important; 
            box-shadow: 0 4px 15px rgba(233,69,96,0.4) !important; 
            transition: all 0.3s ease !important; 
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
        }}
        .stButton button:hover {{ 
            transform: translateY(-2px) !important; 
            box-shadow: 0 8px 25px rgba(233,69,96,0.6) !important; 
        }}
        
        .stDataFrame {{ 
            background: rgba(0,0,0,0.7) !important; 
            backdrop-filter: blur(15px) !important; 
            border-radius: 12px !important; 
            border: 1px solid rgba(255,255,255,0.2) !important; 
        }}
        .stDataFrame th {{ 
            background: rgba(233,69,96,0.8) !important; 
            color: #FFFFFF !important; 
            font-weight: 700 !important; 
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        }}
        .stDataFrame td {{ 
            background: rgba(0,0,0,0.5) !important; 
            color: #FFFFFF !important; 
        }}
        
        .school-code-banner {{ 
            background: rgba(0,0,0,0.7) !important; 
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
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
        }}
        
        .date-display {{
            background: rgba(0,0,0,0.6) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 25px !important;
            padding: 8px 20px !important;
            display: inline-block !important;
            border: 1px solid rgba(212,175,55,0.3) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.7) !important;
        }}
        
        section[data-testid="stSidebar"] {{ 
            background: rgba(0,0,0,0.9) !important; 
            backdrop-filter: blur(20px) !important;
        }}
        section[data-testid="stSidebar"] * {{ 
            color: #FFFFFF !important; 
            text-shadow: 0 1px 3px rgba(0,0,0,0.7) !important; 
        }}
        
        .returned-badge {{ background: #28a745; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; font-weight: 600; }}
        .active-badge {{ background: #e94560; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; font-weight: 600; }}
        .overdue-badge {{ background: #ff4444; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; font-weight: 600; animation: pulse 1s infinite; }}
        
        .stTabs [data-baseweb="tab"] {{
            color: #FFFFFF !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.7) !important;
        }}
        
        .stSelectbox label, .stTextInput label, .stDateInput label {{
            color: #FFFFFF !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.7) !important;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        @media (max-width: 768px) {{ 
            .main .block-container {{ padding: 1rem !important; margin: 0.5rem !important; }} 
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
    st.session_state.wallpaper = "Library Classic"
if 'current_section' not in st.session_state:
    st.session_state.current_section = 'dashboard'
if 'action' not in st.session_state:
    st.session_state.action = None
if 'chat_with' not in st.session_state:
    st.session_state.chat_with = None

# Apply CSS
st.markdown(get_premium_css(st.session_state.wallpaper), unsafe_allow_html=True)

# ============ AUTH PAGES ============
def startup_page():
    current_date = get_current_date_display()
    
    st.markdown(f"""
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
        <div class="date-display" style="margin-top:15px;">📅 {current_date}</div>
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
        
        submit = st.form_submit_button("🔑 Login", use_container_width=True, type="primary")
        
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
                    st.error(f"❌ School '{school_name}' not found!")
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

def forgot_password_form():
    st.markdown('<h3 style="color:#FFFFFF;">🔐 Reset Password</h3>', unsafe_allow_html=True)
    with st.form("frm_forgot_password"):
        email = st.text_input("📧 Registered Email")
        school_name = st.text_input("🏢 School Name")
        if st.form_submit_button("📤 Send Reset Token", use_container_width=True):
            if email and school_name:
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
                        st.info(f"🔑 Token: `{token[:16]}...`")
                    else:
                        st.error("❌ No user found!")
                finally:
                    conn.close()

def signup_form():
    st.markdown('<h3 style="color:#FFFFFF;">📝 Staff Sign Up</h3>', unsafe_allow_html=True)
    with st.form("frm_signup"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Full Name *")
            email = st.text_input("📧 Email *")
            phone = st.text_input("📞 Phone")
        with col2:
            school_name = st.text_input("🏢 School Name *")
            invite_code = st.text_input("🔑 Invite Code *")
            staff_id = st.text_input("👤 Staff ID (Optional)")
        
        password = st.text_input("🔒 Create Password *", type="password", placeholder="Min 6 characters")
        
        if st.form_submit_button("📝 Sign Up", use_container_width=True, type="primary"):
            if not name or not email or not school_name or not invite_code or not password:
                st.error("Please fill in all required fields (*)!")
                return
            
            if len(password) < 6:
                st.error("Password must be at least 6 characters!")
                return
            
            conn = get_db_connection()
            try:
                school = conn.execute(
                    "SELECT * FROM schools WHERE name = ? AND is_active = 1", 
                    (school_name,)
                ).fetchone()
                
                if not school:
                    st.error(f"❌ School '{school_name}' not found!")
                    return
                
                school_dict = dict(school)
                
                if school_dict.get('invite_code', '') != invite_code.upper():
                    st.error(f"❌ Invalid invite code!")
                    return
                
                existing = conn.execute(
                    "SELECT * FROM users WHERE email = ? AND school_name = ?",
                    (email, school_name)
                ).fetchone()
                
                if existing:
                    st.error("❌ Email already registered!")
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
            school_name = st.text_input("🏢 School Name *")
            address = st.text_input("📍 School Address")
            admin_name = st.text_input("👤 Admin Full Name *")
        with col2:
            admin_email = st.text_input("📧 Admin Email *")
            admin_phone = st.text_input("📞 Admin Phone")
        
        password = st.text_input("🔒 Password *", type="password", placeholder="Min 8 characters")
        confirm = st.text_input("🔒 Confirm Password *", type="password")
        
        if st.form_submit_button("🚀 Create School", use_container_width=True, type="primary"):
            if not school_name or not admin_name or not admin_email or not password:
                st.error("Please fill in all required fields (*)!")
                return
            if password != confirm:
                st.error("Passwords don't match!")
                return
            if len(password) < 8:
                st.error("Password must be at least 8 characters!")
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
                
                conn.execute(
                    """INSERT INTO academic_terms (school_name, name, start_date, end_date, is_current, created_by)
                    VALUES (?, 'Term 1', ?, ?, 1, ?)""",
                    (school_name, created_date, 
                     (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'), admin_name)
                )
                
                conn.execute(
                    "INSERT INTO system_settings (school_name, max_borrow_days, max_books_per_student) VALUES (?, ?, ?)",
                    (school_name, 14, 3)
                )
                conn.commit()
                
                school = conn.execute("SELECT * FROM schools WHERE name = ?", (school_name,)).fetchone()
                user = conn.execute("SELECT * FROM users WHERE email = ? AND school_name = ?", 
                                   (admin_email, school_name)).fetchone()
                
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
    current_date = get_current_date_display()
    
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;margin-bottom:25px;">
        <h1 style="font-size:2.2em;">🏫 {sanitize_html(school_name)}</h1>
        <p style="font-size:1.1em;color:#FFFFFF;">👤 {sanitize_html(user['name'])} 
        <span style="background:{'#e94560' if user['role']=='admin' else '#0f3460'};color:#FFF;padding:4px 12px;
        border-radius:20px;font-size:0.8em;margin-left:10px;">{sanitize_html(user['role'].upper())}</span></p>
        <p style="font-size:0.95em;color:#FFFFFF;">📅 {academic_year} | 📖 {term_name}</p>
        <div class="date-display">📅 {current_date}</div>
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
        <div style="text-align:center;padding:15px;background:rgba(0,0,0,0.5);border-radius:12px;margin-bottom:15px;border:1px solid rgba(255,255,255,0.2);">
            <div style="width:50px;height:50px;background:linear-gradient(135deg,#d4af37,#f0d060);border-radius:50%;
                 display:inline-flex;align-items:center;justify-content:center;font-size:22px;font-weight:700;color:#0a0e27;margin-bottom:8px;">
                {sanitize_html(user['name'][0].upper())}
            </div>
            <p style="color:#FFFFFF;font-weight:700;margin:3px 0;text-shadow:1px 1px 3px rgba(0,0,0,0.7);">{sanitize_html(user['name'])}</p>
            <p style="color:#d4af37;font-size:0.8em;margin:3px 0;text-shadow:1px 1px 3px rgba(0,0,0,0.7);">{sanitize_html(user['role'].upper())}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🎨 Theme", expanded=False):
            wallpaper = st.selectbox("Wallpaper:", list(WALLPAPERS.keys()), 
                                    index=list(WALLPAPERS.keys()).index(st.session_state.wallpaper) if st.session_state.wallpaper in WALLPAPERS else 0)
            if wallpaper != st.session_state.wallpaper:
                st.session_state.wallpaper = wallpaper
                st.rerun()
        
        st.markdown("---")
        
        with st.expander("📊 MAIN", expanded=True):
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.current_section = 'dashboard'
                st.rerun()
        
        with st.expander("📖 LIBRARY", expanded=False):
            if st.button("📖 Book Issuing", use_container_width=True):
                st.session_state.current_section = 'bookIssuing'
                st.rerun()
            if st.button("👤 Individual Lending", use_container_width=True):
                st.session_state.current_section = 'individualLending'
                st.rerun()
            if st.button("↩️ Returns", use_container_width=True):
                st.session_state.current_section = 'return'
                st.rerun()
            if st.button("📋 Borrowed Records", use_container_width=True):
                st.session_state.current_section = 'borrowedLog'
                st.rerun()
            if st.button("📚 Catalog", use_container_width=True):
                st.session_state.current_section = 'bookCatalog'
                st.rerun()
        
        with st.expander("🪑 RESOURCES", expanded=False):
            if st.button("🪑 Furniture Allocation", use_container_width=True):
                st.session_state.current_section = 'furnitureAllocation'
                st.rerun()
            if st.button("📊 Furniture Records", use_container_width=True):
                st.session_state.current_section = 'furnitureRecords'
                st.rerun()
            if st.button("📱 QR Codes", use_container_width=True):
                st.session_state.current_section = 'qr'
                st.rerun()
        
        with st.expander("👥 PEOPLE", expanded=False):
            if st.button("👥 Students Database", use_container_width=True):
                st.session_state.current_section = 'studentsDatabase'
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
            if st.button("🔍 System Overview", use_container_width=True):
                st.session_state.current_section = 'systemOverview'
                st.rerun()
            if st.button("📝 Audit Log", use_container_width=True):
                st.session_state.current_section = 'auditLog'
                st.rerun()
            if st.button("📈 Reports", use_container_width=True):
                st.session_state.current_section = 'reports'
                st.rerun()
            if st.button("📅 Events", use_container_width=True):
                st.session_state.current_section = 'events'
                st.rerun()
            if st.button("💰 Fees", use_container_width=True):
                st.session_state.current_section = 'fees'
                st.rerun()
            if st.button("📅 Timetable", use_container_width=True):
                st.session_state.current_section = 'timetable'
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
        
        st.markdown('<p style="color:rgba(255,255,255,0.5);font-size:0.7em;text-align:center;">SRMS v9.0 | WeGEM | © 2025</p>', unsafe_allow_html=True)
    
    # MAIN CONTENT
    section = st.session_state.get('current_section', 'dashboard')
    
    section_routes = {
        'dashboard': render_dashboard,
        'bookIssuing': render_book_issuing,
        'individualLending': render_individual_lending,
        'furnitureAllocation': render_furniture_allocation,
        'furnitureRecords': render_furniture_records,
        'return': render_returns,
        'borrowedLog': render_borrowed_records,
        'studentsDatabase': render_students_database,
        'bookCatalog': render_catalog,
        'teacherAllocation': render_teachers,
        'classListManager': render_classes,
        'academicTerms': render_academic_terms,
        'qr': render_qr,
        'chat': render_chat,
        'forum': render_forum,
        'notepad': render_notepad,
        'systemOverview': render_system_overview,
        'auditLog': render_audit_log,
        'reports': render_reports,
        'settings': render_settings,
        'databaseManager': render_database_manager,
        'events': render_events,
        'fees': render_fees,
        'timetable': render_timetable,
    }
    
    if section in section_routes:
        section_routes[section]()

# ============ RENDER FUNCTIONS (Core ones - rest follow same pattern) ============

def render_dashboard():
    school_name = st.session_state.school['name']
    academic_year = get_academic_year()
    current_term = get_current_term(school_name)
    term_name = current_term.get('name', 'Current Term')
    
    books = load_school_data('books', [])
    borrowed = load_school_data('borrowed', [])
    furniture = load_school_data('furniture', [])
    students = load_school_data('students', [])
    classes = load_school_data('classes', [])
    
    total_books = sum(b.get('quantity', 0) for b in books)
    available_books = sum(b.get('available', 0) for b in books)
    active_borrowed = len([b for b in borrowed if not b.get('returned')])
    active_furniture = len([f for f in furniture if not f.get('returned')])
    overdue_books = len([b for b in borrowed if not b.get('returned') and b.get('return_date', '') < datetime.now().strftime('%Y-%m-%d')])
    
    st.markdown(f'<div class="glass-card"><h2>📊 Dashboard - {term_name} ({academic_year})</h2>', unsafe_allow_html=True)
    
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
        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(students)}</div><div class="stat-label">Students</div></div>', unsafe_allow_html=True)
    
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
        if st.button("👥 View Students", use_container_width=True):
            st.session_state.current_section = 'studentsDatabase'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Allocations by Class
    st.markdown('<div class="glass-card"><h3>📋 Allocations by Class</h3>', unsafe_allow_html=True)
    
    if classes:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            class_options = ["All Classes"] + [f"{c['name']} {c.get('stream', '')}" for c in classes]
            selected_class = st.selectbox("Class:", class_options, key="dash_class")
        with col_f2:
            view_type = st.radio("View:", ["📖 Books", "🪑 Furniture", "Both"], horizontal=True, key="dash_view")
        with col_f3:
            date_filter = st.selectbox("Period:", ["All Time", "Today", "This Week", "This Month", "This Term"], key="dash_date")
        
        now = datetime.now()
        date_filters = {
            "Today": now.strftime('%Y-%m-%d'),
            "This Week": (now - timedelta(days=now.weekday())).strftime('%Y-%m-%d'),
            "This Month": now.replace(day=1).strftime('%Y-%m-%d'),
            "This Term": current_term.get('start_date', '2000-01-01'),
            "All Time": "2000-01-01"
        }
        date_limit = date_filters.get(date_filter, "2000-01-01")
        
        for cls in classes:
            class_display = f"{cls['name']} {cls.get('stream', '')}"
            if selected_class != "All Classes" and class_display != selected_class:
                continue
            
            students_list = cls.get('students', [])
            student_names = [s.get('name', s.get('Name', '')) for s in students_list]
            student_adms = [str(s.get('adm', s.get('ADM', ''))) for s in students_list]
            
            class_books = []
            class_furniture = []
            
            if view_type in ["📖 Books", "Both"]:
                for b in borrowed:
                    if ((b.get('student_name') in student_names or str(b.get('adm')) in student_adms or b.get('form') == cls['name']) 
                        and b.get('borrow_date', '') >= date_limit and not b.get('returned')):
                        class_books.append(b)
            
            if view_type in ["🪑 Furniture", "Both"]:
                for f in furniture:
                    if ((f.get('student_name') in student_names or str(f.get('adm')) in student_adms or f.get('form') == cls['name'])
                        and f.get('allocation_date', '') >= date_limit and not f.get('returned')):
                        class_furniture.append(f)
            
            with st.expander(f"📋 {class_display} - 📖{len(class_books)} 🪑{len(class_furniture)} 👨‍🎓{len(students_list)}"):
                tab1, tab2 = st.tabs(["📖 Books", "🪑 Furniture"])
                with tab1:
                    if class_books:
                        st.dataframe(pd.DataFrame(class_books), use_container_width=True)
                    else:
                        st.info("No active book loans")
                with tab2:
                    if class_furniture:
                        st.dataframe(pd.DataFrame(class_furniture), use_container_width=True)
                    else:
                        st.info("No active furniture allocations")
    else:
        st.info("No classes found.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if overdue_books > 0:
        st.markdown(f'<div class="glass-card" style="border-left: 4px solid #ff4444;"><h3>⚠️ Overdue Books ({overdue_books})</h3>', unsafe_allow_html=True)
        overdue_list = [b for b in borrowed if not b.get('returned') and b.get('return_date', '') < datetime.now().strftime('%Y-%m-%d')]
        if overdue_list:
            st.dataframe(pd.DataFrame(overdue_list).head(10), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_catalog():
    """Fixed book catalog"""
    school_name = st.session_state.school['name']
    books = load_school_data('books', [])
    
    st.markdown('<div class="glass-card"><h2>📚 Book Catalog</h2>', unsafe_allow_html=True)
    
    with st.form("frm_book"):
        col1, col2, col3 = st.columns(3)
        with col1:
            title = st.text_input("Title:")
        with col2:
            btype = st.selectbox("Type:", ["Textbook", "Novel", "Reference", "Magazine", "Other"])
        with col3:
            qty = st.number_input("Quantity:", 1, 1000, 1)
        
        col4, col5 = st.columns(2)
        with col4:
            author = st.text_input("Author:")
        with col5:
            subject = st.text_input("Subject:")
        
        if st.form_submit_button("📖 Add Book", use_container_width=True):
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
                        # FIXED: Match exact column count (11 columns)
                        conn.execute(
                            """INSERT INTO books (school_name, title, author, isbn, type, subject, quantity, available, location, created_by, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (school_name, title, author, '', btype, subject, qty, qty, '', 
                             st.session_state.user['name'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        )
                    conn.commit()
                    add_audit_entry('Book Added', title)
                    st.success("✅ Added!")
                    st.rerun()
                finally:
                    conn.close()
    
    if books:
        search = st.text_input("🔍 Search:", placeholder="Filter by title, author, subject")
        filtered = books
        if search:
            q = search.lower()
            filtered = [b for b in books if q in b.get('title', '').lower() or q in b.get('author', '').lower() or q in b.get('subject', '').lower()]
        
        for book in filtered:
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            with col1:
                st.write(f"📖 **{sanitize_html(book['title'])}**")
                if book.get('author'):
                    st.caption(f"by {book['author']}")
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
        st.info("No books in catalog")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_students_database():
    """Student database"""
    school_name = st.session_state.school['name']
    students = load_school_data('students', [])
    
    st.markdown('<div class="glass-card"><h2>👥 Students Database</h2>', unsafe_allow_html=True)
    
    with st.expander("📥 Import Students", expanded=False):
        uploaded = st.file_uploader("Upload Excel", type=['xlsx', 'xls'])
        if uploaded:
            try:
                df = pd.read_excel(uploaded)
                st.dataframe(df.head(), use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    form = st.text_input("Form/Class:")
                with col2:
                    stream = st.text_input("Stream:")
                
                if st.button("💾 Import", use_container_width=True):
                    conn = get_db_connection()
                    try:
                        count = 0
                        for _, row in df.iterrows():
                            adm = str(row.get('ADM', row.get('adm', generate_code('ADM'))))
                            name = str(row.get('Name', row.get('name', '')))
                            gender = str(row.get('Gender', row.get('gender', '')))
                            conn.execute(
                                """INSERT OR REPLACE INTO students (adm, school_name, name, form, stream, gender, added_by, added_at, is_active)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)""",
                                (adm, school_name, name, form, stream, gender, 
                                 st.session_state.user['name'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            )
                            count += 1
                        conn.commit()
                        add_audit_entry('Students Imported', f"{count} students")
                        st.success(f"✅ Imported {count} students!")
                        st.rerun()
                    finally:
                        conn.close()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with st.expander("➕ Add Student", expanded=False):
        with st.form("frm_student"):
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input("Full Name:")
                adm = st.text_input("ADM No:")
                gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
            with col2:
                form = st.text_input("Form/Class:")
                stream = st.text_input("Stream:")
                dob = st.date_input("Date of Birth:", value=None)
            with col3:
                parent_name = st.text_input("Parent/Guardian:")
                parent_phone = st.text_input("Parent Phone:")
                parent_email = st.text_input("Parent Email:")
            
            if st.form_submit_button("➕ Add", use_container_width=True):
                if name and adm:
                    conn = get_db_connection()
                    try:
                        conn.execute(
                            """INSERT OR REPLACE INTO students (adm, school_name, name, form, stream, gender, dob, 
                            parent_name, parent_phone, parent_email, added_by, added_at, is_active)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""",
                            (adm, school_name, name, form, stream, gender, 
                             dob.strftime('%Y-%m-%d') if dob else '',
                             parent_name, parent_phone, parent_email,
                             st.session_state.user['name'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        )
                        conn.commit()
                        st.success("✅ Added!")
                        st.rerun()
                    finally:
                        conn.close()
    
    if students:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filter_form = st.selectbox("Form:", ["All"] + list(set(s.get('form', '') for s in students if s.get('form'))), key="stu_form")
        with col_f2:
            filter_stream = st.selectbox("Stream:", ["All"] + list(set(s.get('stream', '') for s in students if s.get('stream'))), key="stu_stream")
        with col_f3:
            search_student = st.text_input("🔍 Search:", placeholder="Name or ADM")
        
        filtered = students
        if filter_form != "All":
            filtered = [s for s in filtered if s.get('form') == filter_form]
        if filter_stream != "All":
            filtered = [s for s in filtered if s.get('stream') == filter_stream]
        if search_student:
            q = search_student.lower()
            filtered = [s for s in filtered if q in s.get('name', '').lower() or q in s.get('adm', '').lower()]
        
        st.dataframe(pd.DataFrame(filtered), use_container_width=True)
        
        if st.button("📥 Export", use_container_width=True):
            df = pd.DataFrame(filtered)
            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="students.xlsx">📥 Download</a>', unsafe_allow_html=True)
    else:
        st.info("No students")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_returns():
    """Return items"""
    school_name = st.session_state.school['name']
    classes = load_school_data('classes', [])
    user_email = st.session_state.user['email']
    
    st.markdown('<div class="glass-card"><h2>↩️ Return Items</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📚 Books", "🪑 Furniture"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            search_book = st.text_input("🔍 Search:", placeholder="Name, ADM, book", key="ret_book_search")
        with col2:
            filter_class = st.selectbox("Class:", ["All"] + [c['name'] for c in classes], key="ret_book_class")
        
        if st.button("🔍 Search Books", use_container_width=True, key="ret_book_btn"):
            conn = get_db_connection()
            try:
                if is_admin():
                    query = """SELECT * FROM borrowed WHERE school_name = ? AND returned = 0 
                              AND (LOWER(student_name) LIKE ? OR adm LIKE ? OR book_no LIKE ?)"""
                    params = [school_name, f"%{search_book.lower()}%", f"%{search_book}%", f"%{search_book}%"]
                else:
                    query = """SELECT * FROM borrowed WHERE school_name = ? AND returned = 0 
                              AND issued_by_email = ?
                              AND (LOWER(student_name) LIKE ? OR adm LIKE ? OR book_no LIKE ?)"""
                    params = [school_name, user_email, f"%{search_book.lower()}%", f"%{search_book}%", f"%{search_book}%"]
                
                if filter_class != "All":
                    query += " AND form = ?"
                    params.append(filter_class)
                
                active_books = conn.execute(query, params).fetchall()
            finally:
                conn.close()
            
            if active_books:
                for item in active_books:
                    item_dict = dict(item)
                    is_overdue = item_dict.get('return_date', '') < datetime.now().strftime('%Y-%m-%d')
                    badge = '<span class="overdue-badge">⚠️ OVERDUE</span>' if is_overdue else '<span class="active-badge">Active</span>'
                    
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"**{sanitize_html(item_dict['student_name'])}** - {sanitize_html(item_dict['book_title'])} (#{item_dict['book_no']}) {badge}")
                        st.caption(f"Class: {item_dict.get('form', '')} | Due: {item_dict.get('return_date', '')}")
                    with col2:
                        if st.button("↩️ Return", key=f"ret_book_{item_dict['id']}"):
                            conn = get_db_connection()
                            try:
                                conn.execute(
                                    "UPDATE borrowed SET returned = 1, actual_return_date = ?, status = 'returned' WHERE id = ?",
                                    (datetime.now().strftime('%Y-%m-%d'), item_dict['id'])
                                )
                                conn.execute(
                                    "UPDATE books SET available = available + 1 WHERE school_name = ? AND title = ?",
                                    (school_name, item_dict['book_title'])
                                )
                                conn.commit()
                                add_audit_entry('Book Returned', f"{item_dict['student_name']} - {item_dict['book_title']}")
                                st.success("✅ Returned!")
                                st.rerun()
                            finally:
                                conn.close()
                    st.divider()
            else:
                st.info("No matching active book loans")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            search_furn = st.text_input("🔍 Search:", placeholder="Name, ADM, chair, locker", key="ret_furn_search")
        with col2:
            filter_class_f = st.selectbox("Class:", ["All"] + [c['name'] for c in classes], key="ret_furn_class")
        
        if st.button("🔍 Search Furniture", use_container_width=True, key="ret_furn_btn"):
            conn = get_db_connection()
            try:
                if is_admin():
                    query = """SELECT * FROM furniture WHERE school_name = ? AND returned = 0 
                              AND (LOWER(student_name) LIKE ? OR adm LIKE ? OR chair_no LIKE ? OR locker_no LIKE ?)"""
                    params = [school_name, f"%{search_furn.lower()}%", f"%{search_furn}%", f"%{search_furn}%", f"%{search_furn}%"]
                else:
                    query = """SELECT * FROM furniture WHERE school_name = ? AND returned = 0 
                              AND issued_by_email = ?
                              AND (LOWER(student_name) LIKE ? OR adm LIKE ? OR chair_no LIKE ? OR locker_no LIKE ?)"""
                    params = [school_name, user_email, f"%{search_furn.lower()}%", f"%{search_furn}%", f"%{search_furn}%", f"%{search_furn}%"]
                
                if filter_class_f != "All":
                    query += " AND form LIKE ?"
                    params.append(f"%{filter_class_f}%")
                
                active_furniture = conn.execute(query, params).fetchall()
            finally:
                conn.close()
            
            if active_furniture:
                for item in active_furniture:
                    item_dict = dict(item)
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"**{sanitize_html(item_dict['student_name'])}** - Chair: {item_dict.get('chair_no', '')} | Locker: {item_dict.get('locker_no', '')}")
                        st.caption(f"Class: {item_dict.get('form', '')} | Date: {item_dict.get('allocation_date', '')}")
                    with col2:
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
                st.info("No matching active furniture")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_borrowed_records():
    """Borrowed records with return button"""
    school_name = st.session_state.school['name']
    borrowed = load_school_data('borrowed', [])
    classes = load_school_data('classes', [])
    
    st.markdown('<div class="glass-card"><h2>📋 Borrowed Records</h2>', unsafe_allow_html=True)
    
    if not is_admin():
        st.info("📝 Showing records you issued. Admin can see all records.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_class = st.selectbox("Class:", ["All"] + [c['name'] for c in classes])
    with col2:
        filter_status = st.selectbox("Status:", ["All", "Active", "Returned", "Overdue"])
    with col3:
        search = st.text_input("🔍 Search:", placeholder="Name, ADM, book")
    
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
        q = search.lower()
        filtered = [b for b in filtered if q in b.get('student_name', '').lower() or q in b.get('adm', '').lower() or q in b.get('book_title', '').lower()]
    
    if filtered:
        for item in filtered:
            item_dict = dict(item)
            is_overdue = not item_dict.get('returned') and item_dict.get('return_date', '') < now.strftime('%Y-%m-%d')
            
            if item_dict.get('returned'):
                badge = '<span class="returned-badge">✅ Returned</span>'
            elif is_overdue:
                badge = '<span class="overdue-badge">⚠️ Overdue</span>'
            else:
                badge = '<span class="active-badge">📖 Active</span>'
            
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                **{sanitize_html(item_dict.get('student_name', ''))}** - {sanitize_html(item_dict.get('book_title', ''))} (#{item_dict.get('book_no', '')}) {badge}
                <br><small>Class: {item_dict.get('form', '')} | Borrowed: {item_dict.get('borrow_date', '')} | Due: {item_dict.get('return_date', '')} | Issued by: {item_dict.get('issued_by', '')}</small>
                """, unsafe_allow_html=True)
            with col2:
                if not item_dict.get('returned'):
                    if st.button("↩️ Return", key=f"bor_rec_ret_{item_dict['id']}"):
                        conn = get_db_connection()
                        try:
                            conn.execute(
                                "UPDATE borrowed SET returned = 1, actual_return_date = ?, status = 'returned' WHERE id = ?",
                                (datetime.now().strftime('%Y-%m-%d'), item_dict['id'])
                            )
                            conn.execute(
                                "UPDATE books SET available = available + 1 WHERE school_name = ? AND title = ?",
                                (school_name, item_dict['book_title'])
                            )
                            conn.commit()
                            add_audit_entry('Book Returned from Records', f"{item_dict['student_name']} - {item_dict['book_title']}")
                            st.success("✅ Returned!")
                            st.rerun()
                        finally:
                            conn.close()
            st.divider()
        
        if st.button("📥 Export", use_container_width=True):
            df = pd.DataFrame(filtered)
            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            b64 = base64.b64encode(towrite.read()).decode()
            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="borrowed.xlsx">📥 Download</a>', unsafe_allow_html=True)
    else:
        st.info("No records found")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Simplified render functions for remaining features
def render_book_issuing():
    school_name = st.session_state.school['name']
    books = load_school_data('books', [])
    classes = load_school_data('classes', [])
    academic_year = get_academic_year()
    current_term = get_current_term(school_name)
    user = st.session_state.user
    
    st.markdown('<div class="glass-card"><h2>📖 Book Issuing</h2>', unsafe_allow_html=True)
    
    if not books:
        st.warning("No books in catalog.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        class_options = [f"{c['name']} {c.get('stream', '')}" for c in classes] if classes else ["No classes"]
        selected_class_str = st.selectbox("Class:", class_options)
    with col2:
        book_options = [b['title'] for b in books if b.get('available', b.get('quantity', 0)) > 0]
        selected_book = st.selectbox("Book:", book_options if book_options else ["No books"])
    with col3:
        issue_date = st.date_input("Issue Date:", datetime.now())
    
    col4, col5 = st.columns(2)
    with col4:
        return_date = st.date_input("Return Date:", datetime.now() + timedelta(days=14))
    with col5:
        term_name = st.text_input("Term:", value=current_term.get('name', 'Term 1'))
    
    if classes and selected_class_str != "No classes":
        selected_class = next((c for c in classes if f"{c['name']} {c.get('stream', '')}" == selected_class_str), None)
        if selected_class and selected_class.get('students'):
            students_list = selected_class['students']
            st.markdown(f"### Students ({len(students_list)})")
            
            student_data = []
            for s in students_list:
                student_data.append({
                    'Name': s.get('name', s.get('Name', '')),
                    'ADM': str(s.get('adm', s.get('ADM', ''))),
                    'Book No': '',
                    'Issue': False
                })
            
            df = pd.DataFrame(student_data)
            edited_df = st.data_editor(df, use_container_width=True, hide_index=True,
                column_config={
                    "Name": st.column_config.TextColumn("Name", disabled=True),
                    "ADM": st.column_config.TextColumn("ADM", disabled=True),
                    "Book No": st.column_config.TextColumn("Book No"),
                    "Issue": st.column_config.CheckboxColumn("Issue")
                }, key="book_issue_editor")
            
            if st.button("✅ Issue Books", use_container_width=True, type="primary"):
                issued = 0
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
                                book_title, book_no, borrow_date, return_date, returned, issued_by, issued_by_email, academic_year, term)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?)""",
                                (generate_code("BOR"), school_name, str(row['Name']), adm,
                                 selected_class['name'], selected_class.get('stream', ''),
                                 selected_book, book_no,
                                 issue_date.strftime('%Y-%m-%d'), return_date.strftime('%Y-%m-%d'),
                                 user['name'], user['email'], academic_year, term_name)
                            )
                            
                            conn.execute(
                                "UPDATE books SET available = available - 1 WHERE school_name = ? AND title = ? AND available > 0",
                                (school_name, selected_book)
                            )
                            issued += 1
                    
                    conn.commit()
                    if issued > 0:
                        add_audit_entry('Books Issued', f"{issued} copies")
                        st.success(f"✅ Issued {issued} books!")
                        st.rerun()
                finally:
                    conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_individual_lending():
    school_name = st.session_state.school['name']
    books = load_school_data('books', [])
    classes = load_school_data('classes', [])
    academic_year = get_academic_year()
    current_term = get_current_term(school_name)
    user = st.session_state.user
    
    st.markdown('<div class="glass-card"><h2>👤 Individual Lending</h2>', unsafe_allow_html=True)
    
    with st.form("frm_ind_lend"):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Student Name:")
            adm = st.text_input("ADM No:")
        with col2:
            form = st.selectbox("Form:", [""] + [c['name'] for c in classes])
            stream = st.text_input("Stream:")
        with col3:
            book_options = [b['title'] for b in books if b.get('available', b.get('quantity', 0)) > 0]
            selected_book = st.selectbox("Book:", book_options if book_options else ["No books"])
            book_no = st.text_input("Book No:")
        
        col4, col5 = st.columns(2)
        with col4:
            borrow_date = st.date_input("Borrow Date:", datetime.now())
            return_date = st.date_input("Return Date:", datetime.now() + timedelta(days=14))
        with col5:
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
                            book_title, book_no, borrow_date, return_date, returned, issued_by, issued_by_email, academic_year, term)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?)""",
                            (generate_code("BOR"), school_name, name, adm, form, stream,
                             selected_book, book_no,
                             borrow_date.strftime('%Y-%m-%d'), return_date.strftime('%Y-%m-%d'),
                             user['name'], user['email'], academic_year, term_name)
                        )
                        conn.execute(
                            "UPDATE books SET available = available - 1 WHERE school_name = ? AND title = ? AND available > 0",
                            (school_name, selected_book)
                        )
                        conn.commit()
                        add_audit_entry('Lend Book', f"{name} borrowed '{selected_book}'")
                        st.success("✅ Book lent!")
                        st.rerun()
                    finally:
                        conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_furniture_allocation():
    school_name = st.session_state.school['name']
    classes = load_school_data('classes', [])
    academic_year = get_academic_year()
    current_term = get_current_term(school_name)
    user = st.session_state.user
    
    st.markdown('<div class="glass-card"><h2>🪑 Furniture Allocation</h2>', unsafe_allow_html=True)
    
    if not classes:
        st.warning("No classes available.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    class_options = [f"{c['name']} {c.get('stream', '')}" for c in classes]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_class_str = st.selectbox("Class:", class_options)
    with col2:
        allocation_date = st.date_input("Date:", datetime.now())
    with col3:
        term_name = st.text_input("Term:", value=current_term.get('name', 'Term 1'))
    
    col4, col5 = st.columns(2)
    with col4:
        chair_prefix = st.text_input("Chair Prefix:", "CH-")
        chair_start = st.number_input("Chair Start:", 1, 10000, 1)
    with col5:
        locker_prefix = st.text_input("Locker Prefix:", "LK-")
        locker_start = st.number_input("Locker Start:", 1, 10000, 1)
    
    selected_class = next((c for c in classes if f"{c['name']} {c.get('stream', '')}" == selected_class_str), None)
    if selected_class and selected_class.get('students'):
        students_list = selected_class['students']
        st.markdown(f"### Students ({len(students_list)})")
        
        student_data = []
        for i, s in enumerate(students_list):
            student_data.append({
                'Name': s.get('name', s.get('Name', '')),
                'ADM': str(s.get('adm', s.get('ADM', ''))),
                'Chair No': f"{chair_prefix}{chair_start + i}",
                'Locker No': f"{locker_prefix}{locker_start + i}",
                'Allocate': True
            })
        
        df = pd.DataFrame(student_data)
        edited_df = st.data_editor(df, use_container_width=True, hide_index=True,
            column_config={
                "Name": st.column_config.TextColumn("Name", disabled=True),
                "ADM": st.column_config.TextColumn("ADM", disabled=True),
                "Chair No": st.column_config.TextColumn("Chair No"),
                "Locker No": st.column_config.TextColumn("Locker No"),
                "Allocate": st.column_config.CheckboxColumn("Allocate")
            }, key="furniture_editor")
        
        if st.button("✅ Allocate", use_container_width=True, type="primary"):
            allocated = 0
            conn = get_db_connection()
            try:
                for _, row in edited_df.iterrows():
                    if row['Allocate']:
                        adm = str(row['ADM'])
                        chair_no = str(row['Chair No'])
                        
                        if chair_no and check_duplicate_assignment(school_name, adm, 'chair', chair_no):
                            st.warning(f"⚠️ {row['Name']} already has chair {chair_no}!")
                            continue
                        
                        conn.execute(
                            """INSERT INTO furniture (id, school_name, student_name, adm, form, stream,
                            chair_no, locker_no, allocation_date, returned, issued_by, issued_by_email, academic_year, term)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?)""",
                            (generate_code("FUR"), school_name, str(row['Name']), adm,
                             selected_class['name'], selected_class.get('stream', ''),
                             chair_no, str(row['Locker No']),
                             allocation_date.strftime('%Y-%m-%d'),
                             user['name'], user['email'], academic_year, term_name)
                        )
                        allocated += 1
                
                conn.commit()
                if allocated > 0:
                    add_audit_entry('Furniture Allocated', f"{allocated} items")
                    st.success(f"✅ Allocated {allocated} items!")
                    st.rerun()
            finally:
                conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_furniture_records():
    school_name = st.session_state.school['name']
    furniture = load_school_data('furniture', [])
    classes = load_school_data('classes', [])
    
    st.markdown('<div class="glass-card"><h2>📊 Furniture Records</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_class = st.selectbox("Class:", ["All"] + [c['name'] for c in classes])
    with col2:
        filter_status = st.selectbox("Status:", ["All", "Active", "Returned"])
    with col3:
        filter_date = st.selectbox("Date:", ["All", "Today", "This Week", "This Month"])
    
    filtered = furniture
    now = datetime.now()
    
    if filter_class != "All":
        filtered = [f for f in filtered if f.get('form', '').startswith(filter_class)]
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
    
    if filtered:
        st.dataframe(pd.DataFrame(filtered), use_container_width=True)
        st.metric("Records", len(filtered))
    else:
        st.info("No records")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_teachers():
    school_name = st.session_state.school['name']
    teachers = load_school_data('teachers', [])
    
    st.markdown('<div class="glass-card"><h2>👨‍🏫 Teachers</h2>', unsafe_allow_html=True)
    
    with st.form("frm_teacher"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name:")
            email = st.text_input("Email:")
        with col2:
            subjects = st.text_input("Subjects:")
            classes = st.text_input("Classes:")
        
        if st.form_submit_button("➕ Add", use_container_width=True):
            if name:
                conn = get_db_connection()
                try:
                    conn.execute(
                        """INSERT INTO teachers (id, school_name, name, email, subjects, classes, added_by, is_active)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 1)""",
                        (generate_code("TCH"), school_name, name, email, subjects, classes, 
                         st.session_state.user['name'])
                    )
                    conn.commit()
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
    school_name = st.session_state.school['name']
    classes = load_school_data('classes', [])
    
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
                            (school_name, class_name, stream, json.dumps(students), 
                             st.session_state.user['name'], datetime.now().strftime("%Y-%m-%d"), get_academic_year())
                        )
                        conn.commit()
                        st.success("✅ Saved!")
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
    else:
        st.info("No classes")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_academic_terms():
    school_name = st.session_state.school['name']
    terms = load_school_data('academic_terms', [])
    
    st.markdown('<div class="glass-card"><h2>📅 Academic Terms</h2>', unsafe_allow_html=True)
    
    with st.form("frm_term"):
        col1, col2, col3 = st.columns(3)
        with col1:
            term_name = st.text_input("Term Name:")
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
                    st.success("✅ Added!")
                    st.rerun()
                finally:
                    conn.close()
    
    if terms:
        for term in terms:
            is_current = term.get('is_current')
            st.markdown(f"""
            <div style="padding:10px;margin:5px 0;border-left:4px solid {'#28a745' if is_current else '#666'};background:rgba(0,0,0,0.3);border-radius:8px;">
                <strong>{sanitize_html(term['name'])}</strong> {'✅ Current' if is_current else ''}<br>
                {term.get('start_date', '')} → {term.get('end_date', '')}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_qr():
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
    school_name = st.session_state.school['name']
    user = st.session_state.user
    
    st.markdown('<div class="glass-card"><h2>📢 Group Forum</h2>', unsafe_allow_html=True)
    
    forum = load_school_data('forum_messages', [])
    
    for msg in forum[-20:]:
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.3);padding:10px;border-radius:8px;margin:5px 0;">
            <strong>{sanitize_html(msg['from_name'])}</strong> <small>({msg['timestamp'][:16]})</small><br>
            {sanitize_html(msg['message'])}
        </div>
        """, unsafe_allow_html=True)
    
    with st.form("frm_forum"):
        msg = st.text_area("Message:", height=100)
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
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_system_overview():
    school_name = st.session_state.school['name']
    books = load_school_data('books', [])
    borrowed = load_school_data('borrowed', [])
    furniture = load_school_data('furniture', [])
    students = load_school_data('students', [])
    classes = load_school_data('classes', [])
    
    st.markdown('<div class="glass-card"><h2>🔍 System Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Books", sum(b.get('quantity', 0) for b in books))
    with col2:
        st.metric("📖 Active Loans", len([b for b in borrowed if not b.get('returned')]))
    with col3:
        st.metric("🪑 Furniture", len([f for f in furniture if not f.get('returned')]))
    with col4:
        st.metric("👥 Students", len(students))
    
    if classes:
        class_data = []
        for cls in classes:
            class_name = cls['name']
            class_books = len([b for b in borrowed if b.get('form') == class_name and not b.get('returned')])
            class_furniture = len([f for f in furniture if f.get('form', '').startswith(class_name) and not f.get('returned')])
            class_data.append({'Class': class_name, 'Books': class_books, 'Furniture': class_furniture})
        
        if class_data:
            df = pd.DataFrame(class_data)
            fig = px.bar(df, x='Class', y=['Books', 'Furniture'], barmode='group',
                        color_discrete_sequence=['#e94560', '#28a745'], title="Allocations by Class")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_audit_log():
    st.markdown('<div class="glass-card"><h2>📝 Audit Log</h2>', unsafe_allow_html=True)
    
    audit = load_school_data('audit_log', [])
    
    if not is_admin():
        st.info("Showing your activity log.")
    
    if audit:
        st.dataframe(pd.DataFrame(audit), use_container_width=True)
    else:
        st.info("No entries")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_reports():
    st.markdown('<div class="glass-card"><h2>📈 Reports</h2>', unsafe_allow_html=True)
    
    report_type = st.selectbox("Type:", ["Books Overview", "Overdue Items"])
    
    if st.button("Generate", use_container_width=True):
        school_name = st.session_state.school['name']
        
        if report_type == "Overdue Items":
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

def render_events():
    school_name = st.session_state.school['name']
    events = load_school_data('events', [])
    
    st.markdown('<div class="glass-card"><h2>📅 Events</h2>', unsafe_allow_html=True)
    
    with st.form("frm_event"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title:")
            event_date = st.date_input("Date:", datetime.now())
        with col2:
            event_type = st.selectbox("Type:", ["Academic", "Sports", "Cultural", "Meeting", "Holiday", "Other"])
            description = st.text_area("Description:")
        
        if st.form_submit_button("➕ Add", use_container_width=True):
            if title:
                conn = get_db_connection()
                try:
                    conn.execute(
                        """INSERT INTO events (school_name, title, description, event_date, event_type, created_by, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (school_name, title, description, event_date.strftime('%Y-%m-%d'), event_type,
                         st.session_state.user['name'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    )
                    conn.commit()
                    st.success("✅ Added!")
                    st.rerun()
                finally:
                    conn.close()
    
    if events:
        for event in sorted(events, key=lambda x: x.get('event_date', '')):
            st.markdown(f"""
            <div style="padding:10px;margin:5px 0;border-left:4px solid #e94560;background:rgba(0,0,0,0.3);border-radius:8px;">
                <strong>{sanitize_html(event.get('title', ''))}</strong> ({event.get('event_type', '')})<br>
                📅 {event.get('event_date', '')} - {sanitize_html(event.get('description', ''))}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No events")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_fees():
    school_name = st.session_state.school['name']
    fees = load_school_data('fees', [])
    students = load_school_data('students', [])
    current_term = get_current_term(school_name)
    
    st.markdown('<div class="glass-card"><h2>💰 Fee Records</h2>', unsafe_allow_html=True)
    
    with st.form("frm_fee"):
        col1, col2, col3 = st.columns(3)
        with col1:
            student_select = st.selectbox("Student:", ["Select"] + [f"{s['name']} ({s['adm']})" for s in students])
            amount = st.number_input("Total Fee:", 0.0, 1000000.0, 0.0)
        with col2:
            paid = st.number_input("Paid:", 0.0, 1000000.0, 0.0)
            payment_date = st.date_input("Payment Date:", datetime.now())
        with col3:
            term = st.text_input("Term:", value=current_term.get('name', 'Term 1'))
        
        if st.form_submit_button("💾 Save", use_container_width=True):
            if student_select != "Select":
                student_name = student_select.split(" (")[0]
                student_adm = student_select.split("(")[1].replace(")", "")
                balance = amount - paid
                
                conn = get_db_connection()
                try:
                    conn.execute(
                        """INSERT OR REPLACE INTO fees (id, school_name, student_adm, student_name, form, amount, paid, balance, term, academic_year, last_payment_date, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (generate_code("FEE"), school_name, student_adm, student_name, '',
                         amount, paid, balance, term, get_academic_year(),
                         payment_date.strftime('%Y-%m-%d'), 'completed' if balance <= 0 else 'partial')
                    )
                    conn.commit()
                    st.success("✅ Saved!")
                    st.rerun()
                finally:
                    conn.close()
    
    if fees:
        st.dataframe(pd.DataFrame(fees), use_container_width=True)
        
        total_fees = sum(f.get('amount', 0) for f in fees)
        total_paid = sum(f.get('paid', 0) for f in fees)
        total_balance = sum(f.get('balance', 0) for f in fees)
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Fees", f"KES {total_fees:,.2f}")
        with col_m2:
            st.metric("Total Paid", f"KES {total_paid:,.2f}")
        with col_m3:
            st.metric("Outstanding", f"KES {total_balance:,.2f}")
    else:
        st.info("No fee records")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_timetable():
    school_name = st.session_state.school['name']
    timetable = load_school_data('timetable', [])
    classes = load_school_data('classes', [])
    teachers = load_school_data('teachers', [])
    
    st.markdown('<div class="glass-card"><h2>📅 Timetable</h2>', unsafe_allow_html=True)
    
    with st.form("frm_timetable"):
        col1, col2, col3 = st.columns(3)
        with col1:
            class_name = st.selectbox("Class:", [c['name'] for c in classes] if classes else ["Form 1"])
            day = st.selectbox("Day:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        with col2:
            period = st.selectbox("Period:", ["8:00-8:40", "8:40-9:20", "9:20-10:00", "10:20-11:00", 
                                              "11:00-11:40", "11:40-12:20", "14:00-14:40", "14:40-15:20"])
            subject = st.text_input("Subject:")
        with col3:
            teacher = st.selectbox("Teacher:", [t['name'] for t in teachers] if teachers else [])
            room = st.text_input("Room:")
        
        if st.form_submit_button("➕ Add", use_container_width=True):
            if subject:
                conn = get_db_connection()
                try:
                    conn.execute(
                        """INSERT INTO timetable (school_name, class_name, day, period, subject, teacher, room, created_by)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (school_name, class_name, day, period, subject, teacher, room, st.session_state.user['name'])
                    )
                    conn.commit()
                    st.success("✅ Added!")
                    st.rerun()
                finally:
                    conn.close()
    
    if timetable:
        st.dataframe(pd.DataFrame(timetable), use_container_width=True)
    else:
        st.info("No timetable entries")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_settings():
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
                st.write(f"{'👑' if u['role']=='admin' else '👨‍🏫'} **{sanitize_html(u['name'])}** ({u['role']})")
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
                tables = ['schools', 'users', 'books', 'borrowed', 'furniture', 'students', 'teachers', 'classes', 'audit_log']
                backup = {}
                for table in tables:
                    rows = conn.execute(f"SELECT * FROM {table} WHERE school_name = ?", (school_name,)).fetchall()
                    backup[table] = [dict(r) for r in rows]
                
                b64 = base64.b64encode(json.dumps(backup, indent=2, default=str).encode()).decode()
                st.markdown(f'<a href="data:application/json;base64,{b64}" download="backup_{school_name}.json">📥 Download</a>', unsafe_allow_html=True)
                st.success("✅ Ready!")
            finally:
                conn.close()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_database_manager():
    if not is_admin():
        st.error("🔒 Admin access required!")
        return
    
    school_name = st.session_state.school['name']
    
    st.markdown('<div class="glass-card"><h2>🗄️ Database Manager</h2>', unsafe_allow_html=True)
    st.warning("⚠️ Admin only!")
    
    tables = {
        "Schools": "schools", "Users": "users", "Books": "books",
        "Borrowed": "borrowed", "Furniture": "furniture", "Students": "students",
        "Teachers": "teachers", "Classes": "classes", "Terms": "academic_terms",
        "Audit Log": "audit_log", "Chat": "chat_messages", "Forum": "forum_messages",
        "Events": "events", "Fees": "fees", "Timetable": "timetable"
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
