import hashlib
import random
import string
import textwrap

# ---------------- CONFIG (rules + constants) ---------------- #
MIN_LENGTH = 12   # minimum number of characters a password must have
SPECIALS = "!£$%^&*()-_=+{}[]:;@'~#<,>.?/"  # list of allowed special characters
COMMON_PASSWORDS = {  # a set of very common passwords (weak and unsafe)
    "password", "12345678", "passw0rd", "letmein", "qwerty", "qwerty123", "123456", "123456789", 
    "111111", "iloveyou", "admin", "welcome", "dragon", "abc123"
}

# ---------------- HELPER FUNCTIONS ---------------- #
# These functions each test a specific rule for password safety

def contains_uppercase(text):
    # returns True if the password has at least one uppercase letter (A–Z)
    return any(ch in string.ascii_uppercase for ch in text)

def contains_lowercase(text):
    # returns True if the password has at least one lowercase letter (a–z)
    return any(ch in string.ascii_lowercase for ch in text)

def contains_digit(text):
    # returns True if the password has at least one number (0–9)
    return any(ch in string.digits for ch in text)

def contains_special(text):
    # returns True if the password has at least one special character (like ! or @)
    return any(ch in SPECIALS for ch in text)

def has_repeated_three(text):
    # checks if the same character appears 3 times in a row
    # e.g. "aaa" or "111" would fail this test
    for i in range(len(text) - 2):
        if text[i] == text[i+1] == text[i+2]:
            return True
    return False

def check_password(pw):
    """
    This function checks the password against all rules.
    It returns:
      - a list of issues (things to fix)
      - a rating: Weak, Medium, or Strong
    """
    issues = []  # list that stores problems found with the password
    score = 0    # the password gets points for every good rule it passes

    # rule 1: no spaces at the start or end
    if pw != pw.strip():
        issues.append("Remove spaces at the start or end.")
        pw = pw.strip()  # removes spaces automatically

    # rule 2: check length
    if len(pw) >= MIN_LENGTH:
        score += 2  # long passwords get more points
    else:
        issues.append(f"Password must be at least {MIN_LENGTH} characters long.")

    # rule 3: must have at least one uppercase letter
    if contains_uppercase(pw):
        score += 1
    else:
        issues.append("Add at least one UPPERCASE letter (A–Z).")

    # rule 4: must have at least one lowercase letter
    if contains_lowercase(pw):
        score += 1
    else:
        issues.append("Add at least one lowercase letter (a–z).")

    # rule 5: must have at least one number
    if contains_digit(pw):
        score += 1
    else:
        issues.append("Add at least one number (0–9).")

    # rule 6: must have at least one special symbol
    if contains_special(pw):
        score += 1
    else:
        issues.append(f"Add at least one special character (e.g., {SPECIALS[:6]}…).")

    # rule 7: password must not be a known common password
    if pw.lower() in COMMON_PASSWORDS:
        issues.append("Password is too common (e.g., 'password', '123456').")
    else:
        score += 1

    # rule 8: avoid repeating the same character 3+ times
    if not has_repeated_three(pw):
        score += 1
    else:
        issues.append("Avoid repeating the same character 3 or more times in a row.")

    # rule 9: no spaces in the middle of the password
    if " " not in pw:
        score += 1
    else:
        issues.append("Avoid spaces inside the password.")

    # final: decide strength based on score
    if score <= 3:
        rating = "Weak"
    elif score <= 6:
        rating = "Medium"
    else:
        rating = "Strong"

    return issues, rating

def hash_password(password):
    """
    Turns the password into a secure hash using SHA256.
    - Hashing is one-way (you can’t get the original password back).
    - Used for storing passwords safely in databases.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def generate_otp():
    """
    Creates a 6-digit random number for 2FA.
    This simulates sending a one-time code to the user.
    """
    return str(random.randint(100000, 999999))

# ---------------- MAIN PROGRAM ---------------- #
print("="*50)
print("Welcome to Secure Login (2FA System)")
print("="*50)

# Step 1: Ask user for a password and check it
while True:
    password = input("\nEnter a password to register: ")
    issues, rating = check_password(password)

    print("\nYour password:", password)
    print("Strength rating:", rating)

    if not issues and rating == "Strong":
        print(" Strong password! Proceeding to 2FA...")
        break
    else:
        # show what needs fixing
        print("\n Improvements needed:")
        for prob in issues:
            print(textwrap.fill(" - " + prob, width=70))
        print("\nTry again...")

# Step 2: Hash and show the password (this simulates saving it securely)
hashed_pw = hash_password(password)
print("\nYour password has been hashed for secure storage:")
print(hashed_pw)

# Step 3: Generate and display a 6-digit OTP (in real life sent via SMS/email)
otp = generate_otp()
print("\nA one-time verification code has been sent to your device:")
print(otp)

# Step 4: Ask the user to enter the OTP (3 tries allowed)
attempts = 3
while attempts > 0:
    entered_otp = input("\nEnter the 6-digit code: ")
    if entered_otp == otp:
        print(" 2FA verified. Login successful!")
        break
    else:
        attempts -= 1
        print(f" Incorrect code. Attempts left: {attempts}")

if attempts == 0:
    print(" Too many failed attempts. Access denied.")
