import re
from collections import Counter
from typing import List, Dict


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """Поиск банковских операций по строке в описании.

    Принимает:
        data: Список словарей с банковскими операциями
        search: Строка для поиска в поле 'description'

    Возвращает:
        Список словарей с операциями, подходящими под поиск
    """

    # Создаем список для хранения подходящих операций
    filtered_operations = []

    # Проходим по всем операциям
    for item in data:
        # Получаем описание текущей операции
        description = item.get('description')

        # Проверяем, что описание существует
        if description is not None:
            # Ищем строку поиска в описании (без учета регистра)
            if re.search(search, description, re.IGNORECASE):
                # Добавляем подходящую операцию в результат
                filtered_operations.append(item)

    return filtered_operations


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """Подсчет количества банковских операций по категориям.

    Аргументы:
        data: Список словарей с банковскими операциями
        categories: Список категорий для подсчета

    Возвращает:
        Словарь с количеством операций по каждой категории
    """
    # Создаем счетчик для подсчета операций
    category_counter = Counter()

    # Проходим по всем транзакциям
    for transaction in data:
        # Получаем описание текущей транзакции
        description = transaction.get('description')

        # Проверяем, что описание существует
        if description is not None:
            # Проверяем, что описание есть в списке нужных категорий
            if description in categories:
                # Увеличиваем счетчик для данной категории
                category_counter[description] += 1

    # Преобразуем Counter в обычный словарь для возврата
    return dict(category_counter)

