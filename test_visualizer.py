import unittest
from unittest.mock import patch
import os

from visualizer import get_all_dependencies, generate_plantuml, save_plantuml_to_png


class TestDependencyVisualizer(unittest.TestCase):

    @patch('visualizer.get_package_dependencies')
    def test_get_all_dependencies(self, mock_get_package_dependencies):
        # Мокаем возвращаемые зависимости для различных пакетов
        # Проверим зависимости для пакета 'scipy'
        mock_get_package_dependencies.side_effect = lambda package_name: {
            'scipy': {'numpy', 'matplotlib'},  # scipy зависит от numpy и matplotlib
            'numpy': set(),  # У numpy нет зависимостей
            'matplotlib': set()  # У matplotlib нет зависимостей
        }.get(package_name, set())

        # Получаем все зависимости для 'scipy'
        result = get_all_dependencies('scipy')

        # Проверяем, что зависимости для 'scipy' содержат 'numpy' и 'matplotlib', но не важно в каком порядке
        self.assertTrue({'numpy', 'matplotlib'}.issubset(result))  # Проверяем, что результат содержит эти зависимости

    @patch('visualizer.subprocess.run')
    @patch('visualizer.generate_plantuml')
    def test_save_plantuml_to_png(self, mock_generate_plantuml, mock_subprocess_run):
        mock_generate_plantuml.return_value = "@startuml\n    'dummy graph'\n@enduml"

        # Путь к файлам
        plantuml_path = 'dependency_graph.puml'
        output_path = 'output.png'

        # Вызов функции
        save_plantuml_to_png(plantuml_path, output_path)

        # Проверяем, что subprocess.run был вызван правильно
        mock_subprocess_run.assert_called_with(
            ['plantuml', '-tpng', '-o', os.path.dirname(output_path), plantuml_path],
            check=True
        )

    @patch('visualizer.save_plantuml_to_png')
    @patch('visualizer.generate_plantuml')
    def test_main_function(self, mock_generate_plantuml, mock_save_plantuml_to_png):
        mock_generate_plantuml.return_value = "@startuml\n    'dummy graph'\n@enduml"

        # Симулируем аргументы командной строки
        with patch('sys.argv', ['visualizer.py', 'dependency_graph.puml', 'scipy', 'output.png']):
            # Вызов main
            from visualizer import main
            main()

        # Проверяем, что save_plantuml_to_png был вызван с правильными параметрами
        mock_save_plantuml_to_png.assert_called_with('dependency_graph.puml', 'output.png')


if __name__ == '__main__':
    unittest.main()
