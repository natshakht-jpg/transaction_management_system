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
