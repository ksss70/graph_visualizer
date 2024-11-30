import unittest
from unittest.mock import patch, mock_open
import os
from visualizer import get_all_dependencies, create_dependency_graph, create_plantuml_file, save_plantuml_to_png

class TestDependencyVisualizer(unittest.TestCase):

    @patch('builtins.open', mock_open(read_data="numpy\nscipy\nmatplotlib"))
    def test_get_all_dependencies(self):
        # Тестируем функцию извлечения зависимостей
        dependencies = get_all_dependencies("requirements.txt")
        self.assertEqual(dependencies, {"numpy", "scipy", "matplotlib"})

    @patch('builtins.open', mock_open(read_data="numpy\nscipy\nmatplotlib"))
    def test_create_dependency_graph(self):
        # Тестируем создание графа
        graph = create_dependency_graph("requirements.txt")
        self.assertEqual(len(graph.nodes), 3)  # 3 узла: numpy, scipy, matplotlib
        self.assertTrue(graph.has_edge("scipy", "numpy"))  # Проверяем зависимость scipy -> numpy
        self.assertTrue(graph.has_edge("scipy", "matplotlib"))  # Проверяем зависимость scipy -> matplotlib

    def test_create_plantuml_file(self):
        # Тестируем создание .puml файла без мокирования open
        graph = create_dependency_graph("requirements.txt")
        puml_path = 'test_graph.puml'
        create_plantuml_file(graph, puml_path)

        # Открываем файл и проверяем его содержимое
        with open(puml_path, 'r') as file:
            puml_content = file.read()

        print("---- PUMl FILE CONTENT ----")
        print(puml_content)
        print("--------------------------")

        # Проверяем, что в содержимом puml-файла есть правильные данные
        self.assertIn('@startuml', puml_content)
        self.assertIn('scipy --> numpy', puml_content)
        self.assertIn('scipy --> matplotlib', puml_content)
        self.assertIn('package "numpy" {}', puml_content)
        self.assertIn('package "scipy" {}', puml_content)
        self.assertIn('package "matplotlib" {}', puml_content)

        # Удаляем файл после проверки
        os.remove(puml_path)

    @patch('subprocess.run')  # Мокаем вызов subprocess.run
    def test_save_plantuml_to_png(self, mock_run):
        # Тестируем сохранение в PNG
        mock_run.return_value = None  # Подтверждаем, что subprocess.run не вызывает ошибок
        puml_file = 'test_graph.puml'
        output_path = 'test_graph.png'
        save_plantuml_to_png(puml_file, output_path)

        # Проверяем, что subprocess.run был вызван с нужными аргументами
        mock_run.assert_called_with(['plantuml', '-tpng', '-o', os.path.dirname(output_path), puml_file], check=True)


if __name__ == '__main__':
    unittest.main()
