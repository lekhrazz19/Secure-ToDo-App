# Manual Testing Guide for SecureTodo

This guide helps you manually verify the security features of your application.

## 1. Automated Security Check
First, run the automated test suite to check all security features at once.
```bash
python verify_security.py
```
**Expected Output**: `[PASSED] ALL SECURITY CHECKS PASSED!`

---

## 2. Manual Walkthrough (Step-by-Step)
Follow these steps exactly. If something doesn't work, check the "Troubleshooting" section below.

### Phase 1: Registration & Login
1.  **Start the App**: Double-click `run.bat` or run `python app.py`.
2.  **Open Browser**: Go to `http://127.0.0.1:5000`.
3.  **Register Weak User**:
    *   Click **Register**.
    *   Enter Username: `weakuser`, Password: `password` (lowercase).
    *   **Result**: You should see a red alert: *"Password must be at least 8 characters..."* or *"Must include uppercase..."*.
4.  **Register Strong User**:
    *   Enter Username: `MyUser`, Password: `TestUser123!`.
    *   **Result**: You should see a green alert: *"Registration successful! Please login."* and be redirected to the Login page.
5.  **Login**:
    *   Log in with `MyUser` / `TestUser123!`.
    *   **Result**: You are now on the "My Secure Todos" page.

### Phase 2: Todo Functionality
1.  **Add Todo**: Type "Buy Milk" and click "Add Todo".
    *   **Result**: "Buy Milk" appears in the list.
2.  **Complete**: Click "Done".
    *   **Result**: The text "Buy Milk" gets a line-through (crossed out).
3.  **Delete**: Click "Delete".
    *   **Result**: The item disappears and you see "Todo deleted." in green.

---

### Phase 3: "Hacker" Tests (Security Verification)

#### A. Test XSS Defense (Script Injection)
*Goal: Try to make a popup window appear.*
1.  Add a new Todo with this exact text:
    ```
    <script>alert('Hacked')</script>
    ```
2.  **Result**:
    *   **Secure Behavior**: The text `<script>alert('Hacked')</script>` appears on the screen as normal text. Nothing happens.
    *   **Vulnerable Behavior (Fail)**: A popup box says "Hacked".
    *   *Note: If you just see the text, YOU PASSED.*

#### B. Test Authorization (Access Control)
*Goal: Try to delete someone else's todo.*
1.  **Prepare**:
    *   Log in as `MyUser`. Add a todo "My Secret Task".
    *   Hover over the "Delete" button. Look at the URL in the bottom left (e.g., `.../delete/1`). Remember this ID (e.g., 1).
    *   Click "Logout".
2.  **Attack**:
    *   Register a NEW user: `Attacker` / `TestUser123!`.
    *   Log in as `Attacker`.
    *   Manually type this URL in the browser bar: `http://127.0.0.1:5000/delete/1` (Replace `1` with the ID you found earlier).
    *   Press Enter.
3.  **Result**:
    *   **Secure Behavior**: You are redirected back to your empty list. A red alert says *"You do not have permission to delete this todo."* or *"Todo not found."*
    *   **Vulnerable Behavior (Fail)**: The page loads or you get a generic error, and the other user's task is deleted.

#### C. Test SQL Injection
*Goal: Try to log in without a password.*
1.  Logout. Go to the Login page.
2.  **Username**: `admin' OR '1'='1`
3.  **Password**: `anything`
4.  Click Login.
5.  **Result**:
    *   **Secure Behavior**: A red alert says *"Login unsuccessful. Check username and password."*
    *   **Vulnerable Behavior (Fail)**: You are logged in as the first user in the database.

---

## Troubleshooting
*   **"I don't see any alerts/colors!"**:
    *   Make sure `style.css` is loaded. Try `Ctrl+F5` to hard refresh the page.
*   **"The XSS script disappeared!"**:
    *   Jinja2 might have hidden the tags, but as long as the code didn't run (no popup), you are safe.
*   **"I can't register!"**:
    *   Make sure you use a Capital letter and a Number in your password.
