"""Скрипт генерации тестовых ZIP-архивов."""
import os
import zipfile


def create_minimal_zip(path):
    """Создаёт архив с одним файлом."""
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("file.txt", "hello")


def create_multiple_zip(path):
    """Создаёт архив с несколькими файлами."""
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("a.txt", "file A")
        zf.writestr("b.txt", "file B")
        zf.writestr("c.txt", "file C")


def create_deep_zip(path):
    """Создаёт архив с 3 уровнями вложенности."""
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr(
            "folder1/folder2/folder3/file.txt",
            "deep file"
        )


def main():
    """Генерирует все тестовые архивы."""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    create_minimal_zip(os.path.join(test_dir, "minimal.zip"))
    print("Создан minimal.zip")
    
    create_multiple_zip(os.path.join(test_dir, "multiple.zip"))
    print("Создан multiple.zip")
    
    create_deep_zip(os.path.join(test_dir, "deep.zip"))
    print("Создан deep.zip")
    
    print("Все архивы созданы.")


if __name__ == "__main__":
    main()