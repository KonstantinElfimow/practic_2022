from task_1 import read_keys_from, create_filtered_list_from_key_dict, decrypt_as_png_with_potential_keys, save_key_in
from task_2 import decode_from_png_to_jpeg

if __name__ == '__main__':
    """ Task 1 """
    # Формируем словарь (ключ - частота встречаемости).
    dict_keys = read_keys_from('resources/dump_010.DMP')
    # Далее отсеиваем все ключи, которые встречаются реже 2 раз.
    keys = create_filtered_list_from_key_dict(dict_keys)

    if len(keys) != 0:
        print(" //// Дешифрование //// ")
        is_decrypted, key = decrypt_as_png_with_potential_keys('resources/encr_010', keys)
        if is_decrypted:
            print("Файл успешно дешифрован!")
            # Переводим ключ из bytes в hex
            hex_key = bytes.hex(key)
            print(f'Ключ шифрования в hex представлении: {hex_key}')

            # Записываем ключ в бинарный файл key.bin для последующей работы.
            save_key_in('output_1/key.bin', key)
        else:
            print("Не удалось дешифровать файл")
    else:
        print("Ключи отсутствуют")

    """ Task 2 """
    decode_from_png_to_jpeg('output_1/decrypted_PNG.png')
