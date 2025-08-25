import bcrypt

# -----------------------------
# Registration (store password)
# -----------------------------
password = input("Enter your password to register: ").encode()  # Convert to bytes

# Generate a salt & hash
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password, salt)

print("\nYour password has been securely stored!")
print("Salt:", salt)
print("Hashed password:", hashed_password)

# -----------------------------
# Login (check password)
# -----------------------------
login_attempt = input("\nEnter your password to login: ").encode()

if bcrypt.checkpw(login_attempt, hashed_password):
    print("✅ Login successful!")
else:
    print("❌ Invalid password.")