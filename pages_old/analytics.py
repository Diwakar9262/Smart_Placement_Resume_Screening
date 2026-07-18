import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


def analytics_page(CSV_FILE):

    st.header("📊 ATS Analytics Dashboard")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        st.metric(
            "Total Candidates",
            len(df)
        )

        avg_age = round(df["Age"].mean(), 1)
        avg_experience = round(df["Experience"].mean(), 1)

        st.metric(
            "Average Age",
            avg_age
        )

        st.metric(
            "Average Experience",
            avg_experience
        )

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