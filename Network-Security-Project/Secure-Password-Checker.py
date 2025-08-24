"""
Password Strength Tester (Beginner-Friendly Edition)
----------------------------------------------------
A simple interactive tool that keeps asking for a password
until you enter one that meets multiple strength checks.
"""

import string   # provides ready-made sets of letters & digits
import textwrap # lets us format long feedback messages nicely

# ---------------- SETTINGS ---------------- #
MIN_LENGTH = 12
SPECIALS = "!£$%^&*()-_=+{}[]:;@'~#<,>.?/"
COMMON_PASSWORDS = {
    "password", "12345678", "passw0rd", "letmein", "qwerty", "qwerty123", "123456", "123456789", 
    "111111", "iloveyou", "admin", "welcome", "dragon", "abc123"
}

# ---------------- HELPER FUNCTIONS ---------------- #
def contains_uppercase(text):
    return any(ch in string.ascii_uppercase for ch in text)

def contains_lowercase(text):
    return any(ch in string.ascii_lowercase for ch in text)

def contains_digit(text):
    return any(ch in string.digits for ch in text)

def contains_special(text):
    return any(ch in SPECIALS for ch in text)

def has_repeated_three(text):
    # scan through the string — if the same character repeats
    # 3+ times in a row, we flag it as insecure
    for i in range(len(text) - 2):
        if text[i] == text[i+1] == text[i+2]:
            return True
    return False

# ---------------- CORE CHECKING LOGIC ---------------- #
def check_password(pw):
    issues = []  # collect "what’s wrong" notes here
    score = 0    # password earns points as it passes checks

    # trim spaces from start/end (accidental whitespace is bad)
    if pw != pw.strip():
        issues.append("Remove spaces at the start or end.")
        pw = pw.strip()

    # check rules one by one
    if len(pw) >= MIN_LENGTH:
        score += 2   # longer length = double points
    else:
        issues.append(f"Password must be at least {MIN_LENGTH} characters long.")

    if contains_uppercase(pw):
        score += 1
    else:
        issues.append("Add at least one UPPERCASE letter (A–Z).")

    if contains_lowercase(pw):
        score += 1
    else:
        issues.append("Add at least one lowercase letter (a–z).")

    if contains_digit(pw):
        score += 1
    else:
        issues.append("Add at least one number (0–9).")

    if contains_special(pw):
        score += 1
    else:
        issues.append(f"Add at least one special character (e.g., {SPECIALS[:6]}…).")

    # extra security hygiene checks
    if pw.lower() in COMMON_PASSWORDS:
        issues.append("Password is too common (think 'password' or '123456').")
    else:
        score += 1

    if not has_repeated_three(pw):
        score += 1
    else:
        issues.append("Avoid typing the same character 3+ times in a row.")

    if " " not in pw:
        score += 1
    else:
        issues.append("Do not include spaces in the middle of your password.")

    # translate score into a simple rating
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
    password = input("\nEnter a password to check: ")
    problems, rating = check_password(password)

    print("\n Your password:", password)
    print("Strength rating:", rating)

    if not problems and rating == "Strong":
        print("Nice work! Your password checks out as strong.")
        break
    else:
        print("\n Things you could improve:")
        for prob in problems:
            # keep long suggestions wrapped to the screen width
            print(textwrap.fill(" - " + prob, width=70))
        print("\nPlease try again...")
