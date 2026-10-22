# Полный тест всех команд Этапов 1-3

echo "=== Тест 1: Минимальная VFS ==="
python src/main.py --vfs tests/minimal.zip

echo ""
echo "=== Тест 2: Несколько файлов ==="
python src/main.py --vfs tests/multiple.zip

echo ""
echo "=== Тест 3: Глубокая структура ==="
python src/main.py --vfs tests/deep.zip

echo ""
echo "=== Тест 4: Ошибка - файл не найден ==="
python src/main.py --vfs tests/nonexistent.zip

echo ""
echo "=== Тест 5: Скрипт с VFS ==="
python src/main.py --vfs tests/minimal.zip --script tests/test_script.sh