"""
This program simulates a secure mini chat where all messages are encrypted and decrypted using Fernet.  
It also begins with basic security questions to reinforce safe practices before allowing the chat.
"""

from cryptography.fernet import Fernet

# ------------------- Security Gate -------------------

def run_security_check():
    """
    Ask the user a few quick security questions.
    If any answer is incorrect, access is denied.
    """
    questions = [
        ("What does HTTPS mean your connection is? ", "secure"),
        ("Should passwords be shared with others? ", "no"),
        ("Is encryption useful for privacy? ", "yes")
    ]
    for q, expected in questions:
        response = input(q).strip().lower()
        if response != expected:
            print("Access denied. Review basic security concepts.\n")
            return False
    print("Security check passed. You may start chatting!\n")
    return True


# ------------------- Encryption Helpers -------------------

def encrypt_text(plain: str, cipher: Fernet) -> bytes:
    """Encrypt a message string and return encrypted bytes."""
    return cipher.encrypt(plain.encode())


def decrypt_text(encrypted: bytes, cipher: Fernet) -> str:
    """Decrypt an encrypted message and return the original string."""
    return cipher.decrypt(encrypted).decode()


# ------------------- Main Chat Loop -------------------

def main():
    print("=== Secure Chat ===\n")

    if not run_security_check():
        return

    # Generate a symmetric session key
    key = Fernet.generate_key()
    cipher = Fernet(key)
    print("A session key has been generated for encryption.\n")
    print("Instructions: type 'exit' at any time to leave the chat.\n")

    while True:
        # User 1 sends a message
        msg1 = input("User1: ")
        if msg1.lower() == "exit":
            break
        enc1 = encrypt_text(msg1, cipher)
        dec1 = decrypt_text(enc1, cipher)
        print(f"User2 sees (decrypted): {dec1}\n")

        # User 2 sends a reply
        msg2 = input("User2: ")
        if msg2.lower() == "exit":
            break
        enc2 = encrypt_text(msg2, cipher)
        dec2 = decrypt_text(enc2, cipher)
        print(f"User1 sees (decrypted): {dec2}\n")

    print("Chat ended. All messages in this session were encrypted.")


if __name__ == "__main__":
    main()