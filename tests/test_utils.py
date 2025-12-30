import json
import os
import tempfile
from unittest.mock import Mock, patch

from src.utils import load_transactions


def test_load_transactions_valid_file() -> None:
    """Тест: Загрузка корректного JSON файла"""
    # Создаём временный файл с правильными данными
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump([
            {"id": 1, "amount": "100.0", "currency": "USD"},
            {"id": 2, "amount": "50.0", "currency": "RUB"}
        ], f)
        file_path = f.name

    try:
        # Вызываем нашу функцию
        result = load_transactions(file_path)

        # Проверяем результат
        assert len(result) == 2  # Должно быть 2 транзакции
        assert result[0]["id"] == 1
        assert result[1]["currency"] == "RUB"
    finally:
        # Удаляем временный файл
        os.unlink(file_path)


def test_load_transactions_empty_file() -> None:
    """Тест: Загрузка пустого файла"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        # Просто создаём пустой файл
        file_path = f.name

    try:
        result = load_transactions(file_path)
        assert result == []  # Должен вернуть пустой список
    finally:
        os.unlink(file_path)


def test_load_transactions_not_list() -> None:
    """Тест: Файл содержит не список (а словарь)"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        # JSON словарь, а не список
        json.dump({"not": "a list"}, f)
        file_path = f.name

    try:
        result = load_transactions(file_path)
        assert result == []  # Должен вернуть пустой список
    finally:
        os.unlink(file_path)


def test_load_transactions_nonexistent_file() -> None:
    """Тест: Файл не существует"""
    result = load_transactions("/nonexistent/path/file.json")
    assert result == []  # Должен вернуть пустой список


def test_load_transactions_invalid_json() -> None:
    """Тест: Файл с битым JSON"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        # Неправильный JSON
        f.write("{invalid json")
        file_path = f.name

    try:
        result = load_transactions(file_path)
        assert result == []  # Должен вернуть пустой список
    finally:
        os.unlink(file_path)


@patch('src.utils.os.path.exists')
@patch('src.utils.os.path.getsize')
def test_load_transactions_mocked_simple(mock_getsize: Mock, mock_exists: Mock) -> None:
    """Тест с Mock и patch"""
    # Настраиваем моки
    mock_exists.return_value = True  # файл "существует"
    mock_getsize.return_value = 10  # файл "не пустой" (10 байт)

    # Теперь мокаем open() и json.load()
    with patch('builtins.open'):
        # Настраиваем мок для контекстного менеджера (with open() as f:)

        with patch('src.utils.json.load') as mock_json_load:
            # Говорим json.load() что возвращать
            mock_json_load.return_value = [{"id": 1, "amount": "100.0"}]

            # Вызываем нашу функцию
            result = load_transactions("test.json")

            # Проверяем результат
            assert result == [{"id": 1, "amount": "100.0"}]

            # Проверяем, что моки вызывались с правильными аргументами
            mock_exists.assert_called_once_with("test.json")
            mock_getsize.assert_called_once_with("test.json")
            mock_json_load.assert_called_once()
