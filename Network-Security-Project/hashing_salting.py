"""
Password Hashing & Salting Demo
--------------------------------
A simple program that shows how to securely store a password using bcrypt.
It demonstrates both registration (hashing with salt) and login verification.
"""

import bcrypt

# ------------------- REGISTER USER -------------------

# Ask user to create a password
user_password = input("Create a password to register: ").encode()  # convert to bytes

# Generate a random salt and hash the password
salt = bcrypt.gensalt()
hashed_pw = bcrypt.hashpw(user_password, salt)

print("\nYour password has been safely stored!")
print("Salt used:", salt)
print("Hashed password:", hashed_pw)

# ------------------- LOGIN USER -------------------

# Ask user to login
login_password = input("\nEnter your password to login: ").encode()

# Verify the entered password against the stored hash
if bcrypt.checkpw(login_password, hashed_pw):
    print("Login successful!")
else:
    print("Invalid password. Try again.")