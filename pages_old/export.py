import streamlit as st
import pandas as pd
import os

from openpyxl import Workbook
from reportlab.pdfgen import canvas


# -----------------------------
# Export Excel
# -----------------------------
def export_excel_page(CSV_FILE, DATA_DIR):

    st.header("📥 Export Candidates to Excel")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        if st.button("Generate Excel File"):

            workbook = Workbook()

            sheet = workbook.active
            sheet.title = "Candidates"

            sheet.append(df.columns.tolist())

            for row in df.values.tolist():
                sheet.append(row)

            excel_file = os.path.join(
                DATA_DIR,
                "Candidates_Report.xlsx"
            )

            workbook.save(excel_file)

            st.success("✅ Excel File Generated Successfully")

            with open(excel_file, "rb") as file:

                st.download_button(
                    label="📥 Download Excel Report",
                    data=file,
                    file_name="Candidates_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    else:

        st.warning("No Candidate Data Found.")


# -----------------------------
# Export PDF
# -----------------------------
def export_pdf_page(CSV_FILE, DATA_DIR):

    st.header("📄 Export ATS Report")

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        if st.button("Generate PDF Report"):

            pdf_file = os.path.join(
                DATA_DIR,
                "ATS_Report.pdf"
            )

            c = canvas.Canvas(pdf_file)

            c.setFont("Helvetica-Bold", 18)

            c.drawString(
                150,
                800,
                "Smart Placement ATS Report"
            )

            c.setFont("Helvetica", 12)

            c.drawString(
                50,
                770,
                f"Total Candidates : {len(df)}"
            )

            y = 740

            c.drawString(
                50,
                y,
                "Candidate List"
            )

            y -= 20

            for _, row in df.iterrows():

                line = (
                    f"{row['Name']} | "
                    f"{row['Education']} | "
                    f"{row['Experience']} Years"
                )

                c.drawString(
                    50,
                    y,
                    line
                )

                y -= 20

                if y < 50:

                    c.showPage()

                    y = 800

            c.save()

            st.success("✅ PDF Generated Successfully")

            with open(pdf_file, "rb") as pdf:

                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf,
                    file_name="ATS_Report.pdf",
                    mime="application/pdf"
                )

    else:

        st.warning("No Candidate Data Found.")