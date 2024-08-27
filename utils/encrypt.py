import base64
import hashlib
from cryptography.fernet import Fernet
import os
import zlib
from dotenv import load_dotenv
import time
load_dotenv()



def get_key() -> bytes:
    key = os.getenv("ENCRYPT_KEY").encode()
    key = hashlib.sha256(key).digest()
    return base64.urlsafe_b64encode(key[:32])

def encrypt(data: bytes) -> bytes:
    key = get_key()
    f = Fernet(key)
    return f.encrypt(zlib.compress(data))

def decrypt(encrypted_data: bytes) -> bytes:
    key = get_key()
    f = Fernet(key)
    return zlib.decompress(f.decrypt(encrypted_data))


if __name__ == "__main__":
    s = time.perf_counter()
    data = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNjkxMzIxOCwiaWF0IjoxNzI0MzIxMjE4LCJqdGkiOiIwN2YyM2I2MWFlMzM0MjMzYjcwMmI1NTFlYTQwNGE0MiIsInVzZXJfaWQiOjIsImVtYWlsIjoicHR0NzQWQiOjIsImVtYWlsIjoicHR0NzQxQHB0dC5jb20ifQ.JeSrUkrZ8c-XAmlTNY6oT8iQ6s6_dacU0n-CHr9Evpc"
    encrypted_data = encrypt(data.encode())
    decrypted_data = decrypt(encrypted_data)
    print((time.perf_counter()-s))
    print(data == decrypted_data.decode())