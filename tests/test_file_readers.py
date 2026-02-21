import os
import tempfile
from unittest.mock import Mock, patch

from src.file_readers import load_transactions_from_csv, load_transactions_from_excel


def test_csv_loading():
    """Тест загрузки CSV файла."""
    print("=== Тестируем CSV функцию ===")
    csv_result = load_transactions_from_csv("data/transactions.csv")
    print(f"Загружено транзакций: {len(csv_result)}")
    if csv_result:
        print(f"Первая транзакция: {csv_result[0]}")


def test_excel_loading():
    """Тест загрузки Excel файла."""
    print("\n=== Тестируем Excel функцию ===")
    excel_result = load_transactions_from_excel("data/transactions_excel.xlsx")
    print(f"Загружено транзакций: {len(excel_result)}")
    if excel_result:
        print(f"Первая транзакция: {excel_result[0]}")


def test_load_transactions_from_csv_valid_file():
    """Тест: Загрузка корректного CSV файла"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write('id;state;date;amount\n')
        f.write('1;EXECUTED;2023-09-05;100.0\n')
        f.write('2;EXECUTED;2023-09-06;200.0\n')
        file_path = f.name

    try:
        result = load_transactions_from_csv(file_path)
        assert len(result) == 2
        assert result[0]['id'] == 1.0
    finally:
        os.unlink(file_path)


def test_load_transactions_from_csv_empty_file():
    """Тест: Пустой CSV файл"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        file_path = f.name

    try:
        result = load_transactions_from_csv(file_path)
        assert result == []
    finally:
        os.unlink(file_path)


@patch('src.file_readers.os.path.exists')
@patch('src.file_readers.os.path.getsize')
def test_load_transactions_from_csv_mocked(mock_getsize, mock_exists):
    """Тест CSV с Mock и patch"""
    mock_exists.return_value = True
    mock_getsize.return_value = 100

    with patch('src.file_readers.pd.read_csv') as mock_read_csv:
        mock_df = Mock()
        mock_df.to_dict.return_value = [{'id': 1, 'amount': 100.0}]
        mock_read_csv.return_value = mock_df

        result = load_transactions_from_csv('test.csv')
        assert len(result) == 1
        mock_read_csv.assert_called_once_with('test.csv', encoding='utf-8', delimiter=';')


@patch('src.file_readers.os.path.exists')
@patch('src.file_readers.os.path.getsize')
def test_load_transactions_from_excel_mocked(mock_getsize, mock_exists):
    """Тест Excel с Mock и patch"""
    mock_exists.return_value = True
    mock_getsize.return_value = 100

    with patch('src.file_readers.pd.read_excel') as mock_read_excel:
        mock_df = Mock()
        mock_df.to_dict.return_value = [{'id': 1, 'amount': 100.0}]
        mock_read_excel.return_value = mock_df

        result = load_transactions_from_excel('test.xlsx')
        assert len(result) == 1
        mock_read_excel.assert_called_once_with('test.xlsx', engine='openpyxl')


def test_load_transactions_from_excel_valid_file():
    """Тест: Загрузка корректного Excel файла"""
    import pandas as pd

    # Создаем временный Excel файл
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        file_path = f.name

    try:
        # Создаем DataFrame и сохраняем в Excel
        df = pd.DataFrame({
            'id': [1, 2],
            'state': ['EXECUTED', 'EXECUTED'],
            'amount': [100.0, 200.0]
        })
        df.to_excel(file_path, index=False, engine='openpyxl')

        # Вызываем нашу функцию
        result = load_transactions_from_excel(file_path)

        # Проверяем результат
        assert len(result) == 2
        assert result[0]['id'] == 1
    finally:
        os.unlink(file_path)


def test_load_transactions_from_excel_empty_file():
    """Тест: Пустой Excel файл"""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        file_path = f.name

    try:
        result = load_transactions_from_excel(file_path)
        assert result == []
    finally:
        os.unlink(file_path)


def test_load_transactions_from_csv_file_not_found():
    """Тест: CSV файл не существует"""
    result = load_transactions_from_csv("/несуществующий/путь/file.csv")
    assert result == []


def test_load_transactions_from_excel_file_not_found():
    """Тест: Excel файл не существует"""
    result = load_transactions_from_excel("/несуществующий/путь/file.xlsx")
    assert result == []


