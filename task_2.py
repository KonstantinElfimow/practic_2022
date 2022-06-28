import numpy as np
from PIL import Image
from crc8 import crc8


def decode_from_png_to_jpeg(png_filename: str, jpeg_filename: str) -> None:
    # получим 3-мерную матрицу RGB из decrypted_PNG.png
    img = Image.open(png_filename).convert('RGB')
    matrix = np.asarray(img)
    img.close()

    # высота, ширина, rgb
    height, width, _rgb = matrix.shape
    ba_rec = []

    for y in range(height):
        line = matrix[y]
        for x in range(width):
            p = line[x]

            # формируем целое на основе трех байт rgb (старший байт будет нулевым)
            color = int(p[0])  # r
            color = (color << 8) | int(p[1])  # rg
            color = (color << 8) | int(p[2])  # rgb

            # print(y, x)
            # print(color)

            b_color = color.to_bytes(3, byteorder="big", signed=False)
            # print(b_color)
            crc8_ = crc8()
            crc8_.update(bytearray(b_color))
            ba_rec.append(crc8_.digest())
            # ba_rec.append(crc8_.to_bytes(1, byteorder="little", signed=False))

    with open(jpeg_filename, "wb") as file:
        for ba in ba_rec:
            print(ba)
            file.write(ba)
