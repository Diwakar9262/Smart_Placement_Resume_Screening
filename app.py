import streamlit as st
import os

# -----------------------------
# Import Pages
# -----------------------------
from pages_old.login import login_page
from pages_old.dashboard import dashboard_page
from pages_old.candidate import (
    add_candidate_page,
    view_candidate_page,
    search_candidate_page,
    delete_candidate_page,
    edit_candidate_page
)
from pages_old.analytics import analytics_page
from pages_old.report import report_page
from pages_old.export import (
    export_excel_page,
    export_pdf_page
)
from pages_old.profile import candidate_profile_page
from pages_old.comparison import candidate_comparison_page
from pages_old.performance import candidate_performance_page
from pages_old.history import history_page
from pages_old.resume_upload import resume_upload_page
from pages_old.settings import settings_page
from pages_old.ranking import ranking_page
from pages_old.change_password import change_password_page
from pages_old.register import register_page
# -----------------------------
# Project Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

CSV_FILE = os.path.join(DATA_DIR, "candidates.csv")
HISTORY_FILE = os.path.join(DATA_DIR, "resume_history.csv")
USERS_FILE = os.path.join(DATA_DIR, "users.csv")

# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(
    page_title="Smart Placement ATS",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Session
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# -----------------------------
# Login First
# -----------------------------
if not st.session_state.logged_in:

    login_page(USERS_FILE)
    st.stop()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🚀 Smart Placement ATS")

st.sidebar.success(f"👤 {st.session_state.username}")
st.sidebar.info(f"Role : {st.session_state.role}")

# -----------------------------
# Admin Menu
# -----------------------------
if st.session_state.role == "Admin":

    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👤 Candidate",
            "🏆 Ranking",
            "📊 Analytics",
            "📄 Report",
            "📥 Export",
            "📄 Profile",
            "⚖ Comparison",
            "📈 Performance",
            "📜 History",
            "📤 Resume Upload",
            "⚙ Settings"
        ]
    )

# -----------------------------
# Candidate Menu
# -----------------------------
else:

    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📄 Profile",
            "📈 Performance",
            "📤 Resume Upload",
            "⚙ Settings"
        ]
    )

# -----------------------------
# Dashboard
# -----------------------------
if menu == "🏠 Dashboard":

    dashboard_page(CSV_FILE)

# -----------------------------
# Candidate
# -----------------------------
elif menu == "👤 Candidate":

    candidate_menu =  st.sidebar.radio(
        "Candidate Options",
        [
            "➕ Add Candidate",
            "📋 View Candidates",
            "🔍 Search Candidate",
            "🗑 Delete Candidate",
            "✏ Edit Candidate"
        ]
    )

    if candidate_menu == "➕ Add Candidate":
        add_candidate_page(CSV_FILE)

    elif candidate_menu == "📋 View Candidates":
        view_candidate_page(CSV_FILE)

    elif candidate_menu == "🔍 Search Candidate":
        search_candidate_page(CSV_FILE)

    elif candidate_menu == "🗑 Delete Candidate":
        delete_candidate_page(CSV_FILE)

    elif candidate_menu == "✏ Edit Candidate":
        edit_candidate_page(CSV_FILE)

# -----------------------------
# Ranking
# -----------------------------
elif menu == "🏆 Ranking":

    ranking_page(CSV_FILE)

# -----------------------------
# Analytics
# -----------------------------
elif menu == "📊 Analytics":

    analytics_page(CSV_FILE)

# -----------------------------
# Report
# -----------------------------
elif menu == "📄 Report":

    report_page(CSV_FILE)

# -----------------------------
# Export
# -----------------------------
elif menu == "📥 Export":

    export_menu = st.sidebar.selectbox(
        "Export Options",
        [
            "📥 Export Excel",
            "📄 Export PDF"
        ]
    )

    if export_menu == "📥 Export Excel":
        export_excel_page(CSV_FILE, DATA_DIR)

    else:
        export_pdf_page(CSV_FILE, DATA_DIR)

# -----------------------------
# Profile
# -----------------------------
elif menu == "📄 Profile":

    candidate_profile_page(CSV_FILE)

# -----------------------------
# Comparison
# -----------------------------
elif menu == "⚖ Comparison":

    candidate_comparison_page(CSV_FILE)

# -----------------------------
# Performance
# -----------------------------
elif menu == "📈 Performance":

    candidate_performance_page(CSV_FILE)

# -----------------------------
# History
# -----------------------------
elif menu == "📜 History":

    history_page(HISTORY_FILE)

# -----------------------------
# Resume Upload
# -----------------------------
elif menu == "📤 Resume Upload":

    resume_upload_page(BASE_DIR, HISTORY_FILE)

# -----------------------------
# Settings
# -----------------------------
elif menu == "⚙ Settings":
    setting_menu = st.sidebar.radio(
        "Settings",
        [
            "General Settings",
            "Change Password"
        ]
    )

    if setting_menu == "General Settings":
        settings_page(CSV_FILE, HISTORY_FILE)
    elif setting_menu == "Change Password":
        change_password_page(USERS_FILE)