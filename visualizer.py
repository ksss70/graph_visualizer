import subprocess
import os
import sys
from typing import Set


def get_package_dependencies(package_name: str) -> Set[str]:
    """Получаем зависимости для указанного пакета с помощью pip."""
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'show', package_name],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return set()

    dependencies = set()
    for line in result.stdout.splitlines():
        if line.startswith('Requires:'):
            dependencies = set(line[len('Requires: '):].strip().split(', '))
            break
    return dependencies


def get_all_dependencies(package_name: str) -> Set[str]:
    """Рекурсивно собираем все зависимости пакета."""
    all_deps = set()
    direct_deps = get_package_dependencies(package_name)

    for dep in direct_deps:
        all_deps.add(dep)
        all_deps.update(get_all_dependencies(dep))  # Рекурсивный вызов

    return all_deps


def generate_plantuml(package_name: str, dependencies: Set[str]) -> str:
    """Генерируем код для визуализации графа зависимостей в формате PlantUML."""
    plantuml_code = '@startuml\n'
    plantuml_code += f'package "{package_name}" {{\n'

    for dep in dependencies:
        plantuml_code += f'    "{package_name}" -- "{dep}"\n'

    plantuml_code += '}\n@enduml'
    return plantuml_code


def save_plantuml_to_png(plantuml_path: str, output_path: str) -> None:
    """Сохраняем граф зависимостей из PlantUML в файл PNG."""
    subprocess.run(
        ['plantuml', '-tpng', '-o', os.path.dirname(output_path), plantuml_path],
        check=True
    )


def main():
    if len(sys.argv) != 4:
        print("Usage: python visualizer.py <plantuml_path> <package_name> <output_path>")
        sys.exit(1)

    plantuml_path = sys.argv[1]
    package_name = sys.argv[2]
    output_path = sys.argv[3]

    dependencies = get_all_dependencies(package_name)
    plantuml_code = generate_plantuml(package_name, dependencies)

    with open(plantuml_path, 'w') as f:
        f.write(plantuml_code)

    save_plantuml_to_png(plantuml_path, output_path)
    print(f"Граф зависимостей сохранен в {output_path}")
