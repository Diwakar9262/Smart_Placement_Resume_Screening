import streamlit as st
import pandas as pd
import os
# -----------------------------
# Candidate Profile
# -----------------------------
def candidate_profile_page(CSV_FILE):

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
