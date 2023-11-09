from datetime import datetime
from random import randint

from bcrypt import hashpw, gensalt, checkpw
from cryptography.fernet import Fernet

from .settings import FERNET_KEY

ENCODE = "utf-8"
fernet = Fernet(FERNET_KEY)


def generate_hash(value: str) -> str:
    global ENCODE
    hashed = hashpw(bytes(value, encoding=ENCODE), gensalt(8))
    return hashed.decode(ENCODE)


def generate_fast_hash(value: str) -> str:
    global ENCODE
    hashed = hashpw(bytes(value, encoding=ENCODE), gensalt(4))
    return hashed.decode(ENCODE)


def compare_hash(value: str, hash: str) -> bool:
    global ENCODE
    if type(hash) != bytes:
        hash = bytes(hash, encoding=ENCODE)
    return checkpw(bytes(value, encoding=ENCODE), hash)


def generate_random_hash(fast: bool = False) -> str:
    if fast:
        hash = generate_fast_hash(f"{randint(1, 1000)}{datetime.now()}")
    else:
        hash = generate_hash(f"{randint(1, 100000000)}{datetime.now()}")
    hash = hash.replace("/", "").replace(".", "")
    return hash


def cryptograph_text(text: str) -> str:
    global fernet
    global ENCODE
    return fernet.encrypt(text.encode(ENCODE)).decode(ENCODE)


def decrypt_text(text: str) -> str:
    global fernet
    global ENCODE
    return fernet.decrypt(text).decode(ENCODE)
