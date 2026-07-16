import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import pdfplumber
from openpyxl import Workbook
from reportlab.pdfgen import canvas
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
            len(required_skills)
            *100
        )

    return percentage, matched, missing
def hiring_recommendation(score, match_percentage):

    if score >= 80 and match_percentage >= 80:
        return "✅ Shortlist Candidate"

    elif score >= 60 and match_percentage >= 60:
        return "🟡 Needs Improvement"

    else:
        return "❌ Reject Candidate"
# -----------------------------
# Project Paths
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

CSV_FILE = os.path.join(DATA_DIR, "candidates.csv")
HISTORY_FILE = os.path.join(DATA_DIR, "resume_history.csv")


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
        "✏ Edit Candidate",
        "🏆 Ranking",
        "📊 Analytics",
        "📄 Project Report",
        "📥 Export Excel",
        "📄 Export PDF",
        "📄 Candidate Profile",
        "📜 Resume History",
        "📤 Upload Resume",
        "⚙ Settings"
    ]
)

# -----------------------------
# Dashboard
# -----------------------------

if menu == "🏠 Dashboard":

    st.header("🏠 ATS Dashboard")

    st.markdown("### Welcome to Smart Placement ATS")
       
    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        total_candidates = len(df)
        avg_age = round(df["Age"].mean(), 1)
        avg_exp = round(df["Experience"].mean(), 1)
        max_exp = df["Experience"].max()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "👥 Candidates",
            total_candidates
        )

        c2.metric(
            "💼 Avg Experience",
            avg_exp
        )

        c3.metric(
            "🎂 Avg Age",
            avg_age
        )

        c4.metric(
            "🏆 Highest Exp",
            max_exp
        )
        st.divider()
        left, right = st.columns(2)
        with left:

            st.subheader("🎓 Education Distribution")

            fig, ax = plt.subplots()

            df["Education"].value_counts().plot(
                kind="pie",
                autopct="%1.1f%%",
                ax=ax
            )

            ax.set_ylabel("")

            st.pyplot(fig)

            plt.close(fig)
        with right:

            st.subheader("💼 Experience")

            fig, ax = plt.subplots()

            df.plot(
                x="Name",
                y="Experience",
                kind="bar",
                ax=ax,
                legend=False
            )

            ax.set_title("Candidate Experience")
            ax.set_xlabel("Candidates")
            ax.set_ylabel("Experience (Years)")

            plt.xticks(rotation=30)

            st.pyplot(fig)

            plt.close(fig)
        st.divider()

        st.subheader("🆕 Recently Added Candidates")

        st.dataframe(
            df.tail(5),

            width="stretch"

        )
        st.subheader("📈 Database Usage")

        progress = min(

            len(df) / 100,

            1.0

        )

        st.progress(progress)

        st.write(
            f"Progress: {progress*100:.0f}%"
        )

        st.caption(
            f"{len(df)} / 100 Candidate Target"
        )
        st.divider()

        st.subheader("💡 Quick Insights")

        st.info(f"""
            • Total Candidates : {len(df)}

            • Highest Experience : {df['Experience'].max()} Years

            • Average Experience : {round(df['Experience'].mean(),1)} Years

            • Education Types : {df['Education'].nunique()}
            """
        )
    else:

        st.info("No Candidate Data Available")

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

        if not name.strip():

            st.error("❌ Please enter candidate name.")

        elif not skills.strip():

            st.error("❌ Please enter candidate skills.")

        else:
            # Duplicate Candidate Check

            if os.path.exists(CSV_FILE):

                df = pd.read_csv(CSV_FILE)

                duplicate = df[
                    df["Name"].str.lower() == name.lower()
                ]

                if not duplicate.empty:

                    st.error("❌ Candidate already exists.")

                    st.stop()

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

            df.to_csv(CSV_FILE, index=False)

            st.success("✅ Candidate Saved Successfully")
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
elif menu == "✏ Edit Candidate":

    st.header("✏ Edit Candidate")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        candidate = st.selectbox(
            "Select Candidate",
            df["Name"]
        )

        row_index = df[df["Name"] == candidate].index[0]

        row = df.loc[row_index]

        new_name = st.text_input(
            "Candidate Name",
            value=row["Name"]
        )

        new_age = st.number_input(
            "Age",
            min_value=18,
            max_value=60,
            value=int(row["Age"])
        )

        education_options = [
            "B.Tech",
            "BCA",
            "MCA",
            "B.Sc",
            "M.Tech"
        ]

        current_index = education_options.index(row["Education"])

        new_education = st.selectbox(
            "Education",
            education_options,
            index=current_index
        )

        new_experience = st.number_input(
            "Experience",
            min_value=0,
            max_value=40,
            value=int(row["Experience"])
        )

        new_skills = st.text_area(
            "Skills",
            value=row["Skills"]
        )

        if st.button("Update Candidate"):

            if not new_name.strip():

                st.error("❌ Candidate name cannot be empty.")

            elif not new_skills.strip():

                st.error("❌ Skills cannot be empty.")

            else:

                df.loc[row_index, "Name"] = new_name
                df.loc[row_index, "Age"] = new_age
                df.loc[row_index, "Education"] = new_education
                df.loc[row_index, "Experience"] = new_experience
                df.loc[row_index, "Skills"] = new_skills

                df.to_csv(CSV_FILE, index=False)

                st.success("✅ Candidate Updated Successfully")

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

    st.header("📊 ATS Analytics Dashboard")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        st.metric(
            "Total Candidates",
            len(df)
        )
        avg_age = round(df["Age"].mean(), 1)

        avg_experience = round(df["Experience"].mean(), 1)

        st.metric("Average Age", avg_age)

        st.metric("Average Experience", avg_experience)

        st.subheader("Candidate Data")

        st.dataframe(
            df,
            width="stretch"
        )

        st.subheader("Education Distribution")

        edu_counts = df["Education"].value_counts()

        fig, ax = plt.subplots()

        ax.bar(
            edu_counts.index,
            edu_counts.values
        )

        plt.xticks(rotation=20)

        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Age Distribution")

        fig2, ax2 = plt.subplots()

        ax2.hist(
            df["Age"],
            bins=5
        )

        st.pyplot(fig2)
        plt.close(fig2)      
    else:

        st.warning("No Candidate Data Found.")
