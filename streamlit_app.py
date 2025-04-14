import streamlit as st
from utils.drive_utils import authenticate_google, get_student_submission_data, to_excel_bytes
import pandas as pd

st.set_page_config(page_title="📂 Google Drive Assignment Evaluator")
st.title("📂 Assignment Submission Evaluator")

st.markdown("""
Enter your **Google Drive folder ID** to check how many files each student has submitted.  
This app uses Google OAuth 2.0 to access Drive metadata securely.
""")

folder_id = st.text_input("📁 Enter Google Drive Folder ID")

if folder_id:
    try:
        service = authenticate_google()
        st.success("✅ Connected to Google Drive!")

        submission_data = get_student_submission_data(service, folder_id)

        if not submission_data:
            st.warning("⚠️ No student folders found.")
        else:
            df = pd.DataFrame(submission_data)
            st.dataframe(df)

            excel_bytes = to_excel_bytes(df)
            st.download_button(
                label="📥 Download Excel Report",
                data=excel_bytes,
                file_name="submission_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"❌ Error: {e}")