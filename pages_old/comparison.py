import streamlit as st
import pandas as pd
import os


def candidate_comparison_page(CSV_FILE):

    st.header("⚖ Candidate Comparison")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        col1, col2 = st.columns(2)

        with col1:
            candidate1 = st.selectbox(
                "Candidate 1",
                df["Name"],
                key="c1"
            )

        with col2:
            candidate2 = st.selectbox(
                "Candidate 2",
                df["Name"],
                key="c2"
            )

        if candidate1 == candidate2:
            st.warning("⚠ Please select two different candidates.")
            st.stop()

        row1 = df[df["Name"] == candidate1].iloc[0]
        row2 = df[df["Name"] == candidate2].iloc[0]

        comparison = pd.DataFrame({
            "Feature": [
                "Age",
                "Education",
                "Experience",
                "Skills"
            ],
            candidate1: [
                str(row1["Age"]),
                row1["Education"],
                str(row1["Experience"]),
                row1["Skills"]
            ],
            candidate2: [
                str(row2["Age"]),
                row2["Education"],
                str(row2["Experience"]),
                row2["Skills"]
            ]
        })

        st.subheader("⚖ Candidate Comparison")

        st.dataframe(
            comparison,
           width="stretch"
        )

        score1 = min(
            len(str(row1["Skills"]).split(",")) * 10,
            100
        )

        score2 = min(
            len(str(row2["Skills"]).split(",")) * 10,
            100
        )

        st.subheader("⭐ Resume Scores")

        c1, c2 = st.columns(2)

        c1.metric(candidate1, score1)
        c2.metric(candidate2, score2)

        st.subheader("🏆 Recommendation")

        if score1 > score2:
            st.success(f"{candidate1} is the Better Candidate 🏆")

        elif score2 > score1:
            st.success(f"{candidate2} is the Better Candidate 🏆")

        else:
            st.info("Both Candidates are Equal")

        difference = abs(score1 - score2)

        st.write(f"📌 Score Difference: {difference} points")

        st.subheader("💼 Experience Comparison")

        col1, col2 = st.columns(2)

        col1.metric(
            candidate1,
            f"{row1['Experience']} Years"
        )

        col2.metric(
            candidate2,
            f"{row2['Experience']} Years"
        )

        st.subheader("🎂 Age Comparison")

        col1, col2 = st.columns(2)

        col1.metric(
            candidate1,
            f"{row1['Age']} Years"
        )

        col2.metric(
            candidate2,
            f"{row2['Age']} Years"
        )

        st.subheader("🎓 Education")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**{candidate1}**")
            st.write(row1["Education"])

        with col2:
            st.write(f"**{candidate2}**")
            st.write(row2["Education"])

        st.subheader("🛠 Skills Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"### {candidate1}")
            st.write(row1["Skills"])

        with col2:
            st.write(f"### {candidate2}")
            st.write(row2["Skills"])

    else:
        st.warning("No Candidate Data Found.")