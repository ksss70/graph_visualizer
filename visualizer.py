import requests
import argparse
import re
import os
import subprocess


def get_dependencies(package_name):
    response = requests.get(f'https://pypi.org/pypi/{package_name}/json').json()
    if "requires_dist" in response.get("info", {}):
        dependencies = response.get("info", {})["requires_dist"]
    else:
        return ""
    if dependencies == None:
        return ""
    return ",".join(dependencies).split(',')


def get_dependencies_git(package_url):
    response = requests.get(package_url)
    dependencies = set()
    for line in response.text.splitlines():
        line = line.strip()
        if line and line[0] != '-':
            dependencies.add(line)
    return dependencies


def convertDicts(pack_name, dependencies, depth):
    if dependencies == "" or depth == 0:
        return f"\"{pack_name}\""

    PlantUMLCode = ""
    visited = set()

    for pack in dependencies:
        match = re.match(r'^[a-zA-Z0-9_-]+', pack)
        if match:
            name_pack = pack[:match.end()]
        else:
            name_pack = pack

        if name_pack in visited or name_pack == "":
            pass
        else:
            if re.match(r'^[a-zA-Z0-9_-]+', name_pack) and name_pack != pack_name:
                PlantUMLCode += f"\"{pack_name}\" --> \"{name_pack}\"\n"
                visited.add(name_pack)
                if 1 < depth:
                    depth_pack = depth - 1
                    dependencies_pack = get_dependencies(name_pack)
                    PlantUMLCode += convertDicts(name_pack, dependencies_pack, depth_pack)

    return PlantUMLCode


def render_plantuml(plantuml_code, output_file):
    # Запись в файл
    with open(output_file, 'w') as file:
        file.write('@startuml\n')
        file.write(plantuml_code)
        file.write('@enduml\n')
    print(f"PlantUML code saved as {output_file}")


def generate_png_from_plantuml(plantuml_file):
    # Проверяем, доступен ли PlantUML через командную строку
    command = ["plantuml", plantuml_file]

    try:
        subprocess.run(command, check=True)
        print(f"PNG generated successfully for {plantuml_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error while generating PNG: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Viz")
    parser.add_argument('--package')
    parser.add_argument('--output')
    parser.add_argument('--depth', type=int, default=3, help="Specify the depth of dependency resolution")
    parser.add_argument('--url')
    args = parser.parse_args()

    error_message = "Cannot get dependencies for this package"
    output = args.output
    depth = args.depth

    if args.package:
        package_name = args.package
        dependencies = get_dependencies(package_name)
        if dependencies:
            links = convertDicts(package_name, dependencies, depth)
            render_plantuml(links, output)
            # Генерация PNG из полученного кода PlantUML
            generate_png_from_plantuml(output)
        else:
            print(error_message)
    elif args.url:
        package_url = args.url
        package_name = package_url.split('/')[4]
        dependencies = get_dependencies_git(package_url)
        if dependencies:
            links = convertDicts(package_name, dependencies, depth)
            render_plantuml(links, output)
            # Генерация PNG из полученного кода PlantUML
            generate_png_from_plantuml(output)
        else:
            print(error_message)
    else:
        print(error_message)
