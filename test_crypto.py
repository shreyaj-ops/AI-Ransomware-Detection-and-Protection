from crypto_module import encrypt_file, decrypt_file

password = "MySecret123"

# Encrypt
encrypt_file(
    "test_file.txt",
    "test_file.enc",
    password
)

print("File encrypted successfully!")

# Decrypt
success = decrypt_file(
    "test_file.enc",
    "decrypted_test_file.txt",
    password
)

if success:
    print("File decrypted successfully!")
else:
    print("Decryption failed!")