elif menu == "📄 Project Report":

    st.header("📄 Smart Placement ATS Report")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        total_candidates = len(df)

        avg_age = round(df["Age"].mean(), 1)

        avg_experience = round(df["Experience"].mean(), 1)

        highest_experience = df["Experience"].max()

        lowest_experience = df["Experience"].min()

        st.subheader("📊 Overall Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Candidates", total_candidates)

        with col2:
            st.metric("Average Age", avg_age)

        with col3:
            st.metric("Average Experience", avg_experience)

        st.divider()

        st.subheader("🎓 Education Distribution")

        education = df["Education"].value_counts()

        st.dataframe(
            education.reset_index().rename(
                columns={
                    "index": "Education",
                    "Education": "Count"
                }
            ),
            width="stretch"
        )

        st.divider()

        st.subheader("💼 Experience Summary")

        st.write(f"Highest Experience : **{highest_experience} Years**")

        st.write(f"Lowest Experience : **{lowest_experience} Years**")

        st.divider()

        st.subheader("📋 Candidate List")

        st.dataframe(df, width="stretch")

        st.divider()

        st.success("✅ Report Generated Successfully")

    else:

        st.warning("No Candidate Data Found.")
elif menu == "📥 Export Excel":

    st.header("📥 Export Candidates to Excel")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        if st.button("Generate Excel File"):

            workbook = Workbook()

            sheet = workbook.active

            sheet.title = "Candidates"

            sheet.append(df.columns.tolist())

            for row in df.values.tolist():

                sheet.append(row)

            excel_file = os.path.join(
                DATA_DIR,
                "Candidates_Report.xlsx"
            )

            workbook.save(excel_file)

            st.success("✅ Excel File Generated Successfully")

            with open(excel_file, "rb") as file:

                st.download_button(
                    label="📥 Download Excel Report",
                    data=file,
                    file_name="Candidates_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    else:

        st.warning("No Candidate Data Found.")
elif menu == "📄 Export PDF":

    st.header("📄 Export ATS Report")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        if st.button("Generate PDF Report"):

            pdf_file = os.path.join(
                DATA_DIR,
                "ATS_Report.pdf"
            )

            c = canvas.Canvas(pdf_file)

            c.setFont("Helvetica-Bold", 18)
            c.drawString(
                150,
                800,
                "Smart Placement ATS Report"
            )

            c.setFont("Helvetica", 12)

            c.drawString(
                50,
                770,
                f"Total Candidates : {len(df)}"
            )

            y = 740

            c.drawString(
                50,
                y,
                "Candidate List"
            )

            y -= 20

            for index, row in df.iterrows():

                line = (
                    f"{row['Name']} | "
                    f"{row['Education']} | "
                    f"{row['Experience']} Years"
                )

                c.drawString(
                    50,
                    y,
                    line
                )

                y -= 20

                if y < 50:

                    c.showPage()

                    y = 800

            c.save()

            st.success("✅ PDF Generated Successfully")

            with open(pdf_file, "rb") as pdf:

                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf,
                    file_name="ATS_Report.pdf",
                    mime="application/pdf"
                )

    else:

        st.warning("No Candidate Data Found.")
