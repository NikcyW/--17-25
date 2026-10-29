"""Модуль работы с конфигурацией приложения."""

import json
import os


class ConfigError(Exception):
    """Исключение для ошибок конфигурации."""


def load_config(config_path: str) -> dict:
    """Загружает и валидирует конфигурационный файл JSON.

    Args:
        config_path: Путь к файлу конфигурации.

    Returns:
        dict: Словарь с параметрами.

    Raises:
        ConfigError: Если файл не найден или не валиден.
    """
    if not os.path.exists(config_path):
        raise ConfigError(f"Файл конфигурации не найден: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ConfigError(f"Неверный формат JSON: {e}") from e

    required_keys = [
        "package_name",
        "repository_url",
        "mode",
        "version",
        "output_image",
    ]
    for key in required_keys:
        if key not in config:
            raise ConfigError(f"Отсутствует обязательный параметр: {key}")

    if config["mode"] not in ["real", "test"]:
        raise ConfigError("Параметр 'mode' должен быть 'real' или 'test'")

    return config
