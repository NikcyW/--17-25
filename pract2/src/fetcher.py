"""Модуль получения данных о зависимостях пакетов NuGet."""

import json
import os
import urllib.error
import urllib.request


def fetch_latest_version(package_name: str) -> str:
    """Получает последнюю стабильную версию пакета из NuGet API."""
    lower_pkg = package_name.lower()
    url = f"https://nuget.org{lower_pkg}/index.json"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
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
    url = f"https://nuget.org{lower_pkg}/index.json"

    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
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
        direct_url = f"https://nuget.org{lower_pkg}/{version}.json"
        try:
            with urllib.request.urlopen(urllib.request.Request(direct_url, headers={"User-Agent": "Mozilla/5.0"}), timeout=10) as resp:
                direct_data = json.loads(resp.read().decode("utf-8"))
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
