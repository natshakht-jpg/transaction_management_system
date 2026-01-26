from src.bank_operations import process_bank_operations, process_bank_search


def test_process_bank_search_empty_data() -> None:
    """Поиск при пустом списке транзакций."""
    data = []
    search = "Перевод"

    result = process_bank_search(data, search)

    assert result == []


def test_process_bank_search_match_found() -> None:
    """Успешный поиск транзакции."""
    data = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"}
    ]
    search = "вклад"

    result = process_bank_search(data, search)

    assert result == [{"id": 2, "description": "Открытие вклада"}]


def test_process_bank_search_no_match() -> None:
    """Поиск без результатов."""
    data = [{"description": "Перевод организации"}]
    search = "вклад"

    result = process_bank_search(data, search)

    assert result == []


def test_process_bank_search_case_insensitive() -> None:
    """Поиск без учета регистра."""
    data = [{"description": "Открытие ВКЛАДА"}]
    search = "вклад"

    result = process_bank_search(data, search)

    assert len(result) == 1  # нашел несмотря на разный регистр


def test_process_bank_search_no_description_key() -> None:
    """Транзакция без ключа 'description' игнорируется."""
    data = [
        {"description": "Перевод"},
        {},  # нет ключа 'description'
        {"description": "Вклад"}
    ]
    search = "Перевод"

    result = process_bank_search(data, search)

    assert result == [{"description": "Перевод"}]


def test_process_bank_operations_empty_data() -> None:
    """Подсчет операций при пустом списке."""
    data = []
    categories = ["Перевод", "Вклад"]

    result = process_bank_operations(data, categories)

    assert result == {}


def test_process_bank_operations_count_correct() -> None:
    """Корректный подсчет по категориям."""
    data = [
        {"description": "Перевод"},
        {"description": "Вклад"},
        {"description": "Перевод"},
        {"description": "Платеж"},  # не входит в categories
        {"description": "Перевод"}
    ]
    categories = ["Перевод", "Вклад"]

    result = process_bank_operations(data, categories)

    assert result == {"Перевод": 3, "Вклад": 1}


def test_process_bank_operations_no_description() -> None:
    """Транзакции без описания игнорируются."""
    data = [
        {"description": "Перевод"},
        {},  # нет описания
        {"description": "Вклад"}
    ]
    categories = ["Перевод", "Вклад"]

    result = process_bank_operations(data, categories)

    assert result == {"Перевод": 1, "Вклад": 1}
