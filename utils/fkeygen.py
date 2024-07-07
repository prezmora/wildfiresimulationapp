from cryptography.fernet import Fernet

# Generate an encryption key
key = Fernet.generate_key()

# Print the key
print(f"ENCRYPTION_KEY={key.decode()}")
