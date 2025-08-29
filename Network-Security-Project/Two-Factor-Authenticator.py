"""
This program helps users create strong passwords and simulates a 2FA login.  
It checks password strength, hashes the password, and generates a one-time verification code.
"""

import hashlib
import random
import string
import textwrap


# ------------------- CONFIGURATION -------------------

MIN_LENGTH = 12  # minimum password length
SPECIAL_CHARS = "!£$%^&*()-_=+{}[]:;@'~#<,>.?/"  # allowed special symbols
COMMON_PASSWORDS = {  # very common, weak passwords to avoid
    "password", "12345678", "passw0rd", "letmein", "qwerty", "qwerty123", 
    "123456", "123456789", "111111", "iloveyou", "admin", "welcome", "dragon", "abc123"
}


# ------------------- PASSWORD RULE CHECKS -------------------

def has_uppercase(text):
    """Check if password has at least one uppercase letter."""
    return any(ch in string.ascii_uppercase for ch in text)

def has_lowercase(text):
    """Check if password has at least one lowercase letter."""
    return any(ch in string.ascii_lowercase for ch in text)

def has_number(text):
    """Check if password has at least one digit."""
    return any(ch in string.digits for ch in text)

def has_special(text):
    """Check if password has at least one special character."""
    return any(ch in SPECIAL_CHARS for ch in text)

def repeats_three(text):
    """Return True if a character repeats 3 times in a row."""
    for i in range(len(text)-2):
        if text[i] == text[i+1] == text[i+2]:
            return True
    return False


# ------------------- PASSWORD VALIDATION -------------------

def check_password_strength(password):
    """
    Check password against rules:
    - Length, uppercase, lowercase, digit, special char, repeats, common passwords
    Returns:
      - list of issues
      - rating: Weak, Medium, Strong
    """
    issues = []
    score = 0

    # remove spaces at start/end
    if password != password.strip():
        issues.append("Remove spaces at the start or end.")
        password = password.strip()

    # length check
    if len(password) >= MIN_LENGTH:
        score += 2
    else:
        issues.append(f"Password must be at least {MIN_LENGTH} characters long.")

    # character checks
    if has_uppercase(password):
        score += 1
    else:
        issues.append("Add at least one uppercase letter (A–Z).")

    if has_lowercase(password):
        score += 1
    else:
        issues.append("Add at least one lowercase letter (a–z).")

    if has_number(password):
        score += 1
    else:
        issues.append("Add at least one number (0–9).")

    if has_special(password):
        score += 1
    else:
        issues.append(f"Add at least one special character (e.g., {SPECIAL_CHARS[:6]}…).")

    # common password check
    if password.lower() not in COMMON_PASSWORDS:
        score += 1
    else:
        issues.append("Password is too common. Choose something unique.")

    # repeating characters
    if not repeats_three(password):
        score += 1
    else:
        issues.append("Avoid repeating the same character 3+ times in a row.")

    # no spaces inside
    if " " not in password:
        score += 1
    else:
        issues.append("Avoid spaces inside the password.")

    # final rating
    if score <= 3:
        rating = "Weak"
    elif score <= 6:
        rating = "Medium"
    else:
        rating = "Strong"

    return issues, rating


# ------------------- PASSWORD HASHING -------------------

def hash_password(password):
    """Convert password to a secure SHA256 hash (one-way)."""
    return hashlib.sha256(password.encode()).hexdigest()


# ------------------- ONE-TIME CODE -------------------

def generate_otp():
    """Generate a random 6-digit number for 2FA."""
    return str(random.randint(100000, 999999))


# ------------------- MAIN PROGRAM -------------------

print("="*50)
print("Welcome to Secure Password & 2FA System")
print("="*50)

# Ask user to create a password
while True:
    password = input("\nEnter a password to register: ")
    issues, rating = check_password_strength(password)

    print("\nPassword:", password)
    print("Strength rating:", rating)

    if not issues and rating == "Strong":
        print("Strong password! Proceeding to 2FA...")
        break
    else:
        print("\nIssues to fix:")
        for issue in issues:
            print(textwrap.fill(" - " + issue, width=70))
        print("Please try again...")


# Hash the password
hashed_pw = hash_password(password)
print("\nYour password has been hashed for safe storage:")
print(hashed_pw)

# Generate a 6-digit OTP
otp = generate_otp()
print("\nA one-time verification code has been sent to your device:")
print(otp)

# Verify OTP 
attempts = 3
while attempts > 0:
    entered = input("\nEnter the 6-digit code: ")
    if entered == otp:
        print("2FA verified. Login successful!")
        break
    else:
        attempts -= 1
        print(f"Incorrect code. Attempts left: {attempts}")

if attempts == 0:
    print("Too many failed attempts. Access denied.")
