"""Модуль парсинга командной строки."""
import shlex


def parse_command(input_str):
    """
    Разбирает строку ввода на команду и аргументы.

    Корректно обрабатывает кавычки.

    Args:
        input_str: строка ввода пользователя.

    Returns:
        Список аргументов команды.
    """
    try:
        return shlex.split(input_str)
    except ValueError:
        return []