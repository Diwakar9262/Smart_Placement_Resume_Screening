import streamlit as st
import pandas as pd
import os


def change_password_page(USERS_FILE):

    st.header("🔑 Change Password")

    username = st.session_state.username

    current_password = st.text_input(
        "Current Password",
        type="password"
    )

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Update Password"):

        if not os.path.exists(USERS_FILE):
            st.error("users.csv not found")
            return

        df = pd.read_csv(USERS_FILE)

        user = df[
            (df["Username"] == username) &
            (df["Password"] == current_password)
        ]

        if user.empty:
            st.error("❌ Current Password is incorrect")
            return

        if new_password != confirm_password:
            st.error("❌ New Password and Confirm Password do not match")
            return

        df.loc[
            df["Username"] == username,
            "Password"
        ] = new_password

        df.to_csv(USERS_FILE, index=False)

        st.success("✅ Password Changed Successfully")