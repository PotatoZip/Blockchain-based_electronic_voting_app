import base64, os
from cryptography.fernet import Fernet
from django.conf import settings


def get_fernet() -> Fernet:
    key = settings.ENCRYPTION_KEY  # ze środowiska
    return Fernet(key)


def encrypt_bytes(data: bytes) -> bytes:
    return get_fernet().encrypt(data)


def decrypt_bytes(token: bytes) -> bytes:
    return get_fernet().decrypt(token)
