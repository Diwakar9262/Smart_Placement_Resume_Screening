import streamlit as st
import pandas as pd
import os
# -----------------------------
# Add Candidate
# -----------------------------
def add_candidate_page(CSV_FILE):

    st.header("➕ Add Candidate")

    name = st.text_input("Candidate Name")

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=60
    )

    education = st.selectbox(
        "Education",
        [
            "B.Tech",
            "BCA",
            "MCA",
            "B.Sc",
            "M.Tech"
        ]
    )

    experience = st.number_input(
        "Experience (Years)",
        min_value=0,
        max_value=40
    )

    skills = st.text_area(
        "Skills (Comma Separated)"
    )

    submit = st.button("Add Candidate")

    if submit:

        if not name.strip():

            st.error("❌ Please enter candidate name.")

        elif not skills.strip():

            st.error("❌ Please enter candidate skills.")

        else:

            # Duplicate Candidate Check

            if os.path.exists(CSV_FILE):

                df = pd.read_csv(CSV_FILE)

                duplicate = df[
                    df["Name"].str.lower() == name.lower()
                ]

                if not duplicate.empty:

                    st.error("❌ Candidate already exists.")

                    st.stop()

            else:

                df = pd.DataFrame(
                    columns=[
                        "Name",
                        "Age",
                        "Education",
                        "Experience",
                        "Skills"
                    ]
                )

            new_candidate = {
                "Name": name,
                "Age": age,
                "Education": education,
                "Experience": experience,
                "Skills": skills
            }

            if os.path.exists(CSV_FILE):

                df = pd.read_csv(CSV_FILE)

            else:

                df = pd.DataFrame(
                    columns=[
                        "Name",
                        "Age",
                        "Education",
                        "Experience",
                        "Skills"
                    ]
                )

            df = pd.concat(
                [
                    df,
                    pd.DataFrame([new_candidate])
                ],
                ignore_index=True
            )

            df.to_csv(CSV_FILE, index=False)

            st.success("✅ Candidate Saved Successfully")

            st.write("Rows in DataFrame:", len(df))

            st.write(df)


# -----------------------------
# View Candidates
# -----------------------------
def view_candidate_page(CSV_FILE):

    st.header("📋 All Candidates")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        st.dataframe(
            df,
            width="stretch"
        )

    else:

        st.warning("No Candidate Data Found.")
# -----------------------------
# Search Candidate
# -----------------------------
def search_candidate_page(CSV_FILE):

    st.header("🔍 Search Candidate")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        search_name = st.text_input(
            "Enter Candidate Name"
        )

        if search_name:

            result = df[
                df["Name"].str.lower() == search_name.lower()
            ]

            if not result.empty:

                st.success("Candidate Found ✅")

                st.dataframe(
                    result,
                    width="stretch"
                )

            else:

                st.error("Candidate Not Found ❌")

    else:

        st.warning("No Candidate Data Found.")


# -----------------------------
# Delete Candidate
# -----------------------------
def delete_candidate_page(CSV_FILE):

    st.header("🗑 Delete Candidate")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        candidate = st.selectbox(
            "Select Candidate",
            df["Name"]
        )

        if st.button("Delete Candidate"):

            df = df[
                df["Name"] != candidate
            ]

            df.to_csv(
                CSV_FILE,
                index=False
            )

            st.success(
                "Candidate Deleted Successfully ✅"
            )

            st.rerun()

    else:

        st.warning("No Candidate Data Found.")
# -----------------------------
# Edit Candidate
# -----------------------------
def edit_candidate_page(CSV_FILE):

    st.header("✏ Edit Candidate")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        candidate = st.selectbox(
            "Select Candidate",
            df["Name"]
        )

        row_index = df[df["Name"] == candidate].index[0]

        row = df.loc[row_index]

        new_name = st.text_input(
            "Candidate Name",
            value=row["Name"]
        )

        new_age = st.number_input(
            "Age",
            min_value=18,
            max_value=60,
            value=int(row["Age"])
        )

        education_options = [
            "B.Tech",
            "BCA",
            "MCA",
            "B.Sc",
            "M.Tech"
        ]

        current_index = education_options.index(
            row["Education"]
        )

        new_education = st.selectbox(
            "Education",
            education_options,
            index=current_index
        )

        new_experience = st.number_input(
            "Experience",
            min_value=0,
            max_value=40,
            value=int(row["Experience"])
        )

        new_skills = st.text_area(
            "Skills",
            value=row["Skills"]
        )

        if st.button("Update Candidate"):

            if not new_name.strip():

                st.error("❌ Candidate name cannot be empty.")

            elif not new_skills.strip():

                st.error("❌ Skills cannot be empty.")

            else:

                df.loc[row_index, "Name"] = new_name
                df.loc[row_index, "Age"] = new_age
                df.loc[row_index, "Education"] = new_education
                df.loc[row_index, "Experience"] = new_experience
                df.loc[row_index, "Skills"] = new_skills

                df.to_csv(CSV_FILE, index=False)

                st.success("✅ Candidate Updated Successfully")

                st.rerun()

    else:

        st.warning("No Candidate Data Found.")