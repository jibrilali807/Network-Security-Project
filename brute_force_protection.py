import bcrypt
import time

# Sample user database (username: hashed password)
users = {
    "alice": bcrypt.hashpw(b"mypassword", bcrypt.gensalt())
}

failed_attempts = {}

def login(username, password):
    now = time.time()

    # Check if user exists in failed_attempts; if not, initialize
    if username not in failed_attempts:
        failed_attempts[username] = {"count": 0, "lock_until": 0.0}

    # Lockout check
    if failed_attempts[username]["lock_until"] > now:
        remaining = int(failed_attempts[username]["lock_until"] - now)
        print(f"Account locked. Try again in {remaining} seconds.")
        return False

    # Correct login
    if username in users and bcrypt.checkpw(password.encode(), users[username]):
        print("Successfully logged in!")
        failed_attempts[username] = {"count": 0, "lock_until": 0.0}  # reset
        return True
    else:
        failed_attempts[username]["count"] += 1

        if failed_attempts[username]["count"] >= 3:
            failed_attempts[username]["lock_until"] = now + 30  # lock 30s
            print("Too many failed attempts. Locked for 30 seconds.")
        else:
            print("Wrong password. Try again.")

        return False


if __name__ == "__main__":
    while True:
        uname = input("Username: ")
        pwd = input("Password: ")
        login(uname, pwd)