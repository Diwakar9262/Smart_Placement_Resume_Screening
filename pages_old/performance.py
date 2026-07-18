import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


# -----------------------------
# Candidate Performance
# -----------------------------
def candidate_performance_page(CSV_FILE):

    st.header("📈 Candidate Performance Dashboard")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        # Resume Score Calculation
        def calculate_score(row):

            score = 0

            # Skills Score
            score += min(
                len(str(row["Skills"]).split(",")) * 10,
                50
            )

            # Experience Score
            score += min(
                row["Experience"] * 15,
                30
            )

            # Education Score
            if row["Education"] == "B.Tech":

                score += 20

            elif row["Education"] == "MCA":

                score += 15

            else:

                score += 10

            return min(score, 100)

        df["Resume Score"] = df.apply(
            calculate_score,
            axis=1
        )

        # Sort by Resume Score
        df = df.sort_values(
            by="Resume Score",
            ascending=False
        )

        df.insert(
            0,
            "Rank",
            range(1, len(df) + 1)
        )

        top_candidate = df.iloc[0]

        st.subheader("🏆 Top Performer")

        st.success(
            f"{top_candidate['Name']} "
            f"({top_candidate['Resume Score']}/100)"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "🏆 Highest Resume Score",
            top_candidate["Resume Score"]
        )

        c2.metric(
            "⭐ Average Resume Score",
            round(df["Resume Score"].mean(), 1)
        )

        c3.metric(
            "💼 Average Experience",
            f"{round(df['Experience'].mean(),1)} Years"
        )

        st.divider()

        # Resume Score Chart
        st.subheader("📊 Resume Score Chart")

        fig, ax = plt.subplots()

        df.plot(
            x="Name",
            y="Resume Score",
            kind="bar",
            ax=ax,
            legend=False,
            color="green"
        )

        ax.set_title("Resume Score Comparison")
        ax.set_xlabel("Candidates")
        ax.set_ylabel("Resume Score")

        plt.xticks(rotation=30)

        st.pyplot(fig)

        plt.close(fig)

        st.divider()

        # Experience Chart
        st.subheader("💼 Experience Chart")

        fig, ax = plt.subplots()

        df.plot(
            x="Name",
            y="Experience",
            kind="bar",
            ax=ax,
            legend=False,
            color="orange"
        )

        ax.set_title("Experience Comparison")
        ax.set_xlabel("Candidates")
        ax.set_ylabel("Experience (Years)")

        plt.xticks(rotation=30)

        st.pyplot(fig)

        plt.close(fig)

        st.divider()

        st.success(
            f"Showing {len(df)} Candidates"
        )

        st.subheader("📋 Candidate Performance Table")

        st.dataframe(
            df[
                [
                    "Rank",
                    "Name",
                    "Education",
                    "Experience",
                    "Resume Score"
                ]
            ],
            width="stretch"
        )

        st.divider()

        st.subheader("⭐ Performance Level")

        for _, row in df.iterrows():

            if row["Resume Score"] >= 80:

                st.success(
                    f"🏆 {row['Name']} : Excellent"
                )

            elif row["Resume Score"] >= 60:

                st.warning(
                    f"🟡 {row['Name']} : Good"
                )

            else:

                st.error(
                    f"🔴 {row['Name']} : Needs Improvement"
                )

    else:

        st.warning("No Candidate Data Found.")