def test_load_transactions_from_csv_empty_data_error():
    """Тест: CSV файл пуст (EmptyDataError)"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        # Создаем пустой CSV файл (только заголовки)
        f.write('id;state;date;amount\n')
        file_path = f.name

    try:
        result = load_transactions_from_csv(file_path)
        assert result == []
    finally:
        os.unlink(file_path)


def test_load_transactions_from_csv_general_exception():
    """Тест: Общая ошибка при чтении CSV"""
    with patch('src.file_readers.pd.read_csv') as mock_read_csv:
        mock_read_csv.side_effect = Exception("Test error")

        result = load_transactions_from_csv("test.csv")
        assert result == []


def test_load_transactions_from_excel_empty_data_error():
    """Тест: Excel файл пуст (EmptyDataError)"""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        file_path = f.name

    try:
        # Создаем пустой Excel файл
        import pandas as pd
        df = pd.DataFrame()  # Пустой DataFrame
        df.to_excel(file_path, index=False, engine='openpyxl')

        result = load_transactions_from_excel(file_path)
        assert result == []
    finally:
        os.unlink(file_path)


def test_load_transactions_from_excel_general_exception():
    """Тест: Общая ошибка при чтении Excel"""
    with patch('src.file_readers.pd.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = Exception("Test error")

        result = load_transactions_from_excel("test.xlsx")
        assert result == []


def test_load_transactions_from_excel_corrupted_file():
    """Тест: Поврежденный Excel файл."""
    # Создаем временный файл с расширением .xlsx, но не Excel формат
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False) as f:
        # Пишем случайные байты (не Excel файл)
        f.write(b'Random bytes, not an Excel file')
        file_path = f.name

    try:
        # Вызываем функцию - должна вернуть пустой список при ошибке
        result = load_transactions_from_excel(file_path)
        assert result == []
    finally:
        # Удаляем временный файл
        os.unlink(file_path)


def test_load_transactions_from_csv_read_exception():
    """Тест: Ошибка в pd.read_csv (после проверок)"""
    # Создаем реальный файл, чтобы пройти проверки os.path.exists и getsize
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write('id;state\n')
        f.write('1;EXECUTED\n')
        file_path = f.name

    try:
        # Мокаем только pd.read_csv, чтобы он упал
        with patch('src.file_readers.pd.read_csv') as mock_read_csv:
            mock_read_csv.side_effect = Exception("Read error in pandas")

            result = load_transactions_from_csv(file_path)
            assert result == []
    finally:
        os.unlink(file_path)


def test_load_transactions_from_excel_read_exception():
    """Тест: Ошибка в pd.read_excel (после проверок)"""
    # Создаем реальный файл
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        import pandas as pd
        df = pd.DataFrame({'id': [1]})
        df.to_excel(f.name, index=False, engine='openpyxl')
        file_path = f.name

    try:
        with patch('src.file_readers.pd.read_excel') as mock_read_excel:
            mock_read_excel.side_effect = Exception("Read error in pandas")

            result = load_transactions_from_excel(file_path)
            assert result == []
    finally:
        os.unlink(file_path)


def test_load_transactions_from_csv_empty_data_error_via_mock():
    """Тест: EmptyDataError через mock для CSV"""
    import pandas as pd  # ← ДОБАВЬ ЭТУ СТРОКУ

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write('something\n')
        file_path = f.name

    try:
        with patch('src.file_readers.pd.read_csv') as mock_read_csv:
            mock_read_csv.side_effect = pd.errors.EmptyDataError("No columns to parse")
            result = load_transactions_from_csv(file_path)
            assert result == []
    finally:
        os.unlink(file_path)


def test_load_transactions_from_excel_empty_data_error_via_mock():
    """Тест: EmptyDataError через mock для Excel."""
    import pandas as pd

    # Создаем временный файл с данными (не пустой)
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False) as f:
        f.write(b'test data')  # Записываем данные чтобы файл не был пустым
        file_path = f.name

    try:
        # Мокаем pd.read_excel чтобы вызвать EmptyDataError
        with patch('src.file_readers.pd.read_excel') as mock_read_excel:
            mock_read_excel.side_effect = pd.errors.EmptyDataError("No columns to parse")

            # Вызываем функцию - должна вернуть пустой список
            result = load_transactions_from_excel(file_path)
            assert result == []
    finally:
        # Удаляем временный файл
        os.unlink(file_path)
