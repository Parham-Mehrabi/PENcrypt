import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def create_key(password: str, iterations=700000):
    """ encrypt the password and generate a salt for it """
    salt = salt if salt else os.urandom(16)
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    salt_rounds = base64.b64encode((f"{salt.decode()}:{iterations}").encode())

    return key, salt_rounds


