import pytest
from src.masks import get_mask_card_number, get_mask_account


# ФИКСТУРЫ - переиспользуемые тестовые данные
@pytest.fixture
def valid_card_numbers():
    """Фикстура с валидными номерами карт для тестирования"""
    return [
        "7000792289606361",  # Visa карта
        "7158300734726758",  # MasterCard карта
        "1596837868705199",  # Maestro карта
    ]


@pytest.fixture
def valid_account_numbers():
    """Фикстура с валидными номерами счетов для тестирования"""
    return [
        "73654108430135874305",  # Номер счета 1
        "64686473678894779589",  # Номер счета 2
        "35383033474447895560",  # Номер счета 3
    ]


@pytest.fixture
def invalid_card_data():
    """Фикстура с некорректными данными для карт (должны вызывать ошибки)"""
    return [
        "123456789012345",  # 15 цифр (слишком короткий)
        "12345678901234567",  # 17 цифр (слишком длинный)
        "1234abc567890123",  # Содержит буквы
        "1234-5678-9012-3456",  # Содержит дефисы
        "",  # Пустая строка
    ]


@pytest.fixture
def invalid_account_data():
    """Фикстура с некорректными данными для счетов (должны вызывать ошибки)"""
    return [
        "123",  # 3 цифры (слишком короткий)
        "123456789012345678901",  # 21 цифра (слишком длинный)
        "abc1234567890",  # Содержит буквы
        "1234-5678-9012",  # Содержит дефисы
        "",  # Пустая строка
    ]


# ТЕСТЫ ДЛЯ ФУНКЦИИ get_mask_card_number
def test_get_mask_card_number(valid_card_numbers):
    """Тест маскировки номера карты - проверяем базовую функциональность"""
    # Проверяем что функция корректно маскирует разные номера карт
    result = get_mask_card_number(valid_card_numbers[0])
    assert result == "7000 79** **** 6361"

    result = get_mask_card_number(valid_card_numbers[1])
    assert result == "7158 30** **** 6758"

    result = get_mask_card_number(valid_card_numbers[2])
    assert result == "1596 83** **** 5199"


def test_get_mask_card_number_different_payment_systems(valid_card_numbers):
    """Тест для разных платежных систем - проверяем универсальность функции"""
    # Visa карта
    result = get_mask_card_number(valid_card_numbers[0])
    assert result == "7000 79** **** 6361"

    # MasterCard карта
    result = get_mask_card_number(valid_card_numbers[1])
    assert result == "7158 30** **** 6758"

    # Maestro карта
    result = get_mask_card_number(valid_card_numbers[2])
    assert result == "1596 83** **** 5199"


def test_get_mask_card_number_with_zeros():
    """Тест маскировки номера карты с нулями - граничный случай"""
    # Проверяем работу с номерами содержащими много нулей
    result = get_mask_card_number("0000111122223333")
    assert result == "0000 11** **** 3333"


def test_get_mask_card_number_letters(invalid_card_data):
    """Тест с буквами в номере карты - проверка обработки ошибок"""
    # Функция должна вызывать ValueError при наличии букв
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number(invalid_card_data[2])  # "1234abc567890123"


def test_get_mask_card_number_special_chars(invalid_card_data):
    """Тест со специальными символами в номере карты - проверка обработки ошибок"""
    # Функция должна вызывать ValueError при наличии специальных символов
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number(invalid_card_data[3])  # "1234-5678-9012-3456"


def test_get_mask_card_number_short(invalid_card_data):
    """Тест с коротким номером карты - проверка валидации длины"""
    # Функция должна вызывать ValueError при неправильной длине
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number(invalid_card_data[0])  # "123456789012345"


def test_get_mask_card_number_long(invalid_card_data):
    """Тест с длинным номером карты - проверка валидации длины"""
    # Функция должна вызывать ValueError при неправильной длине
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number(invalid_card_data[1])  # "12345678901234567"


def test_get_mask_card_number_empty(invalid_card_data):
    """Тест с пустым номером карты - проверка обработки пустых данных"""
    # Функция должна вызывать ValueError при пустой строке
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number(invalid_card_data[4])  # ""


# ТЕСТЫ ДЛЯ ФУНКЦИИ get_mask_account
def test_get_mask_account(valid_account_numbers):
    """Тест маскировки номера счета - проверяем базовую функциональность"""
    # Проверяем что функция корректно маскирует разные номера счетов
    result = get_mask_account(valid_account_numbers[0])
    assert result == "**4305"

    result = get_mask_account(valid_account_numbers[1])
    assert result == "**9589"

    result = get_mask_account(valid_account_numbers[2])
    assert result == "**5560"


def test_get_mask_account_different_number(valid_account_numbers):
    """Тест для разных номеров счетов - проверяем универсальность функции"""
    # Проверяем работу с разными номерами счетов
    result = get_mask_account(valid_account_numbers[0])
    assert result == "**4305"

    result = get_mask_account(valid_account_numbers[1])
    assert result == "**9589"


def test_get_mask_account_with_zeros():
    """Тест маскировки номера счета с нулями - граничный случай"""
    # Проверяем работу с номерами содержащими много нулей
    result = get_mask_account("00000000000000000001")
    assert result == "**0001"


def test_get_mask_account_letters(invalid_account_data):
    """Тест с буквами в номере счета - проверка обработки ошибок"""
    # Функция должна вызывать ValueError при наличии букв
    with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
        get_mask_account(invalid_account_data[2])  # "abc1234567890"


def test_get_mask_account_special_chars(invalid_account_data):
    """Тест со специальными символами в номере счета - проверка обработки ошибок"""
    # Функция должна вызывать ValueError при наличии специальных символов
    with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
        get_mask_account(invalid_account_data[3])  # "1234-5678-9012"


def test_get_mask_account_short(invalid_account_data):
    """Тест с коротким номером счета - проверка валидации длины"""
    # Функция должна вызывать ValueError при слишком коротком номере
    with pytest.raises(ValueError, match="Номер счета должен содержать минимум 4 цифры"):
        get_mask_account(invalid_account_data[0])  # "123"


def test_get_mask_account_empty(invalid_account_data):
    """Тест с пустым номером счета - проверка обработки пустых данных"""
    # Функция должна вызывать ValueError при пустой строке
    with pytest.raises(ValueError, match="Номер счета должен содержать только цифры"):
        get_mask_account(invalid_account_data[4])  # ""