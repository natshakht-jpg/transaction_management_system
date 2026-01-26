import json
import logging  # Импортируем библиотеки logging
import os


# Создаем директорию для лог-файлов (если отсутствует)
os.makedirs('logs', exist_ok=True)

# Логер для модуля utils
logger = logging.getLogger(__name__)

# Создаем handler для записи в файл
file_handler = logging.FileHandler('logs/utils.log', mode='w', encoding='utf-8')

# Создаем formatter с нужным форматом
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Добавляем formatter к handler
file_handler.setFormatter(formatter)

# Добавляем handler к логеру
logger.addHandler(file_handler)

# Устанавливаем уровень логирования
logger.setLevel(logging.DEBUG)


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
        logger.error(f"Файл не найден: {file_path}")
        return []

    # 2. Проверяем, что файл не пустой
    if os.path.getsize(file_path) == 0:
        logger.error(f"Файл пустой: {file_path}")
        return []

    # 3. Пытаемся открыть файл и прочитать JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # 4. Проверяем, что загруженные данные являются списком
            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
                return data
            else:
                logger.error(f"Данные не список: {data}")
                return []

    # 5. Обрабатываем возможные ошибки при чтении файла или парсинге JSON
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return []
