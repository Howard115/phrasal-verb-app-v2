from cryptography.fernet import Fernet
from app.config import settings
from base64 import b64encode

def get_encryption_key():
    # Use existing SECRET_KEY to derive a valid Fernet key
    # Fernet requires a 32-byte key that is base64-encoded
    key = b64encode(settings.SECRET_KEY.encode()[:32].ljust(32, b'0'))
    return Fernet(key)

def encrypt_api_key(api_key: str) -> str:
    f = get_encryption_key()
    return f.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_api_key: str) -> str:
    f = get_encryption_key()
    return f.decrypt(encrypted_api_key.encode()).decode() 