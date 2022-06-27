from Crypto.Cipher import AES
import numpy as np


def _entropy(labels: bytearray):
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


def _save_decrypted_data_as_png(filename: str, decrypted_data: bytes):
    """ Сохраняем данные в .png файл (естественно, в бинарном представлении) """
    with open(filename, "wb") as file:
        try:
            file.write(decrypted_data)
        finally:
            file.close()


def _from_hex_chunks_to_bytes(hex_chunks: list):
    """ Переводим из hex list в bytes """
    str_hex_chunks = ""
    for hex_chunk in hex_chunks:
        str_hex_chunks += str(hex_chunk)
    return bytes.fromhex(str_hex_chunks)


def _check_for_png(decrypted_data: bytes):
    """ Проверяем сигнатуру decrypted_data на .png файл """
    png_hex_chunks = ['89', '50', '4E', '47', '0D', '0A', '1A', '0A']
    png_bytes_chunks: bytes = _from_hex_chunks_to_bytes(png_hex_chunks)

    if png_bytes_chunks == decrypted_data[:8]:
        return True
    return False


def read_keys_from(dump_filename: str):
    """ Находим все потенциальные 128-битные ключи шифрования, которые встречаются в .DMP. Записываем их в словарь """
    keys_count = {}
    try:
        with open(dump_filename, 'rb') as dump_file:
            ptr = 0
            while True:
                # Начиная с 0 указателя с последующим шагом в 1 байт в файле,
                # Мы считываем по 16 байт данных (это наши кандидаты в ключи шифрования).
                dump_file.seek(ptr)
                potential_key = dump_file.read(16)
                ptr += 1

                # Если длина ключа составляет меньше 16 байт,
                # то значит, мы достигли конца файла,
                # поэтому прерываем цикл.
                key_array = bytearray(potential_key)
                if len(key_array) != 16:
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


def create_filtered_list_from_key_dict(dict_keys: dict):
    """ Фильтруем ключи, которые встречаются дважды. Записываем их в новый список """
    filtered_k = []
    for k, v in dict_keys.items():
        if v == 2:
            filtered_k.append(k)
    return filtered_k


def save_key_in(key_filename: str, key: bytes):
    """ Сохраняем ключ в файл в bytes представлении """
    with open(key_filename, "wb") as key_file:
        try:
            key_file.write(key)
        finally:
            key_file.close()


def decrypt_as_png_with_potential_keys(encr_filename: str, keys_list: list):
    """ Дешифруем файл filename в .png файл """
    file = open(encr_filename, 'rb')
    try:
        # Блок шифрования в AES 128-битный всегда, поэтому CHUNKSIZE=16.
        CHUNKSIZE: int = 16
        # Прочитаем первый блок данных размером 16 байт.
        ciphertext = file.read(CHUNKSIZE)
        for session_key in keys_list:

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

                # Сохранить оригинальный файл.
                filename_d = 'output_1/decrypted_PNG.png'
                _save_decrypted_data_as_png(filename_d, plaintext)
                return True, session_key
    finally:
        file.close()
    return False, None
