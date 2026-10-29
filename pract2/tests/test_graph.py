"""Модуль построения и визуализации графа зависимостей."""

import urllib.error
import urllib.parse
import urllib.request


def build_dependency_graph(
    root_package: str, version: str, mode: str, repo_source: str
) -> dict:
    """Строит граф зависимостей с помощью алгоритма DFS без рекурсии.

    Returns:
        dict: Смежный список графа { пакет: [зависимости] }
    """
    from src.fetcher import fetch_nuget_dependencies, load_test_repository

    graph = {}
    stack = [root_package]
    visited = set()

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        if mode == "test":
            deps = load_test_repository(repo_source, node)
        else:
            deps = fetch_nuget_dependencies(node, version)

        graph[node] = deps

        for dep in deps:
            if dep not in visited and dep not in stack:
                stack.append(dep)

    return graph


def get_load_order(graph: dict, root: str) -> list:
    """Определяет порядок загрузки (топологическая сортировка через DFS)."""
    order = []
    visited = set()
    visiting = set()

    def dfs(node):
        if node in visiting:
            return
        if node in visited:
            return
        visiting.add(node)
        for neighbor in graph.get(node, []):
            dfs(neighbor)
        visiting.remove(node)
        visited.add(node)
        order.append(node)

    dfs(root)
    return order


def generate_dot(graph: dict) -> str:
    """Генерирует текстовое представление графа на языке Graphviz DOT."""
    lines = ["digraph G {", "    rankdir=LR;"]
    for node, neighbors in graph.items():
        if not neighbors:
            lines.append(f'    "{node}";')
        for neighbor in neighbors:
            lines.append(f'    "{node}" -> "{neighbor}";')
    lines.append("}")
    return "\n".join(lines)


def save_graph_image(dot_content: str, output_path: str):
    """Генерирует PNG изображение графа через онлайн-сервер API."""
    encoded_dot = urllib.parse.quote(dot_content)
    url = f"https://quickchart.io{encoded_dot}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())
    except urllib.error.URLError as e:
        print(f"[Ошибка визуализации]: Не удалось связаться с сервером: {e}")
