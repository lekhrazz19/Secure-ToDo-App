# SecureTodo - Security Learning Guide

## 1. Authentication vs Authorization
*   **Authentication (Who are you?)**: We used `Flask-Login` to handle this. When you log in, the server gives you a session cookie (like a VIP wristband).
*   **Authorization (What can you do?)**: We added checks like `if todo.user_id != current_user.id`. This ensures User A cannot delete User B's todos.

## 2. Password Security
*   **Hashing**: We turn `password` into `pbkdf2:sha256:...`. This is like turning a cow into a burger. You can't turn the burger back into a cow.
*   **Salting**: We add random data before hashing. This stops hackers from seeing if two users have the same password.
*   **Complexity**: We force users to have numbers/uppercase letters to make "Brute Force" attacks (guessing every password) take too long.

## 3. Input Validation (Defense against XSS)
*   **XSS (Cross Site Scripting)**: Attackers try to type `<script>steal_cookies()</script>` into forms.
*   **Solution**: Flask/Jinja2 automatically escapes text. `<` becomes `&lt;`. The browser displays the text but doesn't run the code.
*   **Validation**: We also limit the length of inputs to prevent database overflow.

## 4. SQL Injection (Defense against Database Theft)
*   **SQLi**: Hackers input `admin' OR '1'='1` to trick the database.
*   **Solution**: `Flask-SQLAlchemy` sends the query and the data separately. The database knows `'1'='1'` is just text, not a math equation.

## 5. Security Headers (Defense against Browser Attacks)
*   `X-Frame-Options: SAMEORIGIN`: Stops other sites from putting your site in an iframe (Clickjacking).
*   `X-Content-Type-Options: nosniff`: Stops the browser from guessing that a text file is actually a script.
*   `Referrer-Policy`: Controls how much info passes when you click a link to another site.
