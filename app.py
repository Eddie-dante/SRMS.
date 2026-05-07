<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>SRMS - School Resource Management System by WeGEM</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script src="https://unpkg.com/html5-qrcode@2.3.8/dist/html5-qrcode.min.js"></script>
    <script src="https://cdn.rawgit.com/davidshimjs/qrcodejs/gh-pages/qrcode.min.js"></script>
    <style>
        :root {
            --primary: #0a0e27;
            --accent: #e94560;
            --gold: #d4af37;
            --gold-light: #f0d060;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --info: #0f3460;
            --border-radius: 12px;
            --transition: all 0.3s ease;
            --glass-bg: rgba(255, 255, 255, 0.12);
            --glass-bg-input: rgba(255, 255, 255, 0.08);
            --text-color: rgba(255, 255, 255, 0.95);
            --text-secondary: rgba(255, 255, 255, 0.75);
            --text-muted: rgba(255, 255, 255, 0.55);
            --border-color: rgba(255, 255, 255, 0.15);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: var(--primary);
            min-height: 100vh;
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: var(--text-color);
            position: relative;
        }

        /* Dark overlay for readability */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 14, 39, 0.7);
            z-index: 0;
            pointer-events: none;
        }

        .overlay {
            position: relative;
            z-index: 1;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Startup Page */
        .startup-page {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }

        .startup-particles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }

        .startup-particle {
            position: absolute;
            background: rgba(212, 175, 55, 0.2);
            border-radius: 50%;
            animation: floatUp 15s infinite linear;
        }

        @keyframes floatUp {
            0% { transform: translateY(100vh) scale(0); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-10vh) scale(1.5); opacity: 0; }
        }

        .startup-logo-container {
            text-align: center;
            position: relative;
            z-index: 10;
            background: rgba(10, 14, 39, 0.8);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }

        .logo-main {
            width: 120px;
            height: 120px;
            background: linear-gradient(135deg, #d4af37, #f0d060);
            border-radius: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            font-weight: 900;
            color: #0a0e27;
            margin: 0 auto 20px;
            box-shadow: 0 10px 40px rgba(212, 175, 55, 0.4);
        }

        .system-name {
            font-size: 3em;
            font-weight: 900;
            background: linear-gradient(180deg, #f0d060, #d4af37);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 6px;
        }

        .system-subtitle {
            font-size: 1.2em;
            color: rgba(255, 255, 255, 0.9);
            margin: 10px 0;
            font-weight: 300;
        }

        .credits {
            font-size: 1em;
            color: rgba(212, 175, 55, 0.9);
            margin-bottom: 30px;
        }

        .startup-buttons {
            display: flex;
            flex-direction: column;
            gap: 12px;
            width: 350px;
        }

        .startup-btn {
            padding: 16px 30px;
            border: 2px solid transparent;
            border-radius: 50px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            letter-spacing: 1px;
            width: 100%;
            text-transform: uppercase;
        }

        .startup-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .startup-btn-login {
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.3);
            color: white;
        }

        .startup-btn-signup {
            background: rgba(40, 167, 69, 0.9);
            border-color: #28a745;
            color: white;
        }

        .startup-btn-create {
            background: linear-gradient(135deg, #d4af37, #b8941f);
            border-color: #d4af37;
            color: #0a0e27;
        }

        .hidden {
            display: none !important;
        }

        /* Notification */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 24px;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            z-index: 10000;
            animation: slideIn 0.4s ease;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .notification.success { background: rgba(40, 167, 69, 0.8); }
        .notification.error { background: rgba(220, 53, 69, 0.8); }
        .notification.info { background: rgba(23, 162, 184, 0.8); }

        @keyframes slideIn {
            from { transform: translateX(120%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        /* Main App */
        .main-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            padding: 25px;
            border: 1px solid var(--border-color);
        }

        h1, h2, h3 {
            color: white;
            margin-bottom: 15px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        }

        h2 { border-left: 4px solid var(--accent); padding-left: 15px; }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 13px;
            background: rgba(255, 255, 255, 0.05);
            color: white;
        }

        th, td {
            border: 1px solid var(--border-color);
            padding: 10px;
            text-align: left;
        }

        th {
            background: rgba(10, 14, 39, 0.8);
            color: white;
        }

        button {
            margin: 5px;
            padding: 10px 18px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: var(--transition);
            color: white;
        }

        button:hover { transform: translateY(-2px); }
        button:active { transform: scale(0.95); }

        .btn-primary { background: rgba(233, 69, 96, 0.8); }
        .btn-secondary { background: rgba(15, 52, 96, 0.8); }
        .btn-danger { background: rgba(220, 53, 69, 0.8); }
        .btn-success { background: rgba(40, 167, 69, 0.8); }
        .btn-gold {
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.9), rgba(184, 148, 31, 0.9));
            color: #0a0e27;
            font-weight: 700;
        }

        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: white;
            font-size: 0.9em;
        }

        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 14px;
            background: var(--glass-bg-input);
            color: white;
        }

        .form-group input:focus,
        .form-group select:focus {
            border-color: var(--accent);
            outline: none;
            box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.2);
        }

        select {
            color: white;
            background: rgba(15, 52, 96, 0.5);
        }

        select option {
            background: #1a1f4e;
            color: white;
        }

        .settings-group {
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 25px;
            margin-bottom: 25px;
            background: rgba(255, 255, 255, 0.05);
        }

        .scrollable-table {
            max-height: 500px;
            overflow: auto;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
        }

        .nav-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 20px;
            padding: 15px;
            border-bottom: 1px solid var(--border-color);
            background: rgba(255, 255, 255, 0.05);
            border-radius: var(--border-radius);
        }

        .nav-buttons button {
            background: rgba(255, 255, 255, 0.08);
            color: white;
            border: 1px solid var(--border-color);
        }

        .nav-buttons button:hover,
        .nav-buttons button.active-tab {
            background: rgba(233, 69, 96, 0.7);
            color: white;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: var(--border-radius);
            border: 1px solid var(--border-color);
        }

        .stat-value {
            font-size: 2em;
            font-weight: 800;
            color: white;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9em;
        }

        .school-code-banner {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 2px dashed rgba(233, 69, 96, 0.4);
            border-radius: var(--border-radius);
            padding: 20px;
            margin-bottom: 25px;
            text-align: center;
        }

        .invite-code {
            font-size: 2em;
            font-weight: 800;
            letter-spacing: 6px;
            color: white;
            font-family: 'Courier New', monospace;
            background: rgba(0, 0, 0, 0.3);
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
        }

        .center { text-align: center; }

        .role-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .role-admin { background: rgba(233, 69, 96, 0.8); }
        .role-teacher { background: rgba(15, 52, 96, 0.8); }
        .role-librarian { background: rgba(40, 167, 69, 0.8); }

        .overdue { background: rgba(248, 215, 218, 0.25); color: #ff6b6b; font-weight: bold; }

        .filter-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            margin: 4px;
            border: 1px solid var(--border-color);
        }

        .filter-badge.active {
            background: rgba(233, 69, 96, 0.7);
            color: white;
        }

        .filter-badge:not(.active) {
            background: rgba(255, 255, 255, 0.06);
            color: var(--text-secondary);
        }

        /* Chat Styles */
        .chat-container {
            display: flex;
            height: 600px;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            overflow: hidden;
            background: rgba(0, 0, 0, 0.3);
        }

        .chat-sidebar {
            width: 250px;
            background: rgba(10, 14, 39, 0.8);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
        }

        .chat-sidebar-header {
            padding: 20px;
            border-bottom: 1px solid var(--border-color);
            color: white;
            font-weight: 700;
        }

        .chat-users {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }

        .chat-user {
            padding: 12px 15px;
            cursor: pointer;
            border-radius: 8px;
            margin-bottom: 5px;
            transition: var(--transition);
            color: white;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .chat-user:hover, .chat-user.active {
            background: rgba(233, 69, 96, 0.4);
        }

        .chat-user-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.2em;
            flex-shrink: 0;
            background: linear-gradient(135deg, var(--accent), var(--info));
        }

        .chat-main {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .chat-header {
            padding: 20px;
            border-bottom: 1px solid var(--border-color);
            color: white;
            font-weight: 700;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .chat-message {
            display: flex;
            gap: 10px;
            max-width: 70%;
        }

        .chat-message.mine {
            align-self: flex-end;
            flex-direction: row-reverse;
        }

        .chat-message-content {
            background: rgba(255, 255, 255, 0.15);
            padding: 12px 16px;
            border-radius: 16px;
            color: white;
            font-size: 0.9em;
        }

        .chat-message.mine .chat-message-content {
            background: rgba(233, 69, 96, 0.5);
        }

        .chat-message-time {
            font-size: 0.7em;
            color: var(--text-muted);
            margin-top: 4px;
            text-align: right;
        }

        .chat-input-area {
            padding: 15px;
            border-top: 1px solid var(--border-color);
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .chat-input-area input {
            flex: 1;
            padding: 12px;
            border-radius: 25px;
            border: 1px solid var(--border-color);
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 14px;
        }

        .chat-input-area button {
            border-radius: 50%;
            width: 40px;
            height: 40px;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
        }

        .emoji-picker {
            position: absolute;
            bottom: 60px;
            right: 20px;
            background: #1a1f4e;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 10px;
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: 5px;
            z-index: 1000;
        }

        .emoji-btn {
            font-size: 20px;
            padding: 5px;
            cursor: pointer;
            border: none;
            background: none;
            transition: var(--transition);
        }

        .emoji-btn:hover {
            transform: scale(1.3);
        }

        /* Word Processor Styles */
        .word-processor {
            background: white;
            color: #333;
            border-radius: 8px;
            padding: 20px;
            min-height: 400px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }

        .word-toolbar {
            display: flex;
            gap: 10px;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 8px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }

        .word-toolbar button, .word-toolbar select {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
            cursor: pointer;
            color: #333;
            font-size: 14px;
        }

        .word-toolbar button:hover {
            background: #e9ecef;
        }

        .word-content {
            min-height: 300px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
            outline: none;
            font-size: 14px;
            line-height: 1.6;
            background: white;
            color: #333;
        }

        .word-content:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.1);
        }

        /* Wallpaper Grid */
        .wallpaper-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 15px;
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
        }

        .wallpaper-option {
            cursor: pointer;
            border-radius: 8px;
            overflow: hidden;
            border: 3px solid transparent;
            transition: var(--transition);
            aspect-ratio: 16/10;
            position: relative;
        }

        .wallpaper-option:hover {
            transform: scale(1.05);
            border-color: var(--accent);
        }

        .wallpaper-option img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .wallpaper-option.selected {
            border-color: var(--success);
            box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.4);
        }

        .wallpaper-label {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 5px;
            font-size: 10px;
            text-align: center;
        }

        /* File attachment */
        .attachment-preview {
            display: inline-block;
            padding: 5px 10px;
            background: rgba(233, 69, 96, 0.3);
            border-radius: 8px;
            margin: 5px;
            font-size: 12px;
            cursor: pointer;
        }

        footer {
            text-align: center;
            padding: 20px;
            color: var(--text-muted);
            font-size: 12px;
            margin-top: 20px;
            border-top: 1px solid var(--border-color);
        }

        footer .wegem-credit {
            color: #d4af37;
            font-weight: 700;
        }

        @media (max-width: 768px) {
            .startup-logo-container { padding: 20px; }
            .startup-buttons { width: 90%; }
            .chat-container { flex-direction: column; height: auto; }
            .chat-sidebar { width: 100%; max-height: 200px; }
            .chat-message { max-width: 90%; }
            .nav-buttons { font-size: 11px; }
        }
    </style>
