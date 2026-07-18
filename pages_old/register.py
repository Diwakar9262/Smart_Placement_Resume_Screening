import streamlit as st
import pandas as pd
import os


def register_page(USERS_FILE):

    st.header("📝 Candidate Registration")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register"):

        if not username.strip():
            st.error("❌ Username cannot be empty")
            return

        if password != confirm_password:
            st.error("❌ Passwords do not match")
            return

        if os.path.exists(USERS_FILE):

            df = pd.read_csv(USERS_FILE)

        else:

            df = pd.DataFrame(
                columns=[
                    "Username",
                    "Password",
                    "Role"
                ]
            )

        if username in df["Username"].values:
            st.error("❌ Username already exists")
            return

        new_user = pd.DataFrame([
            {
                "Username": username,
                "Password": password,
                "Role": "Candidate"
            }
        ])

        df = pd.concat(
            [df, new_user],
            ignore_index=True
        )

        df.to_csv(
            USERS_FILE,
            index=False
        )

        st.success("✅ Registration Successful")