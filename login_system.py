import bcrypt
import time

# ----------------- In-memory "database" ----------------- #
users_db = {}          # username: hashed_password
active_sessions = {}   # session_id: {'username': ..., 'last_active': ...}

SESSION_TIMEOUT = 60  # seconds for demo purposes

# ----------------- Register a user ----------------- #
def register_user():
    username = input("Enter a new username: ")
    if username in users_db:
        print("Username already exists. Try a different one.")
        return
   
    password = input("Enter a strong password: ").encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    users_db[username] = hashed
    print(f"✅ {username} registered successfully!")

# ----------------- Login a user ----------------- #
def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ").encode()

    if username not in users_db:
        print("User not found.")
        return None
   
    if bcrypt.checkpw(password, users_db[username]):
        # Create a simple session ID (in real apps, use random UUIDs)
        session_id = f"session_{username}"
        active_sessions[session_id] = {
            'username': username,
            'last_active': time.time()
        }
        print("Login successful!")
        return session_id
    else:
        print("Incorrect password.")
        return None

# ----------------- Check session ----------------- #
def check_session(session_id):
    session = active_sessions.get(session_id)
    if not session:
        print("Session not found or expired.")
        return False
    # Check timeout
    if time.time() - session['last_active'] > SESSION_TIMEOUT:
        print("⏳ Session expired.")
        del active_sessions[session_id]
        return False
    # Update last active time
    session['last_active'] = time.time()
    return True

# ----------------- Logout ----------------- #
def logout(session_id):
    if session_id in active_sessions:
        del active_sessions[session_id]
        print("Logged out successfully.")

# ----------------- Main Program ----------------- #
while True:
    action = input("\nChoose an action: [register/login/logout/exit]: ").lower()
   
    if action == "register":
        register_user()
    elif action == "login":
        session = login_user()
    elif action == "logout":
        if 'session' in locals() and session:
            logout(session)
            session = None
        else:
            print("No active session.")
    elif action == "exit":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Type 'register', 'login', 'logout', or 'exit'.")
   
    # Optional: check if session timed out automatically
    if 'session' in locals() and session:
        check_session(session)