</head>
<body>
    <div class="overlay" id="mainOverlay">
        <!-- STARTUP PAGE -->
        <div id="startupPage" class="startup-page">
            <div class="startup-particles" id="startupParticles"></div>
            <div class="startup-logo-container">
                <div class="logo-main">SRMS</div>
                <div class="system-name">SRMS</div>
                <div class="system-subtitle">School Resource Management System</div>
                <div class="credits">by <span style="color:#f0d060;font-weight:700;">WeGEM</span> (Edwin)</div>
                <div class="startup-buttons" id="startupButtons">
                    <button class="startup-btn startup-btn-login" id="btnLogin">🔑 Staff Login</button>
                    <button class="startup-btn startup-btn-signup" id="btnSignup">📝 Staff Sign Up</button>
                    <button class="startup-btn startup-btn-create" id="btnCreate">🏫 Create School</button>
                </div>
                <div id="startupFormsContainer" style="margin-top: 30px; width: 100%; max-width: 500px;"></div>
            </div>
        </div>

        <!-- MAIN APP -->
        <div id="mainApp" class="hidden">
            <div class="container">
                <div class="main-container">
                    <div class="center" style="margin-bottom: 20px;">
                        <h1 id="schoolHeader">School Resource Management System</h1>
                        <p id="userInfo"></p>
                    </div>

                    <div class="school-code-banner">
                        <div>🏫 School Invite Code</div>
                        <div class="invite-code" id="dashboardInviteCode">------</div>
                        <br>
                        <button class="btn-gold" id="btnCopyCode">📋 Copy Code</button>
                    </div>

                    <div class="nav-buttons" id="navButtons">
                        <button onclick="showSection('dashboardSection')" class="active-tab">📊 Dashboard</button>
                        <button onclick="showSection('bookIssuingSection')">📖 Books</button>
                        <button onclick="showSection('furnitureSection')">🪑 Furniture</button>
                        <button onclick="showSection('borrowedSection')">📋 Borrowed</button>
                        <button onclick="showSection('membersSection')">👥 Members</button>
                        <button onclick="showSection('teachersSection')">👨‍🏫 Teachers</button>
                        <button onclick="showSection('chatSection')">💬 Chat</button>
                        <button onclick="showSection('notesSection')">📝 Notes</button>
                        <button onclick="showSection('qrSection')">📱 QR</button>
                        <button onclick="showSection('wallpaperSection')">🖼️ Theme</button>
                        <button onclick="showSection('settingsSection')">⚙️ Settings</button>
                        <button class="btn-danger" onclick="logout()" style="margin-left: auto;">🚪 Logout</button>
                    </div>

                    <!-- DASHBOARD -->
                    <div id="dashboardSection" class="section">
                        <h2>📊 Dashboard</h2>
                        <div class="stats-grid">
                            <div class="stat-card"><div class="stat-value" id="totalBooks">0</div><div class="stat-label">Total Books</div></div>
                            <div class="stat-card"><div class="stat-value" id="booksBorrowed">0</div><div class="stat-label">Borrowed</div></div>
                            <div class="stat-card"><div class="stat-value" id="totalMembers">0</div><div class="stat-label">Members</div></div>
                            <div class="stat-card"><div class="stat-value" id="totalTeachers">0</div><div class="stat-label">Teachers</div></div>
                            <div class="stat-card"><div class="stat-value" id="overdueCount">0</div><div class="stat-label">Overdue</div></div>
                            <div class="stat-card"><div class="stat-value" id="activeLoans">0</div><div class="stat-label">Active Loans</div></div>
                        </div>
                    </div>

                    <!-- BOOK ISSUING -->
                    <div id="bookIssuingSection" class="section hidden">
                        <h2>📖 Book Management</h2>
                        <div class="settings-group">
                            <h3>Add Book</h3>
                            <div style="display:grid;grid-template-columns:1fr 1fr 1fr 100px;gap:10px;">
                                <input type="text" id="newBookTitle" placeholder="Book Title">
                                <select id="newBookType"><option>Textbook</option><option>Novel</option><option>Reference</option></select>
                                <input type="number" id="newBookQty" value="1" min="1">
                                <button class="btn-primary" id="addBookBtn">Add</button>
                            </div>
                        </div>
                        <div class="settings-group">
                            <h3>Issue Book</h3>
                            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                                <select id="issueBookSelect"></select>
                                <input type="text" id="issueStudentName" placeholder="Student Name">
                                <input type="text" id="issueStudentAdm" placeholder="ADM Number">
                                <input type="date" id="issueDate">
                                <input type="date" id="issueReturnDate">
                            </div>
                            <button class="btn-success" id="issueBookBtn" style="width:100%;margin-top:10px;">📖 Issue Book</button>
                        </div>
                        <div class="scrollable-table">
                            <table id="booksTable">
                                <thead><tr><th>Title</th><th>Type</th><th>Quantity</th><th>Action</th></tr></thead>
                                <tbody id="booksTableBody"></tbody>
                            </table>
                        </div>
                    </div>

                    <!-- FURNITURE -->
                    <div id="furnitureSection" class="section hidden">
                        <h2>🪑 Furniture Allocation</h2>
                        <div class="settings-group">
                            <h3>Assign Furniture</h3>
                            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                                <input type="text" id="furnitureStudent" placeholder="Student Name">
                                <input type="text" id="furnitureAdm" placeholder="ADM Number">
                                <input type="text" id="furnitureChair" placeholder="Chair Number">
                                <input type="text" id="furnitureLocker" placeholder="Locker Number">
                                <input type="date" id="furnitureDate">
                            </div>
                            <button class="btn-success" id="assignFurnitureBtn" style="width:100%;margin-top:10px;">✅ Assign</button>
                        </div>
                        <div class="scrollable-table">
                            <table id="furnitureTable">
                                <thead><tr><th>Student</th><th>ADM</th><th>Chair</th><th>Locker</th><th>Date</th><th>Action</th></tr></thead>
                                <tbody id="furnitureTableBody"></tbody>
                            </table>
                        </div>
                    </div>

                    <!-- BORROWED -->
                    <div id="borrowedSection" class="section hidden">
                        <h2>📋 Borrowed Items</h2>
                        <div style="margin-bottom:10px;">
                            <span class="filter-badge active" onclick="filterBorrowed('all')">All</span>
                            <span class="filter-badge" onclick="filterBorrowed('active')">Active</span>
                            <span class="filter-badge" onclick="filterBorrowed('overdue')">Overdue</span>
                        </div>
                        <div class="scrollable-table">
                            <table>
                                <thead><tr><th>Student</th><th>ADM</th><th>Book</th><th>Borrowed</th><th>Due</th><th>Status</th><th>Action</th></tr></thead>
                                <tbody id="borrowedTableBody"></tbody>
                            </table>
                        </div>
                    </div>

                    <!-- MEMBERS -->
                    <div id="membersSection" class="section hidden">
                        <h2>👥 Members</h2>
                        <div class="settings-group">
                            <div style="display:flex;gap:10px;">
                                <input type="text" id="memberName" placeholder="Name" style="flex:1;">
                                <input type="text" id="memberId" placeholder="ID" style="flex:1;">
                                <button class="btn-primary" id="addMemberBtn">➕ Add</button>
                            </div>
                        </div>
                        <ul id="memberList" style="list-style:none;padding:0;"></ul>
                    </div>

                    <!-- TEACHERS -->
                    <div id="teachersSection" class="section hidden">
                        <h2>👨‍🏫 Teachers</h2>
                        <div class="settings-group">
                            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;">
                                <input type="text" id="teacherName" placeholder="Name">
                                <input type="text" id="teacherSubject" placeholder="Subjects">
                                <input type="text" id="teacherDuty" placeholder="Class">
                            </div>
                            <button class="btn-primary" id="addTeacherBtn" style="width:100%;margin-top:10px;">➕ Add Teacher</button>
                        </div>
                        <div class="scrollable-table">
                            <table>
                                <thead><tr><th>Name</th><th>Subjects</th><th>Class</th><th>Action</th></tr></thead>
                                <tbody id="teacherTableBody"></tbody>
                            </table>
                        </div>
                    </div>

                    <!-- CHAT -->
                    <div id="chatSection" class="section hidden">
                        <h2>💬 Staff Chat</h2>
                        <div class="chat-container">
                            <div class="chat-sidebar">
                                <div class="chat-sidebar-header">👥 Staff</div>
                                <div class="chat-users" id="chatUsersList"></div>
                            </div>
                            <div class="chat-main" style="position:relative;">
                                <div class="chat-header" id="chatActiveUser">Select a user</div>
                                <div class="chat-messages" id="chatMessages"></div>
                                <div id="emojiPicker" class="emoji-picker hidden"></div>
                                <div class="chat-input-area">
                                    <button class="btn-secondary" id="emojiBtn" style="font-size:1.5em;">😊</button>
                                    <button class="btn-secondary" id="attachBtn" style="font-size:1.2em;">📎</button>
                                    <input type="file" id="fileInput" style="display:none;" multiple>
                                    <input type="text" id="chatInput" placeholder="Type a message...">
                                    <button class="btn-primary" onclick="sendChatMessage()">📤</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- NOTES (Word Processor) -->
                    <div id="notesSection" class="section hidden">
                        <h2>📝 Private Notes</h2>
                        <div class="word-processor">
                            <div class="word-toolbar">
                                <button onclick="formatDoc('bold')"><b>B</b></button>
                                <button onclick="formatDoc('italic')"><i>I</i></button>
                                <button onclick="formatDoc('underline')"><u>U</u></button>
                                <select onchange="formatDoc('fontSize', this.value)">
                                    <option value="1">Small</option>
                                    <option value="3" selected>Normal</option>
                                    <option value="5">Large</option>
                                    <option value="7">Huge</option>
                                </select>
                                <select onchange="formatDoc('foreColor', this.value)">
                                    <option value="#000000">Black</option>
                                    <option value="#e94560">Red</option>
                                    <option value="#0f3460">Blue</option>
                                    <option value="#28a745">Green</option>
                                </select>
                                <button onclick="formatDoc('justifyLeft')">⬅️</button>
                                <button onclick="formatDoc('justifyCenter')">⬆️</button>
                                <button onclick="formatDoc('justifyRight')">➡️</button>
                                <button onclick="formatDoc('insertUnorderedList')">📋</button>
                                <button onclick="formatDoc('insertOrderedList')">🔢</button>
                                <input type="file" id="notesFileInput" style="display:none;" multiple>
                                <button onclick="document.getElementById('notesFileInput').click()">📎 Attach</button>
                                <button class="btn-primary" onclick="saveNotes()" style="margin-left:auto;">💾 Save</button>
                            </div>
                            <div class="word-content" id="wordContent" contenteditable="true">
                                Start typing your private notes here...
                            </div>
                            <div id="notesAttachments" style="margin-top:10px;"></div>
                        </div>
                    </div>

                    <!-- QR -->
                    <div id="qrSection" class="section hidden">
                        <h2>📱 QR Codes</h2>
                        <div class="settings-group">
                            <h3>Generate</h3>
                            <div style="display:flex;gap:10px;">
                                <select id="qrType"><option value="book">Book</option><option value="chair">Chair</option><option value="locker">Locker</option></select>
                                <input type="number" id="qrStart" value="1" style="width:80px;">
                                <input type="number" id="qrEnd" value="10" style="width:80px;">
                                <button class="btn-primary" onclick="generateQR()">Generate</button>
                            </div>
                            <div id="qrContainer" style="display:flex;flex-wrap:wrap;gap:10px;margin-top:15px;"></div>
                        </div>
                        <div class="settings-group">
                            <h3>Scan</h3>
                            <button class="btn-primary" id="scanBtn">📷 Start Scanner</button>
                            <div id="qrScanner" style="max-width:400px;margin-top:15px;"></div>
                            <p id="scanResult" style="margin-top:10px;font-weight:bold;"></p>
                        </div>
                    </div>

                    <!-- WALLPAPER -->
                    <div id="wallpaperSection" class="section hidden">
                        <h2>🖼️ Theme & Wallpaper</h2>
                        <div class="settings-group">
                            <h3>Choose Wallpaper</h3>
                            <div class="wallpaper-grid" id="wallpaperGrid"></div>
                        </div>
                        <div class="settings-group">
                            <h3>Upload Custom Wallpaper</h3>
                            <input type="file" id="wallpaperUpload" accept="image/*">
                            <button class="btn-secondary" id="applyWallpaperBtn" style="margin-top:10px;">Apply Custom</button>
                            <button class="btn-primary" id="resetWallpaperBtn" style="margin-top:10px;">Reset Default</button>
                        </div>
                    </div>

                    <!-- SETTINGS -->
                    <div id="settingsSection" class="section hidden">
                        <h2>⚙️ Settings</h2>
                        <div class="settings-group">
                            <h3>Password Recovery</h3>
                            <p style="color:var(--text-secondary);margin-bottom:10px;">Forgot your password? Enter your email to reset.</p>
                            <div style="display:flex;gap:10px;">
                                <input type="email" id="recoveryEmail" placeholder="Your email" style="flex:1;">
                                <button class="btn-primary" onclick="recoverPassword()">🔑 Reset Password</button>
                            </div>
                            <div id="recoveryMessage" style="margin-top:10px;"></div>
                        </div>
                        <div class="settings-group">
                            <h3>Data Management</h3>
                            <button class="btn-danger" onclick="clearAllData()">⚠️ Clear All Data</button>
                            <button class="btn-secondary" onclick="exportData()">📥 Backup</button>
                            <button class="btn-secondary" onclick="document.getElementById('importFile').click()">📤 Restore</button>
                            <input type="file" id="importFile" style="display:none;" accept=".json">
                        </div>
                    </div>

                    <footer>
                        <p>SRMS - School Resource Management System v7.0 | <span class="wegem-credit">by WeGEM (Edwin)</span> | © 2025</p>
                    </footer>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Supabase
        const supabase = window.supabase.createClient(
            'https://mcjkdnhbbnxvvgnjbuzy.supabase.co',
            'sb_publishable_UxInPN35lw3WlOvPHFqUWw_6rDmZ-sd'
        );

        // App State
        let appState = {
            orgId: null,
            orgName: "",
            adminName: "",
            adminEmail: "",
            inviteCode: null,
            users: [],
            currentUser: null,
            currentRole: null,
            books: [],
            members: [],
            borrowed: [],
            teachers: [],
            furnitureAllocations: [],
            chatMessages: [],
            notesData: { content: '', attachments: [] },
            auditLog: [],
            schoolId: null
        };

        let borrowedFilter = 'all';
        let chatActiveUser = null;
        let qrScanner = null;

        // Helper Functions
        function saveState() {
            localStorage.setItem('schoolSystemV6', JSON.stringify(appState));
        }

        function showNotification(msg, type = 'info') {
            const n = document.createElement('div');
            n.className = `notification ${type}`;
            n.textContent = msg;
            document.body.appendChild(n);
            setTimeout(() => { n.remove(); }, 3500);
        }

        function generateInviteCode() {
            return Math.random().toString(36).substring(2, 10).toUpperCase();
        }

        // Create particles
        function createParticles() {
            const container = document.getElementById('startupParticles');
            for (let i = 0; i < 30; i++) {
                const p = document.createElement('div');
                p.className = 'startup-particle';
                p.style.cssText = `width:${Math.random()*60+20}px;height:${Math.random()*60+20}px;left:${Math.random()*100}%;animation-delay:${Math.random()*15}s`;
                container.appendChild(p);
            }
        }

        // Show startup form
        function showStartupForm(type) {
            const container = document.getElementById('startupFormsContainer');
            const style = 'background:rgba(255,255,255,0.1);backdrop-filter:blur(20px);border-radius:16px;padding:30px;border:1px solid rgba(255,255,255,0.2);';
            const is = 'background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.3);color:white;width:100%;padding:12px;border-radius:8px;margin-top:5px;';
            const ls = 'color:rgba(255,255,255,0.9);font-size:0.9em;font-weight:600;';

            if (type === 'login') {
                container.innerHTML = `
                    <div style="${style}">
                        <h3 style="color:white;">🔐 Staff Login</h3>
                        <div style="margin:15px 0;"><label style="${ls}">👤 Name:</label><input id="loginName" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">🏢 School:</label><input id="loginSchool" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">🔑 Code:</label><input id="loginCode" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">🔒 Password:</label><input type="password" id="loginPassword" style="${is}"></div>
                        <button onclick="handleLogin()" class="startup-btn startup-btn-login" style="width:100%;">🔑 Login</button>
                        <p style="text-align:center;margin-top:10px;color:rgba(255,255,255,0.6);cursor:pointer;" onclick="showStartupForm('forgot')">Forgot Password?</p>
                    </div>`;
            } else if (type === 'signup') {
                container.innerHTML = `
                    <div style="${style}">
                        <h3 style="color:white;">📝 Sign Up</h3>
                        <div style="margin:15px 0;"><label style="${ls}">👤 Name:</label><input id="signupName" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">📧 Email:</label><input type="email" id="signupEmail" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">📞 Phone:</label><input type="tel" id="signupPhone" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">🏢 School:</label><input id="signupSchool" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">🔑 Code:</label><input id="signupCode" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">🔒 Password:</label><input type="password" id="signupPassword" style="${is}"></div>
                        <button onclick="handleSignup()" class="startup-btn startup-btn-signup" style="width:100%;">📝 Sign Up</button>
                    </div>`;
            } else if (type === 'create') {
                container.innerHTML = `
                    <div style="${style}">
                        <h3 style="color:white;">🏫 Create School</h3>
                        <div style="margin:15px 0;"><label style="${ls}">🏢 School Name:</label><input id="createSchool" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">📍 Address:</label><input id="createAddress" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">👤 Admin Name:</label><input id="createAdmin" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">📧 Admin Email:</label><input type="email" id="createEmail" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">📞 Phone:</label><input type="tel" id="createPhone" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">🔒 Password:</label><input type="password" id="createPassword" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">🔒 Confirm:</label><input type="password" id="createPassword2" style="${is}"></div>
                        <button onclick="handleCreate()" class="startup-btn startup-btn-create" style="width:100%;">🚀 Create</button>
                    </div>`;
            } else if (type === 'forgot') {
                container.innerHTML = `
                    <div style="${style}">
                        <h3 style="color:white;">🔑 Forgot Password</h3>
                        <p style="color:rgba(255,255,255,0.7);margin-bottom:15px;">Enter your email to reset password</p>
                        <div style="margin:15px 0;"><label style="${ls}">📧 Email:</label><input type="email" id="forgotEmail" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">🏢 School:</label><input id="forgotSchool" style="${is}"></div>
                        <div style="margin:15px 0;"><label style="${ls}">🔑 Code:</label><input id="forgotCode" style="${is}"></div>
                        <button onclick="handleForgotPassword()" class="startup-btn startup-btn-login" style="width:100%;">🔑 Reset</button>
                        <p id="forgotMessage" style="text-align:center;margin-top:10px;color:var(--gold-light);"></p>
                    </div>`;
            }
            container.scrollIntoView({ behavior: 'smooth' });
        }

        // Handle Forgot Password
        function handleForgotPassword() {
            const email = document.getElementById('forgotEmail')?.value.trim();
            const org = document.getElementById('forgotSchool')?.value.trim();
            const code = document.getElementById('forgotCode')?.value.trim().toUpperCase();
            const msg = document.getElementById('forgotMessage');

            if (!email || !org || !code) {
                if (msg) msg.textContent = 'Please fill all fields';
                return;
            }

            if (appState.orgName !== org || appState.inviteCode !== code) {
                if (msg) msg.textContent = 'School or code not found';
                return;
            }

            const user = appState.users.find(u => u.email === email);
            if (!user) {
                if (msg) msg.textContent = 'Email not found';
                return;
            }

            // In a real app, send email. For now, show password hint
            const newPassword = Math.random().toString(36).substring(2, 10);
            user.password = newPassword;
            saveState();
            if (msg) msg.textContent = `✅ New password: ${newPassword} (Please change after login)`;
        }

        // Handle Login
        function handleLogin() {
            const name = document.getElementById('loginName')?.value.trim();
            const org = document.getElementById('loginSchool')?.value.trim();
            const code = document.getElementById('loginCode')?.value.trim().toUpperCase();
            const pw = document.getElementById('loginPassword')?.value;

            if (!name || !org || !code || !pw) {
                showNotification("Fill all fields", "error");
                return;
            }

            if (appState.orgName !== org) {
                showNotification("School not found", "error");
                return;
            }

            const user = appState.users.find(u => u.code === code && u.name.toLowerCase() === name.toLowerCase());
            if (!user || user.password !== pw) {
                showNotification("Invalid credentials", "error");
                return;
            }

            appState.currentUser = { name: user.name, role: user.role, email: user.email, staffId: user.staffId };
            appState.currentRole = user.role;
            saveState();
            showNotification("Welcome back!", "success");
            launchApp();
        }

        // Handle Signup
        function handleSignup() {
            const name = document.getElementById('signupName')?.value.trim();
            const email = document.getElementById('signupEmail')?.value.trim();
            const phone = document.getElementById('signupPhone')?.value.trim();
            const org = document.getElementById('signupSchool')?.value.trim();
            const code = document.getElementById('signupCode')?.value.trim().toUpperCase();
            const pw = document.getElementById('signupPassword')?.value;

            if (!name || !email || !org || !code || !pw) {
                showNotification("Fill required fields", "error");
                return;
            }

            if (pw.length < 6) {
                showNotification("Password min 6 chars", "error");
                return;
            }

            if (appState.orgName !== org || appState.inviteCode !== code) {
                showNotification("Invalid school or code", "error");
                return;
            }

            if (appState.users.find(u => u.email === email)) {
                showNotification("Email already registered", "error");
                return;
            }

            const newUser = { code, name, email, phone, role: 'teacher', password: pw, staffId: `TCH-${Date.now().toString(36).toUpperCase()}` };
            appState.users.push(newUser);
            appState.currentUser = { name, role: 'teacher', email, phone, staffId: newUser.staffId };
            appState.currentRole = 'teacher';
            saveState();
            showNotification("Signed up!", "success");
            launchApp();
        }

        // Handle Create School
        function handleCreate() {
            const org = document.getElementById('createSchool')?.value.trim();
            const address = document.getElementById('createAddress')?.value.trim();
            const admin = document.getElementById('createAdmin')?.value.trim();
            const email = document.getElementById('createEmail')?.value.trim();
            const phone = document.getElementById('createPhone')?.value.trim();
            const pw = document.getElementById('createPassword')?.value;
            const pw2 = document.getElementById('createPassword2')?.value;

            if (!org || !admin || !email || !pw) {
                showNotification("Fill required fields", "error");
                return;
            }

            if (pw !== pw2) {
                showNotification("Passwords don't match", "error");
                return;
            }

            const code = generateInviteCode();
            appState.orgId = Date.now().toString();
            appState.orgName = org;
            appState.adminName = admin;
            appState.adminEmail = email;
            appState.inviteCode = code;
            appState.schoolAddress = address;
            appState.users = [{ code, name: admin, email, phone, role: 'admin', password: pw, staffId: 'ADMIN-001' }];
            appState.currentUser = { name: admin, role: 'admin', email, phone, staffId: 'ADMIN-001' };
            appState.currentRole = 'admin';
            saveState();
            showNotification(`School created! Code: ${code}`, "success");
            launchApp();
        }

        // Launch app
        function launchApp() {
            document.getElementById('startupPage').classList.add('hidden');
            document.getElementById('mainApp').classList.remove('hidden');
            document.getElementById('schoolHeader').textContent = appState.orgName;
            document.getElementById('userInfo').innerHTML = `👤 ${appState.currentUser.name} <span class="role-badge role-${appState.currentRole}">${appState.currentRole}</span>`;
            document.getElementById('dashboardInviteCode').textContent = appState.inviteCode || '------';
            updateDashboard();
            renderAll();
        }

        // Update Dashboard
        function updateDashboard() {
            const tb = appState.books.reduce((s, b) => s + b.quantity, 0);
            const bb = appState.borrowed.filter(b => !b.returned).length;
            document.getElementById('totalBooks').textContent = tb;
            document.getElementById('booksBorrowed').textContent = bb;
            document.getElementById('totalMembers').textContent = appState.members.length;
            document.getElementById('totalTeachers').textContent = appState.teachers.length;
            document.getElementById('overdueCount').textContent = appState.borrowed.filter(b => !b.returned && new Date(b.returnDate) < new Date()).length;
            document.getElementById('activeLoans').textContent = bb;
        }

        // Show Section
        function showSection(id) {
            document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
            const section = document.getElementById(id);
            if (section) section.classList.remove('hidden');

            if (id === 'chatSection') renderChatUsers();
            if (id === 'wallpaperSection') renderWallpapers();
            if (id === 'notesSection') loadNotes();
            if (id === 'qrSection') setupQRScanner();
        }

        // Render Books
        function renderBooks() {
            const tbody = document.getElementById('booksTableBody');
            const select = document.getElementById('issueBookSelect');
            if (tbody) tbody.innerHTML = appState.books.map((b, i) => `<tr><td>${b.title}</td><td>${b.type}</td><td>${b.quantity}</td><td><button class="btn-danger" onclick="deleteBook(${i})">🗑️</button></td></tr>`).join('');
            if (select) select.innerHTML = '<option value="">-- Select --</option>' + appState.books.filter(b => b.quantity > 0).map(b => `<option>${b.title}</option>`).join('');
        }

        function deleteBook(i) { appState.books.splice(i, 1); saveState(); renderBooks(); updateDashboard(); }

        // Issue Book
        document.getElementById('issueBookBtn')?.addEventListener('click', () => {
            const title = document.getElementById('issueBookSelect').value;
            const name = document.getElementById('issueStudentName').value.trim();
            const adm = document.getElementById('issueStudentAdm').value.trim();
            const bDate = document.getElementById('issueDate').value;
            const rDate = document.getElementById('issueReturnDate').value;

            if (!title || !name || !adm || !bDate || !rDate) {
                showNotification("Fill all fields", "error");
                return;
            }

            const book = appState.books.find(b => b.title === title);
            if (!book || book.quantity <= 0) {
                showNotification("Out of stock", "error");
                return;
            }

            book.quantity--;
            appState.borrowed.push({
                id: Date.now(),
                name,
                adm,
                bookTitle: title,
                borrowDate: bDate,
                returnDate: rDate,
                returned: false
            });
            saveState();
            renderBooks();
            renderBorrowed();
            updateDashboard();
            showNotification("Book issued!", "success");
        });

        // Render Borrowed
        function renderBorrowed() {
            const tbody = document.getElementById('borrowedTableBody');
            if (!tbody) return;
            let data = appState.borrowed;
            if (borrowedFilter === 'active') data = data.filter(b => !b.returned);
            if (borrowedFilter === 'overdue') data = data.filter(b => !b.returned && new Date(b.returnDate) < new Date());
            tbody.innerHTML = data.map(b => {
                const isOv = !b.returned && new Date(b.returnDate) < new Date();
                return `<tr><td>${b.name}</td><td>${b.adm}</td><td>${b.bookTitle}</td><td>${b.borrowDate}</td><td class="${isOv?'overdue':''}">${b.returnDate}</td><td>${b.returned?'Returned':(isOv?'🔴 OVERDUE':'Active')}</td><td>${!b.returned?`<button class="btn-success" onclick="returnBook('${b.id}')">Return</button>`:'-'}</td></tr>`;
            }).join('');
        }

        function filterBorrowed(f) {
            borrowedFilter = f;
            document.querySelectorAll('#borrowedSection .filter-badge').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            renderBorrowed();
        }

        function returnBook(id) {
            const rec = appState.borrowed.find(b => b.id == id);
            if (rec) {
                rec.returned = true;
                const book = appState.books.find(b => b.title === rec.bookTitle);
                if (book) book.quantity++;
                saveState();
                renderBorrowed();
                renderBooks();
                updateDashboard();
                showNotification("Book returned!", "success");
            }
        }

        // Furniture
        document.getElementById('assignFurnitureBtn')?.addEventListener('click', () => {
            const name = document.getElementById('furnitureStudent').value.trim();
            const adm = document.getElementById('furnitureAdm').value.trim();
            const chair = document.getElementById('furnitureChair').value.trim();
            const locker = document.getElementById('furnitureLocker').value.trim();
            const date = document.getElementById('furnitureDate').value;

            if (!name || !adm || !date) {
                showNotification("Fill required fields", "error");
                return;
            }

            appState.furnitureAllocations.push({
                id: Date.now(),
                name,
                adm,
                chair,
                locker,
                date,
                returned: false
            });
            saveState();
            renderFurniture();
            showNotification("Furniture assigned!", "success");
        });

        function renderFurniture() {
            const tbody = document.getElementById('furnitureTableBody');
            if (tbody) tbody.innerHTML = appState.furnitureAllocations.map(f =>
                `<tr><td>${f.name}</td><td>${f.adm}</td><td>${f.chair||'-'}</td><td>${f.locker||'-'}</td><td>${f.date}</td><td>${!f.returned?`<button class="btn-success" onclick="returnFurniture('${f.id}')">Return</button>`:'Returned'}</td></tr>`
            ).join('');
        }

        function returnFurniture(id) {
            const item = appState.furnitureAllocations.find(f => f.id == id);
            if (item) { item.returned = true; saveState(); renderFurniture(); showNotification("Returned!", "success"); }
        }

        // Members
        document.getElementById('addMemberBtn')?.addEventListener('click', () => {
            const name = document.getElementById('memberName').value.trim();
            const id = document.getElementById('memberId').value.trim();
            if (name) {
                appState.members.push({ name, id: id || `MEM-${Date.now()}` });
                saveState();
                renderMembers();
                updateDashboard();
                document.getElementById('memberName').value = '';
                document.getElementById('memberId').value = '';
                showNotification("Member added!", "success");
            }
        });

        function renderMembers() {
            const list = document.getElementById('memberList');
            if (list) list.innerHTML = appState.members.map((m, i) =>
                `<li style="padding:10px;border-bottom:1px solid var(--border-color);display:flex;justify-content:space-between;"><span><strong>${m.name}</strong> (${m.id})</span><button class="btn-danger" onclick="deleteMember(${i})" style="padding:5px 10px;">🗑️</button></li>`
            ).join('');
        }

        function deleteMember(i) { appState.members.splice(i, 1); saveState(); renderMembers(); updateDashboard(); }

        // Teachers
        document.getElementById('addTeacherBtn')?.addEventListener('click', () => {
            const name = document.getElementById('teacherName').value.trim();
            const subject = document.getElementById('teacherSubject').value.trim();
            const duty = document.getElementById('teacherDuty').value.trim();
            if (name) {
                appState.teachers.push({ name, subject, duty });
                saveState();
                renderTeachers();
                updateDashboard();
                ['teacherName','teacherSubject','teacherDuty'].forEach(id => document.getElementById(id).value = '');
                showNotification("Teacher added!", "success");
            }
        });

        function renderTeachers() {
            const tbody = document.getElementById('teacherTableBody');
            if (tbody) tbody.innerHTML = appState.teachers.map((t, i) =>
                `<tr><td>${t.name}</td><td>${t.subject||'-'}</td><td>${t.duty||'-'}</td><td><button class="btn-danger" onclick="deleteTeacher(${i})">🗑️</button></td></tr>`
            ).join('');
        }

        function deleteTeacher(i) { appState.teachers.splice(i, 1); saveState(); renderTeachers(); updateDashboard(); }

        // Chat System
        function renderChatUsers() {
            const list = document.getElementById('chatUsersList');
            if (!list) return;
            const others = appState.users.filter(u => u.name !== appState.currentUser?.name);
            list.innerHTML = others.map(u =>
                `<div class="chat-user ${chatActiveUser===u.name?'active':''}" onclick="selectChatUser('${u.name}')">
                    <div class="chat-user-avatar">${u.name[0]}</div>
                    <div>${u.name}<br><small style="color:var(--text-muted);">${u.role}</small></div>
                </div>`
            ).join('') || '<p style="padding:20px;color:var(--text-muted);">No other staff</p>';
        }

        function selectChatUser(name) {
            chatActiveUser = name;
            document.getElementById('chatActiveUser').textContent = `💬 ${name}`;
            renderChatMessages();
        }

        function sendChatMessage() {
            const input = document.getElementById('chatInput');
            const msg = input.value.trim();
            if (!msg || !chatActiveUser) return;
            appState.chatMessages.push({
                id: Date.now(),
                from: appState.currentUser.name,
                to: chatActiveUser,
                message: msg,
                timestamp: new Date().toISOString(),
                read: false
            });
            saveState();
            input.value = '';
            renderChatMessages();
        }

        function renderChatMessages() {
            const container = document.getElementById('chatMessages');
            if (!container) return;
            if (!chatActiveUser) {
                container.innerHTML = '<p style="text-align:center;padding:40px;color:var(--text-muted);">Select a user</p>';
                return;
            }
            const msgs = appState.chatMessages.filter(m =>
                (m.from === appState.currentUser.name && m.to === chatActiveUser) ||
                (m.from === chatActiveUser && m.to === appState.currentUser.name)
            ).sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

            container.innerHTML = msgs.map(m => {
                const isMine = m.from === appState.currentUser.name;
                return `<div class="chat-message ${isMine?'mine':''}">
                    <div class="chat-message-avatar" style="width:30px;height:30px;border-radius:50%;background:var(--accent);display:flex;align-items:center;justify-content:center;font-size:0.8em;">${m.from[0]}</div>
                    <div class="chat-message-content">${m.message}<div class="chat-message-time">${new Date(m.timestamp).toLocaleTimeString()}</div></div>
                </div>`;
            }).join('');
            container.scrollTop = container.scrollHeight;
        }

        // Emoji Picker
        const emojis = ['😀','😂','😍','🥰','😎','🤩','😢','😡','👍','👎','❤️','🔥','⭐','🎉','💡','📚','✏️','💻','✅','❌'];

        document.getElementById('emojiBtn')?.addEventListener('click', () => {
            const picker = document.getElementById('emojiPicker');
            picker.classList.toggle('hidden');
            if (!picker.classList.contains('hidden')) {
                picker.innerHTML = emojis.map(e => `<button class="emoji-btn" onclick="insertEmoji('${e}')">${e}</button>`).join('');
            }
        });

        function insertEmoji(emoji) {
            const input = document.getElementById('chatInput');
            input.value += emoji;
            document.getElementById('emojiPicker').classList.add('hidden');
        }

        // File Attachment in Chat
        document.getElementById('attachBtn')?.addEventListener('click', () => document.getElementById('fileInput').click());
        document.getElementById('fileInput')?.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (ev) => {
                    appState.chatMessages.push({
                        id: Date.now(),
                        from: appState.currentUser.name,
                        to: chatActiveUser,
                        message: `📎 [File: ${file.name}]`,
                        attachment: ev.target.result,
                        timestamp: new Date().toISOString()
                    });
                    saveState();
                    renderChatMessages();
                };
                reader.readAsDataURL(file);
            }
        });

        // Notes (Word Processor)
        function loadNotes() {
            const content = document.getElementById('wordContent');
            const attachments = document.getElementById('notesAttachments');
            if (content && appState.notesData.content) {
                content.innerHTML = appState.notesData.content;
            }
            if (attachments) {
                attachments.innerHTML = (appState.notesData.attachments || []).map((a, i) =>
                    `<span class="attachment-preview" onclick="window.open('${a.data}')">📎 ${a.name}</span>`
                ).join('');
            }
        }

        function saveNotes() {
            const content = document.getElementById('wordContent');
            appState.notesData.content = content.innerHTML;
            saveState();
            showNotification("Notes saved!", "success");
        }

        function formatDoc(command, value = null) {
            document.execCommand(command, false, value);
            document.getElementById('wordContent').focus();
        }

        document.getElementById('notesFileInput')?.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (ev) => {
                    if (!appState.notesData.attachments) appState.notesData.attachments = [];
                    appState.notesData.attachments.push({ name: file.name, data: ev.target.result });
                    saveState();
                    loadNotes();
                    showNotification("File attached!", "success");
                };
                reader.readAsDataURL(file);
            }
        });

        // QR Scanner
        function setupQRScanner() {
            document.getElementById('scanBtn').addEventListener('click', function() {
                if (qrScanner) {
                    qrScanner.stop().then(() => { qrScanner = null; this.textContent = '📷 Start Scanner'; });
                    return;
                }
                document.getElementById('qrScanner').innerHTML = '<div id="qr-reader"></div>';
                qrScanner = new Html5Qrcode("qr-reader");
                qrScanner.start(
                    { facingMode: "environment" },
                    { fps: 10, qrbox: 250 },
                    (decoded) => {
                        document.getElementById('scanResult').textContent = `✅ Scanned: ${decoded}`;
                        qrScanner.stop();
                        qrScanner = null;
                    },
                    () => {}
                ).catch(err => showNotification("Camera error: " + err, "error"));
                this.textContent = '🛑 Stop';
            });
        }

        function generateQR() {
            const type = document.getElementById('qrType').value;
            const start = parseInt(document.getElementById('qrStart').value);
            const end = parseInt(document.getElementById('qrEnd').value);
            const container = document.getElementById('qrContainer');
            container.innerHTML = '';
            for (let i = start; i <= end; i++) {
                const div = document.createElement('div');
                div.innerHTML = `<strong>${type}:${i}</strong><div id="qr-${i}"></div>`;
                container.appendChild(div);
                new QRCode(document.getElementById(`qr-${i}`), { text: `${type}-${i}`, width: 100, height: 100 });
            }
        }

        // Wallpapers
        const wallpapers = [
            { name: 'Library', url: 'https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=400' },
            { name: 'Classroom', url: 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400' },
            { name: 'Study', url: 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400' },
            { name: 'Sunset', url: 'https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=400' },
            { name: 'Ocean', url: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400' },
            { name: 'Forest', url: 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400' },
            { name: 'Mountain', url: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400' },
            { name: 'Night Sky', url: 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=400' },
            { name: 'Abstract', url: 'https://images.unsplash.com/photo-1557683316-973673baf926?w=400' },
            { name: 'Technology', url: 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400' },
            { name: 'Space', url: 'https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=400' },
            { name: 'Nature', url: 'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=400' }
        ];

        function renderWallpapers() {
            const grid = document.getElementById('wallpaperGrid');
            if (!grid) return;
            grid.innerHTML = wallpapers.map(wp =>
                `<div class="wallpaper-option" onclick="setWallpaper('${wp.url}')">
                    <img src="${wp.url}" alt="${wp.name}">
                    <div class="wallpaper-label">${wp.name}</div>
                </div>`
            ).join('');
        }

        function setWallpaper(url) {
            document.body.style.backgroundImage = `url('${url}')`;
            localStorage.setItem('wallpaper', url);
            showNotification("Wallpaper set!", "success");
        }

        document.getElementById('applyWallpaperBtn')?.addEventListener('click', () => {
            const file = document.getElementById('wallpaperUpload').files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => setWallpaper(e.target.result);
                reader.readAsDataURL(file);
            }
        });

        document.getElementById('resetWallpaperBtn')?.addEventListener('click', () => {
            document.body.style.backgroundImage = '';
            localStorage.removeItem('wallpaper');
            showNotification("Reset!", "success");
        });

        // Password Recovery in Settings
        function recoverPassword() {
            const email = document.getElementById('recoveryEmail').value.trim();
            const msg = document.getElementById('recoveryMessage');
            if (!email) {
                msg.innerHTML = '<span style="color:#ff6b6b;">Enter email</span>';
                return;
            }
            const user = appState.users.find(u => u.email === email);
            if (!user) {
                msg.innerHTML = '<span style="color:#ff6b6b;">Email not found</span>';
                return;
            }
            const newPw = Math.random().toString(36).substring(2, 10);
            user.password = newPw;
            saveState();
            msg.innerHTML = `<span style="color:#28a745;">✅ New password: <strong>${newPw}</strong></span>`;
        }

        // Data Management
        function clearAllData() {
            if (confirm("DELETE ALL DATA?") && prompt("Type DELETE:") === 'DELETE') {
                localStorage.clear();
                location.reload();
            }
        }

        function exportData() {
            const blob = new Blob([JSON.stringify(appState)], { type: 'application/json' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `srms_backup_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
        }

        document.getElementById('importFile')?.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (ev) => {
                    try {
                        const data = JSON.parse(ev.target.result);
                        Object.assign(appState, data);
                        saveState();
                        showNotification("Data restored!", "success");
                        location.reload();
                    } catch {
                        showNotification("Invalid file", "error");
                    }
                };
                reader.readAsText(file);
            }
        });

        // Add Book
        document.getElementById('addBookBtn')?.addEventListener('click', () => {
            const title = document.getElementById('newBookTitle').value.trim();
            const type = document.getElementById('newBookType').value;
            const qty = parseInt(document.getElementById('newBookQty').value);
            if (title && qty > 0) {
                const existing = appState.books.find(b => b.title === title);
                if (existing) { existing.quantity += qty; }
                else { appState.books.push({ title, type, quantity: qty }); }
                saveState();
                renderBooks();
                updateDashboard();
                document.getElementById('newBookTitle').value = '';
                showNotification("Book added!", "success");
            }
        });

        // Logout
        function logout() {
            appState.currentUser = null;
            appState.currentRole = null;
            saveState();
            location.reload();
        }

        // Copy code
        function copyDashboardCode() {
            navigator.clipboard.writeText(appState.inviteCode);
            showNotification("Copied!", "success");
        }

        // Render All
        function renderAll() {
            renderBooks();
            renderBorrowed();
            renderMembers();
            renderTeachers();
            renderFurniture();
            renderWallpapers();
            updateDashboard();
        }

        // Initialize
        function initApp() {
            createParticles();

            // Load saved state
            const saved = localStorage.getItem('schoolSystemV6');
            if (saved) {
                try { Object.assign(appState, JSON.parse(saved)); } catch (e) {}
            }

            // Default data
            if (!appState.books.length) appState.books = [
                { title: "Mathematics Form 1", type: "Textbook", quantity: 50 },
                { title: "English Novel", type: "Novel", quantity: 30 },
                { title: "Science Textbook", type: "Textbook", quantity: 40 }
            ];
            if (!appState.members.length) appState.members = [
                { name: "John Doe", id: "MEM-001" },
                { name: "Jane Smith", id: "MEM-002" }
            ];
            if (!appState.teachers.length) appState.teachers = [
                { name: "Mr. Johnson", subject: "Mathematics", duty: "Form 1" },
                { name: "Ms. Williams", subject: "English", duty: "Form 2" }
            ];

            saveState();

            // Check login
            if (appState.currentUser) {
                document.getElementById('startupPage').classList.add('hidden');
                document.getElementById('mainApp').classList.remove('hidden');
                document.getElementById('schoolHeader').textContent = appState.orgName;
                document.getElementById('userInfo').innerHTML = `👤 ${appState.currentUser.name} <span class="role-badge role-${appState.currentRole}">${appState.currentRole}</span>`;
                document.getElementById('dashboardInviteCode').textContent = appState.inviteCode || '------';
                renderAll();
            }

            // Set dates
            const today = new Date().toISOString().split('T')[0];
            const returnDate = new Date();
            returnDate.setDate(returnDate.getDate() + 14);
            document.getElementById('issueDate').value = today;
            document.getElementById('issueReturnDate').value = returnDate.toISOString().split('T')[0];
            document.getElementById('furnitureDate').value = today;

            // Button listeners
            document.getElementById('btnLogin').addEventListener('click', () => showStartupForm('login'));
            document.getElementById('btnSignup').addEventListener('click', () => showStartupForm('signup'));
            document.getElementById('btnCreate').addEventListener('click', () => showStartupForm('create'));
            document.getElementById('btnCopyCode').addEventListener('click', copyDashboardCode);

            // Load wallpaper
            const savedWallpaper = localStorage.getItem('wallpaper');
            if (savedWallpaper) {
                document.body.style.backgroundImage = `url('${savedWallpaper}')`;
            }

            console.log('🏫 SRMS v7.0 by WeGEM | Ready');
        }

        // Expose functions
        window.showStartupForm = showStartupForm;
        window.handleLogin = handleLogin;
        window.handleSignup = handleSignup;
        window.handleCreate = handleCreate;
        window.handleForgotPassword = handleForgotPassword;
        window.showSection = showSection;
        window.deleteBook = deleteBook;
        window.returnBook = returnBook;
        window.filterBorrowed = filterBorrowed;
        window.returnFurniture = returnFurniture;
        window.deleteMember = deleteMember;
        window.deleteTeacher = deleteTeacher;
        window.selectChatUser = selectChatUser;
        window.sendChatMessage = sendChatMessage;
        window.insertEmoji = insertEmoji;
        window.setWallpaper = setWallpaper;
        window.generateQR = generateQR;
        window.formatDoc = formatDoc;
        window.saveNotes = saveNotes;
        window.recoverPassword = recoverPassword;
        window.copyDashboardCode = copyDashboardCode;
        window.logout = logout;
        window.clearAllData = clearAllData;
        window.exportData = exportData;

        initApp();
    </script>
</body>
</html>
