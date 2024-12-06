import unittest
from unittest.mock import patch, Mock
from io import StringIO
import subprocess
import sys
from visualizer import get_dependencies, get_dependencies_git, convertDicts, render_plantuml, generate_png_from_plantuml


# Тесты для функций получения зависимостей
class TestDependenciesFunctions(unittest.TestCase):

    @patch('visualizer.requests.get')
    def test_get_dependencies(self, mock_get):
        # Мокаем ответ от API
        mock_response = {
            "info": {
                "requires_dist": ["numpy", "scipy"]
            }
        }
        mock_get.return_value.json.return_value = mock_response

        result = get_dependencies("matplotlib")
        self.assertEqual(result, ["numpy", "scipy"])

    @patch('visualizer.requests.get')
    def test_get_dependencies_empty(self, mock_get):
        # Мокаем ответ от API, где зависимостей нет
        mock_response = {
            "info": {}
        }
        mock_get.return_value.json.return_value = mock_response

        result = get_dependencies("nonexistent_package")
        self.assertEqual(result, "")

    @patch('visualizer.requests.get')
    def test_get_dependencies_git(self, mock_get):
        # Мокаем ответ от GitHub (например, с зависимостями)
        mock_response = Mock()
        mock_response.text = 'numpy\nscipy\n'  # Имитация текста с зависимостями
        mock_get.return_value = mock_response

        result = get_dependencies_git("https://github.com/some/package")
        self.assertEqual(result, {'numpy', 'scipy'})


# Тесты для функций, генерирующих код PlantUML
class TestPlantUMLFunctions(unittest.TestCase):

    def test_convert_dicts(self):
        dependencies = ["numpy", "scipy"]
        result = convertDicts("matplotlib", dependencies, 1)  # Задаем глубину 1, чтобы избежать рекурсии
        expected_result = "\"matplotlib\" --> \"numpy\"\n\"matplotlib\" --> \"scipy\"\n"
        self.assertEqual(result, expected_result)

    def test_render_plantuml(self):
        # Проверим, что файл создается
        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            render_plantuml("test_code", "test_output.txt")
            mock_file.assert_called_once_with("test_output.txt", "w")
            mock_file().write.assert_any_call("@startuml\n")
            mock_file().write.assert_any_call("test_code")
            mock_file().write.assert_any_call("@enduml\n")


# Тесты для генерации PNG
class TestPNGGeneration(unittest.TestCase):

    @patch("subprocess.run")
    def test_generate_png_from_plantuml(self, mock_run):
        # Мокаем успешный запуск команды
        mock_run.return_value = None  # Симулируем успешное выполнение команды
        generate_png_from_plantuml("test_output.txt")
        mock_run.assert_called_once_with(["plantuml", "test_output.txt"], check=True)





# Запуск тестов
if __name__ == '__main__':
    unittest.main()
