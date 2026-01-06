import pytest

from src.processing import filter_by_state, sort_by_date


# ФИКСТУРЫ - переиспользуемые тестовые данные
@pytest.fixture
def sample_operations():
    """Фикстура с тестовыми операциями разных состояний и дат"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-01T10:00:00"},  # Выполнена, поздняя дата
        {"id": 2, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},  # Выполнена, ранняя дата
        {"id": 3, "state": "EXECUTED", "date": "2024-02-01T10:00:00"},  # Выполнена, средняя дата
        {"id": 4, "state": "EXECUTED", "date": "2024-01-15T10:00:00"},  # Выполнена, средняя дата
    ]


@pytest.fixture
def operations_with_different_states():
    """Фикстура с операциями разных состояний для тестирования фильтрации"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-01T10:00:00"},  # Выполнена
        {"id": 2, "state": "CANCELED", "date": "2024-01-01T10:00:00"},  # Отменена
        {"id": 3, "state": "EXECUTED", "date": "2024-02-01T10:00:00"},  # Выполнена
    ]


@pytest.fixture
def operations_with_same_dates():
    """Фикстура с операциями с одинаковыми датами (проверка стабильности сортировки)"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},  # Одинаковая дата
        {"id": 2, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},  # Одинаковая дата
        {"id": 3, "state": "EXECUTED", "date": "2024-01-01T09:00:00"},  # Более ранняя дата
    ]


@pytest.fixture
def operations_with_invalid_dates():
    """Фикстура с некорректными форматами дат (проверка устойчивости)"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},  # Без времени
        {"id": 2, "state": "EXECUTED", "date": "invalid-date"},  # Неправильный формат
        {"id": 3, "state": "EXECUTED", "date": "2024-03-01T10:00:00.123456"},  # С микросекундами
    ]


# ТЕСТЫ ДЛЯ ФУНКЦИИ filter_by_state
def test_filter_by_state_executed(operations_with_different_states):
    """Тест фильтрации по состоянию EXECUTED"""
    # Проверяем что функция корректно фильтрует операции по статусу EXECUTED
    result = filter_by_state(operations_with_different_states, "EXECUTED")

    # Убеждаемся что все возвращенные операции имеют статус EXECUTED
    assert len(result) == 2
    for operation in result:
        assert operation["state"] == "EXECUTED"


def test_filter_by_state_default(sample_operations):
    """Тест фильтрации с состоянием по умолчанию (EXECUTED)"""
    # Проверяем что функция по умолчанию фильтрует по EXECUTED
    result = filter_by_state(sample_operations)  # Без указания state

    # Все операции должны иметь статус EXECUTED
    assert len(result) == 4
    for operation in result:
        assert operation["state"] == "EXECUTED"


def test_filter_when_no_matching_state(sample_operations):
    """Тест когда нет словарей с указанным статусом state в списке"""
    # Проверяем поведение функции когда запрошенный статус отсутствует в данных
    result = filter_by_state(sample_operations, "PENDING")
    assert result == []  # Должен вернуться пустой список


def test_filter_empty_list():
    """Тест с пустым списком операций - граничный случай"""
    # Проверяем что функция корректно обрабатывает пустой список
    result = filter_by_state([])
    assert result == []


# ТЕСТЫ ДЛЯ ФУНКЦИИ sort_by_date
def test_sort_descending(sample_operations):
    """Тест сортировки по убыванию даты (порядок по умолчанию)"""
    # Проверяем сортировку от самой поздней даты к самой ранней
    result = sort_by_date(sample_operations, reverse=True)

    # Проверяем порядок операций: от поздней к ранней
    assert [op["id"] for op in result] == [1, 3, 4, 2]


def test_sort_ascending(sample_operations):
    """Тест сортировки по возрастанию даты"""
    # Проверяем сортировку от самой ранней даты к самой поздней
    result = sort_by_date(sample_operations, reverse=False)

    # Проверяем порядок операций: от ранней к поздней
    assert [op["id"] for op in result] == [2, 4, 3, 1]


def test_sort_with_same_dates(operations_with_same_dates):
    """Проверка корректности сортировки при одинаковых датах"""
    # Проверяем поведение функции когда несколько операций имеют одинаковую дату
    result = sort_by_date(operations_with_same_dates, reverse=True)

    # При одинаковых датах порядок может сохраниться как в исходном списке
    assert result[0]["id"] in [1, 2]  # Одинаковые даты - любой порядок
    assert result[1]["id"] in [1, 2]  # Одинаковые даты - любой порядок
    assert result[2]["id"] == 3  # Самая ранняя дата - должна быть последней


def test_sort_with_invalid_dates(operations_with_invalid_dates):
    """Тесты на работу функции с некорректными или нестандартными форматами дат"""
    # Проверяем что функция не падает при некорректных форматах дат
    result = sort_by_date(operations_with_invalid_dates)

    # Все элементы должны остаться в результате, даже с некорректными датами
    assert len(result) == 3


def test_sort_empty_list():
    """Тест сортировки пустого списка - граничный случай"""
    # Проверяем что функция корректно обрабатывает пустой список
    result = sort_by_date([])
    assert result == []
