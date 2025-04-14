import os
import pickle
import io
import pandas as pd
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

def create_client_secrets():
    data = {
        "installed": {
            "client_id": os.getenv("94912732903-9fvhldsbi3p6of1da1mmt55peict5fqt.apps.googleusercontent.com"),
            "client_secret": os.getenv("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"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"]
        }
    }

    with open("client_secrets.json", "w") as f:
        import json
        json.dump(data, f)

def authenticate_google():
    creds = None
    if not os.path.exists("client_secrets.json"):
        create_client_secrets()

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)
    return service

def get_subfolders(service, parent_id):
    results = service.files().list(
        q=f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id, name)"
    ).execute()
    return results.get("files", [])

def count_files_in_folder(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed=false",
        fields="files(id)"
    ).execute()
    return len(results.get("files", []))

def get_student_submission_data(service, parent_id):
    folders = get_subfolders(service, parent_id)
    data = []
    for folder in folders:
        count = count_files_in_folder(service, folder["id"])
        data.append({"Student": folder["name"], "Files Submitted": count})
    return data

def to_excel_bytes(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()