import streamlit as st
import pandas as pd
import os

# -----------------------------
# Project Paths
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

CSV_FILE = os.path.join(DATA_DIR, "candidates.csv")

# -----------------------------
# Streamlit Config
# -----------------------------

st.set_page_config(
    page_title="Smart Placement ATS",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------

st.title("📄 Smart Placement & Resume Screening Engine")

st.subheader("AI Powered Applicant Tracking System")

st.write("Welcome to your ATS Project!")

st.success("Day 35 Completed Successfully 🚀")

# Debug (Later remove these lines)
st.write("Current Working Directory:")
st.write(os.getcwd())

st.write("CSV File Path:")
st.write(CSV_FILE)

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("📄 Smart Placement ATS")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👤 Add Candidate",
        "📋 View Candidates",
        "🔍 Search Candidate",
        "🗑 Delete Candidate",
        "🏆 Ranking",
        "📊 Analytics",
        "📄 Project Report",
        "📤 Upload Resume",
        "⚙ Settings"
    ]
)

# -----------------------------
# Dashboard
# -----------------------------

if menu == "🏠 Dashboard":

    st.header("🏠 Dashboard")

    st.info("Welcome to Smart Placement ATS")

# -----------------------------
# Add Candidate
# -----------------------------

elif menu == "👤 Add Candidate":

    st.header("➕ Add Candidate")

    name = st.text_input("Candidate Name")

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=60
    )

    education = st.selectbox(
        "Education",
        [
            "B.Tech",
            "BCA",
            "MCA",
            "B.Sc",
            "M.Tech"
        ]
    )

    experience = st.number_input(
        "Experience (Years)",
        min_value=0,
        max_value=40
    )

    skills = st.text_area(
        "Skills (Comma Separated)"
    )

    submit = st.button("Add Candidate")

    if submit:

        new_candidate = {
            "Name": name,
            "Age": age,
            "Education": education,
            "Experience": experience,
            "Skills": skills
        }

        if os.path.exists(CSV_FILE):

            df = pd.read_csv(CSV_FILE)

        else:

            df = pd.DataFrame(
                columns=[
                    "Name",
                    "Age",
                    "Education",
                    "Experience",
                    "Skills"
                ]
            )

        df = pd.concat(
            [
                df,
                pd.DataFrame([new_candidate])
            ],
            ignore_index=True
        )

        # Save CSV
        df.to_csv(CSV_FILE, index=False)

        st.success("Candidate Saved Successfully ✅")
        st.write("Rows in DataFrame:", len(df))
        st.write(df)
# -----------------------------
# View Candidates
# -----------------------------

elif menu == "📋 View Candidates":

    st.header("📋 All Candidates")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        st.dataframe(
            df,
            width="stretch"
        )

    else:

        st.warning("No Candidate Data Found.")
elif menu == "🔍 Search Candidate":

    st.header("🔍 Search Candidate")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        search_name = st.text_input("Enter Candidate Name")

        if search_name:

            result = df[
                df["Name"].str.lower() == search_name.lower()
            ]

            if not result.empty:

                st.success("Candidate Found ✅")

                st.dataframe(result, width="stretch")

            else:

                st.error("Candidate Not Found ❌")

    else:

        st.warning("No Candidate Data Found.")
elif menu == "🗑 Delete Candidate":

    st.header("🗑 Delete Candidate")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        candidate = st.selectbox(
            "Select Candidate",
            df["Name"]
        )

        if st.button("Delete Candidate"):

            df = df[df["Name"] != candidate]

            df.to_csv(CSV_FILE, index=False)

            st.success("Candidate Deleted Successfully ✅")

            st.rerun()

    else:

        st.warning("No Candidate Data Found.")