elif menu == "📄 Candidate Profile":

    st.header("📄 Candidate Profile")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        candidate = st.selectbox(
            "Select Candidate",
            df["Name"]
        )

        profile = df[df["Name"] == candidate]

        if not profile.empty:

            row = profile.iloc[0]

            st.subheader("👤 Candidate Details")

            st.write("**Name:**", row["Name"])
            st.write("**Age:**", row["Age"])
            st.write("**Education:**", row["Education"])
            st.write("**Experience:**", row["Experience"], "Years")
            st.write("**Skills:**", row["Skills"])

            skills = str(row["Skills"]).split(",")

            score = min(len(skills) * 10, 100)

            st.subheader("⭐ Resume Score")

            st.progress(score / 100)

            st.success(f"{score}/100")

    else:

        st.warning("No Candidate Data Found.")
elif menu == "📤 Upload Resume":

    st.header("📤 Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose Resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        upload_folder = os.path.join(BASE_DIR, "uploads")

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

        st.write("⭐ Resume Score :", score, "/100")
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

            st.progress(percentage/100)

            st.success(f"Match Percentage : {percentage}%")
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
elif menu == "📜 Resume History":

    st.header("📜 Resume Upload History")

    if os.path.exists(HISTORY_FILE):

        history_df = pd.read_csv(HISTORY_FILE)

        st.dataframe(
            history_df,
            width="stretch"
        )

    else:

        st.warning("No Resume History Found.")
# -----------------------------
# Settings
# -----------------------------

elif menu == "⚙ Settings":

    st.header("⚙ ATS Settings")

    st.subheader("Application Information")

    st.write("**Project Name:** Smart Placement & Resume Screening Engine")
    st.write("**Version:** 1.0")
    st.write("**Developer:** Diwakar Kumar Upadhayay")
    st.write("**Framework:** Streamlit")
    st.write("**Language:** Python")

    st.divider()

    st.subheader("Theme")

    st.info(
        "Theme selection is for demonstration. "
        "Change actual theme from Streamlit Settings."
    )
    st.divider()

    st.subheader("Data Information")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        st.write(f"👥 Total Candidates : {len(df)}")

    else:

        st.write("👥 Total Candidates : 0")

    if os.path.exists(HISTORY_FILE):

        history_df = pd.read_csv(HISTORY_FILE)

        st.write(f"📄 Uploaded Resumes : {len(history_df)}")

    else:

        st.write("📄 Uploaded Resumes : 0")

    st.divider()

    if st.button("🗑 Clear Resume History"):

        if os.path.exists(HISTORY_FILE):

            os.remove(HISTORY_FILE)

            st.success("Resume History Cleared Successfully ✅")

        else:

            st.warning("Resume History Not Found.")

    st.divider()

    st.success("Settings Loaded Successfully ✅")