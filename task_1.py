from Crypto.Cipher import AES
import numpy as np


def _entropy(labels: bytearray) -> int:
    """ Вычисление энтропии вектора из 0-1 """
    n_labels = len(labels)

    if n_labels <= 1:
        return 0

    counts = np.bincount(labels)
    probs = counts[np.nonzero(counts)] / n_labels
    n_classes = len(probs)

    if n_classes <= 1:
        return 0
    return - np.sum(probs * np.log(probs)) / np.log(n_classes)


_png_signature: bytes = b'\x89PNG\r\n\x1a\n'  # '0x89', '0x50', '0x4E', '0x47', '0x0D', '0x0A', '0x1A', '0x0A'


def _check_for_png(decrypted_data: bytes) -> bool:
    """ Проверяем сигнатуру decrypted_data на .png файл """
    if _png_signature == decrypted_data[:8]:
        return True
    return False


def read_keys_from(dump_filename: str) -> dict:
    """ Находим все потенциальные 128-битные ключи шифрования, которые встречаются в .DMP. Записываем их в словарь """
    keys_count = {}
    try:
        with open(dump_filename, 'rb') as dump_file:
            ptr = 0
            CHUNKSIZE: int = 16
            while True:
                # Начиная с 0 указателя с последующим шагом в 1 байт в файле,
                # мы считываем по 16 байт данных (это наши кандидаты в ключи шифрования).
                dump_file.seek(ptr)
                potential_key = dump_file.read(CHUNKSIZE)
                ptr += 1

                # Если длина ключа составляет меньше 16 байт,
                # то значит, мы достигли конца файла,
                # поэтому прерываем цикл.
                key_array = bytearray(potential_key)
                if len(key_array) != CHUNKSIZE:
                    break

                # Предположим, что ключ выбран неслучайно,
                # поэтому ключи будут обладать определенными свойствами,
                # такими как высокая энтропия, близкая к равномерному
                # закону распределения двоичных разрядов ключа
                if _entropy(key_array) > 0.99:
                    # Если энтропия ключа достаточно высокая и удовлетворяет условию,
                    # то запоминаем этот ключ и запоминаем его частоту встречаемости в файле.
                    # Конкретно нам будет интересна частота 2 (по условию задачи).
                    keys_count[potential_key] = keys_count.get(potential_key, 0) + 1
                    # print(potential_key)
    except FileNotFoundError:
        print("Невозможно открыть файл")
    return keys_count


def filter_keys_by_frequency(dict_keys: dict, frequency: int) -> list:
    """ Фильтруем ключи, которые встречаются с определённой частотой. Записываем их в новый список """
    filtered_k = []
    for k, v in dict_keys.items():
        if v == 2:
            filtered_k.append(k)
    return filtered_k


def decrypt_pngfile_with_aes_ecb(filename: str, potential_keys: list):
    """ Дешифруем файл filename в .png файл """
    try:
        with open(filename, 'rb') as file:
            # Блок шифрования в AES 128-битный всегда, поэтому CHUNKSIZE=16.
            CHUNKSIZE: int = 16
            # Прочитаем первый блок данных размером 16 байт.
            ciphertext = file.read(CHUNKSIZE)
            for session_key in potential_keys:

                # Нас интересует каким образом session_key дешифрует первый блок данных из encr_10.
                # Если первые 8 байт plaintext будут совпадать с сигнатурой .png,
                # то мы нашли ключ.
                obj = AES.new(session_key, AES.MODE_ECB)
                plaintext = obj.decrypt(ciphertext)
                if _check_for_png(plaintext):
                    # После проверки дешифрации первого блока данных можно дешифровать весь encr_10.
                    # Смещаем указатель в начало файла.
                    file.seek(0)
                    ciphertext = file.read()
                    plaintext = obj.decrypt(ciphertext)

                    return True, plaintext, session_key
    except FileNotFoundError:
        print("Невозможно открыть файл")
    return False, None, None
