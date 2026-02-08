import time
from werkzeug.security import generate_password_hash, check_password_hash

def demo_password_security():
    print("--- PASSWORD SECURITY DEEP DIVE ---\n")

    # 1. Plain Text vs Hashing
    password = "pizza"
    print(f"User's Password: {password}")
    
    # BAD WAY: Storing as plain text
    # DB: "pizza"
    # Hacker steals DB -> Knows password is "pizza"
    print("1. Plain Text Storage: vulnerability!")

    # GOOD WAY: Hashing
    # werkzeug uses pbkdf2:sha256 by default with a salt
    hashed = generate_password_hash(password)
    print(f"2. Hashed Storage: {hashed}")
    print("   Hacker steals DB -> Sees random garbage. Cannot easily reverse it to 'pizza'.\n")

    # 2. Salting (The 'Food' Analogy)
    # Imagine two users both have the password "pizza".
    # Without salt, their hashes would be identical.
    # Hacker sees identical hashes -> Knows they have the same password.
    
    print("--- The Magic of Salting ---")
    user1_pass = "pizza"
    user2_pass = "pizza"
    
    hash1 = generate_password_hash(user1_pass)
    hash2 = generate_password_hash(user2_pass)
    
    print(f"User 1 ('pizza') hash: {hash1}")
    print(f"User 2 ('pizza') hash: {hash2}")
    
    if hash1 != hash2:
        print("Success! Different hashes for the same password.")
        print("Explanation: A random 'salt' (flavor) is added to each password before hashing.")
        print("User 1: Hash('pizza' + 'saltA')")
        print("User 2: Hash('pizza' + 'saltB')")
    
    print("\n--- Brute Force Protection ---")
    # Modern hashing functions are deliberately SLOW.
    # If a computer can try 1 billion passwords a second, it can crack standard hashes fast.
    # If it can only try 1000 a second (because of 'work factor'), cracking takes 1 million times longer.
    
    start = time.time()
    check_password_hash(hash1, "pizza")
    end = time.time()
    print(f"Time to verify one password: {end - start:.5f} seconds")
    print("This delay is intentional to stop hackers from guessing millions of passwords quickly.")

if __name__ == "__main__":
    demo_password_security()
