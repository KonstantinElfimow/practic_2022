import numpy as np
from PIL import Image
from crc8 import crc8


def decode_from_png_to_jpeg(png_filename: str) -> None:
    # получим 3-мерную матрицу RGB из decrypted_PNG.png
    img = Image.open(png_filename).convert('RGB')
    matrix = np.array(img)

    height, width, rgb = matrix.shape
    ba_rec = []
    for y in range(height):
        line = matrix[y]
        for x in range(width):
            p = line[x]

            color = p[0]
            color = (color << 8) | p[1]
            color = (color << 8) | p[2]

            print(y, x)
            print(color)
            crc8_ba = crc8(bytearray(np.int32(color)), 0xFF)

            ba_rec.append(crc8_ba.digest())

    with open('output_2/decoded_JPEG.jpeg', "wb") as decoded_JPEG:
        for ba in ba_rec:
            decoded_JPEG.write(bytes(ba))
