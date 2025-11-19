# Импортируем функции маскировки из модуля masks
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> str:
    """Функция обрабатывает информацию о картах и счетах и
    возвращает строку с замаскированным номером"""
    parts = data.split()
    # Разбиваем входную строку на список слов по пробелам
    if parts[0] == "Счет":
        # Проверяем, является ли первый элемент словом "Счет"
        return "Счет " + get_mask_account(int(parts[1]))
        # Для счета возвращаем "Счет" + маскированный номер
    else:
        card_name = ' '.join(parts[:-1])
        # Объединяем все элементы, кроме последнего, в название карты
        card_number = parts[-1]
        # Берем последний элемент как номер карты
        masked_number = get_mask_card_number(int(card_number))
        # Маскируем номер карты
        return card_name + " " + masked_number
        # Возвращаем название карты + пробел + замаскированный номер


def get_date(date_string: str) -> str:
    """Функция преобразует дату из формата '2024-03-11T02:26:18.671407'
    в формат '11.03.2024'"""
    date_parts = date_string.split("T")
    # Разделяем строку на дату и время по символу 'T'
    date_components = date_parts[0].split("-")
    # Разбиваем дату на компоненты: год, месяц, день
    return date_components[2] + "." + date_components[1] + "." + date_components[0]
    # Возвращаем дату в формате ДД.ММ.ГГГГ
