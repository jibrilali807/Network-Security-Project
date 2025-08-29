"""
This program lets you store sensitive information safely using encryption.
You can save login credentials, private notes, and bank/card info securely.
"""

import os
import json
from cryptography.fernet import Fernet


# ------------------- Key Management -------------------

KEY_FILE = "secret.key"  # File to store encryption key
DATA_FILE = "secure_data.json"  # File to store encrypted data

def get_encryption_key():
    """Get the encryption key. Make a new one if it doesn't exist."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key = f.read()  # Read key from file
    else:
        key = Fernet.generate_key()  # Create a new key
        with open(KEY_FILE, "wb") as f:
            f.write(key)  # Save key for later
    return key

cipher = Fernet(get_encryption_key())  # Create a Fernet object to encrypt/decrypt


# ------------------- Data Handling -------------------

def load_secure_data():
    """Load saved data from file, or start with an empty dictionary if none exists."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            encrypted = f.read()  # Read encrypted data
        try:
            decrypted = cipher.decrypt(encrypted).decode()  # Decrypt it
            return json.loads(decrypted)  # Convert JSON string to dict
        except:
            return {}  # If error, return empty dict
    return {}  # If file doesn't exist, return empty dict

def save_secure_data():
    """Encrypt the data and save it to a file."""
    encrypted = cipher.encrypt(json.dumps(stored_data).encode())
    with open(DATA_FILE, "wb") as f:
        f.write(encrypted)


# ------------------- User Actions -------------------

def add_secure_entry():
    """Ask the user what they want to save and store it safely."""
    print("\nChoose what to store:")
    print("1. Credentials (username & password)")
    print("2. Private Note")
    print("3. Bank/Card Info")
    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "1":
        site = input("Website/Service Name: ")
        username = input("Username: ")
        password = input("Password: ")
        stored_data[site] = {"type": "credentials", "username": username, "password": password}
    elif choice == "2":
        note_title = input("Note Title: ")
        content = input("Note Content: ")
        stored_data[note_title] = {"type": "note", "content": content}
    elif choice == "3":
        bank_name = input("Bank/Card Name: ")
        number = input("Card Number: ")
        expiry = input("Expiry Date: ")
        cvv = input("CVV: ")
        stored_data[bank_name] = {"type": "bank_info", "number": number, "expiry": expiry, "cvv": cvv}
    else:
        print("Invalid choice!")
        return

    save_secure_data()  # Save changes after adding
    print("Entry saved safely!")


def display_entries():
    """Show all saved entries in a readable way."""
    if not stored_data:
        print("No entries stored yet.")
        return

    print("\n--- Stored Entries ---")
    for name, info in stored_data.items():
        print(f"\nName: {name}")
        if info["type"] == "credentials":
            print(f"  Type: Credentials")
            print(f"  Username: {info['username']}")
            print(f"  Password: {info['password']}")
        elif info["type"] == "note":
            print(f"  Type: Note")
            print(f"  Content: {info['content']}")
        elif info["type"] == "bank_info":
            print(f"  Type: Bank/Card Info")
            print(f"  Number: {info['number']}")
            print(f"  Expiry: {info['expiry']}")
            print(f"  CVV: {info['cvv']}")


# ------------------- Main Menu Loop -------------------

stored_data = load_secure_data()  # Load saved data at start

while True:
    print("\n=== Secure Storage Menu ===")
    print("1. Add Entry")
    print("2. View Entries")
    print("3. Exit")
    menu_choice = input("Enter choice: ").strip()

    if menu_choice == "1":
        add_secure_entry()  # Let user add a new entry
    elif menu_choice == "2":
        display_entries()  # Show all entries
    elif menu_choice == "3":
        print("Exiting... Stay safe!")
        break
    else:
        print("Invalid choice. Please try again.")