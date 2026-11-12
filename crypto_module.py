import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_key(password, salt):
    """Derive a 256-bit AES key from a password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )

    return kdf.derive(password.encode("utf-8"))


def encrypt_file(input_file, output_file, password):
    """Encrypt a file using AES-256-GCM."""

    salt = os.urandom(16)
    nonce = os.urandom(12)

    with open(input_file, "rb") as file:
        data = file.read()

    key = derive_key(password, salt)

    aesgcm = AESGCM(key)

    encrypted_data = aesgcm.encrypt(
        nonce,
        data,
        None
    )

    # File format:
    # SALT (16 bytes) + NONCE (12 bytes) + CIPHERTEXT
    with open(output_file, "wb") as file:
        file.write(salt)
        file.write(nonce)
        file.write(encrypted_data)


def decrypt_file(input_file, output_file, password):
    """Decrypt an AES-256-GCM encrypted file."""

    try:

        with open(input_file, "rb") as file:
            encrypted_data = file.read()

        salt = encrypted_data[:16]
        nonce = encrypted_data[16:28]
        ciphertext = encrypted_data[28:]

        key = derive_key(password, salt)

        aesgcm = AESGCM(key)

        decrypted_data = aesgcm.decrypt(
            nonce,
            ciphertext,
            None
        )

        with open(output_file, "wb") as file:
            file.write(decrypted_data)

        return True

    except Exception:
        return False