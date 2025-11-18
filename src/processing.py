def filter_by_state(operations: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Функция принимает список словарей и опционально значение для ключа
    state (по умолчанию 'EXECUTED') и возвращает новый список словарей,
    содержащий только те словари, у которых ключ state соответствует
    указанному значению.
    """
    filtered_operations = []  # Создаем пустой список для отфильтрованных операций
    for operation in operations:  # Перебираем каждую операцию в списке
        if operation['state'] == state:  # Если статус операции совпадает с искомым
            filtered_operations.append(operation)  # Добавляем операцию в результат
    return filtered_operations  # Возвращаем отфильтрованный список


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список операций по дате.
    Аргументы:
        operations: Список словарей с операциями
        reverse: Порядок сортировки (True - по убыванию, False - по возрастанию)
    Возврат:
        Отсортированный список операций
    """
    # Сортируем операции по дате с указанным порядком (по убыванию по умолчанию)
    return sorted(operations, key=lambda x: x['date'], reverse=reverse)
