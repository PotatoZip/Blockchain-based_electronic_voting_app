from cryptography.fernet import Fernet
from django.conf import settings
import base64
import hashlib


def _fernet():
    # klucz z SECRET_KEY → 32 bajty (Fernet wymaga 32 urlsafe base64)
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))


def encrypt_bytes(b: bytes) -> bytes:
    return _fernet().encrypt(b)


def decrypt_bytes(token: bytes) -> bytes:
    return _fernet().decrypt(token)
