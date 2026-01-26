"""
Основной модуль программы работы с банковскими транзакциями.
Содержит функцию main() с пользовательским интерфейсом.
"""

import sys
from typing import NoReturn

from src.bank_operations import process_bank_operations, process_bank_search
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions
from src.widget import get_date, mask_account_card


def get_valid_status() -> str:
    """Запрашивает у пользователя статус операций с проверкой.

    Returns:
        Статус в нижнем регистре (executed/canceled/pending)
    """
    valid_statuses = ["executed", "canceled", "pending"]

    print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    while True:
        status = input("Статус: ").strip()
        normalized = status.lower()

        if normalized in valid_statuses:
            print(f"Операции отфильтрованы по статусу '{status.upper()}'")
            return normalized

        print(f"Статус операции '{status}' недоступен.")


def get_yes_no(question: str) -> bool:
    """Запрашивает ответ Да/Нет с проверкой.

    Args:
        question: Вопрос для пользователя

    Returns:
        True если Да, False если Нет
    """
    while True:
        answer = input(f"{question} (Да/Нет): ").strip().lower()
        if answer in ["да", "д", "yes", "y"]:
            return True
        if answer in ["нет", "н", "no", "n"]:
            return False
        print("Пожалуйста, ответьте 'Да' или 'Нет'")


def display_transaction(transaction: dict) -> None:
    """Выводит одну транзакцию в формате из задания."""
    date = get_date(transaction.get("date", ""))
    description = transaction.get("description", "")

    # Маскировка номеров (упрощенно)
    from_account = mask_account_card(transaction.get("from", "")) if transaction.get("from") else ""
    to_account = mask_account_card(transaction.get("to", "")) if transaction.get("to") else ""

    amount = transaction.get("operationAmount", {}).get("amount", "")
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("name", "")

    print(f"\n{date} {description}")
    if from_account:
        print(f"{from_account} -> {to_account}" if to_account else from_account)
    elif to_account:
        print(f"Счет {to_account}")

    if amount and currency:
        print(f"Сумма: {amount} {currency}")


def main() -> NoReturn:
    """Основная функция с пользовательским интерфейсом."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор файла
    while True:
        choice = input("\nВведите номер пункта: ").strip()
        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            file_path = "data/operations.json"
            break
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            file_path = "data/operations.csv"
            break
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            file_path = "data/operations.xlsx"
            break
        else:
            print("Некорректный выбор. Введите 1, 2 или 3.")

    # Загрузка данных
    try:
        transactions = load_transactions(file_path)
        print(f"Загружено {len(transactions)} транзакций")
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        print("Используются демонстрационные данные.")
        transactions = [
            {
                "date": "2019-12-08T22:46:21.935582",
                "description": "Открытие вклада",
                "from": "Счет 90424923579946435907",
                "to": "Счет 43241152692663622869",
                "operationAmount": {"amount": "40542", "currency": {"name": "руб."}},
                "state": "EXECUTED"
            },
            # ... другие демо-транзакции
        ]

    # Фильтрация по статусу
    status = get_valid_status()
    filtered_transactions = filter_by_state(transactions, status.upper())

    if not filtered_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        sys.exit(0)

    # Сортировка по дате
    if get_yes_no("\nОтсортировать операции по дате?"):
        if get_yes_no("Отсортировать по возрастанию или по убыванию?"):
            filtered_transactions = sort_by_date(filtered_transactions, reverse=False)
            print("Отсортировано по возрастанию")
        else:
            filtered_transactions = sort_by_date(filtered_transactions, reverse=True)
            print("Отсортировано по убыванию")

    # Рублевые транзакции
    if get_yes_no("\nВыводить только рублевые транзакции?"):
        filtered_transactions = [
            t for t in filtered_transactions
            if t.get("operationAmount", {}).get("currency", {}).get("name") == "руб."
        ]
        print("Отфильтрованы рублевые транзакции")

    # Поиск по описанию
    if get_yes_no("\nОтфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            filtered_transactions = process_bank_search(filtered_transactions, search_word)
            print(f"Применен поиск по слову '{search_word}'")

    # Подсчет по категориям (демонстрация второй функции)
    if filtered_transactions:
        categories = list(set(t.get("description", "") for t in filtered_transactions if t.get("description")))
        if categories:
            counts = process_bank_operations(filtered_transactions, categories)
            print("\nСтатистика по категориям:")
            for category, count in counts.items():
                print(f"  {category}: {count}")

    # Вывод результата
    print("\nРаспечатываю итоговый список транзакций...")
    print("=" * 50)

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
        for transaction in filtered_transactions:
            display_transaction(transaction)

    sys.exit(0)


if __name__ == "__main__":
    main()
