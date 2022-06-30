from task_1 import read_keys_from, filter_keys_by_frequency, decrypt_pngfile_with_aes_ecb
from task_2 import decode_data_from_file_with_crc8
from task_3 import decode_password_from_jpeg_with_aes_cbc


def save_binary_data(filename: str, data: bytes):
    """ Сохраняем данные в файл в байтовом представлении """
    with open(filename, "wb") as file:
        try:
            file.write(data)
        finally:
            file.close()


def task_1():
    """ Task 1 """

    print("Task_1")

    # Формируем словарь (ключ - частота встречаемости).
    dump_filename = 'resources/dump_010.DMP'
    dict_keys = read_keys_from(dump_filename)

    # Далее отсеиваем все ключи, которые не встречаются 2 раза.
    keys = filter_keys_by_frequency(dict_keys, 2)

    if len(keys) != 0:
        encr_filename = 'resources/encr_010'
        is_decrypted, plaintext, key = decrypt_pngfile_with_aes_ecb(encr_filename, keys)
        if is_decrypted:
            print("Файл успешно дешифрован!")

            # Выводим ключ в консоль
            print(f'Ключ шифрования в hex представлении: {bytes.hex(key)}')

            # Записываем ключ в бинарный файл key.bin для последующей работы.
            key_filename = 'output_1/key.bin'
            save_binary_data(key_filename, key)

            # Сохранить оригинальный файл.
            png_filename = 'output_1/decrypted_PNG.png'
            save_binary_data(png_filename, plaintext)
        else:
            print("Не удалось дешифровать файл")
            exit(0)
    else:
        print("Ключи отсутствуют")
        exit(0)


def task_2():
    """ Task 2 """

    print("Task_2")

    # Читаем новые данные из .png файла с использованием алгоритма crc8,
    # которые будут являться данными для записи в .jpeg файл.
    png_filename = 'output_1/decrypted_PNG.png'
    decoded_data = decode_data_from_file_with_crc8(png_filename)

    # Записываем новые данные в .jpeg файл
    jpeg_filename = 'output_2/decoded_JPEG.jpg'
    save_binary_data(jpeg_filename, decoded_data)


def task_3():
    """ Task 3 """

    print("Task_3")

    jpeg_filename = 'output_2/decoded_JPEG.jpg'

    # Читаем ключ, который будем вектором инициализации.
    key_filename = 'output_1/key.bin'
    key_file = open(key_filename, "rb")
    key = key_file.read()
    key_file.close()

    # Получаем пароль.
    password = decode_password_from_jpeg_with_aes_cbc(jpeg_filename, key)

    # Выводим пароль.
    print(f'Пароль: {password}')

    # Сохраняем пароль.
    password_filename = 'output_3/password.bin'
    save_binary_data(password_filename, password)


if __name__ == '__main__':
    # task_1()
    task_2()
    # task_3()
