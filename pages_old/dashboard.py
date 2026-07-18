import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


def dashboard_page(CSV_FILE):

    if not st.session_state.get("logged_in", False):

        st.warning("🔒 Please Login First")

        st.stop()

    st.header("🏠 ATS Dashboard")

    st.markdown("""
    ### 👋 Welcome Administrator

    Manage candidates, screen resumes and analyze recruitment data from one dashboard.
    """)

    col1, col2, col3 = st.columns(3)

    col1.success("📄 Resume Screening")
    col2.success("👤 Candidate Management")
    col3.success("📊 Analytics Dashboard")

    if os.path.exists(CSV_FILE):

        filtered_df = pd.read_csv(CSV_FILE)

        st.sidebar.subheader("🔍 Dashboard Filters")

        education_filter = st.sidebar.multiselect(
            "Education",
            options=filtered_df["Education"].unique(),
            default=filtered_df["Education"].unique()
        )

        experience_filter = st.sidebar.slider(
            "Minimum Experience",
            0,
            int(filtered_df["Experience"].max()),
            0
        )

        skill_filter = st.sidebar.text_input(
            "Search Skill"
        )

        filtered_df = filtered_df[
            (filtered_df["Education"].isin(education_filter)) &
            (filtered_df["Experience"] >= experience_filter)
        ]

        if skill_filter:

            filtered_df = filtered_df[
                filtered_df["Skills"]
                .str.lower()
                .str.contains(skill_filter.lower())
            ]

        if filtered_df.empty:

            st.warning("⚠ No Candidate Found!")

            st.stop()

        total_candidates = len(filtered_df)
        avg_age = round(filtered_df["Age"].mean(), 1)
        avg_exp = round(filtered_df["Experience"].mean(), 1)
        max_exp = filtered_df["Experience"].max()

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
            "🏆 Highest Experience",
            f"{max_exp} Years"
        )

        st.success(
            f"Showing {len(filtered_df)} Candidate(s)"
        )

        st.divider()

        left, right = st.columns(2)

        with left:

            st.subheader("🎓 Education Distribution")

            fig, ax = plt.subplots()

            filtered_df["Education"].value_counts().plot(
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

            filtered_df.plot(
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
            filtered_df.tail(5),
           width="stretch"
        )

        st.subheader("📈 Database Usage")

        progress = min(
            len(filtered_df) / 100,
            1.0
        )

        st.progress(progress)

        st.write(
            f"Progress: {progress * 100:.0f}%"
        )

        st.caption(
            f"{len(filtered_df)} / 100 Candidate Target"
        )

        st.divider()

        st.subheader("💡 Quick Insights")

        st.info(f"""
• Total Candidates : {len(filtered_df)}

• Highest Experience : {filtered_df['Experience'].max()} Years

• Average Experience : {round(filtered_df['Experience'].mean(),1)} Years

• Education Types : {filtered_df['Education'].nunique()}
""")

        st.download_button(
            label="📥 Download Filtered CSV",
            data=filtered_df.to_csv(index=False),
            file_name="Filtered_Candidates.csv",
            mime="text/csv"
        )

    else:

        st.info("No Candidate Data Available")