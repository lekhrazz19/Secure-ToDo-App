# SecureTodo - Cryptonic Area Internship Project 🔐

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![Security](https://img.shields.io/badge/Security-OWASP--Top--10-red)

## 📌 Project Overview
**SecureTodo** is a secure, web-based task management application developed as part of the **Cryptonic Area Internship**. 

Unlike standard todo apps, this project focuses heavily on **Application Security (AppSec)**. It demonstrates robust defenses against common web vulnerabilities, including SQL Injection, XSS (Cross-Site Scripting), CSRF, and Weak Authentication.

### 🌟 Key Features
*   **Secure Authentication**: User registration and login with strong password enforcement (8+ chars, uppercase, digits).
*   **Password Security**: Uses `pbkdf2:sha256` hashing with salting (via `Werkzeug`) to protect user credentials.
*   **Data Protection**:
    *   **Anti-SQL Injection**: Utilization of `Flask-SQLAlchemy` ORM to prevent malicious queries.
    *   **Anti-XSS**: Jinja2 auto-escaping + input length validation to neutralize script injections.
*   **Session Management**: Secure session cookies (`HttpOnly`, `SameSite=Lax`) to prevent session hijacking.
*   **Access Control**: strict authorization checks ensure users can only CRUD (Create, Read, Update, Delete) their own data.
*   **Security Headers**: Implemented `X-Frame-Options`, `X-Content-Type-Options`, and `Referrer-Policy` to harden browser security.

---

## 🛠 Tech Stack
*   **Backend**: Python, Flask
*   **Database**: SQLite (SQLAlchemy ORM)
*   **Frontend**: HTML5, CSS3 (Custom Responsive Design)
*   **Security**: Flask-Login, Werkzeug Security, Unittest

---

## 🚀 Setup & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/securetodo.git
cd securetodo
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
You can run the app directly or use the provided batch script:
```bash
# Option A: Command Line
python app.py

# Option B: Batch Script (Windows)
run.bat
```
Access the app at: `http://127.0.0.1:5000`

### 4. Verify Security
Run the automated security test suite to validate all funds:
```bash
python verify_security.py
```
*Sample Output:*
```
[PASSED] ALL SECURITY CHECKS PASSED!
...
```

### 5. Manual Testing (Must Read) 🧪
For a step-by-step guide on how to manually test the security features (like XSS and SQL Injection) yourself, please read:
👉 **[MANUAL_TESTING.md](MANUAL_TESTING.md)**

---

## 📂 Project Structure
```
SecureTodo/
├── app.py                 # Core application logic & routes
├── database.db            # SQLite Database
├── requirements.txt       # Dependencies
├── verify_security.py     # Automated Security Test Suite
├── static/
│   └── style.css          # Custom CSS Styling
└── templates/
    ├── base.html          # Base layout
    ├── login.html         # Secure Login Form
    ├── register.html      # Registration with complexity checks
    └── todo.html          # Main Task Dashboard
```

## 🎓 Learning Outcomes
Through this internship project, I have mastered:
1.  **OWASP Top 10 Defenses**: Practical implementation of mitigations for Injection, Broken Auth, and XSS.
2.  **Secure Coding Design**: Thinking like an attacker to build defensible code.
3.  **Full-Stack Development**: Integrating secure backend logic with a responsive frontend.

---
*Submitted by LEKHRAJ SINGH for Cryptonic Area Internship*
