"""
This program shows a basic login system using bcrypt for secure passwords.  
It supports user registration, login, logout, and automatically checks for session timeouts.
"""

import bcrypt
import time


# ------------------- Data Storage -------------------

users = {}          # Stores usernames and their hashed passwords
sessions = {}       # Keeps track of active sessions and last activity

SESSION_LIFETIME = 60  # Session timeout in seconds


# ------------------- User Registration -------------------

def register():
    username = input("Choose a username: ")
    if username in users:
        print("Username already exists. Try again.")
        return

    password = input("Create a strong password: ").encode()
    hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
    users[username] = hashed_pw
    print(f"User '{username}' registered successfully!")


# ------------------- User Login -------------------

def login():
    username = input("Username: ")
    password = input("Password: ").encode()

    if username not in users:
        print("User not found.")
        return None

    if bcrypt.checkpw(password, users[username]):
        # Create a simple session ID for the user
        session_id = f"session_{username}"
        sessions[session_id] = {
            "username": username,
            "last_active": time.time()
        }
        print("Login successful!")
        return session_id
    else:
        print("Incorrect password.")
        return None


# ------------------- Session Check -------------------

def validate_session(session_id: str) -> bool:
    # Look up the session
    session = sessions.get(session_id)
    if not session:
        print("No active session found.")
        return False

    # Check if the session has timed out
    if time.time() - session["last_active"] > SESSION_LIFETIME:
        print("Session expired.")
        del sessions[session_id]
        return False

    # Refresh last active time
    session["last_active"] = time.time()
    return True


# ------------------- Logout -------------------

def logout(session_id: str):
    # Remove session if it exists
    if session_id in sessions:
        del sessions[session_id]
        print("Logged out successfully.")
    else:
        print("No session to log out from.")


# ------------------- Main Loop -------------------

def main():
    session_id = None

    while True:
        choice = input("\nChoose an action [register/login/logout/exit]: ").lower()

        if choice == "register":
            register()
        elif choice == "login":
            session_id = login()
        elif choice == "logout":
            if session_id and validate_session(session_id):
                logout(session_id)
                session_id = None
            else:
                print("No valid session to log out.")
        elif choice == "exit":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

        # Automatically check if session has expired
        if session_id and not validate_session(session_id):
            session_id = None


if __name__ == "__main__":
    main()