import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import pdfplumber

# -----------------------------
# Skill Database
# -----------------------------

SKILL_DATABASE = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "mysql",
    "git",
    "github",
    "numpy",
    "pandas",
    "matplotlib",
    "streamlit",
    "machine learning",
    "data structures",
    "oop",
    "html",
    "css",
    "javascript"
]

# -----------------------------
# Resume Parser
# -----------------------------

def parse_resume(text):

    lines = text.split("\n")

    name = lines[0] if len(lines) > 0 else "Not Found"

    education = "Not Found"

    for line in lines:

        if "b.tech" in line.lower():
            education = line

        elif "bca" in line.lower():
            education = line

        elif "mca" in line.lower():
            education = line

    found_skills = []

    lower_text = text.lower()

    for skill in SKILL_DATABASE:

        if skill in lower_text:
            found_skills.append(skill)

    score = len(found_skills) * 5

    if score > 100:
        score = 100

    return name, education, found_skills, score
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

elif menu == "🏆 Ranking":

    st.header("🏆 Candidate Ranking")

    def calculate_score(row):

        skills = str(row["Skills"]).split(",")

        skill_score = len(skills) * 10

        experience_score = row["Experience"] * 5

        return skill_score + experience_score

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        df["Score"] = df.apply(calculate_score, axis=1)

        df = df.sort_values(
            by="Score",
            ascending=False
        )

        df.insert(
            0,
            "Rank",
            range(1, len(df)+1)
        )

        st.dataframe(
            df,
            width="stretch"
        )

    else:

        st.warning("No Candidate Data Found.")

elif menu == "📊 Analytics":

    st.header("📊 Analytics Dashboard")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        total_candidates = len(df)

        avg_age = round(df["Age"].mean(), 1)

        avg_experience = round(df["Experience"].mean(), 1)

        st.metric("Total Candidates", total_candidates)

        st.metric("Average Age", avg_age)

        st.metric("Average Experience", avg_experience)
        education_count = df["Education"].value_counts()

        fig, ax = plt.subplots()

        ax.bar(
            education_count.index,
            education_count.values
        )

        ax.set_title("Education Distribution")

        st.pyplot(fig)
        experience_count = df["Experience"].value_counts()

        fig2, ax2 = plt.subplots()

        ax2.bar(
            experience_count.index.astype(str),
            experience_count.values
        )

        ax2.set_title("Experience Distribution")

        st.pyplot(fig2)

    else:

        st.warning("No Candidate Data Found.")
elif menu == "📤 Upload Resume":

    st.header("📤 Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose Resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        upload_folder = "uploads"

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        save_path = os.path.join(
            upload_folder,
            uploaded_file.name
        )

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("Resume Uploaded Successfully ✅")

        st.subheader("Extracted Resume Text")

        text = ""

        with pdfplumber.open(save_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        st.text_area(
            "Resume Content",
            text,
            height=400
        )
        name, education, skills, score = parse_resume(text)

        st.divider()

        st.subheader("AI Resume Analysis")

        st.write("👤 Name :", name)

        st.write("🎓 Education :", education)

        st.write("💻 Skills :", ", ".join(skills))

        st.write("⭐ Resume Score :", score, "/100")