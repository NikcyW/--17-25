"""Модуль построения и визуализации графа зависимостей."""

import subprocess
from src.fetcher import (
    fetch_nuget_dependencies,
    load_test_repository,
)


def build_dependency_graph(
    root_package: str,
    version: str,
    mode: str,
    repo_source: str
) -> dict:
    """Строит граф зависимостей DFS без рекурсии с обнаружением циклов.

    Args:
        root_package: Имя корневого пакета.
        version: Версия пакета.
        mode: Режим работы ('real' или 'test').
        repo_source: URL репозитория или путь к тестовому файлу.

    Returns:
        dict: Граф в формате {package: [dependencies]}.
    """
    graph = {}
    stack = [(root_package, version)]
    visited = set()

    while stack:
        current_pkg, current_ver = stack.pop()

        if current_pkg in visited:
            continue

        visited.add(current_pkg)

        if mode == "test":
            deps = load_test_repository(repo_source, current_pkg)
        else:
            deps = fetch_nuget_dependencies(current_pkg, current_ver)

        graph[current_pkg] = deps

        for dep in deps:
            if dep not in visited:
                stack.append((dep, ""))

    return graph


def get_load_order(graph: dict, root_package: str) -> list:
    """Возвращает порядок загрузки пакетов (топологическая сортировка).

    Использует DFS без рекурсии с явным стеком состояний.

    Args:
        graph: Граф зависимостей.
        root_package: Корневой пакет.

    Returns:
        list: Порядок загрузки от зависимостей к корню.
    """
    visited = set()
    order = []

    # Состояния: 'visiting' - в процессе обработки, 'visited' - завершён
    state = {}

    for start_node in graph:
        if start_node in visited:
            continue

        # Стек содержит кортежи (узел, итератор_соседей, фаза)
        # Фаза: 'pre' - до обхода детей, 'post' - после обхода детей
        stack = [(start_node, iter(graph.get(start_node, [])), 'pre')]

        while stack:
            node, neighbors, phase = stack.pop()

            if phase == 'pre':
                if node in visited:
                    continue

                # Проверка цикла
                if state.get(node) == 'visiting':
                    continue

                state[node] = 'visiting'

                # Добавляем post-обработку этого узла
                stack.append((node, neighbors, 'post'))

                # Добавляем соседей для обработки
                for neighbor in neighbors:
                    if neighbor not in visited:
                        stack.append(
                            (neighbor, iter(graph.get(neighbor, [])), 'pre')
                        )

            elif phase == 'post':
                if node not in visited:
                    visited.add(node)
                    state[node] = 'visited'
                    order.append(node)

    return order


def generate_dot(graph: dict) -> str:
    """Генерирует представление графа в формате Graphviz DOT.

    Args:
        graph: Граф зависимостей.

    Returns:
        str: Содержимое DOT-файла.
    """
    lines = ["digraph dependencies {", "  rankdir=LR;", "  node [shape=box];"]

    for pkg, deps in graph.items():
        for dep in deps:
            lines.append(f'  "{pkg}" -> "{dep}";')

    lines.append("}")
    return "\n".join(lines)


def save_graph_image(dot_content: str, output_path: str) -> None:
    """Сохраняет граф в файл PNG через Graphviz.

    Args:
        dot_content: Содержимое DOT-файла.
        output_path: Путь к выходному PNG-файлу.
    """
    dot_file = output_path.rsplit(".", 1)[0] + ".dot"

    try:
        with open(dot_file, "w", encoding="utf-8") as f:
            f.write(dot_content)
        print(f"DOT-файл сохранён: {dot_file}")

        subprocess.run(
            ["dot", "-Tpng", dot_file, "-o", output_path],
            check=True,
            capture_output=True
        )
        print(f"PNG-изображение сохранено: {output_path}")
    except FileNotFoundError:
        print("Graphviz не установлен, PNG не создан.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка Graphviz: {e.stderr.decode('utf-8')}")
    except IOError as e:
        print(f"Ошибка записи: {e}")

