"""Модуль виртуальной файловой системы."""
import os
import zipfile
import base64


class VFSNode:
    """Узел виртуальной файловой системы."""

    def __init__(self, name, is_dir):
        """Инициализация узла VFS."""
        self.name = name
        self.is_dir = is_dir
        self.content = None
        self.children = {}


class VFS:
    """Управление виртуальной файловой системой."""

    def __init__(self):
        """Инициализация VFS без корня."""
        self.root = None

    def load_from_zip(self, path):
        """
        Загружает ZIP-архив в память без распаковки на диск.

        Двоичные данные конвертируются в base64.
        """
        if not os.path.exists(path):
            print(f"Ошибка: файл '{path}' не найден.")
            return False

        try:
            self.root = VFSNode("/", True)

            with zipfile.ZipFile(path, "r") as zf:
                for name in zf.namelist():
                    info = zf.getinfo(name)
                    self._add_node(name, info.is_dir(), zf)

            print(f"VFS успешно загружена из {path}")
            return True
        except zipfile.BadZipFile:
            print("Ошибка: неверный формат ZIP-файла.")
            return False

    def _add_node(self, path, is_dir, zip_file):
        """Добавляет узел в дерево VFS."""
        parts = path.strip("/").split("/")
        current = self.root

        for i, part in enumerate(parts):
            if part not in current.children:
                is_last = (i == len(parts) - 1)
                node = VFSNode(part, is_dir)

                if not is_dir and is_last:
                    data = zip_file.read(path)
                    node.content = base64.b64encode(data).decode("utf-8")

                current.children[part] = node
            current = current.children[part]