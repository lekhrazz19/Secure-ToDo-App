# Deployment Guide for SecureTodo

## 1. Local Deployment (Windows)
You already have `run.bat`, but here's how to run it manually:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py
```
Open your browser to `http://127.0.0.1:5000`.

## 2. Cloud Deployment (Render.com / Heroku)
This app is ready for the cloud!

### Steps for Render.com (Free Tier):
1.  **Push to GitHub**:
    *   Initialize git: `git init`
    *   Add files: `git add .`
    *   Commit: `git commit -m "Initial commit"`
    *   Create a repo on GitHub and push.

2.  **Create Web Service on Render**:
    *   Connect your GitHub account.
    *   Select the `SecureTodo` repo.
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app` (We created a `Procfile` for this!)

3.  **Environment Variables**:
    *   Add `SECRET_KEY` with a long random string.
    *   (Optional) Use a PostgreSQL URL for `SQLALCHEMY_DATABASE_URI` if you want a persistent logic DB (SQLite resets on deploy).

## 3. Next Projects to Build
1.  **Secure File Storage**: Allow users to upload files, but scan them for viruses and prevent overwriting system files.
2.  **2FA (Two-Factor Auth)**: Add TOTP (Google Authenticator) to the login flow.
3.  **API with JWT**: Convert this app to an API using JSON Web Tokens instead of sessions.
