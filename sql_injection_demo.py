import sqlite3
from app import app, db, User

def demo_sql_injection():
    print("--- SQL INJECTION DEMO ---\n")
    
    # 1. THE VULNERABLE WAY (Raw SQL with string formatting)
    # Imagine a login query like this:
    # "SELECT * FROM user WHERE username = '" + username + "'"
    
    print("Scenario: Login Query")
    username_input = "hacker' OR '1'='1"
    
    unsafe_query = f"SELECT * FROM user WHERE username = '{username_input}'"
    print(f"Malicious Input: {username_input}")
    print(f"Resulting Unsafe Query: {unsafe_query}")
    print("EXPLANATION: The 'OR 1=1' trick makes the condition always TRUE.")
    print("This could log the hacker in as the first user (usually Admin) without a password!\n")

    # 2. THE SECURE WAY (Flask-SQLAlchemy / Parameterized Queries)
    print("--- How We Are Protected ---")
    print("Flask-SQLAlchemy uses 'parameterized queries'.")
    print("It treats user input as data, NOT code.")
    
    with app.app_context():
        # Let's try to find a user with the malicious name using our secure ORM
        user = User.query.filter_by(username=username_input).first()
        
        if user:
            print("Found user? Yes (Wait, do we actually have a user named \"hacker' OR '1'='1\"?)")
        else:
            print("Found user? No.")
            print("SUCCESS: The database looked for a user literally named \"hacker' OR '1'='1\".")
            print("It did NOT execute the SQL command.")

if __name__ == "__main__":
    demo_sql_injection()
