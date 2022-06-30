from Crypto.Cipher import AES
from hashlib import md5


# jpeg_signature: list = list(b'\xff\xd8\xff\xe0')  # '0xff', '0xd8', '0xff', '0xe0'

def decode_password_from_jpeg_with_aes_cbc(filename: str, iv: bytes) -> bytes:
    try:
        with open(filename, 'rb') as file:

            clear_jpeg = b''

            key = md5(clear_jpeg).digest()
            obj = AES.new(key, AES.MODE_CBC, iv)

            # Смещаем указатель в начало файла.
            file.seek(0)
            # Блок шифрования в AES 128-битный всегда, поэтому CHUNKSIZE=16.
            CHUNKSIZE: int = 16
            # Прочитаем первый блок данных размером 16 байт.
            data = file.read(CHUNKSIZE)

            # Получаем пароль.
            password = obj.decrypt(data)
    except FileNotFoundError:
        print("Невозможно открыть файл")
    return password
