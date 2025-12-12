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
**Количество тестов:** 37

## Документация
Дополнительную информацию о структуре проекта и функциях можно найти в [документации Python](https://docs.python.org/3/).

## Лицензия
Проект распространяется под лицензией MIT.
