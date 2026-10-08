# задание 1  
grep -o '^[a-z_][a-z0-9_-]*' /etc/passwd | sort
<img width="998" height="561" alt="image" src="https://github.com/user-attachments/assets/e38f40b5-332e-4ff3-8388-21097b22d7c1" />

# задание 2  
grep -v '^#' /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n 5
<img width="1221" height="218" alt="image" src="https://github.com/user-attachments/assets/8170c4c3-c6ca-4aa4-b413-4f4f1a8f511b" />

# задание 3  
1.
nano banner

2.
#!/usr/bin/env bash

# Берем текст из аргументов командной строки
text="${1:-Hello from RTU MIREA!}"
len=${#text}

# Рассчитываем длину и делаем рамку
line=$(printf '%*s' "$((len + 2))" '' | tr ' ' '-')

# Рисуем баннер на экране
echo "+${line}+"
echo "| ${text} |"
echo "+${line}+"

3.
chmod +x banner

4.
./banner 'Hello from RTU MIREA!'

<img width="800" height="159" alt="image" src="https://github.com/user-attachments/assets/0af98f7f-2d65-4b4a-adf9-938b372cf7d9" />

# задание 4
1) nano id_finder
2)
#!/usr/bin/env bash

# Проверяем: передал ли пользователь файл для анализа?
if [[ -z "$1" ]]; then
    echo "Использование: $0 <имя_файла>"
    exit 1
fi

# Ищем идентификаторы, сортируем их и убираем дубликаты
grep -oE '[a-zA-Z_][a-zA-Z0-9_]*' "$1" | sort -u

3) chmod +x id_finder
4) ./id_finder id_finder

<img width="422" height="443" alt="image" src="https://github.com/user-attachments/assets/d06f88cb-abc4-49bc-b859-7b19a6dbdcd2" />

# задание 5
1) nano reg
2)
#!/usr/bin/env bash

# Проверка на дурака (ввели ли имя файла)
if [[ -z "$1" ]]; then
    echo "Использование: $0 <имя_файла>"
    exit 1
fi

# 755 — даем права на запуск всем пользователям
chmod 755 "$1"

# Копируем в глобальную папку от имени администратора
sudo cp "$1" /usr/local/bin/

echo "Программа $1 успешно зарегистрирована!"

3) chmod +x reg  
4) ./reg banner (можно зарегистрировать что угодно)  
<img width="652" height="98" alt="image" src="https://github.com/user-attachments/assets/9170e43f-32da-4c56-afb8-9b15cd69e720" />

# задание 6
1) nano check_comment
2)
```#!/usr/bin/env bash

# Узнаем имя файла из аргумента
filename="$1"

# Проверяем, существует ли вообще такой файл?
if [[ ! -f "$filename" ]]; then
    echo "Ошибка: Файл не найден."
    exit 1
fi

# Читаем самую первую строчку файла
first_line=$(head -n 1 "$filename")

# Вырезаем расширение файла (все буквы после точки)
ext="${filename##*.}"

### Выбираем правило проверки в зависимости от расширения

bash
case "$ext" in
    c|js)
        # Ищем в начале строки // или /*
        if [[ "$first_line" =~ ^([[:space:]]*\/\/|[[:space:]]*\/\*) ]]; then
            echo "Файл $filename: Комментарий в первой строке НАЙДЕН."
        else
            echo "Файл $filename: Комментарий в первой строке НЕ НАЙДЕН!"
        fi
        ;;
    py)
        # Ищем в начале строки знак #
        if [[ "$first_line" =~ ^[[:space:]]*# ]]; then
            echo "Файл $filename: Комментарий в первой строке НАЙДЕН."
        else
            echo "Файл $filename: Комментарий в первой строке НЕ НАЙДЕН!"
        fi
        ;;
    *)
        echo "Ошибка: Неподдерживаемое расширение файла (.$ext). Нужны только .c, .js, .py"
        ;;
esac
```

3) nano check_comment
4) chmod +x check_comment
<img width="658" height="85" alt="image" src="https://github.com/user-attachments/assets/fb471aef-b78d-41cb-bc00-eb670ac0f068" />
<img width="655" height="76" alt="image" src="https://github.com/user-attachments/assets/16a9b8b1-7053-402e-87de-bf87d585cdf6" />

