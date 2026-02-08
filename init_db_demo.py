from app import app, db, User

# Create the database tables first
with app.app_context():
    db.create_all()
    
    # 1. Create a new user
    print("--- Creating a new user ---")
    username = "secure_user"
    email = "user@example.com"
    password = "supersecretpassword"
    
    # Check if user already exists to avoid error on re-run
    if User.query.filter_by(username=username).first():
        print(f"User {username} already exists!")
    else:
        new_user = User(username=username)
        
        # 2. Hash the password
        # WE NEVER STORE PLAIN PASSWORDS. 
        # Hashing converts the password into a scrambled string.
        # Even if a hacker steals the database, they won't know the real password.
        new_user.set_password(password)
        print(f"Original password: {password}")
        print(f"Stored hash: {new_user.password_hash}")
        
        # 3. Save to database
        db.session.add(new_user)
        db.session.commit()
        print("User saved to database.")

    # 4. Check if user exists & verify password
    print("\n--- Verifying User ---")
    fetched_user = User.query.filter_by(username="secure_user").first()
    if fetched_user:
        print(f"Found user: {fetched_user.username}")
        
        # Check correct password
        is_valid = fetched_user.check_password("supersecretpassword")
        print(f"Password 'supersecretpassword' valid? {is_valid}")
        
        # Check wrong password
        is_invalid = fetched_user.check_password("wrongpassword")
        print(f"Password 'wrongpassword' valid? {is_invalid}")
    else:
        print("User not found.")
