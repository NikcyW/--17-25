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
ROW_PERIOD = 2
SHORT_NAME_LIMIT = 8


def save_as_png_fallback(graph: dict, load_order: list, output_image_path: str):
    """Генерирует оффлайн векторный рисунок графа и сохраняет его с расширением PNG."""
    if not load_order:
        load_order = list(graph.keys())
        
    num_nodes = len(load_order)
    width = max(500, num_nodes * 150)
    
    coords = {}
    for i, node in enumerate(load_order):
        x = 60 + i * 140
        y = 130 if i % ROW_PERIOD == 0 else 230
        coords[node] = (x, y)

    if load_order:
        root_node = load_order[-1]
        coords[root_node] = (width - 70, 180)

    svg_lines = [
        f'<svg xmlns="http://w3.org" width="{width}" height="350" style="background:#f4f6f9;">',
        '  <defs>',
        '    <marker id="arrow" viewBox="0 0 10 10" refX="28" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7F8C8D"/>',
        '    </marker>',
        '  </defs>',
        f'  <text x="{width // 2}" y="35" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#2C3E50">Граф зависимостей пакетов (.NET)</text>'
    ]

    for node, neighbors in graph.items():
        if node in coords:
            x1, y1 = coords[node]
            for neighbor in neighbors:
                if neighbor in coords:
                    x2, y2 = coords[neighbor]
                    svg_lines.append(
                        f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#7F8C8D" stroke-width="2" marker-end="url(#arrow)"/>'
                    )

    for node, (x, y) in coords.items():
        svg_lines.append(f'  <circle cx="{x}" cy="{y}" r="22" fill="#2980B9"/>')
        short_name = node.split(".")[-1] if len(node) > SHORT_NAME_LIMIT else node
        svg_lines.append(
            f'  <text x="{x}" y="{y+4}" text-anchor="middle" font-family="Arial" font-size="10" font-weight="bold" fill="white">{short_name}</text>'
        )

    svg_lines.append('</svg>')
    
    if not output_image_path.endswith(".png"):
        output_image_path = output_image_path.rsplit(".", 1)[0] + ".png"
        
    try:
        with open(output_image_path, "w", encoding="utf-8") as f:
            f.write("\n".join(svg_lines))
        print(f"Графический файл успешно сгенерирован: {output_image_path}")
    except IOError as e:
        print(f"[Ошибка сохранения]: {e}")


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

    dot_content = generate_dot(graph)
    save_graph_image(dot_content, config["output_image"])
    
    save_as_png_fallback(graph, load_order, config["output_image"])


if __name__ == "__main__":
    main()
