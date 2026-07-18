import streamlit as st
import pandas as pd
import pdfplumber
import os
from datetime import datetime


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
# Job Matching
# -----------------------------
def match_resume(job_description, resume_skills):

    jd = job_description.lower()

    required_skills = []

    for skill in SKILL_DATABASE:

        if skill in jd:
            required_skills.append(skill)

    matched = []
    missing = []

    for skill in required_skills:

        if skill in resume_skills:
            matched.append(skill)

        else:
            missing.append(skill)

    if len(required_skills) == 0:

        percentage = 0

    else:

        percentage = int(
            len(matched) /
            len(required_skills) * 100
        )

    return percentage, matched, missing


# -----------------------------
# AI Recommendation
# -----------------------------
def hiring_recommendation(score, match_percentage):

    if score >= 80 and match_percentage >= 80:
        return "✅ Shortlist Candidate"

    elif score >= 60 and match_percentage >= 60:
        return "🟡 Needs Improvement"

    else:
        return "❌ Reject Candidate"


# -----------------------------
# Resume Upload Page
# -----------------------------
def resume_upload_page(BASE_DIR, HISTORY_FILE):

    st.header("📤 Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose Resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        upload_folder = os.path.join(
            BASE_DIR,
            "uploads"
        )

        os.makedirs(upload_folder, exist_ok=True)

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

        history = {
            "Candidate": name,
            "File Name": uploaded_file.name,
            "Upload Time": datetime.now().strftime("%d-%m-%Y %H:%M")
        }

        if os.path.exists(HISTORY_FILE):

            history_df = pd.read_csv(HISTORY_FILE)

        else:

            history_df = pd.DataFrame(
                columns=[
                    "Candidate",
                    "File Name",
                    "Upload Time"
                ]
            )

        history_df = pd.concat(
            [
                history_df,
                pd.DataFrame([history])
            ],
            ignore_index=True
        )

        history_df.to_csv(
            HISTORY_FILE,
            index=False
        )

        st.divider()

        st.subheader("AI Resume Analysis")

        st.write("👤 Name :", name)
        st.write("🎓 Education :", education)
        st.write("💻 Skills :", ", ".join(skills))

        st.metric(
            "⭐ Resume Score",
            f"{score}/100"
        )

        st.divider()

        st.subheader("💼 Job Description Matching")

        job_description = st.text_area(
            "Paste Job Description"
        )

        if st.button("Match Resume"):

            percentage, matched, missing = match_resume(
                job_description,
                skills
            )

            st.write("✅ Matched Skills")
            st.write(matched)

            st.write("❌ Missing Skills")
            st.write(missing)

            st.progress(percentage / 100)

            st.success(
                f"Match Percentage : {percentage}%"
            )

            recommendation = hiring_recommendation(
                score,
                percentage
            )

            st.subheader("🤖 AI Recommendation")

            if "Shortlist" in recommendation:

                st.success(recommendation)

            elif "Needs" in recommendation:

                st.warning(recommendation)

            else:

                st.error(recommendation)