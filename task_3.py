from Crypto.Cipher import AES
from hashlib import md5


def decode_password_from_jpeg_with_aes_cbc(filename: str, iv: bytes) -> bytes:
    try:
        with open(filename, 'rb') as file:

            # "Очищаем" .jpg
            marker_end = bytes.fromhex('FFD9')
            clear_jpeg = b''
            while True:
                b = file.read(2)
                clear_jpeg += b
                if b == marker_end:
                    break

            # Получаем хэш MD5.
            key = md5(clear_jpeg).digest()
            # Инициализируем AES.
            obj = AES.new(key, AES.MODE_CBC, iv)

            # Блок шифрования в AES 128-битный всегда, поэтому CHUNKSIZE=16.
            CHUNKSIZE: int = 16
            # Читаем первый блок данных размером 16 байт после "чистого" .jpg.
            data = file.read(CHUNKSIZE)

            # Получаем пароль.
            password = obj.decrypt(data)
    except FileNotFoundError:
        print("Невозможно открыть файл")
    return password
