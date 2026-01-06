from unittest.mock import Mock, patch

import requests

from src.external_api import convert_to_rub, get_exchange_rate


def test_convert_to_rub_rub() -> None:
    """Тест: транзакция в рублях возвращается без изменений"""
    transaction = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"code": "RUB"}
        }
    }
    result = convert_to_rub(transaction)
    assert result == 100.50


@patch('src.external_api.get_exchange_rate')
def test_convert_to_rub_usd(mock_get_rate: Mock) -> None:
    """Тест: конвертация USD с моком API"""
    # Настраиваем мок: get_exchange_rate возвращает 75.5
    mock_get_rate.return_value = 75.5

    transaction = {
        "operationAmount": {
            "amount": "100.0",
            "currency": {"code": "USD"}
        }
    }
    result = convert_to_rub(transaction)

    # Проверяем: 100.0 × 75.5 = 7550.0
    assert result == 7550.0
    # Проверяем, что функция вызвалась с правильными аргументами
    mock_get_rate.assert_called_once_with("USD", "RUB")


@patch('src.external_api.get_exchange_rate')
def test_convert_to_rub_eur(mock_get_rate: Mock) -> None:
    """Тест: конвертация EUR с моком API"""
    mock_get_rate.return_value = 85.0

    transaction = {
        "operationAmount": {
            "amount": "50.0",
            "currency": {"code": "EUR"}
        }
    }
    result = convert_to_rub(transaction)

    assert result == 4250.0  # 50.0 × 85.0
    mock_get_rate.assert_called_once_with("EUR", "RUB")


def test_convert_to_rub_unknown_currency() -> None:
    """Тест: неизвестная валюта возвращает сумму без конвертации"""
    transaction = {
        "operationAmount": {
            "amount": "200.0",
            "currency": {"code": "GBP"}
        }
    }
    result = convert_to_rub(transaction)
    assert result == 200.0


def test_convert_to_rub_invalid_amount() -> None:
    """Тест: невалидная сумма возвращает 0.0"""
    transaction = {
        "operationAmount": {
            "amount": ["не", "число"],  # Список вызовет TypeError при float()
            "currency": {"code": "USD"}
        }
    }
    result = convert_to_rub(transaction)
    assert result == 0.0


def test_convert_to_rub_no_operation_amount() -> None:
    """Тест: транзакция без operationAmount возвращает 0.0"""
    transaction = {"id": 1}  # Нет operationAmount
    result = convert_to_rub(transaction)
    assert result == 0.0


def test_convert_to_rub_no_currency_code() -> None:
    """Тест: транзакция без currency code возвращает сумму без конвертации"""
    transaction = {
        "operationAmount": {
            "amount": "300.0",
            "currency": {}  # Нет code
        }
    }
    result = convert_to_rub(transaction)
    # currency будет None → попадает в else блок → возвращает 300.0
    assert result == 300.0


@patch('src.external_api.requests.get')
def test_get_exchange_rate_success(mock_get: Mock) -> None:
    """Тест успешного получения курса от API"""
    # Мокируем ответ API
    mock_response = Mock()
    mock_response.json.return_value = {
        "success": True,
        "rates": {"RUB": 75.5}
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    # Патчим переменную окружения
    with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
        rate = get_exchange_rate("USD", "RUB")
        assert rate == 75.5
        mock_get.assert_called_once()


def test_get_exchange_rate_no_api_key() -> None:
    """Тест: отсутствие API-ключа в переменных окружения"""
    with patch.dict('os.environ', {}, clear=True):  # очищаем переменные окружения
        rate = get_exchange_rate("USD", "RUB")
        assert rate == 0.0


@patch('src.external_api.requests.get')
def test_get_exchange_rate_api_error(mock_get: Mock) -> None:
    """Тест: API возвращает ошибку (success: false)"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "success": False,
        "error": {"info": "Invalid API key"}
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
        rate = get_exchange_rate("USD", "RUB")
        assert rate == 0.0


@patch('src.external_api.requests.get')
def test_get_exchange_rate_network_error(mock_get: Mock) -> None:
    """Тест: сетевая ошибка при запросе к API"""
    mock_get.side_effect = requests.exceptions.RequestException("Network error")

    with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
        rate = get_exchange_rate("USD", "RUB")
        assert rate == 0.0


@patch('src.external_api.get_exchange_rate')
def test_convert_to_rub_api_failure(mock_get_rate: Mock) -> None:
    """Тест: API не возвращает курс (rate = 0)"""
    mock_get_rate.return_value = 0.0  # API не сработал

    transaction = {
        "operationAmount": {
            "amount": "100.0",
            "currency": {"code": "USD"}
        }
    }
    result = convert_to_rub(transaction)
    # Должен вернуть исходную сумму, так как rate = 0
    assert result == 100.0


@patch('src.external_api.requests.get')
def test_get_exchange_rate_no_currency_in_response(mock_get: Mock) -> None:
    """Тест: API успешен, но нужной валюты нет в ответе"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "success": True,
        "rates": {"EUR": 0.9}  # Есть EUR, но нет RUB
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    with ((patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}))):
        rate = get_exchange_rate("USD", "RUB")  # Запрашиваем RUB, но его нет
        assert rate == 0.0


@patch('src.external_api.requests.get')
def test_get_exchange_rate_invalid_json_response(mock_get: Mock) -> None:
    """Тест: API возвращает некорректный JSON"""
    mock_response = Mock()
    mock_response.json.side_effect = ValueError("Invalid JSON")  # Имитируем ошибку парсинга
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
        rate = get_exchange_rate("USD", "RUB")
        assert rate == 0.0


@patch('src.external_api.requests.get')
def test_get_exchange_rate_request_params(mock_get: Mock) -> None:
    """Тест: проверяем правильность параметров запроса к API"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "success": True,
        "rates": {"RUB": 75.5}
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
        get_exchange_rate("USD", "RUB")

        # Проверяем, что requests.get вызвана с правильными параметрами
        mock_get.assert_called_once()

        # Получаем аргументы вызова
        call_args = mock_get.call_args
        url = call_args[0][0]  # первый позиционный аргумент
        kwargs = call_args[1]  # именованные аргументы

        # Проверяем URL
        assert url == "https://api.apilayer.com/exchangerates_data/latest"

        # Проверяем params
        assert kwargs['params'] == {"base": "USD", "symbols": "RUB"}

        # Проверяем headers
        assert kwargs['headers'] == {"apikey": "test_key"}

        # Проверяем timeout
        assert kwargs['timeout'] == 10
