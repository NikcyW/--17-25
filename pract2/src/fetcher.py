"""Модуль получения данных о зависимостях пакетов NuGet."""

import gzip
import json
import os
import urllib.error
import urllib.request


def _fetch_json(url: str) -> dict:
    """Загружает и распаковывает JSON с gzip-сжатием.

    Args:
        url: URL для запроса.

    Returns:
        dict: Распарсенный JSON.

    Raises:
        urllib.error.URLError: При ошибке сети.
    """
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as response:
        content = response.read()
        if content[:2] == b'\x1f\x8b':
            content = gzip.decompress(content)
        return json.loads(content.decode("utf-8"))


def fetch_latest_version(package_name: str) -> str:
    """Получает последнюю стабильную версию пакета из NuGet API."""
    lower_pkg = package_name.lower()
    base_url = "https://api.nuget.org/v3/registration5-gz-semver2"
    url = f"{base_url}/{lower_pkg}/index.json"
    try:
        data = _fetch_json(url)
        if "items" in data and data["items"]:
            last_page = data["items"][-1]
            if "items" in last_page and last_page["items"]:
                return last_page["items"][-1]["catalogEntry"]["version"]
    except Exception:
        pass
    return ""


def fetch_nuget_dependencies(package_name: str, version: str) -> list:
    """Получает все зависимости пакета из всех групп фреймворков.

    Сначала сканируется индекс регистрации пакета, затем, если там пусто,
    запрашивается прямая карточка версии.

    Args:
        package_name: Имя пакета.
        version: Версия пакета.

    Returns:
        list: Список уникальных имён пакетов-зависимостей.
    """
    if not version:
        version = fetch_latest_version(package_name)
        if not version:
            return []

    lower_pkg = package_name.lower()
    base_url = "https://api.nuget.org/v3/registration5-gz-semver2"
    url = f"{base_url}/{lower_pkg}/index.json"

    try:
        data = _fetch_json(url)
    except urllib.error.URLError:
        return []

    dependencies = set()

    if "items" in data:
        for page in data["items"]:
            if "items" in page:
                for item in page["items"]:
                    if item.get("catalogEntry", {}).get("version") == version:
                        catalog = item.get("catalogEntry", {})
                        if "dependencyGroups" in catalog:
                            for group in catalog["dependencyGroups"]:
                                if "dependencies" in group:
                                    for dep in group["dependencies"]:
                                        if "id" in dep:
                                            dependencies.add(dep["id"])

    if not dependencies:
        direct_url = f"{base_url}/{lower_pkg}/{version}.json"
        try:
            direct_data = _fetch_json(direct_url)
            if "dependencyGroups" in direct_data:
                for group in direct_data["dependencyGroups"]:
                    if "dependencies" in group:
                        for dep in group["dependencies"]:
                            if "id" in dep:
                                dependencies.add(dep["id"])
        except Exception:
            pass

    return list(dependencies)


def load_test_repository(file_path: str, package_name: str) -> list:
    """Загружает зависимости из локального тестового файла."""
    if not os.path.isabs(file_path):
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        file_path = os.path.join(base_dir, file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            repo = json.load(f)
        return repo.get(package_name, [])
    except (json.JSONDecodeError, FileNotFoundError):
        return []