# задание 7
1) nano find_duplicates
2)
```#!/usr/bin/env bash

# Берем папку для поиска из аргумента. Если ничего не ввели, ищем в текущей папе (.)
dir="${1:-.}"

# Проверяем, существует ли такая директория
if [[ ! -d "$dir" ]]; then
    echo "Ошибка: Директория $dir не существует."
    exit 1
fi

# Находим файлы, считаем хэши и группируем дубликаты через awk
find "$dir" -type f -exec md5sum {} + | \
    sort | \
    awk '
    {
        hash = $1
        $1 = ""
        file = substr($0, 2)
        count[hash]++
        files[hash] = files[hash] ? files[hash] "\n" file : file
    }
    END {
        found = 0
        for (h in count) {
            if (count[h] > 1) {
                found = 1
                print "Дубликаты для хэша " h ":"
                print files[h]
                print "-------------------"
            }
        }
        if (found == 0) {
            print "Дубликаты не найдены."
        }
    }'
```

3) chmod +x find_duplicates
4)
```echo "Привет, МИРЭА" > file1.txt
echo "Привет, МИРЭА" > file2.txt
echo "Другой текст" > file3.txt
```
5) ./find_duplicates
<img width="555" height="99" alt="image" src="https://github.com/user-attachments/assets/db62200c-882e-4ab8-8a4b-bbc1c1b253df" />

# задание 8
1) nano pack_tar
2) 
```#!/usr/bin/env bash

# Запоминаем папку и расширение из аргументов
dir="$1"
ext="$2"

# Проверяем, ввел ли пользователь оба параметра?
if [[ -z "$dir" || -z "$ext" ]]; then
    echo "Использование: $0 <директория> <расширение>"
    exit 1
fi

# Проверяем, существует ли указанная папка?
if [[ ! -d "$dir" ]]; then
    echo "Ошибка: Директория $dir не существует."
    exit 1
fi

# Ищем файлы и передаем их пачкой в архиватор tar
find "$dir" -maxdepth 1 -type f -name "*.${ext}" -print0 | xargs -0 tar -cvf "archive_${ext}.tar"

echo "Архивация завершена! Файл archive_${ext}.tar успешно создан."
```
3) chmod +x pack_tar
<img width="550" height="183" alt="image" src="https://github.com/user-attachments/assets/327c4518-cf83-4bf2-af48-88c7e6dd4578" />

# задача 9
1) nano space_to_tab
2)
```#!/usr/bin/env bash

# Запоминаем имена входного и выходного файлов из аргументов
input_file="$1"
output_file="$2"

# Проверяем: ввел ли пользователь оба имени файла?
if [[ -z "$input_file" || -z "$output_file" ]]; then
    echo "Использование: $0 <входной_файл> <выходной_файл>"
    exit 1
fi

# Проверяем: существует ли вообще входной файл на диске?
if [[ ! -f "$input_file" ]]; then
    echo "Ошибка: Входной файл $input_file не найден."
    exit 1
fi

# Заменяем 4 пробела на символ табуляции (\t) с помощью sed
sed 's/    /\t/g' "$input_file" > "$output_file"

echo "Замена завершена! Результат сохранен в файл: $output_file"
```
3) cmod +x spaces_to_tab
<img width="794" height="101" alt="image" src="https://github.com/user-attachments/assets/f2fe8bc3-09bf-44fd-8832-8f4507701b8f" />

# задание 10
1) nano find_empty
2)
```#!/usr/bin/env bash

# Берем папку для поиска из аргумента. Если ничего не ввели, ищем в текущей папке (.)
dir="${1:-.}"

# Проверяем, существует ли указанная папка?
if [[ ! -d "$dir" ]]; then
    echo "Ошибка: Директория $dir не существует."
    exit 1
fi

# Ищем пустые файлы с помощью утилиты find
find "$dir" -type f -empty
```
3) chmod +x find_empty
<img width="618" height="224" alt="image" src="https://github.com/user-attachments/assets/296407ea-65c8-4865-8c82-c2666126635e" />



















