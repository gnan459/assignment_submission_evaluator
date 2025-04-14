# 📂 Google Drive Assignment Evaluator

A Streamlit app that checks student assignment submissions in Google Drive and generates a downloadable Excel report.

## 🚀 Features

- OAuth 2.0 login to Google Drive
- Counts number of files per student
- Exports results to Excel
- Streamlit-based UI

## 🛠️ Setup Instructions

1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/google-drive-evaluator.git
   cd google-drive-evaluator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file from template:
   ```bash
   cp .env.example .env
   ```

4. Fill in your `.env`:
   - Get credentials from Google Cloud Console → OAuth 2.0 Client ID
   - Paste them into `.env`

5. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

## 🔒 Security

- Do **not** commit `client_secrets.json`, `.env`, or `token.pickle` to GitHub.
- Use `.gitignore` to protect sensitive data.