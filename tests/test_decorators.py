import pytest
import os

from src.decorators import log


def test_log_to_console_success(capsys):
    """Тестируем логирование успешного выполнения в консоль."""

    @log()
    def add(a, b):
        return a + b

    result = add(3, 5)
    assert result == 8

    captured = capsys.readouterr()
    assert captured.out == "add ok\n"


def test_log_to_console_error(capsys):
    """Тестируем логирование ошибки в консоль."""

    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0)" in captured.out


def test_log_to_file_success():
    """Тестируем логирование успешного выполнения в файл."""

    if os.path.exists("test_log.txt"):
        os.remove("test_log.txt")

    @log(filename="test_log.txt")
    def multiply(x, y):
        return x * y

    result = multiply(4, 6)
    assert result == 24

    with open("test_log.txt", "r") as f:
        content = f.read()
        assert content == "multiply ok\n"

    os.remove("test_log.txt")


def test_log_to_file_error():
    """Тестируем логирование ошибки в файл."""

    if os.path.exists("test_error.txt"):
        os.remove("test_error.txt")

    @log(filename="test_error.txt")
    def power(a, b):
        return a ** b

    with pytest.raises(TypeError):
        power("abc", "def")

    with open("test_error.txt", "r") as f:
        content = f.read()
        assert "power error: TypeError" in content
        assert "Inputs: (abc, def)" in content

    os.remove("test_error.txt")


def test_log_with_different_arguments(capsys):
    """Тестируем логирование функции с разными типами аргументов."""

    @log()
    def process_data(name, count=1, enabled=True):
        return f"{name} * {count}"

    result = process_data("test", 3, enabled=False)
    captured = capsys.readouterr()
    assert "process_data ok\n" == captured.out


def test_function_metadata_preserved():
    """Проверяем, что декоратор сохраняет имя и документацию функции."""

    @log()
    def example_function(x, y):
        """Это тестовая функция."""
        return x + y

    assert example_function.__name__ == "example_function"
    assert example_function.__doc__ == "Это тестовая функция."
