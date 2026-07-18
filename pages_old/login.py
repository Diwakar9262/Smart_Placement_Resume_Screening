import streamlit as st
import pandas as pd
import os

# -----------------------------
# Login Session
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login_page(CSV_USERS):
    st.header("🔐 Login")
    option = st.radio(
        "Select Option",
        [
            "Login",
            "Register"
        ]
    )

    if option == "Register":
        from pages_old.register import register_page
        register_page(CSV_USERS)
        return

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if os.path.exists(CSV_USERS):

            df = pd.read_csv(CSV_USERS)

            user = df[
                (df["Username"] == username) &
                (df["Password"] == password)
            ]

            if not user.empty:

                role = user.iloc[0]["Role"]

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role

                st.success("✅ Login Successful")

                st.rerun()

            else:

                st.error("❌ Invalid Username or Password")

        else:

            st.error("users.csv not found")