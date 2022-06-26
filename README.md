# practic_2022
Практика ИБ (2022)

Задачи: 
- знакомство с базовыми криптографическими преобразованиями – шифрованием / расшифрованием, режимами шифрования, хешированием данных;
- знакомство со стеганографическими преобразованиями; 
- получение навыков работы с криптографическими библиотеками.

Форма отчета: 
Краткое описание алгоритмов + исходный код, расшифрованные/декодированные изображения, расшифрованная парольная фраза.


Задание 1. В дампе памяти «dump_#.DMP» содержится криптографический ключ длиной 128 бит, необходимый для расшифрования сообщения «encr», являющегося изображением формата PNG. Известно, что для шифрования применялся алгоритм AES в режиме ECB. Написать алгоритм для извлечения ключа и, используя одну из стандартных криптографических библиотек, расшифровать сообщение. 
Подсказка 1. Для создания симметричных ключей шифрования могут использоваться генераторы случайных числовых последовательностей -> сами ключи будут обладать определенными свойствами, такими как высокая энтропия, близкий к равномерному закон распределения двоичных разрядов ключа и т.д. Данные свойства можно учитывать при поиске возможных ключей в дампе.
Подсказка 2. Ключ в дампе встречается дважды.
Результат выполнения: 128-битный ключ  , расшифрованное сообщение – изображение   формата PNG.
 
Задание 2. Внутри расшифрованного изображения   содержится изображение-сообщение  . Для его извлечения используйте следующий алгоритм. Для каждого пикселя кадра   (в режиме RGB пиксель представляется как целое int32_t, синий канал в младшем байте, старший байт – 0x00) вычисляется циклический избыточный код CRC8 по одному из стандартных алгоритмов. Полученное значение – очередной байт (uint8_t) записывается в выходной байтовый массив, который сохраняется как бинарный файл   после обхода всех пикселей на  . Используется построчный порядок обхода пикселей изображения – слева направо, сверху вниз. Для корректного извлечения информации необходимо определить вид порождающего полинома в алгоритме CRC8.
Подсказка 1. Метаданные в   (ImageMagick).
Подсказка 2. Для целевого алгоритма CRC8 значение кода от строки password равно 0xCF.
Результат выполнения: Декодированное сообщение – изображение   формата JPEG.

Задание 3. Расшифровать сообщение – 16-ти символьный пароль, «записанный» в  . Известно, что для шифрования применялся алгоритм AES в режиме CBC, 128-битный ключ   из задания 1 использовался в качестве вектора инициализации для режима СBС. 128-битный ключ шифрования   формировался путем вычисления MD5-хеша от «чистого» JPEG-файла  .
Подсказка 1. JPEG, маркер 0xFFD9 (первый).
Подсказка 2.  , где  – алгоритм AES,   – 128-битный ключ, на котором реализуется расшифрование,   – «очищенный» JPEG-файл (без доп.нагрузки),  – вектор инициализации, используемый в CBC режиме.
Результат выполнения: Расшифрованный 16-ти символьный пароль  .
