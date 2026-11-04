"""Главный модуль запуска CLI-приложения."""

import sys
from src.config import load_config, ConfigError
from src.graph import (
    build_dependency_graph,
    get_load_order,
    generate_dot,
    save_graph_image,
)

MIN_ARGS_COUNT = 2


def main():
    """Основная функция исполнения."""
    if len(sys.argv) < MIN_ARGS_COUNT:
        print("Использование: python -m src.main <путь_к_config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    try:
        config = load_config(config_path)
    except ConfigError as e:
        print(f"Ошибка конфигурации: {e}")
        sys.exit(1)

    print("--- Этап 1: Настройки конфигурации ---")
    for key, value in config.items():
        print(f"{key}: {value}")

    root_pkg = config["package_name"]
    version = config["version"]
    mode = config["mode"]
    repo_source = config["repository_url"]

    graph = build_dependency_graph(root_pkg, version, mode, repo_source)

    print("\n--- Этап 2 & 3: Найденные зависимости ---")
    for node, deps in graph.items():
        print(f"{node} -> {deps}")

    print("\n--- Этап 4: Порядок загрузки ---")
    load_order = get_load_order(graph, root_pkg)
    print(" -> ".join(load_order))

    print("\n--- Этап 5: Визуализация ---")
    dot_content = generate_dot(graph)
    save_graph_image(dot_content, config["output_image"])


if __name__ == "__main__":
    main()
