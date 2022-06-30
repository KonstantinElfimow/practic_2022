from task_1 import read_keys_from, create_filtered_list_from_key_dict, decrypt_pngfile_with_aes_ecb, save_binary_data
from task_2 import decode_from_png_to_jpeg_with_crc8


def task_1():
    """ Task 1 """
    # Формируем словарь (ключ - частота встречаемости).
    dump_filename = 'resources/dump_010.DMP'
    dict_keys = read_keys_from(dump_filename)
    # Далее отсеиваем все ключи, которые встречаются реже 2 раз.
    keys = create_filtered_list_from_key_dict(dict_keys)

    if len(keys) != 0:
        print(" //// Дешифрование //// ")

        encr_filename = 'resources/encr_010'
        is_decrypted, plaintext, key = decrypt_pngfile_with_aes_ecb(encr_filename, keys)
        if is_decrypted:
            print("Файл успешно дешифрован!")

            # Записываем ключ в бинарный файл key.bin для последующей работы.
            key_filename = 'output_1/key.bin'
            save_binary_data(key_filename, key)
            # Сохранить оригинальный файл.
            png_filename = 'output_1/decrypted_PNG.png'
            save_binary_data(png_filename, plaintext)

            # Переводим ключ из bytes в hex
            hex_key = bytes.hex(key)
            print(f'Ключ шифрования в hex представлении: {hex_key}')
        else:
            print("Не удалось дешифровать файл")
            exit(0)
    else:
        print("Ключи отсутствуют")
        exit(0)


def task_2():
    """ Task 2 """
    png_filename = 'output_1/decrypted_PNG.png'
    jpeg_filename = 'output_2/decoded_JPEG.jpg'
    decode_from_png_to_jpeg_with_crc8(png_filename, jpeg_filename)


if __name__ == '__main__':
    # task_1()
    task_2()

