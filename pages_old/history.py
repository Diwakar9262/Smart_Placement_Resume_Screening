import streamlit as st
import pandas as pd
import os


# -----------------------------
# Resume Upload History
# -----------------------------
def history_page(HISTORY_FILE):

    st.header("📜 Resume Upload History")

    if os.path.exists(HISTORY_FILE):

        history_df = pd.read_csv(HISTORY_FILE)

        st.dataframe(
            history_df,
           width="stretch"
        )

    else:

        st.warning("No Resume History Found.")