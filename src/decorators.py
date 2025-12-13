from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования вызовов функций.

    Аргументы:
        filename: Имя файла для записи логов. Если None - вывод в консоль.

    Возвращает:
        Декоратор для функции
    """

    # Этот декоратор принимает параметр filename,
    # поэтому нужна дополнительная обёртка
    def decorator(func: Callable) -> Callable:
        """Внутренний декоратор, который принимает функцию для обёртки."""

        # Сохраняем имя и документацию оригинальной функции
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обёртка, которая выполняется при каждом вызове функции.

            Здесь происходит:
            1. Логирование вызова функции
            2. Вызов оригинальной функции
            3. Логирование результата или ошибки
            """

            # Получаем имя декорируемой функции
            func_name = func.__name__

            # Формируем строку с аргументами функции
            # Преобразуем все аргументы в строки
            args_list = [str(arg) for arg in args]  # Позиционные аргументы
            kwargs_list = [f"{key}={str(value)}" for key, value in kwargs.items()]  # Именованные аргументы

            # Объединяем все аргументы через запятую
            all_args = ", ".join(args_list + kwargs_list)

            try:
                # Вызываем оригинальную функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                message = f"{func_name} ok\n"

            except Exception as e:
                # Если произошла ошибка, получаем её тип
                error_type = type(e).__name__

                # Формируем сообщение об ошибке
                message = f"{func_name} error: {error_type}. Inputs: ({all_args})\n"

                # Логируем ошибку
                if filename is None:
                    # Вывод в консоль
                    print(message, end='')
                else:
                    # Запись в файл
                    with open(filename, 'a', encoding='utf-8') as file:
                        file.write(message)

                # Пробрасываем исключение дальше
                raise

            # Логируем успешное выполнение
            if filename is None:
                print(message, end='')
            else:
                with open(filename, 'a', encoding='utf-8') as file:
                    file.write(message)

            # Возвращаем результат оригинальной функции
            return result

        return wrapper  # Возвращаем обёрнутую функцию

    return decorator  # Возвращаем декоратор
