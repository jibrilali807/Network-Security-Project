"""
Secure Login Demo with Lockout
-------------------------------
This program demonstrates a basic login system with password hashing using bcrypt.
It also includes a lockout mechanism after multiple failed login attempts.
"""

import bcrypt
import time

# ------------------- USERS DATABASE -------------------
# Example in-memory user database: username -> hashed password
users_db = {
    "alice": bcrypt.hashpw(b"mypassword", bcrypt.gensalt())
}

# Tracks failed login attempts and lockout time per user
login_attempts = {}

LOCK_DURATION = 30  # seconds to lock account after too many failed attempts
MAX_TRIES = 3       # number of allowed failed attempts

# ------------------- LOGIN FUNCTION -------------------
def login(username, password):
    current_time = time.time()

    # Initialize tracking if user not in login_attempts
    if username not in login_attempts:
        login_attempts[username] = {"count": 0, "lock_until": 0.0}

    # Check if account is currently locked
    if login_attempts[username]["lock_until"] > current_time:
        wait = int(login_attempts[username]["lock_until"] - current_time)
        print(f"Account locked. Try again in {wait} seconds.")
        return False

    # Verify password
    if username in users_db and bcrypt.checkpw(password.encode(), users_db[username]):
        print("Login successful!")
        login_attempts[username] = {"count": 0, "lock_until": 0.0}  # reset failed attempts
        return True
    else:
        # Failed attempt
        login_attempts[username]["count"] += 1
        if login_attempts[username]["count"] >= MAX_TRIES:
            login_attempts[username]["lock_until"] = current_time + LOCK_DURATION
            print(f"Too many failed attempts. Account locked for {LOCK_DURATION} seconds.")
        else:
            print("Wrong password. Try again.")
        return False

# ------------------- MAIN LOOP -------------------
if __name__ == "__main__":
    print("=== Secure Login System ===")
    while True:
        uname = input("\nUsername: ")
        pwd = input("Password: ")
        login(uname, pwd)
