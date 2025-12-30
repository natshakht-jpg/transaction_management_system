import json
import os


def load_transactions(file_path: str) -> list:
    """Загружает транзакции из JSON-файла.

    Принимает:
        file_path (str): Путь до JSON-файла с транзакциями

    Возвращает:
        list: Список словарей с данными о финансовых транзакциях.
              Если файл пустой, содержит не список или не найден,
              возвращает пустой список []."""

    # 1. Проверяем, существует ли файл по указанному пути
    if not os.path.exists(file_path):
        return []

    # 2. Проверяем, что файл не пустой
    if os.path.getsize(file_path) == 0:
        return []

    # 3. Пытаемся открыть файл и прочитать JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # 4. Проверяем, что загруженные данные являются списком
            if isinstance(data, list):
                return data
            else:
                return []

    # 5. Обрабатываем возможные ошибки при чтении файла или парсинге JSON
    except (json.JSONDecodeError, IOError):
        return []
