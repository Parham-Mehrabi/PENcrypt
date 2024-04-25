import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet



def create_key(password: str, iterations=700000):
    """ encrypt the password and generate a salt for it """
    salt = os.urandom(16)
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    salt_rounds = base64.b64encode((f"{salt}:{iterations}").encode())
    return key, salt_rounds

def recreate_key(password:str, salt:str, round:str):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=int(round)
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_data(key:bytes, raw_data:str) -> bytes:
    """ encrypt data with given key """
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data=raw_data.encode())
    return encrypted_data


def decrypt_data(key:bytes, encrypted_data:bytes) -> bytes:
    """ decrypt data with given key """
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data
