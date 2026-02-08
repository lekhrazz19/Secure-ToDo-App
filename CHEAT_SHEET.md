# Security Cheat Sheet for Beginners

## 🛡️ Basics
- [ ] **Never trust user input**. Always validate length and content.
- [ ] **Hash passwords**. Use `werkzeug.security` or `bcrypt`.
- [ ] **Use HTTPS**. (We set `SESSION_COOKIE_SECURE = True` in production).

## 🕷️ Web Vulnerabilities
- [ ] **XSS**: Use template engines that auto-escape (like Jinja2, React).
- [ ] **SQL Injection**: Use an ORM (SQLAlchemy, Django ORM). Never use string concatenation for SQL.
- [ ] **CSRF**: use `Flask-WTF` forms (built-in protection) or sets `SameSite` cookies.

## 🍪 Sessions
- [ ] Set `HttpOnly=True` so JavaScript can't read cookies.
- [ ] Set `SameSite='Lax'` or `'Strict'`.
- [ ] Expire sessions after a set time (e.g., 30 mins).

## 🔒 Headers
- [ ] `X-Frame-Options: SAMEORIGIN`
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `Content-Security-Policy`: (Advanced) Whitelist where scripts can load from.
