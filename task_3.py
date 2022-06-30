from Crypto.Cipher import AES
from hashlib import md5
import numpy as np


def decode_password_from_jpeg_with_aes_cbc(filename: str, iv: bytes) -> bytes:
    file = open(filename, "rb")

    file.close()

    key = md5()
    obj = AES.new(key, AES.MODE_CBC, iv)
    password = obj.decrypt()