"""Модуль получения данных о зависимостях пакетов NuGet."""

import json
import urllib.error
import urllib.request


def fetch_nuget_dependencies(package_name: str, version: str) -> list:
    """Получает список прямых зависимостей NuGet-пакета через API.

    Args:
        package_name: Имя пакета (например, 'Newtonsoft.Json').
        version: Версия пакета.

    Returns:
        list: Список имён пакетов-зависимостей.
    """
    lower_pkg = package_name.lower()
    url = f"https://nuget.org{lower_pkg}/{version}.json"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError:
        # Если пакет или версия не найдены, возвращаем пустой список
        return []

    dependencies = []
    # Парсинг групп зависимостей NuGet
    if "dependencyGroups" in data:
        for group in data["dependencyGroups"]:
            if "dependencies" in group:
                for dep in group["dependencies"]:
                    if "id" in dep:
                        dependencies.append(dep["id"])
    return dependencies


def load_test_repository(file_path: str, package_name: str) -> list:
    """Загружает зависимости из локального тестового файла.

    Формат файла тестового репозитория (JSON): {"A": ["B", "C"], "B": ["C"]}
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            repo = json.load(f)
        return repo.get(package_name, [])
    except (json.JSONDecodeError, FileNotFoundError):
        return []
