import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# ФИКСТУРЫ
@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями для генераторов"""
    return [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод организации"},
        {"id": 2, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод со счета на счет"},
        {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}, "description": "Перевод со счета на счет"},
    ]


# ТЕСТЫ ДЛЯ filter_by_currency
def test_filter_by_currency_usd(sample_transactions):
    """Тест фильтрации по USD"""
    generator = filter_by_currency(sample_transactions, "USD")
    result = list(generator)

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


def test_filter_by_currency_rub(sample_transactions):
    """Тест фильтрации по RUB"""
    generator = filter_by_currency(sample_transactions, "RUB")
    result = list(generator)

    assert len(result) == 1
    assert result[0]["id"] == 3


def test_filter_by_currency_empty(sample_transactions):
    """Тест фильтрации по несуществующей валюте"""
    generator = filter_by_currency(sample_transactions, "EUR")
    result = list(generator)

    assert len(result) == 0


def test_filter_by_currency_is_generator(sample_transactions):
    """Тест, что функция возвращает генератор"""
    generator = filter_by_currency(sample_transactions, "USD")
    assert hasattr(generator, "__iter__")
    assert hasattr(generator, "__next__")


def test_filter_by_currency_empty_list():
    """Тест фильтрации пустого списка транзакций"""
    generator = filter_by_currency([], "USD")
    result = list(generator)
    assert result == []


# ТЕСТЫ ДЛЯ transaction_descriptions
def test_transaction_descriptions(sample_transactions):
    """Тест получения описаний транзакций"""
    generator = transaction_descriptions(sample_transactions)
    result = list(generator)

    assert result == ["Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет"]


def test_transaction_descriptions_generator_behavior(sample_transactions):
    """Тест пошагового поведения генератора"""
    gen = transaction_descriptions(sample_transactions)

    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод со счета на счет"

    with pytest.raises(StopIteration):
        next(gen)


def test_transaction_descriptions_empty_list():
    """Тест получения описаний из пустого списка"""
    generator = transaction_descriptions([])
    result = list(generator)
    assert result == []


# ТЕСТЫ ДЛЯ card_number_generator
@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9997, 9999, ["0000 0000 0000 9997", "0000 0000 0000 9998", "0000 0000 0000 9999"]),
        (42, 42, ["0000 0000 0000 0042"]),
    ],
)
def test_card_number_generator_ranges(start, end, expected):
    """Параметризованный тест для разных диапазонов"""
    generator = card_number_generator(start, end)
    result = list(generator)
    assert result == expected


def test_card_number_generator_format():
    """Тест формата вывода"""
    generator = card_number_generator(1234567890123456, 1234567890123456)
    result = next(generator)

    assert len(result) == 19  # 16 цифр + 3 пробела
    assert result.count(" ") == 3
    assert result == "1234 5678 9012 3456"


def test_card_number_generator_edge_cases():
    """Тест граничных случаев"""
    # Минимальное значение
    gen = card_number_generator(1, 1)
    assert next(gen) == "0000 0000 0000 0001"

    # Максимальное значение
    gen = card_number_generator(9999999999999999, 9999999999999999)
    assert next(gen) == "9999 9999 9999 9999"


def test_card_number_generator_is_generator():
    """Тест, что это действительно генератор"""
    gen = card_number_generator(1, 5)
    assert hasattr(gen, "__iter__")
    assert hasattr(gen, "__next__")

    # Проверяем ленивое вычисление
    first = next(gen)
    assert first == "0000 0000 0000 0001"


def test_card_number_generator_reverse_range():
    """Тест, если start > end"""
    generator = card_number_generator(5, 2)
    result = list(generator)
    assert result == []  # Пустой результат
