import streamlit as st
import pandas as pd
import os


def report_page(CSV_FILE):

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

        education_df = education.reset_index()
        education_df.columns = ["Education", "Count"]

        st.dataframe(
            education_df,
            width="stretch"
        )

        st.divider()

        st.subheader("💼 Experience Summary")

        st.write(f"**Highest Experience:** {highest_experience} Years")
        st.write(f"**Lowest Experience:** {lowest_experience} Years")

        st.divider()

        st.subheader("📋 Candidate List")

        st.dataframe(
            df,
            width="stretch"
        )

        st.divider()

        st.success("✅ Report Generated Successfully")

    else:

        st.warning("No Candidate Data Found.")