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


def _extract_dependencies_from_groups(dependency_groups: list) -> set:
    """Извлекает зависимости из групп зависимостей.

    Args:
        dependency_groups: Список групп зависимостей.

    Returns:
        set: Множество имён зависимых пакетов.
    """
    dependencies = set()
    for group in dependency_groups:
        if "dependencies" in group:
            for dep in group["dependencies"]:
                if "id" in dep:
                    dependencies.add(dep["id"])
    return dependencies


def _find_version_in_index(data: dict, version: str) -> set:
    """Ищет зависимости для конкретной версии в индексе.

    Args:
        data: Данные индекса пакета.
        version: Искомая версия.

    Returns:
        set: Множество найденных зависимостей.
    """
    dependencies = set()
    if "items" not in data:
        return dependencies

    for page in data["items"]:
        if "items" not in page:
            continue
        for item in page["items"]:
            catalog = item.get("catalogEntry", {})
            if catalog.get("version") == version:
                groups = catalog.get("dependencyGroups", [])
                dependencies.update(_extract_dependencies_from_groups(groups))
    return dependencies


def _fetch_direct_dependencies(lower_pkg: str, version: str) -> set:
    """Запрашивает зависимости напрямую по версии пакета.

    Args:
        lower_pkg: Имя пакета в нижнем регистре.
        version: Версия пакета.

    Returns:
        set: Множество найденных зависимостей.
    """
    base_url = "https://api.nuget.org/v3/registration5-gz-semver2"
    direct_url = f"{base_url}/{lower_pkg}/{version}.json"
    try:
        direct_data = _fetch_json(direct_url)
        groups = direct_data.get("dependencyGroups", [])
        return _extract_dependencies_from_groups(groups)
    except Exception:
        return set()


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

    dependencies = _find_version_in_index(data, version)

    if not dependencies:
        dependencies = _fetch_direct_dependencies(lower_pkg, version)

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
