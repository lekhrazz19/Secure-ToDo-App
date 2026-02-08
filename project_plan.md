# SecureTodo - Project Plan

## 1. What We're Building
**SecureTodo** is a secure, web-based To-Do list application.
*   **Goal**: Create a functional app where users can sign up, log in, and manage their own private todo lists.
*   **Focus**: We aren't just building the app; we are securing it against common hacker attacks.

## 2. What We'll Learn
*   **Authentication**: How to safely handle user sign-ups and logins.
*   **Password Security**: Why we never save plain text passwords and how to hash them.
*   **Input Validation**: How to stop users from entering dangerous data.
*   **Session Management**: Keeping users logged in securely.
*   **Protection against Attacks**: Defending against SQL Injection and XSS (Cross-Site Scripting).

## 3. 14-Day Timeline
*   **Day 1**: Project Setup & Basic App (Phase 1 & 2)
*   **Day 2**: Database Setup & User Model (Phase 3)
*   **Day 3**: User Registration Form (Phase 4)
*   **Day 4**: User Login & Sessions (Phase 5)
*   **Day 5**: Password Security Deep Dive (Phase 6)
*   **Day 6**: Building the Todo Feature (Phase 7)
*   **Day 8**: Security: Input Validation (Phase 8) & SQL Injection (Phase 9)
*   **Day 9**: Security: Sessions & Cookies (Phase 10)
*   **Day 10**: Security: Basic Security Headers (Phase 11)
*   **Day 11**: UI/UX Improvements (Phase 12)
*   **Day 12**: Testing Our Security (Phase 13)
*   **Day 13**: Deployment (Phase 14)
*   **Day 14**: Final Review & Documentation (Phase 15)

## 4. Simple Folder Structure
This is how our project will look:

```
SecureTodo/
├── app.py              # The main brain of our application
├── database.db         # Where we store users and todos (created later)
├── requirements.txt    # List of tools we need to install
├── static/             # "Static" files like formatting and images
│   └── style.css       # File to make our app look nice
└── templates/          # HTML files (the pages users see)
    ├── base.html       # The common layout (navigation, footer)
    ├── login.html      # Login page
    ├── register.html   # Sign up page
    └── todo.html       # The main todo list page
```

## 5. Security Features We Will Implement
1.  **Password Hashing**: Transforming passwords so they can't be read if stolen.
2.  **Input Sanitization**: Cleaning data to prevent code injection.
3.  **SQL Injection Prevention**: Using safe database queries.
4.  **Secure Sessions**: ensuring nobody can hijack a logged-in user's session.
5.  **Security Headers**: Instructions for the browser to protect users.
6.  **CSRF Protection**: Preventing fake requests from other sites.
