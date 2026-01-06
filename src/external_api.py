import os
from typing import Any, Dict, Optional  # noqa: F401

import requests
from dotenv import load_dotenv


# Загружаем переменные окружения из .env файла
load_dotenv()


def get_exchange_rate(from_currency: str, to_currency: str = "RUB") -> float:
    """
    Получает текущий курс валюты к рублям через внешнее API.

    Args:
        from_currency: Исходная валюта (например, "USD")
        to_currency: Целевая валюта (по умолчанию "RUB")

    Returns:
        Курс обмена (float) или 0.0 в случае ошибки
    """
    # Получаем API-ключ из переменных окружения
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")

    if not api_key:
        print("Ошибка: не найден EXCHANGE_RATE_API_KEY в .env файле")
        return 0.0

    # Формируем URL для запроса
    url = "https://api.apilayer.com/exchangerates_data/latest"

    # Параметры запроса
    params = {
        "base": from_currency,  # валюта, которую конвертируем
        "symbols": to_currency  # в какую валюту конвертируем
    }

    # Заголовки запроса (API-ключ)
    headers = {
        "apikey": api_key
    }

    try:
        # Делаем запрос к API
        response = requests.get(url, params=params, headers=headers, timeout=10)

        # Проверяем статус ответа
        response.raise_for_status()

        # Парсим JSON-ответ
        data = response.json()

        # Проверяем успешность запроса в данных API
        if data.get("success") and to_currency in data.get("rates", {}):
            rate = data["rates"][to_currency]
            rate_float = float(rate)  # ← Явное преобразование в float
            print(f"ОТЛАДКА: Курс {from_currency} -> {to_currency} = {rate_float}")
            return rate_float
        else:
            print(f"Ошибка API: {data.get('error', {}).get('info', 'Неизвестная ошибка')}")
            return 0.0

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return 0.0
    except (KeyError, ValueError) as e:
        print(f"Ошибка при обработке ответа API: {e}")
        return 0.0


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Принимает словарь транзакции с ключами 'amount' и 'currency'.
    Возвращает сумму в рублях (float).
    """
    # 1. Извлекаем данные из транзакции
    operation_amount = transaction.get("operationAmount", {})
    if not operation_amount:
        return 0.0

    amount = operation_amount.get("amount")
    currency_info = operation_amount.get("currency", {})
    currency = currency_info.get("code")

    # Отладка: печатаем что получили
    print(f"ОТЛАДКА: сумма={amount}, валюта={currency}")

    # 2. Проверяем, что amount не None, и преобразуем в дробное число
    if amount is None:
        return 0.0  # pragma: no cover

    try:
        amount_float = float(amount)
    except (ValueError, TypeError):
        # Если не получается преобразовать (например, amount="не число")
        return 0.0  # pragma: no cover

    # 3. Проверяем валюту
    if currency == "RUB":
        return amount_float

    elif currency in ["USD", "EUR"]:
        # Получаем реальный курс от API
        rate = get_exchange_rate(currency, "RUB")
        if rate > 0:
            return amount_float * rate
        else:
            print(f"Не удалось получить курс {currency}. Возвращаем сумму без конвертации.")
            return amount_float

    else:
        print(f"Внимание: неизвестная валюта '{currency}'. Возвращаем сумму без конвертации.")
        return amount_float
