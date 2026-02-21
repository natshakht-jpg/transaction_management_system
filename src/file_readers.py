"""Модуль для чтения финансовых операций из разных форматов файлов."""


import logging  # Импорт для логирования
import os  # Импорт для проверки файлов
from typing import Any, Dict, List  # Импорт для типизации

import pandas as pd  # Импорт для работы с CSV/Excel


# Логер для модуля file_readers
logger = logging.getLogger(__name__)


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из CSV-файла.

    Принимает:
        file_path: Путь до CSV-файла с транзакциями

    Возвращает:
        List[Dict]: Список словарей с данными о финансовых транзакциях.
    """

    # 1. Проверяем, существует ли файл по указанному пути
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    # 2. Проверяем, что файл не пустой (0 байт)
    if os.path.getsize(file_path) == 0:
        logger.error(f"Файл пустой: {file_path}")
        return []

    try:
        # Читаем CSV файл с кодировкой UTF-8 и разделителем ';'
        df = pd.read_csv(file_path, encoding='utf-8', delimiter=';')
        # Преобразуем DataFrame в список словарей, где каждая строка = один словарь
        transactions: List[Dict[str, Any]] = df.to_dict(orient='records')
        # Записываем в лог информацию об успешной загрузке
        logger.info(f"Успешно загружено {len(transactions)} транзакций из {file_path}")
        return transactions
    except pd.errors.EmptyDataError:
        # Ошибка возникает, если CSV файл пустой или в нем только заголовки
        logger.error(f"CSV файл пуст или содержит только заголовки: {file_path}")
        return []
    except Exception as e:
        error_msg = f"Ошибка при чтении CSV файла {file_path}: {e}"
        logger.error(error_msg)
        return []


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из Excel-файла."""

    # 1. Проверяем, существует ли файл по указанному пути
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    # 2. Проверяем, что файл не пустой (0 байт)
    if os.path.getsize(file_path) == 0:
        logger.error(f"Файл пустой: {file_path}")
        return []

    try:
        # Читаем Excel файл
        df = pd.read_excel(file_path, engine='openpyxl')
        # Преобразуем DataFrame в список словарей, где каждая строка = один словарь
        transactions: List[Dict[str, Any]] = df.to_dict(orient='records')
        # Записываем в лог информацию об успешной загрузке
        logger.info(f"Успешно загружено {len(transactions)} транзакций из {file_path}")
        return transactions
    except pd.errors.EmptyDataError:
        logger.error(f"Excel файл пуст или содержит только заголовки: {file_path}")
        return []
    except Exception as e:
        error_msg = f"Ошибка при чтении Excel файла {file_path}: {e}"
        logger.error(error_msg)
        return []
