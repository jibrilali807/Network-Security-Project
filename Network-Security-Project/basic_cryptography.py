
"""
This program demonstrates simple text encryption and decryption
using the Fernet symmetric encryption method from the cryptography library.
It allows the user to enter a message, which is then encrypted and
immediately decrypted back to verify the process.
"""


from cryptography.fernet import Fernet


def create_cipher():
    """
    Create a Fernet cipher with a generated key (not shown to user).
    The key is created in memory and used only during this run.
    """
    key = Fernet.generate_key()
    return Fernet(key)


def encrypt_message(cipher, message: str) -> str:
    """
    Encrypt a string message using the given cipher.
    Returns the encrypted text (as a string).
    """
    encrypted_bytes = cipher.encrypt(message.encode())
    return encrypted_bytes.decode()


def decrypt_message(cipher, encrypted_text: str) -> str:
    """
    Decrypt an encrypted string using the given cipher.
    Returns the original plaintext message.
    """
    decrypted_bytes = cipher.decrypt(encrypted_text.encode())
    return decrypted_bytes.decode()


def main():
    print("\n--- Encryption Tool ---\n")

    # Allows to create a Fernet cipher
    cipher = create_cipher()

    # Asks the user for input text
    user_text = input("Enter the text you want to encrypt: ")

    # Encrypt the input text
    encrypted = encrypt_message(cipher, user_text)
    print(f"\nEncrypted Message: {encrypted}")

    # Decrypt the encrypted text
    decrypted = decrypt_message(cipher, encrypted)
    print(f"Decrypted Message (verification): {decrypted}\n")


if __name__ == "__main__":
    main()