from task_1 import read_keys_from, create_filtered_list_from_key_dict, decrypt_as_png_with_potential_keys, save_key_in

if __name__ == '__main__':
    # Формируем словарь (ключ - частота встречаемости).
    dict_keys = read_keys_from('resources/dump_010.DMP')
    # Далее отсеиваем все ключи, которые встречаются реже 2 раз.
    keys = create_filtered_list_from_key_dict(dict_keys)

    if len(keys) != 0:
        print(" //// Дешифрование //// ")
        is_decrypted, key = decrypt_as_png_with_potential_keys('resources/encr_010', keys)
        if is_decrypted:
            print("Файл успешно дешифрован!")
            print(f'Ключ шифрования: {key}')

            # Записываем ключ в бинарный файл key.bin для последующей работы.
            save_key_in('output_1/key.bin', key)
        else:
            print("Не удалось дешифровать файл")
    else:
        print("Ключи отсутствуют")
