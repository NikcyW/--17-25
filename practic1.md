задание 1  
grep -o '^[a-z_][a-z0-9_-]*' /etc/passwd | sort
<img width="998" height="561" alt="image" src="https://github.com/user-attachments/assets/e38f40b5-332e-4ff3-8388-21097b22d7c1" />

задание 2  
grep -v '^#' /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n 5
<img width="1221" height="218" alt="image" src="https://github.com/user-attachments/assets/8170c4c3-c6ca-4aa4-b413-4f4f1a8f511b" />

задание 3  
1)
nano banner

2)
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

 3)
chmod +x banner

4)
./banner 'Hello from RTU MIREA!'

<img width="800" height="159" alt="image" src="https://github.com/user-attachments/assets/0af98f7f-2d65-4b4a-adf9-938b372cf7d9" />




