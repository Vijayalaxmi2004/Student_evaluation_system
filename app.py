import streamlit as st
import pandas as pd
from auth import init_db, authenticate, register_user, hash_password, reset_password
from student import student_dashboard
from faculty import faculty_dashboard

st.set_page_config(page_title="Student Evaluation System", layout="wide")
init_db()

# ---------- GLOBAL CSS ----------
def global_css():
    st.markdown("""
    <style>
    /* Full screen center */
    .stApp {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
        background: linear-gradient(135deg, #2b1055, #7597de);
        background-size: cover;
        animation: moveStars 200s linear infinite;
        color: white;
    }

    h1, h2, h3 { color: white !important; }

    /* Glass login card */
    .login-card {
        width: 380px;
        padding: 30px;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 50px rgba(0,0,0,0.4);
        text-align: center;
        animation: fadeIn 1.2s ease, slideUp 1s ease;
    }

    /* Profile card in sidebar */
    .profile-card {
        padding: 24px;
        border-radius: 24px;
        background: linear-gradient(135deg, #1f3ec6, #1e2d83);
        border: 2px solid rgba(255,255,255,0.25);
        box-shadow: 0 18px 38px rgba(0,0,0,0.35);
        color: white;
        margin-bottom: 20px;
    }

    .profile-card h2,
    .profile-card h3,
    .profile-card p,
    .profile-card .stText {
        color: white !important;
    }

    /* PROFILE UI no floating round button in dashboard */
    .profile-card {
        margin-top: 20px;
    }

    /* Profile card and sidebar button styling */
    .profile-card button,
    .profile-card .stButton>button,
    .stSidebar .profile-card button,
    .stSidebar .profile-card .stButton>button,
    div[data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
        font-weight: 700 !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.38) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        min-height: 60px !important;
        padding: 0.65rem 1rem !important;
    }

    .profile-card button:hover,
    .profile-card .stButton>button:hover,
    .stSidebar .profile-card button:hover,
    .stSidebar .profile-card .stButton>button:hover,
    div[data-testid="stSidebar"] button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 12px 26px rgba(118, 74, 162, 0.5) !important;
        background: linear-gradient(135deg, #5f72ff, #7b3fdd) !important;
    }

    /* Target ALL Form Submit Buttons */
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #ff8b00, #ff3d00) !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
        font-weight: 700 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(255, 61, 0, 0.3) !important;
        opacity: 1 !important;
        transition: 0.3s ease-in-out !important;
    }


    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 6px 20px rgba(255, 139, 0, 0.5) !important;
        background: linear-gradient(135deg, #ffb347, #ff416c) !important;
    }

    /* Tabs styling */
    button[data-baseweb="tab"] {
        color: white !important;
    }
    button[aria-selected="true"] {
        border-bottom-color: #ff8b00 !important;
    }

    /* Input fields */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 8px !important;
    }
    label {
        color: white !important;
        font-weight: 500 !important;
    }

    /* Alerts */
    .stAlert {
        margin: 1rem auto;
        padding: 1rem 1.25rem;
        border-radius: 6px;
        font-size: 1rem;
        flex-shrink: 0;
        max-width: 600px;
        text-align: center;
    }
    .stAlert[data-baseweb="alert-success"] {
        background-color: #e6ffed;
        border: 1px solid #2ecc71;
        color: #2d7a46;
    }
    .stAlert[data-baseweb="alert-error"] {
        background-color: #ffe6e6;
        border: 1px solid #e74c3c;
        color: #7a2d2d;
    }
    .stAlert[data-baseweb="alert-info"] {
        background-color: #e6f7ff;
        border: 1px solid #3498db;
        color: #2d3a7a;
    }
    .stAlert[data-baseweb="alert-warning"] {
        background-color: #fff8e6;
        border: 1px solid #f39c12;
        color: #7a5a2d;
    }
    </style>
    """, unsafe_allow_html=True)


# ---------- Session State ----------
for key, default in [("logged_in", False), ("role", None), ("username", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ================= AFTER LOGIN =================
if st.session_state.logged_in:
    df = pd.read_csv("data/users_db.csv")
    user = df[df["username"].str.strip().str.lower() == st.session_state.username.strip().lower()]
    
    if user.empty:
        username, role, department = "Unknown", "Unknown", "Not Applicable"
    else:
        username, role = user.iloc[0]["username"], user.iloc[0]["role"]
        department = "Not Applicable" if role != "Student" else user.iloc[0].get("department", "Not Applicable")
    
    st.sidebar.markdown(f"<div class='profile-card'><h2>👤 My Profile</h2><p><strong>Username:</strong> {username}</p><p><strong>Role:</strong> {role}</p><p><strong>Department:</strong> {department}</p></div>", unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()
    
    (faculty_dashboard() if st.session_state.role == "Faculty" else student_dashboard())

# ================= LOGIN PAGE =================
else:
    global_css()
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h1>🎓 Student Evaluation System</h1>", unsafe_allow_html=True)
    st.markdown("<p>Please LOGIN or REGISTER below.</p>", unsafe_allow_html=True)

    tabs = st.tabs(["Login", "Register", "Reset"])

    # ---------- LOGIN ----------
    with tabs[0]:
        with st.form("login"):
            u = st.text_input("👤 Username / Roll No")
            p = st.text_input("🔒 Password", type="password")
            if st.form_submit_button("Login"):
                role = authenticate(u, p)
                if role:
                    st.session_state.logged_in = True
                    st.session_state.username = u.strip().lower()
                    st.session_state.role = role
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

    # ---------- REGISTER ----------
    with tabs[1]:
        with st.form("register"):
            u = st.text_input("👤 Choose Username")
            p = st.text_input("🔒 Password", type="password")
            r = st.selectbox("🎓 Role", ["Student", "Faculty"])

            if r == "Student":
                dept = st.selectbox("🏫 Department", ["CSE", "ECE", "EEE", "MECH", "CIVIL", "IT", "CSE-DS", "CSE-CS", "AIML"])
            else:
                st.text_input("🏫 Department (Faculty not required)", value="Not Applicable", disabled=True)
                dept = "Not Applicable"

            if st.form_submit_button("Register"):
                ok, msg = register_user(u, p, r, dept)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
    # ---------- RESET ----------
    with tabs[2]:
        with st.form("reset"):
            u = st.text_input("👤 Username")
            p = st.text_input("🔑 New Password", type="password")
            if st.form_submit_button("Reset"):
                new_pwd = reset_password(u, p) if p else reset_password(u)
                st.success("✅ Password updated") if new_pwd else st.error("❌ User not found")