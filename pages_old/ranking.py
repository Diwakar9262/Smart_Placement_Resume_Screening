import streamlit as st
import pandas as pd
import os


def ranking_page(CSV_FILE):

    st.header("🏆 Candidate Ranking")

    def calculate_score(row):

        skills = str(row["Skills"]).split(",")

        skill_score = len(skills) * 10

        experience_score = row["Experience"] * 5

        return skill_score + experience_score

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        df["Score"] = df.apply(
            calculate_score,
            axis=1
        )

        df = df.sort_values(
            by="Score",
            ascending=False
        )

        df.insert(
            0,
            "Rank",
            range(1, len(df) + 1)
        )

        st.dataframe(
            df,
            width="stretch"
        )

    else:

        st.warning("No Candidate Data Found.")