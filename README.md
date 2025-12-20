# Transaction Management System

## Описание

Transaction Management System - это Python-библиотека для 
обработки банковских операций. Пользователи могут маскировать 
номера карт и счетов, фильтровать операции по статусу, а также 
сортировать транзакции по дате.

## Установка

1. Клонируйте репозиторий:
```
git clone https://github.com/natshakht-jpg/transaction_management_system.git
```

2. Установите зависимости:
```
poetry install 
```

3. Активируйте виртуальное окружение:
```
poetry shell
```

## Использование

1. Импортируйте нужные функции в вашем Python-коде
2. Используйте функции маскировки для защиты данных карт и счетов
3. Применяйте фильтрацию и сортировку для анализа банковских операций

### Примеры использования
```python
from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date

# Маскировка данных
card_mask = get_mask_card_number("7000792289606361")  # "7000 79** **** 6361"
account_mask = get_mask_account("73654108430135874305")  # "**4305"

# Обработка транзакций
formatted_card = mask_account_card("Visa Platinum 7000792289606361") # "Visa Platinum 7000 79** **** 6361"
formatted_date = get_date("2024-03-11T02:26:18.671407") # "11.03.2024"

# Фильтрация и сортировка
operations = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2024-01-01'},
    {'id': 2, 'state': 'CANCELED', 'date': '2024-01-02'}
]

filtered_operations = filter_by_state(operations, 'EXECUTED')
sorted_operations = sort_by_date(operations)
```

## Модуль генераторов

Новый модуль `src/generators.py` содержит функции для работы с банковскими транзакциями.

### Примеры использования:

```python
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

# Пример данных транзакций (для демонстрации)
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }
]

# 1. Фильтрация транзакций по валюте
usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(f"ID: {transaction['id']}, Сумма: {transaction['operationAmount']['amount']}")

# 2. Получение описаний транзакций
descriptions = transaction_descriptions(transactions)
for description in descriptions:
    print(description)

# 3. Генерация номеров карт
card_numbers = card_number_generator(1, 5)
for card in card_numbers:
    print(card)
# Вывод:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
```

### Пример входных данных (полный список для тестирования):

```python
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {"name": "руб.", "code": "RUB"}
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160"
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229"
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {
            "amount": "67314.70",
            "currency": {"name": "руб.", "code": "RUB"}
        },
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657"
    }
]
```

## Тестирование
Проект покрыт комплексными тестами с использованием pytest. Для запуска тестов:
```bash
# Запуск всех тестов
pytest

# Запуск с покрытием
pytest --cov=src --cov-report=term-missing

# Генерация HTML отчета
pytest --cov=src --cov-report=html
```
**Покрытие тестами:** 100%
**Количество тестов:** 52

## Документация
Дополнительную информацию о структуре проекта и функциях можно найти в [документации Python](https://docs.python.org/3/).

## Лицензия
Проект распространяется под лицензией MIT.
