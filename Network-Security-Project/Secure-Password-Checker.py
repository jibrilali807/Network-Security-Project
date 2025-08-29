"""
Simple Password Strength Checker
--------------------------------
A beginner-friendly program that tests how strong a password is.
It keeps asking until a password passes multiple security checks.
"""

import string
import textwrap


# ---------------- SETTINGS ---------------- #

MIN_LENGTH = 12  # minimum number of characters for a strong password
SPECIAL_CHARS = "!£$%^&*()-_=+{}[]:;@'~#<,>.?/"
COMMON_PASSWORDS = {
    "password", "12345678", "passw0rd", "letmein", "qwerty", "qwerty123", "123456",
    "123456789", "111111", "iloveyou", "admin", "welcome", "dragon", "abc123"
}


# ---------------- HELPER FUNCTIONS ---------------- #

def has_uppercase(text):
    """Check if password contains at least one uppercase letter."""
    return any(ch in string.ascii_uppercase for ch in text)

def has_lowercase(text):
    """Check if password contains at least one lowercase letter."""
    return any(ch in string.ascii_lowercase for ch in text)

def has_number(text):
    """Check if password contains at least one number."""
    return any(ch in string.digits for ch in text)

def has_special(text):
    """Check if password contains at least one special symbol."""
    return any(ch in SPECIAL_CHARS for ch in text)

def repeats_three_times(text):
    """Return True if a character repeats 3 or more times in a row."""
    for i in range(len(text) - 2):
        if text[i] == text[i+1] == text[i+2]:
            return True
    return False


# ---------------- PASSWORD CHECKING ---------------- #

def evaluate_password(password):
    """
    Check the password against multiple rules:
      - length, uppercase, lowercase, digit, special char, repetition, common passwords
    Returns:
      - list of issues (things to improve)
      - rating: Weak, Medium, or Strong
    """
    issues = []
    score = 0

    # trim accidental spaces
    if password != password.strip():
        issues.append("Remove spaces at the start or end.")
        password = password.strip()

    # length
    if len(password) >= MIN_LENGTH:
        score += 2
    else:
        issues.append(f"Password must be at least {MIN_LENGTH} characters long.")

    # uppercase
    if has_uppercase(password):
        score += 1
    else:
        issues.append("Include at least one uppercase letter (A–Z).")

    # lowercase
    if has_lowercase(password):
        score += 1
    else:
        issues.append("Include at least one lowercase letter (a–z).")

    # number
    if has_number(password):
        score += 1
    else:
        issues.append("Include at least one number (0–9).")

    # special character
    if has_special(password):
        score += 1
    else:
        issues.append(f"Include at least one special character (e.g., {SPECIAL_CHARS[:6]}…).")

    # common password
    if password.lower() in COMMON_PASSWORDS:
        issues.append("Password is too common (like 'password' or '123456').")
    else:
        score += 1

    # repeated characters
    if not repeats_three_times(password):
        score += 1
    else:
        issues.append("Avoid repeating the same character 3+ times in a row.")

    # spaces inside
    if " " not in password:
        score += 1
    else:
        issues.append("Do not include spaces in the middle of your password.")

    # final rating
    if score <= 3:
        rating = "Weak"
    elif score <= 6:
        rating = "Medium"
    else:
        rating = "Strong"

    return issues, rating


# ---------------- MAIN PROGRAM ---------------- #

print("="*50)
print("Welcome to the Password Strength Checker")
print("="*50)

while True:
    pwd = input("\nEnter a password to test: ")
    problems, rating = evaluate_password(pwd)

    print("\n Your password:", pwd)
    print("Strength rating:", rating)

    if not problems and rating == "Strong":
        print("Great! Your password is strong.")
        break
    else:
        print("\nSuggestions to improve:")
        for prob in problems:
            print(textwrap.fill(" - " + prob, width=70))
        print("\nPlease try again...")
