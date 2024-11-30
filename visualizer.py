import subprocess
import networkx as nx
import os


# Функция для извлечения зависимостей из requirements.txt
def get_all_dependencies(requirements_file):
    dependencies = set()

    with open(requirements_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):  # Игнорируем комментарии и пустые строки
                dependencies.add(line)

    return dependencies


# Функция для создания графа зависимостей
def create_dependency_graph(requirements_file):
    dependencies = get_all_dependencies(requirements_file)
    G = nx.DiGraph()  # Направленный граф

    # Добавляем узлы для каждого пакета
    for dep in dependencies:
        G.add_node(dep)

    # Пример зависимости: scipy зависит от numpy и matplotlib
    for dep in dependencies:
        if dep == "scipy":  # Мы вручную добавляем зависимости для scipy
            G.add_edge("scipy", "numpy")
            G.add_edge("scipy", "matplotlib")

    return G


# Функция для создания .puml файла
def create_plantuml_file(graph, filename="dependency_graph.puml"):
    with open(filename, 'w') as file:
        file.write("@startuml\n")

        # Генерация пакетов для каждого модуля
        for node in graph.nodes:
            file.write(f"  package \"{node}\" {{}}\n")

        # Генерация зависимостей между модулями
        for u, v in graph.edges:
            file.write(f"  {u} --> {v}\n")

        file.write("@enduml\n")
    print(f"PlantUML file '{filename}' created.")


# Функция для конвертации .puml в .png с помощью PlantUML
def save_plantuml_to_png(puml_path, output_path):
    try:
        subprocess.run(['plantuml', '-tpng', '-o', os.path.dirname(output_path), puml_path], check=True)
        print(f"Graph saved as PNG to '{output_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Error generating PNG: {e}")


def main():
    requirements_file = 'requirements.txt'

    # Создаем граф зависимостей
    graph = create_dependency_graph(requirements_file)

    # Генерируем .puml файл
    puml_file = 'dependency_graph.puml'
    create_plantuml_file(graph, puml_file)

    # Конвертируем .puml файл в .png
    save_plantuml_to_png(puml_file, 'dependency_graph.png')


if __name__ == "__main__":
    main()
