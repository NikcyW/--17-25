import os

def get_load_order(dependencies):
    """
    Возвращает порядок загрузки пакетов (топологическая сортировка).
    """
    visited = set()
    order = []

    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in dependencies.get(node, []):
            dfs(neighbor)
        order.append(node)

    for pkg in dependencies:
        dfs(pkg)
    
    return order[::-1]


def build_dependency_graph(dependencies, output_path):
    """
    Строит граф зависимостей и сохраняет его в формате SVG.
    """
    svg_content = """<svg xmlns="http://w3.org" width="500" height="350" style="background:#f4f6f9;">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="28" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7F8C8D"/>
    </marker>
  </defs>
  <text x="250" y="35" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold" fill="#2C3E50">Граф зависимостей пакетов (.NET)</text>
"""

    y_pos = 100
    for pkg, deps in dependencies.items():
        svg_content += f"""  <circle cx="150" cy="{y_pos}" r="25" fill="#34495E"/>
  <text x="150" y="{y_pos + 4}" text-anchor="middle" font-family="Arial" font-size="10" font-weight="bold" fill="white">{pkg}</text>
"""
        for dep in deps:
            svg_content += f"""  <circle cx="380" cy="{y_pos}" r="22" fill="#2980B9"/>
  <text x="380" y="{y_pos + 4}" text-anchor="middle" font-family="Arial" font-size="10" font-weight="bold" fill="white">{dep}</text>
  <line x1="175" y1="{y_pos}" x2="358" y2="{y_pos}" stroke="#7F8C8D" stroke-width="2" marker-end="url(#arrow)"/>
"""
            y_pos += 80

    svg_content += "</svg>"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

