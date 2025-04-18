import streamlit as st
import pandas as pd
import io
import pickle
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


# --- CONFIG ---
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

# --- AUTH ---
def google_drive_login():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("drive", "v3", credentials=creds)

# --- UTILS ---
def get_subfolders(service, parent_id):
    results = service.files().list(
        q=f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id, name)"
    ).execute()
    return results.get("files", [])

def count_files_in_folder(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed=false",
        fields="files(id, name)"
    ).execute()
    return len(results.get("files", []))

def to_excel_bytes(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Submissions")
    return output.getvalue()

# --- STREAMLIT UI ---
st.set_page_config(page_title="Google Drive Assignment Evaluator", layout="centered")
st.title("📂 Assignment Submission Evaluator")

st.markdown("""
Upload your Google Drive **Students Folder ID**, and get a report of how many files each student submitted.
""")

folder_id = st.text_input("Enter the Folder ID (from Drive link)", "")

if folder_id:
    try:
        service = google_drive_login()
        st.success("✅ Google Drive connected successfully!")

        folders = get_subfolders(service, folder_id)

        if not folders:
            st.warning("⚠️ No student folders found. Please check the Folder ID and permissions.")
        else:
            data = []
            st.info(f"📁 Found {len(folders)} student folders.")
            for folder in folders:
                student_name = folder["name"]
                files_count = count_files_in_folder(service, folder["id"])
                st.write(f"👨‍🎓 {student_name}: {files_count} files")
                data.append({"Student Name": student_name, "Files Submitted": files_count})

            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)

                excel_bytes = to_excel_bytes(df)
                st.download_button(
                    label="📥 Download Excel Report",
                    data=excel_bytes,
                    file_name="submission_report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                st.warning("No files found in any folders.")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
