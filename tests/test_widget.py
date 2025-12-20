import pytest

from src.widget import get_date, mask_account_card


# ФИКСТУРЫ - переиспользуемые тестовые данные
@pytest.fixture
def valid_card_data():
    """Фикстура с валидными данными карт для тестирования"""
    return [
        "Visa Platinum 7000792289606361",  # Карта Visa
        "MasterCard 7158300734726758",     # Карта MasterCard
        "Maestro 1596837868705199",        # Карта Maestro
    ]


@pytest.fixture
def valid_account_data():
    """Фикстура с валидными данными счетов для тестирования"""
    return [
        "Счет 73654108430135874305",  # Счет 1
        "Счет 64686473678894779589",  # Счет 2
    ]


@pytest.fixture
def invalid_widget_data():
    """Фикстура с некорректными данными для widget (проверка устойчивости)"""
    return [
        "",                    # Пустая строка
        "Просто текст",        # Текст без цифр
        "Счет",               # Только название без номера
        "Visa",               # Только название карты без номера
    ]


@pytest.fixture
def valid_date_strings():
    """Фикстура с валидными датами для тестирования преобразования"""
    return [
        "2024-03-11T02:26:18.671407",  # Стандартная дата
        "2023-12-31T23:59:59.999999",  # Конец года
        "2023-01-01T00:00:00.000000",  # Начало года
    ]


@pytest.fixture
def invalid_date_strings():
    """Фикстура с некорректными датами (проверка обработки ошибок)"""
    return [
        "",                              # Пустая строка
        "invalid-date",                  # Неверный формат
        "2024-13-11T02:26:18.671407",   # Неверный месяц (13)
    ]


# ТЕСТЫ ДЛЯ ФУНКЦИИ mask_account_card
def test_recognize_account(valid_account_data):
    """Тест распознавания счета - проверяем что функция определяет тип 'Счет'"""
    # Функция должна распознать что это счет и применить соответствующую маскировку
    result = mask_account_card(valid_account_data[0])
    assert result == "Счет **4305"


def test_recognize_card(valid_card_data):
    """Тест распознавания карты - проверяем что функция определяет тип 'Карта'"""
    # Функция должна распознать что это карта и применить соответствующую маскировку
    result = mask_account_card(valid_card_data[0])
    assert result == "Visa Platinum 7000 79** **** 6361"


@pytest.mark.parametrize("input_data, expected", [
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Счет 64686473678894779589", "Счет **9589"),
])
def test_different_accounts(input_data, expected):
    """Параметризованный тест для разных номеров счетов"""
    # Проверяем что функция корректно работает с разными номерами счетов
    result = mask_account_card(input_data)
    assert result == expected


@pytest.mark.parametrize("input_data, expected", [
    ("Visa 7000792289606361", "Visa 7000 79** **** 6361"),
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
])
def test_different_cards(input_data, expected):
    """Параметризованный тест для разных типов карт"""
    # Проверяем что функция корректно работает с разными типами карт
    result = mask_account_card(input_data)
    assert result == expected


def test_empty_string(invalid_widget_data):
    """Тест пустой строки - проверка обработки граничного случая"""
    # Функция должна корректно обработать пустую строку
    result = mask_account_card(invalid_widget_data[0])  # ""
    assert result == ""


def test_no_numbers(invalid_widget_data):
    """Тест строки без цифр - проверка обработки некорректных данных"""
    # Функция должна вернуть исходную строку если нет цифр для маскировки
    result = mask_account_card(invalid_widget_data[1])  # "Просто текст"
    assert result == "Просто текст"


def test_extra_spaces():
    """Тест с лишними пробелами - проверка устойчивости к форматированию"""
    # Функция должна корректно обработать строку с лишними пробелами
    result = mask_account_card("  Счет  73654108430135874305  ")
    assert result == "Счет **4305"


# ТЕСТЫ ДЛЯ ФУНКЦИИ get_date
def test_get_date_valid(valid_date_strings):
    """Тестирование правильности преобразования даты - основные случаи"""
    # Проверяем корректное преобразование дат из ISO формата в русский формат
    result = get_date(valid_date_strings[0])
    assert result == "11.03.2024"

    result = get_date(valid_date_strings[1])
    assert result == "31.12.2023"

    result = get_date(valid_date_strings[2])
    assert result == "01.01.2023"


def test_get_date_different_formats(valid_date_strings):
    """Проверка работы функции на различных входных форматах даты"""
    # Проверяем что функция работает с разными валидными форматами дат
    result = get_date(valid_date_strings[1])  # Конец года
    assert result == "31.12.2023"

    result = get_date(valid_date_strings[2])  # Начало года
    assert result == "01.01.2023"


def test_get_date_empty_string(invalid_date_strings):
    """Проверка, что функция корректно обрабатывает пустую строку"""
    # Функция должна вернуть пустую строку при получении пустой строки
    result = get_date(invalid_date_strings[0])  # ""
    assert result == ""


def test_mask_account_card_only_name_no_number():
    """Тест когда есть только название без номера"""
    # Передаем только название карты или счета без номера
    result1 = mask_account_card("Счет")
    assert result1 == "Счет"

    result2 = mask_account_card("Visa")
    assert result2 == "Visa"
