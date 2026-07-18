import streamlit as st
import pandas as pd
import os


def settings_page(CSV_FILE, HISTORY_FILE):

    st.header("⚙ ATS Settings")

    # -----------------------------
    # Theme
    # -----------------------------

    if "theme" not in st.session_state:
        st.session_state.theme = "Light"

    st.subheader("🎨 Theme Settings")

    theme = st.radio(
        "Choose Theme",
        ["Light", "Dark"],
        index=0 if st.session_state.theme == "Light" else 1
    )

    st.session_state.theme = theme

    if theme == "Dark":

        st.markdown(
            """
            <style>
            .stApp{
                background-color:#0E1117;
                color:white;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <style>
            .stApp{
                background-color:white;
                color:black;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # -----------------------------
    # Application Information
    # -----------------------------

    st.subheader("Application Information")

    st.write("**Project Name:** Smart Placement & Resume Screening Engine")
    st.write("**Version:** 1.0")
    st.write("**Developer:** Diwakar Kumar Upadhayay")
    st.write("**Framework:** Streamlit")
    st.write("**Language:** Python")

    st.divider()

    # -----------------------------
    # System Status
    # -----------------------------

    st.subheader("🖥 System Status")

    st.success("🟢 ATS Running Successfully")

    st.divider()

    # -----------------------------
    # Theme Note
    # -----------------------------

    st.subheader("Theme")

    st.info(
        "Theme selection is for demonstration. "
        "Change actual theme from Streamlit Settings."
    )

    st.divider()

    # -----------------------------
    # Data Information
    # -----------------------------

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

    # -----------------------------
    # Clear History
    # -----------------------------

    if st.button("🗑 Clear Resume History"):

        if os.path.exists(HISTORY_FILE):

            os.remove(HISTORY_FILE)

            st.success("Resume History Cleared Successfully ✅")

        else:

            st.warning("Resume History Not Found.")

    st.divider()
      

    # -----------------------------
    # Logout
    # -----------------------------

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.success("Logged Out Successfully")

        st.rerun()

    st.divider()

    st.success("Settings Loaded Successfully ✅")

    st.caption(
        "© 2026 Smart Placement ATS | Developed by Diwakar Kumar Upadhayay"
    )