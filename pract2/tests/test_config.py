"""Тестирование модуля конфигурации."""

import json
import os
import unittest
from src.config import load_config, ConfigError


class TestConfig(unittest.TestCase):
    """Тесты для проверки загрузки и валидации config.json."""

    def setUp(self):
        """Создание временного валидного файла конфигурации."""
        self.test_file = "test_temp_config.json"
        self.valid_data = {
            "package_name": "A",
            "repository_url": "test_repo.json",
            "mode": "test",
            "version": "1.0.0",
            "output_image": "out.png",
        }
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(self.valid_data, f)

    def tearDown(self):
        """Удаление временного файла после теста."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_valid_config(self):
        """Проверка успешной загрузки корректной конфигурации."""
        config = load_config(self.test_file)
        self.assertEqual(config["package_name"], "A")

    def test_missing_file(self):
        """Проверка генерации ошибки, если файл не существует."""
        with self.assertRaises(ConfigError):
            load_config("non_existent_file.json")


if __name__ == "__main__":
    unittest.main()
